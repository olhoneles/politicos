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

from elasticsearch.helpers import bulk
from elasticsearch_dsl import InnerDoc, Integer, Keyword, Nested, Text
from elasticsearch_dsl.connections import connections

from .politicians import Politicians


INDEX_NAME = 'candidacies'


class Candidacies(InnerDoc):
    ano_eleicao = Integer()
    ds_cargo = Text(fields={'keyword': Keyword()})
    ds_sit_tot_turno = Text(fields={'keyword': Keyword()})
    nm_ue = Text(fields={'keyword': Keyword()})
    sg_uf = Text(fields={'keyword': Keyword()})


class PoliticianCandidacies(Politicians):
    candidacies = Nested(Candidacies)

    class Index:
        name = INDEX_NAME
        settings = {
            'number_of_shards': 2
        }

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


def setup_index():
    PoliticianCandidacies.init()
