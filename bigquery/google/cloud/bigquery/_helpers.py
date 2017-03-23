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

import base64
from collections import OrderedDict
import datetime

from google.cloud._helpers import UTC
from google.cloud._helpers import _date_from_iso8601_date
from google.cloud._helpers import _datetime_from_microseconds
from google.cloud._helpers import _RFC3339_NO_FRACTION
from google.cloud._helpers import _time_from_iso8601_time_naive
from google.cloud._helpers import _to_bytes

_RFC3339_MICROS_NO_ZULU = '%Y-%m-%dT%H:%M:%S.%f'


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


def _string_from_json(value, _):
    """NOOP string -> string coercion"""
    return value


def _bytes_from_json(value, field):
    """Base64-decode value"""
    if _not_null(value, field):
        return base64.standard_b64decode(_to_bytes(value))


def _timestamp_from_json(value, field):
    """Coerce 'value' to a datetime, if set or not nullable."""
    if _not_null(value, field):
        # value will be a float in seconds, to microsecond precision, in UTC.
        return _datetime_from_microseconds(1e6 * float(value))


def _datetime_from_json(value, field):
    """Coerce 'value' to a datetime, if set or not nullable."""
    if _not_null(value, field):
        # value will be a string, in YYYY-MM-DDTHH:MM:SS form.
        return datetime.datetime.strptime(value, _RFC3339_NO_FRACTION)


def _date_from_json(value, field):
    """Coerce 'value' to a datetime date, if set or not nullable"""
    if _not_null(value, field):
        # value will be a string, in YYYY-MM-DD form.
        return _date_from_iso8601_date(value)


def _time_from_json(value, field):
    """Coerce 'value' to a datetime date, if set or not nullable"""
    if _not_null(value, field):
        # value will be a string, in HH:MM:SS form.
        return _time_from_iso8601_time_naive(value)


def _record_from_json(value, field):
    """Coerce 'value' to a mapping, if set or not nullable."""
    if _not_null(value, field):
        record = {}
        record_iter = zip(field.fields, value['f'])
        for subfield, cell in record_iter:
            converter = _CELLDATA_FROM_JSON[subfield.field_type]
            if subfield.mode == 'REPEATED':
                value = [converter(item['v'], subfield) for item in cell['v']]
            else:
                value = converter(cell['v'], subfield)
            record[subfield.name] = value
        return record


_CELLDATA_FROM_JSON = {
    'INTEGER': _int_from_json,
    'INT64': _int_from_json,
    'FLOAT': _float_from_json,
    'FLOAT64': _float_from_json,
    'BOOLEAN': _bool_from_json,
    'BOOL': _bool_from_json,
    'STRING': _string_from_json,
    'BYTES': _bytes_from_json,
    'TIMESTAMP': _timestamp_from_json,
    'DATETIME': _datetime_from_json,
    'DATE': _date_from_json,
    'TIME': _time_from_json,
    'RECORD': _record_from_json,
}


def _int_to_json(value):
    """Coerce 'value' to an JSON-compatible representation."""
    if isinstance(value, int):
        value = str(value)
    return value


def _float_to_json(value):
    """Coerce 'value' to an JSON-compatible representation."""
    return value


def _bool_to_json(value):
    """Coerce 'value' to an JSON-compatible representation."""
    if isinstance(value, bool):
        value = 'true' if value else 'false'
    return value


def _bytes_to_json(value):
    """Coerce 'value' to an JSON-compatible representation."""
    if isinstance(value, bytes):
        value = base64.standard_b64encode(value).decode('ascii')
    return value


def _timestamp_to_json(value):
    """Coerce 'value' to an JSON-compatible representation."""
    if isinstance(value, datetime.datetime):
        if value.tzinfo not in (None, UTC):
            # Convert to UTC and remove the time zone info.
            value = value.replace(tzinfo=None) - value.utcoffset()
        value = '%s %s+00:00' % (
            value.date().isoformat(), value.time().isoformat())
    return value


def _datetime_to_json(value):
    """Coerce 'value' to an JSON-compatible representation."""
    if isinstance(value, datetime.datetime):
        value = value.strftime(_RFC3339_MICROS_NO_ZULU)
    return value


def _date_to_json(value):
    """Coerce 'value' to an JSON-compatible representation."""
    if isinstance(value, datetime.date):
        value = value.isoformat()
    return value


def _time_to_json(value):
    """Coerce 'value' to an JSON-compatible representation."""
    if isinstance(value, datetime.time):
        value = value.isoformat()
    return value


