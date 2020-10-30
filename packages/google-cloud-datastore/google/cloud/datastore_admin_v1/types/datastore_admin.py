# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
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

import proto  # type: ignore


from google.cloud.datastore_admin_v1.types import index
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore


__protobuf__ = proto.module(
    package="google.datastore.admin.v1",
    manifest={
        "OperationType",
        "CommonMetadata",
        "Progress",
        "ExportEntitiesRequest",
        "ImportEntitiesRequest",
        "ExportEntitiesResponse",
        "ExportEntitiesMetadata",
        "ImportEntitiesMetadata",
        "EntityFilter",
        "GetIndexRequest",
        "ListIndexesRequest",
        "ListIndexesResponse",
        "IndexOperationMetadata",
    },
)


class OperationType(proto.Enum):
    r"""Operation types."""
    OPERATION_TYPE_UNSPECIFIED = 0
    EXPORT_ENTITIES = 1
    IMPORT_ENTITIES = 2
    CREATE_INDEX = 3
    DELETE_INDEX = 4


class CommonMetadata(proto.Message):
    r"""Metadata common to all Datastore Admin operations.

    Attributes:
        start_time (~.timestamp.Timestamp):
            The time that work began on the operation.
        end_time (~.timestamp.Timestamp):
            The time the operation ended, either
            successfully or otherwise.
        operation_type (~.datastore_admin.OperationType):
            The type of the operation. Can be used as a
            filter in ListOperationsRequest.
        labels (Sequence[~.datastore_admin.CommonMetadata.LabelsEntry]):
            The client-assigned labels which were
            provided when the operation was created. May
            also include additional labels.
        state (~.datastore_admin.CommonMetadata.State):
            The current state of the Operation.
    """

    class State(proto.Enum):
        r"""The various possible states for an ongoing Operation."""
        STATE_UNSPECIFIED = 0
        INITIALIZING = 1
        PROCESSING = 2
        CANCELLING = 3
        FINALIZING = 4
        SUCCESSFUL = 5
        FAILED = 6
        CANCELLED = 7

    start_time = proto.Field(proto.MESSAGE, number=1, message=timestamp.Timestamp,)

    end_time = proto.Field(proto.MESSAGE, number=2, message=timestamp.Timestamp,)

    operation_type = proto.Field(proto.ENUM, number=3, enum="OperationType",)

    labels = proto.MapField(proto.STRING, proto.STRING, number=4)

    state = proto.Field(proto.ENUM, number=5, enum=State,)


class Progress(proto.Message):
    r"""Measures the progress of a particular metric.

    Attributes:
        work_completed (int):
            The amount of work that has been completed. Note that this
            may be greater than work_estimated.
        work_estimated (int):
            An estimate of how much work needs to be
            performed. May be zero if the work estimate is
            unavailable.
    """

    work_completed = proto.Field(proto.INT64, number=1)

    work_estimated = proto.Field(proto.INT64, number=2)


class ExportEntitiesRequest(proto.Message):
    r"""The request for
    [google.datastore.admin.v1.DatastoreAdmin.ExportEntities][google.datastore.admin.v1.DatastoreAdmin.ExportEntities].

    Attributes:
        project_id (str):
            Required. Project ID against which to make
            the request.
        labels (Sequence[~.datastore_admin.ExportEntitiesRequest.LabelsEntry]):
            Client-assigned labels.
        entity_filter (~.datastore_admin.EntityFilter):
            Description of what data from the project is
            included in the export.
        output_url_prefix (str):
            Required. Location for the export metadata and data files.

            The full resource URL of the external storage location.
            Currently, only Google Cloud Storage is supported. So
            output_url_prefix should be of the form:
            ``gs://BUCKET_NAME[/NAMESPACE_PATH]``, where ``BUCKET_NAME``
            is the name of the Cloud Storage bucket and
            ``NAMESPACE_PATH`` is an optional Cloud Storage namespace
            path (this is not a Cloud Datastore namespace). For more
            information about Cloud Storage namespace paths, see `Object
            name
            considerations <https://cloud.google.com/storage/docs/naming#object-considerations>`__.

            The resulting files will be nested deeper than the specified
            URL prefix. The final output URL will be provided in the
            [google.datastore.admin.v1.ExportEntitiesResponse.output_url][google.datastore.admin.v1.ExportEntitiesResponse.output_url]
            field. That value should be used for subsequent
            ImportEntities operations.

            By nesting the data files deeper, the same Cloud Storage
            bucket can be used in multiple ExportEntities operations
            without conflict.
    """

    project_id = proto.Field(proto.STRING, number=1)

    labels = proto.MapField(proto.STRING, proto.STRING, number=2)

    entity_filter = proto.Field(proto.MESSAGE, number=3, message="EntityFilter",)

    output_url_prefix = proto.Field(proto.STRING, number=4)


