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

from elasticsearch.helpers import bulk
from elasticsearch_dsl import (
    analyzer, Date, Document, Index, Integer, InnerDoc, Keyword, Nested,
    Short, Text
)
from elasticsearch_dsl.connections import connections


INDEX_NAME = 'politicians'


class Source(InnerDoc):
    filename = Text()
    line = Integer()


class UnidadeEleitoral(InnerDoc):
    bandeira = Text()


class Politicians(Document):
    source = Nested(Source)
    unidade_eleitoral = Nested(UnidadeEleitoral)
    foto_url = Text()
    # CSV fields
    ano_eleicao = Integer(required=True)
    cd_cargo = Text(fields={'keyword': Keyword()})
    cd_cor_raca = Text(fields={'keyword': Keyword()})
    cd_estado_civil = Text(fields={'keyword': Keyword()})
    codigo_legenda = Text(fields={'keyword': Keyword()})
    cd_municipio_nascimento = Text(fields={'keyword': Keyword()})
    cd_nacionalidade = Text(fields={'keyword': Keyword()})
    cd_ocupacao = Text(fields={'keyword': Keyword()})
    cd_genero = Text(fields={'keyword': Keyword()})
    cd_grau_instrucao = Text(fields={'keyword': Keyword()})
    cd_situacao_candidatura = Text(fields={'keyword': Keyword()})
    cd_sit_tot_turno = Text(fields={'keyword': Keyword()})
    composicao_legenda = Text(fields={'keyword': Keyword()})
    nr_cpf_candidato = Text(fields={'keyword': Keyword()})
    dt_geracao = Date()
    dt_nascimento = Text(fields={'keyword': Keyword()})
    ds_cargo = Text(fields={'keyword': Keyword()})
    ds_cor_raca = Text(fields={'keyword': Keyword()})
    ds_eleicao = Text(fields={'keyword': Keyword()})
    ds_estado_civil = Text(fields={'keyword': Keyword()})
    ds_grau_instrucao = Text(fields={'keyword': Keyword()})
    ds_nacionalidade = Text(fields={'keyword': Keyword()})
    ds_ocupacao = Text(fields={'keyword': Keyword()})
    ds_genero = Text(fields={'keyword': Keyword()})
    nm_ue = Text(fields={'keyword': Keyword()})
    ds_sit_tot_turno = Text(fields={'keyword': Keyword()})
    nr_despesa_max_campanha = Text(fields={'keyword': Keyword()})
    ds_situacao_candidatura = Text(fields={'keyword': Keyword()})
    hr_geracao = Text(fields={'keyword': Keyword()})
    idade_data_eleicao = Text(fields={'keyword': Keyword()})
    nm_email = Text(fields={'keyword': Keyword()})
    nm_candidato = Text(fields={'keyword': Keyword()})
    nome_legenda = Text(fields={'keyword': Keyword()})
    nm_municipio_nascimento = Text(fields={'keyword': Keyword()})
    nm_partido = Text(fields={'keyword': Keyword()})
    nm_urna_candidato = Text(fields={'keyword': Keyword()})
    nr_candidato = Text(fields={'keyword': Keyword()})
    nr_partido = Text(fields={'keyword': Keyword()})
    nr_titulo_eleitoral_candidato = Text(fields={'keyword': Keyword()})
    nr_turno = Text(fields={'keyword': Keyword()})
    sq_candidato = Text(fields={'keyword': Keyword()})
    sigla_legenda = Text(fields={'keyword': Keyword()})
    sg_partido = Text(fields={'keyword': Keyword()})
    sg_ue = Text(fields={'keyword': Keyword()})
    sg_uf = Text(fields={'keyword': Keyword()})
    sg_uf_nascimento = Text(fields={'keyword': Keyword()})
    # 2018
    cd_detalhe_situacao_cand = Integer()
    cd_eleicao = Integer()
    cd_tipo_eleicao = Short()
    ds_detalhe_situacao_cand = Text(fields={'keyword': Keyword()})
    dt_eleicao = Text(fields={'keyword': Keyword()})
    nm_social_candidato = Text(fields={'keyword': Keyword()})
    nm_tipo_eleicao = Text(fields={'keyword': Keyword()})
    nr_idade_data_posse = Short()
    nr_processo = Text(fields={'keyword': Keyword()})
    nr_protocolo_candidatura = Text(fields={'keyword': Keyword()})
    st_declarar_bens = Text(fields={'keyword': Keyword()})
    st_reeleicao = Text(fields={'keyword': Keyword()})
    tp_abrangencia = Text(fields={'keyword': Keyword()})
    tp_agremiacao = Text(fields={'keyword': Keyword()})

    @classmethod
    def set_index_name(cls, year):
        return f'{INDEX_NAME}-{year}'

    def save(self, **kwargs):
        kwargs['index'] = Politicians.set_index_name(self.ano_eleicao)
        return super(Politicians, self).save(**kwargs)

    @classmethod
    def bulk_save(cls, dicts):
        objects = (
            dict(
                d.to_dict(include_meta=True),
                **{'_index': cls.set_index_name(int(d.ano_eleicao))}
            )
            for d in dicts
        )
        client = connections.get_connection()
        return bulk(client, objects)

    @classmethod
    def bulk_update(cls, dicts, client=None):
        def upsert(doc):
            d = doc.to_dict(True)
            d['_op_type'] = 'update'
            d['doc'] = d['_source']
            d['doc_as_upsert'] = True
            del d['_source']
            return d
        client = client or connections.get_connection()
        return bulk(client, (upsert(d) for d in dicts))


def setup_indices():
    index = Index(f'{INDEX_NAME}-index')

    index.settings(
        number_of_shards=1,
        number_of_replicas=0
    )

    index.aliases(
        politicians={}
    )

    index.document(Politicians)

    index.analyzer(analyzer('brazilian'))

    index_template = Politicians._index.as_template(
        INDEX_NAME,
        f'{INDEX_NAME}-*',
    )
    index_template.save()
