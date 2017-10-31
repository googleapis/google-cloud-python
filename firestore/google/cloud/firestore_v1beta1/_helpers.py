# Copyright 2017 Google LLC All rights reserved.
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

"""Common helpers shared across Google Cloud Firestore modules."""


import collections
import contextlib
import datetime
import sys

import google.gax
import google.gax.errors
import google.gax.grpc
from google.protobuf import struct_pb2
from google.type import latlng_pb2
import grpc
import six

from google.cloud._helpers import _datetime_to_pb_timestamp
from google.cloud._helpers import _pb_timestamp_to_datetime
from google.cloud import exceptions

from google.cloud.firestore_v1beta1 import constants
from google.cloud.firestore_v1beta1.gapic import enums
from google.cloud.firestore_v1beta1.proto import common_pb2
from google.cloud.firestore_v1beta1.proto import document_pb2
from google.cloud.firestore_v1beta1.proto import write_pb2


BAD_PATH_TEMPLATE = (
    'A path element must be a string. Received {}, which is a {}.')
FIELD_PATH_MISSING_TOP = '{!r} is not contained in the data'
FIELD_PATH_MISSING_KEY = '{!r} is not contained in the data for the key {!r}'
FIELD_PATH_WRONG_TYPE = (
    'The data at {!r} is not a dictionary, so it cannot contain the key {!r}')
FIELD_PATH_DELIMITER = '.'
DOCUMENT_PATH_DELIMITER = '/'
_NO_CREATE_TEMPLATE = (
    'The ``create_if_missing`` option cannot be used '
    'on ``{}()`` requests.')
NO_CREATE_ON_DELETE = _NO_CREATE_TEMPLATE.format('delete')
INACTIVE_TXN = (
    'Transaction not in progress, cannot be used in API requests.')
READ_AFTER_WRITE_ERROR = 'Attempted read after write in a transaction.'
BAD_REFERENCE_ERROR = (
    'Reference value {!r} in unexpected format, expected to be of the form '
    '``projects/{{project}}/databases/{{database}}/'
    'documents/{{document_path}}``.')
WRONG_APP_REFERENCE = (
    'Document {!r} does not correspond to the same database '
    '({!r}) as the client.')
REQUEST_TIME_ENUM = (
    enums.DocumentTransform.FieldTransform.ServerValue.REQUEST_TIME)
_GRPC_ERROR_MAPPING = {
    grpc.StatusCode.ALREADY_EXISTS: exceptions.Conflict,
    grpc.StatusCode.NOT_FOUND: exceptions.NotFound,
}


class GeoPoint(object):
    """Simple container for a geo point value.

    Args:
        latitude (float): Latitude of a point.
        longitude (float): Longitude of a point.
    """

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def to_protobuf(self):
        """Convert the current object to protobuf.

        Returns:
            google.type.latlng_pb2.LatLng: The current point as a protobuf.
        """
        return latlng_pb2.LatLng(latitude=self.latitude,
                                 longitude=self.longitude)

    def __eq__(self, other):
        """Compare two geo points for equality.

        Returns:
            Union[bool, NotImplemented]: :data:`True` if the points compare
            equal, else :data:`False`. (Or :data:`NotImplemented` if
            ``other`` is not a geo point.)
        """
        if not isinstance(other, GeoPoint):
            return NotImplemented

        return (self.latitude == other.latitude and
                self.longitude == other.longitude)

    def __ne__(self, other):
        """Compare two geo points for inequality.

        Returns:
            Union[bool, NotImplemented]: :data:`False` if the points compare
            equal, else :data:`True`. (Or :data:`NotImplemented` if
            ``other`` is not a geo point.)
        """
        equality_val = self.__eq__(other)
        if equality_val is NotImplemented:
            return NotImplemented
        else:
            return not equality_val


