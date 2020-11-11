# Copyright 2016 Google LLC All rights reserved.
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

"""Helper functions for Cloud Spanner."""

import datetime
import decimal
import math

import six

from google.protobuf.struct_pb2 import ListValue
from google.protobuf.struct_pb2 import Value

from google.api_core import datetime_helpers
from google.cloud._helpers import _date_from_iso8601_date
from google.cloud._helpers import _datetime_to_rfc3339
from google.cloud.spanner_v1 import TypeCode
from google.cloud.spanner_v1 import ExecuteSqlRequest


def _try_to_coerce_bytes(bytestring):
    """Try to coerce a byte string into the right thing based on Python
    version and whether or not it is base64 encoded.

    Return a text string or raise ValueError.
    """
    # Attempt to coerce using google.protobuf.Value, which will expect
    # something that is utf-8 (and base64 consistently is).
    try:
        Value(string_value=bytestring)
        return bytestring
    except ValueError:
        raise ValueError(
            "Received a bytes that is not base64 encoded. "
            "Ensure that you either send a Unicode string or a "
            "base64-encoded bytes."
        )


def _merge_query_options(base, merge):
    """Merge higher precedence QueryOptions with current QueryOptions.

    :type base:
        :class:`~google.cloud.spanner_v1.ExecuteSqlRequest.QueryOptions`
        or :class:`dict` or None
    :param base: The current QueryOptions that is intended for use.

    :type merge:
        :class:`~google.cloud.spanner_v1.ExecuteSqlRequest.QueryOptions`
        or :class:`dict` or None
    :param merge:
        The QueryOptions that have a higher priority than base. These options
        should overwrite the fields in base.

    :rtype:
        :class:`~google.cloud.spanner_v1.ExecuteSqlRequest.QueryOptions`
        or None
    :returns:
        QueryOptions object formed by merging the two given QueryOptions.
        If the resultant object only has empty fields, returns None.
    """
    combined = base or ExecuteSqlRequest.QueryOptions()
    if type(combined) == dict:
        combined = ExecuteSqlRequest.QueryOptions(
            optimizer_version=combined.get("optimizer_version", "")
        )
    merge = merge or ExecuteSqlRequest.QueryOptions()
    if type(merge) == dict:
        merge = ExecuteSqlRequest.QueryOptions(
            optimizer_version=merge.get("optimizer_version", "")
        )
    type(combined).pb(combined).MergeFrom(type(merge).pb(merge))
    if not combined.optimizer_version:
        return None
    return combined


# pylint: disable=too-many-return-statements,too-many-branches
def _make_value_pb(value):
    """Helper for :func:`_make_list_value_pbs`.

    :type value: scalar value
    :param value: value to convert

    :rtype: :class:`~google.protobuf.struct_pb2.Value`
    :returns: value protobufs
    :raises ValueError: if value is not of a known scalar type.
    """
    if value is None:
        return Value(null_value="NULL_VALUE")
    if isinstance(value, (list, tuple)):
        return Value(list_value=_make_list_value_pb(value))
    if isinstance(value, bool):
        return Value(bool_value=value)
    if isinstance(value, six.integer_types):
        return Value(string_value=str(value))
    if isinstance(value, float):
        if math.isnan(value):
            return Value(string_value="NaN")
        if math.isinf(value):
            if value > 0:
                return Value(string_value="Infinity")
            else:
                return Value(string_value="-Infinity")
        return Value(number_value=value)
    if isinstance(value, datetime_helpers.DatetimeWithNanoseconds):
        return Value(string_value=value.rfc3339())
    if isinstance(value, datetime.datetime):
        return Value(string_value=_datetime_to_rfc3339(value))
    if isinstance(value, datetime.date):
        return Value(string_value=value.isoformat())
    if isinstance(value, six.binary_type):
        value = _try_to_coerce_bytes(value)
        return Value(string_value=value)
    if isinstance(value, six.text_type):
        return Value(string_value=value)
    if isinstance(value, ListValue):
        return Value(list_value=value)
    if isinstance(value, decimal.Decimal):
        return Value(string_value=str(value))
    raise ValueError("Unknown type: %s" % (value,))


# pylint: enable=too-many-return-statements,too-many-branches


