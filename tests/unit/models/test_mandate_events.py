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

from datetime import datetime

from preggy import expect
from mock import patch, call
from sqlalchemy.exc import IntegrityError

from politicos.models.mandate_events import MandateEvents
from politicos.utils import date_to_timestamp
from tests.unit.base import ApiTestCase
from tests.fixtures import (
    MandateEventsTypeFactory, MandateEventsFactory, MandateFactory
)


class TestMandateEvents(ApiTestCase):

    def test_can_create_mandate_events(self):
        date = datetime.now().date()
        mandate_events_type = MandateEventsTypeFactory.create()
        mandate = MandateFactory.create()

        mandate_events = MandateEventsFactory.create(
            date=date,
            mandate_events_type=mandate_events_type,
            mandate=mandate
        )

        expect(mandate_events.id).not_to_be_null()
        expect(mandate_events.date).to_equal(date)
        expect(mandate_events.mandate).to_equal(mandate)
        expect(mandate_events.mandate_events_type).to_equal(
            mandate_events_type
        )

    def test_can_convert_to_dict(self):
        mandate_events = MandateEventsFactory.create()
        mandate_events_dict = mandate_events.to_dict()

        expect(mandate_events_dict.keys()).to_length(3)

        expect(mandate_events_dict.keys()).to_be_like([
            'date', 'mandate', 'mandate_events_type'
        ])

        date = date_to_timestamp(mandate_events.date)

        expect(mandate_events_dict['date']).to_equal(date)
        expect(mandate_events_dict['mandate_events_type']).to_equal(
            mandate_events.mandate_events_type.to_dict()
        )

    @patch('politicos.models.mandate_events.logging')
    def test_can_add_mandate_events(self, logging_mock):
        mandate = MandateFactory.create()
        mandate_events_type = MandateEventsTypeFactory.create()
        date = datetime.utcnow().date()
        d1 = date_to_timestamp(date)

        data = {
            'mandate_id': mandate.id,
            'mandate_events_type_id': mandate_events_type.id,
            'date': d1,
        }
        mandate_events = MandateEvents.add_mandate_events(self.db, data)

        expect(mandate_events.mandate).to_equal(mandate)
        expect(mandate_events.mandate_events_type).to_equal(
            mandate_events_type
        )
        expect(mandate_events.date).to_equal(date)
        expect(logging_mock.mock_calls).to_include(
            call.debug('Added mandate events: "%s"', str(mandate_events))
        )

    def test_cannot_add_mandate_events_twice(self):
        date = datetime.now().date()
        mandate_events_type = MandateEventsTypeFactory.create()
        mandate = MandateFactory.create()

        MandateEventsFactory.create(
            mandate_events_type=mandate_events_type,
            date=date,
            mandate=mandate
        )

        with expect.error_to_happen(IntegrityError):
            MandateEventsFactory.create(
                mandate_events_type=mandate_events_type,
                date=date,
                mandate=mandate
            )
