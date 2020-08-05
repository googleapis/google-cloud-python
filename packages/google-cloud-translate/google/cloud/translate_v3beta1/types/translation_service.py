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
    package="google.cloud.translation.v3beta1",
    manifest={
        "TranslateTextGlossaryConfig",
        "TranslateTextRequest",
        "TranslateTextResponse",
        "Translation",
        "DetectLanguageRequest",
        "DetectedLanguage",
        "DetectLanguageResponse",
        "GetSupportedLanguagesRequest",
        "SupportedLanguages",
        "SupportedLanguage",
        "GcsSource",
        "InputConfig",
        "GcsDestination",
        "OutputConfig",
        "BatchTranslateTextRequest",
        "BatchTranslateMetadata",
        "BatchTranslateResponse",
        "GlossaryInputConfig",
        "Glossary",
        "CreateGlossaryRequest",
        "GetGlossaryRequest",
        "DeleteGlossaryRequest",
        "ListGlossariesRequest",
        "ListGlossariesResponse",
        "CreateGlossaryMetadata",
        "DeleteGlossaryMetadata",
        "DeleteGlossaryResponse",
    },
)


class TranslateTextGlossaryConfig(proto.Message):
    r"""Configures which glossary should be used for a specific
    target language, and defines options for applying that glossary.

    Attributes:
        glossary (str):
            Required. Specifies the glossary used for this translation.
            Use this format: projects/\ */locations/*/glossaries/\*
        ignore_case (bool):
            Optional. Indicates match is case-
            nsensitive. Default value is false if missing.
    """

    glossary = proto.Field(proto.STRING, number=1)

    ignore_case = proto.Field(proto.BOOL, number=2)


class TranslateTextRequest(proto.Message):
    r"""The request message for synchronous translation.

    Attributes:
        contents (Sequence[str]):
            Required. The content of the input in string
            format. We recommend the total content be less
            than 30k codepoints. Use BatchTranslateText for
            larger text.
        mime_type (str):
            Optional. The format of the source text, for
            example, "text/html",  "text/plain". If left
            blank, the MIME type defaults to "text/html".
        source_language_code (str):
            Optional. The BCP-47 language code of the
            input text if known, for example, "en-US" or
            "sr-Latn". Supported language codes are listed
            in Language Support. If the source language
            isn't specified, the API attempts to identify
            the source language automatically and returns
            the source language within the response.
        target_language_code (str):
            Required. The BCP-47 language code to use for
            translation of the input text, set to one of the
            language codes listed in Language Support.
        parent (str):
            Required. Project or location to make a call. Must refer to
            a caller's project.

            Format: ``projects/{project-id}`` or
            ``projects/{project-id}/locations/{location-id}``.

            For global calls, use
            ``projects/{project-id}/locations/global`` or
            ``projects/{project-id}``.

            Non-global location is required for requests using AutoML
            models or custom glossaries.

            Models and glossaries must be within the same region (have
            same location-id), otherwise an INVALID_ARGUMENT (400) error
            is returned.
        model (str):
            Optional. The ``model`` type requested for this translation.

            The format depends on model type:

            -  AutoML Translation models:
               ``projects/{project-id}/locations/{location-id}/models/{model-id}``

            -  General (built-in) models:
               ``projects/{project-id}/locations/{location-id}/models/general/nmt``,
               ``projects/{project-id}/locations/{location-id}/models/general/base``

            For global (non-regionalized) requests, use ``location-id``
            ``global``. For example,
            ``projects/{project-id}/locations/global/models/general/nmt``.

            If missing, the system decides which google base model to
            use.
        glossary_config (~.translation_service.TranslateTextGlossaryConfig):
            Optional. Glossary to be applied. The glossary must be
            within the same region (have the same location-id) as the
            model, otherwise an INVALID_ARGUMENT (400) error is
            returned.
        labels (Sequence[~.translation_service.TranslateTextRequest.LabelsEntry]):
            Optional. The labels with user-defined
            metadata for the request.
            Label keys and values can be no longer than 63
            characters (Unicode codepoints), can only
            contain lowercase letters, numeric characters,
            underscores and dashes. International characters
            are allowed. Label values are optional. Label
            keys must start with a letter.
            See
            https://cloud.google.com/translate/docs/labels
            for more information.
    """

    contents = proto.RepeatedField(proto.STRING, number=1)

    mime_type = proto.Field(proto.STRING, number=3)

    source_language_code = proto.Field(proto.STRING, number=4)

    target_language_code = proto.Field(proto.STRING, number=5)

    parent = proto.Field(proto.STRING, number=8)

    model = proto.Field(proto.STRING, number=6)

    glossary_config = proto.Field(
        proto.MESSAGE, number=7, message=TranslateTextGlossaryConfig,
    )

    labels = proto.MapField(proto.STRING, proto.STRING, number=10)


