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
    MandateEventsFactory, MandateFactory, MandateEventsTypeFactory
)


class TestAllMandateEventsHandler(ApiTestCase):

    @gen_test
    def test_can_get_empty_mandate_events_info(self):
        response = yield self.anonymous_fetch(
            '/mandate-events/',
            method='GET'
        )

        expect(response.code).to_equal(200)
        mandate_events = loads(response.body)
        expect(mandate_events).to_equal({})
        expect(mandate_events).to_length(0)

    @gen_test
    def test_can_get_all_mandate_events(self):
        events = []
        for x in range(5):
            mandate_events = MandateEventsFactory.create()
            events.append(mandate_events.to_dict())

        response = yield self.anonymous_fetch(
            '/mandate-events/',
            method='GET'
        )

        expect(response.code).to_equal(200)
        mandates_events_loaded = loads(response.body)
        expect(mandates_events_loaded).to_length(5)
        expect(mandates_events_loaded).to_be_like(events)

    @gen_test
    def test_can_add_mandate_events(self):
        mandate = MandateFactory.create()
        mandate_events_type = MandateEventsTypeFactory.create()
        date = date_to_timestamp(datetime.utcnow().date())

        response = yield self.anonymous_fetch(
            '/mandate-events/',
            method='POST',
            body=dumps({
                'date': date,
                'mandate_id': mandate.id,
                'mandate_events_type_id': mandate_events_type.id
            })
        )
        expect(response.code).to_equal(200)
        mandate_events = loads(response.body)
        expect(mandate_events.get('date')).to_equal(date)
        expect(mandate_events.get('mandate')).to_equal(mandate.to_dict())
        expect(mandate_events.get('mandate_events_type')).to_equal(
            mandate_events_type.to_dict()
        )

    @gen_test
    def test_cannot_add_mandate_events_twice(self):
        mandate = MandateFactory.create()
        mandate_events_type = MandateEventsTypeFactory.create()
        date = date_to_timestamp(datetime.utcnow().date())

        yield self.anonymous_fetch(
            '/mandate-events/',
            method='POST',
            body=dumps({
                'date': date,
                'mandate_id': mandate.id,
                'mandate_events_type_id': mandate_events_type.id
            })
        )

        try:
            yield self.anonymous_fetch(
                '/mandate-events/',
                method='POST',
                body=dumps({
                    'date': date,
                    'mandate_id': mandate.id,
                    'mandate_events_type_id': mandate_events_type.id
                })
            )
        except HTTPError as e:
            expect(e).not_to_be_null()
            expect(e.code).to_equal(500)
            expect(e.response.reason).to_be_like('Internal Server Error')

    @gen_test
    def test_cannot_add_mandate_events_without_date(self):
        mandate = MandateFactory.create()
        mandate_events_type = MandateEventsTypeFactory.create()

        try:
            yield self.anonymous_fetch(
                '/mandate-events/',
                method='POST',
                body=dumps({
                    'mandate_id': mandate.id,
                    'mandate_events_type_id': mandate_events_type.id
                })
            )
        except HTTPError as e:
            expect(e).not_to_be_null()
            expect(e.code).to_equal(400)
            expect(e.response.reason).to_be_like('Invalid Mandate Events')

    @gen_test
    def test_cannot_add_mandate_events_without_mandate_id(self):
        mandate_events_type = MandateEventsTypeFactory.create()
        date = date_to_timestamp(datetime.utcnow().date())

        try:
            yield self.anonymous_fetch(
                '/mandate-events/',
                method='POST',
                body=dumps({
                    'date': date,
                    'mandate_events_type_id': mandate_events_type.id
                })
            )
        except HTTPError as e:
            expect(e).not_to_be_null()
            expect(e.code).to_equal(400)
            expect(e.response.reason).to_be_like('Invalid Mandate Events')

    @gen_test
    def test_cannot_add_mandate_events_without_mandate_events_type_id(self):
        mandate = MandateFactory.create()
        date = date_to_timestamp(datetime.utcnow().date())

        try:
            yield self.anonymous_fetch(
                '/mandate-events/',
                method='POST',
                body=dumps({
                    'date': date,
                    'mandate_id': mandate.id,
                })
            )
        except HTTPError as e:
            expect(e).not_to_be_null()
            expect(e.code).to_equal(400)
            expect(e.response.reason).to_be_like('Invalid Mandate Events')
