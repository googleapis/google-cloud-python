# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
from __future__ import annotations

from typing import MutableMapping, MutableSequence

from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.translate_v3.types import common

__protobuf__ = proto.module(
    package="google.cloud.translation.v3",
    manifest={
        "AdaptiveMtDataset",
        "CreateAdaptiveMtDatasetRequest",
        "DeleteAdaptiveMtDatasetRequest",
        "GetAdaptiveMtDatasetRequest",
        "ListAdaptiveMtDatasetsRequest",
        "ListAdaptiveMtDatasetsResponse",
        "AdaptiveMtTranslateRequest",
        "AdaptiveMtTranslation",
        "AdaptiveMtTranslateResponse",
        "AdaptiveMtFile",
        "GetAdaptiveMtFileRequest",
        "DeleteAdaptiveMtFileRequest",
        "ImportAdaptiveMtFileRequest",
        "ImportAdaptiveMtFileResponse",
        "ListAdaptiveMtFilesRequest",
        "ListAdaptiveMtFilesResponse",
        "AdaptiveMtSentence",
        "ListAdaptiveMtSentencesRequest",
        "ListAdaptiveMtSentencesResponse",
    },
)


class AdaptiveMtDataset(proto.Message):
    r"""An Adaptive MT Dataset.

    Attributes:
        name (str):
            Required. The resource name of the dataset, in form of
            ``projects/{project-number-or-id}/locations/{location_id}/adaptiveMtDatasets/{dataset_id}``
        display_name (str):
            The name of the dataset to show in the interface. The name
            can be up to 32 characters long and can consist only of
            ASCII Latin letters A-Z and a-z, underscores (_), and ASCII
            digits 0-9.
        source_language_code (str):
            The BCP-47 language code of the source
            language.
        target_language_code (str):
            The BCP-47 language code of the target
            language.
        example_count (int):
            The number of examples in the dataset.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Timestamp when this dataset was
            created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Timestamp when this dataset was
            last updated.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=2,
    )
    source_language_code: str = proto.Field(
        proto.STRING,
        number=3,
    )
    target_language_code: str = proto.Field(
        proto.STRING,
        number=4,
    )
    example_count: int = proto.Field(
        proto.INT32,
        number=5,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=9,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=10,
        message=timestamp_pb2.Timestamp,
    )


class CreateAdaptiveMtDatasetRequest(proto.Message):
    r"""Request message for creating an AdaptiveMtDataset.

    Attributes:
        parent (str):
            Required. Name of the parent project. In form of
            ``projects/{project-number-or-id}/locations/{location-id}``
        adaptive_mt_dataset (google.cloud.translate_v3.types.AdaptiveMtDataset):
            Required. The AdaptiveMtDataset to be
            created.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    adaptive_mt_dataset: "AdaptiveMtDataset" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="AdaptiveMtDataset",
    )


