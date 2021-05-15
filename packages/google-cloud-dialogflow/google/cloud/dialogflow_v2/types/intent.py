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

from google.cloud.dialogflow_v2.types import context
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import struct_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.dialogflow.v2",
    manifest={
        "IntentView",
        "Intent",
        "ListIntentsRequest",
        "ListIntentsResponse",
        "GetIntentRequest",
        "CreateIntentRequest",
        "UpdateIntentRequest",
        "DeleteIntentRequest",
        "BatchUpdateIntentsRequest",
        "BatchUpdateIntentsResponse",
        "BatchDeleteIntentsRequest",
        "IntentBatch",
    },
)


class IntentView(proto.Enum):
    r"""Represents the options for views of an intent.
    An intent can be a sizable object. Therefore, we provide a
    resource view that does not return training phrases in the
    response by default.
    """
    INTENT_VIEW_UNSPECIFIED = 0
    INTENT_VIEW_FULL = 1


class Intent(proto.Message):
    r"""An intent categorizes an end-user's intention for one conversation
    turn. For each agent, you define many intents, where your combined
    intents can handle a complete conversation. When an end-user writes
    or says something, referred to as an end-user expression or end-user
    input, Dialogflow matches the end-user input to the best intent in
    your agent. Matching an intent is also known as intent
    classification.

    For more information, see the `intent
    guide <https://cloud.google.com/dialogflow/docs/intents-overview>`__.

    Attributes:
        name (str):
            Optional. The unique identifier of this intent. Required for
            [Intents.UpdateIntent][google.cloud.dialogflow.v2.Intents.UpdateIntent]
            and
            [Intents.BatchUpdateIntents][google.cloud.dialogflow.v2.Intents.BatchUpdateIntents]
            methods. Format:
            ``projects/<Project ID>/agent/intents/<Intent ID>``.
        display_name (str):
            Required. The name of this intent.
        webhook_state (google.cloud.dialogflow_v2.types.Intent.WebhookState):
            Optional. Indicates whether webhooks are
            enabled for the intent.
        priority (int):
            Optional. The priority of this intent. Higher numbers
            represent higher priorities.

            -  If the supplied value is unspecified or 0, the service
               translates the value to 500,000, which corresponds to the
               ``Normal`` priority in the console.
            -  If the supplied value is negative, the intent is ignored
               in runtime detect intent requests.
        is_fallback (bool):
            Optional. Indicates whether this is a
            fallback intent.
        ml_disabled (bool):
            Optional. Indicates whether Machine Learning is disabled for
            the intent. Note: If ``ml_disabled`` setting is set to true,
            then this intent is not taken into account during inference
            in ``ML ONLY`` match mode. Also, auto-markup in the UI is
            turned off.
        live_agent_handoff (bool):
            Optional. Indicates that a live agent should be brought in
            to handle the interaction with the user. In most cases, when
            you set this flag to true, you would also want to set
            end_interaction to true as well. Default is false.
        end_interaction (bool):
            Optional. Indicates that this intent ends an
            interaction. Some integrations (e.g., Actions on
            Google or Dialogflow phone gateway) use this
            information to close interaction with an end
            user. Default is false.
        input_context_names (Sequence[str]):
            Optional. The list of context names required for this intent
            to be triggered. Format:
            ``projects/<Project ID>/agent/sessions/-/contexts/<Context ID>``.
        events (Sequence[str]):
            Optional. The collection of event names that
            trigger the intent. If the collection of input
            contexts is not empty, all of the contexts must
            be present in the active user session for an
            event to trigger this intent. Event names are
            limited to 150 characters.
        training_phrases (Sequence[google.cloud.dialogflow_v2.types.Intent.TrainingPhrase]):
            Optional. The collection of examples that the
            agent is trained on.
        action (str):
            Optional. The name of the action associated
            with the intent. Note: The action name must not
            contain whitespaces.
        output_contexts (Sequence[google.cloud.dialogflow_v2.types.Context]):
            Optional. The collection of contexts that are activated when
            the intent is matched. Context messages in this collection
            should not set the parameters field. Setting the
            ``lifespan_count`` to 0 will reset the context when the
            intent is matched. Format:
            ``projects/<Project ID>/agent/sessions/-/contexts/<Context ID>``.
        reset_contexts (bool):
            Optional. Indicates whether to delete all
            contexts in the current session when this intent
            is matched.
        parameters (Sequence[google.cloud.dialogflow_v2.types.Intent.Parameter]):
            Optional. The collection of parameters
            associated with the intent.
        messages (Sequence[google.cloud.dialogflow_v2.types.Intent.Message]):
            Optional. The collection of rich messages corresponding to
            the ``Response`` field in the Dialogflow console.
        default_response_platforms (Sequence[google.cloud.dialogflow_v2.types.Intent.Message.Platform]):
            Optional. The list of platforms for which the first
            responses will be copied from the messages in
            PLATFORM_UNSPECIFIED (i.e. default platform).
        root_followup_intent_name (str):
            Read-only. The unique identifier of the root intent in the
            chain of followup intents. It identifies the correct
            followup intents chain for this intent. We populate this
            field only in the output.

            Format: ``projects/<Project ID>/agent/intents/<Intent ID>``.
        parent_followup_intent_name (str):
            Read-only after creation. The unique identifier of the
            parent intent in the chain of followup intents. You can set
            this field when creating an intent, for example with
            [CreateIntent][google.cloud.dialogflow.v2.Intents.CreateIntent]
            or
            [BatchUpdateIntents][google.cloud.dialogflow.v2.Intents.BatchUpdateIntents],
            in order to make this intent a followup intent.

            It identifies the parent followup intent. Format:
            ``projects/<Project ID>/agent/intents/<Intent ID>``.
        followup_intent_info (Sequence[google.cloud.dialogflow_v2.types.Intent.FollowupIntentInfo]):
            Read-only. Information about all followup
            intents that have this intent as a direct or
            indirect parent. We populate this field only in
            the output.
    """

    class WebhookState(proto.Enum):
        r"""Represents the different states that webhooks can be in."""
        WEBHOOK_STATE_UNSPECIFIED = 0
        WEBHOOK_STATE_ENABLED = 1
        WEBHOOK_STATE_ENABLED_FOR_SLOT_FILLING = 2

    class TrainingPhrase(proto.Message):
        r"""Represents an example that the agent is trained on.
        Attributes:
            name (str):
                Output only. The unique identifier of this
                training phrase.
            type_ (google.cloud.dialogflow_v2.types.Intent.TrainingPhrase.Type):
                Required. The type of the training phrase.
            parts (Sequence[google.cloud.dialogflow_v2.types.Intent.TrainingPhrase.Part]):
                Required. The ordered list of training phrase parts. The
                parts are concatenated in order to form the training phrase.

                Note: The API does not automatically annotate training
                phrases like the Dialogflow Console does.

                Note: Do not forget to include whitespace at part
                boundaries, so the training phrase is well formatted when
                the parts are concatenated.

                If the training phrase does not need to be annotated with
                parameters, you just need a single part with only the
                [Part.text][google.cloud.dialogflow.v2.Intent.TrainingPhrase.Part.text]
                field set.

                If you want to annotate the training phrase, you must create
                multiple parts, where the fields of each part are populated
                in one of two ways:

                -  ``Part.text`` is set to a part of the phrase that has no
                   parameters.
                -  ``Part.text`` is set to a part of the phrase that you
                   want to annotate, and the ``entity_type``, ``alias``, and
                   ``user_defined`` fields are all set.
            times_added_count (int):
                Optional. Indicates how many times this
                example was added to the intent. Each time a
                developer adds an existing sample by editing an
                intent or training, this counter is increased.
        """

        class Type(proto.Enum):
            r"""Represents different types of training phrases."""
            TYPE_UNSPECIFIED = 0
            EXAMPLE = 1
            TEMPLATE = 2

        class Part(proto.Message):
            r"""Represents a part of a training phrase.
            Attributes:
                text (str):
                    Required. The text for this part.
                entity_type (str):
                    Optional. The entity type name prefixed with ``@``. This
                    field is required for annotated parts of the training
                    phrase.
                alias (str):
                    Optional. The parameter name for the value
                    extracted from the annotated part of the
                    example. This field is required for annotated
                    parts of the training phrase.
                user_defined (bool):
                    Optional. Indicates whether the text was
                    manually annotated. This field is set to true
                    when the Dialogflow Console is used to manually
                    annotate the part. When creating an annotated
                    part with the API, you must set this to true.
            """

            text = proto.Field(proto.STRING, number=1,)
            entity_type = proto.Field(proto.STRING, number=2,)
            alias = proto.Field(proto.STRING, number=3,)
            user_defined = proto.Field(proto.BOOL, number=4,)

        name = proto.Field(proto.STRING, number=1,)
        type_ = proto.Field(proto.ENUM, number=2, enum="Intent.TrainingPhrase.Type",)
        parts = proto.RepeatedField(
            proto.MESSAGE, number=3, message="Intent.TrainingPhrase.Part",
        )
        times_added_count = proto.Field(proto.INT32, number=4,)

    class Parameter(proto.Message):
        r"""Represents intent parameters.
        Attributes:
            name (str):
                The unique identifier of this parameter.
            display_name (str):
                Required. The name of the parameter.
            value (str):
                Optional. The definition of the parameter value. It can be:

                -  a constant string,
                -  a parameter value defined as ``$parameter_name``,
                -  an original parameter value defined as
                   ``$parameter_name.original``,
                -  a parameter value from some context defined as
                   ``#context_name.parameter_name``.
            default_value (str):
                Optional. The default value to use when the ``value`` yields
                an empty result. Default values can be extracted from
                contexts by using the following syntax:
                ``#context_name.parameter_name``.
            entity_type_display_name (str):
                Optional. The name of the entity type, prefixed with ``@``,
                that describes values of the parameter. If the parameter is
                required, this must be provided.
            mandatory (bool):
                Optional. Indicates whether the parameter is
                required. That is, whether the intent cannot be
                completed without collecting the parameter
                value.
            prompts (Sequence[str]):
                Optional. The collection of prompts that the
                agent can present to the user in order to
                collect a value for the parameter.
            is_list (bool):
                Optional. Indicates whether the parameter
                represents a list of values.
        """

        name = proto.Field(proto.STRING, number=1,)
        display_name = proto.Field(proto.STRING, number=2,)
        value = proto.Field(proto.STRING, number=3,)
        default_value = proto.Field(proto.STRING, number=4,)
        entity_type_display_name = proto.Field(proto.STRING, number=5,)
        mandatory = proto.Field(proto.BOOL, number=6,)
        prompts = proto.RepeatedField(proto.STRING, number=7,)
        is_list = proto.Field(proto.BOOL, number=8,)

    class Message(proto.Message):
        r"""A rich response message. Corresponds to the intent ``Response``
        field in the Dialogflow console. For more information, see `Rich
        response
        messages <https://cloud.google.com/dialogflow/docs/intents-rich-messages>`__.

        Attributes:
            text (google.cloud.dialogflow_v2.types.Intent.Message.Text):
                The text response.
            image (google.cloud.dialogflow_v2.types.Intent.Message.Image):
                The image response.
            quick_replies (google.cloud.dialogflow_v2.types.Intent.Message.QuickReplies):
                The quick replies response.
            card (google.cloud.dialogflow_v2.types.Intent.Message.Card):
                The card response.
            payload (google.protobuf.struct_pb2.Struct):
                A custom platform-specific response.
            simple_responses (google.cloud.dialogflow_v2.types.Intent.Message.SimpleResponses):
                The voice and text-only responses for Actions
                on Google.
            basic_card (google.cloud.dialogflow_v2.types.Intent.Message.BasicCard):
                The basic card response for Actions on
                Google.
            suggestions (google.cloud.dialogflow_v2.types.Intent.Message.Suggestions):
                The suggestion chips for Actions on Google.
            link_out_suggestion (google.cloud.dialogflow_v2.types.Intent.Message.LinkOutSuggestion):
                The link out suggestion chip for Actions on
                Google.
            list_select (google.cloud.dialogflow_v2.types.Intent.Message.ListSelect):
                The list card response for Actions on Google.
            carousel_select (google.cloud.dialogflow_v2.types.Intent.Message.CarouselSelect):
                The carousel card response for Actions on
                Google.
            browse_carousel_card (google.cloud.dialogflow_v2.types.Intent.Message.BrowseCarouselCard):
                Browse carousel card for Actions on Google.
            table_card (google.cloud.dialogflow_v2.types.Intent.Message.TableCard):
                Table card for Actions on Google.
            media_content (google.cloud.dialogflow_v2.types.Intent.Message.MediaContent):
                The media content card for Actions on Google.
            platform (google.cloud.dialogflow_v2.types.Intent.Message.Platform):
                Optional. The platform that this message is
                intended for.
        """

        class Platform(proto.Enum):
            r"""The rich response message integration platform. See
            `Integrations <https://cloud.google.com/dialogflow/docs/integrations>`__.
            """
            PLATFORM_UNSPECIFIED = 0
            FACEBOOK = 1
            SLACK = 2
            TELEGRAM = 3
            KIK = 4
            SKYPE = 5
            LINE = 6
            VIBER = 7
            ACTIONS_ON_GOOGLE = 8
            GOOGLE_HANGOUTS = 11

        class Text(proto.Message):
            r"""The text response message.
            Attributes:
                text (Sequence[str]):
                    Optional. The collection of the agent's
                    responses.
            """

            text = proto.RepeatedField(proto.STRING, number=1,)

        class Image(proto.Message):
            r"""The image response message.
            Attributes:
                image_uri (str):
                    Optional. The public URI to an image file.
                accessibility_text (str):
                    Optional. A text description of the image to
                    be used for accessibility, e.g., screen readers.
            """

            image_uri = proto.Field(proto.STRING, number=1,)
            accessibility_text = proto.Field(proto.STRING, number=2,)

        class QuickReplies(proto.Message):
            r"""The quick replies response message.
            Attributes:
                title (str):
                    Optional. The title of the collection of
                    quick replies.
                quick_replies (Sequence[str]):
                    Optional. The collection of quick replies.
            """

            title = proto.Field(proto.STRING, number=1,)
            quick_replies = proto.RepeatedField(proto.STRING, number=2,)

        class Card(proto.Message):
            r"""The card response message.
            Attributes:
                title (str):
                    Optional. The title of the card.
                subtitle (str):
                    Optional. The subtitle of the card.
                image_uri (str):
                    Optional. The public URI to an image file for
                    the card.
                buttons (Sequence[google.cloud.dialogflow_v2.types.Intent.Message.Card.Button]):
                    Optional. The collection of card buttons.
            """

            class Button(proto.Message):
                r"""Contains information about a button.
                Attributes:
                    text (str):
                        Optional. The text to show on the button.
                    postback (str):
                        Optional. The text to send back to the
                        Dialogflow API or a URI to open.
                """

                text = proto.Field(proto.STRING, number=1,)
                postback = proto.Field(proto.STRING, number=2,)

            title = proto.Field(proto.STRING, number=1,)
            subtitle = proto.Field(proto.STRING, number=2,)
            image_uri = proto.Field(proto.STRING, number=3,)
            buttons = proto.RepeatedField(
                proto.MESSAGE, number=4, message="Intent.Message.Card.Button",
            )

        class SimpleResponse(proto.Message):
            r"""The simple response message containing speech or text.
            Attributes:
                text_to_speech (str):
                    One of text_to_speech or ssml must be provided. The plain
                    text of the speech output. Mutually exclusive with ssml.
                ssml (str):
                    One of text_to_speech or ssml must be provided. Structured
                    spoken response to the user in the SSML format. Mutually
                    exclusive with text_to_speech.
                display_text (str):
                    Optional. The text to display.
            """

            text_to_speech = proto.Field(proto.STRING, number=1,)
            ssml = proto.Field(proto.STRING, number=2,)
            display_text = proto.Field(proto.STRING, number=3,)

        class SimpleResponses(proto.Message):
            r"""The collection of simple response candidates. This message in
            ``QueryResult.fulfillment_messages`` and
            ``WebhookResponse.fulfillment_messages`` should contain only one
            ``SimpleResponse``.

            Attributes:
                simple_responses (Sequence[google.cloud.dialogflow_v2.types.Intent.Message.SimpleResponse]):
                    Required. The list of simple responses.
            """

            simple_responses = proto.RepeatedField(
                proto.MESSAGE, number=1, message="Intent.Message.SimpleResponse",
            )

        class BasicCard(proto.Message):
            r"""The basic card message. Useful for displaying information.
            Attributes:
                title (str):
                    Optional. The title of the card.
                subtitle (str):
                    Optional. The subtitle of the card.
                formatted_text (str):
                    Required, unless image is present. The body
                    text of the card.
                image (google.cloud.dialogflow_v2.types.Intent.Message.Image):
                    Optional. The image for the card.
                buttons (Sequence[google.cloud.dialogflow_v2.types.Intent.Message.BasicCard.Button]):
                    Optional. The collection of card buttons.
            """

            class Button(proto.Message):
                r"""The button object that appears at the bottom of a card.
                Attributes:
                    title (str):
                        Required. The title of the button.
                    open_uri_action (google.cloud.dialogflow_v2.types.Intent.Message.BasicCard.Button.OpenUriAction):
                        Required. Action to take when a user taps on
                        the button.
                """

                class OpenUriAction(proto.Message):
                    r"""Opens the given URI.
                    Attributes:
                        uri (str):
                            Required. The HTTP or HTTPS scheme URI.
                    """

                    uri = proto.Field(proto.STRING, number=1,)

                title = proto.Field(proto.STRING, number=1,)
                open_uri_action = proto.Field(
                    proto.MESSAGE,
                    number=2,
                    message="Intent.Message.BasicCard.Button.OpenUriAction",
                )

            title = proto.Field(proto.STRING, number=1,)
            subtitle = proto.Field(proto.STRING, number=2,)
            formatted_text = proto.Field(proto.STRING, number=3,)
            image = proto.Field(
                proto.MESSAGE, number=4, message="Intent.Message.Image",
            )
            buttons = proto.RepeatedField(
                proto.MESSAGE, number=5, message="Intent.Message.BasicCard.Button",
            )

        class Suggestion(proto.Message):
            r"""The suggestion chip message that the user can tap to quickly
            post a reply to the conversation.

            Attributes:
                title (str):
                    Required. The text shown the in the
                    suggestion chip.
            """

            title = proto.Field(proto.STRING, number=1,)

        class Suggestions(proto.Message):
            r"""The collection of suggestions.
            Attributes:
                suggestions (Sequence[google.cloud.dialogflow_v2.types.Intent.Message.Suggestion]):
                    Required. The list of suggested replies.
            """

            suggestions = proto.RepeatedField(
                proto.MESSAGE, number=1, message="Intent.Message.Suggestion",
            )

        class LinkOutSuggestion(proto.Message):
            r"""The suggestion chip message that allows the user to jump out
            to the app or website associated with this agent.

            Attributes:
                destination_name (str):
                    Required. The name of the app or site this
                    chip is linking to.
                uri (str):
                    Required. The URI of the app or site to open
                    when the user taps the suggestion chip.
            """

            destination_name = proto.Field(proto.STRING, number=1,)
            uri = proto.Field(proto.STRING, number=2,)

        class ListSelect(proto.Message):
            r"""The card for presenting a list of options to select from.
            Attributes:
                title (str):
                    Optional. The overall title of the list.
                items (Sequence[google.cloud.dialogflow_v2.types.Intent.Message.ListSelect.Item]):
                    Required. List items.
                subtitle (str):
                    Optional. Subtitle of the list.
            """

            class Item(proto.Message):
                r"""An item in the list.
                Attributes:
                    info (google.cloud.dialogflow_v2.types.Intent.Message.SelectItemInfo):
                        Required. Additional information about this
                        option.
                    title (str):
                        Required. The title of the list item.
                    description (str):
                        Optional. The main text describing the item.
                    image (google.cloud.dialogflow_v2.types.Intent.Message.Image):
                        Optional. The image to display.
                """

                info = proto.Field(
                    proto.MESSAGE, number=1, message="Intent.Message.SelectItemInfo",
                )
                title = proto.Field(proto.STRING, number=2,)
                description = proto.Field(proto.STRING, number=3,)
                image = proto.Field(
                    proto.MESSAGE, number=4, message="Intent.Message.Image",
                )

            title = proto.Field(proto.STRING, number=1,)
            items = proto.RepeatedField(
                proto.MESSAGE, number=2, message="Intent.Message.ListSelect.Item",
            )
            subtitle = proto.Field(proto.STRING, number=3,)

        class CarouselSelect(proto.Message):
            r"""The card for presenting a carousel of options to select from.
            Attributes:
                items (Sequence[google.cloud.dialogflow_v2.types.Intent.Message.CarouselSelect.Item]):
                    Required. Carousel items.
            """

            class Item(proto.Message):
                r"""An item in the carousel.
                Attributes:
                    info (google.cloud.dialogflow_v2.types.Intent.Message.SelectItemInfo):
                        Required. Additional info about the option
                        item.
                    title (str):
                        Required. Title of the carousel item.
                    description (str):
                        Optional. The body text of the card.
                    image (google.cloud.dialogflow_v2.types.Intent.Message.Image):
                        Optional. The image to display.
                """

                info = proto.Field(
                    proto.MESSAGE, number=1, message="Intent.Message.SelectItemInfo",
                )
                title = proto.Field(proto.STRING, number=2,)
                description = proto.Field(proto.STRING, number=3,)
                image = proto.Field(
                    proto.MESSAGE, number=4, message="Intent.Message.Image",
                )

            items = proto.RepeatedField(
                proto.MESSAGE, number=1, message="Intent.Message.CarouselSelect.Item",
            )

        class SelectItemInfo(proto.Message):
            r"""Additional info about the select item for when it is
            triggered in a dialog.

            Attributes:
                key (str):
                    Required. A unique key that will be sent back
                    to the agent if this response is given.
                synonyms (Sequence[str]):
                    Optional. A list of synonyms that can also be
                    used to trigger this item in dialog.
            """

            key = proto.Field(proto.STRING, number=1,)
            synonyms = proto.RepeatedField(proto.STRING, number=2,)

        class MediaContent(proto.Message):
            r"""The media content card for Actions on Google.
            Attributes:
                media_type (google.cloud.dialogflow_v2.types.Intent.Message.MediaContent.ResponseMediaType):
                    Optional. What type of media is the content
                    (ie "audio").
                media_objects (Sequence[google.cloud.dialogflow_v2.types.Intent.Message.MediaContent.ResponseMediaObject]):
                    Required. List of media objects.
            """

            class ResponseMediaType(proto.Enum):
                r"""Format of response media type."""
                RESPONSE_MEDIA_TYPE_UNSPECIFIED = 0
                AUDIO = 1

            class ResponseMediaObject(proto.Message):
                r"""Response media object for media content card.
                Attributes:
                    name (str):
                        Required. Name of media card.
                    description (str):
                        Optional. Description of media card.
                    large_image (google.cloud.dialogflow_v2.types.Intent.Message.Image):
                        Optional. Image to display above media
                        content.
                    icon (google.cloud.dialogflow_v2.types.Intent.Message.Image):
                        Optional. Icon to display above media
                        content.
                    content_url (str):
                        Required. Url where the media is stored.
                """

                name = proto.Field(proto.STRING, number=1,)
                description = proto.Field(proto.STRING, number=2,)
                large_image = proto.Field(
                    proto.MESSAGE,
                    number=3,
                    oneof="image",
                    message="Intent.Message.Image",
                )
                icon = proto.Field(
                    proto.MESSAGE,
                    number=4,
                    oneof="image",
                    message="Intent.Message.Image",
                )
                content_url = proto.Field(proto.STRING, number=5,)

            media_type = proto.Field(
                proto.ENUM,
                number=1,
                enum="Intent.Message.MediaContent.ResponseMediaType",
            )
            media_objects = proto.RepeatedField(
                proto.MESSAGE,
                number=2,
                message="Intent.Message.MediaContent.ResponseMediaObject",
            )

        class BrowseCarouselCard(proto.Message):
            r"""Browse Carousel Card for Actions on Google.
            https://developers.google.com/actions/assistant/responses#browsing_carousel

            Attributes:
                items (Sequence[google.cloud.dialogflow_v2.types.Intent.Message.BrowseCarouselCard.BrowseCarouselCardItem]):
                    Required. List of items in the Browse
                    Carousel Card. Minimum of two items, maximum of
                    ten.
                image_display_options (google.cloud.dialogflow_v2.types.Intent.Message.BrowseCarouselCard.ImageDisplayOptions):
                    Optional. Settings for displaying the image. Applies to
                    every image in
                    [items][google.cloud.dialogflow.v2.Intent.Message.BrowseCarouselCard.items].
            """

            class ImageDisplayOptions(proto.Enum):
                r"""Image display options for Actions on Google. This should be
                used for when the image's aspect ratio does not match the image
                container's aspect ratio.
                """
                IMAGE_DISPLAY_OPTIONS_UNSPECIFIED = 0
                GRAY = 1
                WHITE = 2
                CROPPED = 3
                BLURRED_BACKGROUND = 4

            class BrowseCarouselCardItem(proto.Message):
                r"""Browsing carousel tile
                Attributes:
                    open_uri_action (google.cloud.dialogflow_v2.types.Intent.Message.BrowseCarouselCard.BrowseCarouselCardItem.OpenUrlAction):
                        Required. Action to present to the user.
                    title (str):
                        Required. Title of the carousel item. Maximum
                        of two lines of text.
                    description (str):
                        Optional. Description of the carousel item.
                        Maximum of four lines of text.
                    image (google.cloud.dialogflow_v2.types.Intent.Message.Image):
                        Optional. Hero image for the carousel item.
                    footer (str):
                        Optional. Text that appears at the bottom of
                        the Browse Carousel Card. Maximum of one line of
                        text.
                """

                class OpenUrlAction(proto.Message):
                    r"""Actions on Google action to open a given url.
                    Attributes:
                        url (str):
                            Required. URL
                        url_type_hint (google.cloud.dialogflow_v2.types.Intent.Message.BrowseCarouselCard.BrowseCarouselCardItem.OpenUrlAction.UrlTypeHint):
                            Optional. Specifies the type of viewer that
                            is used when opening the URL. Defaults to
                            opening via web browser.
                    """

                    class UrlTypeHint(proto.Enum):
                        r"""Type of the URI."""
                        URL_TYPE_HINT_UNSPECIFIED = 0
                        AMP_ACTION = 1
                        AMP_CONTENT = 2

                    url = proto.Field(proto.STRING, number=1,)
                    url_type_hint = proto.Field(
                        proto.ENUM,
                        number=3,
                        enum="Intent.Message.BrowseCarouselCard.BrowseCarouselCardItem.OpenUrlAction.UrlTypeHint",
                    )

                open_uri_action = proto.Field(
                    proto.MESSAGE,
                    number=1,
                    message="Intent.Message.BrowseCarouselCard.BrowseCarouselCardItem.OpenUrlAction",
                )
                title = proto.Field(proto.STRING, number=2,)
                description = proto.Field(proto.STRING, number=3,)
                image = proto.Field(
                    proto.MESSAGE, number=4, message="Intent.Message.Image",
                )
                footer = proto.Field(proto.STRING, number=5,)

            items = proto.RepeatedField(
                proto.MESSAGE,
                number=1,
                message="Intent.Message.BrowseCarouselCard.BrowseCarouselCardItem",
            )
            image_display_options = proto.Field(
                proto.ENUM,
                number=2,
                enum="Intent.Message.BrowseCarouselCard.ImageDisplayOptions",
            )

        class TableCard(proto.Message):
            r"""Table card for Actions on Google.
            Attributes:
                title (str):
                    Required. Title of the card.
                subtitle (str):
                    Optional. Subtitle to the title.
                image (google.cloud.dialogflow_v2.types.Intent.Message.Image):
                    Optional. Image which should be displayed on
                    the card.
                column_properties (Sequence[google.cloud.dialogflow_v2.types.Intent.Message.ColumnProperties]):
                    Optional. Display properties for the columns
                    in this table.
                rows (Sequence[google.cloud.dialogflow_v2.types.Intent.Message.TableCardRow]):
                    Optional. Rows in this table of data.
                buttons (Sequence[google.cloud.dialogflow_v2.types.Intent.Message.BasicCard.Button]):
                    Optional. List of buttons for the card.
            """

            title = proto.Field(proto.STRING, number=1,)
            subtitle = proto.Field(proto.STRING, number=2,)
            image = proto.Field(
                proto.MESSAGE, number=3, message="Intent.Message.Image",
            )
            column_properties = proto.RepeatedField(
                proto.MESSAGE, number=4, message="Intent.Message.ColumnProperties",
            )
            rows = proto.RepeatedField(
                proto.MESSAGE, number=5, message="Intent.Message.TableCardRow",
            )
            buttons = proto.RepeatedField(
                proto.MESSAGE, number=6, message="Intent.Message.BasicCard.Button",
            )

        class ColumnProperties(proto.Message):
            r"""Column properties for
            [TableCard][google.cloud.dialogflow.v2.Intent.Message.TableCard].

            Attributes:
                header (str):
                    Required. Column heading.
                horizontal_alignment (google.cloud.dialogflow_v2.types.Intent.Message.ColumnProperties.HorizontalAlignment):
                    Optional. Defines text alignment for all
                    cells in this column.
            """

            class HorizontalAlignment(proto.Enum):
                r"""Text alignments within a cell."""
                HORIZONTAL_ALIGNMENT_UNSPECIFIED = 0
                LEADING = 1
                CENTER = 2
                TRAILING = 3

            header = proto.Field(proto.STRING, number=1,)
            horizontal_alignment = proto.Field(
                proto.ENUM,
                number=2,
                enum="Intent.Message.ColumnProperties.HorizontalAlignment",
            )

        class TableCardRow(proto.Message):
            r"""Row of
            [TableCard][google.cloud.dialogflow.v2.Intent.Message.TableCard].

            Attributes:
                cells (Sequence[google.cloud.dialogflow_v2.types.Intent.Message.TableCardCell]):
                    Optional. List of cells that make up this
                    row.
                divider_after (bool):
                    Optional. Whether to add a visual divider
                    after this row.
            """

            cells = proto.RepeatedField(
                proto.MESSAGE, number=1, message="Intent.Message.TableCardCell",
            )
            divider_after = proto.Field(proto.BOOL, number=2,)

        class TableCardCell(proto.Message):
            r"""Cell of
            [TableCardRow][google.cloud.dialogflow.v2.Intent.Message.TableCardRow].

            Attributes:
                text (str):
                    Required. Text in this cell.
            """

            text = proto.Field(proto.STRING, number=1,)

        text = proto.Field(
            proto.MESSAGE, number=1, oneof="message", message="Intent.Message.Text",
        )
        image = proto.Field(
            proto.MESSAGE, number=2, oneof="message", message="Intent.Message.Image",
        )
        quick_replies = proto.Field(
            proto.MESSAGE,
            number=3,
            oneof="message",
            message="Intent.Message.QuickReplies",
        )
        card = proto.Field(
            proto.MESSAGE, number=4, oneof="message", message="Intent.Message.Card",
        )
        payload = proto.Field(
            proto.MESSAGE, number=5, oneof="message", message=struct_pb2.Struct,
        )
        simple_responses = proto.Field(
            proto.MESSAGE,
            number=7,
            oneof="message",
            message="Intent.Message.SimpleResponses",
        )
        basic_card = proto.Field(
            proto.MESSAGE,
            number=8,
            oneof="message",
            message="Intent.Message.BasicCard",
        )
        suggestions = proto.Field(
            proto.MESSAGE,
            number=9,
            oneof="message",
            message="Intent.Message.Suggestions",
        )
        link_out_suggestion = proto.Field(
            proto.MESSAGE,
            number=10,
            oneof="message",
            message="Intent.Message.LinkOutSuggestion",
        )
        list_select = proto.Field(
            proto.MESSAGE,
            number=11,
            oneof="message",
            message="Intent.Message.ListSelect",
        )
        carousel_select = proto.Field(
            proto.MESSAGE,
            number=12,
            oneof="message",
            message="Intent.Message.CarouselSelect",
        )
        browse_carousel_card = proto.Field(
            proto.MESSAGE,
            number=22,
            oneof="message",
            message="Intent.Message.BrowseCarouselCard",
        )
        table_card = proto.Field(
            proto.MESSAGE,
            number=23,
            oneof="message",
            message="Intent.Message.TableCard",
        )
        media_content = proto.Field(
            proto.MESSAGE,
            number=24,
            oneof="message",
            message="Intent.Message.MediaContent",
        )
        platform = proto.Field(proto.ENUM, number=6, enum="Intent.Message.Platform",)

    class FollowupIntentInfo(proto.Message):
        r"""Represents a single followup intent in the chain.
        Attributes:
            followup_intent_name (str):
                The unique identifier of the followup intent. Format:
                ``projects/<Project ID>/agent/intents/<Intent ID>``.
            parent_followup_intent_name (str):
                The unique identifier of the followup intent's parent.
                Format: ``projects/<Project ID>/agent/intents/<Intent ID>``.
        """

        followup_intent_name = proto.Field(proto.STRING, number=1,)
        parent_followup_intent_name = proto.Field(proto.STRING, number=2,)

    name = proto.Field(proto.STRING, number=1,)
    display_name = proto.Field(proto.STRING, number=2,)
    webhook_state = proto.Field(proto.ENUM, number=6, enum=WebhookState,)
    priority = proto.Field(proto.INT32, number=3,)
    is_fallback = proto.Field(proto.BOOL, number=4,)
    ml_disabled = proto.Field(proto.BOOL, number=19,)
    live_agent_handoff = proto.Field(proto.BOOL, number=20,)
    end_interaction = proto.Field(proto.BOOL, number=21,)
    input_context_names = proto.RepeatedField(proto.STRING, number=7,)
    events = proto.RepeatedField(proto.STRING, number=8,)
    training_phrases = proto.RepeatedField(
        proto.MESSAGE, number=9, message=TrainingPhrase,
    )
    action = proto.Field(proto.STRING, number=10,)
    output_contexts = proto.RepeatedField(
        proto.MESSAGE, number=11, message=context.Context,
    )
    reset_contexts = proto.Field(proto.BOOL, number=12,)
    parameters = proto.RepeatedField(proto.MESSAGE, number=13, message=Parameter,)
    messages = proto.RepeatedField(proto.MESSAGE, number=14, message=Message,)
    default_response_platforms = proto.RepeatedField(
        proto.ENUM, number=15, enum=Message.Platform,
    )
    root_followup_intent_name = proto.Field(proto.STRING, number=16,)
    parent_followup_intent_name = proto.Field(proto.STRING, number=17,)
    followup_intent_info = proto.RepeatedField(
        proto.MESSAGE, number=18, message=FollowupIntentInfo,
    )


