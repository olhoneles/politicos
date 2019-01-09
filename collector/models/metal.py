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
from collections import defaultdict

from elasticsearch_dsl import (
    Boolean, Q, Search, InnerDoc, Integer, Nested, Text
)
from elasticsearch_dsl.connections import connections
from elasticsearch.helpers import bulk
from pycpfcnpj import cpfcnpj

from politicians import Politicians


connections.create_connection(hosts=['localhost'], timeout=20)

OBJECT_LIST_MAXIMUM_COUNTER = 3000
INDEX_NAME = 'metal'


# FIXME
FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(
    format=FORMAT,
    level=logging.INFO
)
# mute elasticsearch INFO logs
log = logging.getLogger('elasticsearch')
log.setLevel('ERROR')



class Source(InnerDoc):
    filename = Text()
    line = Integer()


class Candidacies(InnerDoc):
    ano_eleicao = Integer()
    ds_sit_tot_turno = Text()
    nm_ue = Text()
    sg_uf = Text()
    ds_cargo = Text()
    source = Nested(Source)


class Metal(Politicians):

    candidacies = Nested(Candidacies)
    nr_cpf_candidato_validado = Boolean()

    def add_candidacies(
            self, ano_eleicao, ds_sit_tot_turno, nm_ue, sg_uf, ds_cargo,
            source):

        self.candidacies.append(
            Candidacies(
                ano_eleicao=ano_eleicao,
                ds_sit_tot_turno=ds_sit_tot_turno,
                nm_ue=nm_ue, sg_uf=sg_uf,
                ds_cargo=ds_cargo,
                source=source,
            )
        )

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


def insert_documents(candidacies):
    '''Group by cpf and get the last candidacy year'''

    logging.info(f'Getting the last year...')

    # FIXME
    ids = [i for i in candidacies.keys()]

    # FIXME
    search = Search(index='politicians')
    search = search.filter('terms', nr_cpf_candidato=ids)
    search.aggs \
        .bucket(
            'politicians',
            'terms',
            field='nr_cpf_candidato.keyword',
            size=OBJECT_LIST_MAXIMUM_COUNTER,
        ) \
        .metric(
            'candidacies',
            'top_hits',
            size=1,
            sort=[{'ano_eleicao': 'desc'}],
        )

    response = search.execute()

    documents = []
    for bucket in response.aggregations.politicians.buckets:
        for x in bucket.candidacies:
            data = x.to_dict()
            cpf = data['nr_cpf_candidato']
            metal = Metal(**data)
            metal.nr_cpf_candidato_validado = cpfcnpj.validate(cpf)
            for m in candidacies[cpf]:
                metal.add_candidacies(**m)
            documents.append(metal)
    logging.info(f'Added {len(documents)} items...')
    metal.bulk_save(documents)
    documents = []


def main():
    Metal.init()

    logging.info(f'Getting unique CPFs...')
    # FIXME: memory, index or query?
    candidacies_by_cpf= defaultdict(list)  # ~42 MB in RAM (41943152 bytes)
    s = Search(index='politicians')
    s.query = Q('bool', must_not=[Q('match', nr_cpf_candidato='#NULO#')])
    for x in s.scan():
        cpf = x['nr_cpf_candidato']
        candidacies_by_cpf[cpf].append({
            'ano_eleicao': x['ano_eleicao'],
            'ds_sit_tot_turno': x['ds_sit_tot_turno'],
            'nm_ue': x['nm_ue'],
            'sg_uf': x['sg_uf'],
            'ds_cargo': x['ds_cargo'],
            'source': x['source'],
        })

    total = 0
    data = defaultdict(list)
    for candidacy in candidacies_by_cpf:
        if total > OBJECT_LIST_MAXIMUM_COUNTER:
            insert_documents(data)
            total = 0
            data = defaultdict(list)
        data[candidacy] = candidacies_by_cpf[candidacy]
        total += 1
    insert_documents(data)


if __name__ == '__main__':
    main()