class FieldPathHelper(object):
    """Helper to convert field names and paths for usage in a request.

    Also supports field deletes.

    Args:
        field_updates (dict): Field names or paths to update and values
            to update with.
    """

    PATH_END = object()
    FIELD_PATH_CONFLICT = 'Field paths {!r} and {!r} conflict'

    def __init__(self, field_updates):
        self.field_updates = field_updates
        self.update_values = {}
        """Dict[str, Any]: The stage updates to be sent.

        On success of :meth:`add_value_at_field_path`, the unpacked version of
        a field path will be added to this as a key, and it will point to
        the ``value`` provided (unless it is a delete).
        """
        self.field_paths = []
        """List[str, ...]: List of field paths already considered.

        On success of :meth:`add_value_at_field_path`, a ``field_path`` will be
        appended to this list.

        """
        self.unpacked_field_paths = {}
        """Dict[str, Any]: A structured version of ``field_paths``.

        This is used to check for ambiguity.

        ``update_values`` and ``unpacked_field_paths`` **must** be tracked
        separately because ``value``-s inserted could be a dictionary, so at a
        certain level of nesting the distinction between the data and the field
        path would be lost. For example, ``{'a.b': {'c': 10}`` and
        ``{'a.b.c': 10}`` would be indistinguishable if only ``update_values``
        was used to track contradictions. In addition, for deleted values,
        **only** ``field_paths`` is updated, so there would be no way of
        tracking a contradiction in ``update_values``.
        """

    def get_update_values(self, value):
        """Get the dictionary of updates.

        If the ``value`` is the delete sentinel, we'll use a throw-away
        dictionary so that the actual updates are not polluted.

        Args:
            value (Any): A value to (eventually) be added to
                ``update_values``.

        Returns:
            dict: The dictionary of updates.
        """
        if value is constants.DELETE_FIELD:
            return {}
        else:
            return self.update_values

    def check_conflict(self, field_path, parts, index, curr_paths):
        """Check if ``field_path`` has a conflict with an existing field path.

        Args:
            field_path (str): The field path being considered.
            parts (List[str, ...]): The parts in ``field_path``.
            index (int): The number of parts (in ``field_path``) we have nested
                when ``curr_paths`` is reached.
            curr_paths (Union[dict, object]): Either the field_path end
                sentinel or a dictionary of the field paths at the next
                nesting level.

        Raises:
            ValueError: If there is a conflict.
        """
        if curr_paths is self.PATH_END:
            partial = get_field_path(parts[:index + 1])
            msg = self.FIELD_PATH_CONFLICT.format(partial, field_path)
            raise ValueError(msg)

    def path_end_conflict(self, field_path, conflicting_paths):
        """Help raise a useful exception about field path conflicts.

        Helper for :meth:`add_field_path_end`.

        This method is really only needed for raising a useful error, but
        is worth isolating as a method since it is not entirely trivial to
        "re-compute" another field path that conflicts with ``field_path``.
        There may be multiple conflicts, but this just finds **one** field
        path which starts with ``field_path``.

        Args:
            field_path (str): The field path that has conflicts somewhere in
                ``conflicting_paths``.
            conflicting_paths (dict): A sub-dictionary containing path parts
                as keys and nesting until a field path ends, at which point
                the path end sentinel is the value.

        Returns:
            ValueError: Always.
        """
        conflict_parts = [field_path]
        while conflicting_paths is not self.PATH_END:
            # Grab any item, we are just looking for one example.
            part, conflicting_paths = next(six.iteritems(conflicting_paths))
            conflict_parts.append(part)

        conflict = get_field_path(conflict_parts)
        msg = self.FIELD_PATH_CONFLICT.format(field_path, conflict)
        return ValueError(msg)

    def add_field_path_end(
            self, field_path, value, final_part, curr_paths, to_update):
        """Add the last segment in a field path.

        Helper for :meth:`add_value_at_field_path`.

        Args:
            field_path (str): The field path being considered.
            value (Any): The value to update a field with.
            final_part (str): The last segment in ``field_path``.
            curr_paths (Union[dict, object]): Either the path end sentinel
                or a dictionary of the paths at the next nesting level.
            to_update (dict): The dictionary of the unpacked ``field_path``
                which need be updated with ``value``.

        Raises:
            ValueError: If there is a conflict.
        """
        if final_part in curr_paths:
            conflicting_paths = curr_paths[final_part]
            raise self.path_end_conflict(field_path, conflicting_paths)
        else:
            curr_paths[final_part] = self.PATH_END
            # NOTE: For a delete, ``to_update`` won't actually go anywhere
            #       since ``get_update_values`` returns a throw-away
            #       dictionary.
            to_update[final_part] = value
            self.field_paths.append(field_path)

    def add_value_at_field_path(self, field_path, value):
        """Add a field path to the staged updates.

        Also makes sure the field path is not ambiguous or contradictory with
        any existing path in ``field_paths`` / ``unpacked_field_paths``.

        To understand what will be failed, consider the following. If both
        ``foo`` and ``foo.bar`` are paths, then the update from ``foo``
        **should** supersede the update from ``foo.bar``. However, if the
        caller expected the ``foo.bar`` update to occur as well, this could
        cause unexpected behavior. Hence, that combination cause an error.

        Args:
            field_path (str): The field path being considered (it may just be
                a field name).
            value (Any): The value to update a field with.

        Raises:
            ValueError: If there is an ambiguity.
        """
        parts = parse_field_path(field_path)
        to_update = self.get_update_values(value)
        curr_paths = self.unpacked_field_paths
        for index, part in enumerate(parts[:-1]):
            curr_paths = curr_paths.setdefault(part, {})
            self.check_conflict(field_path, parts, index, curr_paths)
            to_update = to_update.setdefault(part, {})

        self.add_field_path_end(
            field_path, value, parts[-1], curr_paths, to_update)

    def parse(self):
        """Parse the ``field_updates`` into update values and field paths.

        Returns:
            Tuple[dict, List[str, ...]]: A pair of

            * The true value dictionary to use for updates (may differ
              from ``field_updates`` after field paths are "unpacked").
            * The list of field paths to send (for updates and deletes).
        """
        for key, value in six.iteritems(self.field_updates):
            self.add_value_at_field_path(key, value)

        return self.update_values, self.field_paths

    @classmethod
    def to_field_paths(cls, field_updates):
        """Convert field names and paths for usage in a request.

        Also supports field deletes.

        Args:
            field_updates (dict): Field names or paths to update and values
                to update with.

        Returns:
            Tuple[dict, List[str, ...]]: A pair of

            * The true value dictionary to use for updates (may differ
              from ``field_updates`` after field paths are "unpacked").
            * The list of field paths to send (for updates and deletes).
        """
        helper = cls(field_updates)
        return helper.parse()