class TranslateTextResponse(proto.Message):
    r"""

    Attributes:
        translations (Sequence[~.translation_service.Translation]):
            Text translation responses with no glossary applied. This
            field has the same length as
            [``contents``][google.cloud.translation.v3beta1.TranslateTextRequest.contents].
        glossary_translations (Sequence[~.translation_service.Translation]):
            Text translation responses if a glossary is provided in the
            request. This can be the same as
            [``translations``][google.cloud.translation.v3beta1.TranslateTextResponse.translations]
            if no terms apply. This field has the same length as
            [``contents``][google.cloud.translation.v3beta1.TranslateTextRequest.contents].
    """

    translations = proto.RepeatedField(proto.MESSAGE, number=1, message="Translation",)

    glossary_translations = proto.RepeatedField(
        proto.MESSAGE, number=3, message="Translation",
    )


class Translation(proto.Message):
    r"""A single translation response.

    Attributes:
        translated_text (str):
            Text translated into the target language.
        model (str):
            Only present when ``model`` is present in the request. This
            is same as ``model`` provided in the request.
        detected_language_code (str):
            The BCP-47 language code of source text in
            the initial request, detected automatically, if
            no source language was passed within the initial
            request. If the source language was passed,
            auto-detection of the language does not occur
            and this field is empty.
        glossary_config (~.translation_service.TranslateTextGlossaryConfig):
            The ``glossary_config`` used for this translation.
    """

    translated_text = proto.Field(proto.STRING, number=1)

    model = proto.Field(proto.STRING, number=2)

    detected_language_code = proto.Field(proto.STRING, number=4)

    glossary_config = proto.Field(
        proto.MESSAGE, number=3, message=TranslateTextGlossaryConfig,
    )


class DetectLanguageRequest(proto.Message):
    r"""The request message for language detection.

    Attributes:
        parent (str):
            Required. Project or location to make a call. Must refer to
            a caller's project.

            Format: ``projects/{project-id}/locations/{location-id}`` or
            ``projects/{project-id}``.

            For global calls, use
            ``projects/{project-id}/locations/global`` or
            ``projects/{project-id}``.

            Only models within the same region (has same location-id)
            can be used. Otherwise an INVALID_ARGUMENT (400) error is
            returned.
        model (str):
            Optional. The language detection model to be used.

            Format:
            ``projects/{project-id}/locations/{location-id}/models/language-detection/{model-id}``

            Only one language detection model is currently supported:
            ``projects/{project-id}/locations/{location-id}/models/language-detection/default``.

            If not specified, the default model is used.
        content (str):
            The content of the input stored as a string.
        mime_type (str):
            Optional. The format of the source text, for
            example, "text/html", "text/plain". If left
            blank, the MIME type defaults to "text/html".
        labels (Sequence[~.translation_service.DetectLanguageRequest.LabelsEntry]):
            Optional. The labels with user-defined
            metadata for the request.
            Label keys and values can be no longer than 63
            characters (Unicode codepoints), can only
            contain lowercase letters, numeric characters,
            underscores and dashes. International characters
            are allowed. Label values are optional. Label
            keys must start with a letter.
            See
            https://cloud.google.com/translate/docs/labels
            for more information.
    """

    parent = proto.Field(proto.STRING, number=5)

    model = proto.Field(proto.STRING, number=4)

    content = proto.Field(proto.STRING, number=1, oneof="source")

    mime_type = proto.Field(proto.STRING, number=3)

    labels = proto.MapField(proto.STRING, proto.STRING, number=6)


