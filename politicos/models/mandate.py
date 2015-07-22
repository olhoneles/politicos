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


class Mandate(Base):
    __tablename__ = 'mandate'

    id = sa.Column(sa.Integer, primary_key=True)
    date_start = sa.Column('date_start', sa.DateTime, nullable=False)
    date_end = sa.Column('date_end', sa.DateTime, nullable=False)
    legislator_id = sa.Column(
        'legislator_id', sa.Integer, sa.ForeignKey('legislator.id')
    )
    legislator = relationship('Legislator', foreign_keys=[legislator_id])
    political_office_id = sa.Column(
        'political_office_id', sa.Integer, sa.ForeignKey('political_office.id')
    )
    political_office = relationship(
        'PoliticalOffice', foreign_keys=[political_office_id]
    )

    def __str__(self):
        return unicode('%s: %s until %s' % (
            self.legislator.name, self.date_start, self.date_end
        )).encode('utf-8')

    def __repr__(self):
        return str(self)

    def to_dict(self):
        return {
            'legislator': self.legislator.to_dict(),
            'political_office': self.political_office.to_dict(),
            'date_start': date_to_timestamp(self.date_start),
            'date_end': date_to_timestamp(self.date_end),
        }

    @classmethod
    def add_mandate(self, db, data):
        date_start = timestamp_to_date(data.get('date_start'))
        date_end = timestamp_to_date(data.get('date_end'))

        mandate = Mandate(
            legislator_id=data.get('legislator_id'),
            political_office_id=data.get('political_office_id'),
            date_start=date_start,
            date_end=date_end,
        )

        db.add(mandate)
        db.flush()

        logging.debug(u'Added mandate: "%s"', str(mandate))

        return mandate
