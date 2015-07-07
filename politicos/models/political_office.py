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

import logging

import sqlalchemy as sa
from slugify import slugify

from politicos.models import Base


class PoliticalOffice(Base):
    __tablename__ = 'political_office'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column('name', sa.String(100), unique=True, nullable=False)
    slug = sa.Column('slug', sa.String(255), unique=True, nullable=False)

    def __str__(self):
        return str('%s' % self.name)

    def __repr__(self):
        return str(self)

    def to_dict(self):
        return {
            'name': self.name,
            'slug': self.slug,
        }

    @classmethod
    def add_political_office(self, db, data):
        political_office = PoliticalOffice(
            name=data.get('name'),
            slug=slugify(data.get('name')),
        )

        db.add(political_office)
        db.flush()

        logging.debug('Added political office: "%s"', str(political_office))

        return political_office
