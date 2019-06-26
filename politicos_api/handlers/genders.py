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

from politicos_api.cache import cache
from politicos_api.handlers.base import BaseHandler


class GenderHandler(BaseHandler):

    @cache()
    async def get(self):
        response = await self.agg_query([
            'cd_genero',
            'ds_genero',
        ])
        await self.json_response(response)


class GenderSuggestHandler(BaseHandler):

    @cache()
    async def get(self):
        await self.suggest_response('ds_genero', ['cd_genero'])
