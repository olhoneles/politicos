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

from tornado.web import url

from politicos_api.handlers.candidacies import CandidaciesHandler
from politicos_api.handlers.candidacies_status import CandidaciesStatusHandler
from politicos_api.handlers.cities import CitiesHandler
from politicos_api.handlers.developers import DevelopersHandler
from politicos_api.handlers.educations import EducationsHandler
from politicos_api.handlers.election_rounds import ElectionRoundsHandler
from politicos_api.handlers.elections import ElectionsHandler
from politicos_api.handlers.ethnicities import EthnicitiesHandler
from politicos_api.handlers.examples import ExamplesHandler
from politicos_api.handlers.genders import GenderHandler
from politicos_api.handlers.main import MainHandler
from politicos_api.handlers.nationalities import NationalitiesHandler
from politicos_api.handlers.occupations import OccupationsHandler
from politicos_api.handlers.political_offices import PoliticalOfficesHandler
from politicos_api.handlers.political_parties import PoliticalPartiesHandler
from politicos_api.handlers.routes import RoutesHandler


handlers_website = [
    url(r'/?', MainHandler, name='main'),
    url(r'/developers/?', DevelopersHandler, name='developers'),
    url(r'/examples/?', ExamplesHandler, name='examples'),
    url(r'/routes/?', RoutesHandler, name='routes'),
    # url(r'/(favicon.ico)', tornado.web.StaticFileHandler, {'path': ''}),
]

handlers_api = [
    # url(
    #     r'/api/v1/candidacies/search/?',
    #     CandidaciesHandler,
    #     name='candidacies-search',
    # ),
    # url(r'/api/v1/institutions/?', MainHandler, name='institutions'),
    # url(r'/api/v1/countries/?', MainHandler, name='countries'),
    url(r'/api/v1/?', CandidaciesHandler, name='api-v1'),
    url(r'/api/v1/candidacies/?', CandidaciesHandler, name='candidacies'),
    url(
        r'/api/v1/political-parties/?',
        PoliticalPartiesHandler,
        name='political-parties',
    ),
    url(
        r'/api/v1/candidacies-status/?',
        CandidaciesStatusHandler,
        name='candidacies-status',
    ),
    url(r'/api/v1/cities/?', CitiesHandler, name='cities'),
    url(r'/api/v1/gender/?', GenderHandler, name='gender'),
    url(r'/api/v1/educations/?', EducationsHandler, name='educations'),
    url(
        r'/api/v1/election-rounds/?',
        ElectionRoundsHandler,
        name='election-rounds',
    ),
    url(r'/api/v1/elections/?', ElectionsHandler, name='elections'),
    url(r'/api/v1/ethnicities/?', EthnicitiesHandler, name='ethnicities'),
    url(
        r'/api/v1/nationalities/?',
        NationalitiesHandler,
        name='nationalities',
    ),
    url(r'/api/v1/occupations/?', OccupationsHandler, name='occupations'),
    url(
        r'/api/v1/political-offices/?',
        PoliticalOfficesHandler,
        name='political-offices',
    ),
]
