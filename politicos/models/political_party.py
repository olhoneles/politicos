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

import sqlalchemy as sa

from politicos.models import Base


class PoliticalParty(Base):
    __tablename__ = 'political_party'

    id = sa.Column(sa.Integer, primary_key=True)
    siglum = sa.Column('siglum', sa.String(15), nullable=False)
    name = sa.Column('name', sa.String(2048), nullable=False)
    wikipedia = sa.Column('wikipedia', sa.String(2048), nullable=True)
    website = sa.Column('website', sa.String(2048), nullable=True)
    founded_date = sa.Column('founded_date', sa.DateTime, nullable=True)
    logo = sa.Column('logo', sa.String(2048), nullable=True)

    def to_dict(self):
        return {
            'siglum': self.siglum,
            'name': self.name,
            'wikipedia': self.wikipedia,
            'website': self.website,
            'founded_date': self.founded_date,
            'logo': self.logo,
        }
