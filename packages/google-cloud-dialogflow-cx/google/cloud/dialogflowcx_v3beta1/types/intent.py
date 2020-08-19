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
        "IntentView",
        "Intent",
        "ListIntentsRequest",
        "ListIntentsResponse",
        "GetIntentRequest",
        "CreateIntentRequest",
        "UpdateIntentRequest",
        "DeleteIntentRequest",
    },
)


class IntentView(proto.Enum):
    r"""Represents the options for views of an intent.
    An intent can be a sizable object. Therefore, we provide a
    resource view that does not return training phrases in the
    response.
    """
    INTENT_VIEW_UNSPECIFIED = 0
    INTENT_VIEW_PARTIAL = 1
    INTENT_VIEW_FULL = 2


class Intent(proto.Message):
    r"""An intent represents a user's intent to interact with a
    conversational agent.
    You can provide information for the Dialogflow API to use to
    match user input to an intent by adding training phrases (i.e.,
    examples of user input) to your intent.

    Attributes:
        name (str):
            The unique identifier of the intent. Required for the
            [Intents.UpdateIntent][google.cloud.dialogflow.cx.v3beta1.Intents.UpdateIntent]
            method.
            [Intents.CreateIntent][google.cloud.dialogflow.cx.v3beta1.Intents.CreateIntent]
            populates the name automatically. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/intents/<Intent ID>``.
        display_name (str):
            Required. The human-readable name of the
            intent, unique within the agent.
        training_phrases (Sequence[~.gcdc_intent.Intent.TrainingPhrase]):
            The collection of training phrases the agent
            is trained on to identify the intent.
        parameters (Sequence[~.gcdc_intent.Intent.Parameter]):
            The collection of parameters associated with
            the intent.
        priority (int):
            The priority of this intent. Higher numbers represent higher
            priorities.

            -  If the supplied value is unspecified or 0, the service
               translates the value to 500,000, which corresponds to the
               ``Normal`` priority in the console.
            -  If the supplied value is negative, the intent is ignored
               in runtime detect intent requests.
        is_fallback (bool):
            Indicates whether this is a fallback intent.
            Currently only default fallback intent is
            allowed in the agent, which is added upon agent
            creation.
            Adding training phrases to fallback intent is
            useful in the case of requests that are
            mistakenly matched, since training phrases
            assigned to fallback intents act as negative
            examples that triggers no-match event.
    """

    class TrainingPhrase(proto.Message):
        r"""Represents an example that the agent is trained on to
        identify the intent.

        Attributes:
            id (str):
                Output only. The unique identifier of the
                training phrase.
            parts (Sequence[~.gcdc_intent.Intent.TrainingPhrase.Part]):
                Required. The ordered list of training phrase parts. The
                parts are concatenated in order to form the training phrase.

                Note: The API does not automatically annotate training
                phrases like the Dialogflow Console does.

                Note: Do not forget to include whitespace at part
                boundaries, so the training phrase is well formatted when
                the parts are concatenated.

                If the training phrase does not need to be annotated with
                parameters, you just need a single part with only the
                [Part.text][google.cloud.dialogflow.cx.v3beta1.Intent.TrainingPhrase.Part.text]
                field set.

                If you want to annotate the training phrase, you must create
                multiple parts, where the fields of each part are populated
                in one of two ways:

                -  ``Part.text`` is set to a part of the phrase that has no
                   parameters.
                -  ``Part.text`` is set to a part of the phrase that you
                   want to annotate, and the ``parameter_id`` field is set.
            repeat_count (int):
                Indicates how many times this example was
                added to the intent.
        """

        class Part(proto.Message):
            r"""Represents a part of a training phrase.

            Attributes:
                text (str):
                    Required. The text for this part.
                parameter_id (str):
                    The
                    [parameter][google.cloud.dialogflow.cx.v3beta1.Intent.Parameter]
                    used to annotate this part of the training phrase. This
                    field is required for annotated parts of the training
                    phrase.
            """

            text = proto.Field(proto.STRING, number=1)

            parameter_id = proto.Field(proto.STRING, number=2)

        id = proto.Field(proto.STRING, number=1)

        parts = proto.RepeatedField(
            proto.MESSAGE, number=2, message="Intent.TrainingPhrase.Part",
        )

        repeat_count = proto.Field(proto.INT32, number=3)

    class Parameter(proto.Message):
        r"""Represents an intent parameter.

        Attributes:
            id (str):
                Required. The unique identifier of the parameter. This field
                is used by [training
                phrases][google.cloud.dialogflow.cx.v3beta1.Intent.TrainingPhrase]
                to annotate their
                [parts][google.cloud.dialogflow.cx.v3beta1.Intent.TrainingPhrase.Part].
            entity_type (str):
                Required. The entity type of the parameter. Format:
                ``projects/-/locations/-/agents/-/entityTypes/<System Entity Type ID>``
                for system entity types (for example,
                ``projects/-/locations/-/agents/-/entityTypes/sys.date``),
                or
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/entityTypes/<Entity Type ID>``
                for developer entity types.
            is_list (bool):
                Indicates whether the parameter represents a
                list of values.
        """

        id = proto.Field(proto.STRING, number=1)

        entity_type = proto.Field(proto.STRING, number=2)

        is_list = proto.Field(proto.BOOL, number=3)

    name = proto.Field(proto.STRING, number=1)

    display_name = proto.Field(proto.STRING, number=2)

    training_phrases = proto.RepeatedField(
        proto.MESSAGE, number=3, message=TrainingPhrase,
    )

    parameters = proto.RepeatedField(proto.MESSAGE, number=4, message=Parameter,)

    priority = proto.Field(proto.INT32, number=5)

    is_fallback = proto.Field(proto.BOOL, number=6)


