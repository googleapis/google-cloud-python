# Copyright 2018 Google LLC
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


class NullValue(enum.IntEnum):
    """
    ``NullValue`` is a singleton enumeration to represent the null value for the
    ``Value`` type union.

     The JSON representation for ``NullValue`` is JSON ``null``.

    Attributes:
      NULL_VALUE (int): Null value.
    """
    NULL_VALUE = 0


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


class AudioEncoding(enum.IntEnum):
    """
    Audio encoding of the audio content sent in the conversational query request.
    Refer to the `Cloud Speech API documentation <https://cloud.google.com/speech/docs/basics>`_ for more
    details.

    Attributes:
      AUDIO_ENCODING_UNSPECIFIED (int): Not specified.
      AUDIO_ENCODING_LINEAR_16 (int): Uncompressed 16-bit signed little-endian samples (Linear PCM).
      AUDIO_ENCODING_FLAC (int): ```FLAC`` <https://xiph.org/flac/documentation.html>`_ (Free Lossless Audio
      Codec) is the recommended encoding because it is lossless (therefore
      recognition is not compromised) and requires only about half the
      bandwidth of ``LINEAR16``. ``FLAC`` stream encoding supports 16-bit and
      24-bit samples, however, not all fields in ``STREAMINFO`` are supported.
      AUDIO_ENCODING_MULAW (int): 8-bit samples that compand 14-bit audio samples using G.711 PCMU/mu-law.
      AUDIO_ENCODING_AMR (int): Adaptive Multi-Rate Narrowband codec. ``sample_rate_hertz`` must be 8000.
      AUDIO_ENCODING_AMR_WB (int): Adaptive Multi-Rate Wideband codec. ``sample_rate_hertz`` must be 16000.
      AUDIO_ENCODING_OGG_OPUS (int): Opus encoded audio frames in Ogg container
      (`OggOpus <https://wiki.xiph.org/OggOpus>`_).
      ``sample_rate_hertz`` must be 16000.
      AUDIO_ENCODING_SPEEX_WITH_HEADER_BYTE (int): Although the use of lossy encodings is not recommended, if a very low
      bitrate encoding is required, ``OGG_OPUS`` is highly preferred over
      Speex encoding. The `Speex <https://speex.org/>`_ encoding supported by
      Dialogflow API has a header byte in each block, as in MIME type
      ``audio/x-speex-with-header-byte``.
      It is a variant of the RTP Speex encoding defined in
      `RFC 5574 <https://tools.ietf.org/html/rfc5574>`_.
      The stream is a sequence of blocks, one block per RTP packet. Each block
      starts with a byte containing the length of the block, in bytes, followed
      by one or more frames of Speex data, padded to an integral number of
      bytes (octets) as specified in RFC 5574. In other words, each RTP header
      is replaced with a single byte containing the block length. Only Speex
      wideband is supported. ``sample_rate_hertz`` must be 16000.
    """
    AUDIO_ENCODING_UNSPECIFIED = 0
    AUDIO_ENCODING_LINEAR_16 = 1
    AUDIO_ENCODING_FLAC = 2
    AUDIO_ENCODING_MULAW = 3
    AUDIO_ENCODING_AMR = 4
    AUDIO_ENCODING_AMR_WB = 5
    AUDIO_ENCODING_OGG_OPUS = 6
    AUDIO_ENCODING_SPEEX_WITH_HEADER_BYTE = 7


class EntityType(object):
    class Kind(enum.IntEnum):
        """
        Represents kinds of entities.

        Attributes:
          KIND_UNSPECIFIED (int): Not specified. This value should be never used.
          KIND_MAP (int): Map entity types allow mapping of a group of synonyms to a canonical
          value.
          KIND_LIST (int): List entity types contain a set of entries that do not map to canonical
          values. However, list entity types can contain references to other entity
          types (with or without aliases).
        """
        KIND_UNSPECIFIED = 0
        KIND_MAP = 1
        KIND_LIST = 2

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


