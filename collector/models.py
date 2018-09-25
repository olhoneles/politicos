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
    analyzer, Date, Document, Index, Integer, InnerDoc, Keyword, Nested, Text
)
from elasticsearch_dsl.connections import connections


# Define a default Elasticsearch client
connections.create_connection()

INDEX_NAME = 'politicians'

text_analyzer = analyzer(
    'text_analyzer',
    tokenizer='standard',
    filter=['standard', 'lowercase', 'stop', 'snowball'],
    char_filter=['html_strip']
)


class Source(InnerDoc):
    filename = Text()
    line = Integer()


class Politicians(Document):
    source = Nested(Source)
    # CSV fields
    ano_eleicao = Integer(required=True)
    codigo_cargo = Text(fields={'keyword': Keyword()})
    codigo_cor_raca = Text(fields={'keyword': Keyword()})
    codigo_estado_civil = Text(fields={'keyword': Keyword()})
    codigo_legenda = Text(fields={'keyword': Keyword()})
    codigo_municipio_nascimento = Text(fields={'keyword': Keyword()})
    codigo_nacionalidade = Text(fields={'keyword': Keyword()})
    codigo_ocupacao = Text(fields={'keyword': Keyword()})
    codigo_sexo = Text(fields={'keyword': Keyword()})
    cod_grau_instrucao = Text(fields={'keyword': Keyword()})
    cod_situacao_candidatura = Text(fields={'keyword': Keyword()})
    cod_sit_tot_turno = Text(fields={'keyword': Keyword()})
    composicao_legenda = Text(fields={'keyword': Keyword()})
    cpf_candidato = Text(fields={'keyword': Keyword()})
    data_geracao = Date()
    data_nascimento = Text(fields={'keyword': Keyword()})
    descricao_cargo = Text(fields={'keyword': Keyword()})
    descricao_cor_raca = Text(fields={'keyword': Keyword()})
    descricao_eleicao = Text(fields={'keyword': Keyword()})
    descricao_estado_civil = Text(fields={'keyword': Keyword()})
    descricao_grau_instrucao = Text(fields={'keyword': Keyword()})
    descricao_nacionalidade = Text(fields={'keyword': Keyword()})
    descricao_ocupacao = Text(fields={'keyword': Keyword()})
    descricao_sexo = Text(fields={'keyword': Keyword()})
    descricao_ue = Text(fields={'keyword': Keyword()})
    desc_sit_tot_turno = Text(fields={'keyword': Keyword()})
    despesa_max_campanha = Text(fields={'keyword': Keyword()})
    des_situacao_candidatura = Text(fields={'keyword': Keyword()})
    hora_geracao = Text(fields={'keyword': Keyword()})
    idade_data_eleicao = Text(fields={'keyword': Keyword()})
    nm_email = Text(fields={'keyword': Keyword()})
    nome_candidato = Text(fields={'keyword': Keyword()})
    nome_legenda = Text(fields={'keyword': Keyword()})
    nome_municipio_nascimento = Text(
        fields={'keyword': Keyword()},
        analyzer=text_analyzer
    )
    nome_partido = Text(fields={'keyword': Keyword()})
    nome_urna_candidato = Text(fields={'keyword': Keyword()})
    numero_candidato = Text(fields={'keyword': Keyword()})
    numero_partido = Text(fields={'keyword': Keyword()})
    num_titulo_eleitoral_candidato = Text(fields={'keyword': Keyword()})
    num_turno = Text(fields={'keyword': Keyword()})
    sequencial_candidato = Text(fields={'keyword': Keyword()})
    sigla_legenda = Text(fields={'keyword': Keyword()})
    sigla_partido = Text(fields={'keyword': Keyword()})
    sigla_ue = Text(fields={'keyword': Keyword()})
    sigla_uf = Text(fields={'keyword': Keyword()})
    sigla_uf_nascimento = Text(fields={'keyword': Keyword()})

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

    index.analyzer(text_analyzer)

    index_template = Politicians._index.as_template(
        INDEX_NAME,
        f'{INDEX_NAME}-*',
    )
    index_template.save()
