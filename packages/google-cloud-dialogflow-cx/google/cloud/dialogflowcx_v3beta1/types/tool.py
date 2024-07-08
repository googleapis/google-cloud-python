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
from google.protobuf import struct_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.dialogflowcx_v3beta1.types import data_store_connection, inline

__protobuf__ = proto.module(
    package="google.cloud.dialogflow.cx.v3beta1",
    manifest={
        "CreateToolRequest",
        "ListToolsRequest",
        "ListToolsResponse",
        "GetToolRequest",
        "ExportToolsRequest",
        "ExportToolsResponse",
        "UpdateToolRequest",
        "DeleteToolRequest",
        "Tool",
        "ExportToolsMetadata",
    },
)


class CreateToolRequest(proto.Message):
    r"""The request message for
    [Tools.CreateTool][google.cloud.dialogflow.cx.v3beta1.Tools.CreateTool].

    Attributes:
        parent (str):
            Required. The agent to create a Tool for. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>``.
        tool (google.cloud.dialogflowcx_v3beta1.types.Tool):
            Required. The Tool to be created.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    tool: "Tool" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Tool",
    )


class ListToolsRequest(proto.Message):
    r"""The request message for
    [Tools.ListTools][google.cloud.dialogflow.cx.v3beta1.Tools.ListTools].

    Attributes:
        parent (str):
            Required. The agent to list the Tools from. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>``.
        page_size (int):
            The maximum number of items to return in a
            single page. By default 100 and at most 1000.
        page_token (str):
            The next_page_token value returned from a previous list
            request.
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


