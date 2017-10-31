# Copyright 2015 Google LLC
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
import datetime
import operator

import six

from google.api_core import retry
from google.cloud._helpers import UTC
from google.cloud._helpers import _date_from_iso8601_date
from google.cloud._helpers import _datetime_from_microseconds
from google.cloud._helpers import _microseconds_from_datetime
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


def _timestamp_query_param_from_json(value, field):
    """Coerce 'value' to a datetime, if set or not nullable.

    Args:
        value (str): The timestamp.
        field (.SchemaField): The field corresponding to the value.

    Returns:
        Optional[datetime.datetime]: The parsed datetime object from
        ``value`` if the ``field`` is not null (otherwise it is
        :data:`None`).
    """
    if _not_null(value, field):
        # Canonical formats for timestamps in BigQuery are flexible. See:
        # g.co/cloud/bigquery/docs/reference/standard-sql/data-types#timestamp-type
        # The separator between the date and time can be 'T' or ' '.
        value = value.replace(' ', 'T', 1)
        # The UTC timezone may be formatted as Z or +00:00.
        value = value.replace('Z', '')
        value = value.replace('+00:00', '')

        if '.' in value:
            # YYYY-MM-DDTHH:MM:SS.ffffff
            return datetime.datetime.strptime(
                value, _RFC3339_MICROS_NO_ZULU).replace(tzinfo=UTC)
        else:
            # YYYY-MM-DDTHH:MM:SS
            return datetime.datetime.strptime(
                value, _RFC3339_NO_FRACTION).replace(tzinfo=UTC)
    else:
        return None


def _datetime_from_json(value, field):
    """Coerce 'value' to a datetime, if set or not nullable.

    Args:
        value (str): The timestamp.
        field (.SchemaField): The field corresponding to the value.

    Returns:
        Optional[datetime.datetime]: The parsed datetime object from
        ``value`` if the ``field`` is not null (otherwise it is
        :data:`None`).
    """
    if _not_null(value, field):
        if '.' in value:
            # YYYY-MM-DDTHH:MM:SS.ffffff
            return datetime.datetime.strptime(value, _RFC3339_MICROS_NO_ZULU)
        else:
            # YYYY-MM-DDTHH:MM:SS
            return datetime.datetime.strptime(value, _RFC3339_NO_FRACTION)
    else:
        return None


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

_QUERY_PARAMS_FROM_JSON = dict(_CELLDATA_FROM_JSON)
_QUERY_PARAMS_FROM_JSON['TIMESTAMP'] = _timestamp_query_param_from_json


class Row(object):
    """A BigQuery row.

    Values can be accessed by position (index), by key like a dict,
    or as properties.

    :type values: tuple
    :param values:  the row values

    :type field_to_index: dict
    :param field_to_index:  a mapping from schema field names to indexes
    """

    # Choose unusual field names to try to avoid conflict with schema fields.
    __slots__ = ('_xxx_values', '_xxx_field_to_index')

    def __init__(self, values, field_to_index):
        self._xxx_values = values
        self._xxx_field_to_index = field_to_index

    def values(self):
        return self._xxx_values

    def __getattr__(self, name):
        i = self._xxx_field_to_index.get(name)
        if i is None:
            raise AttributeError('no row field "%s"' % name)
        return self._xxx_values[i]

    def __len__(self):
        return len(self._xxx_values)

    def __getitem__(self, key):
        if isinstance(key, six.string_types):
            i = self._xxx_field_to_index.get(key)
            if i is None:
                raise KeyError('no row field "%s"' % key)
            key = i
        return self._xxx_values[key]

    def __eq__(self, other):
        if not isinstance(other, Row):
            return NotImplemented
        return(
            self._xxx_values == other._xxx_values and
            self._xxx_field_to_index == other._xxx_field_to_index)

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        # sort field dict by value, for determinism
        items = sorted(self._xxx_field_to_index.items(),
                       key=operator.itemgetter(1))
        f2i = '{' + ', '.join('%r: %d' % i for i in items) + '}'
        return 'Row({}, {})'.format(self._xxx_values, f2i)


def _field_to_index_mapping(schema):
    """Create a mapping from schema field name to index of field."""
    return {f.name: i for i, f in enumerate(schema)}