class ListIntentsRequest(proto.Message):
    r"""The request message for
    [Intents.ListIntents][google.cloud.dialogflow.v2.Intents.ListIntents].

    Attributes:
        parent (str):
            Required. The agent to list all intents from. Format:
            ``projects/<Project ID>/agent`` or
            ``projects/<Project ID>/locations/<Location ID>/agent``.

            Alternatively, you can specify the environment to list
            intents for. Format:
            ``projects/<Project ID>/agent/environments/<Environment ID>``
            or
            ``projects/<Project ID>/locations/<Location ID>/agent/environments/<Environment ID>``.
            Note: training phrases of the intents will not be returned
            for non-draft environment.
        language_code (str):
            Optional. The language used to access language-specific
            data. If not specified, the agent's default language is
            used. For more information, see `Multilingual intent and
            entity
            data <https://cloud.google.com/dialogflow/docs/agents-multilingual#intent-entity>`__.
        intent_view (google.cloud.dialogflow_v2.types.IntentView):
            Optional. The resource view to apply to the
            returned intent.
        page_size (int):
            Optional. The maximum number of items to
            return in a single page. By default 100 and at
            most 1000.
        page_token (str):
            Optional. The next_page_token value returned from a previous
            list request.
    """

    parent = proto.Field(proto.STRING, number=1,)
    language_code = proto.Field(proto.STRING, number=2,)
    intent_view = proto.Field(proto.ENUM, number=3, enum="IntentView",)
    page_size = proto.Field(proto.INT32, number=4,)
    page_token = proto.Field(proto.STRING, number=5,)


