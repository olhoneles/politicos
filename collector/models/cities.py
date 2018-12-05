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

import logging

from elasticsearch_dsl import A, Keyword, Text
from elasticsearch_dsl.connections import connections
from elasticsearch.helpers import bulk

from base import BaseModel, CompletionField
from politicians import Politicians


connections.create_connection(hosts=['localhost'], timeout=20)

OBJECT_LIST_MAXIMUM_COUNTER = 1000


class Cities(BaseModel):
    nm_ue = CompletionField()
    sg_uf = Text(fields={'keyword': Keyword()})

    class Index:
        name = 'cities'
        settings = {
            'number_of_shards': 2
        }

    @classmethod
    def bulk_save(cls, dicts):
        objects = (
            dict(
                d.to_dict(include_meta=True),
                **{'_index': 'cities'}
            )
            for d in dicts
        )
        client = connections.get_connection()
        return bulk(client, objects)


def setup_cities_index():
    Cities.init()

    documents = []
    items = Cities.scan_aggs(
        Politicians.search(),
        {'nm_ue': A('terms', field='nm_ue.keyword')},
        {'sg_uf': A('terms', field='sg_uf.keyword')}
    )

    total = 0
    for item in items:
        city = Cities(nm_ue=item.key.nm_ue, sg_uf=item.sg_uf.buckets[0]['key'])
        documents.append(city)
        if total >= OBJECT_LIST_MAXIMUM_COUNTER:
            Cities.bulk_save(documents)
            logging.info(f'Added {OBJECT_LIST_MAXIMUM_COUNTER} items')
            documents = []
            total = 0
        total += 1

    if documents:
        Cities.bulk_save(documents)
        logging.info(f'Added {total} items')
        documents = []


if __name__ == '__main__':
    setup_cities_index()
