# -*- coding: utf-8 -*-
# Copyright 2026 Google LLC
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

import google.protobuf.struct_pb2 as struct_pb2  # type: ignore
import google.protobuf.timestamp_pb2 as timestamp_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.geminidataanalytics.v1alpha",
    manifest={
        "TaskState",
        "Role",
        "SendMessageConfiguration",
        "A2ATask",
        "TaskStatus",
        "Part",
        "FilePart",
        "DataPart",
        "A2AMessage",
        "A2AArtifact",
        "TaskStatusUpdateEvent",
        "TaskArtifactUpdateEvent",
        "PushNotificationConfig",
        "AuthenticationInfo",
        "AgentInterface",
        "AgentCard",
        "AgentProvider",
        "AgentCapabilities",
        "AgentExtension",
        "AgentSkill",
        "AgentCardSignature",
        "StringList",
        "Security",
        "SecurityScheme",
        "APIKeySecurityScheme",
        "HTTPAuthSecurityScheme",
        "OAuth2SecurityScheme",
        "OpenIdConnectSecurityScheme",
        "MutualTlsSecurityScheme",
        "OAuthFlows",
        "AuthorizationCodeOAuthFlow",
        "ClientCredentialsOAuthFlow",
        "ImplicitOAuthFlow",
        "PasswordOAuthFlow",
        "SendMessageRequest",
        "GetAgentCardRequest",
        "SendMessageResponse",
        "StreamResponse",
    },
)


class TaskState(proto.Enum):
    r"""The set of states a Task can be in.

    Values:
        TASK_STATE_UNSPECIFIED (0):
            Default unspecified task state.
        TASK_STATE_SUBMITTED (1):
            Represents the status that acknowledges a
            task is created.
        TASK_STATE_WORKING (2):
            Represents the status that a task is
            currently in progress.
        TASK_STATE_COMPLETED (3):
            Represents the status that a task is
            completed. This is a terminal state.
        TASK_STATE_FAILED (4):
            Represents the status that a task has failed.
            This is a terminal state.
        TASK_STATE_CANCELLED (5):
            Represents the status that a task was
            cancelled before it finished. This is a terminal
            state.
        TASK_STATE_INPUT_REQUIRED (6):
            Represents the status that the task requires
            information to complete. This is an interrupted
            state.
        TASK_STATE_REJECTED (7):
            Represents the status that a task has been
            rejected by the agent. This is a terminal state.
        TASK_STATE_AUTH_REQUIRED (8):
            Represents the state that some authentication
            is needed from the upstream client.
    """

    TASK_STATE_UNSPECIFIED = 0
    TASK_STATE_SUBMITTED = 1
    TASK_STATE_WORKING = 2
    TASK_STATE_COMPLETED = 3
    TASK_STATE_FAILED = 4
    TASK_STATE_CANCELLED = 5
    TASK_STATE_INPUT_REQUIRED = 6
    TASK_STATE_REJECTED = 7
    TASK_STATE_AUTH_REQUIRED = 8


class Role(proto.Enum):
    r"""Role indicates the sender of a message.

    Values:
        ROLE_UNSPECIFIED (0):
            Default unspecified role.
        ROLE_USER (1):
            USER role refers to communication from the
            client to the server.
        ROLE_AGENT (2):
            AGENT role refers to communication from the
            server to the client.
    """

    ROLE_UNSPECIFIED = 0
    ROLE_USER = 1
    ROLE_AGENT = 2


class SendMessageConfiguration(proto.Message):
    r"""Configuration of a send message request.

    Attributes:
        accepted_output_modes (MutableSequence[str]):
            Optional. The output modes that the agent is
            expected to respond with.
        push_notification (google.cloud.geminidataanalytics_v1alpha.types.PushNotificationConfig):
            Optional. A configuration of a webhook that
            can be used to receive updates.
        history_length (int):
            Optional. The maximum number of messages to
            include in the history. If 0, the history will
            be unlimited.
        blocking (bool):
            Optional. If true, the message will be
            blocking until the task is completed. If false,
            the task will be returned immediately.
    """

    accepted_output_modes: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=1,
    )
    push_notification: "PushNotificationConfig" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="PushNotificationConfig",
    )
    history_length: int = proto.Field(
        proto.INT32,
        number=3,
    )
    blocking: bool = proto.Field(
        proto.BOOL,
        number=4,
    )


