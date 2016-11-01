# Copyright 2015 Google Inc.
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

"""Shared helper functions for BigQuery API classes."""

from google.cloud._helpers import _datetime_from_microseconds
from google.cloud._helpers import _date_from_iso8601_date


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


def _date_from_json(value, field):
    """Coerce 'value' to a datetime date, if set or not nullable"""
    if _not_null(value, field):
        return _date_from_iso8601_date(value)


def _record_from_json(value, field):
    """Coerce 'value' to a mapping, if set or not nullable."""
    if _not_null(value, field):
        record = {}
        for subfield, cell in zip(field.fields, value['f']):
            converter = _CELLDATA_FROM_JSON[subfield.field_type]
            if field.mode == 'REPEATED':
                value = [converter(item, subfield) for item in cell['v']]
            else:
                value = converter(cell['v'], subfield)
            record[subfield.name] = value
        return record


def _string_from_json(value, _):
    """NOOP string -> string coercion"""
    return value


_CELLDATA_FROM_JSON = {
    'INTEGER': _int_from_json,
    'INT64': _int_from_json,
    'FLOAT': _float_from_json,
    'FLOAT64': _float_from_json,
    'BOOLEAN': _bool_from_json,
    'TIMESTAMP': _datetime_from_json,
    'DATE': _date_from_json,
    'RECORD': _record_from_json,
    'STRING': _string_from_json,
}


def _row_from_json(row, schema):
    """Convert JSON row data to row with appropriate types.

    :type row: dict
    :param row: A JSON response row to be converted.

    :type schema: tuple
    :param schema: A tuple of
                   :class:`~google.cloud.bigquery.schema.SchemaField`.

    :rtype: tuple
    :returns: A tuple of data converted to native types.
    """
    row_data = []
    for field, cell in zip(schema, row['f']):
        converter = _CELLDATA_FROM_JSON[field.field_type]
        if field.mode == 'REPEATED':
            row_data.append([converter(item, field)
                             for item in cell['v']])
        else:
            row_data.append(converter(cell['v'], field))

    return tuple(row_data)


def _rows_from_json(rows, schema):
    """Convert JSON row data to rows with appropriate types."""
    return [_row_from_json(row, schema) for row in rows]


class _ConfigurationProperty(object):
    """Base property implementation.

    Values will be stored on a `_configuration` helper attribute of the
    property's job instance.

    :type name: str
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

    :type name: str
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
    """Pseudo-enumeration class.

    Subclasses must define ``ALLOWED`` as a class-level constant:  it must
    be a sequence of strings.

    :type name: str
    :param name:  name of the property.
    """
    def _validate(self, value):
        """Check that ``value`` is one of the allowed values.

        :raises: ValueError if value is not allowed.
        """
        if value not in self.ALLOWED:
            raise ValueError('Pass one of: %s' ', '.join(self.ALLOWED))


class UDFResource(object):
    """Describe a single user-defined function (UDF) resource.

    :type udf_type: str
    :param udf_type: the type of the resource ('inlineCode' or 'resourceUri')

    :type value: str
    :param value: the inline code or resource URI.

    See
    https://cloud.google.com/bigquery/user-defined-functions#api
    """
    def __init__(self, udf_type, value):
        self.udf_type = udf_type
        self.value = value

    def __eq__(self, other):
        return(
            self.udf_type == other.udf_type and
            self.value == other.value)


class UDFResourcesProperty(object):
    """Custom property type, holding :class:`UDFResource` instances."""

    def __get__(self, instance, owner):
        """Descriptor protocol:  accessor"""
        if instance is None:
            return self
        return list(instance._udf_resources)

    def __set__(self, instance, value):
        """Descriptor protocol:  mutator"""
        if not all(isinstance(u, UDFResource) for u in value):
            raise ValueError("udf items must be UDFResource")
        instance._udf_resources = tuple(value)


def _build_udf_resources(resources):
    """
    :type resources: sequence of :class:`UDFResource`
    :param resources: fields to be appended.

    :rtype: mapping
    :returns: a mapping describing userDefinedFunctionResources for the query.
    """
    udfs = []
    for resource in resources:
        udf = {resource.udf_type: resource.value}
        udfs.append(udf)
    return udfs