class DeleteAdaptiveMtDatasetRequest(proto.Message):
    r"""Request message for deleting an AdaptiveMtDataset.

    Attributes:
        name (str):
            Required. Name of the dataset. In the form of
            ``projects/{project-number-or-id}/locations/{location-id}/adaptiveMtDatasets/{adaptive-mt-dataset-id}``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class GetAdaptiveMtDatasetRequest(proto.Message):
    r"""Request message for getting an Adaptive MT dataset.

    Attributes:
        name (str):
            Required. Name of the dataset. In the form of
            ``projects/{project-number-or-id}/locations/{location-id}/adaptiveMtDatasets/{adaptive-mt-dataset-id}``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListAdaptiveMtDatasetsRequest(proto.Message):
    r"""Request message for listing all Adaptive MT datasets that the
    requestor has access to.

    Attributes:
        parent (str):
            Required. The resource name of the project from which to
            list the Adaptive MT datasets.
            ``projects/{project-number-or-id}/locations/{location-id}``
        page_size (int):
            Optional. Requested page size. The server may
            return fewer results than requested. If
            unspecified, the server picks an appropriate
            default.
        page_token (str):
            Optional. A token identifying a page of results the server
            should return. Typically, this is the value of
            ListAdaptiveMtDatasetsResponse.next_page_token returned from
            the previous call to ``ListAdaptiveMtDatasets`` method. The
            first page is returned if ``page_token``\ is empty or
            missing.
        filter (str):
            Optional. An expression for filtering the
            results of the request. Filter is not supported
            yet.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )
    filter: str = proto.Field(
        proto.STRING,
        number=4,
    )


class ListAdaptiveMtDatasetsResponse(proto.Message):
    r"""A list of AdaptiveMtDatasets.

    Attributes:
        adaptive_mt_datasets (MutableSequence[google.cloud.translate_v3.types.AdaptiveMtDataset]):
            Output only. A list of Adaptive MT datasets.
        next_page_token (str):
            Optional. A token to retrieve a page of results. Pass this
            value in the [ListAdaptiveMtDatasetsRequest.page_token]
            field in the subsequent call to ``ListAdaptiveMtDatasets``
            method to retrieve the next page of results.
    """

    @property
    def raw_page(self):
        return self

    adaptive_mt_datasets: MutableSequence["AdaptiveMtDataset"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="AdaptiveMtDataset",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class AdaptiveMtTranslateRequest(proto.Message):
    r"""The request for sending an AdaptiveMt translation query.

    Attributes:
        parent (str):
            Required. Location to make a regional call.

            Format:
            ``projects/{project-number-or-id}/locations/{location-id}``.
        dataset (str):
            Required. The resource name for the dataset to use for
            adaptive MT.
            ``projects/{project}/locations/{location-id}/adaptiveMtDatasets/{dataset}``
        content (MutableSequence[str]):
            Required. The content of the input in string
            format. For now only one sentence per request is
            supported.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    dataset: str = proto.Field(
        proto.STRING,
        number=2,
    )
    content: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class AdaptiveMtTranslation(proto.Message):
    r"""An AdaptiveMt translation.

    Attributes:
        translated_text (str):
            Output only. The translated text.
    """

    translated_text: str = proto.Field(
        proto.STRING,
        number=1,
    )


class AdaptiveMtTranslateResponse(proto.Message):
    r"""An AdaptiveMtTranslate response.

    Attributes:
        translations (MutableSequence[google.cloud.translate_v3.types.AdaptiveMtTranslation]):
            Output only. The translation.
        language_code (str):
            Output only. The translation's language code.
    """

    translations: MutableSequence["AdaptiveMtTranslation"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="AdaptiveMtTranslation",
    )
    language_code: str = proto.Field(
        proto.STRING,
        number=2,
    )


class AdaptiveMtFile(proto.Message):
    r"""An AdaptiveMtFile.

    Attributes:
        name (str):
            Required. The resource name of the file, in form of
            ``projects/{project-number-or-id}/locations/{location_id}/adaptiveMtDatasets/{dataset}/adaptiveMtFiles/{file}``
        display_name (str):
            The file's display name.
        entry_count (int):
            The number of entries that the file contains.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Timestamp when this file was
            created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Timestamp when this file was
            last updated.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=2,
    )
    entry_count: int = proto.Field(
        proto.INT32,
        number=3,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )


class GetAdaptiveMtFileRequest(proto.Message):
    r"""The request for getting an AdaptiveMtFile.

    Attributes:
        name (str):
            Required. The resource name of the file, in form of
            ``projects/{project-number-or-id}/locations/{location_id}/adaptiveMtDatasets/{dataset}/adaptiveMtFiles/{file}``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class DeleteAdaptiveMtFileRequest(proto.Message):
    r"""The request for deleting an AdaptiveMt file.

    Attributes:
        name (str):
            Required. The resource name of the file to delete, in form
            of
            ``projects/{project-number-or-id}/locations/{location_id}/adaptiveMtDatasets/{dataset}/adaptiveMtFiles/{file}``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ImportAdaptiveMtFileRequest(proto.Message):
    r"""The request for importing an AdaptiveMt file along with its
    sentences.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        parent (str):
            Required. The resource name of the file, in form of
            ``projects/{project-number-or-id}/locations/{location_id}/adaptiveMtDatasets/{dataset}``
        file_input_source (google.cloud.translate_v3.types.FileInputSource):
            Inline file source.

            This field is a member of `oneof`_ ``source``.
        gcs_input_source (google.cloud.translate_v3.types.GcsInputSource):
            Google Cloud Storage file source.

            This field is a member of `oneof`_ ``source``.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    file_input_source: common.FileInputSource = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="source",
        message=common.FileInputSource,
    )
    gcs_input_source: common.GcsInputSource = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="source",
        message=common.GcsInputSource,
    )