def _row_tuple_from_json(row, schema):
    """Convert JSON row data to row with appropriate types.

    Note:  ``row['f']`` and ``schema`` are presumed to be of the same length.

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


def _rows_from_json(values, schema):
    """Convert JSON row data to rows with appropriate types."""
    field_to_index = _field_to_index_mapping(schema)
    return [Row(_row_tuple_from_json(r, schema), field_to_index)
            for r in values]


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


def _timestamp_to_json_parameter(value):
    """Coerce 'value' to an JSON-compatible representation.

    This version returns the string representation used in query parameters.
    """
    if isinstance(value, datetime.datetime):
        if value.tzinfo not in (None, UTC):
            # Convert to UTC and remove the time zone info.
            value = value.replace(tzinfo=None) - value.utcoffset()
        value = '%s %s+00:00' % (
            value.date().isoformat(), value.time().isoformat())
    return value


def _timestamp_to_json_row(value):
    """Coerce 'value' to an JSON-compatible representation.

    This version returns floating-point seconds value used in row data.
    """
    if isinstance(value, datetime.datetime):
        value = _microseconds_from_datetime(value) * 1e-6
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


# Converters used for scalar values marshalled as row data.
_SCALAR_VALUE_TO_JSON_ROW = {
    'INTEGER': _int_to_json,
    'INT64': _int_to_json,
    'FLOAT': _float_to_json,
    'FLOAT64': _float_to_json,
    'BOOLEAN': _bool_to_json,
    'BOOL': _bool_to_json,
    'BYTES': _bytes_to_json,
    'TIMESTAMP': _timestamp_to_json_row,
    'DATETIME': _datetime_to_json,
    'DATE': _date_to_json,
    'TIME': _time_to_json,
}


# Converters used for scalar values marshalled as query parameters.
_SCALAR_VALUE_TO_JSON_PARAM = _SCALAR_VALUE_TO_JSON_ROW.copy()
_SCALAR_VALUE_TO_JSON_PARAM['TIMESTAMP'] = _timestamp_to_json_parameter


def _snake_to_camel_case(value):
    """Convert snake case string to camel case."""
    words = value.split('_')
    return words[0] + ''.join(map(str.capitalize, words[1:]))


class _ApiResourceProperty(object):
    """Base property implementation.

    Values will be stored on a `_properties` helper attribute of the
    property's job instance.

    :type name: str
    :param name:  name of the property

    :type resource_name: str
    :param resource_name:  name of the property in the resource dictionary
    """

    def __init__(self, name, resource_name):
        self.name = name
        self.resource_name = resource_name

    def __get__(self, instance, owner):
        """Descriptor protocol:  accessor"""
        if instance is None:
            return self
        return instance._properties.get(self.resource_name)

    def _validate(self, value):
        """Subclasses override to impose validation policy."""
        pass

    def __set__(self, instance, value):
        """Descriptor protocol:  mutator"""
        self._validate(value)
        instance._properties[self.resource_name] = value

    def __delete__(self, instance):
        """Descriptor protocol:  deleter"""
        del instance._properties[self.resource_name]


class _TypedApiResourceProperty(_ApiResourceProperty):
    """Property implementation:  validates based on value type.

    :type name: str
    :param name:  name of the property

    :type resource_name: str
    :param resource_name:  name of the property in the resource dictionary

    :type property_type: type or sequence of types
    :param property_type: type to be validated
    """
    def __init__(self, name, resource_name, property_type):
        super(_TypedApiResourceProperty, self).__init__(
            name, resource_name)
        self.property_type = property_type

    def _validate(self, value):
        """Ensure that 'value' is of the appropriate type.

        :raises: ValueError on a type mismatch.
        """
        if value is None:
            return
        if not isinstance(value, self.property_type):
            raise ValueError('Required type: %s' % (self.property_type,))


class _ListApiResourceProperty(_ApiResourceProperty):
    """Property implementation:  validates based on value type.

    :type name: str
    :param name:  name of the property

    :type resource_name: str
    :param resource_name:  name of the property in the resource dictionary

    :type property_type: type or sequence of types
    :param property_type: type to be validated
    """
    def __init__(self, name, resource_name, property_type):
        super(_ListApiResourceProperty, self).__init__(
            name, resource_name)
        self.property_type = property_type

    def __get__(self, instance, owner):
        """Descriptor protocol:  accessor"""
        if instance is None:
            return self
        return instance._properties.get(self.resource_name, [])

    def _validate(self, value):
        """Ensure that 'value' is of the appropriate type.

        :raises: ValueError on a type mismatch.
        """
        if value is None:
            raise ValueError((
                'Required type: list of {}. '
                'To unset, use del or set to empty list').format(
                    self.property_type,))
        if not all(isinstance(item, self.property_type) for item in value):
            raise ValueError(
                'Required type: list of %s' % (self.property_type,))


class _EnumApiResourceProperty(_ApiResourceProperty):
    """Pseudo-enumeration class.

    :type name: str
    :param name:  name of the property.

    :type resource_name: str
    :param resource_name:  name of the property in the resource dictionary
    """


def _item_to_row(iterator, resource):
    """Convert a JSON row to the native object.

    .. note::

        This assumes that the ``schema`` attribute has been
        added to the iterator after being created, which
        should be done by the caller.

    :type iterator: :class:`~google.api_core.page_iterator.Iterator`
    :param iterator: The iterator that is currently in use.

    :type resource: dict
    :param resource: An item to be converted to a row.

    :rtype: :class:`~google.cloud.bigquery.Row`
    :returns: The next row in the page.
    """
    return Row(_row_tuple_from_json(resource, iterator.schema),
               iterator._field_to_index)


# pylint: disable=unused-argument
def _rows_page_start(iterator, page, response):
    """Grab total rows when :class:`~google.cloud.iterator.Page` starts.

    :type iterator: :class:`~google.api_core.page_iterator.Iterator`
    :param iterator: The iterator that is currently in use.

    :type page: :class:`~google.api_core.page_iterator.Page`
    :param page: The page that was just created.

    :type response: dict
    :param response: The JSON API response for a page of rows in a table.
    """
    total_rows = response.get('totalRows')
    if total_rows is not None:
        total_rows = int(total_rows)
    iterator.total_rows = total_rows
# pylint: enable=unused-argument


def _should_retry(exc):
    """Predicate for determining when to retry.

    We retry if and only if the 'reason' is 'backendError'
    or 'rateLimitExceeded'.
    """
    if not hasattr(exc, 'errors'):
        return False
    if len(exc.errors) == 0:
        return False
    reason = exc.errors[0]['reason']
    return reason == 'backendError' or reason == 'rateLimitExceeded'


DEFAULT_RETRY = retry.Retry(predicate=_should_retry)
"""The default retry object.

Any method with a ``retry`` parameter will be retried automatically,
with reasonable defaults. To disable retry, pass ``retry=None``.
To modify the default retry behavior, call a ``with_XXX`` method
on ``DEFAULT_RETRY``. For example, to change the deadline to 30 seconds,
pass ``retry=bigquery.DEFAULT_RETRY.with_deadline(30)``.
"""


def _int_or_none(value):
    """Helper: deserialize int value from JSON string."""
    if isinstance(value, int):
        return value
    if value is not None:
        return int(value)
