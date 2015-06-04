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

from ujson import loads
from preggy import expect
from tornado.testing import gen_test

from tests.unit.base import ApiTestCase
from tests.fixtures import PoliticalPartyFactory


class TestPoliticalPartyHandler(ApiTestCase):

    @gen_test
    def test_cannot_get_political_party_info(self):
        response = yield self.anonymous_fetch(
            '/political-party/PBA',
            method='GET'
        )
        expect(response.code).to_equal(200)
        political_party = loads(response.body)
        expect(political_party).to_equal({})
        expect(political_party).to_length(0)

    @gen_test
    def test_can_get_political_party_info(self):
        PoliticalPartyFactory.create(name='Partido Blah', siglum='PBA')

        response = yield self.anonymous_fetch(
            '/political-party/PBA',
            method='GET'
        )
        expect(response.code).to_equal(200)
        political_party = loads(response.body)
        expect(political_party).to_length(6)
        expect(political_party.get('name')).to_equal("Partido Blah")
        expect(political_party.get('siglum')).to_equal("PBA")


class TestAllPoliticalPartyHandler(ApiTestCase):

    @gen_test
    def test_cannot_get_political_party_info(self):
        response = yield self.anonymous_fetch(
            '/political-party/',
            method='GET'
        )

        expect(response.code).to_equal(200)
        political_party = loads(response.body)
        expect(political_party).to_equal({})
        expect(political_party).to_length(0)

    @gen_test
    def test_can_get_all_political_parties(self):
        political_parties = []
        for x in range(5):
            party = PoliticalPartyFactory.create(
                name='Partido %s' % x,
                siglum='%s' % x,
                founded_date=None,
            )
            political_parties.append(party.to_dict())

        response = yield self.anonymous_fetch(
            '/political-party/',
            method='GET'
        )

        expect(response.code).to_equal(200)
        political_parties_loaded = loads(response.body)
        expect(political_parties_loaded).to_length(5)
        expect(political_parties_loaded).to_be_like(political_parties)