class DetectedLanguage(proto.Message):
    r"""The response message for language detection.

    Attributes:
        language_code (str):
            The BCP-47 language code of source content in
            the request, detected automatically.
        confidence (float):
            The confidence of the detection result for
            this language.
    """

    language_code = proto.Field(proto.STRING, number=1)

    confidence = proto.Field(proto.FLOAT, number=2)


class DetectLanguageResponse(proto.Message):
    r"""The response message for language detection.

    Attributes:
        languages (Sequence[~.translation_service.DetectedLanguage]):
            A list of detected languages sorted by
            detection confidence in descending order. The
            most probable language first.
    """

    languages = proto.RepeatedField(proto.MESSAGE, number=1, message=DetectedLanguage,)


class GetSupportedLanguagesRequest(proto.Message):
    r"""The request message for discovering supported languages.

    Attributes:
        parent (str):
            Required. Project or location to make a call. Must refer to
            a caller's project.

            Format: ``projects/{project-id}`` or
            ``projects/{project-id}/locations/{location-id}``.

            For global calls, use
            ``projects/{project-id}/locations/global`` or
            ``projects/{project-id}``.

            Non-global location is required for AutoML models.

            Only models within the same region (have same location-id)
            can be used, otherwise an INVALID_ARGUMENT (400) error is
            returned.
        display_language_code (str):
            Optional. The language to use to return
            localized, human readable names of supported
            languages. If missing, then display names are
            not returned in a response.
        model (str):
            Optional. Get supported languages of this model.

            The format depends on model type:

            -  AutoML Translation models:
               ``projects/{project-id}/locations/{location-id}/models/{model-id}``

            -  General (built-in) models:
               ``projects/{project-id}/locations/{location-id}/models/general/nmt``,
               ``projects/{project-id}/locations/{location-id}/models/general/base``

            Returns languages supported by the specified model. If
            missing, we get supported languages of Google general base
            (PBMT) model.
    """

    parent = proto.Field(proto.STRING, number=3)

    display_language_code = proto.Field(proto.STRING, number=1)

    model = proto.Field(proto.STRING, number=2)


class SupportedLanguages(proto.Message):
    r"""The response message for discovering supported languages.

    Attributes:
        languages (Sequence[~.translation_service.SupportedLanguage]):
            A list of supported language responses. This
            list contains an entry for each language the
            Translation API supports.
    """

    languages = proto.RepeatedField(
        proto.MESSAGE, number=1, message="SupportedLanguage",
    )


class SupportedLanguage(proto.Message):
    r"""A single supported language response corresponds to
    information related to one supported language.

    Attributes:
        language_code (str):
            Supported language code, generally consisting
            of its ISO 639-1 identifier, for example, 'en',
            'ja'. In certain cases, BCP-47 codes including
            language and region identifiers are returned
            (for example, 'zh-TW' and 'zh-CN')
        display_name (str):
            Human readable name of the language localized
            in the display language specified in the
            request.
        support_source (bool):
            Can be used as source language.
        support_target (bool):
            Can be used as target language.
    """

    language_code = proto.Field(proto.STRING, number=1)

    display_name = proto.Field(proto.STRING, number=2)

    support_source = proto.Field(proto.BOOL, number=3)

    support_target = proto.Field(proto.BOOL, number=4)


