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
from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.developerconnect.v1",
    manifest={
        "Connection",
        "InstallationState",
        "GitHubConfig",
        "OAuthCredential",
        "ListConnectionsRequest",
        "ListConnectionsResponse",
        "GetConnectionRequest",
        "CreateConnectionRequest",
        "UpdateConnectionRequest",
        "DeleteConnectionRequest",
        "OperationMetadata",
        "GitRepositoryLink",
        "CreateGitRepositoryLinkRequest",
        "DeleteGitRepositoryLinkRequest",
        "ListGitRepositoryLinksRequest",
        "ListGitRepositoryLinksResponse",
        "GetGitRepositoryLinkRequest",
        "FetchReadWriteTokenRequest",
        "FetchReadTokenRequest",
        "FetchReadTokenResponse",
        "FetchReadWriteTokenResponse",
        "FetchLinkableGitRepositoriesRequest",
        "FetchLinkableGitRepositoriesResponse",
        "LinkableGitRepository",
        "FetchGitHubInstallationsRequest",
        "FetchGitHubInstallationsResponse",
        "FetchGitRefsRequest",
        "FetchGitRefsResponse",
    },
)


class Connection(proto.Message):
    r"""Message describing Connection object

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        github_config (google.cloud.developerconnect_v1.types.GitHubConfig):
            Configuration for connections to github.com.

            This field is a member of `oneof`_ ``connection_config``.
        name (str):
            Identifier. The resource name of the connection, in the
            format
            ``projects/{project}/locations/{location}/connections/{connection_id}``.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. [Output only] Create timestamp
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. [Output only] Update timestamp
        delete_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. [Output only] Delete timestamp
        labels (MutableMapping[str, str]):
            Optional. Labels as key value pairs
        installation_state (google.cloud.developerconnect_v1.types.InstallationState):
            Output only. Installation state of the
            Connection.
        disabled (bool):
            Optional. If disabled is set to true,
            functionality is disabled for this connection.
            Repository based API methods and webhooks
            processing for repositories in this connection
            will be disabled.
        reconciling (bool):
            Output only. Set to true when the connection
            is being set up or updated in the background.
        annotations (MutableMapping[str, str]):
            Optional. Allows clients to store small
            amounts of arbitrary data.
        etag (str):
            Optional. This checksum is computed by the
            server based on the value of other fields, and
            may be sent on update and delete requests to
            ensure the client has an up-to-date value before
            proceeding.
        uid (str):
            Output only. A system-assigned unique
            identifier for a the GitRepositoryLink.
    """

    github_config: "GitHubConfig" = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="connection_config",
        message="GitHubConfig",
    )
    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    delete_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=11,
        message=timestamp_pb2.Timestamp,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=4,
    )
    installation_state: "InstallationState" = proto.Field(
        proto.MESSAGE,
        number=6,
        message="InstallationState",
    )
    disabled: bool = proto.Field(
        proto.BOOL,
        number=7,
    )
    reconciling: bool = proto.Field(
        proto.BOOL,
        number=8,
    )
    annotations: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=9,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=10,
    )
    uid: str = proto.Field(
        proto.STRING,
        number=12,
    )


class InstallationState(proto.Message):
    r"""Describes stage and necessary actions to be taken by the
    user to complete the installation. Used for GitHub and GitHub
    Enterprise based connections.

    Attributes:
        stage (google.cloud.developerconnect_v1.types.InstallationState.Stage):
            Output only. Current step of the installation
            process.
        message (str):
            Output only. Message of what the user should
            do next to continue the installation. Empty
            string if the installation is already complete.
        action_uri (str):
            Output only. Link to follow for next action.
            Empty string if the installation is already
            complete.
    """

    class Stage(proto.Enum):
        r"""Stage of the installation process.

        Values:
            STAGE_UNSPECIFIED (0):
                No stage specified.
            PENDING_CREATE_APP (1):
                Only for GitHub Enterprise. An App creation
                has been requested. The user needs to confirm
                the creation in their GitHub enterprise host.
            PENDING_USER_OAUTH (2):
                User needs to authorize the GitHub (or
                Enterprise) App via OAuth.
            PENDING_INSTALL_APP (3):
                User needs to follow the link to install the
                GitHub (or Enterprise) App.
            COMPLETE (10):
                Installation process has been completed.
        """
        STAGE_UNSPECIFIED = 0
        PENDING_CREATE_APP = 1
        PENDING_USER_OAUTH = 2
        PENDING_INSTALL_APP = 3
        COMPLETE = 10

    stage: Stage = proto.Field(
        proto.ENUM,
        number=1,
        enum=Stage,
    )
    message: str = proto.Field(
        proto.STRING,
        number=2,
    )
    action_uri: str = proto.Field(
        proto.STRING,
        number=3,
    )


