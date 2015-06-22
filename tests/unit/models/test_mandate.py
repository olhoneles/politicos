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

from politicos.models.mandate import Mandate
from politicos.utils import date_to_timestamp
from tests.unit.base import ApiTestCase
from tests.fixtures import (
    MandateFactory, PoliticalOfficeFactory, LegislatorFactory
)


class TestMandate(ApiTestCase):

    def test_can_create_mandate(self):
        date_start = datetime.now().date()
        date_end = (datetime.now() + timedelta(days=10)).date()
        political_office = PoliticalOfficeFactory.create()
        legislator = LegislatorFactory.create()

        mandate = MandateFactory.create(
            legislator=legislator,
            political_office=political_office,
            date_start=date_start,
            date_end=date_end
        )

        expect(mandate.id).not_to_be_null()
        expect(mandate.date_start).to_equal(date_start)
        expect(mandate.date_end).to_equal(date_end)
        expect(mandate.political_office).to_equal(political_office)

    def test_can_convert_to_dict(self):
        mandate = MandateFactory.create()
        mandate_dict = mandate.to_dict()

        expect(mandate_dict.keys()).to_length(4)

        expect(mandate_dict.keys()).to_be_like([
            'date_start', 'date_end', 'political_office', 'legislator'
        ])

        date_start = date_to_timestamp(mandate.date_start)
        date_end = date_to_timestamp(mandate.date_end)

        expect(mandate_dict['date_start']).to_equal(date_start)
        expect(mandate_dict['date_end']).to_equal(date_end)
        expect(mandate_dict['political_office']).to_equal(
            mandate.political_office.to_dict()
        )
        expect(mandate_dict['legislator']).to_equal(
            mandate.legislator.to_dict()
        )

    @patch('politicos.models.mandate.logging')
    def test_can_add_mandate(self, logging_mock):
        political_office = PoliticalOfficeFactory.create()
        legislator = LegislatorFactory.create()

        now = datetime.utcnow()
        d1 = now.date()
        date_start = date_to_timestamp(d1)
        d2 = (now + timedelta(days=10)).date()
        date_end = date_to_timestamp(d2)

        data = {
            'legislator_id': legislator.id,
            'political_office_id': political_office.id,
            'date_start': date_start,
            'date_end': date_end,
        }
        mandate = Mandate.add_mandate(self.db, data)

        expect(mandate.legislator).to_equal(legislator)
        expect(mandate.political_office).to_equal(political_office)
        expect(mandate.date_start).to_equal(d1)
        expect(mandate.date_end).to_equal(d2)
        expect(logging_mock.mock_calls).to_include(
            call.debug('Added mandate: "%s"', str(mandate))
        )

    def test_cannot_add_mandate_twice(self):
        date_start = datetime.now().date()
        date_end = (datetime.now() + timedelta(days=10)).date()
        political_office = PoliticalOfficeFactory.create()
        legislator = LegislatorFactory.create()

        MandateFactory.create(
            legislator=legislator,
            political_office=political_office,
            date_start=date_start,
            date_end=date_end
        )

        with expect.error_to_happen(IntegrityError):
            MandateFactory.create(
                legislator=legislator,
                political_office=political_office,
                date_start=date_start,
                date_end=date_end
            )