class A2ATask(proto.Message):
    r"""A2ATask is the core unit of action for A2A. It has a current
    status and when results are created for the task they are stored
    in the artifact. If there are multiple turns for a task, these
    are stored in history.

    Attributes:
        id (str):
            Optional. Unique identifier (e.g. UUID) for
            the task, generated by the server for a new
            task.
        context_id (str):
            Optional. Unique identifier (e.g. UUID) for
            the contextual collection of interactions (tasks
            and messages). Created by the A2A server.
        status (google.cloud.geminidataanalytics_v1alpha.types.TaskStatus):
            Optional. The current status of a Task,
            including state and a message.
        artifacts (MutableSequence[google.cloud.geminidataanalytics_v1alpha.types.A2AArtifact]):
            Optional. A set of output artifacts for a
            Task.
        history (MutableSequence[google.cloud.geminidataanalytics_v1alpha.types.A2AMessage]):
            Optional. The history of interactions from a
            task.
        metadata (google.protobuf.struct_pb2.Struct):
            Optional. A key/value object to store custom
            metadata about a task.
    """

    id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    context_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    status: "TaskStatus" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="TaskStatus",
    )
    artifacts: MutableSequence["A2AArtifact"] = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message="A2AArtifact",
    )
    history: MutableSequence["A2AMessage"] = proto.RepeatedField(
        proto.MESSAGE,
        number=5,
        message="A2AMessage",
    )
    metadata: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=6,
        message=struct_pb2.Struct,
    )


class TaskStatus(proto.Message):
    r"""A container for the status of a task.

    Attributes:
        state (google.cloud.geminidataanalytics_v1alpha.types.TaskState):
            Output only. The current state of this task.
        update (google.cloud.geminidataanalytics_v1alpha.types.A2AMessage):
            Optional. A message associated with the
            status.
        timestamp (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Timestamp when the status was
            recorded.
    """

    state: "TaskState" = proto.Field(
        proto.ENUM,
        number=1,
        enum="TaskState",
    )
    update: "A2AMessage" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="A2AMessage",
    )
    timestamp: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )


class Part(proto.Message):
    r"""Part represents a container for a section of communication
    content. Parts can be purely textual, some sort of file (image,
    video, etc) or a structured data blob (i.e. JSON).

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        text (str):
            Plain text content.

            This field is a member of `oneof`_ ``part``.
        file (google.cloud.geminidataanalytics_v1alpha.types.FilePart):
            File content payload.

            This field is a member of `oneof`_ ``part``.
        data (google.cloud.geminidataanalytics_v1alpha.types.DataPart):
            Structured data content payload.

            This field is a member of `oneof`_ ``part``.
        metadata (google.protobuf.struct_pb2.Struct):
            Optional. Metadata associated with the part.
    """

    text: str = proto.Field(
        proto.STRING,
        number=1,
        oneof="part",
    )
    file: "FilePart" = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="part",
        message="FilePart",
    )
    data: "DataPart" = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="part",
        message="DataPart",
    )
    metadata: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=4,
        message=struct_pb2.Struct,
    )


class FilePart(proto.Message):
    r"""FilePart represents the different ways files can be provided.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        file_with_uri (str):
            The URI pointing to the file.

            This field is a member of `oneof`_ ``file``.
        file_with_bytes (bytes):
            The raw bytes of the file.

            This field is a member of `oneof`_ ``file``.
        mime_type (str):
            Optional. The MIME type of the file.
        name (str):
            Optional. The name of the file.
    """

    file_with_uri: str = proto.Field(
        proto.STRING,
        number=1,
        oneof="file",
    )
    file_with_bytes: bytes = proto.Field(
        proto.BYTES,
        number=2,
        oneof="file",
    )
    mime_type: str = proto.Field(
        proto.STRING,
        number=3,
    )
    name: str = proto.Field(
        proto.STRING,
        number=4,
    )


class DataPart(proto.Message):
    r"""DataPart represents a structured blob. This is most commonly
    a JSON payload.

    Attributes:
        data (google.protobuf.struct_pb2.Struct):
            Optional. The structured data payload.
    """

    data: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=1,
        message=struct_pb2.Struct,
    )


