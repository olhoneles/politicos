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

from ujson import loads, dumps
from preggy import expect
from tornado.testing import gen_test
from tornado.httpclient import HTTPError

from tests.unit.base import ApiTestCase
from tests.fixtures import InstitutionFactory


class TestInstitutionHandler(ApiTestCase):

    @gen_test
    def test_cannot_get_institution_info(self):
        response = yield self.anonymous_fetch(
            '/institutions/HMI',
            method='GET'
        )
        expect(response.code).to_equal(200)
        institution = loads(response.body)
        expect(institution).to_equal({})
        expect(institution).to_length(0)

    @gen_test
    def test_can_get_institution_info(self):
        InstitutionFactory.create(
            name='Heavy Metal Institution',
            siglum='HMI',
            logo='http://l.com/logo.png'
        )

        response = yield self.anonymous_fetch(
            '/institutions/HMI',
            method='GET'
        )
        expect(response.code).to_equal(200)
        institution = loads(response.body)
        expect(institution).to_length(3)
        expect(institution.get('name')).to_equal('Heavy Metal Institution')
        expect(institution.get('siglum')).to_equal('HMI')
        expect(institution.get('logo')).to_equal('http://l.com/logo.png')


class TestAllInstitutionHandler(ApiTestCase):

    @gen_test
    def test_cannot_get_institution_info(self):
        response = yield self.anonymous_fetch(
            '/institutions/',
            method='GET'
        )

        expect(response.code).to_equal(200)
        institution = loads(response.body)
        expect(institution).to_equal({})
        expect(institution).to_length(0)

    @gen_test
    def test_can_get_all_institutions(self):
        institutions = []
        for x in range(5):
            institution = InstitutionFactory.create(
                name='Institution %s' % x,
                siglum='%s' % x,
            )
            institutions.append(institution.to_dict())

        response = yield self.anonymous_fetch(
            '/institutions/',
            method='GET'
        )

        expect(response.code).to_equal(200)
        institutions_loaded = loads(response.body)
        expect(institutions_loaded).to_length(5)
        expect(institutions_loaded).to_be_like(institutions)

    @gen_test
    def test_can_add_institution(self):
        response = yield self.anonymous_fetch(
            '/institutions/',
            method='POST',
            body=dumps({'name': 'Heavy Metal Institution', 'siglum': 'HMI'})
        )
        expect(response.code).to_equal(200)
        data = loads(response.body)
        expect(data.get('name')).to_equal('Heavy Metal Institution')
        expect(data.get('siglum')).to_equal('HMI')

    @gen_test
    def test_cannot_add_institution_twice(self):
        yield self.anonymous_fetch(
            '/institutions/',
            method='POST',
            body=dumps({'name': 'Heavy Metal Institution', 'siglum': 'HMI'})
        )

        try:
            yield self.anonymous_fetch(
                '/institutions/',
                method='POST',
                body=dumps({
                    'name': 'Heavy Metal Institution', 'siglum': 'HMI'
                })
            )
        except HTTPError as e:
            expect(e).not_to_be_null()
            expect(e.code).to_equal(500)
            expect(e.response.reason).to_be_like('Internal Server Error')

    @gen_test
    def test_cannot_add_institution_without_name(self):
        try:
            yield self.anonymous_fetch(
                '/institutions/',
                method='POST',
                body=dumps({'siglum': 'HMI'})
            )
        except HTTPError as e:
            expect(e).not_to_be_null()
            expect(e.code).to_equal(400)
            expect(e.response.reason).to_be_like('Invalid Institution')

    @gen_test
    def test_cannot_add_institution_without_siglum(self):
        try:
            yield self.anonymous_fetch(
                '/institutions/',
                method='POST',
                body=dumps({'name': 'Heavy Metal Institution'})
            )
        except HTTPError as e:
            expect(e).not_to_be_null()
            expect(e.code).to_equal(400)
            expect(e.response.reason).to_be_like('Invalid Institution')
