# -*- coding: utf-8 -*-
#
# Copyright (c) 2019, Marcelo Jorge Vieira <metal@alucinados.com>
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

import os


LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

CACHE_TIMEOUT = int(os.environ.get("CACHE_TIMEOUT", 7200))

OBJECT_LIST_MAXIMUM_COUNTER = 5000
TSE_IMAGE_URL = "http://divulgacandcontas.tse.jus.br/divulga/images"
TSE_URL = "http://divulgacandcontas.tse.jus.br/candidaturas/oficial"

DEFAULT_DOWNLOAD_DIRECTORY = os.path.abspath(os.path.expanduser("~/Downloads/tse"))
