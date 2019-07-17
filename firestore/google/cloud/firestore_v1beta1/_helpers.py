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

import datetime

from google.protobuf import struct_pb2
from google.type import latlng_pb2
import grpc
import six

from google.cloud import exceptions
from google.cloud._helpers import _datetime_to_pb_timestamp
from google.api_core.datetime_helpers import DatetimeWithNanoseconds
from google.cloud.firestore_v1beta1 import transforms
from google.cloud.firestore_v1beta1 import types
from google.cloud.firestore_v1beta1.field_path import FieldPath
from google.cloud.firestore_v1beta1.field_path import parse_field_path
from google.cloud.firestore_v1beta1.gapic import enums
from google.cloud.firestore_v1beta1.proto import common_pb2
from google.cloud.firestore_v1beta1.proto import document_pb2
from google.cloud.firestore_v1beta1.proto import write_pb2


BAD_PATH_TEMPLATE = "A path element must be a string. Received {}, which is a {}."
DOCUMENT_PATH_DELIMITER = "/"
INACTIVE_TXN = "Transaction not in progress, cannot be used in API requests."
READ_AFTER_WRITE_ERROR = "Attempted read after write in a transaction."
BAD_REFERENCE_ERROR = (
    "Reference value {!r} in unexpected format, expected to be of the form "
    "``projects/{{project}}/databases/{{database}}/"
    "documents/{{document_path}}``."
)
WRONG_APP_REFERENCE = (
    "Document {!r} does not correspond to the same database " "({!r}) as the client."
)
REQUEST_TIME_ENUM = enums.DocumentTransform.FieldTransform.ServerValue.REQUEST_TIME
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
        return latlng_pb2.LatLng(latitude=self.latitude, longitude=self.longitude)

    def __eq__(self, other):
        """Compare two geo points for equality.

        Returns:
            Union[bool, NotImplemented]: :data:`True` if the points compare
            equal, else :data:`False`. (Or :data:`NotImplemented` if
            ``other`` is not a geo point.)
        """
        if not isinstance(other, GeoPoint):
            return NotImplemented

        return self.latitude == other.latitude and self.longitude == other.longitude

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
        raise ValueError("Document or collection path cannot be empty")

    if is_collection:
        if num_elements % 2 == 0:
            raise ValueError("A collection must have an odd number of path elements")
    else:
        if num_elements % 2 == 1:
            raise ValueError("A document must have an even number of path elements")

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

    if isinstance(value, DatetimeWithNanoseconds):
        return document_pb2.Value(timestamp_value=value.timestamp_pb())

    if isinstance(value, datetime.datetime):
        return document_pb2.Value(timestamp_value=_datetime_to_pb_timestamp(value))

    if isinstance(value, six.text_type):
        return document_pb2.Value(string_value=value)

    if isinstance(value, six.binary_type):
        return document_pb2.Value(bytes_value=value)

    # NOTE: We avoid doing an isinstance() check for a Document
    #       here to avoid import cycles.
    document_path = getattr(value, "_document_path", None)
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
        "Cannot convert to a Firestore Value", value, "Invalid type", type(value)
    )


def encode_dict(values_dict):
    """Encode a dictionary into protobuf ``Value``-s.

    Args:
        values_dict (dict): The dictionary to encode as protobuf fields.

    Returns:
        Dict[str, ~google.cloud.firestore_v1beta1.types.Value]: A
        dictionary of string keys and ``Value`` protobufs as dictionary
        values.
    """
    return {key: encode_value(value) for key, value in six.iteritems(values_dict)}


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
        msg = WRONG_APP_REFERENCE.format(reference_value, client._database_string)
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
    value_type = value.WhichOneof("value_type")

    if value_type == "null_value":
        return None
    elif value_type == "boolean_value":
        return value.boolean_value
    elif value_type == "integer_value":
        return value.integer_value
    elif value_type == "double_value":
        return value.double_value
    elif value_type == "timestamp_value":
        return DatetimeWithNanoseconds.from_timestamp_pb(value.timestamp_value)
    elif value_type == "string_value":
        return value.string_value
    elif value_type == "bytes_value":
        return value.bytes_value
    elif value_type == "reference_value":
        return reference_value_to_document(value.reference_value, client)
    elif value_type == "geo_point_value":
        return GeoPoint(value.geo_point_value.latitude, value.geo_point_value.longitude)
    elif value_type == "array_value":
        return [decode_value(element, client) for element in value.array_value.values]
    elif value_type == "map_value":
        return decode_dict(value.map_value.fields, client)
    else:
        raise ValueError("Unknown ``value_type``", value_type)


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
        key: decode_value(value, client) for key, value in six.iteritems(value_fields)
    }


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
    prefix, document_id = document_pb.name.rsplit(DOCUMENT_PATH_DELIMITER, 1)
    if prefix != expected_prefix:
        raise ValueError(
            "Unexpected document name",
            document_pb.name,
            "Expected to begin with",
            expected_prefix,
        )

    return document_id