_SCALAR_VALUE_TO_JSON = {
    'INTEGER': _int_to_json,
    'INT64': _int_to_json,
    'FLOAT': _float_to_json,
    'FLOAT64': _float_to_json,
    'BOOLEAN': _bool_to_json,
    'BOOL': _bool_to_json,
    'BYTES': _bytes_to_json,
    'TIMESTAMP': _timestamp_to_json,
    'DATETIME': _datetime_to_json,
    'DATE': _date_to_json,
    'TIME': _time_to_json,
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
            row_data.append([converter(item['v'], field)
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


class AbstractQueryParameter(object):
    """Base class for named / positional query parameters.
    """
    @classmethod
    def from_api_repr(cls, resource):
        """Factory: construct paramter from JSON resource.

        :type resource: dict
        :param resource: JSON mapping of parameter

        :rtype: :class:`ScalarQueryParameter`
        """
        raise NotImplementedError

    def to_api_repr(self):
        """Construct JSON API representation for the parameter.

        :rtype: dict
        """
        raise NotImplementedError


class ScalarQueryParameter(AbstractQueryParameter):
    """Named / positional query parameters for scalar values.

    :type name: str or None
    :param name: Parameter name, used via ``@foo`` syntax.  If None, the
                 paramter can only be addressed via position (``?``).

    :type type_: str
    :param type_: name of parameter type.  One of 'STRING', 'INT64',
                  'FLOAT64', 'BOOL', 'TIMESTAMP', 'DATETIME', or 'DATE'.

    :type value: str, int, float, bool, :class:`datetime.datetime`, or
                 :class:`datetime.date`.
    :param value: the scalar parameter value.
    """
    def __init__(self, name, type_, value):
        self.name = name
        self.type_ = type_
        self.value = value

    @classmethod
    def positional(cls, type_, value):
        """Factory for positional paramters.

        :type type_: str
        :param type_:
            name of paramter type.  One of 'STRING', 'INT64',
            'FLOAT64', 'BOOL', 'TIMESTAMP', 'DATETIME', or 'DATE'.

        :type value: str, int, float, bool, :class:`datetime.datetime`, or
                     :class:`datetime.date`.
        :param value: the scalar parameter value.

        :rtype: :class:`ScalarQueryParameter`
        :returns: instance without name
        """
        return cls(None, type_, value)

    @classmethod
    def from_api_repr(cls, resource):
        """Factory: construct paramter from JSON resource.

        :type resource: dict
        :param resource: JSON mapping of parameter

        :rtype: :class:`ScalarQueryParameter`
        :returns: instance
        """
        name = resource.get('name')
        type_ = resource['parameterType']['type']
        value = resource['parameterValue']['value']
        converted = _CELLDATA_FROM_JSON[type_](value, None)
        return cls(name, type_, converted)

    def to_api_repr(self):
        """Construct JSON API representation for the parameter.

        :rtype: dict
        :returns: JSON mapping
        """
        value = self.value
        converter = _SCALAR_VALUE_TO_JSON.get(self.type_)
        if converter is not None:
            value = converter(value)
        resource = {
            'parameterType': {
                'type': self.type_,
            },
            'parameterValue': {
                'value': value,
            },
        }
        if self.name is not None:
            resource['name'] = self.name
        return resource


class ArrayQueryParameter(AbstractQueryParameter):
    """Named / positional query parameters for array values.

    :type name: str or None
    :param name: Parameter name, used via ``@foo`` syntax.  If None, the
                 paramter can only be addressed via position (``?``).

    :type array_type: str
    :param array_type:
        name of type of array elements.  One of `'STRING'`, `'INT64'`,
        `'FLOAT64'`, `'BOOL'`, `'TIMESTAMP'`, or `'DATE'`.

    :type values: list of appropriate scalar type.
    :param values: the parameter array values.
    """
    def __init__(self, name, array_type, values):
        self.name = name
        self.array_type = array_type
        self.values = values

    @classmethod
    def positional(cls, array_type, values):
        """Factory for positional paramters.

        :type array_type: str
        :param array_type:
            name of type of array elements.  One of `'STRING'`, `'INT64'`,
            `'FLOAT64'`, `'BOOL'`, `'TIMESTAMP'`, or `'DATE'`.

        :type values: list of appropriate scalar type
        :param values: the parameter array values.

        :rtype: :class:`ArrayQueryParameter`
        :returns: instance without name
        """
        return cls(None, array_type, values)

    @classmethod
    def from_api_repr(cls, resource):
        """Factory: construct paramter from JSON resource.

        :type resource: dict
        :param resource: JSON mapping of parameter

        :rtype: :class:`ArrayQueryParameter`
        :returns: instance
        """
        name = resource.get('name')
        array_type = resource['parameterType']['arrayType']['type']
        values = [
            value['value']
            for value
            in resource['parameterValue']['arrayValues']]
        converted = [
            _CELLDATA_FROM_JSON[array_type](value, None) for value in values]
        return cls(name, array_type, converted)

    def to_api_repr(self):
        """Construct JSON API representation for the parameter.

        :rtype: dict
        :returns: JSON mapping
        """
        values = self.values
        if self.array_type == 'RECORD':
            reprs = [value.to_api_repr() for value in values]
            a_type = reprs[0]['parameterType']
            a_values = [repr_['parameterValue'] for repr_ in reprs]
        else:
            a_type = {'type': self.array_type}
            converter = _SCALAR_VALUE_TO_JSON.get(self.array_type)
            if converter is not None:
                values = [converter(value) for value in values]
            a_values = [{'value': value} for value in values]
        resource = {
            'parameterType': {
                'type': 'ARRAY',
                'arrayType': a_type,
            },
            'parameterValue': {
                'arrayValues': a_values,
            },
        }
        if self.name is not None:
            resource['name'] = self.name
        return resource


class StructQueryParameter(AbstractQueryParameter):
    """Named / positional query parameters for struct values.

    :type name: str or None
    :param name: Parameter name, used via ``@foo`` syntax.  If None, the
                 paramter can only be addressed via position (``?``).

    :type sub_params: tuple of :class:`ScalarQueryParameter`
    :param sub_params: the sub-parameters for the struct
    """
    def __init__(self, name, *sub_params):
        self.name = name
        types = self.struct_types = OrderedDict()
        values = self.struct_values = {}
        for sub in sub_params:
            if isinstance(sub, self.__class__):
                types[sub.name] = 'STRUCT'
                values[sub.name] = sub
            elif isinstance(sub, ArrayQueryParameter):
                types[sub.name] = 'ARRAY'
                values[sub.name] = sub
            else:
                types[sub.name] = sub.type_
                values[sub.name] = sub.value

    @classmethod
    def positional(cls, *sub_params):
        """Factory for positional paramters.

        :type sub_params: tuple of :class:`ScalarQueryParameter`
        :param sub_params: the sub-parameters for the struct

        :rtype: :class:`StructQueryParameter`
        :returns: instance without name
        """
        return cls(None, *sub_params)

    @classmethod
    def from_api_repr(cls, resource):
        """Factory: construct paramter from JSON resource.

        :type resource: dict
        :param resource: JSON mapping of parameter

        :rtype: :class:`StructQueryParameter`
        :returns: instance
        """
        name = resource.get('name')
        instance = cls(name)
        types = instance.struct_types
        for item in resource['parameterType']['structTypes']:
            types[item['name']] = item['type']['type']
        struct_values = resource['parameterValue']['structValues']
        for key, value in struct_values.items():
            type_ = types[key]
            value = value['value']
            converted = _CELLDATA_FROM_JSON[type_](value, None)
            instance.struct_values[key] = converted
        return instance

    def to_api_repr(self):
        """Construct JSON API representation for the parameter.

        :rtype: dict
        :returns: JSON mapping
        """
        s_types = {}
        values = {}
        for name, value in self.struct_values.items():
            type_ = self.struct_types[name]
            if type_ in ('STRUCT', 'ARRAY'):
                repr_ = value.to_api_repr()
                s_types[name] = {'name': name, 'type': repr_['parameterType']}
                values[name] = repr_['parameterValue']
            else:
                s_types[name] = {'name': name, 'type': {'type': type_}}
                converter = _SCALAR_VALUE_TO_JSON.get(type_)
                if converter is not None:
                    value = converter(value)
                values[name] = {'value': value}

        resource = {
            'parameterType': {
                'type': 'STRUCT',
                'structTypes': [s_types[key] for key in self.struct_types],
            },
            'parameterValue': {
                'structValues': values,
            },
        }
        if self.name is not None:
            resource['name'] = self.name
        return resource


class QueryParametersProperty(object):
    """Custom property type, holding query parameter instances."""

    def __get__(self, instance, owner):
        """Descriptor protocol:  accessor

        :type instance: :class:`QueryParametersProperty`
        :param instance: instance owning the property (None if accessed via
                         the class).

        :type owner: type
        :param owner: the class owning the property.

        :rtype: list of instances of classes derived from
                :class:`AbstractQueryParameter`.
        :returns: the descriptor, if accessed via the class, or the instance's
                  query paramters.
        """
        if instance is None:
            return self
        return list(instance._query_parameters)

    def __set__(self, instance, value):
        """Descriptor protocol:  mutator

        :type instance: :class:`QueryParametersProperty`
        :param instance: instance owning the property (None if accessed via
                         the class).

        :type value: list of instances of classes derived from
                     :class:`AbstractQueryParameter`.
        :param value: new query parameters for the instance.
        """
        if not all(isinstance(u, AbstractQueryParameter) for u in value):
            raise ValueError(
                "query parameters must be derived from AbstractQueryParameter")
        instance._query_parameters = tuple(value)
