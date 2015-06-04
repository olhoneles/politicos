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

from unittest import TestCase

from preggy import expect

from politicos.utils import get_class, load_classes


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

    def test_cannot_load_classes(self):
        classes = load_classes(default=['blah.models.blah.Test'])
        expect(classes).to_length(0)