class GcsSource(proto.Message):
    r"""The Google Cloud Storage location for the input content.

    Attributes:
        input_uri (str):
            Required. Source data URI. For example,
            ``gs://my_bucket/my_object``.
    """

    input_uri = proto.Field(proto.STRING, number=1)


class InputConfig(proto.Message):
    r"""Input configuration for BatchTranslateText request.

    Attributes:
        mime_type (str):
            Optional. Can be "text/plain" or "text/html". For ``.tsv``,
            "text/html" is used if mime_type is missing. For ``.html``,
            this field must be "text/html" or empty. For ``.txt``, this
            field must be "text/plain" or empty.
        gcs_source (~.translation_service.GcsSource):
            Required. Google Cloud Storage location for the source
            input. This can be a single file (for example,
            ``gs://translation-test/input.tsv``) or a wildcard (for
            example, ``gs://translation-test/*``). If a file extension
            is ``.tsv``, it can contain either one or two columns. The
            first column (optional) is the id of the text request. If
            the first column is missing, we use the row number (0-based)
            from the input file as the ID in the output file. The second
            column is the actual text to be translated. We recommend
            each row be <= 10K Unicode codepoints, otherwise an error
            might be returned. Note that the input tsv must be RFC 4180
            compliant.

            You could use https://github.com/Clever/csvlint to check
            potential formatting errors in your tsv file. csvlint
            --delimiter='\t' your_input_file.tsv

            The other supported file extensions are ``.txt`` or
            ``.html``, which is treated as a single large chunk of text.
    """

    mime_type = proto.Field(proto.STRING, number=1)

    gcs_source = proto.Field(
        proto.MESSAGE, number=2, oneof="source", message=GcsSource,
    )


class GcsDestination(proto.Message):
    r"""The Google Cloud Storage location for the output content.

    Attributes:
        output_uri_prefix (str):
            Required. There must be no files under 'output_uri_prefix'.
            'output_uri_prefix' must end with "/" and start with
            "gs://", otherwise an INVALID_ARGUMENT (400) error is
            returned.
    """

    output_uri_prefix = proto.Field(proto.STRING, number=1)


class OutputConfig(proto.Message):
    r"""Output configuration for BatchTranslateText request.

    Attributes:
        gcs_destination (~.translation_service.GcsDestination):
            Google Cloud Storage destination for output content. For
            every single input file (for example,
            gs://a/b/c.[extension]), we generate at most 2 \* n output
            files. (n is the # of target_language_codes in the
            BatchTranslateTextRequest).

            Output files (tsv) generated are compliant with RFC 4180
            except that record delimiters are '\n' instead of '\r\n'. We
            don't provide any way to change record delimiters.

            While the input files are being processed, we write/update
            an index file 'index.csv' under 'output_uri_prefix' (for
            example, gs://translation-test/index.csv) The index file is
            generated/updated as new files are being translated. The
            format is:

            input_file,target_language_code,translations_file,errors_file,
            glossary_translations_file,glossary_errors_file

            input_file is one file we matched using
            gcs_source.input_uri. target_language_code is provided in
            the request. translations_file contains the translations.
            (details provided below) errors_file contains the errors
            during processing of the file. (details below). Both
            translations_file and errors_file could be empty strings if
            we have no content to output. glossary_translations_file and
            glossary_errors_file are always empty strings if the
            input_file is tsv. They could also be empty if we have no
            content to output.

            Once a row is present in index.csv, the input/output
            matching never changes. Callers should also expect all the
            content in input_file are processed and ready to be consumed
            (that is, no partial output file is written).

            The format of translations_file (for target language code
            'trg') is:
            ``gs://translation_test/a_b_c\_'trg'_translations.[extension]``

            If the input file extension is tsv, the output has the
            following columns: Column 1: ID of the request provided in
            the input, if it's not provided in the input, then the input
            row number is used (0-based). Column 2: source sentence.
            Column 3: translation without applying a glossary. Empty
            string if there is an error. Column 4 (only present if a
            glossary is provided in the request): translation after
            applying the glossary. Empty string if there is an error
            applying the glossary. Could be same string as column 3 if
            there is no glossary applied.

            If input file extension is a txt or html, the translation is
            directly written to the output file. If glossary is
            requested, a separate glossary_translations_file has format
            of
            ``gs://translation_test/a_b_c\_'trg'_glossary_translations.[extension]``

            The format of errors file (for target language code 'trg')
            is: ``gs://translation_test/a_b_c\_'trg'_errors.[extension]``

            If the input file extension is tsv, errors_file contains the
            following: Column 1: ID of the request provided in the
            input, if it's not provided in the input, then the input row
            number is used (0-based). Column 2: source sentence. Column
            3: Error detail for the translation. Could be empty. Column
            4 (only present if a glossary is provided in the request):
            Error when applying the glossary.

            If the input file extension is txt or html,
            glossary_error_file will be generated that contains error
            details. glossary_error_file has format of
            ``gs://translation_test/a_b_c\_'trg'_glossary_errors.[extension]``
    """

    gcs_destination = proto.Field(
        proto.MESSAGE, number=1, oneof="destination", message=GcsDestination,
    )