class ListIntentsRequest(proto.Message):
    r"""The request message for
    [Intents.ListIntents][google.cloud.dialogflow.cx.v3beta1.Intents.ListIntents].

    Attributes:
        parent (str):
            Required. The agent to list all intents for. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>``.
        language_code (str):
            The language to list intents for. The following fields are
            language dependent:

            -  ``Intent.training_phrases.parts.text``

            If not specified, the agent's default language is used.
            `Many
            languages <https://cloud.google.com/dialogflow/docs/reference/language>`__
            are supported. Note: languages must be enabled in the agent
            before they can be used.
        intent_view (~.gcdc_intent.IntentView):
            The resource view to apply to the returned
            intent.
        page_size (int):
            The maximum number of items to return in a
            single page. By default 100 and at most 1000.
        page_token (str):
            The next_page_token value returned from a previous list
            request.
    """

    parent = proto.Field(proto.STRING, number=1)

    language_code = proto.Field(proto.STRING, number=2)

    intent_view = proto.Field(proto.ENUM, number=5, enum="IntentView",)

    page_size = proto.Field(proto.INT32, number=3)

    page_token = proto.Field(proto.STRING, number=4)


class ListIntentsResponse(proto.Message):
    r"""The response message for
    [Intents.ListIntents][google.cloud.dialogflow.cx.v3beta1.Intents.ListIntents].

    Attributes:
        intents (Sequence[~.gcdc_intent.Intent]):
            The list of intents. There will be a maximum number of items
            returned based on the page_size field in the request.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
    """

    @property
    def raw_page(self):
        return self

    intents = proto.RepeatedField(proto.MESSAGE, number=1, message=Intent,)

    next_page_token = proto.Field(proto.STRING, number=2)


class GetIntentRequest(proto.Message):
    r"""The request message for
    [Intents.GetIntent][google.cloud.dialogflow.cx.v3beta1.Intents.GetIntent].

    Attributes:
        name (str):
            Required. The name of the intent. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/intents/<Intent ID>``.
        language_code (str):
            The language to retrieve the intent for. The following
            fields are language dependent:

            -  ``Intent.training_phrases.parts.text``

            If not specified, the agent's default language is used.
            `Many
            languages <https://cloud.google.com/dialogflow/docs/reference/language>`__
            are supported. Note: languages must be enabled in the agent
            before they can be used.
    """

    name = proto.Field(proto.STRING, number=1)

    language_code = proto.Field(proto.STRING, number=2)


class CreateIntentRequest(proto.Message):
    r"""The request message for
    [Intents.CreateIntent][google.cloud.dialogflow.cx.v3beta1.Intents.CreateIntent].

    Attributes:
        parent (str):
            Required. The agent to create an intent for. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>``.
        intent (~.gcdc_intent.Intent):
            Required. The intent to create.
        language_code (str):
            The language of the following fields in ``intent``:

            -  ``Intent.training_phrases.parts.text``

            If not specified, the agent's default language is used.
            `Many
            languages <https://cloud.google.com/dialogflow/docs/reference/language>`__
            are supported. Note: languages must be enabled in the agent
            before they can be used.
    """

    parent = proto.Field(proto.STRING, number=1)

    intent = proto.Field(proto.MESSAGE, number=2, message=Intent,)

    language_code = proto.Field(proto.STRING, number=3)


class UpdateIntentRequest(proto.Message):
    r"""The request message for
    [Intents.UpdateIntent][google.cloud.dialogflow.cx.v3beta1.Intents.UpdateIntent].

    Attributes:
        intent (~.gcdc_intent.Intent):
            Required. The intent to update.
        language_code (str):
            The language of the following fields in ``intent``:

            -  ``Intent.training_phrases.parts.text``

            If not specified, the agent's default language is used.
            `Many
            languages <https://cloud.google.com/dialogflow/docs/reference/language>`__
            are supported. Note: languages must be enabled in the agent
            before they can be used.
        update_mask (~.field_mask.FieldMask):
            The mask to control which fields get updated.
            If the mask is not present, all fields will be
            updated.
    """

    intent = proto.Field(proto.MESSAGE, number=1, message=Intent,)

    language_code = proto.Field(proto.STRING, number=2)

    update_mask = proto.Field(proto.MESSAGE, number=3, message=field_mask.FieldMask,)


class DeleteIntentRequest(proto.Message):
    r"""The request message for
    [Intents.DeleteIntent][google.cloud.dialogflow.cx.v3beta1.Intents.DeleteIntent].

    Attributes:
        name (str):
            Required. The name of the intent to delete. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/intents/<Intent ID>``.
    """

    name = proto.Field(proto.STRING, number=1)


__all__ = tuple(sorted(__protobuf__.manifest))
