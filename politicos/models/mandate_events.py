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


class MandateEvents(Base):
    __tablename__ = 'mandate_events'

    id = sa.Column(sa.Integer, primary_key=True)
    date = sa.Column('date', sa.Date, nullable=False)
    mandate_events_type_id = sa.Column(
        'mandate_events_type_id',
        sa.Integer,
        sa.ForeignKey('mandate_events_type.id')
    )
    mandate_events_type = relationship(
        'MandateEventsType', foreign_keys=[mandate_events_type_id]
    )
    mandate_id = sa.Column(
        'mandate_id', sa.Integer, sa.ForeignKey('mandate.id')
    )
    mandate = relationship('Mandate', foreign_keys=[mandate_id])

    def __str__(self):
        return unicode('%s: %s' % (
            self.date, self.mandate_events_type.name
        )).encode('utf-8')

    def __repr__(self):
        return str(self)

    def to_dict(self):
        return {
            'date': date_to_timestamp(self.date),
            'mandate': self.mandate.to_dict(),
            'mandate_events_type': self.mandate_events_type.to_dict(),
        }

    @classmethod
    def add_mandate_events(self, db, data):
        date = timestamp_to_date(data.get('date'))

        mandate_events = MandateEvents(
            mandate_events_type_id=data.get('mandate_events_type_id'),
            mandate_id=data.get('mandate_id'),
            date=date,
        )

        db.add(mandate_events)
        db.flush()

        logging.debug(u'Added mandate events: "%s"', str(mandate_events))

        return mandate_events