class ImportAdaptiveMtFileResponse(proto.Message):
    r"""The response for importing an AdaptiveMtFile

    Attributes:
        adaptive_mt_file (google.cloud.translate_v3.types.AdaptiveMtFile):
            Output only. The Adaptive MT file that was
            imported.
    """

    adaptive_mt_file: "AdaptiveMtFile" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="AdaptiveMtFile",
    )


class ListAdaptiveMtFilesRequest(proto.Message):
    r"""The request to list all AdaptiveMt files under a given
    dataset.

    Attributes:
        parent (str):
            Required. The resource name of the project from which to
            list the Adaptive MT files.
            ``projects/{project}/locations/{location}/adaptiveMtDatasets/{dataset}``
        page_size (int):
            Optional.
        page_token (str):
            Optional. A token identifying a page of results the server
            should return. Typically, this is the value of
            ListAdaptiveMtFilesResponse.next_page_token returned from
            the previous call to ``ListAdaptiveMtFiles`` method. The
            first page is returned if ``page_token``\ is empty or
            missing.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ListAdaptiveMtFilesResponse(proto.Message):
    r"""The response for listing all AdaptiveMt files under a given
    dataset.

    Attributes:
        adaptive_mt_files (MutableSequence[google.cloud.translate_v3.types.AdaptiveMtFile]):
            Output only. The Adaptive MT files.
        next_page_token (str):
            Optional. A token to retrieve a page of results. Pass this
            value in the ListAdaptiveMtFilesRequest.page_token field in
            the subsequent call to ``ListAdaptiveMtFiles`` method to
            retrieve the next page of results.
    """

    @property
    def raw_page(self):
        return self

    adaptive_mt_files: MutableSequence["AdaptiveMtFile"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="AdaptiveMtFile",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )


class AdaptiveMtSentence(proto.Message):
    r"""An AdaptiveMt sentence entry.

    Attributes:
        name (str):
            Required. The resource name of the file, in form of
            ``projects/{project-number-or-id}/locations/{location_id}/adaptiveMtDatasets/{dataset}/adaptiveMtFiles/{file}/adaptiveMtSentences/{sentence}``
        source_sentence (str):
            Required. The source sentence.
        target_sentence (str):
            Required. The target sentence.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Timestamp when this sentence was
            created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Timestamp when this sentence was
            last updated.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    source_sentence: str = proto.Field(
        proto.STRING,
        number=2,
    )
    target_sentence: str = proto.Field(
        proto.STRING,
        number=3,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )


class ListAdaptiveMtSentencesRequest(proto.Message):
    r"""The request for listing Adaptive MT sentences from a
    Dataset/File.

    Attributes:
        parent (str):
            Required. The resource name of the project from which to
            list the Adaptive MT files. The following format lists all
            sentences under a file.
            ``projects/{project}/locations/{location}/adaptiveMtDatasets/{dataset}/adaptiveMtFiles/{file}``
            The following format lists all sentences within a dataset.
            ``projects/{project}/locations/{location}/adaptiveMtDatasets/{dataset}``
        page_size (int):

        page_token (str):
            A token identifying a page of results the server should
            return. Typically, this is the value of
            ListAdaptiveMtSentencesRequest.next_page_token returned from
            the previous call to ``ListTranslationMemories`` method. The
            first page is returned if ``page_token`` is empty or
            missing.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ListAdaptiveMtSentencesResponse(proto.Message):
    r"""List AdaptiveMt sentences response.

    Attributes:
        adaptive_mt_sentences (MutableSequence[google.cloud.translate_v3.types.AdaptiveMtSentence]):
            Output only. The list of AdaptiveMtSentences.
        next_page_token (str):
            Optional.
    """

    @property
    def raw_page(self):
        return self

    adaptive_mt_sentences: MutableSequence["AdaptiveMtSentence"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="AdaptiveMtSentence",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
