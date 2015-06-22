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

from datetime import datetime, timedelta

from preggy import expect
from mock import patch, call
from sqlalchemy.exc import IntegrityError

from politicos.models.legislature import Legislature
from politicos.utils import date_to_timestamp
from tests.unit.base import ApiTestCase
from tests.fixtures import LegislatureFactory, InstitutionFactory


class TestLegislature(ApiTestCase):

    def test_can_create_legislature(self):
        date_start = datetime.now().date()
        date_end = (datetime.now() + timedelta(days=10)).date()
        institution = InstitutionFactory.create()

        legislature = LegislatureFactory.create(
            institution=institution,
            date_start=date_start,
            date_end=date_end
        )

        expect(legislature.id).not_to_be_null()
        expect(legislature.date_start).to_equal(date_start)
        expect(legislature.date_end).to_equal(date_end)
        expect(legislature.institution).to_equal(institution)

    def test_can_convert_to_dict(self):
        legislature = LegislatureFactory.create()
        legislature_dict = legislature.to_dict()

        expect(legislature_dict.keys()).to_length(3)

        expect(legislature_dict.keys()).to_be_like([
            'date_start', 'date_end', 'institution'
        ])

        date_start = date_to_timestamp(legislature.date_start)
        date_end = date_to_timestamp(legislature.date_end)

        expect(legislature_dict['date_start']).to_equal(date_start)
        expect(legislature_dict['date_end']).to_equal(date_end)
        expect(legislature_dict['institution']).to_equal(
            legislature.institution.to_dict()
        )

    @patch('politicos.models.legislature.logging')
    def test_can_add_legislature(self, logging_mock):
        institution = InstitutionFactory.create()

        now = datetime.utcnow()
        d1 = now.date()
        date_start = date_to_timestamp(d1)
        d2 = (now + timedelta(days=10)).date()
        date_end = date_to_timestamp(d2)

        data = {
            'institution_id': institution.id,
            'date_start': date_start,
            'date_end': date_end,
        }
        legislature = Legislature.add_legislature(self.db, data)

        expect(legislature.institution).to_equal(institution)
        expect(legislature.date_start).to_equal(d1)
        expect(legislature.date_end).to_equal(d2)
        expect(logging_mock.mock_calls).to_include(
            call.debug('Added legislature: "%s"', str(legislature))
        )

    def test_cannot_add_legislature_twice(self):
        date_start = datetime.now().date()
        date_end = (datetime.now() + timedelta(days=10)).date()
        institution = InstitutionFactory.create()

        LegislatureFactory.create(
            institution=institution,
            date_start=date_start,
            date_end=date_end
        )

        with expect.error_to_happen(IntegrityError):
            LegislatureFactory.create(
                institution=institution,
                date_start=date_start,
                date_end=date_end
            )