_EmptyDict = transforms.Sentinel("Marker for an empty dict value")


def extract_fields(document_data, prefix_path, expand_dots=False):
    """Do depth-first walk of tree, yielding field_path, value"""
    if not document_data:
        yield prefix_path, _EmptyDict
    else:
        for key, value in sorted(six.iteritems(document_data)):

            if expand_dots:
                sub_key = FieldPath.from_string(key)
            else:
                sub_key = FieldPath(key)

            field_path = FieldPath(*(prefix_path.parts + sub_key.parts))

            if isinstance(value, dict):
                for s_path, s_value in extract_fields(value, field_path):
                    yield s_path, s_value
            else:
                yield field_path, value


def set_field_value(document_data, field_path, value):
    """Set a value into a document for a field_path"""
    current = document_data
    for element in field_path.parts[:-1]:
        current = current.setdefault(element, {})
    if value is _EmptyDict:
        value = {}
    current[field_path.parts[-1]] = value


def get_field_value(document_data, field_path):
    if not field_path.parts:
        raise ValueError("Empty path")

    current = document_data
    for element in field_path.parts[:-1]:
        current = current[element]
    return current[field_path.parts[-1]]


class DocumentExtractor(object):
    """ Break document data up into actual data and transforms.

    Handle special values such as ``DELETE_FIELD``, ``SERVER_TIMESTAMP``.

    Args:
        document_data (dict):
            Property names and values to use for sending a change to
            a document.
    """

    def __init__(self, document_data):
        self.document_data = document_data
        self.field_paths = []
        self.deleted_fields = []
        self.server_timestamps = []
        self.array_removes = {}
        self.array_unions = {}
        self.set_fields = {}
        self.empty_document = False

        prefix_path = FieldPath()
        iterator = self._get_document_iterator(prefix_path)

        for field_path, value in iterator:

            if field_path == prefix_path and value is _EmptyDict:
                self.empty_document = True

            elif value is transforms.DELETE_FIELD:
                self.deleted_fields.append(field_path)

            elif value is transforms.SERVER_TIMESTAMP:
                self.server_timestamps.append(field_path)

            elif isinstance(value, transforms.ArrayRemove):
                self.array_removes[field_path] = value.values

            elif isinstance(value, transforms.ArrayUnion):
                self.array_unions[field_path] = value.values

            else:
                self.field_paths.append(field_path)
                set_field_value(self.set_fields, field_path, value)

    def _get_document_iterator(self, prefix_path):
        return extract_fields(self.document_data, prefix_path)

    @property
    def has_transforms(self):
        return bool(self.server_timestamps or self.array_removes or self.array_unions)

    @property
    def transform_paths(self):
        return sorted(
            self.server_timestamps + list(self.array_removes) + list(self.array_unions)
        )

    def _get_update_mask(self, allow_empty_mask=False):
        return None

    def get_update_pb(self, document_path, exists=None, allow_empty_mask=False):

        if exists is not None:
            current_document = common_pb2.Precondition(exists=exists)
        else:
            current_document = None

        update_pb = write_pb2.Write(
            update=document_pb2.Document(
                name=document_path, fields=encode_dict(self.set_fields)
            ),
            update_mask=self._get_update_mask(allow_empty_mask),
            current_document=current_document,
        )

        return update_pb

    def get_transform_pb(self, document_path, exists=None):
        def make_array_value(values):
            value_list = [encode_value(element) for element in values]
            return document_pb2.ArrayValue(values=value_list)

        path_field_transforms = (
            [
                (
                    path,
                    write_pb2.DocumentTransform.FieldTransform(
                        field_path=path.to_api_repr(),
                        set_to_server_value=REQUEST_TIME_ENUM,
                    ),
                )
                for path in self.server_timestamps
            ]
            + [
                (
                    path,
                    write_pb2.DocumentTransform.FieldTransform(
                        field_path=path.to_api_repr(),
                        remove_all_from_array=make_array_value(values),
                    ),
                )
                for path, values in self.array_removes.items()
            ]
            + [
                (
                    path,
                    write_pb2.DocumentTransform.FieldTransform(
                        field_path=path.to_api_repr(),
                        append_missing_elements=make_array_value(values),
                    ),
                )
                for path, values in self.array_unions.items()
            ]
        )
        field_transforms = [
            transform for path, transform in sorted(path_field_transforms)
        ]
        transform_pb = write_pb2.Write(
            transform=write_pb2.DocumentTransform(
                document=document_path, field_transforms=field_transforms
            )
        )
        if exists is not None:
            transform_pb.current_document.CopyFrom(
                common_pb2.Precondition(exists=exists)
            )

        return transform_pb