class ReadAfterWriteError(Exception):
    """Raised when a read is attempted after a write.

    Raised by "read" methods that use transactions.
    """


def verify_path(path, is_collection):
    """Verifies that a ``path`` has the correct form.

    Checks that all of the elements in ``path`` are strings.

    Args:
        path (Tuple[str, ...]): The components in a collection or
            document path.
        is_collection (bool): Indicates if the ``path`` represents
            a document or a collection.

    Raises:
        ValueError: if

            * the ``path`` is empty
            * ``is_collection=True`` and there are an even number of elements
            * ``is_collection=False`` and there are an odd number of elements
            * an element is not a string
    """
    num_elements = len(path)
    if num_elements == 0:
        raise ValueError('Document or collection path cannot be empty')

    if is_collection:
        if num_elements % 2 == 0:
            raise ValueError(
                'A collection must have an odd number of path elements')
    else:
        if num_elements % 2 == 1:
            raise ValueError(
                'A document must have an even number of path elements')

    for element in path:
        if not isinstance(element, six.string_types):
            msg = BAD_PATH_TEMPLATE.format(element, type(element))
            raise ValueError(msg)


def encode_value(value):
    """Converts a native Python value into a Firestore protobuf ``Value``.

    Args:
        value (Union[NoneType, bool, int, float, datetime.datetime, \
            str, bytes, dict, ~google.cloud.Firestore.GeoPoint]): A native
            Python value to convert to a protobuf field.

    Returns:
        ~google.cloud.firestore_v1beta1.types.Value: A
        value encoded as a Firestore protobuf.

    Raises:
        TypeError: If the ``value`` is not one of the accepted types.
    """
    if value is None:
        return document_pb2.Value(null_value=struct_pb2.NULL_VALUE)

    # Must come before six.integer_types since ``bool`` is an integer subtype.
    if isinstance(value, bool):
        return document_pb2.Value(boolean_value=value)

    if isinstance(value, six.integer_types):
        return document_pb2.Value(integer_value=value)

    if isinstance(value, float):
        return document_pb2.Value(double_value=value)

    if isinstance(value, datetime.datetime):
        return document_pb2.Value(
            timestamp_value=_datetime_to_pb_timestamp(value))

    if isinstance(value, six.text_type):
        return document_pb2.Value(string_value=value)

    if isinstance(value, six.binary_type):
        return document_pb2.Value(bytes_value=value)

    # NOTE: We avoid doing an isinstance() check for a Document
    #       here to avoid import cycles.
    document_path = getattr(value, '_document_path', None)
    if document_path is not None:
        return document_pb2.Value(reference_value=document_path)

    if isinstance(value, GeoPoint):
        return document_pb2.Value(geo_point_value=value.to_protobuf())

    if isinstance(value, list):
        value_list = [encode_value(element) for element in value]
        value_pb = document_pb2.ArrayValue(values=value_list)
        return document_pb2.Value(array_value=value_pb)

    if isinstance(value, dict):
        value_dict = encode_dict(value)
        value_pb = document_pb2.MapValue(fields=value_dict)
        return document_pb2.Value(map_value=value_pb)

    raise TypeError(
        'Cannot convert to a Firestore Value', value,
        'Invalid type', type(value))


