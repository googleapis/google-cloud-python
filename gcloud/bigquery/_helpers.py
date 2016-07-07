# Copyright 2015 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Shared elper functions for BigQuery API classes."""

from gcloud._helpers import _datetime_from_microseconds


def _not_null(value, field):
    """Check whether 'value' should be coerced to 'field' type."""
    return value is not None or field.mode != 'NULLABLE'


def _int_from_json(value, field):
    """Coerce 'value' to an int, if set or not nullable."""
    if _not_null(value, field):
        return int(value)


def _float_from_json(value, field):
    """Coerce 'value' to a float, if set or not nullable."""
    if _not_null(value, field):
        return float(value)


def _bool_from_json(value, field):
    """Coerce 'value' to a bool, if set or not nullable."""
    if _not_null(value, field):
        return value.lower() in ['t', 'true', '1']


def _datetime_from_json(value, field):
    """Coerce 'value' to a datetime, if set or not nullable."""
    if _not_null(value, field):
        # value will be a float in seconds, to microsecond precision, in UTC.
        return _datetime_from_microseconds(1e6 * float(value))


def _record_from_json(value, field):
    """Coerce 'value' to a mapping, if set or not nullable."""
    if _not_null(value, field):
        record = {}
        for subfield, cell in zip(field.fields, value['f']):
            converter = _CELLDATA_FROM_JSON[subfield.field_type]
            if field.mode == 'REPEATED':
                value = [converter(item, field) for item in cell['v']]
            else:
                value = converter(cell['v'], field)
            record[subfield.name] = value
        return record


def _string_from_json(value, _):
    """NOOP string -> string coercion"""
    return value


_CELLDATA_FROM_JSON = {
    'INTEGER': _int_from_json,
    'FLOAT': _float_from_json,
    'BOOLEAN': _bool_from_json,
    'TIMESTAMP': _datetime_from_json,
    'RECORD': _record_from_json,
    'STRING': _string_from_json,
}


def _rows_from_json(rows, schema):
    """Convert JSON row data to rows w/ appropriate types."""
    rows_data = []
    for row in rows:
        row_data = []
        for field, cell in zip(schema, row['f']):
            converter = _CELLDATA_FROM_JSON[field.field_type]
            if field.mode == 'REPEATED':
                row_data.append([converter(item, field)
                                 for item in cell['v']])
            else:
                row_data.append(converter(cell['v'], field))
        rows_data.append(tuple(row_data))
    return rows_data


class _ConfigurationProperty(object):
    """Base property implementation.

    Values will be stored on a `_configuration` helper attribute of the
    property's job instance.

    :type name: string
    :param name:  name of the property
    """

    def __init__(self, name):
        self.name = name
        self._backing_name = '_%s' % (self.name,)

    def __get__(self, instance, owner):
        """Descriptor protocal:  accesstor"""
        if instance is None:
            return self
        return getattr(instance._configuration, self._backing_name)

    def _validate(self, value):
        """Subclasses override to impose validation policy."""
        pass

    def __set__(self, instance, value):
        """Descriptor protocal:  mutator"""
        self._validate(value)
        setattr(instance._configuration, self._backing_name, value)

    def __delete__(self, instance):
        """Descriptor protocal:  deleter"""
        delattr(instance._configuration, self._backing_name)


class _TypedProperty(_ConfigurationProperty):
    """Property implementation:  validates based on value type.

    :type name: string
    :param name:  name of the property

    :type property_type: type or sequence of types
    :param property_type: type to be validated
    """
    def __init__(self, name, property_type):
        super(_TypedProperty, self).__init__(name)
        self.property_type = property_type

    def _validate(self, value):
        """Ensure that 'value' is of the appropriate type.

        :raises: ValueError on a type mismatch.
        """
        if not isinstance(value, self.property_type):
            raise ValueError('Required type: %s' % (self.property_type,))


class _EnumProperty(_ConfigurationProperty):
    """Psedo-enumeration class.

    Subclasses must define ``ALLOWED`` as a class-level constant:  it must
    be a sequence of strings.

    :type name: string
    :param name:  name of the property
    """
    def _validate(self, value):
        """Check that ``value`` is one of the allowed values.

        :raises: ValueError if value is not allowed.
        """
        if value not in self.ALLOWED:
            raise ValueError('Pass one of: %s' ', '.join(self.ALLOWED))
