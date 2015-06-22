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

from datetime import datetime, timedelta

from ujson import loads, dumps
from preggy import expect
from tornado.testing import gen_test
from tornado.httpclient import HTTPError

from politicos.utils import date_to_timestamp
from tests.unit.base import ApiTestCase
from tests.fixtures import InstitutionFactory, LegislatureFactory


class TestAllLegislaturesHandler(ApiTestCase):

    @gen_test
    def test_can_get_empty_legislature_info(self):
        response = yield self.anonymous_fetch(
            '/legislatures/',
            method='GET'
        )

        expect(response.code).to_equal(200)
        legislature = loads(response.body)
        expect(legislature).to_equal({})
        expect(legislature).to_length(0)

    @gen_test
    def test_can_get_all_legislatures(self):
        legislatures = []
        for x in range(5):
            legislature = LegislatureFactory.create()
            legislatures.append(legislature.to_dict())

        response = yield self.anonymous_fetch(
            '/legislatures/',
            method='GET'
        )

        expect(response.code).to_equal(200)
        legislatures_loaded = loads(response.body)
        expect(legislatures_loaded).to_length(5)
        expect(legislatures_loaded).to_be_like(legislatures)

    @gen_test
    def test_can_add_legislature(self):
        institution = InstitutionFactory.create()

        now = datetime.utcnow()
        date_start = date_to_timestamp(now.date())
        date_end = date_to_timestamp((now + timedelta(days=10)).date())

        response = yield self.anonymous_fetch(
            '/legislatures/',
            method='POST',
            body=dumps({
                'date_start': date_start,
                'date_end': date_end,
                'institution_id': institution.id,
            })
        )
        expect(response.code).to_equal(200)
        legislature = loads(response.body)
        expect(legislature.get('date_start')).to_equal(date_start)
        expect(legislature.get('date_end')).to_equal(date_end)
        expect(legislature.get('institution')).to_equal(institution.to_dict())

    @gen_test
    def test_cannot_add_legislature_twice(self):
        institution = InstitutionFactory.create()
        now = datetime.utcnow()
        date_start = date_to_timestamp(now.date())
        date_end = date_to_timestamp((now + timedelta(days=10)).date())

        yield self.anonymous_fetch(
            '/legislatures/',
            method='POST',
            body=dumps({
                'date_start': date_start,
                'date_end': date_end,
                'institution_id': institution.id,
            })
        )

        try:
            yield self.anonymous_fetch(
                '/legislatures/',
                method='POST',
                body=dumps({
                    'date_start': date_start,
                    'date_end': date_end,
                    'institution_id': institution.id,
                })
            )
        except HTTPError as e:
            expect(e).not_to_be_null()
            expect(e.code).to_equal(500)
            expect(e.response.reason).to_be_like('Internal Server Error')

    @gen_test
    def test_cannot_add_legislature_without_date_start(self):
        institution = InstitutionFactory.create()
        now = datetime.utcnow()
        date_end = date_to_timestamp((now + timedelta(days=10)).date())

        try:
            yield self.anonymous_fetch(
                '/legislatures/',
                method='POST',
                body=dumps({
                    'date_end': date_end,
                    'institution_id': institution.id,
                })
            )
        except HTTPError as e:
            expect(e).not_to_be_null()
            expect(e.code).to_equal(400)
            expect(e.response.reason).to_be_like('Invalid Legislature')

    @gen_test
    def test_cannot_add_legislature_without_date_end(self):
        institution = InstitutionFactory.create()
        now = datetime.utcnow()
        date_start = date_to_timestamp(now.date())

        try:
            yield self.anonymous_fetch(
                '/legislatures/',
                method='POST',
                body=dumps({
                    'date_start': date_start,
                    'institution_id': institution.id,
                })
            )
        except HTTPError as e:
            expect(e).not_to_be_null()
            expect(e.code).to_equal(400)
            expect(e.response.reason).to_be_like('Invalid Legislature')

    @gen_test
    def test_cannot_add_legislature_without_institution(self):
        now = datetime.utcnow()
        date_start = date_to_timestamp(now.date())
        date_end = date_to_timestamp((now + timedelta(days=10)).date())

        try:
            yield self.anonymous_fetch(
                '/legislatures/',
                method='POST',
                body=dumps({
                    'date_start': date_start,
                    'date_end': date_end,
                })
            )
        except HTTPError as e:
            expect(e).not_to_be_null()
            expect(e.code).to_equal(400)
            expect(e.response.reason).to_be_like('Invalid Legislature')