class BatchTranslateTextRequest(proto.Message):
    r"""The batch translation request.

    Attributes:
        parent (str):
            Required. Location to make a call. Must refer to a caller's
            project.

            Format: ``projects/{project-id}/locations/{location-id}``.

            The ``global`` location is not supported for batch
            translation.

            Only AutoML Translation models or glossaries within the same
            region (have the same location-id) can be used, otherwise an
            INVALID_ARGUMENT (400) error is returned.
        source_language_code (str):
            Required. Source language code.
        target_language_codes (Sequence[str]):
            Required. Specify up to 10 language codes
            here.
        models (Sequence[~.translation_service.BatchTranslateTextRequest.ModelsEntry]):
            Optional. The models to use for translation. Map's key is
            target language code. Map's value is model name. Value can
            be a built-in general model, or an AutoML Translation model.

            The value format depends on model type:

            -  AutoML Translation models:
               ``projects/{project-id}/locations/{location-id}/models/{model-id}``

            -  General (built-in) models:
               ``projects/{project-id}/locations/{location-id}/models/general/nmt``,
               ``projects/{project-id}/locations/{location-id}/models/general/base``

            If the map is empty or a specific model is not requested for
            a language pair, then default google model (nmt) is used.
        input_configs (Sequence[~.translation_service.InputConfig]):
            Required. Input configurations.
            The total number of files matched should be <=
            1000. The total content size should be <= 100M
            Unicode codepoints. The files must use UTF-8
            encoding.
        output_config (~.translation_service.OutputConfig):
            Required. Output configuration.
            If 2 input configs match to the same file (that
            is, same input path), we don't generate output
            for duplicate inputs.
        glossaries (Sequence[~.translation_service.BatchTranslateTextRequest.GlossariesEntry]):
            Optional. Glossaries to be applied for
            translation. It's keyed by target language code.
        labels (Sequence[~.translation_service.BatchTranslateTextRequest.LabelsEntry]):
            Optional. The labels with user-defined
            metadata for the request.
            Label keys and values can be no longer than 63
            characters (Unicode codepoints), can only
            contain lowercase letters, numeric characters,
            underscores and dashes. International characters
            are allowed. Label values are optional. Label
            keys must start with a letter.
            See
            https://cloud.google.com/translate/docs/labels
            for more information.
    """

    parent = proto.Field(proto.STRING, number=1)

    source_language_code = proto.Field(proto.STRING, number=2)

    target_language_codes = proto.RepeatedField(proto.STRING, number=3)

    models = proto.MapField(proto.STRING, proto.STRING, number=4)

    input_configs = proto.RepeatedField(proto.MESSAGE, number=5, message=InputConfig,)

    output_config = proto.Field(proto.MESSAGE, number=6, message=OutputConfig,)

    glossaries = proto.MapField(
        proto.STRING, proto.MESSAGE, number=7, message=TranslateTextGlossaryConfig,
    )

    labels = proto.MapField(proto.STRING, proto.STRING, number=9)


