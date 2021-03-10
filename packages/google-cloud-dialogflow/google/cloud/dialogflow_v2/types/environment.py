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


from google.protobuf import timestamp_pb2 as timestamp  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.dialogflow.v2",
    manifest={"Environment", "ListEnvironmentsRequest", "ListEnvironmentsResponse",},
)


class Environment(proto.Message):
    r"""You can create multiple versions of your agent and publish them to
    separate environments.

    When you edit an agent, you are editing the draft agent. At any
    point, you can save the draft agent as an agent version, which is an
    immutable snapshot of your agent.

    When you save the draft agent, it is published to the default
    environment. When you create agent versions, you can publish them to
    custom environments. You can create a variety of custom environments
    for:

    -  testing
    -  development
    -  production
    -  etc.

    For more information, see the `versions and environments
    guide <https://cloud.google.com/dialogflow/docs/agents-versions>`__.

    Attributes:
        name (str):
            Output only. The unique identifier of this agent
            environment. Format:
            ``projects/<Project ID>/agent/environments/<Environment ID>``.
            For Environment ID, "-" is reserved for 'draft' environment.
        description (str):
            Optional. The developer-provided description
            for this environment. The maximum length is 500
            characters. If exceeded, the request is
            rejected.
        agent_version (str):
            Optional. The agent version loaded into this environment.
            Format:
            ``projects/<Project ID>/agent/versions/<Version ID>``.
        state (google.cloud.dialogflow_v2.types.Environment.State):
            Output only. The state of this environment.
            This field is read-only, i.e., it cannot be set
            by create and update methods.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The last update time of this
            environment. This field is read-only, i.e., it
            cannot be set by create and update methods.
    """

    class State(proto.Enum):
        r"""Represents an environment state. When an environment is pointed to a
        new agent version, the environment is temporarily set to the
        ``LOADING`` state. During that time, the environment keeps on
        serving the previous version of the agent. After the new agent
        version is done loading, the environment is set back to the
        ``RUNNING`` state.
        """
        STATE_UNSPECIFIED = 0
        STOPPED = 1
        LOADING = 2
        RUNNING = 3

    name = proto.Field(proto.STRING, number=1)

    description = proto.Field(proto.STRING, number=2)

    agent_version = proto.Field(proto.STRING, number=3)

    state = proto.Field(proto.ENUM, number=4, enum=State,)

    update_time = proto.Field(proto.MESSAGE, number=5, message=timestamp.Timestamp,)


class ListEnvironmentsRequest(proto.Message):
    r"""The request message for
    [Environments.ListEnvironments][google.cloud.dialogflow.v2.Environments.ListEnvironments].

    Attributes:
        parent (str):
            Required. The agent to list all environments from. Format:
            ``projects/<Project ID>/agent``.
        page_size (int):
            Optional. The maximum number of items to
            return in a single page. By default 100 and at
            most 1000.
        page_token (str):
            Optional. The next_page_token value returned from a previous
            list request.
    """

    parent = proto.Field(proto.STRING, number=1)

    page_size = proto.Field(proto.INT32, number=2)

    page_token = proto.Field(proto.STRING, number=3)


class ListEnvironmentsResponse(proto.Message):
    r"""The response message for
    [Environments.ListEnvironments][google.cloud.dialogflow.v2.Environments.ListEnvironments].

    Attributes:
        environments (Sequence[google.cloud.dialogflow_v2.types.Environment]):
            The list of agent environments. There will be a maximum
            number of items returned based on the page_size field in the
            request.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
    """

    @property
    def raw_page(self):
        return self

    environments = proto.RepeatedField(proto.MESSAGE, number=1, message="Environment",)

    next_page_token = proto.Field(proto.STRING, number=2)


__all__ = tuple(sorted(__protobuf__.manifest))
