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

from tornado.gen import coroutine

from ujson import loads

from politicos.models import PoliticalParty
from politicos.handlers import BaseHandler


class PoliticalPartyHandler(BaseHandler):

    @coroutine
    def get(self, siglum):
        query = self.db.query(PoliticalParty)
        political_party = query.filter(PoliticalParty.siglum == siglum).first()
        if not political_party:
            self.write('{}')
            return

        result = political_party.to_dict()
        self.write_json(result)


class AllPoliticalPartyHandler(BaseHandler):

    @coroutine
    def get(self):
        query = self.db.query(PoliticalParty)
        political_party = query.order_by(PoliticalParty.name.asc()).all()

        if not political_party:
            self.write('{}')
            return

        result = [x.to_dict() for x in political_party]
        self.write_json(result)

    @coroutine
    def post(self):
        post_data = loads(self.request.body)

        name = post_data.get('name')
        siglum = post_data.get('siglum')

        if not name or not siglum:
            self.set_status(400, 'Invalid political party.')
            return

        data = {
            'name': name,
            'siglum': siglum,
            'wikipedia': post_data.get('wikipedia'),
            'website': post_data.get('website'),
            'founded_date': post_data.get('founded_date'),
            'logo': post_data.get('logo'),
        }

        siglum = PoliticalParty.add_political_party(self.db, data)
        self.write_json({'siglum': siglum})
