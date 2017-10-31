# -*- coding: utf-8 -*-
#
# Copyright (c) 2016, Marcelo Jorge Vieira <metal@alucinados.com>
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

from datetime import datetime

from django.db import IntegrityError

from politicians.management.commands._base import PoliticosCommand
from politicians.models import Election, ElectionRound


class Command(PoliticosCommand):

    def handle(self, *args, **options):
        self.set_options(*args, **options)

        elections = [
            ('2000', [(1, '01/10/2000'), (2, '29/10/2000')]),
            ('2002', [(1, '06/10/2002'), (2, '27/10/2002')]),
            ('2004', [(1, '03/10/2004'), (2, '31/10/2004')]),
            ('2006', [(1, '01/10/2006'), (2, '29/10/2006')]),
            ('2008', [(1, '05/10/2008'), (2, '26/10/2008')]),
            ('2010', [(1, '03/10/2010'), (2, '31/10/2010')]),
            ('2012', [(1, '07/10/2012'), (2, '28/10/2012')]),
            ('2014', [(1, '05/10/2014'), (2, '26/10/2014')]),
            ('2016', [(1, '02/10/2016'), (2, '30/10/2016')]),
        ]

        for year, rounds in elections:
            try:
                election = Election(year=year)
                election.save()
                self.logger.info(
                    'Added Election: %s', election
                )
            except IntegrityError as e:
                self.logger.error(e)

            for round_number, date in rounds:
                try:
                    election_round = ElectionRound(
                        election=election,
                        round_number=round_number,
                        date=datetime.strptime(date, '%d/%m/%Y')
                    )
                    election_round.save()
                    self.logger.info(
                        'Added Election Round: %s', election_round.round_number
                    )
                except IntegrityError as e:
                    self.logger.error(e)
