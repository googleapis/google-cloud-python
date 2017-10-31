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
import math

import six

from google.gax import CallOptions
from google.protobuf.struct_pb2 import ListValue
from google.protobuf.struct_pb2 import Value
from google.cloud.spanner_v1.proto import type_pb2

from google.cloud._helpers import _date_from_iso8601_date
from google.cloud._helpers import _datetime_to_rfc3339
from google.cloud._helpers import _RFC3339_NANOS
from google.cloud._helpers import _RFC3339_NO_FRACTION
from google.cloud._helpers import UTC


class TimestampWithNanoseconds(datetime.datetime):
    """Track nanosecond in addition to normal datetime attrs.

    nanosecond can be passed only as a keyword argument.
    """
    __slots__ = ('_nanosecond',)

    # pylint: disable=arguments-differ
    def __new__(cls, *args, **kw):
        nanos = kw.pop('nanosecond', 0)
        if nanos > 0:
            if 'microsecond' in kw:
                raise TypeError(
                    "Specify only one of 'microsecond' or 'nanosecond'")
            kw['microsecond'] = nanos // 1000
        inst = datetime.datetime.__new__(cls, *args, **kw)
        inst._nanosecond = nanos or 0
        return inst
    # pylint: disable=arguments-differ

    @property
    def nanosecond(self):
        """Read-only: nanosecond precision."""
        return self._nanosecond

    def rfc3339(self):
        """RFC 3339-compliant timestamp.

        :rtype: str
        :returns: Timestamp string according to RFC 3339 spec.
        """
        if self._nanosecond == 0:
            return _datetime_to_rfc3339(self)
        nanos = str(self._nanosecond).rstrip('0')
        return '%s.%sZ' % (self.strftime(_RFC3339_NO_FRACTION), nanos)

    @classmethod
    def from_rfc3339(cls, stamp):
        """Parse RFC 3339-compliant timestamp, preserving nanoseconds.

        :type stamp: str
        :param stamp: RFC 3339 stamp, with up to nanosecond precision

        :rtype: :class:`TimestampWithNanoseconds`
        :returns: an instance matching the timestamp string
        :raises ValueError: if ``stamp`` does not match the expected format
        """
        with_nanos = _RFC3339_NANOS.match(stamp)
        if with_nanos is None:
            raise ValueError(
                'Timestamp: %r, does not match pattern: %r' % (
                    stamp, _RFC3339_NANOS.pattern))
        bare = datetime.datetime.strptime(
            with_nanos.group('no_fraction'), _RFC3339_NO_FRACTION)
        fraction = with_nanos.group('nanos')
        if fraction is None:
            nanos = 0
        else:
            scale = 9 - len(fraction)
            nanos = int(fraction) * (10 ** scale)
        return cls(bare.year, bare.month, bare.day,
                   bare.hour, bare.minute, bare.second,
                   nanosecond=nanos, tzinfo=UTC)


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
        raise ValueError('Received a bytes that is not base64 encoded. '
                         'Ensure that you either send a Unicode string or a '
                         'base64-encoded bytes.')


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
        return Value(null_value='NULL_VALUE')
    if isinstance(value, list):
        return Value(list_value=_make_list_value_pb(value))
    if isinstance(value, bool):
        return Value(bool_value=value)
    if isinstance(value, six.integer_types):
        return Value(string_value=str(value))
    if isinstance(value, float):
        if math.isnan(value):
            return Value(string_value='NaN')
        if math.isinf(value):
            if value > 0:
                return Value(string_value='Infinity')
            else:
                return Value(string_value='-Infinity')
        return Value(number_value=value)
    if isinstance(value, TimestampWithNanoseconds):
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
def _parse_value_pb(value_pb, field_type):
    """Convert a Value protobuf to cell data.

    :type value_pb: :class:`~google.protobuf.struct_pb2.Value`
    :param value_pb: protobuf to convert

    :type field_type: :class:`~google.cloud.spanner_v1.proto.type_pb2.Type`
    :param field_type: type code for the value

    :rtype: varies on field_type
    :returns: value extracted from value_pb
    :raises ValueError: if unknown type is passed
    """
    if value_pb.HasField('null_value'):
        return None
    if field_type.code == type_pb2.STRING:
        result = value_pb.string_value
    elif field_type.code == type_pb2.BYTES:
        result = value_pb.string_value.encode('utf8')
    elif field_type.code == type_pb2.BOOL:
        result = value_pb.bool_value
    elif field_type.code == type_pb2.INT64:
        result = int(value_pb.string_value)
    elif field_type.code == type_pb2.FLOAT64:
        if value_pb.HasField('string_value'):
            result = float(value_pb.string_value)
        else:
            result = value_pb.number_value
    elif field_type.code == type_pb2.DATE:
        result = _date_from_iso8601_date(value_pb.string_value)
    elif field_type.code == type_pb2.TIMESTAMP:
        result = TimestampWithNanoseconds.from_rfc3339(value_pb.string_value)
    elif field_type.code == type_pb2.ARRAY:
        result = [
            _parse_value_pb(item_pb, field_type.array_element_type)
            for item_pb in value_pb.list_value.values]
    elif field_type.code == type_pb2.STRUCT:
        result = [
            _parse_value_pb(item_pb, field_type.struct_type.fields[i].type)
            for (i, item_pb) in enumerate(value_pb.list_value.values)]
    else:
        raise ValueError("Unknown type: %s" % (field_type,))
    return result
# pylint: enable=too-many-branches


def _parse_list_value_pbs(rows, row_type):
    """Convert a list of ListValue protobufs into a list of list of cell data.

    :type rows: list of :class:`~google.protobuf.struct_pb2.ListValue`
    :param rows: row data returned from a read/query

    :type row_type: :class:`~google.cloud.spanner_v1.proto.type_pb2.StructType`
    :param row_type: row schema specification

    :rtype: list of list of cell data
    :returns: data for the rows, coerced into appropriate types
    """
    result = []
    for row in rows:
        row_data = []
        for value_pb, field in zip(row.values, row_type.fields):
            row_data.append(_parse_value_pb(value_pb, field.type))
        result.append(row_data)
    return result


class _SessionWrapper(object):
    """Base class for objects wrapping a session.

    :type session: :class:`~google.cloud.spanner_v1.session.Session`
    :param session: the session used to perform the commit
    """
    def __init__(self, session):
        self._session = session


def _options_with_prefix(prefix, **kw):
    """Create GAPIC options w/ prefix.

    :type prefix: str
    :param prefix: appropriate resource path

    :type kw: dict
    :param kw: other keyword arguments passed to the constructor

    :rtype: :class:`~google.gax.CallOptions`
    :returns: GAPIC call options with supplied prefix
    """
    return CallOptions(
        metadata=[('google-cloud-resource-prefix', prefix)], **kw)
