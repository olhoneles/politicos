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

from datetime import datetime
from unittest import TestCase

from mock import patch, call
from preggy import expect

from politicos.utils import (
    get_class, load_classes, date_to_timestamp, datetime_to_timestamp,
    timestamp_to_date, timestamp_to_datetime
)


class TestUtils(TestCase):

    def test_can_get_class(self):
        from Queue import Queue

        loaded = get_class('Queue.Queue')
        expect(loaded).to_equal(Queue)

    def test_can_load_classes(self):
        from politicos.models.political_party import PoliticalParty

        classes = load_classes(default=[
            'politicos.models.political_party.PoliticalParty',
        ])

        expect(classes).to_length(1)
        expect(classes[0]).to_equal(PoliticalParty)

    def test_can_load_classes_with_list(self):
        from politicos.models.political_party import PoliticalParty

        classes = load_classes(default=[
            ['politicos.models.political_party.PoliticalParty'],
        ])

        expect(classes).to_length(1)
        expect(classes[0]).to_equal(PoliticalParty)

    @patch('politicos.utils.logging')
    @patch('politicos.utils.get_class')
    def test_cannot_load_classes_import_error(self, get_class_mock, log_mock):
        get_class_mock.side_effect = ImportError
        classes = load_classes(default=['blah.models.blah.Test'])

        expect(classes).to_length(0)
        expect(log_mock.mock_calls).to_include(
            call.warn(
                'Module [%s] not found. Will be ignored.',
                'blah.models.blah.Test'
            )
        )

    @patch('politicos.utils.logging')
    @patch('politicos.utils.get_class')
    def test_cannot_load_classes_value_error(self, get_class_mock, log_mock):
        get_class_mock.side_effect = ValueError
        classes = load_classes(default=['blah.models.blah.Test'])

        expect(classes).to_length(0)
        expect(log_mock.mock_calls).to_include(
            call.warn(
                'Invalid class name [%s]. Will be ignored.',
                'blah.models.blah.Test'
            )
        )

    @patch('politicos.utils.logging')
    @patch('politicos.utils.get_class')
    def test_cannot_load_classes_attr_error(self, get_class_mock, log_mock):
        get_class_mock.side_effect = AttributeError
        classes = load_classes(default=['blah.models.blah.Test'])

        expect(classes).to_length(0)
        expect(log_mock.mock_calls).to_include(
            call.warn(
                'Class [%s] not found. Will be ignored.',
                'blah.models.blah.Test'
            )
        )

    def test_can_convert_date_to_timestamp(self):
        dt = datetime.strptime('Jun 27 2015', '%b %d %Y').date()
        expect(date_to_timestamp(dt)).to_equal(1435363200)

    def test_can_convert_datetime_to_timestamp(self):
        dt = datetime.strptime('Jun 27 2015 6:33PM', '%b %d %Y %I:%M%p')
        expect(datetime_to_timestamp(dt)).to_equal(1435429980)

    def test_can_convert_timestamp_to_date(self):
        dt1 = timestamp_to_date(1435363200)
        dt2 = datetime.strptime('Jun 27 2015', '%b %d %Y').date()
        expect(dt1).to_equal(dt2)

    def test_can_convert_timestamp_to_datetime(self):
        dt1 = timestamp_to_datetime(1435429980)
        dt2 = datetime.strptime('Jun 27 2015 6:33PM', '%b %d %Y %I:%M%p')
        expect(dt1).to_equal(dt2)