class GitHubConfig(proto.Message):
    r"""Configuration for connections to github.com.

    Attributes:
        github_app (google.cloud.developerconnect_v1.types.GitHubConfig.GitHubApp):
            Required. Immutable. The GitHub Application
            that was installed to the GitHub user or
            organization.
        authorizer_credential (google.cloud.developerconnect_v1.types.OAuthCredential):
            Optional. OAuth credential of the account
            that authorized the GitHub App. It is
            recommended to use a robot account instead of a
            human user account. The OAuth token must be tied
            to the GitHub App of this config.
        app_installation_id (int):
            Optional. GitHub App installation id.
        installation_uri (str):
            Output only. The URI to navigate to in order
            to manage the installation associated with this
            GitHubConfig.
    """

    class GitHubApp(proto.Enum):
        r"""Represents the various GitHub Applications that can be
        installed to a GitHub user or organization and used with
        Developer Connect.

        Values:
            GIT_HUB_APP_UNSPECIFIED (0):
                GitHub App not specified.
            DEVELOPER_CONNECT (1):
                The Developer Connect GitHub Application.
            FIREBASE (2):
                The Firebase GitHub Application.
        """
        GIT_HUB_APP_UNSPECIFIED = 0
        DEVELOPER_CONNECT = 1
        FIREBASE = 2

    github_app: GitHubApp = proto.Field(
        proto.ENUM,
        number=1,
        enum=GitHubApp,
    )
    authorizer_credential: "OAuthCredential" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="OAuthCredential",
    )
    app_installation_id: int = proto.Field(
        proto.INT64,
        number=3,
    )
    installation_uri: str = proto.Field(
        proto.STRING,
        number=4,
    )


class OAuthCredential(proto.Message):
    r"""Represents an OAuth token of the account that authorized the
    Connection, and associated metadata.

    Attributes:
        oauth_token_secret_version (str):
            Required. A SecretManager resource containing the OAuth
            token that authorizes the connection. Format:
            ``projects/*/secrets/*/versions/*``.
        username (str):
            Output only. The username associated with
            this token.
    """

    oauth_token_secret_version: str = proto.Field(
        proto.STRING,
        number=1,
    )
    username: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ListConnectionsRequest(proto.Message):
    r"""Message for requesting list of Connections

    Attributes:
        parent (str):
            Required. Parent value for
            ListConnectionsRequest
        page_size (int):
            Optional. Requested page size. Server may
            return fewer items than requested. If
            unspecified, server will pick an appropriate
            default.
        page_token (str):
            Optional. A token identifying a page of
            results the server should return.
        filter (str):
            Optional. Filtering results
        order_by (str):
            Optional. Hint for how to order the results
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


class ListConnectionsResponse(proto.Message):
    r"""Message for response to listing Connections

    Attributes:
        connections (MutableSequence[google.cloud.developerconnect_v1.types.Connection]):
            The list of Connection
        next_page_token (str):
            A token identifying a page of results the
            server should return.
        unreachable (MutableSequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    connections: MutableSequence["Connection"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Connection",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class GetConnectionRequest(proto.Message):
    r"""Message for getting a Connection

    Attributes:
        name (str):
            Required. Name of the resource
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateConnectionRequest(proto.Message):
    r"""Message for creating a Connection

    Attributes:
        parent (str):
            Required. Value for parent.
        connection_id (str):
            Required. Id of the requesting object If auto-generating Id
            server-side, remove this field and connection_id from the
            method_signature of Create RPC
        connection (google.cloud.developerconnect_v1.types.Connection):
            Required. The resource being created
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server will
            know to ignore the request if it has already
            been completed. The server will guarantee that
            for at least 60 minutes since the first request.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.

            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
        validate_only (bool):
            Optional. If set, validate the request, but
            do not actually post it.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    connection_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    connection: "Connection" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="Connection",
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=4,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=5,
    )


class UpdateConnectionRequest(proto.Message):
    r"""Message for updating a Connection

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Field mask is used to specify the fields to be
            overwritten in the Connection resource by the update. The
            fields specified in the update_mask are relative to the
            resource, not the full request. A field will be overwritten
            if it is in the mask. If the user does not provide a mask
            then all fields will be overwritten.
        connection (google.cloud.developerconnect_v1.types.Connection):
            Required. The resource being updated
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server will
            know to ignore the request if it has already
            been completed. The server will guarantee that
            for at least 60 minutes since the first request.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.

            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
        allow_missing (bool):
            Optional. If set to true, and the connection is not found a
            new connection will be created. In this situation
            ``update_mask`` is ignored. The creation will succeed only
            if the input connection has all the necessary information
            (e.g a github_config with both user_oauth_token and
            installation_id properties).
        validate_only (bool):
            Optional. If set, validate the request, but
            do not actually post it.
    """

    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=1,
        message=field_mask_pb2.FieldMask,
    )
    connection: "Connection" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Connection",
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    allow_missing: bool = proto.Field(
        proto.BOOL,
        number=4,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=5,
    )


