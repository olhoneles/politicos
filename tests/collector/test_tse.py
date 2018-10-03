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

import unittest

from collector.tse import TSE


class TSETestCase(unittest.TestCase):

    def setUp(self):
        self.tse = TSE(2018)
        # tse.download_and_extract(remove_tmp_dir=False, remove_zip=False)
        # tse.all_candidates()

    def test_domain_url(self):
        self.assertEqual(self.tse.domain_url, 'http://agencia.tse.jus.br')

    def test_url(self):
        url = 'http://agencia.tse.jus.br/estatistica/sead/odsele/consulta_cand'
        self.assertEqual(self.tse.url, f'{url}/consulta_cand_2018.zip')

    def test_out_file_without_path(self):
        self.assertEqual(self.tse.out_file, '/tmp/consulta_cand_2018.zip')

    def test_out_file_with_path(self):
        new_path = '/tmp/cand_directory'
        tse = TSE(2018, path=new_path)
        self.assertEqual(tse.out_file, f'{new_path}/consulta_cand_2018.zip')

    def test_download_and_extract(self):
        pass

    def test_all_candidates(self):
        pass
