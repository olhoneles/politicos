#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2015, Marcelo Jorge Vieira <metal@alucinados.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging

import requests
from ujson import dumps
from SPARQLWrapper import SPARQLWrapper, JSON


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

sparql = SPARQLWrapper("http://pt.dbpedia.org/sparql")
sparql.setQuery("""
SELECT DISTINCT ?tse, ?s, ?wikipedia, ?label, ?thumbnail, ?found, ?foundpt, ?website, ?nameNative
WHERE {
    ?s rdf:type <http://dbpedia.org/ontology/PoliticalParty> .

    OPTIONAL {
        ?s foaf:isPrimaryTopicOf ?wikipedia  .
    }

    OPTIONAL {
        ?s rdfs:label ?label .
        FILTER (
            langMatches( lang(?label), "PT" )
        )
    }

    OPTIONAL {
        ?s dbpedia-owl:thumbnail ?thumbnail .
    }

    OPTIONAL {
        ?s dbpprop:nameNative ?nameNative
    }

    ?s <http://pt.dbpedia.org/property/numeroTse> ?tse

    OPTIONAL {
        ?s dbpprop:fundado ?found .
    }

    OPTIONAL {
        ?s dbpprop-pt:fundado ?foundpt .
    }

    OPTIONAL {
        ?s  dbpprop-pt:website ?website .
    }
}
order by ?tse
limit 1000
""")

sparql.setReturnFormat(JSON)
results = sparql.query().convert()

parties = list()


for result in results["results"]["bindings"]:
    # print(result["label"]["value"])
    # print result

    try:
        tse_number = int(result.get('tse', {}).get('value'))
    except ValueError:
        tse_number = None

    website = result.get('website', {}).get('value')
    if website and not website.startswith('http'):
        website = None

    try:
        # FIXME
        from random import randint
        siglum = randint(0, 10000)

        political_party = {
            'siglum': siglum,
            'name': result.get('label', {}).get('value').split('(')[0].strip(),
            'tse_number': tse_number,
            'wikipedia': result.get('wikipedia', {}).get('value'),
            'website': website,
        }
        parties.append(political_party)

        resp = requests.put(
            'http://localhost:2368/political-parties/',
            data=dumps(political_party)
        )
        if resp.status_code == 200:
            logging.info(
                'Added political party: "%s"', political_party.get('name')
            )
        else:
            logging.info(
                'Error when add political party: "%s"',
                political_party.get('name')
            )
    except Exception as e:
        logging.info(
            'Error when add political party: "%s". Details: %s',
            political_party.get('siglum'), str(e)
        )
