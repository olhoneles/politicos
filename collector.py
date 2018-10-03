#!/usr/bin/env python3
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

from collector.tse import TSE
from collector.tse_headers import year_headers


# FIXME
FILES_DIR = '/home/metal/Downloads/blah'


def main():
    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.INFO)
    # mute elasticsearch INFO logs
    log = logging.getLogger('elasticsearch')
    log.setLevel('ERROR')

    for year in year_headers.keys():
        tse = TSE(year, path=FILES_DIR)
        tse.download_and_extract(remove_tmp_dir=False, remove_zip=False)
        tse.all_candidates()


if __name__ == '__main__':
    main()
