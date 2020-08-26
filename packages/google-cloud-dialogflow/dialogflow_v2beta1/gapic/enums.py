# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Wrappers for protocol buffer enum types."""

import enum


class AudioEncoding(enum.IntEnum):
    """
    Audio encoding of the audio content sent in the conversational query
    request. Refer to the `Cloud Speech API
    documentation <https://cloud.google.com/speech-to-text/docs/basics>`__
    for more details.

    Attributes:
      AUDIO_ENCODING_UNSPECIFIED (int): Not specified.
      AUDIO_ENCODING_LINEAR_16 (int): Uncompressed 16-bit signed little-endian samples (Linear PCM).
      AUDIO_ENCODING_FLAC (int): ```FLAC`` <https://xiph.org/flac/documentation.html>`__ (Free
      Lossless Audio Codec) is the recommended encoding because it is lossless
      (therefore recognition is not compromised) and requires only about half
      the bandwidth of ``LINEAR16``. ``FLAC`` stream encoding supports 16-bit
      and 24-bit samples, however, not all fields in ``STREAMINFO`` are
      supported.
      AUDIO_ENCODING_MULAW (int): 8-bit samples that compand 14-bit audio samples using G.711 PCMU/mu-law.
      AUDIO_ENCODING_AMR (int): Adaptive Multi-Rate Narrowband codec. ``sample_rate_hertz`` must be
      8000.
      AUDIO_ENCODING_AMR_WB (int): Adaptive Multi-Rate Wideband codec. ``sample_rate_hertz`` must be
      16000.
      AUDIO_ENCODING_OGG_OPUS (int): Opus encoded audio frames in Ogg container
      (`OggOpus <https://wiki.xiph.org/OggOpus>`__). ``sample_rate_hertz``
      must be 16000.
      AUDIO_ENCODING_SPEEX_WITH_HEADER_BYTE (int): Although the use of lossy encodings is not recommended, if a very
      low bitrate encoding is required, ``OGG_OPUS`` is highly preferred over
      Speex encoding. The `Speex <https://speex.org/>`__ encoding supported by
      Dialogflow API has a header byte in each block, as in MIME type
      ``audio/x-speex-with-header-byte``. It is a variant of the RTP Speex
      encoding defined in `RFC 5574 <https://tools.ietf.org/html/rfc5574>`__.
      The stream is a sequence of blocks, one block per RTP packet. Each block
      starts with a byte containing the length of the block, in bytes,
      followed by one or more frames of Speex data, padded to an integral
      number of bytes (octets) as specified in RFC 5574. In other words, each
      RTP header is replaced with a single byte containing the block length.
      Only Speex wideband is supported. ``sample_rate_hertz`` must be 16000.
    """

    AUDIO_ENCODING_UNSPECIFIED = 0
    AUDIO_ENCODING_LINEAR_16 = 1
    AUDIO_ENCODING_FLAC = 2
    AUDIO_ENCODING_MULAW = 3
    AUDIO_ENCODING_AMR = 4
    AUDIO_ENCODING_AMR_WB = 5
    AUDIO_ENCODING_OGG_OPUS = 6
    AUDIO_ENCODING_SPEEX_WITH_HEADER_BYTE = 7


class IntentView(enum.IntEnum):
    """
    Represents the options for views of an intent.
    An intent can be a sizable object. Therefore, we provide a resource view that
    does not return training phrases in the response by default.

    Attributes:
      INTENT_VIEW_UNSPECIFIED (int): Training phrases field is not populated in the response.
      INTENT_VIEW_FULL (int): All fields are populated.
    """

    INTENT_VIEW_UNSPECIFIED = 0
    INTENT_VIEW_FULL = 1


class NullValue(enum.IntEnum):
    """
    ``NullValue`` is a singleton enumeration to represent the null value
    for the ``Value`` type union.

    The JSON representation for ``NullValue`` is JSON ``null``.

    Attributes:
      NULL_VALUE (int): Null value.
    """

    NULL_VALUE = 0


