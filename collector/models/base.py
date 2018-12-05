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

from elasticsearch_dsl import analyzer, Document, Completion, Keyword, Text


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

    # https://github.com/elastic/elasticsearch-dsl-py/blob/master/examples/composite_agg.py
    @classmethod
    def scan_aggs(cls, search, source_aggs, inner_aggs={}, size=10):
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