def pbs_for_create(document_path, document_data):
    """Make ``Write`` protobufs for ``create()`` methods.

    Args:
        document_path (str): A fully-qualified document path.
        document_data (dict): Property names and values to use for
            creating a document.

    Returns:
        List[google.cloud.firestore_v1beta1.types.Write]: One or two
        ``Write`` protobuf instances for ``create()``.
    """
    extractor = DocumentExtractor(document_data)

    if extractor.deleted_fields:
        raise ValueError("Cannot apply DELETE_FIELD in a create request.")

    write_pbs = []

    # Conformance tests require skipping the 'update_pb' if the document
    # contains only transforms.
    if extractor.empty_document or extractor.set_fields:
        write_pbs.append(extractor.get_update_pb(document_path, exists=False))

    if extractor.has_transforms:
        exists = None if write_pbs else False
        transform_pb = extractor.get_transform_pb(document_path, exists)
        write_pbs.append(transform_pb)

    return write_pbs


def pbs_for_set_no_merge(document_path, document_data):
    """Make ``Write`` protobufs for ``set()`` methods.

    Args:
        document_path (str): A fully-qualified document path.
        document_data (dict): Property names and values to use for
            replacing a document.

    Returns:
        List[google.cloud.firestore_v1beta1.types.Write]: One
        or two ``Write`` protobuf instances for ``set()``.
    """
    extractor = DocumentExtractor(document_data)

    if extractor.deleted_fields:
        raise ValueError(
            "Cannot apply DELETE_FIELD in a set request without "
            "specifying 'merge=True' or 'merge=[field_paths]'."
        )

    # Conformance tests require send the 'update_pb' even if the document
    # contains only transforms.
    write_pbs = [extractor.get_update_pb(document_path)]

    if extractor.has_transforms:
        transform_pb = extractor.get_transform_pb(document_path)
        write_pbs.append(transform_pb)

    return write_pbs