class SessionEntityType(object):
    class EntityOverrideMode(enum.IntEnum):
        """
        The types of modifications for a session entity type.

        Attributes:
          ENTITY_OVERRIDE_MODE_UNSPECIFIED (int): Not specified. This value should be never used.
          ENTITY_OVERRIDE_MODE_OVERRIDE (int): The collection of session entities overrides the collection of entities
          in the corresponding developer entity type.
          ENTITY_OVERRIDE_MODE_SUPPLEMENT (int): The collection of session entities extends the collection of entities in
          the corresponding developer entity type.
          Calls to ``ListSessionEntityTypes``, ``GetSessionEntityType``,
          ``CreateSessionEntityType`` and ``UpdateSessionEntityType`` return the full
          collection of entities from the developer entity type in the agent's
          default language and the session entity type.
        """
        ENTITY_OVERRIDE_MODE_UNSPECIFIED = 0
        ENTITY_OVERRIDE_MODE_OVERRIDE = 1
        ENTITY_OVERRIDE_MODE_SUPPLEMENT = 2


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
              ACTIONS_ON_GOOGLE (int): Actions on Google.
              When using Actions on Google, you can choose one of the specific
              Intent.Message types that mention support for Actions on Google,
              or you can use the advanced Intent.Message.payload field.
              The payload field provides access to AoG features not available in the
              specific message types.
              If using the Intent.Message.payload field, it should have a structure
              similar to the JSON message shown here. For more information, see
              [Actions on Google Webhook
              Format](https://developers.google.com/actions/dialogflow/webhook)
              <pre>{
                \"expectUserResponse\": true,
                \"isSsml\": false,
                \"noInputPrompts\": [],
                \"richResponse\": {
              ::

                  \"items\": [
                    {
                      \"simpleResponse\": {
                        \"displayText\": \"hi\",
                        \"textToSpeech\": \"hello\"
                      }
                    }
                  ],
                  \"suggestions\": [
                    {
                      \"title\": \"Say this\"
                    },
                    {
                      \"title\": \"or this\"
                    }
                  ]
                },
                \"systemIntent\": {
              ::

                  \"data\": {
                    \"@type\": \"type.googleapis.com/google.actions.v2.OptionValueSpec\",
                    \"listSelect\": {
                      \"items\": [
                        {
                          \"optionInfo\": {
                            \"key\": \"key1\",
                            \"synonyms\": [
                              \"key one\"
                            ]
                          },
                          \"title\": \"must not be empty, but unique\"
                        },
                        {
                          \"optionInfo\": {
                            \"key\": \"key2\",
                            \"synonyms\": [
                              \"key two\"
                            ]
                          },
                          \"title\": \"must not be empty, but unique\"
                        }
                      ]
                    }
                  },
                  \"intent\": \"actions.intent.OPTION\"
                }
              }</pre>
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


class StreamingRecognitionResult(object):
    class MessageType(enum.IntEnum):
        """
        Type of the response message.

        Attributes:
          MESSAGE_TYPE_UNSPECIFIED (int): Not specified. Should never be used.
          TRANSCRIPT (int): Message contains a (possibly partial) transcript.
          END_OF_SINGLE_UTTERANCE (int): Event indicates that the server has detected the end of the user's speech
          utterance and expects no additional speech. Therefore, the server will
          not process additional audio (although it may subsequently return
          additional results). The client should stop sending additional audio
          data, half-close the gRPC connection, and wait for any additional results
          until the server closes the gRPC connection. This message is only sent if
          ``single_utterance`` was set to ``true``, and is not used otherwise.
        """
        MESSAGE_TYPE_UNSPECIFIED = 0
        TRANSCRIPT = 1
        END_OF_SINGLE_UTTERANCE = 2


class Agent(object):
    class MatchMode(enum.IntEnum):
        """
        Match mode determines how intents are detected from user queries.

        Attributes:
          MATCH_MODE_UNSPECIFIED (int): Not specified.
          MATCH_MODE_HYBRID (int): Best for agents with a small number of examples in intents and/or wide
          use of templates syntax and composite entities.
          MATCH_MODE_ML_ONLY (int): Can be used for agents with a large number of examples in intents,
          especially the ones using @sys.any or very large developer entities.
        """
        MATCH_MODE_UNSPECIFIED = 0
        MATCH_MODE_HYBRID = 1
        MATCH_MODE_ML_ONLY = 2
