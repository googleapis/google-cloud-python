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

from google.cloud.dialogflow_v2beta1.types import gcs
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.dialogflow.v2beta1",
    manifest={
        "Document",
        "GetDocumentRequest",
        "ListDocumentsRequest",
        "ListDocumentsResponse",
        "CreateDocumentRequest",
        "ImportDocumentsRequest",
        "ImportDocumentTemplate",
        "ImportDocumentsResponse",
        "DeleteDocumentRequest",
        "UpdateDocumentRequest",
        "KnowledgeOperationMetadata",
        "ReloadDocumentRequest",
    },
)


class Document(proto.Message):
    r"""A knowledge document to be used by a
    [KnowledgeBase][google.cloud.dialogflow.v2beta1.KnowledgeBase].

    For more information, see the `knowledge base
    guide <https://cloud.google.com/dialogflow/docs/how/knowledge-bases>`__.

    Note: The ``projects.agent.knowledgeBases.documents`` resource is
    deprecated; only use ``projects.knowledgeBases.documents``.

    Attributes:
        name (str):
            Optional. The document resource name. The name must be empty
            when creating a document. Format:
            ``projects/<Project ID>/locations/<Location ID>/knowledgeBases/<Knowledge Base ID>/documents/<Document ID>``.
        display_name (str):
            Required. The display name of the document.
            The name must be 1024 bytes or less; otherwise,
            the creation request fails.
        mime_type (str):
            Required. The MIME type of this document.
        knowledge_types (Sequence[google.cloud.dialogflow_v2beta1.types.Document.KnowledgeType]):
            Required. The knowledge type of document
            content.
        content_uri (str):
            The URI where the file content is located.

            For documents stored in Google Cloud Storage, these URIs
            must have the form ``gs://<bucket-name>/<object-name>``.

            NOTE: External URLs must correspond to public webpages,
            i.e., they must be indexed by Google Search. In particular,
            URLs for showing documents in Google Cloud Storage (i.e. the
            URL in your browser) are not supported. Instead use the
            ``gs://`` format URI described above.
        content (str):
            The raw content of the document. This field is only
            permitted for EXTRACTIVE_QA and FAQ knowledge types. Note:
            This field is in the process of being deprecated, please use
            raw_content instead.
        raw_content (bytes):
            The raw content of the document. This field is only
            permitted for EXTRACTIVE_QA and FAQ knowledge types.
        enable_auto_reload (bool):
            Optional. If true, we try to automatically reload the
            document every day (at a time picked by the system). If
            false or unspecified, we don't try to automatically reload
            the document.

            Currently you can only enable automatic reload for documents
            sourced from a public url, see ``source`` field for the
            source types.

            Reload status can be tracked in ``latest_reload_status``. If
            a reload fails, we will keep the document unchanged.

            If a reload fails with internal errors, the system will try
            to reload the document on the next day. If a reload fails
            with non-retriable errors (e.g. PERMISION_DENIED), the
            system will not try to reload the document anymore. You need
            to manually reload the document successfully by calling
            ``ReloadDocument`` and clear the errors.
        latest_reload_status (google.cloud.dialogflow_v2beta1.types.Document.ReloadStatus):
            Output only. The time and status of the
            latest reload. This reload may have been
            triggered automatically or manually and may not
            have succeeded.
        metadata (Sequence[google.cloud.dialogflow_v2beta1.types.Document.MetadataEntry]):
            Optional. Metadata for the document. The metadata supports
            arbitrary key-value pairs. Suggested use cases include
            storing a document's title, an external URL distinct from
            the document's content_uri, etc. The max size of a ``key``
            or a ``value`` of the metadata is 1024 bytes.
    """

    class KnowledgeType(proto.Enum):
        r"""The knowledge type of document content."""
        KNOWLEDGE_TYPE_UNSPECIFIED = 0
        FAQ = 1
        EXTRACTIVE_QA = 2
        ARTICLE_SUGGESTION = 3
        SMART_REPLY = 4

    class ReloadStatus(proto.Message):
        r"""The status of a reload attempt.
        Attributes:
            time (google.protobuf.timestamp_pb2.Timestamp):
                Output only. The time of a reload attempt.
                This reload may have been triggered
                automatically or manually and may not have
                succeeded.
            status (google.rpc.status_pb2.Status):
                Output only. The status of a reload attempt
                or the initial load.
        """

        time = proto.Field(proto.MESSAGE, number=1, message=timestamp_pb2.Timestamp,)
        status = proto.Field(proto.MESSAGE, number=2, message=status_pb2.Status,)

    name = proto.Field(proto.STRING, number=1,)
    display_name = proto.Field(proto.STRING, number=2,)
    mime_type = proto.Field(proto.STRING, number=3,)
    knowledge_types = proto.RepeatedField(proto.ENUM, number=4, enum=KnowledgeType,)
    content_uri = proto.Field(proto.STRING, number=5, oneof="source",)
    content = proto.Field(proto.STRING, number=6, oneof="source",)
    raw_content = proto.Field(proto.BYTES, number=9, oneof="source",)
    enable_auto_reload = proto.Field(proto.BOOL, number=11,)
    latest_reload_status = proto.Field(proto.MESSAGE, number=12, message=ReloadStatus,)
    metadata = proto.MapField(proto.STRING, proto.STRING, number=7,)


