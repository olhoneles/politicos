# -*- coding: utf-8 -*-
#
# Copyright (c) 2018, Marcelo Jorge Vieira <metal@alucinados.com>
#
#  This program is free software: you can redistribute it and/or modify it
#  under the terms of the GNU Affero General Public License as published by the
#  Free Software Foundation, either version 3 of the License, or (at your
#  option) any later version.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License
#  for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program. If not, see <http://www.gnu.org/licenses/>.

from tornado.options import options

from politicos_api.cache import cache
from politicos_api.handlers.base import BaseHandler
from collector.models.politicians import Politicians


class CandidaciesHandler(BaseHandler):

    @cache(5)
    async def get(self):
        # FIXME: scroll api?
        body = {
            'from': self.per_page * (self.page - 1),
        }

        errors = []
        # mapping = await self.es.indices.get_mapping(index=options.es_index)
        for field in self.query_arguments:
            if not Politicians._doc_type.mapping.resolve_field(field):
                errors.append({field: 'Invalid Attribute'})
        if errors:
            errors = dict(errors=errors)
            return await self.json_response(errors, 422)

        # FIXME
        if self.query_arguments:
            items = [
                {'match': {x: y}} for x, y in self.query_arguments.items()
            ]
            body.update({'query': {'bool': {'must': items}}})

        result = await self.es.search(
            index=options.es_index,
            # filter_path=['hits.hits.*'],
            body=body,
            size=self.per_page,
        )

        response = {
            'meta': self.get_meta(result),
            'objects': [
                x.get('_source')
                for x in result.get('hits', {}).get('hits', {})
            ]
        }
        await self.json_response(response)