class OutputAudioEncoding(enum.IntEnum):
    """
    Audio encoding of the output audio format in Text-To-Speech.

    Attributes:
      OUTPUT_AUDIO_ENCODING_UNSPECIFIED (int): Not specified.
      OUTPUT_AUDIO_ENCODING_LINEAR_16 (int): Uncompressed 16-bit signed little-endian samples (Linear PCM).
      Audio content returned as LINEAR16 also contains a WAV header.
      OUTPUT_AUDIO_ENCODING_MP3 (int): MP3 audio at 32kbps.
      OUTPUT_AUDIO_ENCODING_OGG_OPUS (int): Opus encoded audio wrapped in an ogg container. The result will be a
      file which can be played natively on Android, and in browsers (at least
      Chrome and Firefox). The quality of the encoding is considerably higher
      than MP3 while using approximately the same bitrate.
    """

    OUTPUT_AUDIO_ENCODING_UNSPECIFIED = 0
    OUTPUT_AUDIO_ENCODING_LINEAR_16 = 1
    OUTPUT_AUDIO_ENCODING_MP3 = 2
    OUTPUT_AUDIO_ENCODING_OGG_OPUS = 3


class SpeechModelVariant(enum.IntEnum):
    """
    Variant of the specified ``Speech model`` to use.

    See the `Cloud Speech
    documentation <https://cloud.google.com/speech-to-text/docs/enhanced-models>`__
    for which models have different variants. For example, the "phone_call"
    model has both a standard and an enhanced variant. When you use an
    enhanced model, you will generally receive higher quality results than
    for a standard model.

    Attributes:
      SPEECH_MODEL_VARIANT_UNSPECIFIED (int): No model variant specified. In this case Dialogflow defaults to
      USE_BEST_AVAILABLE.
      USE_BEST_AVAILABLE (int): Use the best available variant of the ``Speech model`` that the
      caller is eligible for.

      Please see the `Dialogflow
      docs <https://cloud.google.com/dialogflow/docs/data-logging>`__ for how
      to make your project eligible for enhanced models.
      USE_STANDARD (int): Use standard model variant even if an enhanced model is available.
      See the `Cloud Speech
      documentation <https://cloud.google.com/speech-to-text/docs/enhanced-models>`__
      for details about enhanced models.
      USE_ENHANCED (int): Use an enhanced model variant:

      -  If an enhanced variant does not exist for the given ``model`` and
         request language, Dialogflow falls back to the standard variant.

         The `Cloud Speech
         documentation <https://cloud.google.com/speech-to-text/docs/enhanced-models>`__
         describes which models have enhanced variants.

      -  If the API caller isn't eligible for enhanced models, Dialogflow
         returns an error. Please see the `Dialogflow
         docs <https://cloud.google.com/dialogflow/docs/data-logging>`__ for
         how to make your project eligible.
    """

    SPEECH_MODEL_VARIANT_UNSPECIFIED = 0
    USE_BEST_AVAILABLE = 1
    USE_STANDARD = 2
    USE_ENHANCED = 3


class SsmlVoiceGender(enum.IntEnum):
    """
    Gender of the voice as described in `SSML voice
    element <https://www.w3.org/TR/speech-synthesis11/#edef_voice>`__.

    Attributes:
      SSML_VOICE_GENDER_UNSPECIFIED (int): An unspecified gender, which means that the client doesn't care which
      gender the selected voice will have.
      SSML_VOICE_GENDER_MALE (int): A male voice.
      SSML_VOICE_GENDER_FEMALE (int): A female voice.
      SSML_VOICE_GENDER_NEUTRAL (int): A gender-neutral voice.
    """

    SSML_VOICE_GENDER_UNSPECIFIED = 0
    SSML_VOICE_GENDER_MALE = 1
    SSML_VOICE_GENDER_FEMALE = 2
    SSML_VOICE_GENDER_NEUTRAL = 3