class ListIntentsResponse(proto.Message):
    r"""The response message for
    [Intents.ListIntents][google.cloud.dialogflow.v2.Intents.ListIntents].

    Attributes:
        intents (Sequence[google.cloud.dialogflow_v2.types.Intent]):
            The list of agent intents. There will be a maximum number of
            items returned based on the page_size field in the request.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
    """

    @property
    def raw_page(self):
        return self

    intents = proto.RepeatedField(proto.MESSAGE, number=1, message="Intent",)
    next_page_token = proto.Field(proto.STRING, number=2,)


class GetIntentRequest(proto.Message):
    r"""The request message for
    [Intents.GetIntent][google.cloud.dialogflow.v2.Intents.GetIntent].

    Attributes:
        name (str):
            Required. The name of the intent. Format:
            ``projects/<Project ID>/agent/intents/<Intent ID>``.
        language_code (str):
            Optional. The language used to access language-specific
            data. If not specified, the agent's default language is
            used. For more information, see `Multilingual intent and
            entity
            data <https://cloud.google.com/dialogflow/docs/agents-multilingual#intent-entity>`__.
        intent_view (google.cloud.dialogflow_v2.types.IntentView):
            Optional. The resource view to apply to the
            returned intent.
    """

    name = proto.Field(proto.STRING, number=1,)
    language_code = proto.Field(proto.STRING, number=2,)
    intent_view = proto.Field(proto.ENUM, number=3, enum="IntentView",)


