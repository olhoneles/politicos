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

from django import forms

from politicians.models import (
    Candidacy, PoliticianEvent, PoliticianPoliticalParty, MandateEvent,
    Mandate, Politician
)


class PoliticianForm(forms.ModelForm):

    class Meta:
        model = Politician
        fields = '__all__'
        widgets = {
            'occupation': forms.TextInput(),
        }


class PoliticianEventForm(forms.ModelForm):

    class Meta:
        model = PoliticianEvent
        fields = '__all__'
        widgets = {
            'politician': forms.TextInput(),
        }


class CandidacyForm(forms.ModelForm):

    class Meta:
        model = Candidacy
        fields = '__all__'
        widgets = {
            'politician': forms.TextInput(),
            'institution': forms.TextInput(),
            'city': forms.TextInput(),
        }


class PoliticianPoliticalPartyForm(forms.ModelForm):

    class Meta:
        model = PoliticianPoliticalParty
        fields = '__all__'
        widgets = {
            'politician': forms.TextInput(),
        }


class MandateEventForm(forms.ModelForm):

    class Meta:
        model = MandateEvent
        fields = '__all__'
        widgets = {
            'mandate': forms.TextInput(),
        }


class MandateForm(forms.ModelForm):

    class Meta:
        model = Mandate
        fields = '__all__'
        widgets = {
            'institution': forms.TextInput(),
            'politician': forms.TextInput(),
        }