class A2AMessage(proto.Message):
    r"""A2AMessage is one unit of communication between client and
    server.

    Attributes:
        message_id (str):
            Optional. The unique identifier (e.g. UUID)
            of the message.
        context_id (str):
            Optional. The context id of the message.
        task_id (str):
            Optional. The task id of the message.
        role (google.cloud.geminidataanalytics_v1alpha.types.Role):
            Optional. A role for the message.
        content (MutableSequence[google.cloud.geminidataanalytics_v1alpha.types.Part]):
            Optional. Content is the container of the
            message content.
        metadata (google.protobuf.struct_pb2.Struct):
            Optional. Any optional metadata to provide
            along with the message.
        extensions (MutableSequence[str]):
            Optional. The URIs of extensions that are
            present or contributed to this Message.
    """

    message_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    context_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    task_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    role: "Role" = proto.Field(
        proto.ENUM,
        number=4,
        enum="Role",
    )
    content: MutableSequence["Part"] = proto.RepeatedField(
        proto.MESSAGE,
        number=5,
        message="Part",
    )
    metadata: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=6,
        message=struct_pb2.Struct,
    )
    extensions: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=7,
    )


class A2AArtifact(proto.Message):
    r"""A2AArtifact is the container for task completed results.

    Attributes:
        artifact_id (str):
            Optional. Unique identifier (e.g. UUID) for
            the artifact.
        name (str):
            Optional. A human readable name for the
            artifact.
        description (str):
            Optional. A human readable description of the
            artifact, optional.
        parts (MutableSequence[google.cloud.geminidataanalytics_v1alpha.types.Part]):
            Optional. The content of the artifact.
        metadata (google.protobuf.struct_pb2.Struct):
            Optional. Optional metadata included with the
            artifact.
        extensions (MutableSequence[str]):
            Optional. The URIs of extensions that are
            present or contributed to this Artifact.
    """

    artifact_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    name: str = proto.Field(
        proto.STRING,
        number=3,
    )
    description: str = proto.Field(
        proto.STRING,
        number=4,
    )
    parts: MutableSequence["Part"] = proto.RepeatedField(
        proto.MESSAGE,
        number=5,
        message="Part",
    )
    metadata: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=6,
        message=struct_pb2.Struct,
    )
    extensions: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=7,
    )


class TaskStatusUpdateEvent(proto.Message):
    r"""TaskStatusUpdateEvent is a delta event on a task indicating
    that a task has changed.

    Attributes:
        task_id (str):
            Optional. The id of the task that is changed.
        context_id (str):
            Optional. The id of the context that the task
            belongs to.
        status (google.cloud.geminidataanalytics_v1alpha.types.TaskStatus):
            Optional. The new status of the task.
        final (bool):
            Optional. Whether this is the last status
            update expected for this task.
        metadata (google.protobuf.struct_pb2.Struct):
            Optional. Optional metadata to associate with
            the task update.
    """

    task_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    context_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    status: "TaskStatus" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="TaskStatus",
    )
    final: bool = proto.Field(
        proto.BOOL,
        number=4,
    )
    metadata: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=5,
        message=struct_pb2.Struct,
    )


class TaskArtifactUpdateEvent(proto.Message):
    r"""TaskArtifactUpdateEvent represents a task delta where an
    artifact has been generated.

    Attributes:
        task_id (str):
            Optional. The id of the task for this
            artifact.
        context_id (str):
            Optional. The id of the context that this
            task belongs to.
        artifact (google.cloud.geminidataanalytics_v1alpha.types.A2AArtifact):
            Optional. The artifact itself.
        append (bool):
            Optional. Whether this should be appended to
            a prior one produced.
        last_chunk (bool):
            Optional. Whether this represents the last
            part of an artifact.
        metadata (google.protobuf.struct_pb2.Struct):
            Optional. Optional metadata associated with
            the artifact update.
    """

    task_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    context_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    artifact: "A2AArtifact" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="A2AArtifact",
    )
    append: bool = proto.Field(
        proto.BOOL,
        number=4,
    )
    last_chunk: bool = proto.Field(
        proto.BOOL,
        number=5,
    )
    metadata: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=6,
        message=struct_pb2.Struct,
    )


