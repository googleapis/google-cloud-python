# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
#
from __future__ import annotations

from typing import MutableMapping, MutableSequence

from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.storage.control.v2",
    manifest={
        "PendingRenameInfo",
        "Folder",
        "GetFolderRequest",
        "CreateFolderRequest",
        "DeleteFolderRequest",
        "ListFoldersRequest",
        "ListFoldersResponse",
        "RenameFolderRequest",
        "CommonLongRunningOperationMetadata",
        "RenameFolderMetadata",
        "StorageLayout",
        "GetStorageLayoutRequest",
        "ManagedFolder",
        "GetManagedFolderRequest",
        "CreateManagedFolderRequest",
        "DeleteManagedFolderRequest",
        "ListManagedFoldersRequest",
        "ListManagedFoldersResponse",
    },
)


class PendingRenameInfo(proto.Message):
    r"""Contains information about a pending rename operation.

    Attributes:
        operation (str):
            Output only. The name of the rename
            operation.
    """

    operation: str = proto.Field(
        proto.STRING,
        number=1,
    )


class Folder(proto.Message):
    r"""A folder resource. This resource can only exist in a
    hierarchical namespace enabled bucket.

    Attributes:
        name (str):
            Identifier. The name of this folder. Format:
            ``projects/{project}/buckets/{bucket}/folders/{folder}``
        metageneration (int):
            Output only. The version of the metadata for
            this folder. Used for preconditions and for
            detecting changes in metadata.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The creation time of the folder.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The modification time of the
            folder.
        pending_rename_info (google.cloud.storage_control_v2.types.PendingRenameInfo):
            Output only. Only present if the folder is
            part of an ongoing RenameFolder operation.
            Contains information which can be used to query
            the operation status. The presence of this field
            also indicates all write operations are blocked
            for this folder, including folder, managed
            folder, and object operations.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    metageneration: int = proto.Field(
        proto.INT64,
        number=3,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )
    pending_rename_info: "PendingRenameInfo" = proto.Field(
        proto.MESSAGE,
        number=7,
        message="PendingRenameInfo",
    )


class GetFolderRequest(proto.Message):
    r"""Request message for GetFolder. This operation is only
    applicable to a hierarchical namespace enabled bucket.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Required. Name of the folder. Format:
            ``projects/{project}/buckets/{bucket}/folders/{folder}``
        if_metageneration_match (int):
            Makes the operation only succeed conditional
            on whether the folder's current metageneration
            matches the given value.

            This field is a member of `oneof`_ ``_if_metageneration_match``.
        if_metageneration_not_match (int):
            Makes the operation only succeed conditional
            on whether the folder's current metageneration
            does not match the given value.

            This field is a member of `oneof`_ ``_if_metageneration_not_match``.
        request_id (str):
            Optional. A unique identifier for this
            request. UUID is the recommended format, but
            other formats are still accepted.
    """

    name: str = proto.Field(
        proto.STRING,
        number=6,
    )
    if_metageneration_match: int = proto.Field(
        proto.INT64,
        number=3,
        optional=True,
    )
    if_metageneration_not_match: int = proto.Field(
        proto.INT64,
        number=4,
        optional=True,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=5,
    )


class CreateFolderRequest(proto.Message):
    r"""Request message for CreateFolder. This operation is only
    applicable to a hierarchical namespace enabled bucket.

    Attributes:
        parent (str):
            Required. Name of the bucket in which the
            folder will reside. The bucket must be a
            hierarchical namespace enabled bucket.
        folder (google.cloud.storage_control_v2.types.Folder):
            Required. Properties of the new folder being created. The
            bucket and name of the folder are specified in the parent
            and folder_id fields, respectively. Populating those fields
            in ``folder`` will result in an error.
        folder_id (str):
            Required. The full name of a folder, including all its
            parent folders. Folders use single '/' characters as a
            delimiter. The folder_id must end with a slash. For example,
            the folder_id of "books/biographies/" would create a new
            "biographies/" folder under the "books/" folder.
        recursive (bool):
            Optional. If true, parent folder doesn't have
            to be present and all missing ancestor folders
            will be created atomically.
        request_id (str):
            Optional. A unique identifier for this
            request. UUID is the recommended format, but
            other formats are still accepted.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    folder: "Folder" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Folder",
    )
    folder_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    recursive: bool = proto.Field(
        proto.BOOL,
        number=4,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=5,
    )


