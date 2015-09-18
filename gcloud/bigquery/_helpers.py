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
    return value is not None or field.mode != 'NULLABLE'


def _int_from_json(value, field):
    if _not_null(value, field):
        return int(value)


def _float_from_json(value, field):
    if _not_null(value, field):
        return float(value)


def _bool_from_json(value, field):
    if _not_null(value, field):
        return value.lower() in ['t', 'true', '1']


def _datetime_from_json(value, field):
    if _not_null(value, field):
        # value will be a float in seconds, to microsecond precision, in UTC.
        return _datetime_from_microseconds(1e6 * float(value))


def _record_from_json(value, field):
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
