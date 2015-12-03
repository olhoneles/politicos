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

from django.utils.text import slugify

from politicians.management.commands._base import PoliticosCommand
from politicians.models import MandateEventType


class Command(PoliticosCommand):

    def handle(self, *args, **options):
        self.set_options(*args, **options)

        items = {
            'Eleito',
            'Posse',
            'Licença',
            'Assumiu cargo no executivo',
            'Cassado',
            'Falecido',
        }

        for item in items:
            try:
                mandate_event_type = MandateEventType(
                    name=item,
                    slug=slugify(item)
                )
                mandate_event_type.save()
                self.logger.info('Added mandate event type: "%s"', item)
            except Exception as e:
                self.logger.error('Error when add mandate event type: %s', e)
