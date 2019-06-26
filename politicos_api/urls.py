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
from politicos_api.handlers.candidacies_status import (
    CandidaciesStatusHandler,
    CandidaciesStatusSuggestHandler,
)
from politicos_api.handlers.cities import CitiesHandler, CitiesSuggestHandler
from politicos_api.handlers.developers import DevelopersHandler
from politicos_api.handlers.educations import (
    EducationsHandler,
    EducationsSuggestHandler,
)
from politicos_api.handlers.election_rounds import ElectionRoundsHandler
from politicos_api.handlers.elections import (
    ElectionsHandler,
    ElectionsSuggestHandler,
)
from politicos_api.handlers.ethnicities import (
    EthnicitiesHandler,
    EthnicitiesSuggestHandler,
)
from politicos_api.handlers.examples import ExamplesHandler
from politicos_api.handlers.genders import GenderHandler, GenderSuggestHandler
from politicos_api.handlers.main import MainHandler
from politicos_api.handlers.nationalities import (
    NationalitiesHandler,
    NationalitiesSuggestHandler,
)
from politicos_api.handlers.occupations import (
    OccupationsHandler,
    OccupationsSuggestHandler,
)
from politicos_api.handlers.political_offices import (
    PoliticalOfficesHandler,
    PoliticalOfficesSuggestHandler,
)
from politicos_api.handlers.political_parties import (
    PoliticalPartiesHandler,
    PoliticalPartiesSuggestHandler,
)
from politicos_api.handlers.politicians import PoliticiansSuggestHandler
from politicos_api.handlers.routes import RoutesHandler
from politicos_api.handlers.states import StatesHandler, StatesSuggestHandler
from politicos_api.handlers.marital_status import (
    MaritalStatusHandler,
    MaritalStatusSuggestHandler,
)


handlers_website = [
    url(r"/?", MainHandler, name="main"),
    url(r"/developers/?", DevelopersHandler, name="developers"),
    url(r"/examples/?", ExamplesHandler, name="examples"),
    url(r"/routes/?", RoutesHandler, name="routes"),
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
    url(r"/api/v1/?", CandidaciesHandler, name="api-v1"),
    url(r"/api/v1/candidacies/?", CandidaciesHandler, name="candidacies"),
    url(
        r"/api/v1/politicians/suggest/?",
        PoliticiansSuggestHandler,
        name="politicians-suggest",
    ),
    url(
        r"/api/v1/political-parties/suggest/?",
        PoliticalPartiesSuggestHandler,
        name="political-parties-suggest",
    ),
    url(
        r"/api/v1/political-parties/?",
        PoliticalPartiesHandler,
        name="political-parties",
    ),
    url(
        r"/api/v1/candidacies-status/suggest/?",
        CandidaciesStatusSuggestHandler,
        name="candidacies-status/-suggest",
    ),
    url(
        r"/api/v1/candidacies-status/?",
        CandidaciesStatusHandler,
        name="candidacies-status",
    ),
    url(
        r"/api/v1/cities/suggest/?", CitiesSuggestHandler, name="cities-suggest"
    ),
    url(r"/api/v1/cities/?", CitiesHandler, name="cities"),
    url(
        r"/api/v1/gender/suggest/?", GenderSuggestHandler, name="gender-suggest"
    ),
    url(r"/api/v1/gender/?", GenderHandler, name="gender"),
    url(
        r"/api/v1/educations/suggest/?",
        EducationsSuggestHandler,
        name="educations-suggest",
    ),
    url(r"/api/v1/educations/?", EducationsHandler, name="educations"),
    url(
        r"/api/v1/election-rounds/?",
        ElectionRoundsHandler,
        name="election-rounds",
    ),
    url(
        r"/api/v1/elections/suggest/?",
        ElectionsSuggestHandler,
        name="elections-suggest",
    ),
    url(r"/api/v1/elections/?", ElectionsHandler, name="elections"),
    url(
        r"/api/v1/ethnicities/suggest/?",
        EthnicitiesSuggestHandler,
        name="ethnicities-suggest",
    ),
    url(r"/api/v1/ethnicities/?", EthnicitiesHandler, name="ethnicities"),
    url(
        r"/api/v1/nationalities/suggest/?",
        NationalitiesSuggestHandler,
        name="nationalities-suggest",
    ),
    url(r"/api/v1/nationalities/?", NationalitiesHandler, name="nationalities"),
    url(
        r"/api/v1/occupations/suggest/?",
        OccupationsSuggestHandler,
        name="occupations-suggest",
    ),
    url(r"/api/v1/occupations/?", OccupationsHandler, name="occupations"),
    url(
        r"/api/v1/political-offices/suggest/?",
        PoliticalOfficesSuggestHandler,
        name="political-offices-suggest",
    ),
    url(
        r"/api/v1/political-offices/?",
        PoliticalOfficesHandler,
        name="political-offices",
    ),
    url(
        r"/api/v1/states/suggest/?", StatesSuggestHandler, name="states-suggest"
    ),
    url(r"/api/v1/states/?", StatesHandler, name="states"),
    url(
        r"/api/v1/marital-status/suggest/?",
        MaritalStatusSuggestHandler,
        name="marital-status-suggest",
    ),
    url(
        r"/api/v1/marital-status/?", MaritalStatusHandler, name="marital-status"
    ),
]
