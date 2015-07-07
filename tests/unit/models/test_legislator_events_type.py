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

from politicos.models.legislator_events_type import LegislatorEventsType
from tests.unit.base import ApiTestCase
from tests.fixtures import LegislatorEventsTypeFactory


class TestPoliticalOffice(ApiTestCase):

    def test_can_create_legislator_events_type(self):
        legislator_events_type = LegislatorEventsTypeFactory.create(
            name='Presidente do Partido'
        )

        expect(legislator_events_type.id).not_to_be_null()
        expect(legislator_events_type.name).to_equal('Presidente do Partido')
        expect(legislator_events_type.slug).to_equal('presidente-do-partido')

    def test_can_convert_to_dict(self):
        legislator_events_type = LegislatorEventsTypeFactory.create()
        legislator_events_type_dict = legislator_events_type.to_dict()

        expect(legislator_events_type_dict.keys()).to_length(2)
        expect(legislator_events_type_dict.keys()).to_be_like(['name', 'slug'])
        expect(legislator_events_type_dict['name']).to_equal(
            legislator_events_type.name
        )
        expect(legislator_events_type_dict['slug']).to_equal(
            legislator_events_type.slug
        )

    @patch('politicos.models.legislator_events_type.logging')
    def test_can_add_legislator_events_type(self, logging_mock):
        data = {'name': 'Presidente do Partido'}
        legislator_events_type = LegislatorEventsType \
            .add_legislator_events_type(self.db, data)

        expect(str(legislator_events_type)).to_equal('Presidente do Partido')
        expect(logging_mock.mock_calls).to_include(
            call.debug(
                'Added legislator events type: "%s"', 'Presidente do Partido'
            )
        )

    def test_cannot_add_legislator_events_type_twice(self):
        LegislatorEventsTypeFactory.create(name='Presidente do Partido')

        with expect.error_to_happen(IntegrityError):
            LegislatorEventsTypeFactory.create(name='Presidente do Partido')
