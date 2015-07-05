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

from mock import patch, call
from preggy import expect
from sqlalchemy.exc import IntegrityError

from politicos.models.mandate_events_type import MandateEventsType
from tests.unit.base import ApiTestCase
from tests.fixtures import MandateEventsTypeFactory


class TestPoliticalOffice(ApiTestCase):

    def test_can_create_mandate_events_type(self):
        mandate_events_type = MandateEventsTypeFactory.create(
            name='Assumiu cargo no executivo'
        )

        expect(mandate_events_type.id).not_to_be_null()
        expect(mandate_events_type.name).to_equal('Assumiu cargo no executivo')
        expect(mandate_events_type.slug).to_equal('assumiu-cargo-no-executivo')

    def test_can_convert_to_dict(self):
        mandate_events_type = MandateEventsTypeFactory.create()
        mandate_events_type_dict = mandate_events_type.to_dict()

        expect(mandate_events_type_dict.keys()).to_length(2)
        expect(mandate_events_type_dict.keys()).to_be_like(['name', 'slug'])
        expect(mandate_events_type_dict['name']).to_equal(
            mandate_events_type.name
        )
        expect(mandate_events_type_dict['slug']).to_equal(
            mandate_events_type.slug
        )

    @patch('politicos.models.mandate_events_type.logging')
    def test_can_add_mandate_events_type(self, logging_mock):
        data = {'name': 'Assumiu cargo no executivo'}
        mandate_events_type = MandateEventsType.add_mandate_events_type(
            self.db, data
        )

        expect(str(mandate_events_type)).to_equal('Assumiu cargo no executivo')
        expect(logging_mock.mock_calls).to_include(
            call.debug(
                'Added mandate events type: "%s"', 'Assumiu cargo no executivo'
            )
        )

    def test_cannot_add_mandate_events_type_twice(self):
        MandateEventsTypeFactory.create(name='Assumiu cargo no executivo')

        with expect.error_to_happen(IntegrityError):
            MandateEventsTypeFactory.create(name='Assumiu cargo no executivo')
