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

import argparse
import logging
import os

from collector.models import setup_indices
from collector.tse import TSE
from collector.tse_headers import year_headers


DEFAULT_DOWNLOAD_DIRECTORY = os.path.abspath(
    os.path.expanduser('~/Downloads/tse')
)


def run(args):
    "Collect data"
    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=FORMAT, level=args.log_level)
    # mute elasticsearch INFO logs
    log = logging.getLogger('elasticsearch')
    log.setLevel('ERROR')
    # Setup elastic search indices once before starting
    setup_indices()
    # Collect!
    for year in year_headers.keys():
        tse = TSE(year, path=args.download_directory)
        tse.download_and_extract(remove_tmp_dir=False, remove_zip=False)
        tse.all_candidates()


def main():
    "Parse command line and launch collector"
    parser = argparse.ArgumentParser(description='Data Collector')

    # Log levels accepted by logging library. Probably a good idea to
    # rely on _levelToName but didn't find anything better :(
    log_levels = list(logging._levelToName.values())

    parser.add_argument(
        '-d', '--download-dir',
        dest='download_directory',
        action='store',
        default=DEFAULT_DOWNLOAD_DIRECTORY,
        help='Directory where files will be downloaded',
    )

    parser.add_argument(
        '-l', '--log-level',
        default='CRITICAL',
        choices=log_levels,
        type=lambda x: x.upper(),
        help=f'Log verbosity level: {", ".join(log_levels)}',
    )

    run(parser.parse_args())


if __name__ == '__main__':
    main()
