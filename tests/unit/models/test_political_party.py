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

from tests.unit.base import ApiTestCase
from tests.fixtures import PoliticalPartyFactory


class TestPoliticalParty(ApiTestCase):

    def test_can_create_political_party(self):
        political_party = PoliticalPartyFactory.create(
            siglum='HMP',
            name='Hevy Metal Party',
            wikipedia='http://metalparty.com/'
        )

        expect(political_party.id).not_to_be_null()
        expect(political_party.siglum).to_equal('HMP')
        expect(political_party.name).to_equal('Hevy Metal Party')
        expect(political_party.wikipedia).to_equal('http://metalparty.com/')

    def test_can_convert_to_dict(self):
        political_party = PoliticalPartyFactory.create()
        political_party_dict = political_party.to_dict()

        expect(political_party_dict['siglum']).to_equal(political_party.siglum)
        expect(political_party_dict['name']).to_equal(political_party.name)
        expect(political_party_dict['wikipedia']).to_equal(
            political_party.wikipedia
        )