class PushNotificationConfig(proto.Message):
    r"""Configuration for setting up push notifications for task
    updates.

    Attributes:
        id (str):
            Optional. A unique identifier (e.g. UUID) for
            this push notification.
        url (str):
            Optional. Url to send the notification to.
        token (str):
            Optional. Token unique for this task/session.
        authentication (google.cloud.geminidataanalytics_v1alpha.types.AuthenticationInfo):
            Optional. Information about the
            authentication to send with the notification.
    """

    id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    url: str = proto.Field(
        proto.STRING,
        number=2,
    )
    token: str = proto.Field(
        proto.STRING,
        number=3,
    )
    authentication: "AuthenticationInfo" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="AuthenticationInfo",
    )


class AuthenticationInfo(proto.Message):
    r"""Defines authentication details, used for push notifications.

    Attributes:
        schemes (MutableSequence[str]):
            Optional. Supported authentication schemes -
            e.g. Basic, Bearer, etc.
        credentials (str):
            Optional. Optional credentials.
    """

    schemes: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=1,
    )
    credentials: str = proto.Field(
        proto.STRING,
        number=2,
    )


class AgentInterface(proto.Message):
    r"""Defines additional transport information for the agent.

    Attributes:
        url (str):
            Optional. The url this interface is found at.
        transport (str):
            Optional. The transport supported at this
            url.
        tenant (str):
            Optional. Tenant to be set in the request
            when calling the agent.
    """

    url: str = proto.Field(
        proto.STRING,
        number=1,
    )
    transport: str = proto.Field(
        proto.STRING,
        number=2,
    )
    tenant: str = proto.Field(
        proto.STRING,
        number=3,
    )


class AgentCard(proto.Message):
    r"""AgentCard conveys key information about an agent.

    Attributes:
        protocol_version (str):
            Optional. The version of the A2A protocol
            this agent supports.
        name (str):
            Optional. A human readable name for the
            agent.
        description (str):
            Optional. A description of the agent's domain
            of action/solution space.
        url (str):
            Optional. A URL to the address the agent is
            hosted at.
        preferred_transport (str):
            Optional. The transport of the preferred
            endpoint. If empty, defaults to JSONRPC.
        additional_interfaces (MutableSequence[google.cloud.geminidataanalytics_v1alpha.types.AgentInterface]):
            Optional. Announcement of additional
            supported transports.
        provider (google.cloud.geminidataanalytics_v1alpha.types.AgentProvider):
            Optional. The service provider of the agent.
        version (str):
            Optional. The version of the agent.
        documentation_url (str):
            Optional. A url to provide additional
            documentation about the agent.
        capabilities (google.cloud.geminidataanalytics_v1alpha.types.AgentCapabilities):
            Optional. A2A Capability set supported by the
            agent.
        security_schemes (MutableMapping[str, google.cloud.geminidataanalytics_v1alpha.types.SecurityScheme]):
            The security scheme details used for
            authenticating with this agent.
        security (MutableSequence[google.cloud.geminidataanalytics_v1alpha.types.Security]):
            Security requirements for contacting the
            agent.
        default_input_modes (MutableSequence[str]):
            Optional. The set of interaction modes that
            the agent supports across all skills.
        default_output_modes (MutableSequence[str]):
            Optional. The mime types supported as outputs
            from this agent.
        skills (MutableSequence[google.cloud.geminidataanalytics_v1alpha.types.AgentSkill]):
            Optional. Skills represent a unit of ability
            an agent can perform.
        supports_authenticated_extended_card (bool):
            Optional. Whether the agent supports
            providing an extended agent card when the user
            is authenticated.
        signatures (MutableSequence[google.cloud.geminidataanalytics_v1alpha.types.AgentCardSignature]):
            Optional. JSON Web Signatures computed for
            this AgentCard.
        icon_url (str):
            Optional. An optional URL to an icon for the
            agent.
    """

    protocol_version: str = proto.Field(
        proto.STRING,
        number=16,
    )
    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    description: str = proto.Field(
        proto.STRING,
        number=2,
    )
    url: str = proto.Field(
        proto.STRING,
        number=3,
    )
    preferred_transport: str = proto.Field(
        proto.STRING,
        number=14,
    )
    additional_interfaces: MutableSequence["AgentInterface"] = proto.RepeatedField(
        proto.MESSAGE,
        number=15,
        message="AgentInterface",
    )
    provider: "AgentProvider" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="AgentProvider",
    )
    version: str = proto.Field(
        proto.STRING,
        number=5,
    )
    documentation_url: str = proto.Field(
        proto.STRING,
        number=6,
    )
    capabilities: "AgentCapabilities" = proto.Field(
        proto.MESSAGE,
        number=7,
        message="AgentCapabilities",
    )
    security_schemes: MutableMapping[str, "SecurityScheme"] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=8,
        message="SecurityScheme",
    )
    security: MutableSequence["Security"] = proto.RepeatedField(
        proto.MESSAGE,
        number=9,
        message="Security",
    )
    default_input_modes: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=10,
    )
    default_output_modes: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=11,
    )
    skills: MutableSequence["AgentSkill"] = proto.RepeatedField(
        proto.MESSAGE,
        number=12,
        message="AgentSkill",
    )
    supports_authenticated_extended_card: bool = proto.Field(
        proto.BOOL,
        number=13,
    )
    signatures: MutableSequence["AgentCardSignature"] = proto.RepeatedField(
        proto.MESSAGE,
        number=17,
        message="AgentCardSignature",
    )
    icon_url: str = proto.Field(
        proto.STRING,
        number=18,
    )