class DeleteConnectionRequest(proto.Message):
    r"""Message for deleting a Connection

    Attributes:
        name (str):
            Required. Name of the resource
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server will
            know to ignore the request if it has already
            been completed. The server will guarantee that
            for at least 60 minutes after the first request.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.

            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
        validate_only (bool):
            Optional. If set, validate the request, but
            do not actually post it.
        etag (str):
            Optional. The current etag of the Connection.
            If an etag is provided and does not match the
            current etag of the Connection, deletion will be
            blocked and an ABORTED error will be returned.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=3,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=4,
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
            cancelled successfully have [Operation.error][] value with a
            [google.rpc.Status.code][google.rpc.Status.code] of 1,
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


class GitRepositoryLink(proto.Message):
    r"""Message describing the GitRepositoryLink object

    Attributes:
        name (str):
            Identifier. Resource name of the repository, in the format
            ``projects/*/locations/*/connections/*/gitRepositoryLinks/*``.
        clone_uri (str):
            Required. Git Clone URI.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. [Output only] Create timestamp
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. [Output only] Update timestamp
        delete_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. [Output only] Delete timestamp
        labels (MutableMapping[str, str]):
            Optional. Labels as key value pairs
        etag (str):
            Optional. This checksum is computed by the
            server based on the value of other fields, and
            may be sent on update and delete requests to
            ensure the client has an up-to-date value before
            proceeding.
        reconciling (bool):
            Output only. Set to true when the connection
            is being set up or updated in the background.
        annotations (MutableMapping[str, str]):
            Optional. Allows clients to store small
            amounts of arbitrary data.
        uid (str):
            Output only. A system-assigned unique
            identifier for a the GitRepositoryLink.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    clone_uri: str = proto.Field(
        proto.STRING,
        number=2,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    delete_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=6,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=7,
    )
    reconciling: bool = proto.Field(
        proto.BOOL,
        number=8,
    )
    annotations: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=9,
    )
    uid: str = proto.Field(
        proto.STRING,
        number=10,
    )


class CreateGitRepositoryLinkRequest(proto.Message):
    r"""Message for creating a GitRepositoryLink

    Attributes:
        parent (str):
            Required. Value for parent.
        git_repository_link (google.cloud.developerconnect_v1.types.GitRepositoryLink):
            Required. The resource being created
        git_repository_link_id (str):
            Required. The ID to use for the repository, which will
            become the final component of the repository's resource
            name. This ID should be unique in the connection. Allows
            alphanumeric characters and any of -._~%!$&'()*+,;=@.
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server will
            know to ignore the request if it has already
            been completed. The server will guarantee that
            for at least 60 minutes since the first request.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.

            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
        validate_only (bool):
            Optional. If set, validate the request, but
            do not actually post it.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    git_repository_link: "GitRepositoryLink" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="GitRepositoryLink",
    )
    git_repository_link_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=4,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=5,
    )


class DeleteGitRepositoryLinkRequest(proto.Message):
    r"""Message for deleting a GitRepositoryLink

    Attributes:
        name (str):
            Required. Name of the resource
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server will
            know to ignore the request if it has already
            been completed. The server will guarantee that
            for at least 60 minutes after the first request.

            For example, consider a situation where you make
            an initial request and the request times out. If
            you make the request again with the same request
            ID, the server can check if original operation
            with the same request ID was received, and if
            so, will ignore the second request. This
            prevents clients from accidentally creating
            duplicate commitments.

            The request ID must be a valid UUID with the
            exception that zero UUID is not supported
            (00000000-0000-0000-0000-000000000000).
        validate_only (bool):
            Optional. If set, validate the request, but
            do not actually post it.
        etag (str):
            Optional. This checksum is computed by the
            server based on the value of other fields, and
            may be sent on update and delete requests to
            ensure the client has an up-to-date value before
            proceeding.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=3,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=4,
    )


class ListGitRepositoryLinksRequest(proto.Message):
    r"""Message for requesting a list of GitRepositoryLinks

    Attributes:
        parent (str):
            Required. Parent value for
            ListGitRepositoryLinksRequest
        page_size (int):
            Optional. Requested page size. Server may
            return fewer items than requested. If
            unspecified, server will pick an appropriate
            default.
        page_token (str):
            Optional. A token identifying a page of
            results the server should return.
        filter (str):
            Optional. Filtering results
        order_by (str):
            Optional. Hint for how to order the results
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


class ListGitRepositoryLinksResponse(proto.Message):
    r"""Message for response to listing GitRepositoryLinks

    Attributes:
        git_repository_links (MutableSequence[google.cloud.developerconnect_v1.types.GitRepositoryLink]):
            The list of GitRepositoryLinks
        next_page_token (str):
            A token identifying a page of results the
            server should return.
        unreachable (MutableSequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    git_repository_links: MutableSequence["GitRepositoryLink"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="GitRepositoryLink",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class GetGitRepositoryLinkRequest(proto.Message):
    r"""Message for getting a GitRepositoryLink

    Attributes:
        name (str):
            Required. Name of the resource
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class FetchReadWriteTokenRequest(proto.Message):
    r"""Message for fetching SCM read/write token.

    Attributes:
        git_repository_link (str):
            Required. The resource name of the gitRepositoryLink in the
            format
            ``projects/*/locations/*/connections/*/gitRepositoryLinks/*``.
    """

    git_repository_link: str = proto.Field(
        proto.STRING,
        number=1,
    )


class FetchReadTokenRequest(proto.Message):
    r"""Message for fetching SCM read token.

    Attributes:
        git_repository_link (str):
            Required. The resource name of the gitRepositoryLink in the
            format
            ``projects/*/locations/*/connections/*/gitRepositoryLinks/*``.
    """

    git_repository_link: str = proto.Field(
        proto.STRING,
        number=1,
    )


class FetchReadTokenResponse(proto.Message):
    r"""Message for responding to get read token.

    Attributes:
        token (str):
            The token content.
        expiration_time (google.protobuf.timestamp_pb2.Timestamp):
            Expiration timestamp. Can be empty if unknown
            or non-expiring.
        git_username (str):
            The git_username to specify when making a git clone with the
            token. For example, for GitHub GitRepositoryLinks, this
            would be "x-access-token".
    """

    token: str = proto.Field(
        proto.STRING,
        number=1,
    )
    expiration_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    git_username: str = proto.Field(
        proto.STRING,
        number=3,
    )


class FetchReadWriteTokenResponse(proto.Message):
    r"""Message for responding to get read/write token.

    Attributes:
        token (str):
            The token content.
        expiration_time (google.protobuf.timestamp_pb2.Timestamp):
            Expiration timestamp. Can be empty if unknown
            or non-expiring.
        git_username (str):
            The git_username to specify when making a git clone with the
            token. For example, for GitHub GitRepositoryLinks, this
            would be "x-access-token".
    """

    token: str = proto.Field(
        proto.STRING,
        number=1,
    )
    expiration_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    git_username: str = proto.Field(
        proto.STRING,
        number=3,
    )


class FetchLinkableGitRepositoriesRequest(proto.Message):
    r"""Request message for FetchLinkableGitRepositoriesRequest.

    Attributes:
        connection (str):
            Required. The name of the Connection. Format:
            ``projects/*/locations/*/connections/*``.
        page_size (int):
            Optional. Number of results to return in the
            list. Defaults to 20.
        page_token (str):
            Optional. Page start.
    """

    connection: str = proto.Field(
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


class FetchLinkableGitRepositoriesResponse(proto.Message):
    r"""Response message for FetchLinkableGitRepositories.

    Attributes:
        linkable_git_repositories (MutableSequence[google.cloud.developerconnect_v1.types.LinkableGitRepository]):
            The git repositories that can be linked to
            the connection.
        next_page_token (str):
            A token identifying a page of results the
            server should return.
    """

    @property
    def raw_page(self):
        return self

    linkable_git_repositories: MutableSequence[
        "LinkableGitRepository"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="LinkableGitRepository",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class LinkableGitRepository(proto.Message):
    r"""LinkableGitRepository represents a git repository that can be
    linked to a connection.

    Attributes:
        clone_uri (str):
            The clone uri of the repository.
    """

    clone_uri: str = proto.Field(
        proto.STRING,
        number=1,
    )


class FetchGitHubInstallationsRequest(proto.Message):
    r"""Request for fetching github installations.

    Attributes:
        connection (str):
            Required. The resource name of the connection in the format
            ``projects/*/locations/*/connections/*``.
    """

    connection: str = proto.Field(
        proto.STRING,
        number=1,
    )


class FetchGitHubInstallationsResponse(proto.Message):
    r"""Response of fetching github installations.

    Attributes:
        installations (MutableSequence[google.cloud.developerconnect_v1.types.FetchGitHubInstallationsResponse.Installation]):
            List of installations available to the OAuth
            user (for github.com) or all the installations
            (for GitHub enterprise).
    """

    class Installation(proto.Message):
        r"""Represents an installation of the GitHub App.

        Attributes:
            id (int):
                ID of the installation in GitHub.
            name (str):
                Name of the GitHub user or organization that
                owns this installation.
            type_ (str):
                Either "user" or "organization".
        """

        id: int = proto.Field(
            proto.INT64,
            number=1,
        )
        name: str = proto.Field(
            proto.STRING,
            number=2,
        )
        type_: str = proto.Field(
            proto.STRING,
            number=3,
        )

    installations: MutableSequence[Installation] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=Installation,
    )


class FetchGitRefsRequest(proto.Message):
    r"""Request for fetching git refs.

    Attributes:
        git_repository_link (str):
            Required. The resource name of GitRepositoryLink in the
            format
            ``projects/*/locations/*/connections/*/gitRepositoryLinks/*``.
        ref_type (google.cloud.developerconnect_v1.types.FetchGitRefsRequest.RefType):
            Required. Type of refs to fetch.
        page_size (int):
            Optional. Number of results to return in the
            list. Default to 20.
        page_token (str):
            Optional. Page start.
    """

    class RefType(proto.Enum):
        r"""Type of refs.

        Values:
            REF_TYPE_UNSPECIFIED (0):
                No type specified.
            TAG (1):
                To fetch tags.
            BRANCH (2):
                To fetch branches.
        """
        REF_TYPE_UNSPECIFIED = 0
        TAG = 1
        BRANCH = 2

    git_repository_link: str = proto.Field(
        proto.STRING,
        number=1,
    )
    ref_type: RefType = proto.Field(
        proto.ENUM,
        number=2,
        enum=RefType,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=4,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=5,
    )


class FetchGitRefsResponse(proto.Message):
    r"""Response for fetching git refs.

    Attributes:
        ref_names (MutableSequence[str]):
            Name of the refs fetched.
        next_page_token (str):
            A token identifying a page of results the
            server should return.
    """

    @property
    def raw_page(self):
        return self

    ref_names: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=1,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
