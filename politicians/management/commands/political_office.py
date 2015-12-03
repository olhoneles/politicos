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

from django.db import IntegrityError
from django.utils.text import slugify

from politicians.management.commands._base import PoliticosCommand
from politicians.models import PoliticalOffice


class Command(PoliticosCommand):

    def handle(self, *args, **options):
        self.set_options(*args, **options)

        political_offices = [
            {'name': 'Presidente', 'term': 4},
            {'name': 'Vice-Presidente', 'term': 4},
            {'name': 'Governador', 'term': 4},
            {'name': 'Vice-Governador', 'term': 4},
            {'name': 'Deputado Federal', 'term': 4},
            {'name': 'Deputado Estadual', 'term': 4},
            {'name': 'Deputado Distrital', 'term': 4},
            {'name': 'Prefeito', 'term': 4},
            {'name': 'Vice-Prefeito', 'term': 4},
            {'name': 'Vereador', 'term': 4},
            {'name': 'Senador', 'term': 8},
            {'name': 'Senador 1º Suplente', 'term': 8},
            {'name': 'Senador 2º Suplente', 'term': 8},
        ]

        for item in political_offices:
            try:
                political_office = PoliticalOffice(
                    name=item.get('name'),
                    term=item.get('term'),
                    slug=slugify(item.get('name')),
                )
                political_office.save()
                self.logger.info(
                    'Added Political Office: %s', item.get('name')
                )
            except IntegrityError as e:
                self.logger.error(e)