class BatchTranslateMetadata(proto.Message):
    r"""State metadata for the batch translation operation.

    Attributes:
        state (~.translation_service.BatchTranslateMetadata.State):
            The state of the operation.
        translated_characters (int):
            Number of successfully translated characters
            so far (Unicode codepoints).
        failed_characters (int):
            Number of characters that have failed to
            process so far (Unicode codepoints).
        total_characters (int):
            Total number of characters (Unicode
            codepoints). This is the total number of
            codepoints from input files times the number of
            target languages and appears here shortly after
            the call is submitted.
        submit_time (~.timestamp.Timestamp):
            Time when the operation was submitted.
    """

    class State(proto.Enum):
        r"""State of the job."""
        STATE_UNSPECIFIED = 0
        RUNNING = 1
        SUCCEEDED = 2
        FAILED = 3
        CANCELLING = 4
        CANCELLED = 5

    state = proto.Field(proto.ENUM, number=1, enum=State,)

    translated_characters = proto.Field(proto.INT64, number=2)

    failed_characters = proto.Field(proto.INT64, number=3)

    total_characters = proto.Field(proto.INT64, number=4)

    submit_time = proto.Field(proto.MESSAGE, number=5, message=timestamp.Timestamp,)


class BatchTranslateResponse(proto.Message):
    r"""Stored in the
    [google.longrunning.Operation.response][google.longrunning.Operation.response]
    field returned by BatchTranslateText if at least one sentence is
    translated successfully.

    Attributes:
        total_characters (int):
            Total number of characters (Unicode
            codepoints).
        translated_characters (int):
            Number of successfully translated characters
            (Unicode codepoints).
        failed_characters (int):
            Number of characters that have failed to
            process (Unicode codepoints).
        submit_time (~.timestamp.Timestamp):
            Time when the operation was submitted.
        end_time (~.timestamp.Timestamp):
            The time when the operation is finished and
            [google.longrunning.Operation.done][google.longrunning.Operation.done]
            is set to true.
    """

    total_characters = proto.Field(proto.INT64, number=1)

    translated_characters = proto.Field(proto.INT64, number=2)

    failed_characters = proto.Field(proto.INT64, number=3)

    submit_time = proto.Field(proto.MESSAGE, number=4, message=timestamp.Timestamp,)

    end_time = proto.Field(proto.MESSAGE, number=5, message=timestamp.Timestamp,)


class GlossaryInputConfig(proto.Message):
    r"""Input configuration for glossaries.

    Attributes:
        gcs_source (~.translation_service.GcsSource):
            Required. Google Cloud Storage location of glossary data.
            File format is determined based on the filename extension.
            API returns [google.rpc.Code.INVALID_ARGUMENT] for
            unsupported URI-s and file formats. Wildcards are not
            allowed. This must be a single file in one of the following
            formats:

            For unidirectional glossaries:

            -  TSV/CSV (``.tsv``/``.csv``): 2 column file, tab- or
               comma-separated. The first column is source text. The
               second column is target text. The file must not contain
               headers. That is, the first row is data, not column
               names.

            -  TMX (``.tmx``): TMX file with parallel data defining
               source/target term pairs.

            For equivalent term sets glossaries:

            -  CSV (``.csv``): Multi-column CSV file defining equivalent
               glossary terms in multiple languages. The format is
               defined for Google Translation Toolkit and documented in
               `Use a
               glossary <https://support.google.com/translatortoolkit/answer/6306379?hl=en>`__.
    """

    gcs_source = proto.Field(
        proto.MESSAGE, number=1, oneof="source", message=GcsSource,
    )


