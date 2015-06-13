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
from datetime import datetime

import factory
import factory.alchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from politicos.models import PoliticalParty
from politicos.models.legislator import Legislator
from politicos.models.institution import Institution


sqlalchemy_echo = logging.getLogger('nose').getEffectiveLevel() < logging.INFO
engine = create_engine(
    'mysql+mysqldb://root@localhost:3306/test_politicos',
    convert_unicode=True,
    pool_size=1,
    max_overflow=0,
    echo=sqlalchemy_echo
)
maker = sessionmaker(bind=engine, autoflush=True)
db = scoped_session(maker)


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = db

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        instance = super(BaseFactory, cls)._create(target_class, *args, **kwargs)
        if (hasattr(cls, '_meta')
           and cls._meta is not None
           and hasattr(cls._meta, 'sqlalchemy_session')
           and cls._meta.sqlalchemy_session is not None):
            cls._meta.sqlalchemy_session.flush()
        return instance


class PoliticalPartyFactory(BaseFactory):
    class Meta:
        model = PoliticalParty

    name = factory.Sequence(lambda n: 'political party {0}'.format(n))
    siglum = factory.Sequence(lambda n: 'siglum {0}'.format(n))
    wikipedia = factory.Sequence(lambda n: 'http://wiki-{0}.com/'.format(n))
    website = factory.Sequence(lambda n: 'http://website-{0}.com/'.format(n))
    logo = factory.Sequence(lambda n: 'http://logo-{0}.com/'.format(n))
    founded_date = datetime.utcnow()


class LegislatorFactory(BaseFactory):
    class Meta:
        model = Legislator

    name = factory.Sequence(lambda n: 'Legislator {0}'.format(n))
    picture = factory.Sequence(lambda n: 'http://d.com/p{0}.png'.format(n))
    website = factory.Sequence(lambda n: 'http://d{0}.com/'.format(n))
    email = factory.Sequence(lambda n: 'name@d{0}.com'.format(n))
    gender = factory.Iterator(['M', 'F'])
    date_of_birth = datetime.now().date()
    about = factory.Sequence(lambda n: ' My About {0}'.format(n))


class InstitutionFactory(BaseFactory):
    class Meta:
        model = Institution

    siglum = factory.Sequence(lambda n: 'siglum {0}'.format(n))
    name = factory.Sequence(lambda n: 'Institution {0}'.format(n))
    logo = factory.Sequence(lambda n: 'http://i.com/p{0}.png'.format(n))