class DeleteFolderRequest(proto.Message):
    r"""Request message for DeleteFolder. This operation is only
    applicable to a hierarchical namespace enabled bucket.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Required. Name of the folder. Format:
            ``projects/{project}/buckets/{bucket}/folders/{folder}``
        if_metageneration_match (int):
            Makes the operation only succeed conditional
            on whether the folder's current metageneration
            matches the given value.

            This field is a member of `oneof`_ ``_if_metageneration_match``.
        if_metageneration_not_match (int):
            Makes the operation only succeed conditional
            on whether the folder's current metageneration
            does not match the given value.

            This field is a member of `oneof`_ ``_if_metageneration_not_match``.
        request_id (str):
            Optional. A unique identifier for this
            request. UUID is the recommended format, but
            other formats are still accepted.
    """

    name: str = proto.Field(
        proto.STRING,
        number=6,
    )
    if_metageneration_match: int = proto.Field(
        proto.INT64,
        number=3,
        optional=True,
    )
    if_metageneration_not_match: int = proto.Field(
        proto.INT64,
        number=4,
        optional=True,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=5,
    )


class ListFoldersRequest(proto.Message):
    r"""Request message for ListFolders. This operation is only
    applicable to a hierarchical namespace enabled bucket.

    Attributes:
        parent (str):
            Required. Name of the bucket in which to look
            for folders. The bucket must be a hierarchical
            namespace enabled bucket.
        page_size (int):
            Optional. Maximum number of folders to return
            in a single response. The service will use this
            parameter or 1,000 items, whichever is smaller.
        page_token (str):
            Optional. A previously-returned page token
            representing part of the larger set of results
            to view.
        prefix (str):
            Optional. Filter results to folders whose
            names begin with this prefix. If set, the value
            must either be an empty string or end with a
            '/'.
        delimiter (str):
            Optional. If set, returns results in a
            directory-like mode. The results will only
            include folders that either exactly match the
            above prefix, or are one level below the prefix.
            The only supported value is '/'.
        lexicographic_start (str):
            Optional. Filter results to folders whose names are
            lexicographically equal to or after lexicographic_start. If
            lexicographic_end is also set, the folders listed have names
            between lexicographic_start (inclusive) and
            lexicographic_end (exclusive).
        lexicographic_end (str):
            Optional. Filter results to folders whose names are
            lexicographically before lexicographic_end. If
            lexicographic_start is also set, the folders listed have
            names between lexicographic_start (inclusive) and
            lexicographic_end (exclusive).
        request_id (str):
            Optional. A unique identifier for this
            request. UUID is the recommended format, but
            other formats are still accepted.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )
    prefix: str = proto.Field(
        proto.STRING,
        number=4,
    )
    delimiter: str = proto.Field(
        proto.STRING,
        number=8,
    )
    lexicographic_start: str = proto.Field(
        proto.STRING,
        number=6,
    )
    lexicographic_end: str = proto.Field(
        proto.STRING,
        number=7,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=9,
    )


class ListFoldersResponse(proto.Message):
    r"""Response message for ListFolders.

    Attributes:
        folders (MutableSequence[google.cloud.storage_control_v2.types.Folder]):
            The list of child folders
        next_page_token (str):
            The continuation token, used to page through
            large result sets. Provide this value in a
            subsequent request to return the next page of
            results.
    """

    @property
    def raw_page(self):
        return self

    folders: MutableSequence["Folder"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Folder",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class RenameFolderRequest(proto.Message):
    r"""Request message for RenameFolder. This operation is only
    applicable to a hierarchical namespace enabled bucket.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Required. Name of the source folder being renamed. Format:
            ``projects/{project}/buckets/{bucket}/folders/{folder}``
        destination_folder_id (str):
            Required. The destination folder ID, e.g. ``foo/bar/``.
        if_metageneration_match (int):
            Makes the operation only succeed conditional
            on whether the source folder's current
            metageneration matches the given value.

            This field is a member of `oneof`_ ``_if_metageneration_match``.
        if_metageneration_not_match (int):
            Makes the operation only succeed conditional
            on whether the source folder's current
            metageneration does not match the given value.

            This field is a member of `oneof`_ ``_if_metageneration_not_match``.
        request_id (str):
            Optional. A unique identifier for this request. UUID is the
            recommended format, but other formats are still accepted.
            This request is only idempotent if a ``request_id`` is
            provided.
    """

    name: str = proto.Field(
        proto.STRING,
        number=7,
    )
    destination_folder_id: str = proto.Field(
        proto.STRING,
        number=8,
    )
    if_metageneration_match: int = proto.Field(
        proto.INT64,
        number=4,
        optional=True,
    )
    if_metageneration_not_match: int = proto.Field(
        proto.INT64,
        number=5,
        optional=True,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=6,
    )


class CommonLongRunningOperationMetadata(proto.Message):
    r"""The message contains metadata that is common to all Storage Control
    long-running operations, present in its
    ``google.longrunning.Operation`` messages, and accessible via
    ``metadata.common_metadata``.

    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation was
            created.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation finished
            running.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation was last
            modified.
        type_ (str):
            Output only. The type of operation invoked.
        requested_cancellation (bool):
            Output only. Identifies whether the user has
            requested cancellation.
        progress_percent (int):
            Output only. The estimated progress of the operation in
            percentage [0, 100]. The value -1 means the progress is
            unknown.
    """

    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    end_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    type_: str = proto.Field(
        proto.STRING,
        number=4,
    )
    requested_cancellation: bool = proto.Field(
        proto.BOOL,
        number=5,
    )
    progress_percent: int = proto.Field(
        proto.INT32,
        number=6,
    )


class RenameFolderMetadata(proto.Message):
    r"""Message returned in the metadata field of the Operation
    resource for RenameFolder operations.

    Attributes:
        common_metadata (google.cloud.storage_control_v2.types.CommonLongRunningOperationMetadata):
            Generic metadata for the long running
            operation.
        source_folder_id (str):
            The path of the source folder.
        destination_folder_id (str):
            The path of the destination folder.
    """

    common_metadata: "CommonLongRunningOperationMetadata" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="CommonLongRunningOperationMetadata",
    )
    source_folder_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    destination_folder_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class StorageLayout(proto.Message):
    r"""The storage layout configuration of a bucket.

    Attributes:
        name (str):
            Output only. The name of the StorageLayout resource. Format:
            ``projects/{project}/buckets/{bucket}/storageLayout``
        location (str):
            Output only. The location of the bucket.
        location_type (str):
            Output only. The location type of the bucket
            (region, dual-region, multi-region, etc).
        custom_placement_config (google.cloud.storage_control_v2.types.StorageLayout.CustomPlacementConfig):
            Output only. The data placement configuration
            for custom dual region. If there is no
            configuration, this is not a custom dual region
            bucket.
        hierarchical_namespace (google.cloud.storage_control_v2.types.StorageLayout.HierarchicalNamespace):
            Output only. The bucket's hierarchical
            namespace configuration. If there is no
            configuration, the hierarchical namespace is
            disabled.
    """

    class CustomPlacementConfig(proto.Message):
        r"""Configuration for Custom Dual Regions. It should specify precisely
        two eligible regions within the same Multiregion. More information
        on regions may be found
        [https://cloud.google.com/storage/docs/locations][here].

        Attributes:
            data_locations (MutableSequence[str]):
                List of locations to use for data placement.
        """

        data_locations: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=1,
        )

    class HierarchicalNamespace(proto.Message):
        r"""Configuration for a bucket's hierarchical namespace feature.

        Attributes:
            enabled (bool):
                Enables the hierarchical namespace feature.
        """

        enabled: bool = proto.Field(
            proto.BOOL,
            number=1,
        )

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    location: str = proto.Field(
        proto.STRING,
        number=2,
    )
    location_type: str = proto.Field(
        proto.STRING,
        number=3,
    )
    custom_placement_config: CustomPlacementConfig = proto.Field(
        proto.MESSAGE,
        number=4,
        message=CustomPlacementConfig,
    )
    hierarchical_namespace: HierarchicalNamespace = proto.Field(
        proto.MESSAGE,
        number=5,
        message=HierarchicalNamespace,
    )


class GetStorageLayoutRequest(proto.Message):
    r"""Request message for GetStorageLayout.

    Attributes:
        name (str):
            Required. The name of the StorageLayout resource. Format:
            ``projects/{project}/buckets/{bucket}/storageLayout``
        prefix (str):
            An optional prefix used for permission check.
            It is useful when the caller only has limited
            permissions under a specific prefix.
        request_id (str):
            Optional. A unique identifier for this
            request. UUID is the recommended format, but
            other formats are still accepted.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    prefix: str = proto.Field(
        proto.STRING,
        number=2,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ManagedFolder(proto.Message):
    r"""A managed folder.

    Attributes:
        name (str):
            Identifier. The name of this managed folder. Format:
            ``projects/{project}/buckets/{bucket}/managedFolders/{managedFolder}``
        metageneration (int):
            Output only. The metadata version of this
            managed folder. It increases whenever the
            metadata is updated. Used for preconditions and
            for detecting changes in metadata. Managed
            folders don't have a generation number.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The creation time of the managed
            folder.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The modification time of the
            managed folder.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    metageneration: int = proto.Field(
        proto.INT64,
        number=3,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )


class GetManagedFolderRequest(proto.Message):
    r"""Request message for GetManagedFolder.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Required. Name of the managed folder. Format:
            ``projects/{project}/buckets/{bucket}/managedFolders/{managedFolder}``
        if_metageneration_match (int):
            The operation succeeds conditional on the
            managed folder's current metageneration matching
            the value here specified.

            This field is a member of `oneof`_ ``_if_metageneration_match``.
        if_metageneration_not_match (int):
            The operation succeeds conditional on the
            managed folder's current metageneration NOT
            matching the value here specified.

            This field is a member of `oneof`_ ``_if_metageneration_not_match``.
        request_id (str):
            Optional. A unique identifier for this
            request. UUID is the recommended format, but
            other formats are still accepted.
    """

    name: str = proto.Field(
        proto.STRING,
        number=6,
    )
    if_metageneration_match: int = proto.Field(
        proto.INT64,
        number=3,
        optional=True,
    )
    if_metageneration_not_match: int = proto.Field(
        proto.INT64,
        number=4,
        optional=True,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=5,
    )


class CreateManagedFolderRequest(proto.Message):
    r"""Request message for CreateManagedFolder.

    Attributes:
        parent (str):
            Required. Name of the bucket this managed
            folder belongs to.
        managed_folder (google.cloud.storage_control_v2.types.ManagedFolder):
            Required. Properties of the managed folder being created.
            The bucket and managed folder names are specified in the
            ``parent`` and ``managed_folder_id`` fields. Populating
            these fields in ``managed_folder`` will result in an error.
        managed_folder_id (str):
            Required. The name of the managed folder. It uses a single
            ``/`` as delimiter and leading and trailing ``/`` are
            allowed.
        request_id (str):
            Optional. A unique identifier for this
            request. UUID is the recommended format, but
            other formats are still accepted.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    managed_folder: "ManagedFolder" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="ManagedFolder",
    )
    managed_folder_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=4,
    )