def encode_dict(values_dict):
    """Encode a dictionary into protobuf ``Value``-s.

    Args:
        values_dict (dict): The dictionary to encode as protobuf fields.

    Returns:
        Dict[str, ~google.cloud.firestore_v1beta1.types.Value]: A
        dictionary of string keys and ``Value`` protobufs as dictionary
        values.
    """
    return {
        key: encode_value(value)
        for key, value in six.iteritems(values_dict)
    }


def reference_value_to_document(reference_value, client):
    """Convert a reference value string to a document.

    Args:
        reference_value (str): A document reference value.
        client (~.firestore_v1beta1.client.Client): A client that has
            a document factory.

    Returns:
        ~.firestore_v1beta1.document.DocumentReference: The document
        corresponding to ``reference_value``.

    Raises:
        ValueError: If the ``reference_value`` is not of the expected
            format: ``projects/{project}/databases/{database}/documents/...``.
        ValueError: If the ``reference_value`` does not come from the same
            project / database combination as the ``client``.
    """
    # The first 5 parts are
    # projects, {project}, databases, {database}, documents
    parts = reference_value.split(DOCUMENT_PATH_DELIMITER, 5)
    if len(parts) != 6:
        msg = BAD_REFERENCE_ERROR.format(reference_value)
        raise ValueError(msg)

    # The sixth part is `a/b/c/d` (i.e. the document path)
    document = client.document(parts[-1])
    if document._document_path != reference_value:
        msg = WRONG_APP_REFERENCE.format(
            reference_value, client._database_string)
        raise ValueError(msg)

    return document


def decode_value(value, client):
    """Converts a Firestore protobuf ``Value`` to a native Python value.

    Args:
        value (google.cloud.firestore_v1beta1.types.Value): A
            Firestore protobuf to be decoded / parsed / converted.
        client (~.firestore_v1beta1.client.Client): A client that has
            a document factory.

    Returns:
        Union[NoneType, bool, int, float, datetime.datetime, \
            str, bytes, dict, ~google.cloud.Firestore.GeoPoint]: A native
        Python value converted from the ``value``.

    Raises:
        NotImplementedError: If the ``value_type`` is ``reference_value``.
        ValueError: If the ``value_type`` is unknown.
    """
    value_type = value.WhichOneof('value_type')

    if value_type == 'null_value':
        return None
    elif value_type == 'boolean_value':
        return value.boolean_value
    elif value_type == 'integer_value':
        return value.integer_value
    elif value_type == 'double_value':
        return value.double_value
    elif value_type == 'timestamp_value':
        # NOTE: This conversion is "lossy", Python ``datetime.datetime``
        #       has microsecond precision but ``timestamp_value`` has
        #       nanosecond precision.
        return _pb_timestamp_to_datetime(value.timestamp_value)
    elif value_type == 'string_value':
        return value.string_value
    elif value_type == 'bytes_value':
        return value.bytes_value
    elif value_type == 'reference_value':
        return reference_value_to_document(value.reference_value, client)
    elif value_type == 'geo_point_value':
        return GeoPoint(
            value.geo_point_value.latitude,
            value.geo_point_value.longitude)
    elif value_type == 'array_value':
        return [decode_value(element, client)
                for element in value.array_value.values]
    elif value_type == 'map_value':
        return decode_dict(value.map_value.fields, client)
    else:
        raise ValueError('Unknown ``value_type``', value_type)


