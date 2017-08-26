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

from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from politicos import __version__


# Admin
admin.autodiscover()


urlpatterns = [
    url(r'api/v0/',
        include('tastypie_swagger.urls', namespace='politicians-v0'),
        kwargs={
            'namespace': 'politicians-v0',
            'tastypie_api_module': 'politicians.api.urls.api',
            'version': __version__,
        }),
    url(r'^api/', include('politicians.api.urls')),

    # Website
    url(r'^',
        include('website.urls', namespace='website', app_name='website')),

    # Admin
    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