class AgentProvider(proto.Message):
    r"""Represents information about the service provider of an
    agent.

    Attributes:
        url (str):
            Optional. The provider's reference url.
        organization (str):
            Optional. The provider's organization name.
    """

    url: str = proto.Field(
        proto.STRING,
        number=1,
    )
    organization: str = proto.Field(
        proto.STRING,
        number=2,
    )


class AgentCapabilities(proto.Message):
    r"""Defines the A2A feature set supported by the agent.

    Attributes:
        streaming (bool):
            Optional. If the agent will support streaming
            responses.
        push_notifications (bool):
            Optional. If the agent can send push
            notifications to the client's webhook.
        extensions (MutableSequence[google.cloud.geminidataanalytics_v1alpha.types.AgentExtension]):
            Optional. Extensions supported by this agent.
    """

    streaming: bool = proto.Field(
        proto.BOOL,
        number=1,
    )
    push_notifications: bool = proto.Field(
        proto.BOOL,
        number=2,
    )
    extensions: MutableSequence["AgentExtension"] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message="AgentExtension",
    )


class AgentExtension(proto.Message):
    r"""A declaration of an extension supported by an Agent.

    Attributes:
        uri (str):
            Optional. The URI of the extension.
        description (str):
            Optional. A description of how this agent
            uses this extension.
        required (bool):
            Optional. Whether the client must follow
            specific requirements of the extension.
        params (google.protobuf.struct_pb2.Struct):
            Optional. Optional configuration for the
            extension.
    """

    uri: str = proto.Field(
        proto.STRING,
        number=1,
    )
    description: str = proto.Field(
        proto.STRING,
        number=2,
    )
    required: bool = proto.Field(
        proto.BOOL,
        number=3,
    )
    params: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=4,
        message=struct_pb2.Struct,
    )


class AgentSkill(proto.Message):
    r"""AgentSkill represents a unit of action/solution that the
    agent can perform.

    Attributes:
        id (str):
            Optional. Unique identifier of the skill
            within this agent.
        name (str):
            Optional. A human readable name for the
            skill.
        description (str):
            Optional. A human readable description of the
            skill details and behaviors.
        tags (MutableSequence[str]):
            Optional. A set of tags for the skill to
            enhance categorization/utilization.
        examples (MutableSequence[str]):
            Optional. A set of example queries that this
            skill is designed to address.
        input_modes (MutableSequence[str]):
            Optional. Possible input modalities
            supported.
        output_modes (MutableSequence[str]):
            Optional. Possible output modalities
            produced.
        security (MutableSequence[google.cloud.geminidataanalytics_v1alpha.types.Security]):
            Security schemes necessary for the agent to
            leverage this skill.
    """

    id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    name: str = proto.Field(
        proto.STRING,
        number=2,
    )
    description: str = proto.Field(
        proto.STRING,
        number=3,
    )
    tags: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=4,
    )
    examples: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=5,
    )
    input_modes: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=6,
    )
    output_modes: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=7,
    )
    security: MutableSequence["Security"] = proto.RepeatedField(
        proto.MESSAGE,
        number=8,
        message="Security",
    )