def decode_dict(value_fields, client):
    """Converts a protobuf map of Firestore ``Value``-s.

    Args:
        value_fields (google.protobuf.pyext._message.MessageMapContainer): A
            protobuf map of Firestore ``Value``-s.
        client (~.firestore_v1beta1.client.Client): A client that has
            a document factory.

    Returns:
        Dict[str, Union[NoneType, bool, int, float, datetime.datetime, \
            str, bytes, dict, ~google.cloud.Firestore.GeoPoint]]: A dictionary
        of native Python values converted from the ``value_fields``.
    """
    return {
        key: decode_value(value, client)
        for key, value in six.iteritems(value_fields)
    }


def get_field_path(field_names):
    """Create a **field path** from a list of nested field names.

    A **field path** is a ``.``-delimited concatenation of the field
    names. It is used to represent a nested field. For example,
    in the data

    .. code-block: python

       data = {
          'aa': {
              'bb': {
                  'cc': 10,
              },
          },
       }

    the field path ``'aa.bb.cc'`` represents that data stored in
    ``data['aa']['bb']['cc']``.

    Args:
        field_names (Iterable[str, ...]): The list of field names.

    Returns:
        str: The ``.``-delimited field path.
    """
    return FIELD_PATH_DELIMITER.join(field_names)


def parse_field_path(field_path):
    """Parse a **field path** from into a list of nested field names.

    See :func:`field_path` for more on **field paths**.

    Args:
        field_path (str): The ``.``-delimited field path to parse.

    Returns:
        List[str, ...]: The list of field names in the field path.
    """
    return field_path.split(FIELD_PATH_DELIMITER)


def get_nested_value(field_path, data):
    """Get a (potentially nested) value from a dictionary.

    If the data is nested, for example:

    .. code-block:: python

       >>> data
       {
           'top1': {
               'middle2': {
                   'bottom3': 20,
                   'bottom4': 22,
               },
               'middle5': True,
           },
           'top6': b'\x00\x01 foo',
       }

    a **field path** can be used to access the nested data. For
    example:

    .. code-block:: python

       >>> get_nested_value('top1', data)
       {
           'middle2': {
               'bottom3': 20,
               'bottom4': 22,
           },
           'middle5': True,
       }
       >>> get_nested_value('top1.middle2', data)
       {
           'bottom3': 20,
           'bottom4': 22,
       }
       >>> get_nested_value('top1.middle2.bottom3', data)
       20

    See :meth:`~.firestore_v1beta1.client.Client.field_path` for
    more information on **field paths**.

    Args:
        field_path (str): A field path (``.``-delimited list of
            field names).
        data (Dict[str, Any]): The (possibly nested) data.

    Returns:
        Any: (A copy of) the value stored for the ``field_path``.

    Raises:
        KeyError: If the ``field_path`` does not match nested data.
    """
    field_names = parse_field_path(field_path)

    nested_data = data
    for index, field_name in enumerate(field_names):
        if isinstance(nested_data, collections.Mapping):
            if field_name in nested_data:
                nested_data = nested_data[field_name]
            else:
                if index == 0:
                    msg = FIELD_PATH_MISSING_TOP.format(field_name)
                    raise KeyError(msg)
                else:
                    partial = get_field_path(field_names[:index])
                    msg = FIELD_PATH_MISSING_KEY.format(field_name, partial)
                    raise KeyError(msg)
        else:
            partial = get_field_path(field_names[:index])
            msg = FIELD_PATH_WRONG_TYPE.format(partial, field_name)
            raise KeyError(msg)

    return nested_data