class Glossary(proto.Message):
    r"""Represents a glossary built from user provided data.

    Attributes:
        name (str):
            Required. The resource name of the glossary. Glossary names
            have the form
            ``projects/{project-id}/locations/{location-id}/glossaries/{glossary-id}``.
        language_pair (~.translation_service.Glossary.LanguageCodePair):
            Used with unidirectional glossaries.
        language_codes_set (~.translation_service.Glossary.LanguageCodesSet):
            Used with equivalent term set glossaries.
        input_config (~.translation_service.GlossaryInputConfig):
            Required. Provides examples to build the
            glossary from. Total glossary must not exceed
            10M Unicode codepoints.
        entry_count (int):
            Output only. The number of entries defined in
            the glossary.
        submit_time (~.timestamp.Timestamp):
            Output only. When CreateGlossary was called.
        end_time (~.timestamp.Timestamp):
            Output only. When the glossary creation was
            finished.
    """

    class LanguageCodePair(proto.Message):
        r"""Used with unidirectional glossaries.

        Attributes:
            source_language_code (str):
                Required. The BCP-47 language code of the input text, for
                example, "en-US". Expected to be an exact match for
                GlossaryTerm.language_code.
            target_language_code (str):
                Required. The BCP-47 language code for translation output,
                for example, "zh-CN". Expected to be an exact match for
                GlossaryTerm.language_code.
        """

        source_language_code = proto.Field(proto.STRING, number=1)

        target_language_code = proto.Field(proto.STRING, number=2)

    class LanguageCodesSet(proto.Message):
        r"""Used with equivalent term set glossaries.

        Attributes:
            language_codes (Sequence[str]):
                The BCP-47 language code(s) for terms defined in the
                glossary. All entries are unique. The list contains at least
                two entries. Expected to be an exact match for
                GlossaryTerm.language_code.
        """

        language_codes = proto.RepeatedField(proto.STRING, number=1)

    name = proto.Field(proto.STRING, number=1)

    language_pair = proto.Field(
        proto.MESSAGE, number=3, oneof="languages", message=LanguageCodePair,
    )

    language_codes_set = proto.Field(
        proto.MESSAGE, number=4, oneof="languages", message=LanguageCodesSet,
    )

    input_config = proto.Field(proto.MESSAGE, number=5, message=GlossaryInputConfig,)

    entry_count = proto.Field(proto.INT32, number=6)

    submit_time = proto.Field(proto.MESSAGE, number=7, message=timestamp.Timestamp,)

    end_time = proto.Field(proto.MESSAGE, number=8, message=timestamp.Timestamp,)


class CreateGlossaryRequest(proto.Message):
    r"""Request message for CreateGlossary.

    Attributes:
        parent (str):
            Required. The project name.
        glossary (~.translation_service.Glossary):
            Required. The glossary to create.
    """

    parent = proto.Field(proto.STRING, number=1)

    glossary = proto.Field(proto.MESSAGE, number=2, message=Glossary,)


class GetGlossaryRequest(proto.Message):
    r"""Request message for GetGlossary.

    Attributes:
        name (str):
            Required. The name of the glossary to
            retrieve.
    """

    name = proto.Field(proto.STRING, number=1)


class DeleteGlossaryRequest(proto.Message):
    r"""Request message for DeleteGlossary.

    Attributes:
        name (str):
            Required. The name of the glossary to delete.
    """

    name = proto.Field(proto.STRING, number=1)


class ListGlossariesRequest(proto.Message):
    r"""Request message for ListGlossaries.

    Attributes:
        parent (str):
            Required. The name of the project from which
            to list all of the glossaries.
        page_size (int):
            Optional. Requested page size. The server may
            return fewer glossaries than requested. If
            unspecified, the server picks an appropriate
            default.
        page_token (str):
            Optional. A token identifying a page of results the server
            should return. Typically, this is the value of
            [ListGlossariesResponse.next_page_token] returned from the
            previous call to ``ListGlossaries`` method. The first page
            is returned if ``page_token``\ is empty or missing.
        filter (str):
            Optional. Filter specifying constraints of a
            list operation. Filtering is not supported yet,
            and the parameter currently has no effect. If
            missing, no filtering is performed.
    """

    parent = proto.Field(proto.STRING, number=1)

    page_size = proto.Field(proto.INT32, number=2)

    page_token = proto.Field(proto.STRING, number=3)

    filter = proto.Field(proto.STRING, number=4)


