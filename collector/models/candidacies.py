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

from elasticsearch_dsl import Document, Q, Integer, Keyword, Search, Text
from elasticsearch_dsl.connections import connections
from elasticsearch.helpers import bulk


connections.create_connection(hosts=['localhost'], timeout=20)

OBJECT_LIST_MAXIMUM_COUNTER = 5000
INDEX_NAME = 'candidacies'


class Candidacies(Document):

    ano_eleicao = Integer()
    ds_cargo = Text(fields={'keyword': Keyword()})
    ds_sit_tot_turno = Text(fields={'keyword': Keyword()})
    nm_ue = Text(fields={'keyword': Keyword()})
    nr_cpf_candidato = Text(fields={'keyword': Keyword()})
    sg_uf = Text(fields={'keyword': Keyword()})

    class Index:
        name = INDEX_NAME
        settings = {
            'number_of_shards': 2
        }

    @classmethod
    def bulk_save(cls, dicts):
        objects = (
            dict(
                d.to_dict(include_meta=True),
                **{'_index': INDEX_NAME}
            )
            for d in dicts
        )
        client = connections.get_connection()
        return bulk(client, objects)


# https://github.com/elastic/elasticsearch-dsl-py/blob/master/examples/composite_agg.py
def scan_aggs(search, source_aggs, inner_aggs={}, size=10):
    def run_search(**kwargs):
        s = search[:0]
        s.aggs.bucket(
            'comp', 'composite', sources=source_aggs, size=size, **kwargs
        )
        for agg_name, agg in inner_aggs.items():
            s.aggs['comp'][agg_name] = agg
        return s.execute()

    response = run_search()
    while response.aggregations.comp.buckets:
        for b in response.aggregations.comp.buckets:
            yield b
        if 'after_key' in response.aggregations.comp:
            after = response.aggregations.comp.after_key
        else:
            after= response.aggregations.comp.buckets[-1].key
        response = run_search(after=after)


def main():
    Candidacies.init()

    documents = []
    s = Search(index='politicians')
    s.query = Q('bool', must_not=[Q('match', nr_cpf_candidato='#NULO#')])
    for x in s.scan():
        candidacy = Candidacies(
            nr_cpf_candidato=x['nr_cpf_candidato'],
            ano_eleicao=x['ano_eleicao'],
            ds_sit_tot_turno=x['ds_sit_tot_turno'],
            nm_ue=x['nm_ue'],
            sg_uf=x['sg_uf'],
            ds_cargo=x['ds_cargo']
        )
        documents.append(candidacy)
        if len(documents) == OBJECT_LIST_MAXIMUM_COUNTER:
            Candidacies.bulk_save(documents)
            logging.info(f'Added {OBJECT_LIST_MAXIMUM_COUNTER} items')
            documents = []
    if documents:
        Candidacies.bulk_save(documents)
        logging.info(f'Added {len(documents)} items')
        documents = []


if __name__ == '__main__':
    main()
