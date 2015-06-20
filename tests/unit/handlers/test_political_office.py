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
from tests.fixtures import PoliticalOfficeFactory


class TestPoliticalOfficeHandler(ApiTestCase):

    @gen_test
    def test_can_get_empty_political_office_info(self):
        response = yield self.anonymous_fetch(
            '/political-offices/deputado-estadual/',
            method='GET'
        )
        expect(response.code).to_equal(200)
        political_office = loads(response.body)
        expect(political_office).to_equal({})
        expect(political_office).to_length(0)

    @gen_test
    def test_can_get_political_office_info(self):
        PoliticalOfficeFactory.create(name='Deputado Estadual')

        response = yield self.anonymous_fetch(
            '/political-offices/deputado-estadual/',
            method='GET'
        )
        expect(response.code).to_equal(200)
        political_office = loads(response.body)
        expect(political_office).to_length(2)
        expect(political_office.get('name')).to_equal('Deputado Estadual')
        expect(political_office.get('slug')).to_equal('deputado-estadual')


class TestAllPoliticalOfficesHandler(ApiTestCase):

    @gen_test
    def test_can_get_empty_political_office_info(self):
        response = yield self.anonymous_fetch(
            '/political-offices/',
            method='GET'
        )

        expect(response.code).to_equal(200)
        political_office = loads(response.body)
        expect(political_office).to_equal({})
        expect(political_office).to_length(0)

    @gen_test
    def test_can_get_all_political_offices(self):
        political_offices = []
        for x in range(5):
            political_office = PoliticalOfficeFactory.create()
            political_offices.append(political_office.to_dict())

        response = yield self.anonymous_fetch(
            '/political-offices/',
            method='GET'
        )

        expect(response.code).to_equal(200)
        political_offices_loaded = loads(response.body)
        expect(political_offices_loaded).to_length(5)
        expect(political_offices_loaded).to_be_like(political_offices)

    @gen_test
    def test_can_add_political_office(self):
        response = yield self.anonymous_fetch(
            '/political-offices/',
            method='POST',
            body=dumps({'name': 'Deputado Estadual'})
        )
        expect(response.code).to_equal(200)
        data = loads(response.body)
        expect(data.get('name')).to_equal('Deputado Estadual')

    @gen_test
    def test_cannot_add_political_office_twice(self):
        yield self.anonymous_fetch(
            '/political-offices/',
            method='POST',
            body=dumps({'name': 'Deputado Estadual'})
        )

        try:
            yield self.anonymous_fetch(
                '/political-offices/',
                method='POST',
                body=dumps({'name': 'Deputado Estadual'})
            )
        except HTTPError as e:
            expect(e).not_to_be_null()
            expect(e.code).to_equal(500)
            expect(e.response.reason).to_be_like('Internal Server Error')

    @gen_test
    def test_cannot_add_political_office_without_name(self):
        try:
            yield self.anonymous_fetch(
                '/political-offices/',
                method='POST',
                body=dumps({})
            )
        except HTTPError as e:
            expect(e).not_to_be_null()
            expect(e.code).to_equal(400)
            expect(e.response.reason).to_be_like('Invalid Political Office')
