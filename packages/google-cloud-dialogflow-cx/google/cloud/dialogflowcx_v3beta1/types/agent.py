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


__protobuf__ = proto.module(
    package="google.cloud.dialogflow.cx.v3beta1",
    manifest={
        "SpeechToTextSettings",
        "Agent",
        "ListAgentsRequest",
        "ListAgentsResponse",
        "GetAgentRequest",
        "CreateAgentRequest",
        "UpdateAgentRequest",
        "DeleteAgentRequest",
        "ExportAgentRequest",
        "ExportAgentResponse",
        "RestoreAgentRequest",
    },
)


class SpeechToTextSettings(proto.Message):
    r"""Settings related to speech recognition.

    Attributes:
        enable_speech_adaptation (bool):
            Whether to use speech adaptation for speech
            recognition.
    """

    enable_speech_adaptation = proto.Field(proto.BOOL, number=1)


class Agent(proto.Message):
    r"""Agents are best described as Natural Language Understanding (NLU)
    modules that transform user requests into actionable data. You can
    include agents in your app, product, or service to determine user
    intent and respond to the user in a natural way.

    After you create an agent, you can add
    [Intents][google.cloud.dialogflow.cx.v3beta1.Intent], [Entity
    Types][google.cloud.dialogflow.cx.v3beta1.EntityType],
    [Flows][google.cloud.dialogflow.cx.v3beta1.Flow],
    [Fulfillments][google.cloud.dialogflow.cx.v3beta1.Fulfillment],
    [Webhooks][google.cloud.dialogflow.cx.v3beta1.Webhook], and so on to
    manage the conversation flows..

    Attributes:
        name (str):
            The unique identifier of the agent. Required for the
            [Agents.UpdateAgent][google.cloud.dialogflow.cx.v3beta1.Agents.UpdateAgent]
            method.
            [Agents.CreateAgent][google.cloud.dialogflow.cx.v3beta1.Agents.CreateAgent]
            populates the name automatically. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>``.
        display_name (str):
            Required. The human-readable name of the
            agent, unique within the location.
        default_language_code (str):
            Immutable. The default language of the agent as a language
            tag. See `Language
            Support <https://cloud.google.com/dialogflow/docs/reference/language>`__
            for a list of the currently supported language codes. This
            field cannot be set by the
            [Agents.UpdateAgent][google.cloud.dialogflow.cx.v3beta1.Agents.UpdateAgent]
            method.
        time_zone (str):
            Required. The time zone of the agent from the `time zone
            database <https://www.iana.org/time-zones>`__, e.g.,
            America/New_York, Europe/Paris.
        description (str):
            The description of the agent. The maximum
            length is 500 characters. If exceeded, the
            request is rejected.
        avatar_uri (str):
            The URI of the agent's avatar. Avatars are used throughout
            the Dialogflow console and in the self-hosted `Web
            Demo <https://cloud.google.com/dialogflow/docs/integrations/web-demo>`__
            integration.
        speech_to_text_settings (~.gcdc_agent.SpeechToTextSettings):
            Speech recognition related settings.
        start_flow (str):
            Immutable. Name of the start flow in this agent. A start
            flow will be automatically created when the agent is
            created, and can only be deleted by deleting the agent.
            Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/flows/<Flow ID>``.
        enable_stackdriver_logging (bool):
            Indicates if stackdriver logging is enabled
            for the agent.
        enable_spell_correction (bool):
            Indicates if automatic spell correction is
            enabled in detect intent requests.
    """

    name = proto.Field(proto.STRING, number=1)

    display_name = proto.Field(proto.STRING, number=2)

    default_language_code = proto.Field(proto.STRING, number=3)

    time_zone = proto.Field(proto.STRING, number=5)

    description = proto.Field(proto.STRING, number=6)

    avatar_uri = proto.Field(proto.STRING, number=7)

    speech_to_text_settings = proto.Field(
        proto.MESSAGE, number=13, message=SpeechToTextSettings,
    )

    start_flow = proto.Field(proto.STRING, number=16)

    enable_stackdriver_logging = proto.Field(proto.BOOL, number=18)

    enable_spell_correction = proto.Field(proto.BOOL, number=20)


class ListAgentsRequest(proto.Message):
    r"""The request message for
    [Agents.ListAgents][google.cloud.dialogflow.cx.v3beta1.Agents.ListAgents].

    Attributes:
        parent (str):
            Required. The location to list all agents for. Format:
            ``projects/<Project ID>/locations/<Location ID>``.
        page_size (int):
            The maximum number of items to return in a
            single page. By default 100 and at most 1000.
        page_token (str):
            The next_page_token value returned from a previous list
            request.
    """

    parent = proto.Field(proto.STRING, number=1)

    page_size = proto.Field(proto.INT32, number=2)

    page_token = proto.Field(proto.STRING, number=3)