class Agent(object):
    class ApiVersion(enum.IntEnum):
        """
        API version for the agent.

        Attributes:
          API_VERSION_UNSPECIFIED (int): Not specified.
          API_VERSION_V1 (int): Legacy V1 API.
          API_VERSION_V2 (int): V2 API.
          API_VERSION_V2_BETA_1 (int): V2beta1 API.
        """

        API_VERSION_UNSPECIFIED = 0
        API_VERSION_V1 = 1
        API_VERSION_V2 = 2
        API_VERSION_V2_BETA_1 = 3

    class MatchMode(enum.IntEnum):
        """
        Match mode determines how intents are detected from user queries.

        Attributes:
          MATCH_MODE_UNSPECIFIED (int): Not specified.
          MATCH_MODE_HYBRID (int): Best for agents with a small number of examples in intents and/or wide
          use of templates syntax and composite entities.
          MATCH_MODE_ML_ONLY (int): Can be used for agents with a large number of examples in intents,
          especially the ones using @sys.any or very large custom entities.
        """

        MATCH_MODE_UNSPECIFIED = 0
        MATCH_MODE_HYBRID = 1
        MATCH_MODE_ML_ONLY = 2

    class Tier(enum.IntEnum):
        """
        Represents the agent tier.

        Attributes:
          TIER_UNSPECIFIED (int): Not specified. This value should never be used.
          TIER_STANDARD (int): Standard tier.
          TIER_ENTERPRISE (int): Enterprise tier (Essentials).
          TIER_ENTERPRISE_PLUS (int): Enterprise tier (Plus).
        """

        TIER_UNSPECIFIED = 0
        TIER_STANDARD = 1
        TIER_ENTERPRISE = 2
        TIER_ENTERPRISE_PLUS = 3


class Document(object):
    class KnowledgeType(enum.IntEnum):
        """
        The knowledge type of document content.

        Attributes:
          KNOWLEDGE_TYPE_UNSPECIFIED (int): The type is unspecified or arbitrary.
          FAQ (int): The document content contains question and answer pairs as either HTML or
          CSV. Typical FAQ HTML formats are parsed accurately, but unusual formats
          may fail to be parsed.

          CSV must have questions in the first column and answers in the second,
          with no header. Because of this explicit format, they are always parsed
          accurately.
          EXTRACTIVE_QA (int): Documents for which unstructured text is extracted and used for
          question answering.
        """

        KNOWLEDGE_TYPE_UNSPECIFIED = 0
        FAQ = 1
        EXTRACTIVE_QA = 2


class EntityType(object):
    class AutoExpansionMode(enum.IntEnum):
        """
        Represents different entity type expansion modes. Automated expansion
        allows an agent to recognize values that have not been explicitly listed in
        the entity (for example, new kinds of shopping list items).

        Attributes:
          AUTO_EXPANSION_MODE_UNSPECIFIED (int): Auto expansion disabled for the entity.
          AUTO_EXPANSION_MODE_DEFAULT (int): Allows an agent to recognize values that have not been explicitly
          listed in the entity.
        """

        AUTO_EXPANSION_MODE_UNSPECIFIED = 0
        AUTO_EXPANSION_MODE_DEFAULT = 1

    class Kind(enum.IntEnum):
        """
        Represents kinds of entities.

        Attributes:
          KIND_UNSPECIFIED (int): Not specified. This value should be never used.
          KIND_MAP (int): Map entity types allow mapping of a group of synonyms to a reference
          value.
          KIND_LIST (int): List entity types contain a set of entries that do not map to reference
          values. However, list entity types can contain references to other entity
          types (with or without aliases).
          KIND_REGEXP (int): Regexp entity types allow to specify regular expressions in entries
          values.
        """

        KIND_UNSPECIFIED = 0
        KIND_MAP = 1
        KIND_LIST = 2
        KIND_REGEXP = 3


