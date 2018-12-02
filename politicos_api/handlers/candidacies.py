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

from collections import defaultdict

from tornado.options import options

from politicos_api.cache import cache
from politicos_api.handlers.base import BaseHandler
from collector.models import Politicians


class CandidaciesHandler(BaseHandler):

    @cache(5)
    async def get(self):
        # FIXME: scroll api?
        body = {
            'from': self.per_page * (self.page - 1),
        }

        errors = []
        # mapping = await self.es.indices.get_mapping(index=options.es_index)
        for field in self.query_arguments:
            if not Politicians._doc_type.mapping.resolve_field(field):
                errors.append({field: 'Invalid Attribute'})
        if errors:
            errors = dict(errors=errors)
            return await self.json_response(errors, 422)

        # FIXME: wrong data
        body.update({
            'query': {
                'bool': {
                    'must_not': [
                        {'match': {'nr_cpf_candidato': '#NULO#'}},
                        {'match': {'nr_cpf_candidato': '00000000000'}},
                        {'match': {'nr_cpf_candidato': '99999999999'}}
                    ]
                },
            }
        })

        # FIXME: array of items
        if self.query_arguments:
            items = [
                {'match': {x: y}} for x, y in self.query_arguments.items()
            ]
            body.update({
                'query': {
                    'bool': {'must': items},
                }
            })

        body.update({
            'size': 0,
            'aggs': {
                'politicians': {
                    'terms': {
                        'field': 'nr_cpf_candidato.keyword',
                        'size': self.per_page
                    },
                    'aggs': {
                        'candidacies': {
                            'top_hits': {
                                'size': 1,
                                'sort': [{
                                    'ano_eleicao': {
                                        'order': 'desc'
                                    }
                                }],
                            }
                        }
                    }
                }
            }
        })

        result = await self.es.search(
            index=options.es_index,
            body=body,
        )

        buckets = result \
            .get('aggregations', {}) \
            .get('politicians', {}) \
            .get('buckets', [])
        objects = []
        politicians = []
        for bucket in buckets:
            hits = bucket.get('candidacies', {}).get('hits',{}).get('hits', [])
            for hit in hits:
                source = hit.get('_source')
                politicians.append(source.get('nr_cpf_candidato'))
                objects.append(source)

        # FIXME: size
        candidacies_query = {
            'size': 1000,
            '_source': [
                'ds_sit_tot_turno',
                'nr_turno',
                'ano_eleicao',
                'nr_cpf_candidato',
                'nm_ue',
                'sg_uf',
                'ds_cargo'

            ],
            'query': {
                'bool': {
                    'must': [{
                        'terms': {'nr_cpf_candidato.keyword': politicians}
                    }]
                }
            }
        }

        result = await self.es.search(
            index=options.es_index,
            body=candidacies_query,
        )

        candidacies = defaultdict(list)
        for hits in result.get('hits', {}).get('hits', []):
            cpf = hits.get('_source', {}).get('nr_cpf_candidato')
            source = hits.get('_source', {})
            del source['nr_cpf_candidato']
            candidacies[cpf].append(source)

        for x in objects:
            x['candidacies'] = candidacies[x.get('nr_cpf_candidato')]

        response = {
            'meta': self.get_meta(result),
            'objects': objects,
        }

        await self.json_response(response)