def get_doc_id(document_pb, expected_prefix):
    """Parse a document ID from a document protobuf.

    Args:
        document_pb (google.cloud.proto.firestore.v1beta1.\
            document_pb2.Document): A protobuf for a document that
            was created in a ``CreateDocument`` RPC.
        expected_prefix (str): The expected collection prefix for the
            fully-qualified document name.

    Returns:
        str: The document ID from the protobuf.

    Raises:
        ValueError: If the name does not begin with the prefix.
    """
    prefix, document_id = document_pb.name.rsplit(
        DOCUMENT_PATH_DELIMITER, 1)
    if prefix != expected_prefix:
        raise ValueError(
            'Unexpected document name', document_pb.name,
            'Expected to begin with', expected_prefix)

    return document_id


def remove_server_timestamp(document_data):
    """Remove all server timestamp sentinel values from data.

    If the data is nested, for example:

    .. code-block:: python

       >>> data
       {
           'top1': {
               'bottom2': firestore.SERVER_TIMESTAMP,
               'bottom3': 1.5,
           },
           'top4': firestore.SERVER_TIMESTAMP,
           'top5': 200,
       }

    then this method will split out the "actual" data from
    the server timestamp fields:

    .. code-block:: python

       >>> field_paths, actual_data = remove_server_timestamp(data)
       >>> field_paths
       ['top1.bottom2', 'top4']
       >>> actual_data
       {
           'top1': {
               'bottom3': 1.5,
           },
           'top5': 200,
       }

    Args:
        document_data (dict): Property names and values to use for
            sending a change to a document.

    Returns:
        Tuple[List[str, ...], Dict[str, Any]]: A two-tuple of

        * A list of all field paths that use the server timestamp sentinel
        * The remaining keys in ``document_data`` after removing the
          server timestamp sentinels
    """
    field_paths = []
    actual_data = {}
    for field_name, value in six.iteritems(document_data):
        if isinstance(value, dict):
            sub_field_paths, sub_data = remove_server_timestamp(value)
            field_paths.extend(
                get_field_path([field_name, sub_path])
                for sub_path in sub_field_paths
            )
            if sub_data:
                # Only add a key to ``actual_data`` if there is data.
                actual_data[field_name] = sub_data
        elif value is constants.SERVER_TIMESTAMP:
            field_paths.append(field_name)
        else:
            actual_data[field_name] = value

    if field_paths:
        return field_paths, actual_data
    else:
        return field_paths, document_data


def get_transform_pb(document_path, transform_paths):
    """Get a ``Write`` protobuf for performing a document transform.

    The only document transform is the ``set_to_server_value`` transform,
    which sets the field to the current time on the server.

    Args:
        document_path (str): A fully-qualified document path.
        transform_paths (List[str]): A list of field paths to transform.

    Returns:
        google.cloud.firestore_v1beta1.types.Write: A
        ``Write`` protobuf instance for a document transform.
    """
    return write_pb2.Write(
        transform=write_pb2.DocumentTransform(
            document=document_path,
            field_transforms=[
                write_pb2.DocumentTransform.FieldTransform(
                    field_path=field_path,
                    set_to_server_value=REQUEST_TIME_ENUM,
                )
                for field_path in transform_paths
            ],
        ),
    )


def pbs_for_set(document_path, document_data, option):
    """Make ``Write`` protobufs for ``set()`` methods.

    Args:
        document_path (str): A fully-qualified document path.
        document_data (dict): Property names and values to use for
            replacing a document.
        option (optional[~.firestore_v1beta1.client.WriteOption]): A
           write option to make assertions / preconditions on the server
           state of the document before applying changes.

    Returns:
        List[google.cloud.firestore_v1beta1.types.Write]: One
        or two ``Write`` protobuf instances for ``set()``.
    """
    transform_paths, actual_data = remove_server_timestamp(document_data)

    update_pb = write_pb2.Write(
        update=document_pb2.Document(
            name=document_path,
            fields=encode_dict(actual_data),
        ),
    )
    if option is not None:
        option.modify_write(update_pb)

    write_pbs = [update_pb]
    if transform_paths:
        # NOTE: We **explicitly** don't set any write option on
        #       the ``transform_pb``.
        transform_pb = get_transform_pb(document_path, transform_paths)
        write_pbs.append(transform_pb)

    return write_pbs