class ListAgentsResponse(proto.Message):
    r"""The response message for
    [Agents.ListAgents][google.cloud.dialogflow.cx.v3beta1.Agents.ListAgents].

    Attributes:
        agents (Sequence[~.gcdc_agent.Agent]):
            The list of agents. There will be a maximum number of items
            returned based on the page_size field in the request.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
    """

    @property
    def raw_page(self):
        return self

    agents = proto.RepeatedField(proto.MESSAGE, number=1, message=Agent,)

    next_page_token = proto.Field(proto.STRING, number=2)


class GetAgentRequest(proto.Message):
    r"""The request message for
    [Agents.GetAgent][google.cloud.dialogflow.cx.v3beta1.Agents.GetAgent].

    Attributes:
        name (str):
            Required. The name of the agent. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>``.
    """

    name = proto.Field(proto.STRING, number=1)


class CreateAgentRequest(proto.Message):
    r"""The request message for
    [Agents.CreateAgent][google.cloud.dialogflow.cx.v3beta1.Agents.CreateAgent].

    Attributes:
        parent (str):
            Required. The location to create a agent for. Format:
            ``projects/<Project ID>/locations/<Location ID>``.
        agent (~.gcdc_agent.Agent):
            Required. The agent to create.
    """

    parent = proto.Field(proto.STRING, number=1)

    agent = proto.Field(proto.MESSAGE, number=2, message=Agent,)


class UpdateAgentRequest(proto.Message):
    r"""The request message for
    [Agents.UpdateAgent][google.cloud.dialogflow.cx.v3beta1.Agents.UpdateAgent].

    Attributes:
        agent (~.gcdc_agent.Agent):
            Required. The agent to update.
        update_mask (~.field_mask.FieldMask):
            The mask to control which fields get updated.
            If the mask is not present, all fields will be
            updated.
    """

    agent = proto.Field(proto.MESSAGE, number=1, message=Agent,)

    update_mask = proto.Field(proto.MESSAGE, number=2, message=field_mask.FieldMask,)


class DeleteAgentRequest(proto.Message):
    r"""The request message for
    [Agents.DeleteAgent][google.cloud.dialogflow.cx.v3beta1.Agents.DeleteAgent].

    Attributes:
        name (str):
            Required. The name of the agent to delete. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>``.
    """

    name = proto.Field(proto.STRING, number=1)


class ExportAgentRequest(proto.Message):
    r"""The request message for
    [Agents.ExportAgent][google.cloud.dialogflow.cx.v3beta1.Agents.ExportAgent].

    Attributes:
        name (str):
            Required. The name of the agent to export. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>``.
        agent_uri (str):
            Optional. The `Google Cloud
            Storage <https://cloud.google.com/storage/docs/>`__ URI to
            export the agent to. The format of this URI must be
            ``gs://<bucket-name>/<object-name>``. If left unspecified,
            the serialized agent is returned inline.
    """

    name = proto.Field(proto.STRING, number=1)

    agent_uri = proto.Field(proto.STRING, number=2)


class ExportAgentResponse(proto.Message):
    r"""The response message for
    [Agents.ExportAgent][google.cloud.dialogflow.cx.v3beta1.Agents.ExportAgent].

    Attributes:
        agent_uri (str):
            The URI to a file containing the exported agent. This field
            is populated only if ``agent_uri`` is specified in
            [ExportAgentRequest][google.cloud.dialogflow.cx.v3beta1.ExportAgentRequest].
        agent_content (bytes):
            Uncompressed raw byte content for agent.
    """

    agent_uri = proto.Field(proto.STRING, number=1, oneof="agent")

    agent_content = proto.Field(proto.BYTES, number=2, oneof="agent")


class RestoreAgentRequest(proto.Message):
    r"""The request message for
    [Agents.RestoreAgent][google.cloud.dialogflow.cx.v3beta1.Agents.RestoreAgent].

    Attributes:
        name (str):
            Required. The name of the agent to restore into. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>``.
        agent_uri (str):
            The `Google Cloud
            Storage <https://cloud.google.com/storage/docs/>`__ URI to
            restore agent from. The format of this URI must be
            ``gs://<bucket-name>/<object-name>``.
        agent_content (bytes):
            Uncompressed raw byte content for agent.
    """

    name = proto.Field(proto.STRING, number=1)

    agent_uri = proto.Field(proto.STRING, number=2, oneof="agent")

    agent_content = proto.Field(proto.BYTES, number=3, oneof="agent")


__all__ = tuple(sorted(__protobuf__.manifest))
