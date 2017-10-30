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
from captcha.fields import ReCaptchaField


class ContactUsForm(forms.Form):

    name = forms.CharField(
        label=u'Nome',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Seu nome'})
    )

    email = forms.EmailField(
        label=u'Email',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Seu email'})
    )

    message = forms.CharField(
        label=u'Mensagem',
        required=True,
        widget=forms.Textarea(attrs={'placeholder': 'Sua mensagem', 'rows': 5})
    )

    captcha = ReCaptchaField(attrs={'theme': 'clean'})
