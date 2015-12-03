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

from django.contrib import admin
from django.utils.translation import ugettext as _

from politicians.forms import (
    CandidacyForm, PoliticianEventForm, PoliticianPoliticalPartyForm,
    MandateEventForm, MandateForm, PoliticianForm
)
from politicians.models import (
    PoliticalParty, Institution, Politician, PoliticianEventType,
    PoliticianEvent, PoliticalOffice, Mandate, MandateEventType,
    MandateEvent, PoliticianAlternativeName, Ethnicity, Education,
    PoliticianPoliticalParty, ElectionRound, Election, Candidacy,
    CandidacyStatus, City, State, Country, MaritalStatus, Nationality,
    Occupation
)


class ElectionRoundInline(admin.TabularInline):
    model = ElectionRound
    extra = 1


class ElectionAdmin(admin.ModelAdmin):
    inlines = [ElectionRoundInline]


class PoliticianPoliticalPartyInline(admin.TabularInline):
    model = PoliticianPoliticalParty
    extra = 1


class PoliticianEventInline(admin.TabularInline):
    model = PoliticianEvent
    extra = 1


class PoliticianAdmin(admin.ModelAdmin):
    model = Politician
    form = PoliticianForm
    list_display = ['__str__', 'cpf', 'date_of_birth']
    list_filter = ['ethnicity', 'education']
    exclude = ['alternative_names']
    search_fields = ['name']
    inlines = [PoliticianPoliticalPartyInline, PoliticianEventInline]
    readonly_fields = ['show_alternative_names']

    def show_alternative_names(self, obj):
        return ', '.join([y for x, y in obj.alternative_names.values_list()])
    show_alternative_names.short_description = _('Alternative Names')
    show_alternative_names.allow_tags = True


class PoliticianEventAdmin(admin.ModelAdmin):
    model = PoliticianEvent
    form = PoliticianEventForm
    search_fields = ['politician__name']


class PoliticianPoliticalPartyAdmin(admin.ModelAdmin):
    model = PoliticianPoliticalParty
    form = PoliticianPoliticalPartyForm
    list_filter = ['political_party']
    search_fields = ['politician__name']


class CandidacyAdmin(admin.ModelAdmin):
    model = Candidacy
    form = CandidacyForm
    list_filter = [
        'election_round__round_number',
        'election_round__election',
        'elected'
    ]
    search_fields = ['politician__name']


class MandateEventInline(admin.TabularInline):
    model = MandateEvent
    extra = 1


class MandateAdmin(admin.ModelAdmin):
    model = Mandate
    inlines = [MandateEventInline]
    search_fields = ['politician__name']
    form = MandateForm


class MandateEventAdmin(admin.ModelAdmin):
    model = MandateEvent
    form = MandateEventForm


class CityAdmin(admin.ModelAdmin):
    model = City
    list_filter = ['state']
    search_fields = ['name']


admin.site.register(Education)
admin.site.register(Election, ElectionAdmin)
admin.site.register(ElectionRound)
admin.site.register(Ethnicity)
admin.site.register(Institution)
admin.site.register(Politician, PoliticianAdmin)
admin.site.register(PoliticianAlternativeName)
admin.site.register(Candidacy, CandidacyAdmin)
admin.site.register(PoliticianEvent, PoliticianEventAdmin)
admin.site.register(PoliticianEventType)
admin.site.register(PoliticianPoliticalParty, PoliticianPoliticalPartyAdmin)
admin.site.register(Mandate, MandateAdmin)
admin.site.register(MandateEvent, MandateEventAdmin)
admin.site.register(MandateEventType)
admin.site.register(PoliticalOffice)
admin.site.register(PoliticalParty)
admin.site.register(CandidacyStatus)
admin.site.register(City, CityAdmin)
admin.site.register(State)
admin.site.register(Country)
admin.site.register(MaritalStatus)
admin.site.register(Nationality)
admin.site.register(Occupation)
