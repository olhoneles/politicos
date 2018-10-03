# -*- coding: utf-8 -*-
#
# Copyright (c) 2016, Marcelo Jorge Vieira <metal@alucinados.com>
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

import csv
import glob
import logging
import os
import tempfile
import zipfile

import requests
import shutil
from dateutil import parser
from pandas import read_csv
from pandas.errors import EmptyDataError

from collector.tse_headers import year_headers
from collector.models import Politicians


OBJECT_LIST_MAXIMUM_COUNTER = 5000


class TSE(object):

    def __init__(self, year, path='/tmp'):
        self.year = year
        self.domain_url = 'http://agencia.tse.jus.br'
        self.url = '{0}/estatistica/sead/odsele/{1}/{1}_{2}.zip'.format(
            self.domain_url, 'consulta_cand', self.year
        )

        if not path:
            self.temp_dir = tempfile.mkdtemp()
        else:
            self.temp_dir = path

        self.out_file = os.path.join(
            self.temp_dir,
            f'consulta_cand_{self.year}.zip'
        )

    def _download(self):
        logging.info(f'Downloading {self.year} file...')
        response = requests.get(self.url, stream=True)
        with open(self.out_file, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response

    def _extract(self):
        logging.info(f'Extracting files from year {self.year}')
        dir_name = f'consulta_cand_{self.year}'
        zip_ref = zipfile.ZipFile(self.out_file)
        zip_ref.extractall(os.path.join(self.temp_dir, dir_name))
        zip_ref.close()

    def _remove_zip_file(self):
        os.remove(self.out_file)

    def _remove_tmp_dir(self):
        shutil.rmtree(self.temp_dir)

    def _csv2dict(self, filename):
        csv_rows = []
        with open(filename) as csvfile:
            # FIXME: use pandas?
            reader = csv.DictReader(csvfile)
            names = reader.fieldnames
            for row in reader:
                csv_rows.extend(
                    [{names[i]: row[names[i]] for i in range(len(names))}]
                )
        return csv_rows

    def _get_all_csv_files(self):
        dir_name = os.path.join(self.temp_dir, f'consulta_cand_{self.year}')
        return glob.glob(os.path.join(dir_name, '*.txt'.format(dir_name)))

    def _get_data(self, filename):
        # read file and add header
        try:
            file_data = os.path.basename(filename).split('_')
            state = file_data[3].split('.txt')[0]
            logging.info(f'Processing state {state}')
            df = read_csv(
                filename,
                delimiter=';',
                encoding='ISO-8859-1',
                quotechar='"',
                header=None,
            )
        except EmptyDataError:
            logging.info(f'{filename} is empty')
            return []

        df.columns = year_headers.get(self.year)
        # return df.to_dict(orient='records')
        # create new file with header
        header_file = f'{filename}_header.csv'
        df.to_csv(header_file, index=False)
        return self._csv2dict(header_file)

    def _string_int_to_int(self, rows, value):
        if not rows[value]:
            return None
        try:
            rows[value] = int(rows[value])
        except ValueError:
            pass

    def _string_float_to_int(self, rows, value):
        if not rows[value]:
            return None
        try:
            rows[value] = int(float(rows[value]))
        except ValueError:
            pass

    # FIXME: use pandas?
    def _parse_str(self, rows):
        # convert all to string =/
        # rows = {x: str(y) for x, y in rows.items()}
        rows['ano_eleicao'] = int(rows['ano_eleicao'])
        rows['data_geracao'] = parser.parse(rows['data_geracao'])

        self._string_int_to_int(rows, 'codigo_cargo')
        self._string_int_to_int(rows, 'codigo_estado_civil')
        self._string_int_to_int(rows, 'codigo_nacionalidade')
        self._string_int_to_int(rows, 'codigo_ocupacao')
        self._string_int_to_int(rows, 'codigo_sexo')
        self._string_int_to_int(rows, 'cod_grau_instrucao')
        self._string_int_to_int(rows, 'cod_situacao_candidatura')
        self._string_int_to_int(rows, 'numero_partido')
        self._string_int_to_int(rows, 'sequencial_candidato')

        self._string_float_to_int(rows, 'codigo_legenda')
        self._string_float_to_int(rows, 'cod_sit_tot_turno')
        self._string_float_to_int(rows, 'numero_candidato')
        self._string_float_to_int(rows, 'num_turno')

        # FIXME: leap year (convert model to Date)
        try:
            birthday = rows['data_nascimento']
            if birthday == 'nan':
                rows['data_nascimento'] = None
            elif birthday.find('/') != -1:
                birthday = birthday.split('/')
                if len(birthday[2]) == 2:
                    # FIXME
                    birthday[2] = f'19{birthday[2]}'
                birthday = f'{birthday[2]}-{birthday[1]}-{birthday[0]}'
                rows['data_nascimento'] = birthday
            else:
                if len(birthday) == 9:
                    birthday = f'0{birthday}'
                birthday = birthday.replace('.0', '')
                birthday = f'{birthday[4:]}-{birthday[2:4]}-{birthday[:2]}'
                rows['data_nascimento'] = birthday
        except Exception:
            pass

        return rows

    def download_and_extract(self, remove_zip=False, remove_tmp_dir=False):
        if not os.path.exists(self.out_file):
            self._download()
        self._extract()
        if remove_zip:
            self._remove_zip_file()
        if remove_tmp_dir:
            self._remove_tmp_dir()

    def all_candidates(self):
        for filename in self._get_all_csv_files():
            rows = self._get_data(filename)
            documents = []
            for idx, row in enumerate(rows):
                row = self._parse_str(row)
                politician = Politicians(**row)
                politician.source = dict(
                    filename=os.path.basename(filename),
                    line=idx + 1,
                )
                documents.append(politician)
                if len(documents) == OBJECT_LIST_MAXIMUM_COUNTER:
                    Politicians.bulk_save(documents)
                    logging.info(f'Added {OBJECT_LIST_MAXIMUM_COUNTER} items')
                    documents = []
            if documents:
                Politicians.bulk_save(documents)
                logging.info(f'Added {len(documents)} items')
                documents = []
