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

from ujson import loads, dumps
from preggy import expect
from tornado.testing import gen_test
from tornado.httpclient import HTTPError

from politicos.utils import date_to_timestamp
from tests.unit.base import ApiTestCase
from tests.fixtures import (
    LegislatorEventsFactory, LegislatorFactory, LegislatorEventsTypeFactory
)


class TestAllLegislatorEventsHandler(ApiTestCase):

    @gen_test
    def test_can_get_empty_legislator_events_info(self):
        response = yield self.anonymous_fetch(
            '/legislator-events/',
            method='GET'
        )

        expect(response.code).to_equal(200)
        legislator_events = loads(response.body)
        expect(legislator_events).to_equal({})
        expect(legislator_events).to_length(0)

    @gen_test
    def test_can_get_all_legislator_events(self):
        events = []
        for x in range(5):
            legislator_events = LegislatorEventsFactory.create()
            events.append(legislator_events.to_dict())

        response = yield self.anonymous_fetch(
            '/legislator-events/',
            method='GET'
        )

        expect(response.code).to_equal(200)
        legislator_events_loaded = loads(response.body)
        expect(legislator_events_loaded).to_length(5)
        expect(legislator_events_loaded).to_be_like(events)

    @gen_test
    def test_can_add_legislator_events(self):
        legislator = LegislatorFactory.create()
        legislator_events_type = LegislatorEventsTypeFactory.create()
        date = date_to_timestamp(datetime.utcnow().date())

        response = yield self.anonymous_fetch(
            '/legislator-events/',
            method='POST',
            body=dumps({
                'date': date,
                'legislator_id': legislator.id,
                'legislator_events_type_id': legislator_events_type.id
            })
        )
        expect(response.code).to_equal(200)
        legislator_events = loads(response.body)
        expect(legislator_events.get('date')).to_equal(date)
        expect(legislator_events.get('legislator')).to_equal(legislator.to_dict())
        expect(legislator_events.get('legislator_events_type')).to_equal(
            legislator_events_type.to_dict()
        )

    @gen_test
    def test_cannot_add_legislator_events_twice(self):
        legislator = LegislatorFactory.create()
        legislator_events_type = LegislatorEventsTypeFactory.create()
        date = date_to_timestamp(datetime.utcnow().date())

        yield self.anonymous_fetch(
            '/legislator-events/',
            method='POST',
            body=dumps({
                'date': date,
                'legislator_id': legislator.id,
                'legislator_events_type_id': legislator_events_type.id
            })
        )

        try:
            yield self.anonymous_fetch(
                '/legislator-events/',
                method='POST',
                body=dumps({
                    'date': date,
                    'legislator_id': legislator.id,
                    'legislator_events_type_id': legislator_events_type.id
                })
            )
        except HTTPError as e:
            expect(e).not_to_be_null()
            expect(e.code).to_equal(500)
            expect(e.response.reason).to_be_like('Internal Server Error')

    @gen_test
    def test_cannot_add_legislator_events_without_date(self):
        legislator = LegislatorFactory.create()
        legislator_events_type = LegislatorEventsTypeFactory.create()

        try:
            yield self.anonymous_fetch(
                '/legislator-events/',
                method='POST',
                body=dumps({
                    'legislator_id': legislator.id,
                    'legislator_events_type_id': legislator_events_type.id
                })
            )
        except HTTPError as e:
            expect(e).not_to_be_null()
            expect(e.code).to_equal(400)
            expect(e.response.reason).to_be_like('Invalid Legislator Events')

    @gen_test
    def test_cannot_add_legislator_events_without_legislator_id(self):
        legislator_events_type = LegislatorEventsTypeFactory.create()
        date = date_to_timestamp(datetime.utcnow().date())

        try:
            yield self.anonymous_fetch(
                '/legislator-events/',
                method='POST',
                body=dumps({
                    'date': date,
                    'legislator_events_type_id': legislator_events_type.id
                })
            )
        except HTTPError as e:
            expect(e).not_to_be_null()
            expect(e.code).to_equal(400)
            expect(e.response.reason).to_be_like('Invalid Legislator Events')

    @gen_test
    def test_cannot_add_legislator_events_without_legislator_events_type_id(self):
        legislator = LegislatorFactory.create()
        date = date_to_timestamp(datetime.utcnow().date())

        try:
            yield self.anonymous_fetch(
                '/legislator-events/',
                method='POST',
                body=dumps({
                    'date': date,
                    'legislator_id': legislator.id,
                })
            )
        except HTTPError as e:
            expect(e).not_to_be_null()
            expect(e.code).to_equal(400)
            expect(e.response.reason).to_be_like('Invalid Legislator Events')
