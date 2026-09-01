# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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

import google.protobuf.timestamp_pb2 as timestamp_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.apptopology_v1.types import graph as gca_graph
from google.cloud.apptopology_v1.types import query, schema

__protobuf__ = proto.module(
    package="google.cloud.apptopology.v1",
    manifest={
        "OperationMetadata",
        "GenerateDiscoveredResourcesTopologyRequest",
        "GenerateDiscoveredResourcesTopologyResponse",
        "GetSchemaRequest",
        "GetDomainRequest",
        "ListDomainsRequest",
        "ListDomainsResponse",
    },
)


class OperationMetadata(proto.Message):
    r"""Represents the metadata of the long-running operation.

    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation was
            created.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation finished
            running.
        target (str):
            Output only. Server-defined resource path for
            the target of the operation.
        verb (str):
            Output only. Name of the verb executed by the
            operation.
        status_message (str):
            Output only. Human-readable status of the
            operation, if any.
        requested_cancellation (bool):
            Output only. Identifies whether the user has requested
            cancellation of the operation. Operations that have been
            cancelled successfully have
            [google.longrunning.Operation.error][google.longrunning.Operation.error]
            value with a
            [google.rpc.Status.code][google.rpc.Status.code] of ``1``,
            corresponding to ``Code.CANCELLED``.
        api_version (str):
            Output only. API version used to start the
            operation.
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
    target: str = proto.Field(
        proto.STRING,
        number=3,
    )
    verb: str = proto.Field(
        proto.STRING,
        number=4,
    )
    status_message: str = proto.Field(
        proto.STRING,
        number=5,
    )
    requested_cancellation: bool = proto.Field(
        proto.BOOL,
        number=6,
    )
    api_version: str = proto.Field(
        proto.STRING,
        number=7,
    )


class GenerateDiscoveredResourcesTopologyRequest(proto.Message):
    r"""Request for GenerateDiscoveredResourcesTopology.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        filter (google.cloud.apptopology_v1.types.GraphPattern):
            Filters for the topology nodes and edges;
            Detail format see GraphPattern proto. A separate
            'LookupSchema' method will be added that will
            return the necessary information to be able to
            construct these filters.

            This field is a member of `oneof`_ ``query``.
        name (str):
            Required. The project to query discoverable resources on.
            Expected format:
            ``projects/{project}/locations/{location}/discoveredResourcesTopology``.
            Only ``global`` location is supported.
        topology_domains (MutableSequence[str]):
            Required. The full resource name of the domain of the app
            topology. Format:
            ``projects/{project}/locations/{location}/domains/{domain}``
            Caller must have apptopology.domains.get permission on each
            of the domains.
    """

    filter: query.GraphPattern = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="query",
        message=query.GraphPattern,
    )
    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    topology_domains: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )


class GenerateDiscoveredResourcesTopologyResponse(proto.Message):
    r"""Response for GenerateDiscoveredResourcesTopology.

    Attributes:
        graph (google.cloud.apptopology_v1.types.Graph):
            The generated topology graph.
    """

    graph: gca_graph.Graph = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gca_graph.Graph,
    )


class GetSchemaRequest(proto.Message):
    r"""Request for GetSchema.

    Attributes:
        name (str):
            Required. The name of the singleton domain schema resource.
            Format:
            ``projects/{project}/locations/{location}/domains/{domain}/schema``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class GetDomainRequest(proto.Message):
    r"""Request for GetDomain.

    Attributes:
        name (str):
            Required. The name of the domain to retrieve. Format:
            ``projects/{project}/locations/{location}/domains/{domain}``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListDomainsRequest(proto.Message):
    r"""Request for ListDomains.

    Attributes:
        parent (str):
            Required. The parent location to list domains for. Format:
            ``projects/{project}/locations/{location}`` Only ``global``
            location is supported.
        page_size (int):
            Optional. The maximum number of domains to
            return. The service may return fewer than this
            value. If unspecified, at most 50 domains will
            be returned. The maximum value is 1000; values
            above 1000 will be coerced to 1000.
        page_token (str):
            Optional. A page token, received from a previous
            ``ListDomains`` call. Provide this to retrieve the
            subsequent page.

            When paginating, all other parameters provided to
            ``ListDomains`` must match the call that provided the page
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


class ListDomainsResponse(proto.Message):
    r"""Response for ListDomains.

    Attributes:
        domains (MutableSequence[google.cloud.apptopology_v1.types.Domain]):
            The domains in the specified location.
        next_page_token (str):
            A token that can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    domains: MutableSequence[schema.Domain] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=schema.Domain,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
