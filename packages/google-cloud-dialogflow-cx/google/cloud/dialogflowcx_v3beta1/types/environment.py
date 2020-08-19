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


from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.dialogflow.cx.v3beta1",
    manifest={
        "Environment",
        "ListEnvironmentsRequest",
        "ListEnvironmentsResponse",
        "GetEnvironmentRequest",
        "CreateEnvironmentRequest",
        "UpdateEnvironmentRequest",
        "DeleteEnvironmentRequest",
        "LookupEnvironmentHistoryRequest",
        "LookupEnvironmentHistoryResponse",
    },
)


class Environment(proto.Message):
    r"""Represents an environment for an agent. You can create
    multiple versions of your agent and publish them to separate
    environments. When you edit an agent, you are editing the draft
    agent. At any point, you can save the draft agent as an agent
    version, which is an immutable snapshot of your agent. When you
    save the draft agent, it is published to the default
    environment. When you create agent versions, you can publish
    them to custom environments. You can create a variety of custom
    environments for testing, development, production, etc.

    Attributes:
        name (str):
            The name of the environment. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/environments/<Environment ID>``.
        display_name (str):
            Required. The human-readable name of the
            environment (unique in an agent). Limit of 64
            characters.
        description (str):
            The human-readable description of the
            environment. The maximum length is 500
            characters. If exceeded, the request is
            rejected.
        version_configs (Sequence[~.gcdc_environment.Environment.VersionConfig]):
            Required. A list of configurations for flow versions. You
            should include version configs for all flows that are
            reachable from [``Start Flow``][Agent.start_flow] in the
            agent. Otherwise, an error will be returned.
        update_time (~.timestamp.Timestamp):
            Output only. Update time of this environment.
    """

    class VersionConfig(proto.Message):
        r"""Configuration for the version.

        Attributes:
            version (str):
                Required. Format: projects/<Project
                ID>/locations/<Location ID>/agents/<Agent
                ID>/flows/<Flow ID>/versions/<Version ID>.
        """

        version = proto.Field(proto.STRING, number=1)

    name = proto.Field(proto.STRING, number=1)

    display_name = proto.Field(proto.STRING, number=2)

    description = proto.Field(proto.STRING, number=3)

    version_configs = proto.RepeatedField(
        proto.MESSAGE, number=6, message=VersionConfig,
    )

    update_time = proto.Field(proto.MESSAGE, number=5, message=timestamp.Timestamp,)


class ListEnvironmentsRequest(proto.Message):
    r"""The request message for
    [Environments.ListEnvironments][google.cloud.dialogflow.cx.v3beta1.Environments.ListEnvironments].

    Attributes:
        parent (str):
            Required. The
            [Agent][google.cloud.dialogflow.cx.v3beta1.Agent] to list
            all environments for. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>``.
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


class ListEnvironmentsResponse(proto.Message):
    r"""The response message for
    [Environments.ListEnvironments][google.cloud.dialogflow.cx.v3beta1.Environments.ListEnvironments].

    Attributes:
        environments (Sequence[~.gcdc_environment.Environment]):
            The list of environments. There will be a maximum number of
            items returned based on the page_size field in the request.
            The list may in some cases be empty or contain fewer entries
            than page_size even if this isn't the last page.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
    """

    @property
    def raw_page(self):
        return self

    environments = proto.RepeatedField(proto.MESSAGE, number=1, message=Environment,)

    next_page_token = proto.Field(proto.STRING, number=2)


class GetEnvironmentRequest(proto.Message):
    r"""The request message for
    [Environments.GetEnvironment][google.cloud.dialogflow.cx.v3beta1.Environments.GetEnvironment].

    Attributes:
        name (str):
            Required. The name of the
            [Environment][google.cloud.dialogflow.cx.v3beta1.Environment].
            Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/environments/<Environment ID>``.
    """

    name = proto.Field(proto.STRING, number=1)


class CreateEnvironmentRequest(proto.Message):
    r"""The request message for
    [Environments.CreateEnvironment][google.cloud.dialogflow.cx.v3beta1.Environments.CreateEnvironment].

    Attributes:
        parent (str):
            Required. The
            [Agent][google.cloud.dialogflow.cx.v3beta1.Agent] to create
            an
            [Environment][google.cloud.dialogflow.cx.v3beta1.Environment]
            for. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>``.
        environment (~.gcdc_environment.Environment):
            Required. The environment to create.
    """

    parent = proto.Field(proto.STRING, number=1)

    environment = proto.Field(proto.MESSAGE, number=2, message=Environment,)


class UpdateEnvironmentRequest(proto.Message):
    r"""The request message for
    [Environments.UpdateEnvironment][google.cloud.dialogflow.cx.v3beta1.Environments.UpdateEnvironment].

    Attributes:
        environment (~.gcdc_environment.Environment):
            Required. The environment to update.
        update_mask (~.field_mask.FieldMask):
            Required. The mask to control which fields
            get updated.
    """

    environment = proto.Field(proto.MESSAGE, number=1, message=Environment,)

    update_mask = proto.Field(proto.MESSAGE, number=2, message=field_mask.FieldMask,)


class DeleteEnvironmentRequest(proto.Message):
    r"""The request message for
    [Environments.DeleteEnvironment][google.cloud.dialogflow.cx.v3beta1.Environments.DeleteEnvironment].

    Attributes:
        name (str):
            Required. The name of the
            [Environment][google.cloud.dialogflow.cx.v3beta1.Environment]
            to delete. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/environments/<Environment ID>``.
    """

    name = proto.Field(proto.STRING, number=1)


class LookupEnvironmentHistoryRequest(proto.Message):
    r"""The request message for
    [Environments.LookupEnvironmentHistory][google.cloud.dialogflow.cx.v3beta1.Environments.LookupEnvironmentHistory].

    Attributes:
        name (str):
            Required. Resource name of the environment to look up the
            history for. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/environments/<Environment ID>``.
        page_size (int):
            The maximum number of items to return in a
            single page. By default 100 and at most 1000.
        page_token (str):
            The next_page_token value returned from a previous list
            request.
    """

    name = proto.Field(proto.STRING, number=1)

    page_size = proto.Field(proto.INT32, number=2)

    page_token = proto.Field(proto.STRING, number=3)


class LookupEnvironmentHistoryResponse(proto.Message):
    r"""The response message for
    [Environments.LookupEnvironmentHistory][google.cloud.dialogflow.cx.v3beta1.Environments.LookupEnvironmentHistory].

    Attributes:
        environments (Sequence[~.gcdc_environment.Environment]):
            Represents a list of snapshots for an environment. Time of
            the snapshots is stored in
            [``update_time``][google.cloud.dialogflow.cx.v3beta1.Environment.update_time].
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
    """

    @property
    def raw_page(self):
        return self

    environments = proto.RepeatedField(proto.MESSAGE, number=1, message=Environment,)

    next_page_token = proto.Field(proto.STRING, number=2)


__all__ = tuple(sorted(__protobuf__.manifest))
