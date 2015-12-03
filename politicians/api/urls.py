# -*- coding: utf-8 -*-
#
# Copyright (c) 2015, Marcelo Jorge Vieira <metal@alucinados.com>
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

from tastypie.api import Api

from politicians.api.resources import (
    PoliticalPartyResource, InstitutionResource, PoliticianResource,
    PoliticianEventTypeResource, PoliticalOfficeResource, MandateResource,
    MandateEventTypeResource, EthnicityResource, EducationResource,
    ElectionResource, CandidacyResource, ElectionRoundResource,
    CandidacyStatusResource, PoliticianEventResource, MandateEventResource,
    CityResource, StateResource, CountryResource, OccupationResource,
    NationalityResource, MaritalStatusResource
)


api = Api(api_name='v0')
api.register(CityResource(), canonical=True)
api.register(StateResource(), canonical=True)
api.register(PoliticalPartyResource(), canonical=True)
api.register(InstitutionResource(), canonical=True)
api.register(EthnicityResource(), canonical=True)
api.register(EducationResource(), canonical=True)
api.register(PoliticianResource(), canonical=True)
api.register(PoliticianEventResource(), canonical=True)
api.register(PoliticianEventTypeResource(), canonical=True)
api.register(PoliticalOfficeResource(), canonical=True)
api.register(MandateResource(), canonical=True)
api.register(MandateEventResource(), canonical=True)
api.register(MandateEventTypeResource(), canonical=True)
api.register(ElectionResource(), canonical=True)
api.register(ElectionRoundResource(), canonical=True)
api.register(CandidacyResource(), canonical=True)
api.register(CandidacyStatusResource(), canonical=True)
api.register(CountryResource(), canonical=True)
api.register(OccupationResource(), canonical=True)
api.register(MaritalStatusResource(), canonical=True)
api.register(NationalityResource(), canonical=True)


urlpatterns = api.urls
