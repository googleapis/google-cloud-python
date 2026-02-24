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

import proto  # type: ignore

from google.cloud.ces_v1.types import auth, common

__protobuf__ = proto.module(
    package="google.cloud.ces.v1",
    manifest={
        "McpToolset",
    },
)


class McpToolset(proto.Message):
    r"""A toolset that contains a list of tools that are offered by
    the MCP server.

    Attributes:
        server_address (str):
            Required. The address of the MCP server, for
            example, "https://example.com/mcp/". If the
            server is built with the MCP SDK, the url should
            be suffixed with
            "/mcp/". Only Streamable HTTP transport based
            servers are supported. See
            https://modelcontextprotocol.io/specification/2025-03-26/basic/transports#streamable-http
            for more details.
        api_authentication (google.cloud.ces_v1.types.ApiAuthentication):
            Optional. Authentication information required
            to access tools and execute a tool against the
            MCP server. For bearer token authentication, the
            token applies only to tool execution, not to
            listing tools. This requires that tools can be
            listed without authentication.
        service_directory_config (google.cloud.ces_v1.types.ServiceDirectoryConfig):
            Optional. Service Directory configuration for
            VPC-SC, used to resolve service names within a
            perimeter.
        tls_config (google.cloud.ces_v1.types.TlsConfig):
            Optional. The TLS configuration. Includes the
            custom server certificates that the client
            should trust.
    """

    server_address: str = proto.Field(
        proto.STRING,
        number=1,
    )
    api_authentication: auth.ApiAuthentication = proto.Field(
        proto.MESSAGE,
        number=2,
        message=auth.ApiAuthentication,
    )
    service_directory_config: common.ServiceDirectoryConfig = proto.Field(
        proto.MESSAGE,
        number=3,
        message=common.ServiceDirectoryConfig,
    )
    tls_config: common.TlsConfig = proto.Field(
        proto.MESSAGE,
        number=4,
        message=common.TlsConfig,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
