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

from google.protobuf import field_mask_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.managedkafka_v1.types import resources

__protobuf__ = proto.module(
    package="google.cloud.managedkafka.v1",
    manifest={
        "ListClustersRequest",
        "ListClustersResponse",
        "GetClusterRequest",
        "CreateClusterRequest",
        "UpdateClusterRequest",
        "DeleteClusterRequest",
        "ListTopicsRequest",
        "ListTopicsResponse",
        "GetTopicRequest",
        "CreateTopicRequest",
        "UpdateTopicRequest",
        "DeleteTopicRequest",
        "ListConsumerGroupsRequest",
        "ListConsumerGroupsResponse",
        "GetConsumerGroupRequest",
        "UpdateConsumerGroupRequest",
        "DeleteConsumerGroupRequest",
    },
)


class ListClustersRequest(proto.Message):
    r"""Request for ListClusters.

    Attributes:
        parent (str):
            Required. The parent location whose clusters are to be
            listed. Structured like
            ``projects/{project}/locations/{location}``.
        page_size (int):
            Optional. The maximum number of clusters to
            return. The service may return fewer than this
            value. If unspecified, server will pick an
            appropriate default.
        page_token (str):
            Optional. A page token, received from a previous
            ``ListClusters`` call. Provide this to retrieve the
            subsequent page.

            When paginating, all other parameters provided to
            ``ListClusters`` must match the call that provided the page
            token.
        filter (str):
            Optional. Filter expression for the result.
        order_by (str):
            Optional. Order by fields for the result.
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
    filter: str = proto.Field(
        proto.STRING,
        number=4,
    )
    order_by: str = proto.Field(
        proto.STRING,
        number=5,
    )


class ListClustersResponse(proto.Message):
    r"""Response for ListClusters.

    Attributes:
        clusters (MutableSequence[google.cloud.managedkafka_v1.types.Cluster]):
            The list of Clusters in the requested parent.
        next_page_token (str):
            A token that can be sent as ``page_token`` to retrieve the
            next page of results. If this field is omitted, there are no
            more results.
        unreachable (MutableSequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    clusters: MutableSequence[resources.Cluster] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=resources.Cluster,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class GetClusterRequest(proto.Message):
    r"""Request for GetCluster.

    Attributes:
        name (str):
            Required. The name of the cluster whose
            configuration to return.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateClusterRequest(proto.Message):
    r"""Request for CreateCluster.

    Attributes:
        parent (str):
            Required. The parent region in which to create the cluster.
            Structured like ``projects/{project}/locations/{location}``.
        cluster_id (str):
            Required. The ID to use for the cluster, which will become
            the final component of the cluster's name. The ID must be
            1-63 characters long, and match the regular expression
            ``[a-z]([-a-z0-9]*[a-z0-9])?`` to comply with RFC 1035.

            This value is structured like: ``my-cluster-id``.
        cluster (google.cloud.managedkafka_v1.types.Cluster):
            Required. Configuration of the cluster to create. Its
            ``name`` field is ignored.
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID to avoid
            duplication of requests. If a request times out
            or fails, retrying with the same ID allows the
            server to recognize the previous attempt. For at
            least 60 minutes, the server ignores duplicate
            requests bearing the same ID.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID within 60 minutes of the last request, the
            server checks if an original operation with the
            same request ID was received. If so, the server
            ignores the second request.

            The request ID must be a valid UUID. A zero UUID
            is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    cluster_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    cluster: resources.Cluster = proto.Field(
        proto.MESSAGE,
        number=3,
        message=resources.Cluster,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=4,
    )


class UpdateClusterRequest(proto.Message):
    r"""Request for UpdateCluster.

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Field mask is used to specify the fields to be
            overwritten in the cluster resource by the update. The
            fields specified in the update_mask are relative to the
            resource, not the full request. A field will be overwritten
            if it is in the mask. The mask is required and a value of \*
            will update all fields.
        cluster (google.cloud.managedkafka_v1.types.Cluster):
            Required. The cluster to update. Its ``name`` field must be
            populated.
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID to avoid
            duplication of requests. If a request times out
            or fails, retrying with the same ID allows the
            server to recognize the previous attempt. For at
            least 60 minutes, the server ignores duplicate
            requests bearing the same ID.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID within 60 minutes of the last request, the
            server checks if an original operation with the
            same request ID was received. If so, the server
            ignores the second request.

            The request ID must be a valid UUID. A zero UUID
            is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=1,
        message=field_mask_pb2.FieldMask,
    )
    cluster: resources.Cluster = proto.Field(
        proto.MESSAGE,
        number=2,
        message=resources.Cluster,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class DeleteClusterRequest(proto.Message):
    r"""Request for DeleteCluster.

    Attributes:
        name (str):
            Required. The name of the cluster to delete.
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID to avoid
            duplication of requests. If a request times out
            or fails, retrying with the same ID allows the
            server to recognize the previous attempt. For at
            least 60 minutes, the server ignores duplicate
            requests bearing the same ID.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID within 60 minutes of the last request, the
            server checks if an original operation with the
            same request ID was received. If so, the server
            ignores the second request.

            The request ID must be a valid UUID. A zero UUID
            is not supported
            (00000000-0000-0000-0000-000000000000).
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ListTopicsRequest(proto.Message):
    r"""Request for ListTopics.

    Attributes:
        parent (str):
            Required. The parent cluster whose topics are to be listed.
            Structured like
            ``projects/{project}/locations/{location}/clusters/{cluster}``.
        page_size (int):
            Optional. The maximum number of topics to
            return. The service may return fewer than this
            value. If unset or zero, all topics for the
            parent is returned.
        page_token (str):
            Optional. A page token, received from a previous
            ``ListTopics`` call. Provide this to retrieve the subsequent
            page.

            When paginating, all other parameters provided to
            ``ListTopics`` must match the call that provided the page
            token.
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


class ListTopicsResponse(proto.Message):
    r"""Response for ListTopics.

    Attributes:
        topics (MutableSequence[google.cloud.managedkafka_v1.types.Topic]):
            The list of topics in the requested parent.
            The order of the topics is unspecified.
        next_page_token (str):
            A token that can be sent as ``page_token`` to retrieve the
            next page of results. If this field is omitted, there are no
            more results.
    """

    @property
    def raw_page(self):
        return self

    topics: MutableSequence[resources.Topic] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=resources.Topic,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetTopicRequest(proto.Message):
    r"""Request for GetTopic.

    Attributes:
        name (str):
            Required. The name of the topic whose
            configuration to return. Structured like:

            projects/{project}/locations/{location}/clusters/{cluster}/topics/{topic}.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateTopicRequest(proto.Message):
    r"""Request for CreateTopic.

    Attributes:
        parent (str):
            Required. The parent cluster in which to create the topic.
            Structured like
            ``projects/{project}/locations/{location}/clusters/{cluster}``.
        topic_id (str):
            Required. The ID to use for the topic, which will become the
            final component of the topic's name.

            This value is structured like: ``my-topic-name``.
        topic (google.cloud.managedkafka_v1.types.Topic):
            Required. Configuration of the topic to create. Its ``name``
            field is ignored.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    topic_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    topic: resources.Topic = proto.Field(
        proto.MESSAGE,
        number=3,
        message=resources.Topic,
    )


class UpdateTopicRequest(proto.Message):
    r"""Request for UpdateTopic.

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Field mask is used to specify the fields to be
            overwritten in the Topic resource by the update. The fields
            specified in the update_mask are relative to the resource,
            not the full request. A field will be overwritten if it is
            in the mask. The mask is required and a value of \* will
            update all fields.
        topic (google.cloud.managedkafka_v1.types.Topic):
            Required. The topic to update. Its ``name`` field must be
            populated.
    """

    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=1,
        message=field_mask_pb2.FieldMask,
    )
    topic: resources.Topic = proto.Field(
        proto.MESSAGE,
        number=2,
        message=resources.Topic,
    )


class DeleteTopicRequest(proto.Message):
    r"""Request for DeleteTopic.

    Attributes:
        name (str):
            Required. The name of the topic to delete.
            ``projects/{project}/locations/{location}/clusters/{cluster}/topics/{topic}``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListConsumerGroupsRequest(proto.Message):
    r"""Request for ListConsumerGroups.

    Attributes:
        parent (str):
            Required. The parent cluster whose consumer groups are to be
            listed. Structured like
            ``projects/{project}/locations/{location}/clusters/{cluster}``.
        page_size (int):
            Optional. The maximum number of consumer
            groups to return. The service may return fewer
            than this value. If unset or zero, all consumer
            groups for the parent is returned.
        page_token (str):
            Optional. A page token, received from a previous
            ``ListConsumerGroups`` call. Provide this to retrieve the
            subsequent page.

            When paginating, all other parameters provided to
            ``ListConsumerGroups`` must match the call that provided the
            page token.
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


class ListConsumerGroupsResponse(proto.Message):
    r"""Response for ListConsumerGroups.

    Attributes:
        consumer_groups (MutableSequence[google.cloud.managedkafka_v1.types.ConsumerGroup]):
            The list of consumer group in the requested
            parent. The order of the consumer groups is
            unspecified.
        next_page_token (str):
            A token that can be sent as ``page_token`` to retrieve the
            next page of results. If this field is omitted, there are no
            more results.
    """

    @property
    def raw_page(self):
        return self

    consumer_groups: MutableSequence[resources.ConsumerGroup] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=resources.ConsumerGroup,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetConsumerGroupRequest(proto.Message):
    r"""Request for GetConsumerGroup.

    Attributes:
        name (str):
            Required. The name of the consumer group whose configuration
            to return.
            ``projects/{project}/locations/{location}/clusters/{cluster}/consumerGroups/{consumerGroup}``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class UpdateConsumerGroupRequest(proto.Message):
    r"""Request for UpdateConsumerGroup.

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Field mask is used to specify the fields to be
            overwritten in the ConsumerGroup resource by the update. The
            fields specified in the update_mask are relative to the
            resource, not the full request. A field will be overwritten
            if it is in the mask. The mask is required and a value of \*
            will update all fields.
        consumer_group (google.cloud.managedkafka_v1.types.ConsumerGroup):
            Required. The consumer group to update. Its ``name`` field
            must be populated.
    """

    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=1,
        message=field_mask_pb2.FieldMask,
    )
    consumer_group: resources.ConsumerGroup = proto.Field(
        proto.MESSAGE,
        number=2,
        message=resources.ConsumerGroup,
    )


class DeleteConsumerGroupRequest(proto.Message):
    r"""Request for DeleteConsumerGroup.

    Attributes:
        name (str):
            Required. The name of the consumer group to delete.
            ``projects/{project}/locations/{location}/clusters/{cluster}/consumerGroups/{consumerGroup}``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