class GetDocumentRequest(proto.Message):
    r"""Request message for
    [Documents.GetDocument][google.cloud.dialogflow.v2beta1.Documents.GetDocument].

    Attributes:
        name (str):
            Required. The name of the document to retrieve. Format
            ``projects/<Project ID>/locations/<Location ID>/knowledgeBases/<Knowledge Base ID>/documents/<Document ID>``.
    """

    name = proto.Field(proto.STRING, number=1,)


class ListDocumentsRequest(proto.Message):
    r"""Request message for
    [Documents.ListDocuments][google.cloud.dialogflow.v2beta1.Documents.ListDocuments].

    Attributes:
        parent (str):
            Required. The knowledge base to list all documents for.
            Format:
            ``projects/<Project ID>/locations/<Location ID>/knowledgeBases/<Knowledge Base ID>``.
        page_size (int):
            The maximum number of items to return in a
            single page. By default 10 and at most 100.
        page_token (str):
            The next_page_token value returned from a previous list
            request.
        filter (str):
            The filter expression used to filter documents returned by
            the list method. The expression has the following syntax:

             [AND ] ...

            The following fields and operators are supported:

            -  knowledge_types with has(:) operator
            -  display_name with has(:) operator
            -  state with equals(=) operator

            Examples:

            -  "knowledge_types:FAQ" matches documents with FAQ
               knowledge type.
            -  "display_name:customer" matches documents whose display
               name contains "customer".
            -  "state=ACTIVE" matches documents with ACTIVE state.
            -  "knowledge_types:FAQ AND state=ACTIVE" matches all active
               FAQ documents.

            For more information about filtering, see `API
            Filtering <https://aip.dev/160>`__.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)
    filter = proto.Field(proto.STRING, number=4,)


class ListDocumentsResponse(proto.Message):
    r"""Response message for
    [Documents.ListDocuments][google.cloud.dialogflow.v2beta1.Documents.ListDocuments].

    Attributes:
        documents (Sequence[google.cloud.dialogflow_v2beta1.types.Document]):
            The list of documents.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
    """

    @property
    def raw_page(self):
        return self

    documents = proto.RepeatedField(proto.MESSAGE, number=1, message="Document",)
    next_page_token = proto.Field(proto.STRING, number=2,)


class CreateDocumentRequest(proto.Message):
    r"""Request message for
    [Documents.CreateDocument][google.cloud.dialogflow.v2beta1.Documents.CreateDocument].

    Attributes:
        parent (str):
            Required. The knowledge base to create a document for.
            Format:
            ``projects/<Project ID>/locations/<Location ID>/knowledgeBases/<Knowledge Base ID>``.
        document (google.cloud.dialogflow_v2beta1.types.Document):
            Required. The document to create.
        import_gcs_custom_metadata (bool):
            Whether to import custom metadata from Google
            Cloud Storage. Only valid when the document
            source is Google Cloud Storage URI.
    """

    parent = proto.Field(proto.STRING, number=1,)
    document = proto.Field(proto.MESSAGE, number=2, message="Document",)
    import_gcs_custom_metadata = proto.Field(proto.BOOL, number=3,)


class ImportDocumentsRequest(proto.Message):
    r"""Request message for
    [Documents.ImportDocuments][google.cloud.dialogflow.v2beta1.Documents.ImportDocuments].

    Attributes:
        parent (str):
            Required. The knowledge base to import documents into.
            Format:
            ``projects/<Project ID>/locations/<Location ID>/knowledgeBases/<Knowledge Base ID>``.
        gcs_source (google.cloud.dialogflow_v2beta1.types.GcsSources):
            The Google Cloud Storage location for the documents. The
            path can include a wildcard.

            These URIs may have the forms
            ``gs://<bucket-name>/<object-name>``.
            ``gs://<bucket-name>/<object-path>/*.<extension>``.
        document_template (google.cloud.dialogflow_v2beta1.types.ImportDocumentTemplate):
            Required. Document template used for
            importing all the documents.
        import_gcs_custom_metadata (bool):
            Whether to import custom metadata from Google
            Cloud Storage. Only valid when the document
            source is Google Cloud Storage URI.
    """

    parent = proto.Field(proto.STRING, number=1,)
    gcs_source = proto.Field(
        proto.MESSAGE, number=2, oneof="source", message=gcs.GcsSources,
    )
    document_template = proto.Field(
        proto.MESSAGE, number=3, message="ImportDocumentTemplate",
    )
    import_gcs_custom_metadata = proto.Field(proto.BOOL, number=4,)


class ImportDocumentTemplate(proto.Message):
    r"""The template used for importing documents.
    Attributes:
        mime_type (str):
            Required. The MIME type of the document.
        knowledge_types (Sequence[google.cloud.dialogflow_v2beta1.types.Document.KnowledgeType]):
            Required. The knowledge type of document
            content.
        metadata (Sequence[google.cloud.dialogflow_v2beta1.types.ImportDocumentTemplate.MetadataEntry]):
            Metadata for the document. The metadata supports arbitrary
            key-value pairs. Suggested use cases include storing a
            document's title, an external URL distinct from the
            document's content_uri, etc. The max size of a ``key`` or a
            ``value`` of the metadata is 1024 bytes.
    """

    mime_type = proto.Field(proto.STRING, number=1,)
    knowledge_types = proto.RepeatedField(
        proto.ENUM, number=2, enum="Document.KnowledgeType",
    )
    metadata = proto.MapField(proto.STRING, proto.STRING, number=3,)


class ImportDocumentsResponse(proto.Message):
    r"""Response message for
    [Documents.ImportDocuments][google.cloud.dialogflow.v2beta1.Documents.ImportDocuments].

    Attributes:
        warnings (Sequence[google.rpc.status_pb2.Status]):
            Includes details about skipped documents or
            any other warnings.
    """

    warnings = proto.RepeatedField(proto.MESSAGE, number=1, message=status_pb2.Status,)


class DeleteDocumentRequest(proto.Message):
    r"""Request message for
    [Documents.DeleteDocument][google.cloud.dialogflow.v2beta1.Documents.DeleteDocument].

    Attributes:
        name (str):
            Required. The name of the document to delete. Format:
            ``projects/<Project ID>/locations/<Location ID>/knowledgeBases/<Knowledge Base ID>/documents/<Document ID>``.
    """

    name = proto.Field(proto.STRING, number=1,)


class UpdateDocumentRequest(proto.Message):
    r"""Request message for
    [Documents.UpdateDocument][google.cloud.dialogflow.v2beta1.Documents.UpdateDocument].

    Attributes:
        document (google.cloud.dialogflow_v2beta1.types.Document):
            Required. The document to update.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Optional. Not specified means ``update all``. Currently,
            only ``display_name`` can be updated, an InvalidArgument
            will be returned for attempting to update other fields.
    """

    document = proto.Field(proto.MESSAGE, number=1, message="Document",)
    update_mask = proto.Field(
        proto.MESSAGE, number=2, message=field_mask_pb2.FieldMask,
    )


class KnowledgeOperationMetadata(proto.Message):
    r"""Metadata in google::longrunning::Operation for Knowledge
    operations.

    Attributes:
        state (google.cloud.dialogflow_v2beta1.types.KnowledgeOperationMetadata.State):
            Required. Output only. The current state of
            this operation.
    """

    class State(proto.Enum):
        r"""States of the operation."""
        STATE_UNSPECIFIED = 0
        PENDING = 1
        RUNNING = 2
        DONE = 3

    state = proto.Field(proto.ENUM, number=1, enum=State,)


class ReloadDocumentRequest(proto.Message):
    r"""Request message for
    [Documents.ReloadDocument][google.cloud.dialogflow.v2beta1.Documents.ReloadDocument].

    Attributes:
        name (str):
            Required. The name of the document to reload. Format:
            ``projects/<Project ID>/locations/<Location ID>/knowledgeBases/<Knowledge Base ID>/documents/<Document ID>``
        gcs_source (google.cloud.dialogflow_v2beta1.types.GcsSource):
            The path for a Cloud Storage source file for
            reloading document content. If not provided, the
            Document's existing source will be reloaded.
        import_gcs_custom_metadata (bool):
            Whether to import custom metadata from Google
            Cloud Storage. Only valid when the document
            source is Google Cloud Storage URI.
    """

    name = proto.Field(proto.STRING, number=1,)
    gcs_source = proto.Field(
        proto.MESSAGE, number=3, oneof="source", message=gcs.GcsSource,
    )
    import_gcs_custom_metadata = proto.Field(proto.BOOL, number=4,)


__all__ = tuple(sorted(__protobuf__.manifest))