def pbs_for_update(client, document_path, field_updates, option):
    """Make ``Write`` protobufs for ``update()`` methods.

    Args:
        client (~.firestore_v1beta1.client.Client): A client that has
            a write option factory.
        document_path (str): A fully-qualified document path.
        field_updates (dict): Field names or paths to update and values
            to update with.
        option (optional[~.firestore_v1beta1.client.WriteOption]): A
           write option to make assertions / preconditions on the server
           state of the document before applying changes.

    Returns:
        List[google.cloud.firestore_v1beta1.types.Write]: One
        or two ``Write`` protobuf instances for ``update()``.
    """
    if option is None:
        # Default uses ``exists=True``.
        option = client.write_option(create_if_missing=False)

    transform_paths, actual_updates = remove_server_timestamp(field_updates)
    update_values, field_paths = FieldPathHelper.to_field_paths(actual_updates)

    update_pb = write_pb2.Write(
        update=document_pb2.Document(
            name=document_path,
            fields=encode_dict(update_values),
        ),
        update_mask=common_pb2.DocumentMask(field_paths=field_paths),
    )
    # Due to the default, we don't have to check if ``None``.
    option.modify_write(update_pb)
    write_pbs = [update_pb]

    if transform_paths:
        # NOTE: We **explicitly** don't set any write option on
        #       the ``transform_pb``.
        transform_pb = get_transform_pb(document_path, transform_paths)
        write_pbs.append(transform_pb)

    return write_pbs


def pb_for_delete(document_path, option):
    """Make a ``Write`` protobuf for ``delete()`` methods.

    Args:
        document_path (str): A fully-qualified document path.
        option (optional[~.firestore_v1beta1.client.WriteOption]): A
           write option to make assertions / preconditions on the server
           state of the document before applying changes.

    Returns:
        google.cloud.firestore_v1beta1.types.Write: A
        ``Write`` protobuf instance for the ``delete()``.
    """
    write_pb = write_pb2.Write(delete=document_path)
    if option is not None:
        option.modify_write(write_pb, no_create_msg=NO_CREATE_ON_DELETE)

    return write_pb


def get_transaction_id(transaction, read_operation=True):
    """Get the transaction ID from a ``Transaction`` object.

    Args:
        transaction (Optional[~.firestore_v1beta1.transaction.\
            Transaction]): An existing transaction that this query will
            run in.
        read_operation (Optional[bool]): Indicates if the transaction ID
            will be used in a read operation. Defaults to :data:`True`.

    Returns:
        Optional[bytes]: The ID of the transaction, or :data:`None` if the
        ``transaction`` is :data:`None`.

    Raises:
        ValueError: If the ``transaction`` is not in progress (only if
            ``transaction`` is not :data:`None`).
        ReadAfterWriteError: If the ``transaction`` has writes stored on
            it and ``read_operation`` is :data:`True`.
    """
    if transaction is None:
        return None
    else:
        if not transaction.in_progress:
            raise ValueError(INACTIVE_TXN)
        if read_operation and len(transaction._write_pbs) > 0:
            raise ReadAfterWriteError(READ_AFTER_WRITE_ERROR)
        return transaction.id


@contextlib.contextmanager
def remap_gax_error_on_commit():
    """Remap GAX exceptions that happen in context.

    Remaps gRPC exceptions that can occur during the ``Comitt`` RPC to
    the classes defined in :mod:`~google.cloud.exceptions`.
    """
    try:
        yield
    except google.gax.errors.GaxError as exc:
        status_code = google.gax.grpc.exc_to_code(exc.cause)
        error_class = _GRPC_ERROR_MAPPING.get(status_code)
        if error_class is None:
            raise
        else:
            new_exc = error_class(exc.cause.details())
            six.reraise(error_class, new_exc, sys.exc_info()[2])


def options_with_prefix(database_string):
    """Create GAPIC options w / cloud resource prefix.

    Args:
        database_string (str): A database string of the form
            ``projects/{project_id}/databases/{database_id}``.

    Returns:
        ~google.gax.CallOptions: GAPIC call options with supplied prefix.
    """
    return google.gax.CallOptions(
        metadata=[('google-cloud-resource-prefix', database_string)],
    )
