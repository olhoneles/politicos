# -*- coding: utf-8 -*-
#
# Copyright (c) 2015, Marcelo Jorge Vieira <metal@alucinados.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import csv
import logging
import multiprocessing
import os
import re
from datetime import datetime

from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.text import slugify

from politicians.management.commands._tse import TSE
from politicians.models import (
    PoliticalParty, Institution, PoliticalOffice, Politician,
    Mandate, Ethnicity, Education, PoliticianAlternativeName,
    PoliticianEventType, PoliticianEvent, PoliticianPoliticalParty,
    Candidacy, Election, CandidacyStatus, City, State, MaritalStatus,
    Nationality, Occupation
)


def call_it(instance, name, args=(), kwargs=None):
    if kwargs is None:
        kwargs = {}
    return getattr(instance, name)(*args, **kwargs)


class Base(object):

    @classmethod
    def set_options(cls, *args, **kwargs):
        if kwargs.get('log-level', '').lower() == 'debug':
            log_level = logging.DEBUG
        elif kwargs.get('log-level', '').lower() == 'info':
            log_level = logging.INFO
        else:
            log_level = logging.ERROR

        cls.logger = logging.getLogger('politicos_command')
        cls.logger.setLevel(log_level)

    # Inspired by http://miud.in/1H8y
    @classmethod
    def title_except(cls, s, exceptions=['do', 'de', 'da', 'dos', 'a', 'e']):
        word_list = re.split(' ', s.lower())  # re.split behaves as expected
        final = [word_list[0].title()]
        for word in word_list[1:]:
            final.append(word in exceptions and word or word.title())
        return ' '.join(final)

    @classmethod
    def create_siglum(cls, s):
        exceptions = ['do', 'dos', 'de', 'da', 'das', 'a', 'e']
        word_list = slugify(s).split('-')
        final = [word_list[0].title()[:1]]
        for w in word_list[1:]:
            final.append(w not in exceptions and w.title()[:1] or '')
        return ''.join(final)

    @classmethod
    def get_urls_in_text(cls, text):
        urls = re.finditer(
            r'(([a-z]{3,6}:\/\/)|(^|\s))([a-zA-Z0-9\-]+\.)+[a-z]{2,13}(?:\/[a-zA-Z0-9]{1,})*',  # noqa
            text
        )
        return [x.group(0).strip() for x in urls]

    @classmethod
    def get_emails_in_text(cls, text):
        emails = re.findall(r'[\w\.-]+@[\w\.-]+', text)
        return emails if emails else None


class PoliticosCommand(BaseCommand, Base):

    def add_arguments(self, parser):
        parser.add_argument(
            '--log-level',
            dest='log-level',
            default='error',
            help='Debugger level'
        )

    def process_tse_data_by_year(self, politicos_class, year):
        tse = TSE(year)
        tse.download_and_extract()
        politicos_class.process_tse_files(tse, year)
        tse.remove_tmp_dir()

    @classmethod
    def raise_error(cls, text):
        cls.logger.error(text)
        raise


