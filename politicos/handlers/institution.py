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

from politicos.models.institution import Institution
from politicos.handlers import BaseHandler


class InstitutionHandler(BaseHandler):

    @coroutine
    def get(self, siglum):
        query = self.db.query(Institution)
        institution = query.filter(Institution.siglum == siglum).first()
        if not institution:
            self.write('{}')
            return

        result = institution.to_dict()
        self.write_json(result)


class AllInstitutionsHandler(BaseHandler):

    @coroutine
    def get(self):
        query = self.db.query(Institution)
        institutions = query.order_by(Institution.name.asc()).all()

        if not institutions:
            self.write('{}')
            return

        result = [x.to_dict() for x in institutions]
        self.write_json(result)

    @coroutine
    def post(self):
        post_data = loads(self.request.body)

        name = post_data.get('name')
        siglum = post_data.get('siglum')

        if not name or not siglum:
            self.set_status(400, 'Invalid Institution')
            return

        data = {
            'name': name,
            'siglum': siglum,
            'logo': post_data.get('logo'),
        }

        institution = Institution.add_institution(self.db, data)
        self.write_json(institution.to_dict())
