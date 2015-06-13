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

from preggy import expect
from mock import patch, call
from sqlalchemy.exc import IntegrityError

from politicos.models.institution import Institution
from tests.unit.base import ApiTestCase
from tests.fixtures import InstitutionFactory


class TestInstitution(ApiTestCase):

    def test_can_create_institution(self):
        institution = InstitutionFactory.create(
            siglum='HMI',
            name='Hevy Metal Institution',
            logo='http://metal.com/logo.png'
        )

        expect(institution.id).not_to_be_null()
        expect(institution.siglum).to_equal('HMI')
        expect(institution.name).to_equal('Hevy Metal Institution')
        expect(institution.logo).to_equal('http://metal.com/logo.png')

    def test_can_convert_to_dict(self):
        institution = InstitutionFactory.create()
        institution_dict = institution.to_dict()

        expect(institution_dict.keys()).to_length(3)

        expect(institution_dict.keys()).to_be_like([
            'siglum', 'name', 'logo'
        ])

        expect(institution_dict['siglum']).to_equal(institution.siglum)
        expect(institution_dict['name']).to_equal(institution.name)
        expect(institution_dict['logo']).to_equal(institution.logo)

    @patch('politicos.models.institution.logging')
    def test_can_add_institution(self, logging_mock):
        data = {'name': 'Hevy Metal Institution', 'siglum': 'HMI'}
        name = Institution.add_institution(self.db, data)

        expect(name).to_equal('Hevy Metal Institution')
        expect(logging_mock.mock_calls).to_include(
            call.debug('Added institution: "%s"', 'Hevy Metal Institution')
        )

    def test_cannot_add_institution_twice(self):
        InstitutionFactory.create(siglum='HMI', name='Hevy Metal Institution')

        with expect.error_to_happen(IntegrityError):
            InstitutionFactory.create(
                siglum='HMI', name='Hevy Metal Institution'
            )
