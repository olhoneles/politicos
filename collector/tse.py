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
from pandas import read_csv, concat
from pandas.errors import EmptyDataError

from collector.tse_headers import year_headers
from collector.models.candidacies import PoliticianCandidacies


OBJECT_LIST_MAXIMUM_COUNTER = 5000
TSE_IMAGE_URL = 'http://divulgacandcontas.tse.jus.br/divulga/images'
TSE_URL = 'http://divulgacandcontas.tse.jus.br/candidaturas/oficial'


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
        def _get_files(extension):
            dir_name = os.path.join(
                self.temp_dir,
                f'consulta_cand_{self.year}'
            )
            files = os.path.join(dir_name, f'*.{extension}')
            return sorted([
                fn for fn in glob.glob(files)
                if not fn.endswith(f'_BRASIL.{extension}')
            ])

        # FIXME
        if int(self.year) >= 2014:
            return _get_files('csv')
        return _get_files('txt')

    def _read_csv(self, filename, without_header=False):
        params = {
            'delimiter': ';',
            'encoding': 'ISO-8859-1',
            'quotechar': '"',
            # Avoiding converting string to int (nr_cpf_candidato)
            'dtype': object
        }
        if without_header:
            params['header'] = None
        try:
            df = read_csv(filename, **params)
            return df
        except EmptyDataError:
            logging.info(f'{filename} is empty')
            return []

    def _get_data_frame(self, filename):
        basename = os.path.basename(filename)
        file_data = basename.split('_')
        state = os.path.splitext(file_data[3])[0]
        logging.info(f'Processing state {state}')
        # FIXME
        if int(self.year) >= 2014:
            df = self._read_csv(filename)
            df['filename'] = filename
            df.columns = df.columns.str.lower()
            return df

        # read file and add header
        df = self._read_csv(filename, without_header=True)
        df.columns = year_headers.get(self.year)
        df['filename'] = filename
        # create new file with header
        header_file = f'{filename}_header.csv'
        df.to_csv(header_file, index=False)
        return df

    def download_and_extract(self, remove_zip=False, remove_tmp_dir=False):
        if not os.path.exists(self.out_file):
            self._download()
        self._extract()
        if remove_zip:
            self._remove_zip_file()
        if remove_tmp_dir:
            self._remove_tmp_dir()

    def all_state_data_frames(self):
        "Concatenate all data frames of a single year"
        data_frames = []
        for filename in self._get_all_csv_files():
            rows = self._get_data_frame(filename)
            data_frames.append(rows)
        return concat(data_frames)


def all_data_frames_together(years, path):
    "Concat data frames for all the `years'"
    data_frames = []
    for year in years:
        tse = TSE(year, path=path)
        tse.download_and_extract(remove_tmp_dir=False, remove_zip=False)
        data_frames.append(tse.all_state_data_frames())
    return concat(data_frames, sort=True)


def _string_int_to_int(rows, value):
    if not rows[value]:
        return None
    try:
        rows[value] = int(rows[value])
    except ValueError:
        pass

def _string_float_to_int(rows, value):
    if not rows[value]:
        return None
    try:
        rows[value] = int(float(rows[value]))
    except ValueError:
        pass

def _format_sigla_uf(data):
    if data['sg_uf']:
        state_image = f'{TSE_IMAGE_URL}/{data["sg_uf"]}.png'
        data['unidade_eleitoral'] = {}
        data['unidade_eleitoral']['bandeira'] = state_image

def _format_sigla_ue(data):
    sg_ue = data['sg_ue']
    # FIXME
    if isinstance(sg_ue, str):
        return
    zeros = '0' * (5 - len(str(data['sg_ue'])))
    data['sg_ue'] = f'{zeros}{sg_ue}'

def _format_electoral_card(data):
    if len(str(data['nr_titulo_eleitoral_candidato'])) == 11:
        electoral_card = f'0{data["nr_titulo_eleitoral_candidato"]}'
        data['nr_titulo_eleitoral_candidato'] = electoral_card