def _make_list_value_pb(values):
    """Construct of ListValue protobufs.

    :type values: list of scalar
    :param values: Row data

    :rtype: :class:`~google.protobuf.struct_pb2.ListValue`
    :returns: protobuf
    """
    return ListValue(values=[_make_value_pb(value) for value in values])


def _make_list_value_pbs(values):
    """Construct a sequence of ListValue protobufs.

    :type values: list of list of scalar
    :param values: Row data

    :rtype: list of :class:`~google.protobuf.struct_pb2.ListValue`
    :returns: sequence of protobufs
    """
    return [_make_list_value_pb(row) for row in values]


# pylint: disable=too-many-branches
def _parse_value(value, field_type):
    if value is None:
        return None
    if field_type.code == TypeCode.STRING:
        result = value
    elif field_type.code == TypeCode.BYTES:
        result = value.encode("utf8")
    elif field_type.code == TypeCode.BOOL:
        result = value
    elif field_type.code == TypeCode.INT64:
        result = int(value)
    elif field_type.code == TypeCode.FLOAT64:
        if isinstance(value, str):
            result = float(value)
        else:
            result = value
    elif field_type.code == TypeCode.DATE:
        result = _date_from_iso8601_date(value)
    elif field_type.code == TypeCode.TIMESTAMP:
        DatetimeWithNanoseconds = datetime_helpers.DatetimeWithNanoseconds
        result = DatetimeWithNanoseconds.from_rfc3339(value)
    elif field_type.code == TypeCode.ARRAY:
        result = [_parse_value(item, field_type.array_element_type) for item in value]
    elif field_type.code == TypeCode.STRUCT:
        result = [
            _parse_value(item, field_type.struct_type.fields[i].type_)
            for (i, item) in enumerate(value)
        ]
    elif field_type.code == TypeCode.NUMERIC:
        result = decimal.Decimal(value)
    else:
        raise ValueError("Unknown type: %s" % (field_type,))
    return result


def _parse_value_pb(value_pb, field_type):
    """Convert a Value protobuf to cell data.

    :type value_pb: :class:`~google.protobuf.struct_pb2.Value`
    :param value_pb: protobuf to convert

    :type field_type: :class:`~google.cloud.spanner_v1.Type`
    :param field_type: type code for the value

    :rtype: varies on field_type
    :returns: value extracted from value_pb
    :raises ValueError: if unknown type is passed
    """
    if value_pb.HasField("null_value"):
        return None
    if value_pb.HasField("string_value"):
        return _parse_value(value_pb.string_value, field_type)
    if value_pb.HasField("bool_value"):
        return _parse_value(value_pb.bool_value, field_type)
    if value_pb.HasField("number_value"):
        return _parse_value(value_pb.number_value, field_type)
    if value_pb.HasField("list_value"):
        return _parse_value(value_pb.list_value, field_type)
    raise ValueError("No value set in Value: %s" % (value_pb,))


# pylint: enable=too-many-branches


def _parse_list_value_pbs(rows, row_type):
    """Convert a list of ListValue protobufs into a list of list of cell data.

    :type rows: list of :class:`~google.protobuf.struct_pb2.ListValue`
    :param rows: row data returned from a read/query

    :type row_type: :class:`~google.cloud.spanner_v1.StructType`
    :param row_type: row schema specification

    :rtype: list of list of cell data
    :returns: data for the rows, coerced into appropriate types
    """
    result = []
    for row in rows:
        row_data = []
        for value_pb, field in zip(row.values, row_type.fields):
            row_data.append(_parse_value_pb(value_pb, field.type_))
        result.append(row_data)
    return result


class _SessionWrapper(object):
    """Base class for objects wrapping a session.

    :type session: :class:`~google.cloud.spanner_v1.session.Session`
    :param session: the session used to perform the commit
    """

    def __init__(self, session):
        self._session = session


def _metadata_with_prefix(prefix, **kw):
    """Create RPC metadata containing a prefix.

    Args:
        prefix (str): appropriate resource path.

    Returns:
        List[Tuple[str, str]]: RPC metadata with supplied prefix
    """
    return [("google-cloud-resource-prefix", prefix)]