class Politicos(Base):

    @classmethod
    def raise_error(cls, text):
        cls.logger.error(text)
        raise

    @classmethod
    def get_picture(cls, *args, **kwargs):
        raise NotImplementedError('Subclasses should implement this!')

    @classmethod
    def convert_to_dict(cls, *args, **kwargs):
        raise NotImplementedError('Subclasses should implement this!')

    @classmethod
    def formatter(cls, text):
        try:
            return cls.title_except(text.decode('latin1')).strip()
        except Exception:
            return cls.title_except(text).strip()

    @classmethod
    def add_city(cls, item):
        if item.get('state_siglum') == 'BR':
            return None

        state = State.objects.cache().get(siglum=item.get('state_siglum'))

        city = None
        if item.get('city_name'):
            city, city_created = City.objects.cache().get_or_create(
                name=item.get('city_name'), state=state
            )
            if city_created:
                cls.logger.debug(
                    'Added City: %s (%s)', str(city), str(city.state)
                )

        return city

    @classmethod
    def add_institution_vereador(cls, item):
        city = cls.add_city(item)
        institution, created = Institution.objects.cache().get_or_create(
            name=u'Camara Municipal {0}'.format(city.name),
            siglum='CM{0}'.format(cls.create_siglum(city.name)),
            state=city.state,
        )
        if created:
            po = PoliticalOffice.get_by_name('Vereador')
            institution.political_offices.add(po)
            cls.logger.debug(
                'Addd Institution: "{0}"'.format(str(institution))
            )
        return institution

    @classmethod
    def add_institution_prefeito(cls, item):
        city = cls.add_city(item)
        institution, created = Institution.objects.cache().get_or_create(
            name=u'Prefeitura Municipal {}'.format(city.name),
            siglum='PM{0}'.format(cls.create_siglum(city.name)),
            state=city.state,
        )
        if created:
            po1 = PoliticalOffice.get_by_name('Prefeito')
            po2 = PoliticalOffice.get_by_name('Vice-Prefeito')
            institution.political_offices.add(po1, po2)
            cls.logger.debug(
                'Added Institution: "{0}"'.format(str(institution))
            )
        return institution

    @classmethod
    def process_tse_files(cls, tse, year):
        try:
            election = Election.objects.cache().get_or_create(year=year)
        except Election.DoesNotExist:
            cls.raise_error('Election not found: {0}'.format(year))

        states = [(x.siglum, x.name) for x in State.objects.all()]
        states = ((u'BR', u'Brasil'),) + tuple(states)

        if settings.TSE_CONCURRENCY <= 1:
            for state in states:
                cls.process_tse_file(tse, year, state, election)
            return

        pool = multiprocessing.Pool(processes=settings.TSE_CONCURRENCY)
        async_results = [
            pool.apply_async(
                call_it,
                args=(cls, 'process_tse_file', (tse, year, state, election))
            ) for state in states
        ]
        pool.close()
        map(multiprocessing.pool.ApplyResult.wait, async_results)

    @classmethod
    def process_tse_file(cls, tse, year, state, election):
        """
        The MySQL protocol can not handle multiple threads using the same
        connection at once. If you close the database connection, Django will
        open a new one the next time it needs it.
        """
        from django.db import connection
        connection.close()

        state_siglum, state_name = state
        file_name = '{0}/consulta_cand_{1}_{2}.txt'.format(
            tse.temp_dir, year, state_siglum
        )
        if not os.path.exists(file_name):
            cls.logger.error('File "%s" not found', file_name)
            return

        cls.logger.info(
            'Starting %s (%s) at %s',
            state_siglum, year, datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        with open(file_name, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for line in reader:
                item = cls.convert_to_dict(line, state_siglum)
                cls.process_tse_items(item, election)

        cls.logger.info(
            'Finished %s (%s) at %s',
            state_siglum, year, datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

    @classmethod
    def add_politician_status(cls, candidacy, item, election_round, po):

        status_aux = 'Eleito'
        status = item.get('status').lower()
        if u'eleito' not in status or u'não' in status:
            status_aux = 'Não Eleito'
        event_type, _ = PoliticianEventType.objects.cache().get_or_create(
            name=status_aux
        )
        politician_event = PoliticianEvent(
            politician=candidacy.politician,
            politician_event_type=event_type,
            date=election_round.date,
            description=status,
        )
        politician_event.save()

        if status_aux == 'Eleito':
            mandate = Mandate(
                candidacy=candidacy,
                date_start=election_round.date,
                date_end=None
            )
            mandate.save()
            cls.logger.debug('Added Mandate: %s', str(mandate))

    @classmethod
    def add_candidacy(cls, politician, election, item):
        election_round = election.rounds.get(
            round_number=item.get('election_round_number')
        )

        # FIXME
        elected = True
        elected_aux = item.get('status').lower()
        if u'eleito' not in elected_aux or u'não' in elected_aux:
            elected = False

        candidacy_status, _ = CandidacyStatus.objects.cache().get_or_create(
            name=item.get('candidacy_status')
        )

        political_party = cls.get_political_party(
            item.get('political_party_siglum')
        )

        political_office = cls.add_political_office(item)

        institution = cls.add_institution(item, political_office)

        if item.get('state_siglum') == 'BR':
            state = None
        else:
            state = State.objects.cache().get(siglum=item.get('state_siglum'))

        city = cls.add_city(item)

        candidacy, created = Candidacy.objects.get_or_create(
            politician=politician,
            political_party=political_party,
            election_round=election_round,
            elected=elected,
            state=state,
            city=city,
            political_office=political_office,
            candidacy_status=candidacy_status,
            institution=institution,
        )
        if created:
            cls.logger.debug(
                'Added Candidacy: %s', str(candidacy.election_round)
            )

            cls.add_politician_status(
                candidacy, item, election_round, political_office
            )

        return candidacy, created

    @classmethod
    def add_politician(cls, item):
        email = None
        if item.get('emails'):
            email = cls.formatter(item.get('emails')[0]).lower()

        ethnicity = None
        if item.get('ethnicity'):
            ethnicity, _ = Ethnicity.objects.cache().get_or_create(
                name=item.get('ethnicity')
            )

        education, _ = Education.objects.cache().get_or_create(
            name=item.get('education')
        )

        nationality, _ = Nationality.objects.cache().get_or_create(
            name=item.get('nationality')
        )

        marital_status, _ = MaritalStatus.objects.cache().get_or_create(
            name=item.get('marital_status')
        )

        try:
            occupation_slug = slugify(item.get('occupation'))
            occupation = Occupation.objects.cache().get(slug=occupation_slug)
        except Occupation.DoesNotExist:
            occupation = Occupation(name=item.get('occupation'))
            occupation.save()
            cls.logger.debug('Added Occupation: %s', str(occupation))

        try:
            state = State.objects.cache().get(
                siglum=item.get('state_of_birth')
            )
        except State.DoesNotExist:
            state = None
        place_of_birth = item.get('place_of_birth')

        try:
            politician = Politician(
                name=item.get('name'),
                cpf=item.get('cpf'),
                picture=item.get('picture'),
                gender=item.get('gender')[:1],
                date_of_birth=item.get('date_of_birth'),
                marital_status=marital_status,
                nationality=nationality,
                place_of_birth=place_of_birth,
                state=state,
                email=email,
                education=education,
                ethnicity=ethnicity,
                occupation=occupation,
            )
            politician.save()
            cls.logger.debug('Added Politician: %s', str(politician))
        except Exception as e:
            cls.logger.error('On save Politician. Details: %s', str(e))
            return None

        try:
            lan, _ = PoliticianAlternativeName.objects.get_or_create(
                name=item.get('alternative_name')
            )
            politician.alternative_names.add(lan)
            politician.save()
            cls.logger.debug('Added Politician Alternative Name: %s', str(lan))
        except Exception as e:
            cls.logger.error('On save Alternative Name. Details: %s', str(e))

        return politician

    @classmethod
    def add_political_office(cls, item):
        political_office = item.get('political_office')
        if item.get('political_office_cod') == '9':
            political_office = u'Senador 1º Suplente'
        elif item.get('political_office_cod') == '10':
            political_office = u'Senador 2º Suplente'
        else:
            political_office = item.get('political_office')

        po = PoliticalOffice.get_by_name(political_office)
        if not po:
            cls.raise_error(
                'Political Office not found: {0}'.format(political_office)
            )
        return po

    @classmethod
    def add_institution(cls, item, political_office):
        if item.get('political_office_cod') == '13':
            institution = cls.add_institution_vereador(item)
        elif item.get('political_office_cod') in ['11', '12']:
            institution = cls.add_institution_prefeito(item)
        else:
            cods = ['1', '2', '5', '6', '9', '10']
            if item.get('political_office_cod') in cods:
                state = None
            else:
                siglum = item.get('state_siglum')
                state = State.objects.cache().get(siglum=siglum)

            institution = Institution.get_by_political_office_name_and_state(
                name=political_office.name,
                state=state
            )
        return institution

    @classmethod
    def get_political_party(cls, siglum):
        pp_siglum = siglum.replace(' ', '')
        return PoliticalParty.get_by_siglum(pp_siglum)

    @classmethod
    def add_politician_political_party(cls, item, politician, election):
        political_party = cls.get_political_party(
            item.get('political_party_siglum')
        )
        if not political_party:
            cls.logger.error(
                'Political Party not found: %s (%s)',
                item.get('political_party_name'),
                item.get('political_party_siglum')
            )
            return

        pp, created = PoliticianPoliticalParty.objects.cache().get_or_create(
            politician=politician, political_party=political_party
        )

        if created or not pp.date_start or election.year < pp.date_start.year:
            date = '01/01/{0}'.format(election.year)
            pp.date_start = datetime.strptime(date, '%d/%M/%Y')
            pp.save()

            if created:
                msg = 'Added Politician Political Party: %s'
            else:
                msg = 'Updated date of Politician Political Party: %s'

            cls.logger.debug(msg, str(pp))

    @classmethod
    def process_tse_items(cls, item, election):
        if not item:
            cls.logger.error('Empty item for election: %s', str(election))
            return

        try:
            politician = Politician.objects.get(cpf=item.get('cpf'))
            cls.logger.debug('Politician already exist: %s', str(politician))
        except Politician.DoesNotExist:
            politician = None

        if politician:
            if not politician.picture and item.get('picture'):
                politician.picture = item.get('picture')
                politician.save()
        else:
            politician = cls.add_politician(item)

        if politician:
            cls.add_politician_political_party(item, politician, election)
            cls.add_candidacy(politician, election, item)
