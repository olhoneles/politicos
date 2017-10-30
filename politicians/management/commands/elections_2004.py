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

from politicians.management.commands._base import Politicos, PoliticosCommand


class Politicos2004(Politicos):

    @classmethod
    def get_picture(cls, politician_id, city_cod, state_siglum):
        domain = 'http://www.tse.jus.br/sadEleicao2004DivCand'
        url = '{0}/candidatoFoto.jsp?sq_cand={1}&sg_ue={2}&sg_ue_sup={3}'.format(  # noqa
            domain, politician_id, city_cod, state_siglum
        )
        return url

    @classmethod
    def convert_to_dict(cls, data, state_siglum):
        item = dict(
            state_siglum=state_siglum,
            election_round_number=data[3],
            city_cod=data[6],
            city_name=cls.formatter(data[7]),
            political_office_cod=cls.formatter(data[8]),
            political_office=cls.formatter(data[9]),
            name=cls.formatter(data[10]),
            politician_id=cls.formatter(data[11]),
            cpf=cls.formatter(data[13]),
            alternative_name=cls.formatter(data[14]),
            candidacy_status=cls.formatter(data[16]),
            political_party_siglum=data[18],
            political_party_name=cls.formatter(data[19]),
            occupation=cls.formatter(data[25]),
            date_of_birth=None,
            gender=data[30],
            education=cls.formatter(data[32]),
            marital_status=cls.formatter(data[34]),
            nationality=cls.formatter(data[36]),
            state_of_birth=data[37],
            place_of_birth=cls.formatter(data[39]),
            status=cls.formatter(data[42]),
        )
        item.update(
            picture=cls.get_picture(
                item.get('politician_id'),
                item.get('city_cod'),
                item.get('state_siglum'),
            )
        )
        return item


class Command(PoliticosCommand):

    def handle(self, *args, **options):
        Politicos2004.set_options(*args, **options)
        self.process_tse_data_by_year(Politicos2004, 2004)
