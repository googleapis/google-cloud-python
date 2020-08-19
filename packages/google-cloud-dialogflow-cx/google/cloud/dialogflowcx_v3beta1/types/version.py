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


from google.cloud.dialogflowcx_v3beta1.types import flow
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.dialogflow.cx.v3beta1",
    manifest={
        "CreateVersionOperationMetadata",
        "Version",
        "ListVersionsRequest",
        "ListVersionsResponse",
        "GetVersionRequest",
        "CreateVersionRequest",
        "UpdateVersionRequest",
        "DeleteVersionRequest",
        "LoadVersionRequest",
    },
)


class CreateVersionOperationMetadata(proto.Message):
    r"""Metadata associated with the long running operation for
    [Versions.CreateVersion][google.cloud.dialogflow.cx.v3beta1.Versions.CreateVersion].

    Attributes:
        version (str):
            Name of the created version. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/flows/<Flow ID>/versions/<Version ID>``.
    """

    version = proto.Field(proto.STRING, number=1)


class Version(proto.Message):
    r"""Represents a version of a flow.

    Attributes:
        name (str):
            Format: projects/<Project
            ID>/locations/<Location ID>/agents/<Agent
            ID>/flows/<Flow ID>/versions/<Version ID>.
            Version ID is a self-increasing number generated
            by Dialogflow upon version creation.
        display_name (str):
            Required. The human-readable name of the
            version. Limit of 64 characters.
        description (str):
            The description of the version. The maximum
            length is 500 characters. If exceeded, the
            request is rejected.
        nlu_settings (~.flow.NluSettings):
            Output only. The NLU settings of the flow at
            version creation.
        create_time (~.timestamp.Timestamp):
            Output only. Create time of the version.
        state (~.gcdc_version.Version.State):
            Output only. The state of this version. This
            field is read-only and cannot be set by create
            and update methods.
    """

    class State(proto.Enum):
        r"""The state of the version."""
        STATE_UNSPECIFIED = 0
        RUNNING = 1
        SUCCEEDED = 2
        FAILED = 3

    name = proto.Field(proto.STRING, number=1)

    display_name = proto.Field(proto.STRING, number=2)

    description = proto.Field(proto.STRING, number=3)

    nlu_settings = proto.Field(proto.MESSAGE, number=4, message=flow.NluSettings,)

    create_time = proto.Field(proto.MESSAGE, number=5, message=timestamp.Timestamp,)

    state = proto.Field(proto.ENUM, number=6, enum=State,)


class ListVersionsRequest(proto.Message):
    r"""The request message for
    [Versions.ListVersions][google.cloud.dialogflow.cx.v3beta1.Versions.ListVersions].

    Attributes:
        parent (str):
            Required. The
            [Flow][google.cloud.dialogflow.cx.v3beta1.Flow] to list all
            versions for. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/flows/<Flow ID>``.
        page_size (int):
            The maximum number of items to return in a
            single page. By default 20 and at most 100.
        page_token (str):
            The next_page_token value returned from a previous list
            request.
    """

    parent = proto.Field(proto.STRING, number=1)

    page_size = proto.Field(proto.INT32, number=2)

    page_token = proto.Field(proto.STRING, number=3)


class ListVersionsResponse(proto.Message):
    r"""The response message for
    [Versions.ListVersions][google.cloud.dialogflow.cx.v3beta1.Versions.ListVersions].

    Attributes:
        versions (Sequence[~.gcdc_version.Version]):
            A list of versions. There will be a maximum number of items
            returned based on the page_size field in the request. The
            list may in some cases be empty or contain fewer entries
            than page_size even if this isn't the last page.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
    """

    @property
    def raw_page(self):
        return self

    versions = proto.RepeatedField(proto.MESSAGE, number=1, message=Version,)

    next_page_token = proto.Field(proto.STRING, number=2)


class GetVersionRequest(proto.Message):
    r"""The request message for
    [Versions.GetVersion][google.cloud.dialogflow.cx.v3beta1.Versions.GetVersion].

    Attributes:
        name (str):
            Required. The name of the
            [Version][google.cloud.dialogflow.cx.v3beta1.Version].
            Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/flows/<Flow ID>/versions/<Version ID>``.
    """

    name = proto.Field(proto.STRING, number=1)


class CreateVersionRequest(proto.Message):
    r"""The request message for
    [Versions.CreateVersion][google.cloud.dialogflow.cx.v3beta1.Versions.CreateVersion].

    Attributes:
        parent (str):
            Required. The
            [Flow][google.cloud.dialogflow.cx.v3beta1.Flow] to create an
            [Version][google.cloud.dialogflow.cx.v3beta1.Version] for.
            Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/flows/<Flow ID>``.
        version (~.gcdc_version.Version):
            Required. The version to create.
    """

    parent = proto.Field(proto.STRING, number=1)

    version = proto.Field(proto.MESSAGE, number=2, message=Version,)


class UpdateVersionRequest(proto.Message):
    r"""The request message for
    [Versions.UpdateVersion][google.cloud.dialogflow.cx.v3beta1.Versions.UpdateVersion].

    Attributes:
        version (~.gcdc_version.Version):
            Required. The version to update.
        update_mask (~.field_mask.FieldMask):
            Required. The mask to control which fields get updated.
            Currently only ``description`` and ``display_name`` can be
            updated.
    """

    version = proto.Field(proto.MESSAGE, number=1, message=Version,)

    update_mask = proto.Field(proto.MESSAGE, number=2, message=field_mask.FieldMask,)


class DeleteVersionRequest(proto.Message):
    r"""The request message for
    [Versions.DeleteVersion][google.cloud.dialogflow.cx.v3beta1.Versions.DeleteVersion].

    Attributes:
        name (str):
            Required. The name of the
            [Version][google.cloud.dialogflow.cx.v3beta1.Version] to
            delete. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/flows/<Flow ID>/versions/<Version ID>``.
    """

    name = proto.Field(proto.STRING, number=1)


class LoadVersionRequest(proto.Message):
    r"""The request message for
    [Versions.LoadVersion][google.cloud.dialogflow.cx.v3beta1.Versions.LoadVersion].

    Attributes:
        name (str):
            Required. The
            [Version][google.cloud.dialogflow.cx.v3beta1.Version] to be
            loaded to draft version. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/flows/<Flow ID>/versions/<Version ID>``.
        allow_override_agent_resources (bool):
            This field is used to prevent accidental overwrite of other
            agent resources in the draft version, which can potentially
            impact other flow's behavior. If
            ``allow_override_agent_resources`` is false, conflicted
            agent-level resources will not be overridden (i.e. intents,
            entities, webhooks).
    """

    name = proto.Field(proto.STRING, number=1)

    allow_override_agent_resources = proto.Field(proto.BOOL, number=2)


__all__ = tuple(sorted(__protobuf__.manifest))