class CreateIntentRequest(proto.Message):
    r"""The request message for
    [Intents.CreateIntent][google.cloud.dialogflow.v2.Intents.CreateIntent].

    Attributes:
        parent (str):
            Required. The agent to create a intent for. Format:
            ``projects/<Project ID>/agent``.
        intent (google.cloud.dialogflow_v2.types.Intent):
            Required. The intent to create.
        language_code (str):
            Optional. The language used to access language-specific
            data. If not specified, the agent's default language is
            used. For more information, see `Multilingual intent and
            entity
            data <https://cloud.google.com/dialogflow/docs/agents-multilingual#intent-entity>`__.
        intent_view (google.cloud.dialogflow_v2.types.IntentView):
            Optional. The resource view to apply to the
            returned intent.
    """

    parent = proto.Field(proto.STRING, number=1,)
    intent = proto.Field(proto.MESSAGE, number=2, message="Intent",)
    language_code = proto.Field(proto.STRING, number=3,)
    intent_view = proto.Field(proto.ENUM, number=4, enum="IntentView",)


class UpdateIntentRequest(proto.Message):
    r"""The request message for
    [Intents.UpdateIntent][google.cloud.dialogflow.v2.Intents.UpdateIntent].

    Attributes:
        intent (google.cloud.dialogflow_v2.types.Intent):
            Required. The intent to update.
        language_code (str):
            Optional. The language used to access language-specific
            data. If not specified, the agent's default language is
            used. For more information, see `Multilingual intent and
            entity
            data <https://cloud.google.com/dialogflow/docs/agents-multilingual#intent-entity>`__.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Optional. The mask to control which fields
            get updated.
        intent_view (google.cloud.dialogflow_v2.types.IntentView):
            Optional. The resource view to apply to the
            returned intent.
    """

    intent = proto.Field(proto.MESSAGE, number=1, message="Intent",)
    language_code = proto.Field(proto.STRING, number=2,)
    update_mask = proto.Field(
        proto.MESSAGE, number=3, message=field_mask_pb2.FieldMask,
    )
    intent_view = proto.Field(proto.ENUM, number=4, enum="IntentView",)


