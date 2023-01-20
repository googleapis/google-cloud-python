# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
from typing import MutableMapping, MutableSequence

from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.documentai_v1beta2.types import geometry

__protobuf__ = proto.module(
    package="google.cloud.documentai.v1beta2",
    manifest={
        "BatchProcessDocumentsRequest",
        "ProcessDocumentRequest",
        "BatchProcessDocumentsResponse",
        "ProcessDocumentResponse",
        "OcrParams",
        "TableExtractionParams",
        "TableBoundHint",
        "FormExtractionParams",
        "KeyValuePairHint",
        "EntityExtractionParams",
        "AutoMlParams",
        "InputConfig",
        "OutputConfig",
        "GcsSource",
        "GcsDestination",
        "OperationMetadata",
    },
)


class BatchProcessDocumentsRequest(proto.Message):
    r"""Request to batch process documents as an asynchronous operation. The
    output is written to Cloud Storage as JSON in the [Document] format.

    Attributes:
        requests (MutableSequence[google.cloud.documentai_v1beta2.types.ProcessDocumentRequest]):
            Required. Individual requests for each
            document.
        parent (str):
            Target project and location to make a call.

            Format: ``projects/{project-id}/locations/{location-id}``.

            If no location is specified, a region will be chosen
            automatically.
    """

    requests: MutableSequence["ProcessDocumentRequest"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="ProcessDocumentRequest",
    )
    parent: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ProcessDocumentRequest(proto.Message):
    r"""Request to process one document.

    Attributes:
        parent (str):
            Target project and location to make a call.

            Format: ``projects/{project-id}/locations/{location-id}``.

            If no location is specified, a region will be chosen
            automatically. This field is only populated when used in
            ProcessDocument method.
        input_config (google.cloud.documentai_v1beta2.types.InputConfig):
            Required. Information about the input file.
        output_config (google.cloud.documentai_v1beta2.types.OutputConfig):
            Optional. The desired output location. This
            field is only needed in
            BatchProcessDocumentsRequest.
        document_type (str):
            Specifies a known document type for deeper
            structure detection. Valid values are currently
            "general" and "invoice". If not provided,
            "general"\ is used as default. If any other
            value is given, the request is rejected.
        table_extraction_params (google.cloud.documentai_v1beta2.types.TableExtractionParams):
            Controls table extraction behavior. If not
            specified, the system will decide reasonable
            defaults.
        form_extraction_params (google.cloud.documentai_v1beta2.types.FormExtractionParams):
            Controls form extraction behavior. If not
            specified, the system will decide reasonable
            defaults.
        entity_extraction_params (google.cloud.documentai_v1beta2.types.EntityExtractionParams):
            Controls entity extraction behavior. If not
            specified, the system will decide reasonable
            defaults.
        ocr_params (google.cloud.documentai_v1beta2.types.OcrParams):
            Controls OCR behavior. If not specified, the
            system will decide reasonable defaults.
        automl_params (google.cloud.documentai_v1beta2.types.AutoMlParams):
            Controls AutoML model prediction behavior.
            AutoMlParams cannot be used together with other
            Params.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=9,
    )
    input_config: "InputConfig" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="InputConfig",
    )
    output_config: "OutputConfig" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="OutputConfig",
    )
    document_type: str = proto.Field(
        proto.STRING,
        number=3,
    )
    table_extraction_params: "TableExtractionParams" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="TableExtractionParams",
    )
    form_extraction_params: "FormExtractionParams" = proto.Field(
        proto.MESSAGE,
        number=5,
        message="FormExtractionParams",
    )
    entity_extraction_params: "EntityExtractionParams" = proto.Field(
        proto.MESSAGE,
        number=6,
        message="EntityExtractionParams",
    )
    ocr_params: "OcrParams" = proto.Field(
        proto.MESSAGE,
        number=7,
        message="OcrParams",
    )
    automl_params: "AutoMlParams" = proto.Field(
        proto.MESSAGE,
        number=8,
        message="AutoMlParams",
    )


class BatchProcessDocumentsResponse(proto.Message):
    r"""Response to an batch document processing request. This is
    returned in the LRO Operation after the operation is complete.

    Attributes:
        responses (MutableSequence[google.cloud.documentai_v1beta2.types.ProcessDocumentResponse]):
            Responses for each individual document.
    """

    responses: MutableSequence["ProcessDocumentResponse"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="ProcessDocumentResponse",
    )


class ProcessDocumentResponse(proto.Message):
    r"""Response to a single document processing request.

    Attributes:
        input_config (google.cloud.documentai_v1beta2.types.InputConfig):
            Information about the input file. This is the
            same as the corresponding input config in the
            request.
        output_config (google.cloud.documentai_v1beta2.types.OutputConfig):
            The output location of the parsed responses. The responses
            are written to this location as JSON-serialized ``Document``
            objects.
    """

    input_config: "InputConfig" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="InputConfig",
    )
    output_config: "OutputConfig" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="OutputConfig",
    )


class OcrParams(proto.Message):
    r"""Parameters to control Optical Character Recognition (OCR)
    behavior.

    Attributes:
        language_hints (MutableSequence[str]):
            List of languages to use for OCR. In most cases, an empty
            value yields the best results since it enables automatic
            language detection. For languages based on the Latin
            alphabet, setting ``language_hints`` is not needed. In rare
            cases, when the language of the text in the image is known,
            setting a hint will help get better results (although it
            will be a significant hindrance if the hint is wrong).
            Document processing returns an error if one or more of the
            specified languages is not one of the supported languages.
    """

    language_hints: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=1,
    )


class TableExtractionParams(proto.Message):
    r"""Parameters to control table extraction behavior.

    Attributes:
        enabled (bool):
            Whether to enable table extraction.
        table_bound_hints (MutableSequence[google.cloud.documentai_v1beta2.types.TableBoundHint]):
            Optional. Table bounding box hints that can
            be provided to complex cases which our algorithm
            cannot locate the table(s) in.
        header_hints (MutableSequence[str]):
            Optional. Table header hints. The extraction
            will bias towards producing these terms as table
            headers, which may improve accuracy.
        model_version (str):
            Model version of the table extraction system.
            Default is "builtin/stable". Specify
            "builtin/latest" for the latest model.
    """

    enabled: bool = proto.Field(
        proto.BOOL,
        number=1,
    )
    table_bound_hints: MutableSequence["TableBoundHint"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="TableBoundHint",
    )
    header_hints: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )
    model_version: str = proto.Field(
        proto.STRING,
        number=4,
    )


class TableBoundHint(proto.Message):
    r"""A hint for a table bounding box on the page for table
    parsing.

    Attributes:
        page_number (int):
            Optional. Page number for multi-paged inputs
            this hint applies to. If not provided, this hint
            will apply to all pages by default. This value
            is 1-based.
        bounding_box (google.cloud.documentai_v1beta2.types.BoundingPoly):
            Bounding box hint for a table on this page. The coordinates
            must be normalized to [0,1] and the bounding box must be an
            axis-aligned rectangle.
    """

    page_number: int = proto.Field(
        proto.INT32,
        number=1,
    )
    bounding_box: geometry.BoundingPoly = proto.Field(
        proto.MESSAGE,
        number=2,
        message=geometry.BoundingPoly,
    )


class FormExtractionParams(proto.Message):
    r"""Parameters to control form extraction behavior.

    Attributes:
        enabled (bool):
            Whether to enable form extraction.
        key_value_pair_hints (MutableSequence[google.cloud.documentai_v1beta2.types.KeyValuePairHint]):
            User can provide pairs of (key text, value type) to improve
            the parsing result.

            For example, if a document has a field called "Date" that
            holds a date value and a field called "Amount" that may hold
            either a currency value (e.g., "$500.00") or a simple number
            value (e.g., "20"), you could use the following hints: [
            {"key": "Date", value_types: [ "DATE"]}, {"key": "Amount",
            "value_types": [ "PRICE", "NUMBER" ]} ]

            If the value type is unknown, but you want to provide hints
            for the keys, you can leave the value_types field blank.
            e.g. {"key": "Date", "value_types": []}
        model_version (str):
            Model version of the form extraction system. Default is
            "builtin/stable". Specify "builtin/latest" for the latest
            model. For custom form models, specify:
            “custom/{model_name}". Model name format is
            "bucket_name/path/to/modeldir" corresponding to
            "gs://bucket_name/path/to/modeldir" where annotated examples
            are stored.
    """

    enabled: bool = proto.Field(
        proto.BOOL,
        number=1,
    )
    key_value_pair_hints: MutableSequence["KeyValuePairHint"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="KeyValuePairHint",
    )
    model_version: str = proto.Field(
        proto.STRING,
        number=3,
    )


class KeyValuePairHint(proto.Message):
    r"""User-provided hint for key value pair.

    Attributes:
        key (str):
            The key text for the hint.
        value_types (MutableSequence[str]):
            Type of the value. This is case-insensitive, and could be
            one of: ADDRESS, LOCATION, ORGANIZATION, PERSON,
            PHONE_NUMBER, ID, NUMBER, EMAIL, PRICE, TERMS, DATE, NAME.
            Types not in this list will be ignored.
    """

    key: str = proto.Field(
        proto.STRING,
        number=1,
    )
    value_types: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )


class EntityExtractionParams(proto.Message):
    r"""Parameters to control entity extraction behavior.

    Attributes:
        enabled (bool):
            Whether to enable entity extraction.
        model_version (str):
            Model version of the entity extraction.
            Default is "builtin/stable". Specify
            "builtin/latest" for the latest model.
    """

    enabled: bool = proto.Field(
        proto.BOOL,
        number=1,
    )
    model_version: str = proto.Field(
        proto.STRING,
        number=2,
    )


class AutoMlParams(proto.Message):
    r"""Parameters to control AutoML model prediction behavior.

    Attributes:
        model (str):
            Resource name of the AutoML model.

            Format:
            ``projects/{project-id}/locations/{location-id}/models/{model-id}``.
    """

    model: str = proto.Field(
        proto.STRING,
        number=1,
    )


class InputConfig(proto.Message):
    r"""The desired input location and metadata.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        gcs_source (google.cloud.documentai_v1beta2.types.GcsSource):
            The Google Cloud Storage location to read the
            input from. This must be a single file.

            This field is a member of `oneof`_ ``source``.
        contents (bytes):
            Content in bytes, represented as a stream of bytes. Note: As
            with all ``bytes`` fields, proto buffer messages use a pure
            binary representation, whereas JSON representations use
            base64.

            This field only works for synchronous ProcessDocument
            method.

            This field is a member of `oneof`_ ``source``.
        mime_type (str):
            Required. Mimetype of the input. Current supported mimetypes
            are application/pdf, image/tiff, and image/gif. In addition,
            application/json type is supported for requests with
            [ProcessDocumentRequest.automl_params][google.cloud.documentai.v1beta2.ProcessDocumentRequest.automl_params]
            field set. The JSON file needs to be in
            [Document][google.cloud.documentai.v1beta2.Document] format.
    """

    gcs_source: "GcsSource" = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="source",
        message="GcsSource",
    )
    contents: bytes = proto.Field(
        proto.BYTES,
        number=3,
        oneof="source",
    )
    mime_type: str = proto.Field(
        proto.STRING,
        number=2,
    )


class OutputConfig(proto.Message):
    r"""The desired output location and metadata.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        gcs_destination (google.cloud.documentai_v1beta2.types.GcsDestination):
            The Google Cloud Storage location to write
            the output to.

            This field is a member of `oneof`_ ``destination``.
        pages_per_shard (int):
            The max number of pages to include into each output Document
            shard JSON on Google Cloud Storage.

            The valid range is [1, 100]. If not specified, the default
            value is 20.

            For example, for one pdf file with 100 pages, 100 parsed
            pages will be produced. If ``pages_per_shard`` = 20, then 5
            Document shard JSON files each containing 20 parsed pages
            will be written under the prefix
            [OutputConfig.gcs_destination.uri][] and suffix
            pages-x-to-y.json where x and y are 1-indexed page numbers.

            Example GCS outputs with 157 pages and pages_per_shard = 50:

            pages-001-to-050.json pages-051-to-100.json
            pages-101-to-150.json pages-151-to-157.json
    """

    gcs_destination: "GcsDestination" = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="destination",
        message="GcsDestination",
    )
    pages_per_shard: int = proto.Field(
        proto.INT32,
        number=2,
    )


class GcsSource(proto.Message):
    r"""The Google Cloud Storage location where the input file will
    be read from.

    Attributes:
        uri (str):

    """

    uri: str = proto.Field(
        proto.STRING,
        number=1,
    )


class GcsDestination(proto.Message):
    r"""The Google Cloud Storage location where the output file will
    be written to.

    Attributes:
        uri (str):

    """

    uri: str = proto.Field(
        proto.STRING,
        number=1,
    )


class OperationMetadata(proto.Message):
    r"""Contains metadata for the BatchProcessDocuments operation.

    Attributes:
        state (google.cloud.documentai_v1beta2.types.OperationMetadata.State):
            The state of the current batch processing.
        state_message (str):
            A message providing more details about the
            current state of processing.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            The creation time of the operation.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            The last update time of the operation.
    """

    class State(proto.Enum):
        r"""

        Values:
            STATE_UNSPECIFIED (0):
                The default value. This value is used if the
                state is omitted.
            ACCEPTED (1):
                Request is received.
            WAITING (2):
                Request operation is waiting for scheduling.
            RUNNING (3):
                Request is being processed.
            SUCCEEDED (4):
                The batch processing completed successfully.
            CANCELLED (5):
                The batch processing was cancelled.
            FAILED (6):
                The batch processing has failed.
        """
        STATE_UNSPECIFIED = 0
        ACCEPTED = 1
        WAITING = 2
        RUNNING = 3
        SUCCEEDED = 4
        CANCELLED = 5
        FAILED = 6

    state: State = proto.Field(
        proto.ENUM,
        number=1,
        enum=State,
    )
    state_message: str = proto.Field(
        proto.STRING,
        number=2,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