class DocumentExtractorForMerge(DocumentExtractor):
    """ Break document data up into actual data and transforms.
    """

    def __init__(self, document_data):
        super(DocumentExtractorForMerge, self).__init__(document_data)
        self.data_merge = []
        self.transform_merge = []
        self.merge = []

    @property
    def has_updates(self):
        # for whatever reason, the conformance tests want to see the parent
        # of nested transform paths in the update mask
        # (see set-st-merge-nonleaf-alone.textproto)
        update_paths = set(self.data_merge)

        for transform_path in self.transform_paths:
            if len(transform_path.parts) > 1:
                parent_fp = FieldPath(*transform_path.parts[:-1])
                update_paths.add(parent_fp)

        return bool(update_paths)

    def _apply_merge_all(self):
        self.data_merge = sorted(self.field_paths + self.deleted_fields)
        # TODO: other transforms
        self.transform_merge = self.transform_paths
        self.merge = sorted(self.data_merge + self.transform_paths)

    def _construct_merge_paths(self, merge):
        for merge_field in merge:
            if isinstance(merge_field, FieldPath):
                yield merge_field
            else:
                yield FieldPath(*parse_field_path(merge_field))

    def _normalize_merge_paths(self, merge):
        merge_paths = sorted(self._construct_merge_paths(merge))

        # Raise if any merge path is a parent of another.  Leverage sorting
        # to avoid quadratic behavior.
        for index in range(len(merge_paths) - 1):
            lhs, rhs = merge_paths[index], merge_paths[index + 1]
            if lhs.eq_or_parent(rhs):
                raise ValueError("Merge paths overlap: {}, {}".format(lhs, rhs))

        for merge_path in merge_paths:
            if merge_path in self.deleted_fields:
                continue
            try:
                get_field_value(self.document_data, merge_path)
            except KeyError:
                raise ValueError("Invalid merge path: {}".format(merge_path))

        return merge_paths

    def _apply_merge_paths(self, merge):

        if self.empty_document:
            raise ValueError("Cannot merge specific fields with empty document.")

        merge_paths = self._normalize_merge_paths(merge)

        del self.data_merge[:]
        del self.transform_merge[:]
        self.merge = merge_paths

        for merge_path in merge_paths:

            if merge_path in self.transform_paths:
                self.transform_merge.append(merge_path)

            for field_path in self.field_paths:
                if merge_path.eq_or_parent(field_path):
                    self.data_merge.append(field_path)

        # Clear out data for fields not merged.
        merged_set_fields = {}
        for field_path in self.data_merge:
            value = get_field_value(self.document_data, field_path)
            set_field_value(merged_set_fields, field_path, value)
        self.set_fields = merged_set_fields

        unmerged_deleted_fields = [
            field_path
            for field_path in self.deleted_fields
            if field_path not in self.merge
        ]
        if unmerged_deleted_fields:
            raise ValueError(
                "Cannot delete unmerged fields: {}".format(unmerged_deleted_fields)
            )
        self.data_merge = sorted(self.data_merge + self.deleted_fields)

        # Keep only transforms which are within merge.
        merged_transform_paths = set()
        for merge_path in self.merge:
            tranform_merge_paths = [
                transform_path
                for transform_path in self.transform_paths
                if merge_path.eq_or_parent(transform_path)
            ]
            merged_transform_paths.update(tranform_merge_paths)

        self.server_timestamps = [
            path for path in self.server_timestamps if path in merged_transform_paths
        ]

        self.array_removes = {
            path: values
            for path, values in self.array_removes.items()
            if path in merged_transform_paths
        }

        self.array_unions = {
            path: values
            for path, values in self.array_unions.items()
            if path in merged_transform_paths
        }

    def apply_merge(self, merge):
        if merge is True:  # merge all fields
            self._apply_merge_all()
        else:
            self._apply_merge_paths(merge)

    def _get_update_mask(self, allow_empty_mask=False):
        # Mask uses dotted / quoted paths.
        mask_paths = [
            field_path.to_api_repr()
            for field_path in self.merge
            if field_path not in self.transform_merge
        ]

        if mask_paths or allow_empty_mask:
            return common_pb2.DocumentMask(field_paths=mask_paths)


def pbs_for_set_with_merge(document_path, document_data, merge):
    """Make ``Write`` protobufs for ``set()`` methods.

    Args:
        document_path (str): A fully-qualified document path.
        document_data (dict): Property names and values to use for
            replacing a document.
        merge (Optional[bool] or Optional[List<apispec>]):
            If True, merge all fields; else, merge only the named fields.

    Returns:
        List[google.cloud.firestore_v1beta1.types.Write]: One
        or two ``Write`` protobuf instances for ``set()``.
    """
    extractor = DocumentExtractorForMerge(document_data)
    extractor.apply_merge(merge)

    merge_empty = not document_data

    write_pbs = []

    if extractor.has_updates or merge_empty:
        write_pbs.append(
            extractor.get_update_pb(document_path, allow_empty_mask=merge_empty)
        )

    if extractor.transform_paths:
        transform_pb = extractor.get_transform_pb(document_path)
        write_pbs.append(transform_pb)

    return write_pbs


class DocumentExtractorForUpdate(DocumentExtractor):
    """ Break document data up into actual data and transforms.
    """

    def __init__(self, document_data):
        super(DocumentExtractorForUpdate, self).__init__(document_data)
        self.top_level_paths = sorted(
            [FieldPath.from_string(key) for key in document_data]
        )
        tops = set(self.top_level_paths)
        for top_level_path in self.top_level_paths:
            for ancestor in top_level_path.lineage():
                if ancestor in tops:
                    raise ValueError(
                        "Conflicting field path: {}, {}".format(
                            top_level_path, ancestor
                        )
                    )

        for field_path in self.deleted_fields:
            if field_path not in tops:
                raise ValueError(
                    "Cannot update with nest delete: {}".format(field_path)
                )

    def _get_document_iterator(self, prefix_path):
        return extract_fields(self.document_data, prefix_path, expand_dots=True)

    def _get_update_mask(self, allow_empty_mask=False):
        mask_paths = []
        for field_path in self.top_level_paths:
            if field_path not in self.transform_paths:
                mask_paths.append(field_path.to_api_repr())

        return common_pb2.DocumentMask(field_paths=mask_paths)


