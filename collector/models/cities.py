# -*- coding: utf-8 -*-
#
# Copyright (c) 2019, Marcelo Jorge Vieira <metal@alucinados.com>
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

from elasticsearch_dsl import Keyword, Text

from .base import BaseModel, CompletionField


class Cities(BaseModel):
    nm_ue = CompletionField()
    sg_uf = Text(fields={'keyword': Keyword()})

    class Index:
        name = 'cities'
        settings = {
            'number_of_shards': 2
        }


def setup_index():
    Cities.init()
