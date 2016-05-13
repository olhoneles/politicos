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

import re

import requests
import lxml.html

from politicians.management.commands._base import PoliticosCommand
from politicians.models import Institution, PoliticalOffice, State


# FIXME: Verify CPF
# http://postgresqlbr.blogspot.com.br/2008/06/validao-de-cpf-com-pl-pgsql.html


class Command(PoliticosCommand):

    def formatter(self, name):
        return name.text_content().replace('\n', '').strip()

    def get_logo(self, url):
        response = requests.get(url)
        if response.status_code != 200:
            self.logger.error('Error on get institution url')
            return
        data = lxml.html.fromstring(response.content)
        imgs = data.cssselect('table.infobox_v2 tr img')
        if not imgs:
            imgs = data.cssselect('table.infobox tr img')
        if not imgs:
            self.logger.error('Error on get institution logo')
            return
        logo = imgs[0].get('src')
        self.logger.info('Get institution logo')
        return logo

    def add_governador(self):
        domain = 'https://pt.wikipedia.org'
        url = '{}/wiki/Unidades_federativas_do_Brasil'.format(domain)
        response = requests.get(url)
        if response.status_code != 200:
            self.raise_error('Error on get "Unidades federativas do Brasil"')

        data = lxml.html.fromstring(response.content)
        trs = data.cssselect('table.wikitable tr')
        trs.pop(0)
        for row in trs:
            try:
                logo, name, state_siglum = row.getchildren()[:3]
                state_siglum = self.formatter(state_siglum).upper()
                state = State.objects.cache().get(siglum=state_siglum)

                logo = logo.find('a').find('img').get('src')
                wikipedia = '{}{}'.format(domain, name.find('a').get('href'))
                siglum = 'G{}'.format(state.siglum)
                website = 'http://www.{}.gov.br'.format(state.siglum.lower())
                name = self.formatter(name)

                institution = Institution(
                    name=name,
                    siglum=siglum,
                    logo=logo,
                    state=state,
                    website=website,
                    wikipedia=wikipedia,
                )
                institution.save()

                po1 = PoliticalOffice.get_by_name('Governador')
                po2 = PoliticalOffice.get_by_name('Vice-Governador')
                institution.political_offices.add(po1, po2)

                self.logger.info('Added institution: "%s"', name)
            except Exception as e:
                self.logger.error('Error when add institution: %s', e)

    def add_assembleias_legislativas(self):
        domain = 'https://pt.wikipedia.org'
        url = '{}/wiki/Assembleia_legislativa_(Brasil)'.format(domain)
        response = requests.get(url)

        if response.status_code != 200:
            self.raise_error('Error on get "Assembleias legislativas"')

        data = lxml.html.fromstring(response.content)
        trs = data.cssselect('table.wikitable tr')
        trs.pop(0)
        for row in trs:
            try:
                name, _, _, _, website = row.getchildren()

                wikipedia = '{}{}'.format(domain, name.find('a').get('href'))
                logo = self.get_logo(wikipedia)

                # FIXME
                ex = 'Legislativa do | de | da '
                _, state_name = re.compile(ex).split(self.formatter(name), 1)
                state = State.objects.cache().get(name=state_name)

                if state.siglum == 'DF':
                    siglum = 'CLDF'
                    political_office = PoliticalOffice.get_by_name(
                        'Deputado Distrital'
                    )
                else:
                    siglum = 'AL{0}'.format(state.siglum)
                    political_office = PoliticalOffice.get_by_name(
                        'Deputado Estadual'
                    )

                website = 'http://{}'.format(self.formatter(website))

                name = self.formatter(name)

                institution = Institution(
                    name=name,
                    siglum=siglum,
                    logo=logo,
                    state=state,
                    website=website,
                    wikipedia=wikipedia,
                )
                institution.save()

                po = PoliticalOffice.get_by_name(political_office)
                institution.political_offices.add(po)

                self.logger.info('Added institution: "%s"', name)
            except Exception as e:
                self.logger.error('Error when add institution: %s', e)

    def add_senado(self):
        domain = 'https://pt.wikipedia.org'
        url = '{}/wiki/Senado_Federal_do_Brasil'.format(domain)

        name = 'Senado Federal do Brasil'

        institution = Institution(
            name=name,
            siglum='Senado',
            logo=self.get_logo(url),
            state=None,
            website='http://www.senado.leg.br',
            wikipedia=url,
        )
        institution.save()

        po1 = PoliticalOffice.get_by_name('Senador')
        po2 = PoliticalOffice.get_by_name('Senador 1º Suplente')
        po3 = PoliticalOffice.get_by_name('Senador 2º Suplente')
        institution.political_offices.add(po1, po2, po3)

        self.logger.info('Added institution: "%s"', name)

    def add_camara_federal(self):
        domain = 'https://pt.wikipedia.org'
        url = '{}/wiki/C%C3%A2mara_dos_Deputados_do_Brasil'.format(domain)

        name = 'Câmara dos Deputados do Brasil'

        institution = Institution(
            name=name,
            siglum='CDF',
            logo=self.get_logo(url),
            state=None,
            website='http://www.camara.leg.br',
            wikipedia=url,
        )
        institution.save()

        po = PoliticalOffice.get_by_name('Deputado Federal')
        institution.political_offices.add(po)

        self.logger.info('Added institution: "%s"', name)

    def add_presidencia(self):
        domain = 'https://pt.wikipedia.org'
        url = '{}/wiki/Presidente_do_Brasil'.format(domain)

        name = 'Presidência da República'

        institution = Institution(
            name=name,
            siglum='PR',
            logo=self.get_logo(url),
            state=None,
            website='http://www.presidencia.gov.br',
            wikipedia=url,
        )
        institution.save()

        po1 = PoliticalOffice.get_by_name('Presidente')
        po2 = PoliticalOffice.get_by_name('Vice-Presidente')
        institution.political_offices.add(po1, po2)

        self.logger.info('Added institution: "%s"', name)

    def handle(self, *args, **options):
        self.set_options(*args, **options)

        self.add_assembleias_legislativas()
        self.add_camara_federal()
        self.add_senado()
        self.add_presidencia()
        self.add_governador()
