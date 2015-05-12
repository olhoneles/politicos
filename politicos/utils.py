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


def get_class(klass):
    module_name, class_name = klass.rsplit('.', 1)

    module = __import__(module_name)

    if '.' in module_name:
        module = reduce(getattr, module_name.split('.')[1:], module)

    return getattr(module, class_name)


def load_classes(classes=None, classes_to_load=None, default=None):
    if classes_to_load is None:
        classes_to_load = default

    if classes is None:
        classes = []

    for class_full_name in classes_to_load:
        if isinstance(class_full_name, (tuple, set, list)):
            load_classes(classes, class_full_name)
            continue

        try:
            klass = get_class(class_full_name)
            classes.append(klass)
        except ValueError:
            logging.warn(
                'Invalid class name [%s]. Will be ignored.' % class_full_name
            )
        except AttributeError:
            logging.warn(
                'Class [%s] not found. Will be ignored.' % class_full_name
            )
        except ImportError:
            logging.warn(
                'Module [%s] not found. Will be ignored.' % class_full_name
            )

    return classes
