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

from politicos.models.political_office import PoliticalOffice
from tests.unit.base import ApiTestCase
from tests.fixtures import PoliticalOfficeFactory


class TestPoliticalOffice(ApiTestCase):

    def test_can_create_political_office(self):
        political_office = PoliticalOfficeFactory.create(
            name='Deputado Federal',
        )

        expect(political_office.id).not_to_be_null()
        expect(political_office.name).to_equal('Deputado Federal')
        expect(political_office.slug).to_equal('deputado-federal')

    def test_can_convert_to_dict(self):
        political_office = PoliticalOfficeFactory.create()
        political_office_dict = political_office.to_dict()

        expect(political_office_dict.keys()).to_length(2)
        expect(political_office_dict.keys()).to_be_like(['name', 'slug'])
        expect(political_office_dict['name']).to_equal(political_office.name)
        expect(political_office_dict['slug']).to_equal(political_office.slug)

    @patch('politicos.models.political_office.logging')
    def test_can_add_political_office(self, logging_mock):
        data = {'name': 'Deputado Federal'}
        political_office = PoliticalOffice.add_political_office(self.db, data)

        expect(political_office.name).to_equal('Deputado Federal')
        expect(logging_mock.mock_calls).to_include(
            call.debug('Added political office: "%s"', 'Deputado Federal')
        )

    def test_cannot_add_political_office_twice(self):
        PoliticalOfficeFactory.create(name='Deputado Federal')

        with expect.error_to_happen(IntegrityError):
            PoliticalOfficeFactory.create(name='Deputado Federal')