def pbs_for_update(document_path, field_updates, option):
    """Make ``Write`` protobufs for ``update()`` methods.

    Args:
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
    extractor = DocumentExtractorForUpdate(field_updates)

    if extractor.empty_document:
        raise ValueError("Cannot update with an empty document.")

    if option is None:  # Default is to use ``exists=True``.
        option = ExistsOption(exists=True)

    write_pbs = []

    if extractor.field_paths or extractor.deleted_fields:
        update_pb = extractor.get_update_pb(document_path)
        option.modify_write(update_pb)
        write_pbs.append(update_pb)

    if extractor.has_transforms:
        transform_pb = extractor.get_transform_pb(document_path)
        if not write_pbs:
            # NOTE: set the write option on the ``transform_pb`` only if there
            #       is no ``update_pb``
            option.modify_write(transform_pb)
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
        option.modify_write(write_pb)

    return write_pb


class ReadAfterWriteError(Exception):
    """Raised when a read is attempted after a write.

    Raised by "read" methods that use transactions.
    """


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


def metadata_with_prefix(prefix, **kw):
    """Create RPC metadata containing a prefix.

    Args:
        prefix (str): appropriate resource path.

    Returns:
        List[Tuple[str, str]]: RPC metadata with supplied prefix
    """
    return [("google-cloud-resource-prefix", prefix)]


class WriteOption(object):
    """Option used to assert a condition on a write operation."""

    def modify_write(self, write_pb, no_create_msg=None):
        """Modify a ``Write`` protobuf based on the state of this write option.

        This is a virtual method intended to be implemented by subclasses.

        Args:
            write_pb (google.cloud.firestore_v1beta1.types.Write): A
                ``Write`` protobuf instance to be modified with a precondition
                determined by the state of this option.
            no_create_msg (Optional[str]): A message to use to indicate that
                a create operation is not allowed.

        Raises:
            NotImplementedError: Always, this method is virtual.
        """
        raise NotImplementedError


class LastUpdateOption(WriteOption):
    """Option used to assert a "last update" condition on a write operation.

    This will typically be created by
    :meth:`~google.cloud.firestore_v1beta1.client.Client.write_option`.

    Args:
        last_update_time (google.protobuf.timestamp_pb2.Timestamp): A
            timestamp. When set, the target document must exist and have
            been last updated at that time. Protobuf ``update_time`` timestamps
            are typically returned from methods that perform write operations
            as part of a "write result" protobuf or directly.
    """

    def __init__(self, last_update_time):
        self._last_update_time = last_update_time

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._last_update_time == other._last_update_time

    def modify_write(self, write_pb, **unused_kwargs):
        """Modify a ``Write`` protobuf based on the state of this write option.

        The ``last_update_time`` is added to ``write_pb`` as an "update time"
        precondition. When set, the target document must exist and have been
        last updated at that time.

        Args:
            write_pb (google.cloud.firestore_v1beta1.types.Write): A
                ``Write`` protobuf instance to be modified with a precondition
                determined by the state of this option.
            unused_kwargs (Dict[str, Any]): Keyword arguments accepted by
                other subclasses that are unused here.
        """
        current_doc = types.Precondition(update_time=self._last_update_time)
        write_pb.current_document.CopyFrom(current_doc)


class ExistsOption(WriteOption):
    """Option used to assert existence on a write operation.

    This will typically be created by
    :meth:`~google.cloud.firestore_v1beta1.client.Client.write_option`.

    Args:
        exists (bool): Indicates if the document being modified
            should already exist.
    """

    def __init__(self, exists):
        self._exists = exists

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._exists == other._exists

    def modify_write(self, write_pb, **unused_kwargs):
        """Modify a ``Write`` protobuf based on the state of this write option.

        If:

        * ``exists=True``, adds a precondition that requires existence
        * ``exists=False``, adds a precondition that requires non-existence

        Args:
            write_pb (google.cloud.firestore_v1beta1.types.Write): A
                ``Write`` protobuf instance to be modified with a precondition
                determined by the state of this option.
            unused_kwargs (Dict[str, Any]): Keyword arguments accepted by
                other subclasses that are unused here.
        """
        current_doc = types.Precondition(exists=self._exists)
        write_pb.current_document.CopyFrom(current_doc)
