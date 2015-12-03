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

from localflavor.br.br_states import STATE_CHOICES

from politicians.management.commands._base import PoliticosCommand
from politicians.models import State, Country


class Command(PoliticosCommand):

    def handle(self, *args, **options):
        self.set_options(*args, **options)

        country = Country.objects.cache().get(siglum='BR')
        for siglum, name in STATE_CHOICES:
            try:
                state = State(name=name, siglum=siglum, country=country)
                state.save()
                self.logger.info('Added state: "%s"', state)
            except Exception as e:
                self.logger.error('Error when add state: %s', e)
