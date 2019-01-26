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
import time
import signal
from multiprocessing import Pool
from multiprocessing.pool import MaybeEncodingError
from urllib.request import urlopen

import sqlite3
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Q, Search
from ujson import loads

from models.politicians import Politicians


FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(
    format=FORMAT,
    level=logging.INFO
)
# mute elasticsearch INFO logs
log = logging.getLogger('elasticsearch')
log.setLevel('ERROR')

ANO_ELEICAO = 2018
NUM_WORKERS = 3
OBJECT_LIST_MAXIMUM_COUNTER = 5000

conn = sqlite3.connect('politician_pictures.db')
cursor = conn.cursor()
cursor.execute('PRAGMA synchronous = OFF')
cursor.execute('PRAGMA journal_mode = MEMORY')
# cursor.execute('PRAGMA locking_mode = EXCLUSIVE')


def create_db(cursor):
    logging.info('Creating politicians table...')
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS pictures (
            doc_id TEXT NOT NULL,
            sg_ue TEXT NOT NULL,
            sq_candidato TEXT NOT NULL,
            url TEXT NOT NULL
        )
        '''
    )
    conn.commit()


def clear_db(conn, cursor):
    logging.info('Erasing politicians table...')
    sql = 'DELETE FROM pictures'
    cursor.execute(sql)
    conn.commit()


def get_pictures(client):
    es_data = (
        Search(using=client, index='politicians')
        .query(Q('bool', must=[Q('match', ano_eleicao=ANO_ELEICAO)]))
        .source(['sq_candidato', 'sg_ue'])
        .scan()
    )
    data = []
    for hit in es_data:
        url = 'http://divulgacandcontas.tse.jus.br/divulga'
        url = f'{url}/rest/v1/candidatura/buscar'
        url = f'{url}/{ANO_ELEICAO}/{hit.sg_ue}/2022802018'
        url = f'{url}/candidato/{hit.sq_candidato}'
        data.append(
            {
                'doc_id': hit.meta.id,
                'url': url,
                'sg_ue': hit.sg_ue,
                'sq_candidato': hit.sq_candidato,
            }
        )
    return data


def insert_sqlite_data(data):
    cursor.execute('BEGIN TRANSACTION')
    for x in data:
        foto_url = x['foto_url']
        sg_ue = x['sg_ue']
        doc_id = x['doc_id']
        sq_candidato = x['sq_candidato']
        cursor.execute(
            '''
            INSERT INTO pictures (doc_id, sg_ue, sq_candidato, url)
            VALUES (?, ?, ?, ?)
            ''',
            (doc_id, sg_ue, sq_candidato, foto_url),
        )
    conn.commit()


def _http_get(data):
    # Avoiding flood the TSE API
    time.sleep(0.5)

    url = data.get('url')
    response = urlopen(url)
    # logging.info(f'{response.getcode()}: {url}')
    content = response.read()
    if not content:
        logging.error(f'Empty response: {url}')
        return {
            'foto_url': '',
            'sg_ue': '',
            'doc_id': '',
            'sq_candidato': '',
        }
    json = loads(content)
    return {
        'foto_url': json.get('fotoUrl', ''),
        'sg_ue': data.get('sg_ue'),
        'doc_id': data.get('doc_id'),
        'sq_candidato': data.get('sq_candidato'),
    }


def update_es_data(cursor, client):
    logging.info('Select all politicians...')
    sql = 'SELECT * FROM pictures'
    cursor.execute(sql)
    rows = cursor.fetchall()
    documents = []
    for row in rows:
        doc_id = row[0]
        if not doc_id:
            continue
        politician = Politicians.get(
            id=doc_id,
            index='politicians',
            using=client,
        )
        politician.foto_url = row[3]
        documents.append(politician)
        if len(documents) == OBJECT_LIST_MAXIMUM_COUNTER:
            Politicians.bulk_update(documents, client)
            logging.info(f'Updated {OBJECT_LIST_MAXIMUM_COUNTER} items')
            documents = []
    if documents:
        Politicians.bulk_update(documents, client)
        logging.info(f'Updated {len(documents)} items')
        documents = []


def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def main():
    client = Elasticsearch()

    create_db(cursor)
    clear_db(conn, cursor)

    try:
        logging.info(f'Getting photo URL...')
        pool = Pool(NUM_WORKERS, init_worker)
        data = pool.imap_unordered(_http_get, get_pictures(client))
    except KeyboardInterrupt:
        pool.terminate()
        pool.join()
        raise SystemExit(1)
    except MaybeEncodingError:
        pass

    insert_sqlite_data(data)
    update_es_data(cursor, client)

    conn.close()


if __name__ == '__main__':
    main()