class Environment(object):
    class State(enum.IntEnum):
        """
        Represents an environment state. When an environment is pointed to a
        new agent version, the environment is temporarily set to the ``LOADING``
        state. During that time, the environment keeps on serving the previous
        version of the agent. After the new agent version is done loading, the
        environment is set back to the ``RUNNING`` state.

        Attributes:
          STATE_UNSPECIFIED (int): Not specified. This value is not used.
          STOPPED (int): Stopped.
          LOADING (int): Loading.
          RUNNING (int): Running.
        """

        STATE_UNSPECIFIED = 0
        STOPPED = 1
        LOADING = 2
        RUNNING = 3


class Intent(object):
    class WebhookState(enum.IntEnum):
        """
        Represents the different states that webhooks can be in.

        Attributes:
          WEBHOOK_STATE_UNSPECIFIED (int): Webhook is disabled in the agent and in the intent.
          WEBHOOK_STATE_ENABLED (int): Webhook is enabled in the agent and in the intent.
          WEBHOOK_STATE_ENABLED_FOR_SLOT_FILLING (int): Webhook is enabled in the agent and in the intent. Also, each slot
          filling prompt is forwarded to the webhook.
        """

        WEBHOOK_STATE_UNSPECIFIED = 0
        WEBHOOK_STATE_ENABLED = 1
        WEBHOOK_STATE_ENABLED_FOR_SLOT_FILLING = 2

    class TrainingPhrase(object):
        class Type(enum.IntEnum):
            """
            Represents different types of training phrases.

            Attributes:
              TYPE_UNSPECIFIED (int): Not specified. This value should never be used.
              EXAMPLE (int): Examples do not contain @-prefixed entity type names, but example parts
              can be annotated with entity types.
              TEMPLATE (int): Templates are not annotated with entity types, but they can contain
              @-prefixed entity type names as substrings.
              Template mode has been deprecated. Example mode is the only supported
              way to create new training phrases. If you have existing training
              phrases that you've created in template mode, those will continue to
              work.
            """

            TYPE_UNSPECIFIED = 0
            EXAMPLE = 1
            TEMPLATE = 2

    class Message(object):
        class Platform(enum.IntEnum):
            """
            Represents different platforms that a rich message can be intended for.

            Attributes:
              PLATFORM_UNSPECIFIED (int): Not specified.
              FACEBOOK (int): Facebook.
              SLACK (int): Slack.
              TELEGRAM (int): Telegram.
              KIK (int): Kik.
              SKYPE (int): Skype.
              LINE (int): Line.
              VIBER (int): Viber.
              ACTIONS_ON_GOOGLE (int): Google Assistant See `Dialogflow webhook
              format <https://developers.google.com/assistant/actions/build/json/dialogflow-webhook-json>`__
              TELEPHONY (int): Telephony Gateway.
              GOOGLE_HANGOUTS (int): Google Hangouts.
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
            TELEPHONY = 10
            GOOGLE_HANGOUTS = 11

        class RbmCarouselCard(object):
            class CardWidth(enum.IntEnum):
                """
                The width of the cards in the carousel.

                Attributes:
                  CARD_WIDTH_UNSPECIFIED (int): Not specified.
                  SMALL (int): 120 DP. Note that tall media cannot be used.
                  MEDIUM (int): 232 DP.
                """

                CARD_WIDTH_UNSPECIFIED = 0
                SMALL = 1
                MEDIUM = 2

        class RbmStandaloneCard(object):
            class CardOrientation(enum.IntEnum):
                """
                Orientation of the card.

                Attributes:
                  CARD_ORIENTATION_UNSPECIFIED (int): Not specified.
                  HORIZONTAL (int): Horizontal layout.
                  VERTICAL (int): Vertical layout.
                """

                CARD_ORIENTATION_UNSPECIFIED = 0
                HORIZONTAL = 1
                VERTICAL = 2

            class ThumbnailImageAlignment(enum.IntEnum):
                """
                Thumbnail preview alignment for standalone cards with horizontal
                layout.

                Attributes:
                  THUMBNAIL_IMAGE_ALIGNMENT_UNSPECIFIED (int): Not specified.
                  LEFT (int): Thumbnail preview is left-aligned.
                  RIGHT (int): Thumbnail preview is right-aligned.
                """

                THUMBNAIL_IMAGE_ALIGNMENT_UNSPECIFIED = 0
                LEFT = 1
                RIGHT = 2

        class RbmCardContent(object):
            class RbmMedia(object):
                class Height(enum.IntEnum):
                    """
                    Media height

                    Attributes:
                      HEIGHT_UNSPECIFIED (int): Not specified.
                      SHORT (int): 112 DP.
                      MEDIUM (int): 168 DP.
                      TALL (int): 264 DP. Not available for rich card carousels when the card width
                      is set to small.
                    """

                    HEIGHT_UNSPECIFIED = 0
                    SHORT = 1
                    MEDIUM = 2
                    TALL = 3

        class MediaContent(object):
            class ResponseMediaType(enum.IntEnum):
                """
                Format of response media type.

                Attributes:
                  RESPONSE_MEDIA_TYPE_UNSPECIFIED (int): Unspecified.
                  AUDIO (int): Response media type is audio.
                """

                RESPONSE_MEDIA_TYPE_UNSPECIFIED = 0
                AUDIO = 1

        class BrowseCarouselCard(object):
            class ImageDisplayOptions(enum.IntEnum):
                """
                Image display options for Actions on Google. This should be used for
                when the image's aspect ratio does not match the image container's
                aspect ratio.

                Attributes:
                  IMAGE_DISPLAY_OPTIONS_UNSPECIFIED (int): Fill the gaps between the image and the image container with gray
                  bars.
                  GRAY (int): Fill the gaps between the image and the image container with gray
                  bars.
                  WHITE (int): Fill the gaps between the image and the image container with white
                  bars.
                  CROPPED (int): Image is scaled such that the image width and height match or exceed
                  the container dimensions. This may crop the top and bottom of the
                  image if the scaled image height is greater than the container
                  height, or crop the left and right of the image if the scaled image
                  width is greater than the container width. This is similar to "Zoom
                  Mode" on a widescreen TV when playing a 4:3 video.
                  BLURRED_BACKGROUND (int): Pad the gaps between image and image frame with a blurred copy of the
                  same image.
                """

                IMAGE_DISPLAY_OPTIONS_UNSPECIFIED = 0
                GRAY = 1
                WHITE = 2
                CROPPED = 3
                BLURRED_BACKGROUND = 4

            class BrowseCarouselCardItem(object):
                class OpenUrlAction(object):
                    class UrlTypeHint(enum.IntEnum):
                        """
                        Type of the URI.

                        Attributes:
                          URL_TYPE_HINT_UNSPECIFIED (int): Unspecified
                          AMP_ACTION (int): Url would be an amp action
                          AMP_CONTENT (int): URL that points directly to AMP content, or to a canonical URL
                          which refers to AMP content via <link rel="amphtml">.
                        """

                        URL_TYPE_HINT_UNSPECIFIED = 0
                        AMP_ACTION = 1
                        AMP_CONTENT = 2

        class ColumnProperties(object):
            class HorizontalAlignment(enum.IntEnum):
                """
                Text alignments within a cell.

                Attributes:
                  HORIZONTAL_ALIGNMENT_UNSPECIFIED (int): Text is aligned to the leading edge of the column.
                  LEADING (int): Text is aligned to the leading edge of the column.
                  CENTER (int): Text is centered in the column.
                  TRAILING (int): Text is aligned to the trailing edge of the column.
                """

                HORIZONTAL_ALIGNMENT_UNSPECIFIED = 0
                LEADING = 1
                CENTER = 2
                TRAILING = 3


class KnowledgeAnswers(object):
    class Answer(object):
        class MatchConfidenceLevel(enum.IntEnum):
            """
            Represents the system's confidence that this knowledge answer is a good
            match for this conversational query.

            Attributes:
              MATCH_CONFIDENCE_LEVEL_UNSPECIFIED (int): Not specified.
              LOW (int): Indicates that the confidence is low.
              MEDIUM (int): Indicates our confidence is medium.
              HIGH (int): Indicates our confidence is high.
            """

            MATCH_CONFIDENCE_LEVEL_UNSPECIFIED = 0
            LOW = 1
            MEDIUM = 2
            HIGH = 3


class KnowledgeOperationMetadata(object):
    class State(enum.IntEnum):
        """
        States of the operation.

        Attributes:
          STATE_UNSPECIFIED (int): State unspecified.
          PENDING (int): The operation has been created.
          RUNNING (int): The operation is currently running.
          DONE (int): The operation is done, either cancelled or completed.
        """

        STATE_UNSPECIFIED = 0
        PENDING = 1
        RUNNING = 2
        DONE = 3


class SessionEntityType(object):
    class EntityOverrideMode(enum.IntEnum):
        """
        The types of modifications for a session entity type.

        Attributes:
          ENTITY_OVERRIDE_MODE_UNSPECIFIED (int): Not specified. This value should be never used.
          ENTITY_OVERRIDE_MODE_OVERRIDE (int): The collection of session entities overrides the collection of entities
          in the corresponding custom entity type.
          ENTITY_OVERRIDE_MODE_SUPPLEMENT (int): The collection of session entities extends the collection of
          entities in the corresponding custom entity type.

          Note: Even in this override mode calls to ``ListSessionEntityTypes``,
          ``GetSessionEntityType``, ``CreateSessionEntityType`` and
          ``UpdateSessionEntityType`` only return the additional entities added in
          this session entity type. If you want to get the supplemented list,
          please call ``EntityTypes.GetEntityType`` on the custom entity type and
          merge.
        """

        ENTITY_OVERRIDE_MODE_UNSPECIFIED = 0
        ENTITY_OVERRIDE_MODE_OVERRIDE = 1
        ENTITY_OVERRIDE_MODE_SUPPLEMENT = 2


class StreamingRecognitionResult(object):
    class MessageType(enum.IntEnum):
        """
        Type of the response message.

        Attributes:
          MESSAGE_TYPE_UNSPECIFIED (int): Not specified. Should never be used.
          TRANSCRIPT (int): Message contains a (possibly partial) transcript.
          END_OF_SINGLE_UTTERANCE (int): Event indicates that the server has detected the end of the user's
          speech utterance and expects no additional speech. Therefore, the server
          will not process additional audio (although it may subsequently return
          additional results). The client should stop sending additional audio
          data, half-close the gRPC connection, and wait for any additional
          results until the server closes the gRPC connection. This message is
          only sent if ``single_utterance`` was set to ``true``, and is not used
          otherwise.
        """

        MESSAGE_TYPE_UNSPECIFIED = 0
        TRANSCRIPT = 1
        END_OF_SINGLE_UTTERANCE = 2


class ValidationError(object):
    class Severity(enum.IntEnum):
        """
        Represents a level of severity.

        Attributes:
          SEVERITY_UNSPECIFIED (int): Not specified. This value should never be used.
          INFO (int): The agent doesn't follow Dialogflow best practicies.
          WARNING (int): The agent may not behave as expected.
          ERROR (int): The agent may experience partial failures.
          CRITICAL (int): The agent may completely fail.
        """

        SEVERITY_UNSPECIFIED = 0
        INFO = 1
        WARNING = 2
        ERROR = 3
        CRITICAL = 4
