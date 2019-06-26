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


class PoliticalOfficesHandler(BaseHandler):

    # political_offices = [
    #     {'name': 'Presidente', 'term': 4},
    #     {'name': 'Vice-Presidente', 'term': 4},
    #     {'name': 'Governador', 'term': 4},
    #     {'name': 'Vice-Governador', 'term': 4},
    #     {'name': 'Deputado Federal', 'term': 4},
    #     {'name': 'Deputado Estadual', 'term': 4},
    #     {'name': 'Deputado Distrital', 'term': 4},
    #     {'name': 'Prefeito', 'term': 4},
    #     {'name': 'Vice-Prefeito', 'term': 4},
    #     {'name': 'Vereador', 'term': 4},
    #     {'name': 'Senador', 'term': 8},
    #     {'name': 'Senador 1º Suplente', 'term': 8},
    #     {'name': 'Senador 2º Suplente', 'term': 8},
    # ]

    @cache()
    async def get(self):
        response = await self.agg_query([
            'cd_cargo',
            'ds_cargo',
        ])
        await self.json_response(response)


class PoliticalOfficesSuggestHandler(BaseHandler):

    @cache()
    async def get(self):
        await self.suggest_response('ds_cargo', ['cd_cargo'])