class ListToolsResponse(proto.Message):
    r"""The response message for
    [Tools.ListTools][google.cloud.dialogflow.cx.v3beta1.Tools.ListTools].

    Attributes:
        tools (MutableSequence[google.cloud.dialogflowcx_v3beta1.types.Tool]):
            The list of Tools. There will be a maximum number of items
            returned based on the page_size field in the request.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
    """

    @property
    def raw_page(self):
        return self

    tools: MutableSequence["Tool"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Tool",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetToolRequest(proto.Message):
    r"""The request message for
    [Tools.GetTool][google.cloud.dialogflow.cx.v3beta1.Tools.GetTool].

    Attributes:
        name (str):
            Required. The name of the Tool. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/tools/<Tool ID>``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ExportToolsRequest(proto.Message):
    r"""The request message for
    [Tools.ExportTools][google.cloud.dialogflow.cx.v3beta1.Tools.ExportTools].

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        parent (str):
            Required. The agent to export tools from. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>``.
        tools (MutableSequence[str]):
            Required. The name of the tools to export. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/tools/<Tool ID>``.
        tools_uri (str):
            Optional. The `Google Cloud
            Storage <https://cloud.google.com/storage/docs/>`__ URI to
            export the tools to. The format of this URI must be
            ``gs://<bucket-name>/<object-name>``.

            Dialogflow performs a write operation for the Cloud Storage
            object on the caller's behalf, so your request
            authentication must have write permissions for the object.
            For more information, see `Dialogflow access
            control <https://cloud.google.com/dialogflow/cx/docs/concept/access-control#storage>`__.

            This field is a member of `oneof`_ ``destination``.
        tools_content_inline (bool):
            Optional. The option to return the serialized
            tools inline.

            This field is a member of `oneof`_ ``destination``.
        data_format (google.cloud.dialogflowcx_v3beta1.types.ExportToolsRequest.DataFormat):
            Optional. The data format of the exported tools. If not
            specified, ``BLOB`` is assumed.
    """

    class DataFormat(proto.Enum):
        r"""Data format of the exported tools.

        Values:
            DATA_FORMAT_UNSPECIFIED (0):
                Unspecified format. Treated as ``BLOB``.
            BLOB (1):
                Tools will be exported as raw bytes.
            JSON (2):
                Tools will be exported in JSON format.
        """
        DATA_FORMAT_UNSPECIFIED = 0
        BLOB = 1
        JSON = 2

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    tools: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )
    tools_uri: str = proto.Field(
        proto.STRING,
        number=3,
        oneof="destination",
    )
    tools_content_inline: bool = proto.Field(
        proto.BOOL,
        number=4,
        oneof="destination",
    )
    data_format: DataFormat = proto.Field(
        proto.ENUM,
        number=5,
        enum=DataFormat,
    )


class ExportToolsResponse(proto.Message):
    r"""The response message for
    [Tools.ExportTools][google.cloud.dialogflow.cx.v3beta1.Tools.ExportTools].

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        tools_uri (str):
            The URI to a file containing the exported tools. This field
            is populated only if ``tools_uri`` is specified in
            [ExportToolsRequest][google.cloud.dialogflow.cx.v3beta1.ExportToolsRequest].

            This field is a member of `oneof`_ ``tools``.
        tools_content (google.cloud.dialogflowcx_v3beta1.types.InlineDestination):
            Uncompressed byte content for tools. This field is populated
            only if ``tools_content_inline`` is set to true in
            [ExportToolsRequest][google.cloud.dialogflow.cx.v3beta1.ExportToolsRequest].

            This field is a member of `oneof`_ ``tools``.
    """

    tools_uri: str = proto.Field(
        proto.STRING,
        number=1,
        oneof="tools",
    )
    tools_content: inline.InlineDestination = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="tools",
        message=inline.InlineDestination,
    )


class UpdateToolRequest(proto.Message):
    r"""The request message for
    [Tools.UpdateTool][google.cloud.dialogflow.cx.v3beta1.Tools.UpdateTool].

    Attributes:
        tool (google.cloud.dialogflowcx_v3beta1.types.Tool):
            Required. The Tool to be updated.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            The mask to control which fields get updated.
            If the mask is not present, all fields will be
            updated.
    """

    tool: "Tool" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="Tool",
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class DeleteToolRequest(proto.Message):
    r"""The request message for
    [Tools.DeleteTool][google.cloud.dialogflow.cx.v3beta1.Tools.DeleteTool].

    Attributes:
        name (str):
            Required. The name of the Tool to be deleted. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/tools/<Tool ID>``.
        force (bool):
            This field has no effect for Tools not being used. For Tools
            that are used:

            -  If ``force`` is set to false, an error will be returned
               with message indicating the referenced resources.
            -  If ``force`` is set to true, Dialogflow will remove the
               tool, as well as any references to the tool.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    force: bool = proto.Field(
        proto.BOOL,
        number=2,
    )


class Tool(proto.Message):
    r"""A tool provides a list of actions which are available to the
    [Playbook][google.cloud.dialogflow.cx.v3beta1.Playbook] to attain
    its goal. A Tool consists of a description of the tool's usage and a
    specification of the tool which contains the schema and
    authentication information.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            The unique identifier of the Tool. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/tools/<Tool ID>``.
        display_name (str):
            Required. The human-readable name of the
            Tool, unique within an agent.
        description (str):
            Required. High level description of the Tool
            and its usage.
        open_api_spec (google.cloud.dialogflowcx_v3beta1.types.Tool.OpenApiTool):
            OpenAPI specification of the Tool.

            This field is a member of `oneof`_ ``specification``.
        data_store_spec (google.cloud.dialogflowcx_v3beta1.types.Tool.DataStoreTool):
            Data store search tool specification.

            This field is a member of `oneof`_ ``specification``.
        extension_spec (google.cloud.dialogflowcx_v3beta1.types.Tool.ExtensionTool):
            Vertex extension tool specification.

            This field is a member of `oneof`_ ``specification``.
        function_spec (google.cloud.dialogflowcx_v3beta1.types.Tool.FunctionTool):
            Client side executed function specification.

            This field is a member of `oneof`_ ``specification``.
        tool_type (google.cloud.dialogflowcx_v3beta1.types.Tool.ToolType):
            Output only. The tool type.
    """

    class ToolType(proto.Enum):
        r"""Represents the type of the tool.

        Values:
            TOOL_TYPE_UNSPECIFIED (0):
                Default value. This value is unused.
            CUSTOMIZED_TOOL (1):
                Customer provided tool.
            BUILTIN_TOOL (2):
                First party built-in tool created by
                Dialogflow which cannot be modified.
        """
        TOOL_TYPE_UNSPECIFIED = 0
        CUSTOMIZED_TOOL = 1
        BUILTIN_TOOL = 2

    class OpenApiTool(proto.Message):
        r"""An OpenAPI tool is a way to provide the Tool specifications
        in the Open API schema format.


        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            text_schema (str):
                Required. The OpenAPI schema specified as a
                text.

                This field is a member of `oneof`_ ``schema``.
            authentication (google.cloud.dialogflowcx_v3beta1.types.Tool.Authentication):
                Optional. Authentication information required
                by the API.
            tls_config (google.cloud.dialogflowcx_v3beta1.types.Tool.TLSConfig):
                Optional. TLS configuration for the HTTPS
                verification.
        """

        text_schema: str = proto.Field(
            proto.STRING,
            number=1,
            oneof="schema",
        )
        authentication: "Tool.Authentication" = proto.Field(
            proto.MESSAGE,
            number=2,
            message="Tool.Authentication",
        )
        tls_config: "Tool.TLSConfig" = proto.Field(
            proto.MESSAGE,
            number=3,
            message="Tool.TLSConfig",
        )

    class DataStoreTool(proto.Message):
        r"""A DataStoreTool is a way to provide specifications needed to
        search a list of data stores.

        Attributes:
            data_store_connections (MutableSequence[google.cloud.dialogflowcx_v3beta1.types.DataStoreConnection]):
                Required. List of data stores to search.
            fallback_prompt (google.cloud.dialogflowcx_v3beta1.types.Tool.DataStoreTool.FallbackPrompt):
                Required. Fallback prompt configurations to
                use.
        """

        class FallbackPrompt(proto.Message):
            r"""A FallbackPrompt is a way to provide specifications for the
            Data Store fallback prompt when generating responses.

            """

        data_store_connections: MutableSequence[
            data_store_connection.DataStoreConnection
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message=data_store_connection.DataStoreConnection,
        )
        fallback_prompt: "Tool.DataStoreTool.FallbackPrompt" = proto.Field(
            proto.MESSAGE,
            number=3,
            message="Tool.DataStoreTool.FallbackPrompt",
        )

    class ExtensionTool(proto.Message):
        r"""An ExtensionTool is a way to use Vertex Extensions as a tool.

        Attributes:
            name (str):
                Required. The full name of the referenced vertex extension.
                Formats:
                ``projects/{project}/locations/{location}/extensions/{extension}``
        """

        name: str = proto.Field(
            proto.STRING,
            number=1,
        )

    class FunctionTool(proto.Message):
        r"""A Function tool describes the functions to be invoked on the
        client side.

        Attributes:
            input_schema (google.protobuf.struct_pb2.Struct):
                Optional. The JSON schema is encapsulated in a
                [google.protobuf.Struct][google.protobuf.Struct] to describe
                the input of the function. This input is a JSON object that
                contains the function's parameters as properties of the
                object.
            output_schema (google.protobuf.struct_pb2.Struct):
                Optional. The JSON schema is encapsulated in a
                [google.protobuf.Struct][google.protobuf.Struct] to describe
                the output of the function. This output is a JSON object
                that contains the function's parameters as properties of the
                object.
        """

        input_schema: struct_pb2.Struct = proto.Field(
            proto.MESSAGE,
            number=1,
            message=struct_pb2.Struct,
        )
        output_schema: struct_pb2.Struct = proto.Field(
            proto.MESSAGE,
            number=2,
            message=struct_pb2.Struct,
        )

    class Authentication(proto.Message):
        r"""Authentication information required for API calls

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            api_key_config (google.cloud.dialogflowcx_v3beta1.types.Tool.Authentication.ApiKeyConfig):
                Config for API key auth.

                This field is a member of `oneof`_ ``auth_config``.
            oauth_config (google.cloud.dialogflowcx_v3beta1.types.Tool.Authentication.OAuthConfig):
                Config for OAuth.

                This field is a member of `oneof`_ ``auth_config``.
            service_agent_auth_config (google.cloud.dialogflowcx_v3beta1.types.Tool.Authentication.ServiceAgentAuthConfig):
                Config for `Diglogflow service
                agent <https://cloud.google.com/iam/docs/service-agents#dialogflow-service-agent>`__
                auth.

                This field is a member of `oneof`_ ``auth_config``.
        """

        class RequestLocation(proto.Enum):
            r"""The location of the API key in the request.

            Values:
                REQUEST_LOCATION_UNSPECIFIED (0):
                    Default value. This value is unused.
                HEADER (1):
                    Represents the key in http header.
                QUERY_STRING (2):
                    Represents the key in query string.
            """
            REQUEST_LOCATION_UNSPECIFIED = 0
            HEADER = 1
            QUERY_STRING = 2

        class ApiKeyConfig(proto.Message):
            r"""Config for authentication with API key.

            Attributes:
                key_name (str):
                    Required. The parameter name or the header
                    name of the API key. E.g., If the API request is
                    "https://example.com/act?X-Api-Key=<API KEY>",
                    "X-Api-Key" would be the parameter name.
                api_key (str):
                    Required. The API key.
                request_location (google.cloud.dialogflowcx_v3beta1.types.Tool.Authentication.RequestLocation):
                    Required. Key location in the request.
            """

            key_name: str = proto.Field(
                proto.STRING,
                number=1,
            )
            api_key: str = proto.Field(
                proto.STRING,
                number=2,
            )
            request_location: "Tool.Authentication.RequestLocation" = proto.Field(
                proto.ENUM,
                number=3,
                enum="Tool.Authentication.RequestLocation",
            )

        class OAuthConfig(proto.Message):
            r"""Config for authentication with OAuth.

            Attributes:
                oauth_grant_type (google.cloud.dialogflowcx_v3beta1.types.Tool.Authentication.OAuthConfig.OauthGrantType):
                    Required. OAuth grant types.
                client_id (str):
                    Required. The client ID from the OAuth
                    provider.
                client_secret (str):
                    Required. The client secret from the OAuth
                    provider.
                token_endpoint (str):
                    Required. The token endpoint in the OAuth
                    provider to exchange for an access token.
            """

            class OauthGrantType(proto.Enum):
                r"""OAuth grant types. Only `client credential
                grant <https://oauth.net/2/grant-types/client-credentials>`__ is
                supported.

                Values:
                    OAUTH_GRANT_TYPE_UNSPECIFIED (0):
                        Default value. This value is unused.
                    CLIENT_CREDENTIAL (1):
                        Represents the `client credential
                        flow <https://oauth.net/2/grant-types/client-credentials>`__.
                """
                OAUTH_GRANT_TYPE_UNSPECIFIED = 0
                CLIENT_CREDENTIAL = 1

            oauth_grant_type: "Tool.Authentication.OAuthConfig.OauthGrantType" = (
                proto.Field(
                    proto.ENUM,
                    number=1,
                    enum="Tool.Authentication.OAuthConfig.OauthGrantType",
                )
            )
            client_id: str = proto.Field(
                proto.STRING,
                number=2,
            )
            client_secret: str = proto.Field(
                proto.STRING,
                number=3,
            )
            token_endpoint: str = proto.Field(
                proto.STRING,
                number=4,
            )

        class ServiceAgentAuthConfig(proto.Message):
            r"""Config for auth using `Diglogflow service
            agent <https://cloud.google.com/iam/docs/service-agents#dialogflow-service-agent>`__.

            """

        api_key_config: "Tool.Authentication.ApiKeyConfig" = proto.Field(
            proto.MESSAGE,
            number=1,
            oneof="auth_config",
            message="Tool.Authentication.ApiKeyConfig",
        )
        oauth_config: "Tool.Authentication.OAuthConfig" = proto.Field(
            proto.MESSAGE,
            number=2,
            oneof="auth_config",
            message="Tool.Authentication.OAuthConfig",
        )
        service_agent_auth_config: "Tool.Authentication.ServiceAgentAuthConfig" = (
            proto.Field(
                proto.MESSAGE,
                number=3,
                oneof="auth_config",
                message="Tool.Authentication.ServiceAgentAuthConfig",
            )
        )

    class TLSConfig(proto.Message):
        r"""The TLS configuration.

        Attributes:
            ca_certs (MutableSequence[google.cloud.dialogflowcx_v3beta1.types.Tool.TLSConfig.CACert]):
                Required. Specifies a list of allowed custom
                CA certificates for HTTPS verification.
        """

        class CACert(proto.Message):
            r"""The CA certificate.

            Attributes:
                display_name (str):
                    Required. The name of the allowed custom CA
                    certificates. This can be used to disambiguate
                    the custom CA certificates.
                cert (bytes):
                    Required. The allowed custom CA certificates
                    (in DER format) for HTTPS verification. This
                    overrides the default SSL trust store. If this
                    is empty or unspecified, Dialogflow will use
                    Google's default trust store to verify
                    certificates. N.B. Make sure the HTTPS server
                    certificates are signed with "subject alt name".
                    For instance a certificate can be self-signed
                    using the following command:

                    ::

                        openssl x509
                        -req -days 200 -in example.com.csr \
                        -signkey example.com.key \
                            -out example.com.crt \
                            -extfile <(printf
                        "\nsubjectAltName='DNS:www.example.com'")

            """

            display_name: str = proto.Field(
                proto.STRING,
                number=1,
            )
            cert: bytes = proto.Field(
                proto.BYTES,
                number=2,
            )

        ca_certs: MutableSequence["Tool.TLSConfig.CACert"] = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message="Tool.TLSConfig.CACert",
        )

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=2,
    )
    description: str = proto.Field(
        proto.STRING,
        number=3,
    )
    open_api_spec: OpenApiTool = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="specification",
        message=OpenApiTool,
    )
    data_store_spec: DataStoreTool = proto.Field(
        proto.MESSAGE,
        number=8,
        oneof="specification",
        message=DataStoreTool,
    )
    extension_spec: ExtensionTool = proto.Field(
        proto.MESSAGE,
        number=11,
        oneof="specification",
        message=ExtensionTool,
    )
    function_spec: FunctionTool = proto.Field(
        proto.MESSAGE,
        number=13,
        oneof="specification",
        message=FunctionTool,
    )
    tool_type: ToolType = proto.Field(
        proto.ENUM,
        number=12,
        enum=ToolType,
    )


class ExportToolsMetadata(proto.Message):
    r"""Metadata returned for the
    [Tools.ExportTools][google.cloud.dialogflow.cx.v3beta1.Tools.ExportTools]
    long running operation.

    """


__all__ = tuple(sorted(__protobuf__.manifest))