class AgentCardSignature(proto.Message):
    r"""AgentCardSignature represents a JWS signature of an
    AgentCard.

    Attributes:
        protected (str):
            Required. The protected JWS header for the
            signature. Base64url-encoded.
        signature (str):
            Required. The computed signature,
            base64url-encoded.
        header (google.protobuf.struct_pb2.Struct):
            Optional. The unprotected JWS header values.
    """

    protected: str = proto.Field(
        proto.STRING,
        number=1,
    )
    signature: str = proto.Field(
        proto.STRING,
        number=2,
    )
    header: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=3,
        message=struct_pb2.Struct,
    )


class StringList(proto.Message):
    r"""StringList is a wrapper for a repeated list of strings.

    Attributes:
        list_ (MutableSequence[str]):
            The list of strings.
    """

    list_: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=1,
    )


class Security(proto.Message):
    r"""Security requirements for contacting the agent.

    Attributes:
        schemes (MutableMapping[str, google.cloud.geminidataanalytics_v1alpha.types.StringList]):
            Map of scheme names to lists of scopes or
            configurations.
    """

    schemes: MutableMapping[str, "StringList"] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=1,
        message="StringList",
    )


class SecurityScheme(proto.Message):
    r"""SecurityScheme defines a security scheme for contacting the
    agent.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        api_key_security_scheme (google.cloud.geminidataanalytics_v1alpha.types.APIKeySecurityScheme):
            API key security scheme.

            This field is a member of `oneof`_ ``scheme``.
        http_auth_security_scheme (google.cloud.geminidataanalytics_v1alpha.types.HTTPAuthSecurityScheme):
            HTTP authentication security scheme.

            This field is a member of `oneof`_ ``scheme``.
        oauth2_security_scheme (google.cloud.geminidataanalytics_v1alpha.types.OAuth2SecurityScheme):
            OAuth2 security scheme.

            This field is a member of `oneof`_ ``scheme``.
        open_id_connect_security_scheme (google.cloud.geminidataanalytics_v1alpha.types.OpenIdConnectSecurityScheme):
            OpenID Connect security scheme.

            This field is a member of `oneof`_ ``scheme``.
        mtls_security_scheme (google.cloud.geminidataanalytics_v1alpha.types.MutualTlsSecurityScheme):
            Mutual TLS security scheme.

            This field is a member of `oneof`_ ``scheme``.
    """

    api_key_security_scheme: "APIKeySecurityScheme" = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="scheme",
        message="APIKeySecurityScheme",
    )
    http_auth_security_scheme: "HTTPAuthSecurityScheme" = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="scheme",
        message="HTTPAuthSecurityScheme",
    )
    oauth2_security_scheme: "OAuth2SecurityScheme" = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="scheme",
        message="OAuth2SecurityScheme",
    )
    open_id_connect_security_scheme: "OpenIdConnectSecurityScheme" = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="scheme",
        message="OpenIdConnectSecurityScheme",
    )
    mtls_security_scheme: "MutualTlsSecurityScheme" = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="scheme",
        message="MutualTlsSecurityScheme",
    )


class APIKeySecurityScheme(proto.Message):
    r"""APIKeySecurityScheme defines an API key security scheme.

    Attributes:
        description (str):
            Optional. Description of this security
            scheme.
        location (str):
            Optional. Location of the API key, valid
            values are "query", "header", or "cookie".
        name (str):
            Optional. Name of the header, query or cookie
            parameter to be used.
    """

    description: str = proto.Field(
        proto.STRING,
        number=1,
    )
    location: str = proto.Field(
        proto.STRING,
        number=2,
    )
    name: str = proto.Field(
        proto.STRING,
        number=3,
    )


class HTTPAuthSecurityScheme(proto.Message):
    r"""HTTPAuthSecurityScheme defines an HTTP authentication
    security scheme.

    Attributes:
        description (str):
            Optional. Description of this security
            scheme.
        scheme (str):
            Optional. The name of the HTTP Authentication
            scheme to be used in the Authorization header.
        bearer_format (str):
            Optional. A hint to the client to identify
            how the bearer token is formatted.
    """

    description: str = proto.Field(
        proto.STRING,
        number=1,
    )
    scheme: str = proto.Field(
        proto.STRING,
        number=2,
    )
    bearer_format: str = proto.Field(
        proto.STRING,
        number=3,
    )