class DeleteManagedFolderRequest(proto.Message):
    r"""DeleteManagedFolder RPC request message.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Required. Name of the managed folder. Format:
            ``projects/{project}/buckets/{bucket}/managedFolders/{managedFolder}``
        if_metageneration_match (int):
            The operation succeeds conditional on the
            managed folder's current metageneration matching
            the value here specified.

            This field is a member of `oneof`_ ``_if_metageneration_match``.
        if_metageneration_not_match (int):
            The operation succeeds conditional on the
            managed folder's current metageneration NOT
            matching the value here specified.

            This field is a member of `oneof`_ ``_if_metageneration_not_match``.
        allow_non_empty (bool):
            Allows deletion of a managed folder even if
            it is not empty. A managed folder is empty if it
            manages no child managed folders or objects.
            Caller must have permission for
            storage.managedFolders.setIamPolicy.
        request_id (str):
            Optional. A unique identifier for this
            request. UUID is the recommended format, but
            other formats are still accepted.
    """

    name: str = proto.Field(
        proto.STRING,
        number=7,
    )
    if_metageneration_match: int = proto.Field(
        proto.INT64,
        number=3,
        optional=True,
    )
    if_metageneration_not_match: int = proto.Field(
        proto.INT64,
        number=4,
        optional=True,
    )
    allow_non_empty: bool = proto.Field(
        proto.BOOL,
        number=5,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=6,
    )


class ListManagedFoldersRequest(proto.Message):
    r"""Request message for ListManagedFolders.

    Attributes:
        parent (str):
            Required. Name of the bucket this managed
            folder belongs to.
        page_size (int):
            Optional. Maximum number of managed folders
            to return in a single response. The service will
            use this parameter or 1,000 items, whichever is
            smaller.
        page_token (str):
            Optional. A previously-returned page token
            representing part of the larger set of results
            to view.
        prefix (str):
            Optional. Filter results to match managed
            folders with name starting with this prefix.
        request_id (str):
            Optional. A unique identifier for this
            request. UUID is the recommended format, but
            other formats are still accepted.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )
    prefix: str = proto.Field(
        proto.STRING,
        number=4,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=5,
    )


class ListManagedFoldersResponse(proto.Message):
    r"""Response message for ListManagedFolders.

    Attributes:
        managed_folders (MutableSequence[google.cloud.storage_control_v2.types.ManagedFolder]):
            The list of matching managed folders
        next_page_token (str):
            The continuation token, used to page through
            large result sets. Provide this value in a
            subsequent request to return the next page of
            results.
    """

    @property
    def raw_page(self):
        return self

    managed_folders: MutableSequence["ManagedFolder"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="ManagedFolder",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