def _format_politician_image(data):
    elections_id = {
        2004: '14431',
        2006: '14423',
        2008: '14422',
        2010: '14417',
        2012: '1699',
        2014: '680',
        2016: '01120',
    }
    election_id = elections_id.get(data['ano_eleicao'])

    if not election_id:
        data['foto_url'] = ''
        return

    sg_ue = data['sg_ue']
    politician_id = data['sq_candidato']
    uf = data['sg_uf']
    url = f'{TSE_URL}/{data["ano_eleicao"]}'
    electoral_card = data['nr_titulo_eleitoral_candidato']
    if data['ano_eleicao'] in [2004, 2008, 2012]:
        foto_url = f'{url}/{uf}/{sg_ue}/{election_id}'
        foto_url = f'{foto_url}/{election_id}/{politician_id}/foto.png'
    elif data['ano_eleicao'] in [2006, 2010]:
        foto_url = f'{url}/BR/{uf}/{election_id}/{politician_id}'
        foto_url = f'{foto_url}/foto.png'
    elif data['ano_eleicao'] == 2014:
        foto_url = f'{url}/BR/{uf}/{election_id}/{politician_id}'
        foto_url = f'{foto_url}/{electoral_card}.jpg'
    elif data['ano_eleicao'] == 2016:
        foto_url = f'{url}/{uf}/{sg_ue}/2/{politician_id}'
        foto_url = f'{foto_url}/{electoral_card}.jpg'
    data['foto_url'] = foto_url

# FIXME: use pandas?
def _parse_str(rows):
    # convert all to string =/
    # rows = {x: str(y) for x, y in rows.items()}
    rows['ano_eleicao'] = int(rows['ano_eleicao'])
    rows['dt_geracao'] = parser.parse(rows['dt_geracao'])

    _string_int_to_int(rows, 'cd_cargo')
    _string_int_to_int(rows, 'cd_estado_civil')
    _string_int_to_int(rows, 'cd_nacionalidade')
    _string_int_to_int(rows, 'cd_ocupacao')
    _string_int_to_int(rows, 'cd_genero')
    _string_int_to_int(rows, 'cd_grau_instrucao')
    _string_int_to_int(rows, 'cd_situacao_candidatura')
    _string_int_to_int(rows, 'nr_partido')
    _string_int_to_int(rows, 'sq_candidato')

    if 'codigo_legenda' in rows:
        _string_float_to_int(rows, 'codigo_legenda')
    _string_float_to_int(rows, 'cd_sit_tot_turno')
    _string_float_to_int(rows, 'nr_candidato')
    _string_float_to_int(rows, 'nr_turno')

    # FIXME: leap year (convert model to Date)
    try:
        birthday = rows['dt_nascimento']
        if birthday == 'nan':
            rows['dt_nascimento'] = None
        elif birthday.find('/') != -1:
            birthday = birthday.split('/')
            if len(birthday[2]) == 2:
                # FIXME
                birthday[2] = f'19{birthday[2]}'
            birthday = f'{birthday[2]}-{birthday[1]}-{birthday[0]}'
            rows['dt_nascimento'] = birthday
        else:
            if len(birthday) == 9:
                birthday = f'0{birthday}'
            birthday = birthday.replace('.0', '')
            birthday = f'{birthday[4:]}-{birthday[2:4]}-{birthday[:2]}'
            rows['dt_nascimento'] = birthday
    except Exception:
        pass

    _format_sigla_uf(rows)
    _format_electoral_card(rows)
    _format_sigla_ue(rows)
    _format_politician_image(rows)

    return rows


def import_tse(years, path):
    "Collect data frames and push their data into elastic search"
    df = all_data_frames_together(years, path)
    logging.info(f'Categorize data')
    cpf_unique = df['nr_cpf_candidato'].unique()
    cpf_groups = df.groupby('nr_cpf_candidato')

    logging.info(f'Save data')
    documents = []

    def save_batch():
        PoliticianCandidacies.bulk_save(documents)
        logging.info(f'Added {OBJECT_LIST_MAXIMUM_COUNTER} items')
        documents[:] = []

    for cpf in cpf_unique:
        group = (cpf_groups
                 .get_group(cpf)
                 .sort_values('ano_eleicao', ascending=False)
                 .to_dict(orient='records'))

        politician_data = _parse_str(group[0])
        politician = PoliticianCandidacies(**politician_data)

        for idx, candidacy in enumerate(group):
            politician.add_candidacies(
                int(candidacy['ano_eleicao']),
                candidacy['ds_sit_tot_turno'],
                candidacy['nm_ue'],
                candidacy['sg_uf'],
                candidacy['ds_cargo'],
                source='',
            )
        documents.append(politician)
        if len(documents) == OBJECT_LIST_MAXIMUM_COUNTER:
            save_batch()
    if documents:
        save_batch()
    logging.info(f'Done with data indexing')
