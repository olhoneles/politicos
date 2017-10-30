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
from datetime import datetime

from politicians.management.commands._base import PoliticosCommand
from politicians.models import PoliticalParty


class Command(PoliticosCommand):

    def formatter(self, name):
        return name.text_content().replace('\n', '').strip()

    def add_political_party(self, name, siglum, tse_number):
        try:
            political_party = PoliticalParty(
                siglum=siglum,
                name=name,
                tse_number=tse_number
            )
            political_party.save()
            self.logger.info(
                'Added political party: "%s"', political_party.siglum
            )
        except Exception as e:
            self.logger.error(
                'Error when add political party: "%s (%s)". Details: %s',
                name, siglum, str(e)
            )

    def handle(self, *args, **options):
        self.set_options(*args, **options)

        url = 'http://www.tse.jus.br/partidos/partidos-politicos'
        response = requests.get(url)

        if response.status_code != 200:
            self.raise_error('Error on get political parties')

        data = lxml.html.fromstring(response.content)
        trs = data.cssselect('table tr')
        trs.pop(0)
        for row in trs:
            try:
                _, siglum, name, _, _, tse_number = row.getchildren()
            except Exception:
                continue
            self.add_political_party(
                self.title_except(self.formatter(name)),
                self.formatter(siglum),
                self.formatter(tse_number)
            )

        self.add_political_party(
            'Partido Liberal', 'PL', '22'
        )
        self.add_political_party(
            'Partido da Frente Liberal', 'PFL', '25'
        )
        self.add_political_party(
            'Partido dos Aposentados da Nação', 'PAN', '26'
        )
        self.add_political_party(
            'Partido de Reedificação da Ordem Nacional', 'PRONA', '56'
        )
        self.add_political_party(
            'Partido Progressista Brasileiro', 'PPB', '11'
        )
        self.add_political_party(
            'Partido Geral dos Trabalhadores', 'PGT', '30'
        )
        self.add_political_party(
            'Partido Social Trabalhista', 'PST', '52'
        )
        self.add_political_party(
            'Partido da Reconstrução Nacional', 'PRN', '36'
        )

        self.update_by_wikipedia()

    def get_logo(self, url):
        response = requests.get(url)
        if response.status_code != 200:
            self.logger.error('Error on get political party url')
            return
        data = lxml.html.fromstring(response.content)
        imgs = data.cssselect('table.infobox_v2 tr img')
        if not imgs:
            imgs = data.cssselect('table.infobox tr img')
        if not imgs:
            self.logger.error('Error on get  political party logo')
            return
        logo = imgs[0].get('src')
        self.logger.info('Get political party logo')
        return logo

    def update_by_wikipedia(self):
        domain = 'https://pt.wikipedia.org'
        url = '{0}/wiki/Lista_de_partidos_pol%C3%ADticos_no_Brasil'.format(
            domain
        )
        response = requests.get(url)

        if response.status_code != 200:
            self.raise_error('Error on get political parties')

        items = []
        data = lxml.html.fromstring(response.content)
        trs = data.cssselect('table.wikitable tr')
        trs.pop(0)
        for row in trs:
            try:
                _, name, siglum, _, founded_date = row.getchildren()[:5]
                wikipedia = '{0}{1}'.format(domain, name.find('a').get('href'))
                founded_date = self.formatter(founded_date)
                founded_date = re.sub(r'\[.*\]', '', founded_date).strip()
                name = re.sub(r'\[.*\]', '', self.formatter(name)).strip()
            except Exception:
                continue

            logo = self.get_logo(wikipedia)

            try:
                founded_date = datetime.strptime(founded_date, '%d/%m/%Y')
            except ValueError:
                if isinstance(founded_date, int):
                    founded_date = datetime.strptime(founded_date, '%Y')
                else:
                    founded_date = None

            items.append({
                'name': name,
                'siglum': self.formatter(siglum),
                'founded_date': founded_date,
                'wikipedia': wikipedia,
                'logo': logo,
            })

        political_parties = PoliticalParty.objects.all()
        for political_party in political_parties:
            party = [x for x in items if x['siglum'] == political_party.siglum]
            if party:
                political_party.founded_date = party[0].get('founded_date')
                political_party.wikipedia = party[0].get('wikipedia')
                political_party.logo = party[0].get('logo')
                political_party.save()
                self.logger.info(
                    'Updated political party: %s', political_party
                )
