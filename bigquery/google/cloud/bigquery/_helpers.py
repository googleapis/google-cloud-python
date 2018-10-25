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
import decimal

from google.cloud._helpers import UTC
from google.cloud._helpers import _date_from_iso8601_date
from google.cloud._helpers import _datetime_from_microseconds
from google.cloud._helpers import _microseconds_from_datetime
from google.cloud._helpers import _RFC3339_NO_FRACTION
from google.cloud._helpers import _to_bytes

_RFC3339_MICROS_NO_ZULU = '%Y-%m-%dT%H:%M:%S.%f'
_TIMEONLY_WO_MICROS = '%H:%M:%S'
_TIMEONLY_W_MICROS = '%H:%M:%S.%f'


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


def _decimal_from_json(value, field):
    """Coerce 'value' to a Decimal, if set or not nullable."""
    if _not_null(value, field):
        return decimal.Decimal(value)


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
        if len(value) == 8:  # HH:MM:SS
            fmt = _TIMEONLY_WO_MICROS
        elif len(value) == 15:  # HH:MM:SS.micros
            fmt = _TIMEONLY_W_MICROS
        else:
            raise ValueError("Unknown time format: {}".format(value))
        return datetime.datetime.strptime(value, fmt).time()


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
    'NUMERIC': _decimal_from_json,
    'BOOLEAN': _bool_from_json,
    'BOOL': _bool_from_json,
    'STRING': _string_from_json,
    'GEOGRAPHY': _string_from_json,
    'BYTES': _bytes_from_json,
    'TIMESTAMP': _timestamp_from_json,
    'DATETIME': _datetime_from_json,
    'DATE': _date_from_json,
    'TIME': _time_from_json,
    'RECORD': _record_from_json,
}

_QUERY_PARAMS_FROM_JSON = dict(_CELLDATA_FROM_JSON)
_QUERY_PARAMS_FROM_JSON['TIMESTAMP'] = _timestamp_query_param_from_json


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
    from google.cloud.bigquery import Row

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


def _decimal_to_json(value):
    """Coerce 'value' to a JSON-compatible representation."""
    if isinstance(value, decimal.Decimal):
        value = str(value)
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
    'NUMERIC': _decimal_to_json,
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


def _get_sub_prop(container, keys, default=None):
    """Get a nested value from a dictionary.

    This method works like ``dict.get(key)``, but for nested values.

    Arguments:
        container (dict):
            A dictionary which may contain other dictionaries as values.
        keys (iterable):
            A sequence of keys to attempt to get the value for. Each item in
            the sequence represents a deeper nesting. The first key is for
            the top level. If there is a dictionary there, the second key
            attempts to get the value within that, and so on.
        default (object):
            (Optional) Value to returned if any of the keys are not found.
            Defaults to ``None``.

    Examples:
        Get a top-level value (equivalent to ``container.get('key')``).

        >>> _get_sub_prop({'key': 'value'}, ['key'])
        'value'

        Get a top-level value, providing a default (equivalent to
        ``container.get('key', default='default')``).

        >>> _get_sub_prop({'nothere': 123}, ['key'], default='not found')
        'not found'

        Get a nested value.

        >>> _get_sub_prop({'key': {'subkey': 'value'}}, ['key', 'subkey'])
        'value'

    Returns:
        object: The value if present or the default.
    """
    sub_val = container
    for key in keys:
        if key not in sub_val:
            return default
        sub_val = sub_val[key]
    return sub_val


def _set_sub_prop(container, keys, value):
    """Set a nested value in a dictionary.

    Arguments:
        container (dict):
            A dictionary which may contain other dictionaries as values.
        keys (iterable):
            A sequence of keys to attempt to set the value for. Each item in
            the sequence represents a deeper nesting. The first key is for
            the top level. If there is a dictionary there, the second key
            attempts to get the value within that, and so on.
        value (object): Value to set within the container.

    Examples:
        Set a top-level value (equivalent to ``container['key'] = 'value'``).

        >>> container = {}
        >>> _set_sub_prop(container, ['key'], 'value')
        >>> container
        {'key': 'value'}

        Set a nested value.

        >>> container = {}
        >>> _set_sub_prop(container, ['key', 'subkey'], 'value')
        >>> container
        {'key': {'subkey': 'value'}}

        Replace a nested value.

        >>> container = {'key': {'subkey': 'prev'}}
        >>> _set_sub_prop(container, ['key', 'subkey'], 'new')
        >>> container
        {'key': {'subkey': 'new'}}
    """
    sub_val = container
    for key in keys[:-1]:
        if key not in sub_val:
            sub_val[key] = {}
        sub_val = sub_val[key]
    sub_val[keys[-1]] = value


def _del_sub_prop(container, keys):
    """Remove a nested key fro a dictionary.

    Arguments:
        container (dict):
            A dictionary which may contain other dictionaries as values.
        keys (iterable):
            A sequence of keys to attempt to clear the value for. Each item in
            the sequence represents a deeper nesting. The first key is for
            the top level. If there is a dictionary there, the second key
            attempts to get the value within that, and so on.

    Examples:
        Remove a top-level value (equivalent to ``del container['key']``).

        >>> container = {'key': 'value'}
        >>> _del_sub_prop(container, ['key'])
        >>> container
        {}

        Remove a nested value.

        >>> container = {'key': {'subkey': 'value'}}
        >>> _del_sub_prop(container, ['key', 'subkey'])
        >>> container
        {'key': {}}
    """
    sub_val = container
    for key in keys[:-1]:
        if key not in sub_val:
            sub_val[key] = {}
        sub_val = sub_val[key]
    if keys[-1] in sub_val:
        del sub_val[keys[-1]]


def _int_or_none(value):
    """Helper: deserialize int value from JSON string."""
    if isinstance(value, int):
        return value
    if value is not None:
        return int(value)


def _str_or_none(value):
    """Helper: serialize value to JSON string."""
    if value is not None:
        return str(value)