class DeleteIntentRequest(proto.Message):
    r"""The request message for
    [Intents.DeleteIntent][google.cloud.dialogflow.v2.Intents.DeleteIntent].

    Attributes:
        name (str):
            Required. The name of the intent to delete. If this intent
            has direct or indirect followup intents, we also delete
            them. Format:
            ``projects/<Project ID>/agent/intents/<Intent ID>``.
    """

    name = proto.Field(proto.STRING, number=1,)


class BatchUpdateIntentsRequest(proto.Message):
    r"""
    Attributes:
        parent (str):
            Required. The name of the agent to update or create intents
            in. Format: ``projects/<Project ID>/agent``.
        intent_batch_uri (str):
            The URI to a Google Cloud Storage file
            containing intents to update or create. The file
            format can either be a serialized proto (of
            IntentBatch type) or JSON object. Note: The URI
            must start with "gs://".
        intent_batch_inline (google.cloud.dialogflow_v2.types.IntentBatch):
            The collection of intents to update or
            create.
        language_code (str):
            Optional. The language used to access language-specific
            data. If not specified, the agent's default language is
            used. For more information, see `Multilingual intent and
            entity
            data <https://cloud.google.com/dialogflow/docs/agents-multilingual#intent-entity>`__.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Optional. The mask to control which fields
            get updated.
        intent_view (google.cloud.dialogflow_v2.types.IntentView):
            Optional. The resource view to apply to the
            returned intent.
    """

    parent = proto.Field(proto.STRING, number=1,)
    intent_batch_uri = proto.Field(proto.STRING, number=2, oneof="intent_batch",)
    intent_batch_inline = proto.Field(
        proto.MESSAGE, number=3, oneof="intent_batch", message="IntentBatch",
    )
    language_code = proto.Field(proto.STRING, number=4,)
    update_mask = proto.Field(
        proto.MESSAGE, number=5, message=field_mask_pb2.FieldMask,
    )
    intent_view = proto.Field(proto.ENUM, number=6, enum="IntentView",)


