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
import lxml.html
from ujson import dumps

# Requirements: requests, cssselect, lxml, usjon

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


def formatter(name):
    return name.text_content().replace('\n', '').strip()


def xtitle(name):
    skip_list = ['e', 'de', 'do', 'da', 'dos']
    name = name.lower()
    word_list = name.split(' ')
    final = [word_list[0].capitalize()]
    for word in word_list[1:]:
        final.append(word in skip_list and word or word.capitalize())
    return ' '.join(final)


url = 'http://www.tse.jus.br/partidos/partidos-politicos'
response = requests.get(url)

if response.status_code != 200:
    exit(0)

data = lxml.html.fromstring(response.content)
trs = data.cssselect('table tr')
parties = list()
trs.pop(0)
for row in trs:
    try:
        _, siglum, name, _, _, tse_number = row.getchildren()
        political_party = {
            'siglum': formatter(siglum),
            'name': xtitle(formatter(name)),
            'tse_number': formatter(tse_number)
        }
        parties.append(political_party)

        resp = requests.post(
            'http://localhost:2368/political-parties/',
            data=dumps(political_party)
        )
        if resp.status_code == 200:
            logging.info(
                'Added political party: "%s"', political_party.get('siglum')
            )
        else:
            logging.info(
                'Error when add political party: "%s"',
                political_party.get('siglum')
            )
    except:
        pass
