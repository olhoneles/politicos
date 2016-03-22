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

import operator

from django.conf import settings
from django.conf.urls import url
from django.db.models import Q
from django.utils.html import escape, strip_tags
from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.cache import SimpleCache
from tastypie.throttle import CacheThrottle
from tastypie.resources import ALL, ALL_WITH_RELATIONS
from tastypie.paginator import Paginator
from tastypie.utils import trailing_slash

from politicians.models import (
    PoliticalParty, Institution, Politician, PoliticianEventType,
    PoliticianEvent, PoliticalOffice, Mandate, MandateEventType,
    MandateEvent, Ethnicity, Education, PoliticianAlternativeName,
    PoliticianPoliticalParty, Election, ElectionRound, Candidacy,
    CandidacyStatus, City, State, Country, Nationality, Occupation,
    MaritalStatus
)


class BasicResource(ModelResource):

    class Meta:
        cache = SimpleCache(timeout=settings.RESOURCE_CACHE_TIMEOUT)
        throttle = CacheThrottle(throttle_at=settings.RESOURCE_MAX_REQUESTS)
        allowed_methods = ['get']

    def get_filters(self, request):
        query = escape(strip_tags(request.GET.get('q', '')))
        return [Q(name__icontains=word) for word in query.split(' ')]

    def basic_search(self, request, results, method, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        paginator = Paginator(
            request.GET,
            results,
            resource_uri=self._build_reverse_url(method, kwargs=kwargs)
        )

        objects = []
        for result in paginator.page().get('objects'):
            bundle = self.build_bundle(obj=result, request=request)
            objects.append(self.full_dehydrate(bundle))

        object_list = {
            'objects': objects,
            'meta': paginator.page().get('meta'),
        }

        self.log_throttled_access(request)
        return self.create_response(request, object_list)


class CountryResource(BasicResource):

    class Meta(BasicResource.Meta):
        resource_name = 'countries'
        queryset = Country.objects.all()
        filtering = {
            'name': ALL,
            'siglum': ALL,
            'slug': ALL,
        }


class StateResource(BasicResource):

    country = fields.ToOneField(
        CountryResource,
        'country',
        null=True,
    )

    class Meta(BasicResource.Meta):
        resource_name = 'states'
        queryset = State.objects.all()
        filtering = {
            'name': ALL,
            'siglum': ALL,
            'slug': ALL,
        }


class CityResource(BasicResource):

    state = fields.ToOneField(
        StateResource,
        'state',
        null=True,
    )

    class Meta(BasicResource.Meta):
        resource_name = 'cities'
        queryset = City.objects.all()
        filtering = {
            'state': ALL_WITH_RELATIONS,
            'name': ALL,
        }
        extra_actions = [{
            'name': 'search',
            'http_method': 'GET',
            'resource_type': 'list',
            'description': 'Search endpoint',
            'fields': {
                'q': {
                    'type': 'string',
                    'required': False,
                    'description': 'Search query terms'
                }
            }
        }]

    def prepend_urls(self):
        return [url(
            r'^(?P<resource_name>{0})/search{1}$'.format(
                self._meta.resource_name, trailing_slash()
            ),
            self.wrap_view('city_search'),
            name="city_get_search"
         )]

    def city_search(self, request, **kwargs):
        filters = self.get_filters(request)
        results = City.objects.filter(reduce(operator.and_, filters))
        url = 'city_get_search'
        return self.basic_search(request, results, url, **kwargs)


class ElectionRoundResource(BasicResource):

    election = fields.ToOneField(
        'politicians.api.resources.ElectionResource',
        'election',
        null=True,
    )

    politician = fields.ToOneField(
        'politicians.api.resources.PoliticianResource',
        'politician',
        null=True,
    )

    class Meta(BasicResource.Meta):
        resource_name = 'election-rounds'
        queryset = ElectionRound.objects.all()
        filtering = {
            'election': ALL_WITH_RELATIONS,
            'politician': ALL_WITH_RELATIONS,
        }


class ElectionResource(BasicResource):

    rounds = fields.ToManyField(
        ElectionRoundResource,
        'rounds',
        related_name='rounds',
        null=True,
        blank=True,
        full=True
    )

    class Meta(BasicResource.Meta):
        resource_name = 'elections'
        queryset = Election.objects.all()
        filtering = {
            'year': ALL,
        }


class PoliticalPartyResource(BasicResource):

    class Meta(BasicResource.Meta):
        resource_name = 'political-parties'
        queryset = PoliticalParty.objects.all()
        filtering = {
            'name': ALL,
            'siglum': ALL,
        }


class PoliticalOfficeResource(BasicResource):

    class Meta(BasicResource.Meta):
        resource_name = 'political-offices'
        queryset = PoliticalOffice.objects.all()
        filtering = {
            'name': ALL,
            'slug': ALL,
        }


class InstitutionResource(BasicResource):

    political_offices = fields.ToManyField(
        PoliticalOfficeResource,
        'political_offices',
        related_name='political_offices',
        null=True,
        full=True,
    )

    class Meta(BasicResource.Meta):
        resource_name = 'institutions'
        queryset = Institution.objects.all()
        filtering = {
            'name': ALL,
            'political_offices': ALL_WITH_RELATIONS,
        }


class PoliticianPoliticalPartyResource(BasicResource):

    political_party = fields.ToOneField(
        PoliticalPartyResource,
        'political_party',
        null=True,
        full=True,
    )

    class Meta(BasicResource.Meta):
        resource_name = 'politician-political-parties'
        queryset = PoliticianPoliticalParty.objects.all()
        filtering = {
            'political_party': ALL_WITH_RELATIONS,
        }


class PoliticianAlternativeNameResource(BasicResource):

    class Meta(BasicResource.Meta):
        resource_name = 'politician-alternative-names'
        queryset = PoliticianAlternativeName.objects.all()
        filtering = {
            'name': ALL,
        }


class NationalityResource(BasicResource):

    class Meta(BasicResource.Meta):
        resource_name = 'nationalities'
        queryset = Nationality.objects.all()
        filtering = {
            'name': ALL,
            'slug': ALL,
        }


class OccupationResource(BasicResource):

    class Meta(BasicResource.Meta):
        resource_name = 'occupations'
        queryset = Occupation.objects.all()
        filtering = {
            'name': ALL,
            'slug': ALL,
        }
        extra_actions = [{
            'name': 'search',
            'http_method': 'GET',
            'resource_type': 'list',
            'description': 'Search endpoint',
            'fields': {
                'q': {
                    'type': 'string',
                    'required': False,
                    'description': 'Search query terms'
                }
            }
        }]

    def prepend_urls(self):
        return [url(
            r'^(?P<resource_name>{0})/search{1}$'.format(
                self._meta.resource_name, trailing_slash()
            ),
            self.wrap_view('occupation_search'),
            name="occupation_get_search"
         )]

    def occupation_search(self, request, **kwargs):
        filters = self.get_filters(request)
        results = Occupation.objects.filter(reduce(operator.and_, filters))
        url = 'occupation_get_search'
        return self.basic_search(request, results, url, **kwargs)


class MaritalStatusResource(BasicResource):

    class Meta(BasicResource.Meta):
        resource_name = 'marital-status'
        queryset = MaritalStatus.objects.all()
        filtering = {
            'name': ALL,
            'slug': ALL,
        }


class EthnicityResource(BasicResource):

    class Meta(BasicResource.Meta):
        resource_name = 'ethnicities'
        queryset = Ethnicity.objects.all()
        filtering = {
            'name': ALL,
        }


class EducationResource(BasicResource):

    class Meta(BasicResource.Meta):
        resource_name = 'educations'
        queryset = Education.objects.all()
        filtering = {
            'name': ALL,
        }


class PoliticianEventTypeResource(BasicResource):

    class Meta(BasicResource.Meta):
        resource_name = 'politician-event-types'
        queryset = PoliticianEventType.objects.all()
        filtering = {
            'slug': ALL,
            'name': ALL,
        }


class PoliticianEventResource(BasicResource):

    politician_event_type = fields.ToOneField(
        PoliticianEventTypeResource,
        'politician_event_type',
        null=True,
        full=True,
    )

    class Meta(BasicResource.Meta):
        resource_name = 'politician-events'
        queryset = PoliticianEvent.objects.all()
        filtering = {
            'politician_event_type': ALL_WITH_RELATIONS,
        }


class PoliticianResource(BasicResource):

    occupation = fields.ToOneField(
        OccupationResource,
        'occupation',
        null=True,
        full=True
    )

    nationality = fields.ToOneField(
        NationalityResource,
        'nationality',
        null=True,
        full=True
    )

    marital_status = fields.ToOneField(
        MaritalStatusResource,
        'marital_status',
        null=True,
        full=True
    )

    state = fields.ToOneField(
        StateResource,
        'state',
        null=True,
        full=True
    )

    education = fields.ToOneField(
        EducationResource,
        'education',
        null=True,
        full=True
    )

    ethnicity = fields.ToOneField(
        EthnicityResource,
        'ethnicity',
        null=True,
        full=True
    )

    political_parties = fields.ToManyField(
        PoliticianPoliticalPartyResource,
        'politicians',
        related_name='political_parties',
        null=True,
        blank=True,
        full=True
    )

    events = fields.ToManyField(
        PoliticianEventResource,
        'politicians_events',
        related_name='events',
        null=True,
        full=True,
    )

    alternative_names = fields.ToManyField(
        PoliticianAlternativeNameResource,
        'alternative_names',
        related_name='alternative_names',
        null=True,
        full=True,
    )

    candidacies = fields.ToManyField(
        'politicians.api.resources.CandidacyResource',
        'candidacies',
        related_name='candidacies',
        null=True,
        blank=True,
        full=True,
    )

    class Meta(BasicResource.Meta):
        resource_name = 'politicians'
        queryset = Politician.objects.all()
        filtering = {
            'cpf': ALL,
            'name': ALL,
            'gender': ALL,
            'date_of_birth': ALL,
            'state': ALL_WITH_RELATIONS,
            'education': ALL_WITH_RELATIONS,
            'ethnicity': ALL_WITH_RELATIONS,
            'political_parties': ALL_WITH_RELATIONS,
            'marital_status': ALL_WITH_RELATIONS,
            'alternative_names': ALL_WITH_RELATIONS,
            'occupation': ALL_WITH_RELATIONS,
            'nationality': ALL_WITH_RELATIONS,
            'candidacies': ALL_WITH_RELATIONS,
        }
        extra_actions = [{
            'name': 'search',
            'http_method': 'GET',
            'resource_type': 'list',
            'description': 'Search endpoint',
            'fields': {
                'q': {
                    'type': 'string',
                    'required': False,
                    'description': 'Search query terms'
                }
            }
        }]

    def prepend_urls(self):
        return [url(
            r'^(?P<resource_name>{0})/search{1}$'.format(
                self._meta.resource_name, trailing_slash()
            ),
            self.wrap_view('politician_search'),
            name="politician_get_search"
         )]

    def politician_search(self, request, **kwargs):
        filters = self.get_filters(request)
        results = Politician.objects.filter(reduce(operator.and_, filters))
        url = 'politician_get_search'
        return self.basic_search(request, results, url, **kwargs)

    def apply_filters(self, request, applicable_filters):
        resource = super(PoliticianResource, self)
        return resource.apply_filters(request, applicable_filters).distinct()


class MandateEventTypeResource(BasicResource):

    class Meta(BasicResource.Meta):
        resource_name = 'mandate-event-types'
        queryset = MandateEventType.objects.all()
        filtering = {
            'slug': ALL,
            'name': ALL,
        }


class MandateEventResource(BasicResource):

    mandate = fields.ToOneField(
        'politicians.api.resources.MandateResource',
        'mandate',
        null=True,
        full=True,
    )

    mandate_event_type = fields.ToOneField(
        MandateEventTypeResource,
        'mandate_event_type',
        null=True,
        full=True,
    )

    class Meta(BasicResource.Meta):
        resource_name = 'mandate-events'
        queryset = MandateEvent.objects.all()
        filtering = {
            'mandate_event_type': ALL_WITH_RELATIONS,
        }


class CandidacyStatusResource(BasicResource):

    class Meta(BasicResource.Meta):
        resource_name = 'candidacies-status'
        queryset = CandidacyStatus.objects.all()
        filtering = {
            'name': ALL,
        }


class CandidacyResource(BasicResource):

    election_round = fields.ToOneField(
        ElectionRoundResource,
        'election_round',
        null=True,
        full=True,
    )

    politician = fields.ToOneField(
        PoliticianResource,
        'politician',
        null=True,
        full=True,
        use_in='list',
    )

    state = fields.ToOneField(
        StateResource,
        'state',
        null=True,
        full=True,
    )

    city = fields.ToOneField(
        CityResource,
        'city',
        null=True,
        full=True,
    )

    political_office = fields.ToOneField(
        PoliticalOfficeResource,
        'political_office',
        null=True,
        full=True,
    )

    candidacy_status = fields.ToOneField(
        CandidacyStatusResource,
        'candidacy_status',
        null=True,
        full=True,
    )

    institution = fields.ToOneField(
        InstitutionResource,
        'institution',
        null=True,
        full=True,
    )

    class Meta(BasicResource.Meta):
        resource_name = 'candidacies'
        queryset = Candidacy.objects.all()
        filtering = {
            'status': ALL,
            'elected': ALL,
            'politician': ALL_WITH_RELATIONS,
            'election_round': ALL_WITH_RELATIONS,
            'political_office': ALL_WITH_RELATIONS,
            'candidacy_status': ALL_WITH_RELATIONS,
            'institution': ALL_WITH_RELATIONS,
            'state': ALL_WITH_RELATIONS,
            'city': ALL_WITH_RELATIONS,
        }


class MandateResource(BasicResource):

    candidacy = fields.ToOneField(
        CandidacyResource,
        'candidacy',
        null=True,
        full=True,
    )

    events = fields.ToManyField(
        MandateEventResource,
        'mandates',
        related_name='events',
        null=True,
        full=True,
    )

    class Meta(BasicResource.Meta):
        resource_name = 'mandates'
        queryset = Mandate.objects.all()
        filtering = {
            'date_start': ALL,
            'date_start': ALL,
            'candidacy': ALL_WITH_RELATIONS,
        }