class BatchUpdateIntentsResponse(proto.Message):
    r"""The response message for
    [Intents.BatchUpdateIntents][google.cloud.dialogflow.v2.Intents.BatchUpdateIntents].

    Attributes:
        intents (Sequence[google.cloud.dialogflow_v2.types.Intent]):
            The collection of updated or created intents.
    """

    intents = proto.RepeatedField(proto.MESSAGE, number=1, message="Intent",)


class BatchDeleteIntentsRequest(proto.Message):
    r"""The request message for
    [Intents.BatchDeleteIntents][google.cloud.dialogflow.v2.Intents.BatchDeleteIntents].

    Attributes:
        parent (str):
            Required. The name of the agent to delete all entities types
            for. Format: ``projects/<Project ID>/agent``.
        intents (Sequence[google.cloud.dialogflow_v2.types.Intent]):
            Required. The collection of intents to delete. Only intent
            ``name`` must be filled in.
    """

    parent = proto.Field(proto.STRING, number=1,)
    intents = proto.RepeatedField(proto.MESSAGE, number=2, message="Intent",)


class IntentBatch(proto.Message):
    r"""This message is a wrapper around a collection of intents.
    Attributes:
        intents (Sequence[google.cloud.dialogflow_v2.types.Intent]):
            A collection of intents.
    """

    intents = proto.RepeatedField(proto.MESSAGE, number=1, message="Intent",)


__all__ = tuple(sorted(__protobuf__.manifest))
