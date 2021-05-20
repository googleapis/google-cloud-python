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

from google.protobuf import field_mask_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.asset.v1p2beta1",
    manifest={
        "ContentType",
        "CreateFeedRequest",
        "GetFeedRequest",
        "ListFeedsRequest",
        "ListFeedsResponse",
        "UpdateFeedRequest",
        "DeleteFeedRequest",
        "OutputConfig",
        "GcsDestination",
        "PubsubDestination",
        "FeedOutputConfig",
        "Feed",
    },
)


class ContentType(proto.Enum):
    r"""Asset content type."""
    CONTENT_TYPE_UNSPECIFIED = 0
    RESOURCE = 1
    IAM_POLICY = 2


class CreateFeedRequest(proto.Message):
    r"""Create asset feed request.
    Attributes:
        parent (str):
            Required. The name of the
            project/folder/organization where this feed
            should be created in. It can only be an
            organization number (such as
            "organizations/123"), a folder number (such as
            "folders/123"), a project ID (such as
            "projects/my-project-id")", or a project number
            (such as "projects/12345").
        feed_id (str):
            Required. This is the client-assigned asset
            feed identifier and it needs to be unique under
            a specific parent project/folder/organization.
        feed (google.cloud.asset_v1p2beta1.types.Feed):
            Required. The feed details. The field ``name`` must be empty
            and it will be generated in the format of:
            projects/project_number/feeds/feed_id
            folders/folder_number/feeds/feed_id
            organizations/organization_number/feeds/feed_id
    """

    parent = proto.Field(proto.STRING, number=1,)
    feed_id = proto.Field(proto.STRING, number=2,)
    feed = proto.Field(proto.MESSAGE, number=3, message="Feed",)


class GetFeedRequest(proto.Message):
    r"""Get asset feed request.
    Attributes:
        name (str):
            Required. The name of the Feed and it must be in the format
            of: projects/project_number/feeds/feed_id
            folders/folder_number/feeds/feed_id
            organizations/organization_number/feeds/feed_id
    """

    name = proto.Field(proto.STRING, number=1,)


class ListFeedsRequest(proto.Message):
    r"""List asset feeds request.
    Attributes:
        parent (str):
            Required. The parent
            project/folder/organization whose feeds are to
            be listed. It can only be using
            project/folder/organization number (such as
            "folders/12345")", or a project ID (such as
            "projects/my-project-id").
    """

    parent = proto.Field(proto.STRING, number=1,)


class ListFeedsResponse(proto.Message):
    r"""
    Attributes:
        feeds (Sequence[google.cloud.asset_v1p2beta1.types.Feed]):
            A list of feeds.
    """

    feeds = proto.RepeatedField(proto.MESSAGE, number=1, message="Feed",)


class UpdateFeedRequest(proto.Message):
    r"""Update asset feed request.
    Attributes:
        feed (google.cloud.asset_v1p2beta1.types.Feed):
            Required. The new values of feed details. It must match an
            existing feed and the field ``name`` must be in the format
            of: projects/project_number/feeds/feed_id or
            folders/folder_number/feeds/feed_id or
            organizations/organization_number/feeds/feed_id.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Only updates the ``feed`` fields indicated by this
            mask. The field mask must not be empty, and it must not
            contain fields that are immutable or only set by the server.
    """

    feed = proto.Field(proto.MESSAGE, number=1, message="Feed",)
    update_mask = proto.Field(
        proto.MESSAGE, number=2, message=field_mask_pb2.FieldMask,
    )


class DeleteFeedRequest(proto.Message):
    r"""
    Attributes:
        name (str):
            Required. The name of the feed and it must be in the format
            of: projects/project_number/feeds/feed_id
            folders/folder_number/feeds/feed_id
            organizations/organization_number/feeds/feed_id
    """

    name = proto.Field(proto.STRING, number=1,)


class OutputConfig(proto.Message):
    r"""Output configuration for export assets destination.
    Attributes:
        gcs_destination (google.cloud.asset_v1p2beta1.types.GcsDestination):
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
    """

    uri = proto.Field(proto.STRING, number=1, oneof="object_uri",)


class PubsubDestination(proto.Message):
    r"""A Cloud Pubsub destination.
    Attributes:
        topic (str):
            The name of the Cloud Pub/Sub topic to publish to. For
            example: ``projects/PROJECT_ID/topics/TOPIC_ID``.
    """

    topic = proto.Field(proto.STRING, number=1,)


class FeedOutputConfig(proto.Message):
    r"""Output configuration for asset feed destination.
    Attributes:
        pubsub_destination (google.cloud.asset_v1p2beta1.types.PubsubDestination):
            Destination on Cloud Pubsub.
    """

    pubsub_destination = proto.Field(
        proto.MESSAGE, number=1, oneof="destination", message="PubsubDestination",
    )


class Feed(proto.Message):
    r"""An asset feed used to export asset updates to a destinations.
    An asset feed filter controls what updates are exported. The
    asset feed must be created within a project, organization, or
    folder. Supported destinations are:
    Cloud Pub/Sub topics.

    Attributes:
        name (str):
            Required. The format will be
            projects/{project_number}/feeds/{client-assigned_feed_identifier}
            or
            folders/{folder_number}/feeds/{client-assigned_feed_identifier}
            or
            organizations/{organization_number}/feeds/{client-assigned_feed_identifier}

            The client-assigned feed identifier must be unique within
            the parent project/folder/organization.
        asset_names (Sequence[str]):
            A list of the full names of the assets to receive updates.
            You must specify either or both of asset_names and
            asset_types. Only asset updates matching specified
            asset_names and asset_types are exported to the feed. For
            example:
            ``//compute.googleapis.com/projects/my_project_123/zones/zone1/instances/instance1``.
            See `Resource
            Names <https://cloud.google.com/apis/design/resource_names#full_resource_name>`__
            for more info.
        asset_types (Sequence[str]):
            A list of types of the assets to receive updates. You must
            specify either or both of asset_names and asset_types. Only
            asset updates matching specified asset_names and asset_types
            are exported to the feed. For example:
            "compute.googleapis.com/Disk" See `Introduction to Cloud
            Asset
            Inventory <https://cloud.google.com/resource-manager/docs/cloud-asset-inventory/overview>`__
            for all supported asset types.
        content_type (google.cloud.asset_v1p2beta1.types.ContentType):
            Asset content type. If not specified, no
            content but the asset name and type will be
            returned.
        feed_output_config (google.cloud.asset_v1p2beta1.types.FeedOutputConfig):
            Required. Feed output configuration defining
            where the asset updates are published to.
    """

    name = proto.Field(proto.STRING, number=1,)
    asset_names = proto.RepeatedField(proto.STRING, number=2,)
    asset_types = proto.RepeatedField(proto.STRING, number=3,)
    content_type = proto.Field(proto.ENUM, number=4, enum="ContentType",)
    feed_output_config = proto.Field(
        proto.MESSAGE, number=5, message="FeedOutputConfig",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
