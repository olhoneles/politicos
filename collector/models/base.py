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

from elasticsearch_dsl import analyzer, Completion, Keyword, Text, Document
from elasticsearch_dsl.connections import connections
from elasticsearch.helpers import bulk


connections.create_connection(hosts=['localhost'], timeout=20)

brazilian_analyzer = analyzer('brazilian')


class CompletionField(Text):
    def __init__(self, *args, **kwargs):
        kwargs['fields'] = {
            'keyword': Keyword(),
            'suggest': Completion(
                analyzer=brazilian_analyzer,
                preserve_separators=False,
                preserve_position_increments=False,
            )
        }
        super(CompletionField, self).__init__(*args, **kwargs)


class BaseModel(Document):

    @classmethod
    def bulk_save(cls, dicts):
        objects = (
            dict(
                d.to_dict(include_meta=True),
                **{'_index': cls.Index.name}
            )
            for d in dicts
        )
        client = connections.get_connection()
        return bulk(client, objects)
