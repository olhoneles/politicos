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


class LegislatorEvents(Base):
    __tablename__ = 'legislator_events'

    id = sa.Column(sa.Integer, primary_key=True)
    date = sa.Column('date', sa.Date, nullable=False)
    legislator_events_type_id = sa.Column(
        'legislator_events_type_id',
        sa.Integer,
        sa.ForeignKey('legislator_events_type.id')
    )
    legislator_events_type = relationship(
        'LegislatorEventsType', foreign_keys=[legislator_events_type_id]
    )
    legislator_id = sa.Column(
        'legislator_id', sa.Integer, sa.ForeignKey('legislator.id')
    )
    legislator = relationship('Legislator', foreign_keys=[legislator_id])

    def __str__(self):
        return str('%s: %s' % (self.date, self.legislator_events_type.name))

    def __repr__(self):
        return str(self)

    def to_dict(self):
        return {
            'date': date_to_timestamp(self.date),
            'legislator': self.legislator.to_dict(),
            'legislator_events_type': self.legislator_events_type.to_dict(),
        }

    @classmethod
    def add_legislator_events(self, db, data):
        date = timestamp_to_date(data.get('date'))

        legislator_events = LegislatorEvents(
            legislator_events_type_id=data.get('legislator_events_type_id'),
            legislator_id=data.get('legislator_id'),
            date=date,
        )

        db.add(legislator_events)
        db.flush()

        logging.debug('Added legislator events: "%s"', str(legislator_events))

        return legislator_events
