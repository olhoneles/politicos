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

from django.conf import settings
from django.core.mail import send_mail
from django.template import RequestContext
from django.shortcuts import render_to_response, render

from forms import ContactUsForm


def home(request):
    return render_to_response('home.html', RequestContext(request, {}))


def examples(request):
    return render_to_response('examples.html', RequestContext(request, {}))


def developers(request):
    return render_to_response('developers.html', RequestContext(request, {}))


def contact_us(request):
    contact_us_form = ContactUsForm(request.POST or None)
    success_message = ''

    if request.POST and contact_us_form.is_valid():
        subject = '[Politicos API]: Fale Conosco'

        message = ('Nome: {0}\nEmail: {1}\nIP: {2}\nMensagem:\n\n{3}').format(
            contact_us_form.cleaned_data['name'],
            contact_us_form.cleaned_data['email'],
            request.META['REMOTE_ADDR'],
            contact_us_form.cleaned_data['message']
        )

        from_field = '{0} <{1}>'.format(
            contact_us_form.cleaned_data['name'],
            contact_us_form.cleaned_data['email']
        )

        send_mail(subject, message, from_field, [settings.CONTACT_US_EMAIL])

        success_message = (
            """Sua mensagem foi enviada com sucesso. """
            """Em breve entraremos em contato!"""
        )

        contact_us_form = ContactUsForm(None)

    c = {
        'contact_us_form': contact_us_form,
        'success_message': success_message
    }

    return render(request, 'contact_us.html', c)
