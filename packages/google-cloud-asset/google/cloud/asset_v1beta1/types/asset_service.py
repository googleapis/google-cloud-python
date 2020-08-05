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


from google.cloud.asset_v1beta1.types import assets as gca_assets
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.asset.v1beta1",
    manifest={
        "ContentType",
        "ExportAssetsRequest",
        "ExportAssetsResponse",
        "BatchGetAssetsHistoryRequest",
        "BatchGetAssetsHistoryResponse",
        "OutputConfig",
        "GcsDestination",
    },
)


class ContentType(proto.Enum):
    r"""Asset content type."""
    CONTENT_TYPE_UNSPECIFIED = 0
    RESOURCE = 1
    IAM_POLICY = 2


class ExportAssetsRequest(proto.Message):
    r"""Export asset request.

    Attributes:
        parent (str):
            Required. The relative name of the root
            asset. This can only be an organization number
            (such as "organizations/123"), a project ID
            (such as "projects/my-project-id"), a project
            number (such as "projects/12345"), or a folder
            number (such as "folders/123").
        read_time (~.timestamp.Timestamp):
            Timestamp to take an asset snapshot. This can
            only be set to a timestamp between 2018-10-02
            UTC (inclusive) and the current time. If not
            specified, the current time will be used. Due to
            delays in resource data collection and indexing,
            there is a volatile window during which running
            the same query may get different results.
        asset_types (Sequence[str]):
            A list of asset types of which to take a snapshot for. For
            example: "google.compute.Disk". If specified, only matching
            assets will be returned. See `Introduction to Cloud Asset
            Inventory <https://cloud.google.com/resource-manager/docs/cloud-asset-inventory/overview>`__
            for all supported asset types.
        content_type (~.asset_service.ContentType):
            Asset content type. If not specified, no
            content but the asset name will be returned.
        output_config (~.asset_service.OutputConfig):
            Required. Output configuration indicating
            where the results will be output to. All results
            will be in newline delimited JSON format.
    """

    parent = proto.Field(proto.STRING, number=1)

    read_time = proto.Field(proto.MESSAGE, number=2, message=timestamp.Timestamp,)

    asset_types = proto.RepeatedField(proto.STRING, number=3)

    content_type = proto.Field(proto.ENUM, number=4, enum="ContentType",)

    output_config = proto.Field(proto.MESSAGE, number=5, message="OutputConfig",)


class ExportAssetsResponse(proto.Message):
    r"""The export asset response. This message is returned by the
    [google.longrunning.Operations.GetOperation][google.longrunning.Operations.GetOperation]
    method in the returned
    [google.longrunning.Operation.response][google.longrunning.Operation.response]
    field.

    Attributes:
        read_time (~.timestamp.Timestamp):
            Time the snapshot was taken.
        output_config (~.asset_service.OutputConfig):
            Output configuration indicating where the
            results were output to. All results are in JSON
            format.
    """

    read_time = proto.Field(proto.MESSAGE, number=1, message=timestamp.Timestamp,)

    output_config = proto.Field(proto.MESSAGE, number=2, message="OutputConfig",)


class BatchGetAssetsHistoryRequest(proto.Message):
    r"""Batch get assets history request.

    Attributes:
        parent (str):
            Required. The relative name of the root
            asset. It can only be an organization number
            (such as "organizations/123"), a project ID
            (such as "projects/my-project-id")", or a
            project number (such as "projects/12345").
        asset_names (Sequence[str]):
            A list of the full names of the assets. For example:
            ``//compute.googleapis.com/projects/my_project_123/zones/zone1/instances/instance1``.
            See `Resource
            Names <https://cloud.google.com/apis/design/resource_names#full_resource_name>`__
            for more info.

            The request becomes a no-op if the asset name list is empty,
            and the max size of the asset name list is 100 in one
            request.
        content_type (~.asset_service.ContentType):
            Optional. The content type.
        read_time_window (~.gca_assets.TimeWindow):
            Optional. The time window for the asset history. Both
            start_time and end_time are optional and if set, it must be
            after 2018-10-02 UTC. If end_time is not set, it is default
            to current timestamp. If start_time is not set, the snapshot
            of the assets at end_time will be returned. The returned
            results contain all temporal assets whose time window
            overlap with read_time_window.
    """

    parent = proto.Field(proto.STRING, number=1)

    asset_names = proto.RepeatedField(proto.STRING, number=2)

    content_type = proto.Field(proto.ENUM, number=3, enum="ContentType",)

    read_time_window = proto.Field(
        proto.MESSAGE, number=4, message=gca_assets.TimeWindow,
    )


class BatchGetAssetsHistoryResponse(proto.Message):
    r"""Batch get assets history response.

    Attributes:
        assets (Sequence[~.gca_assets.TemporalAsset]):
            A list of assets with valid time windows.
    """

    assets = proto.RepeatedField(
        proto.MESSAGE, number=1, message=gca_assets.TemporalAsset,
    )


class OutputConfig(proto.Message):
    r"""Output configuration for export assets destination.

    Attributes:
        gcs_destination (~.asset_service.GcsDestination):
            Destination on Cloud Storage.
    """

    gcs_destination = proto.Field(
        proto.MESSAGE, number=1, oneof="destination", message="GcsDestination",
    )


class GcsDestination(proto.Message):
    r"""A Cloud Storage location.

    Attributes:
        uri (str):
            The uri of the Cloud Storage object. It's the same uri that
            is used by gsutil. For example:
            "gs://bucket_name/object_name". See `Viewing and Editing
            Object
            Metadata <https://cloud.google.com/storage/docs/viewing-editing-metadata>`__
            for more information.
        uri_prefix (str):
            The uri prefix of all generated Cloud Storage objects. For
            example: "gs://bucket_name/object_name_prefix". Each object
            uri is in format: "gs://bucket_name/object_name_prefix// and
            only contains assets for that type. starts from 0. For
            example:
            "gs://bucket_name/object_name_prefix/google.compute.disk/0"
            is the first shard of output objects containing all
            google.compute.disk assets. An INVALID_ARGUMENT error will
            be returned if file with the same name
            "gs://bucket_name/object_name_prefix" already exists.
    """

    uri = proto.Field(proto.STRING, number=1, oneof="object_uri")

    uri_prefix = proto.Field(proto.STRING, number=2, oneof="object_uri")


__all__ = tuple(sorted(__protobuf__.manifest))
