# -*- coding: utf-8 -*-
#
# Copyright (c) 2016, Marcelo Jorge Vieira <metal@alucinados.com>
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

import os
import requests
import shutil
import tempfile
import zipfile


class TSE(object):

    def __init__(self, year):
        self.domain_url = 'http://agencia.tse.jus.br'
        self.url = '{0}/estatistica/sead/odsele/{1}/{1}_{2}.zip'.format(
            self.domain_url, 'consulta_cand', year
        )
        self.temp_dir = tempfile.mkdtemp()
        # FIXME
        self.out_file = '/tmp/consulta_cand_{0}.zip'.format(year)

    def download(self):
        response = requests.get(self.url, stream=True)
        with open(self.out_file, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response

    def extract(self):
        zip_content = zipfile.ZipFile(self.out_file)
        zip_content.extractall(self.temp_dir)

    def download_and_extract(self):
        if not os.path.exists(self.out_file):
            self.download()
        self.extract()

    def remove_zip_file(self):
        shutil.rmtree(self.out_file)

    def remove_tmp_dir(self):
        shutil.rmtree(self.temp_dir)