class ImportEntitiesRequest(proto.Message):
    r"""The request for
    [google.datastore.admin.v1.DatastoreAdmin.ImportEntities][google.datastore.admin.v1.DatastoreAdmin.ImportEntities].

    Attributes:
        project_id (str):
            Required. Project ID against which to make
            the request.
        labels (Sequence[~.datastore_admin.ImportEntitiesRequest.LabelsEntry]):
            Client-assigned labels.
        input_url (str):
            Required. The full resource URL of the external storage
            location. Currently, only Google Cloud Storage is supported.
            So input_url should be of the form:
            ``gs://BUCKET_NAME[/NAMESPACE_PATH]/OVERALL_EXPORT_METADATA_FILE``,
            where ``BUCKET_NAME`` is the name of the Cloud Storage
            bucket, ``NAMESPACE_PATH`` is an optional Cloud Storage
            namespace path (this is not a Cloud Datastore namespace),
            and ``OVERALL_EXPORT_METADATA_FILE`` is the metadata file
            written by the ExportEntities operation. For more
            information about Cloud Storage namespace paths, see `Object
            name
            considerations <https://cloud.google.com/storage/docs/naming#object-considerations>`__.

            For more information, see
            [google.datastore.admin.v1.ExportEntitiesResponse.output_url][google.datastore.admin.v1.ExportEntitiesResponse.output_url].
        entity_filter (~.datastore_admin.EntityFilter):
            Optionally specify which kinds/namespaces are to be
            imported. If provided, the list must be a subset of the
            EntityFilter used in creating the export, otherwise a
            FAILED_PRECONDITION error will be returned. If no filter is
            specified then all entities from the export are imported.
    """

    project_id = proto.Field(proto.STRING, number=1)

    labels = proto.MapField(proto.STRING, proto.STRING, number=2)

    input_url = proto.Field(proto.STRING, number=3)

    entity_filter = proto.Field(proto.MESSAGE, number=4, message="EntityFilter",)


class ExportEntitiesResponse(proto.Message):
    r"""The response for
    [google.datastore.admin.v1.DatastoreAdmin.ExportEntities][google.datastore.admin.v1.DatastoreAdmin.ExportEntities].

    Attributes:
        output_url (str):
            Location of the output metadata file. This can be used to
            begin an import into Cloud Datastore (this project or
            another project). See
            [google.datastore.admin.v1.ImportEntitiesRequest.input_url][google.datastore.admin.v1.ImportEntitiesRequest.input_url].
            Only present if the operation completed successfully.
    """

    output_url = proto.Field(proto.STRING, number=1)


class ExportEntitiesMetadata(proto.Message):
    r"""Metadata for ExportEntities operations.

    Attributes:
        common (~.datastore_admin.CommonMetadata):
            Metadata common to all Datastore Admin
            operations.
        progress_entities (~.datastore_admin.Progress):
            An estimate of the number of entities
            processed.
        progress_bytes (~.datastore_admin.Progress):
            An estimate of the number of bytes processed.
        entity_filter (~.datastore_admin.EntityFilter):
            Description of which entities are being
            exported.
        output_url_prefix (str):
            Location for the export metadata and data files. This will
            be the same value as the
            [google.datastore.admin.v1.ExportEntitiesRequest.output_url_prefix][google.datastore.admin.v1.ExportEntitiesRequest.output_url_prefix]
            field. The final output location is provided in
            [google.datastore.admin.v1.ExportEntitiesResponse.output_url][google.datastore.admin.v1.ExportEntitiesResponse.output_url].
    """

    common = proto.Field(proto.MESSAGE, number=1, message="CommonMetadata",)

    progress_entities = proto.Field(proto.MESSAGE, number=2, message="Progress",)

    progress_bytes = proto.Field(proto.MESSAGE, number=3, message="Progress",)

    entity_filter = proto.Field(proto.MESSAGE, number=4, message="EntityFilter",)

    output_url_prefix = proto.Field(proto.STRING, number=5)


