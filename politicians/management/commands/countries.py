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

import requests
from django.db import IntegrityError
from json import loads

from politicians.management.commands._base import PoliticosCommand
from politicians.models import Country


class Command(PoliticosCommand):

    def formatter(self, name):
        return name.text_content().replace('\n', '').strip()

    def handle(self, *args, **options):
        self.set_options(*args, **options)

        url = 'https://restcountries.eu/rest/v2/all'
        response = requests.get(url)

        if response.status_code != 200:
            self.raise_error('Error on get countries')

        data = loads(response.content)
        for country in data:
            try:
                country = Country(
                    name=country.get('translations', {}).get('br'),
                    siglum=country.get('alpha2Code'),
                )
                country.save()
                self.logger.info('Added country: %s', country)
            except IntegrityError as e:
                self.logger.info(
                    'Error on save country: %s. Details: %s', country, e
                )