class OAuth2SecurityScheme(proto.Message):
    r"""OAuth2SecurityScheme defines an OAuth2 security scheme.

    Attributes:
        description (str):
            Optional. Description of this security
            scheme.
        flows (google.cloud.geminidataanalytics_v1alpha.types.OAuthFlows):
            Optional. An object containing configuration
            information for the flow types supported.
        oauth2_metadata_url (str):
            Optional. URL to the oauth2 authorization
            server metadata.
    """

    description: str = proto.Field(
        proto.STRING,
        number=1,
    )
    flows: "OAuthFlows" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="OAuthFlows",
    )
    oauth2_metadata_url: str = proto.Field(
        proto.STRING,
        number=3,
    )


class OpenIdConnectSecurityScheme(proto.Message):
    r"""OpenIdConnectSecurityScheme defines an OpenID Connect
    security scheme.

    Attributes:
        description (str):
            Optional. Description of this security
            scheme.
        open_id_connect_url (str):
            Optional. Well-known URL to discover the
            OpenID Connect provider metadata.
    """

    description: str = proto.Field(
        proto.STRING,
        number=1,
    )
    open_id_connect_url: str = proto.Field(
        proto.STRING,
        number=2,
    )


class MutualTlsSecurityScheme(proto.Message):
    r"""MutualTlsSecurityScheme defines a Mutual TLS security scheme.

    Attributes:
        description (str):
            Optional. Description of this security
            scheme.
    """

    description: str = proto.Field(
        proto.STRING,
        number=1,
    )


class OAuthFlows(proto.Message):
    r"""OAuthFlows contains configuration information for supported
    OAuth flows.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        authorization_code (google.cloud.geminidataanalytics_v1alpha.types.AuthorizationCodeOAuthFlow):
            Authorization code flow.

            This field is a member of `oneof`_ ``flow``.
        client_credentials (google.cloud.geminidataanalytics_v1alpha.types.ClientCredentialsOAuthFlow):
            Client credentials flow.

            This field is a member of `oneof`_ ``flow``.
        implicit (google.cloud.geminidataanalytics_v1alpha.types.ImplicitOAuthFlow):
            Implicit flow.

            This field is a member of `oneof`_ ``flow``.
        password (google.cloud.geminidataanalytics_v1alpha.types.PasswordOAuthFlow):
            Resource owner password credentials flow.

            This field is a member of `oneof`_ ``flow``.
    """

    authorization_code: "AuthorizationCodeOAuthFlow" = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="flow",
        message="AuthorizationCodeOAuthFlow",
    )
    client_credentials: "ClientCredentialsOAuthFlow" = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="flow",
        message="ClientCredentialsOAuthFlow",
    )
    implicit: "ImplicitOAuthFlow" = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="flow",
        message="ImplicitOAuthFlow",
    )
    password: "PasswordOAuthFlow" = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="flow",
        message="PasswordOAuthFlow",
    )


class AuthorizationCodeOAuthFlow(proto.Message):
    r"""AuthorizationCodeOAuthFlow defines an authorization code
    OAuth flow.

    Attributes:
        authorization_url (str):
            Optional. The authorization URL to be used
            for this flow.
        token_url (str):
            Optional. The token URL to be used for this
            flow.
        refresh_url (str):
            Optional. The URL to be used for obtaining
            refresh tokens.
        scopes (MutableMapping[str, str]):
            The available scopes for the OAuth2 security
            scheme.
    """

    authorization_url: str = proto.Field(
        proto.STRING,
        number=1,
    )
    token_url: str = proto.Field(
        proto.STRING,
        number=2,
    )
    refresh_url: str = proto.Field(
        proto.STRING,
        number=3,
    )
    scopes: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=4,
    )


class ClientCredentialsOAuthFlow(proto.Message):
    r"""ClientCredentialsOAuthFlow defines a client credentials OAuth
    flow.

    Attributes:
        token_url (str):
            Optional. The token URL to be used for this
            flow.
        refresh_url (str):
            Optional. The URL to be used for obtaining
            refresh tokens.
        scopes (MutableMapping[str, str]):
            The available scopes for the OAuth2 security
            scheme.
    """

    token_url: str = proto.Field(
        proto.STRING,
        number=1,
    )
    refresh_url: str = proto.Field(
        proto.STRING,
        number=2,
    )
    scopes: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=3,
    )