class ImportEntitiesMetadata(proto.Message):
    r"""Metadata for ImportEntities operations.

    Attributes:
        common (~.datastore_admin.CommonMetadata):
            Metadata common to all Datastore Admin
            operations.
        progress_entities (~.datastore_admin.Progress):
            An estimate of the number of entities
            processed.
        progress_bytes (~.datastore_admin.Progress):
            An estimate of the number of bytes processed.
        entity_filter (~.datastore_admin.EntityFilter):
            Description of which entities are being
            imported.
        input_url (str):
            The location of the import metadata file. This will be the
            same value as the
            [google.datastore.admin.v1.ExportEntitiesResponse.output_url][google.datastore.admin.v1.ExportEntitiesResponse.output_url]
            field.
    """

    common = proto.Field(proto.MESSAGE, number=1, message="CommonMetadata",)

    progress_entities = proto.Field(proto.MESSAGE, number=2, message="Progress",)

    progress_bytes = proto.Field(proto.MESSAGE, number=3, message="Progress",)

    entity_filter = proto.Field(proto.MESSAGE, number=4, message="EntityFilter",)

    input_url = proto.Field(proto.STRING, number=5)


class EntityFilter(proto.Message):
    r"""Identifies a subset of entities in a project. This is specified as
    combinations of kinds and namespaces (either or both of which may be
    all, as described in the following examples). Example usage:

    Entire project: kinds=[], namespace_ids=[]

    Kinds Foo and Bar in all namespaces: kinds=['Foo', 'Bar'],
    namespace_ids=[]

    Kinds Foo and Bar only in the default namespace: kinds=['Foo',
    'Bar'], namespace_ids=['']

    Kinds Foo and Bar in both the default and Baz namespaces:
    kinds=['Foo', 'Bar'], namespace_ids=['', 'Baz']

    The entire Baz namespace: kinds=[], namespace_ids=['Baz']

    Attributes:
        kinds (Sequence[str]):
            If empty, then this represents all kinds.
        namespace_ids (Sequence[str]):
            An empty list represents all namespaces. This
            is the preferred usage for projects that don't
            use namespaces.
            An empty string element represents the default
            namespace. This should be used if the project
            has data in non-default namespaces, but doesn't
            want to include them.
            Each namespace in this list must be unique.
    """

    kinds = proto.RepeatedField(proto.STRING, number=1)

    namespace_ids = proto.RepeatedField(proto.STRING, number=2)


class GetIndexRequest(proto.Message):
    r"""The request for
    [google.datastore.admin.v1.DatastoreAdmin.GetIndex][google.datastore.admin.v1.DatastoreAdmin.GetIndex].

    Attributes:
        project_id (str):
            Project ID against which to make the request.
        index_id (str):
            The resource ID of the index to get.
    """

    project_id = proto.Field(proto.STRING, number=1)

    index_id = proto.Field(proto.STRING, number=3)


class ListIndexesRequest(proto.Message):
    r"""The request for
    [google.datastore.admin.v1.DatastoreAdmin.ListIndexes][google.datastore.admin.v1.DatastoreAdmin.ListIndexes].

    Attributes:
        project_id (str):
            Project ID against which to make the request.
        filter (str):

        page_size (int):
            The maximum number of items to return.  If
            zero, then all results will be returned.
        page_token (str):
            The next_page_token value returned from a previous List
            request, if any.
    """

    project_id = proto.Field(proto.STRING, number=1)

    filter = proto.Field(proto.STRING, number=3)

    page_size = proto.Field(proto.INT32, number=4)

    page_token = proto.Field(proto.STRING, number=5)


class ListIndexesResponse(proto.Message):
    r"""The response for
    [google.datastore.admin.v1.DatastoreAdmin.ListIndexes][google.datastore.admin.v1.DatastoreAdmin.ListIndexes].

    Attributes:
        indexes (Sequence[~.index.Index]):
            The indexes.
        next_page_token (str):
            The standard List next-page token.
    """

    @property
    def raw_page(self):
        return self

    indexes = proto.RepeatedField(proto.MESSAGE, number=1, message=index.Index,)

    next_page_token = proto.Field(proto.STRING, number=2)


class IndexOperationMetadata(proto.Message):
    r"""Metadata for Index operations.

    Attributes:
        common (~.datastore_admin.CommonMetadata):
            Metadata common to all Datastore Admin
            operations.
        progress_entities (~.datastore_admin.Progress):
            An estimate of the number of entities
            processed.
        index_id (str):
            The index resource ID that this operation is
            acting on.
    """

    common = proto.Field(proto.MESSAGE, number=1, message="CommonMetadata",)

    progress_entities = proto.Field(proto.MESSAGE, number=2, message="Progress",)

    index_id = proto.Field(proto.STRING, number=3)


__all__ = tuple(sorted(__protobuf__.manifest))
