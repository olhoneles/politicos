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
from sqlalchemy.orm import relationship

from politicos.models import Base
from politicos.utils import date_to_timestamp, timestamp_to_date


class Legislature(Base):
    __tablename__ = 'legislature'

    id = sa.Column(sa.Integer, primary_key=True)
    date_start = sa.Column('date_start', sa.Date, nullable=False)
    date_end = sa.Column('date_end', sa.Date, nullable=False)
    institution_id = sa.Column(
        'institution_id', sa.Integer, sa.ForeignKey('institution.id')
    )
    institution = relationship('Institution', foreign_keys=[institution_id])

    def __str__(self):
        return str('%s: %s until %s' % (
            self.institution.name, self.date_start, self.date_end
        ))

    def __repr__(self):
        return str(self)

    def to_dict(self):
        return {
            'institution': self.institution.to_dict(),
            'date_start': date_to_timestamp(self.date_start),
            'date_end': date_to_timestamp(self.date_end),
        }

    @classmethod
    def add_legislature(self, db, data):
        date_start = timestamp_to_date(data.get('date_start'))
        date_end = timestamp_to_date(data.get('date_end'))

        legislature = Legislature(
            institution_id=data.get('institution_id'),
            date_start=date_start,
            date_end=date_end,
        )

        db.add(legislature)
        db.flush()

        logging.debug('Added legislature: "%s"', str(legislature))

        return legislature