class ImplicitOAuthFlow(proto.Message):
    r"""ImplicitOAuthFlow defines an implicit OAuth flow.

    Attributes:
        authorization_url (str):
            Optional. The authorization URL to be used
            for this flow.
        refresh_url (str):
            Optional. The URL to be used for obtaining
            refresh tokens.
        scopes (MutableMapping[str, str]):
            The available scopes for the OAuth2 security
            scheme.
    """

    authorization_url: str = proto.Field(
        proto.STRING,
        number=1,
    )
    refresh_url: str = proto.Field(
        proto.STRING,
        number=2,
    )
    scopes: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=3,
    )


class PasswordOAuthFlow(proto.Message):
    r"""PasswordOAuthFlow defines a password OAuth flow.

    Attributes:
        token_url (str):
            Optional. The token URL to be used for this
            flow.
        refresh_url (str):
            Optional. The URL to be used for obtaining
            refresh tokens.
        scopes (MutableMapping[str, str]):
            The available scopes for the OAuth2 security
            scheme.
    """

    token_url: str = proto.Field(
        proto.STRING,
        number=1,
    )
    refresh_url: str = proto.Field(
        proto.STRING,
        number=2,
    )
    scopes: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=3,
    )


class SendMessageRequest(proto.Message):
    r"""Request message for SendMessage and SendStreamingMessage.

    Attributes:
        message (google.cloud.geminidataanalytics_v1alpha.types.A2AMessage):
            Required. The message to send to the agent.
        configuration (google.cloud.geminidataanalytics_v1alpha.types.SendMessageConfiguration):
            Optional. Configuration for the send request.
        metadata (google.protobuf.struct_pb2.Struct):
            Optional. Optional metadata for the request.
        tenant (str):
            Optional. Optional tenant, provided as a path
            parameter.
    """

    message: "A2AMessage" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="A2AMessage",
    )
    configuration: "SendMessageConfiguration" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="SendMessageConfiguration",
    )
    metadata: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=3,
        message=struct_pb2.Struct,
    )
    tenant: str = proto.Field(
        proto.STRING,
        number=4,
    )


class GetAgentCardRequest(proto.Message):
    r"""Request message for GetAgentCard.

    Attributes:
        tenant (str):
            Optional. Optional tenant, provided as a path
            parameter.
    """

    tenant: str = proto.Field(
        proto.STRING,
        number=1,
    )


class SendMessageResponse(proto.Message):
    r"""Response message for SendMessage.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        task (google.cloud.geminidataanalytics_v1alpha.types.A2ATask):
            Completed task.

            This field is a member of `oneof`_ ``payload``.
        msg (google.cloud.geminidataanalytics_v1alpha.types.A2AMessage):
            Single message response.

            This field is a member of `oneof`_ ``payload``.
    """

    task: "A2ATask" = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="payload",
        message="A2ATask",
    )
    msg: "A2AMessage" = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="payload",
        message="A2AMessage",
    )


class StreamResponse(proto.Message):
    r"""The stream response for a message.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        task (google.cloud.geminidataanalytics_v1alpha.types.A2ATask):
            Completed task event.

            This field is a member of `oneof`_ ``payload``.
        msg (google.cloud.geminidataanalytics_v1alpha.types.A2AMessage):
            Message event.

            This field is a member of `oneof`_ ``payload``.
        status_update (google.cloud.geminidataanalytics_v1alpha.types.TaskStatusUpdateEvent):
            Task status update event.

            This field is a member of `oneof`_ ``payload``.
        artifact_update (google.cloud.geminidataanalytics_v1alpha.types.TaskArtifactUpdateEvent):
            Task artifact update event.

            This field is a member of `oneof`_ ``payload``.
    """

    task: "A2ATask" = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="payload",
        message="A2ATask",
    )
    msg: "A2AMessage" = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="payload",
        message="A2AMessage",
    )
    status_update: "TaskStatusUpdateEvent" = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="payload",
        message="TaskStatusUpdateEvent",
    )
    artifact_update: "TaskArtifactUpdateEvent" = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="payload",
        message="TaskArtifactUpdateEvent",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
