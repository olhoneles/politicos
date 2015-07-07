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
from tests.fixtures import LegislatorEventsTypeFactory


class TestLegislatorEventsTypeHandler(ApiTestCase):

    @gen_test
    def test_can_get_empty_legislator_events_type_info(self):
        response = yield self.anonymous_fetch(
            '/legislator-events-types/presidente-do-partido/',
            method='GET'
        )
        expect(response.code).to_equal(200)
        legislator_events_type = loads(response.body)
        expect(legislator_events_type).to_equal({})
        expect(legislator_events_type).to_length(0)

    @gen_test
    def test_can_get_legislator_events_type_info(self):
        LegislatorEventsTypeFactory.create(name='Presidente do Partido')

        response = yield self.anonymous_fetch(
            '/legislator-events-types/presidente-do-partido/',
            method='GET'
        )
        expect(response.code).to_equal(200)
        legislator_events_type = loads(response.body)
        expect(legislator_events_type).to_length(2)
        expect(legislator_events_type.get('name')).to_equal(
            'Presidente do Partido'
        )
        expect(legislator_events_type.get('slug')).to_equal(
            'presidente-do-partido'
        )


class TestAllPoliticalOfficesHandler(ApiTestCase):

    @gen_test
    def test_can_get_empty_legislator_events_type_info(self):
        response = yield self.anonymous_fetch(
            '/legislator-events-types/',
            method='GET'
        )

        expect(response.code).to_equal(200)
        legislator_events_type = loads(response.body)
        expect(legislator_events_type).to_equal({})
        expect(legislator_events_type).to_length(0)

    @gen_test
    def test_can_get_all_legislator_events_types(self):
        legislator_events_types = []
        for x in range(5):
            legislator_events_type = LegislatorEventsTypeFactory.create()
            legislator_events_types.append(legislator_events_type.to_dict())

        response = yield self.anonymous_fetch(
            '/legislator-events-types/',
            method='GET'
        )

        expect(response.code).to_equal(200)
        legislator_events_types_loaded = loads(response.body)
        expect(legislator_events_types_loaded).to_length(5)
        expect(legislator_events_types_loaded).to_be_like(
            legislator_events_types
        )

    @gen_test
    def test_can_add_legislator_events_type(self):
        response = yield self.anonymous_fetch(
            '/legislator-events-types/',
            method='POST',
            body=dumps({'name': 'Presidente do Partido'})
        )
        expect(response.code).to_equal(200)
        data = loads(response.body)
        expect(data.get('name')).to_equal('Presidente do Partido')

    @gen_test
    def test_cannot_add_legislator_events_type_twice(self):
        yield self.anonymous_fetch(
            '/legislator-events-types/',
            method='POST',
            body=dumps({'name': 'Presidente do Partido'})
        )

        try:
            yield self.anonymous_fetch(
                '/legislator-events-types/',
                method='POST',
                body=dumps({'name': 'Presidente do Partido'})
            )
        except HTTPError as e:
            expect(e).not_to_be_null()
            expect(e.code).to_equal(500)
            expect(e.response.reason).to_be_like('Internal Server Error')

    @gen_test
    def test_cannot_add_legislator_events_type_without_name(self):
        try:
            yield self.anonymous_fetch(
                '/legislator-events-types/',
                method='POST',
                body=dumps({})
            )
        except HTTPError as e:
            expect(e).not_to_be_null()
            expect(e.code).to_equal(400)
            expect(e.response.reason).to_be_like(
                'Invalid legislator Events Type'
            )
