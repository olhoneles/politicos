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

from politicos.models import Base


class Institution(Base):
    __tablename__ = 'institution'

    id = sa.Column(sa.Integer, primary_key=True)
    siglum = sa.Column('siglum', sa.Unicode(15), unique=True, nullable=False)
    name = sa.Column('name', sa.Unicode(255), unique=True, nullable=False)
    logo = sa.Column('logo', sa.Unicode(2048), nullable=True)

    def __str__(self):
        return unicode('%s (%s)' % (self.siglum, self.name)).encode('utf-8')

    def __repr__(self):
        return str(self)

    def to_dict(self):
        return {
            'siglum': self.siglum,
            'name': self.name,
            'logo': self.logo,
        }

    @classmethod
    def add_institution(self, db, data):
        institution = Institution(
            siglum=data.get('siglum'),
            name=data.get('name'),
            logo=data.get('logo'),
        )

        db.add(institution)
        db.flush()

        logging.debug(u'Added institution: "%s"', str(institution))

        return institution
