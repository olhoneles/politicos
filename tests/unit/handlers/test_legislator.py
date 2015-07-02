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
from tests.fixtures import LegislatorFactory


class TestAllLegislatorsHandler(ApiTestCase):

    @gen_test
    def test_can_get_all_legislators(self):
        legislators = []
        for x in range(5):
            legislator = LegislatorFactory.create()
            legislators.append(legislator.to_dict())

        response = yield self.anonymous_fetch(
            '/legislators/',
            method='GET'
        )

        expect(response.code).to_equal(200)
        legislators_loaded = loads(response.body)
        expect(legislators_loaded).to_length(5)
        expect(legislators_loaded).to_be_like(legislators)

    @gen_test
    def test_cannot_get_legislators_info(self):
        response = yield self.anonymous_fetch(
            '/legislators/',
            method='GET'
        )

        expect(response.code).to_equal(200)
        legislators = loads(response.body)
        expect(legislators).to_equal({})
        expect(legislators).to_length(0)

    @gen_test
    def test_can_add_legislator(self):
        response = yield self.anonymous_fetch(
            '/legislators/',
            method='POST',
            body=dumps({'name': 'Marcelo Jorge Vieira'})
        )
        expect(response.code).to_equal(200)
        data = loads(response.body)
        expect(data.get('name')).to_equal('Marcelo Jorge Vieira')

    @gen_test
    def test_cannot_add_legislator_without_name(self):
        try:
            yield self.anonymous_fetch(
                '/legislators/',
                method='POST',
                body=dumps({'gender': 'M'})
            )
        except HTTPError as e:
            expect(e).not_to_be_null()
            expect(e.code).to_equal(400)
            expect(e.response.reason).to_be_like('Invalid legislator')