class ListGlossariesResponse(proto.Message):
    r"""Response message for ListGlossaries.

    Attributes:
        glossaries (Sequence[~.translation_service.Glossary]):
            The list of glossaries for a project.
        next_page_token (str):
            A token to retrieve a page of results. Pass this value in
            the [ListGlossariesRequest.page_token] field in the
            subsequent call to ``ListGlossaries`` method to retrieve the
            next page of results.
    """

    @property
    def raw_page(self):
        return self

    glossaries = proto.RepeatedField(proto.MESSAGE, number=1, message=Glossary,)

    next_page_token = proto.Field(proto.STRING, number=2)


class CreateGlossaryMetadata(proto.Message):
    r"""Stored in the
    [google.longrunning.Operation.metadata][google.longrunning.Operation.metadata]
    field returned by CreateGlossary.

    Attributes:
        name (str):
            The name of the glossary that is being
            created.
        state (~.translation_service.CreateGlossaryMetadata.State):
            The current state of the glossary creation
            operation.
        submit_time (~.timestamp.Timestamp):
            The time when the operation was submitted to
            the server.
    """

    class State(proto.Enum):
        r"""Enumerates the possible states that the creation request can
        be in.
        """
        STATE_UNSPECIFIED = 0
        RUNNING = 1
        SUCCEEDED = 2
        FAILED = 3
        CANCELLING = 4
        CANCELLED = 5

    name = proto.Field(proto.STRING, number=1)

    state = proto.Field(proto.ENUM, number=2, enum=State,)

    submit_time = proto.Field(proto.MESSAGE, number=3, message=timestamp.Timestamp,)


class DeleteGlossaryMetadata(proto.Message):
    r"""Stored in the
    [google.longrunning.Operation.metadata][google.longrunning.Operation.metadata]
    field returned by DeleteGlossary.

    Attributes:
        name (str):
            The name of the glossary that is being
            deleted.
        state (~.translation_service.DeleteGlossaryMetadata.State):
            The current state of the glossary deletion
            operation.
        submit_time (~.timestamp.Timestamp):
            The time when the operation was submitted to
            the server.
    """

    class State(proto.Enum):
        r"""Enumerates the possible states that the creation request can
        be in.
        """
        STATE_UNSPECIFIED = 0
        RUNNING = 1
        SUCCEEDED = 2
        FAILED = 3
        CANCELLING = 4
        CANCELLED = 5

    name = proto.Field(proto.STRING, number=1)

    state = proto.Field(proto.ENUM, number=2, enum=State,)

    submit_time = proto.Field(proto.MESSAGE, number=3, message=timestamp.Timestamp,)


class DeleteGlossaryResponse(proto.Message):
    r"""Stored in the
    [google.longrunning.Operation.response][google.longrunning.Operation.response]
    field returned by DeleteGlossary.

    Attributes:
        name (str):
            The name of the deleted glossary.
        submit_time (~.timestamp.Timestamp):
            The time when the operation was submitted to
            the server.
        end_time (~.timestamp.Timestamp):
            The time when the glossary deletion is finished and
            [google.longrunning.Operation.done][google.longrunning.Operation.done]
            is set to true.
    """

    name = proto.Field(proto.STRING, number=1)

    submit_time = proto.Field(proto.MESSAGE, number=2, message=timestamp.Timestamp,)

    end_time = proto.Field(proto.MESSAGE, number=3, message=timestamp.Timestamp,)


__all__ = tuple(sorted(__protobuf__.manifest))
