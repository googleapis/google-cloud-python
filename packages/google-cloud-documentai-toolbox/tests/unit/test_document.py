# pylint: disable=protected-access
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

import os
import shutil

# try/except added for compatibility with python < 3.8
try:
    from unittest import mock
except ImportError:  # pragma: NO COVER
    import mock

import pytest
import glob

from google.cloud.documentai_toolbox import document
from google.cloud.documentai_toolbox import gcs_utilities

from google.cloud import documentai
from google.cloud.vision import AnnotateFileResponse


def get_bytes(file_name):
    result = []
    for filename in glob.glob(os.path.join(file_name, "*.json")):
        with open(os.path.join(os.getcwd(), filename), "rb") as f:
            result.append(f.read())

    return result


@pytest.fixture
def get_bytes_single_file_mock():
    with mock.patch.object(gcs_utilities, "get_bytes") as byte_factory:
        byte_factory.return_value = get_bytes("tests/unit/resources/0")
        yield byte_factory


@pytest.fixture
def get_bytes_multiple_files_mock():
    with mock.patch.object(gcs_utilities, "get_bytes") as byte_factory:
        byte_factory.return_value = get_bytes("tests/unit/resources/1")
        yield byte_factory


@pytest.fixture
def get_bytes_unordered_files_mock():
    with mock.patch.object(gcs_utilities, "get_bytes") as byte_factory:
        byte_factory.return_value = get_bytes("tests/unit/resources/unordered_shards")
        yield byte_factory


@pytest.fixture(params=["tests/unit/resources/0", "tests/unit/resources/1"])
def get_bytes_multiple_directories_mock(request):
    with mock.patch.object(gcs_utilities, "get_bytes") as byte_factory:
        byte_factory.return_value = get_bytes(request.param)
        yield byte_factory


@pytest.fixture
def get_bytes_form_parser_mock():
    with mock.patch.object(gcs_utilities, "get_bytes") as byte_factory:
        byte_factory.return_value = get_bytes("tests/unit/resources/form_parser")
        yield byte_factory


@pytest.fixture
def get_bytes_splitter_mock():
    with mock.patch.object(gcs_utilities, "get_bytes") as byte_factory:
        byte_factory.return_value = get_bytes("tests/unit/resources/splitter")
        yield byte_factory


@pytest.fixture
def get_bytes_images_mock():
    with mock.patch.object(gcs_utilities, "get_bytes") as byte_factory:
        byte_factory.return_value = get_bytes("tests/unit/resources/images")
        yield byte_factory


def test_get_shards_with_gcs_uri_contains_file_type():
    with pytest.raises(ValueError, match="gcs_prefix cannot contain file types"):
        document._get_shards(
            gcs_bucket_name="test-directory",
            gcs_prefix="documentai/output/123456789/0.json",
        )


def test_get_shards_with_valid_gcs_uri(get_bytes_single_file_mock):
    actual = document._get_shards(
        gcs_bucket_name="test-directory", gcs_prefix="documentai/output/123456789/0/"
    )

    get_bytes_single_file_mock.assert_called_once()
    # We are testing only one of the fields to make sure the file content could be loaded.
    assert actual[0].pages[0].page_number == 1


def test_pages_from_shards():
    shards = []
    for byte in get_bytes("tests/unit/resources/0"):
        shards.append(documentai.Document.from_json(byte))

    actual = document._pages_from_shards(shards=shards)
    assert len(actual[0].paragraphs) == 31

    for page_index, page in enumerate(actual):
        assert page.documentai_page.page_number == page_index + 1


def test_entities_from_shard():
    shards = []
    for byte in get_bytes("tests/unit/resources/0"):
        shards.append(documentai.Document.from_json(byte))

    actual = document._entities_from_shards(shards=shards)

    assert actual[0].mention_text == "$140.00"
    assert actual[0].type_ == "vat"
    assert actual[1].mention_text == "$140.00"
    assert actual[1].type_ == "vat/tax_amount"
    assert actual[1].normalized_text == "140 USD"


@mock.patch("google.cloud.documentai_toolbox.wrappers.document.documentai")
def test_get_batch_process_metadata_with_valid_operation(
    mock_docai,
):
    mock_client = mock_docai.DocumentProcessorServiceClient.return_value

    metadata = documentai.BatchProcessMetadata(
        state=documentai.BatchProcessMetadata.State.SUCCEEDED,
        individual_process_statuses=[
            documentai.BatchProcessMetadata.IndividualProcessStatus(
                input_gcs_source="gs://test-directory/documentai/input.pdf",
                output_gcs_destination="gs://test-directory/documentai/output/123456789/1/",
            )
        ],
    )

    mock_operation = mock.Mock(
        done=True,
        metadata=mock.Mock(
            type_url="type.googleapis.com/google.cloud.documentai.v1.BatchProcessMetadata",
            value=documentai.BatchProcessMetadata.serialize(metadata),
        ),
    )

    mock_client.get_operation.return_value = mock_operation

    location = "us"
    operation_name = "projects/123456/locations/us/operations/7890123"
    document._get_batch_process_metadata(location, operation_name)

    mock_client.get_operation.assert_called()
    mock_docai.BatchProcessMetadata.deserialize.assert_called()


@mock.patch("google.cloud.documentai_toolbox.wrappers.document.documentai")
def test_get_batch_process_metadata_with_no_metadata(mock_docai):
    with pytest.raises(
        ValueError,
        match="Operation does not contain metadata:",
    ):
        mock_client = mock_docai.DocumentProcessorServiceClient.return_value

        location = "us"
        operation_name = "projects/123456/locations/us/operations/7890123"
        mock_operation = mock.Mock(done=True, metadata=None)
        mock_client.get_operation.return_value = mock_operation

        document._get_batch_process_metadata(location, operation_name)


@mock.patch("google.cloud.documentai_toolbox.wrappers.document.documentai")
def test_get_batch_process_metadata_with_invalid_metadata_type(mock_docai):
    with pytest.raises(
        ValueError,
        match="Operation metadata type is not",
    ):
        mock_client = mock_docai.DocumentProcessorServiceClient.return_value

        location = "us"
        operation_name = "projects/123456/locations/us/operations/7890123"
        mock_operation = mock.Mock(
            done=True,
            metadata=mock.Mock(
                type_url="type.googleapis.com/google.cloud.documentai.uiv1beta3.TrainProcessorVersionResponse",
            ),
        )
        mock_client.get_operation.return_value = mock_operation

        document._get_batch_process_metadata(location, operation_name)


def test_bigquery_column_name():
    string_map = {
        "Phone #:": "phone_num",
        "Emergency Contact:": "emergency_contact",
        "Marital Status:": "marital_status",
        "Are you currently taking any medication? (If yes, please describe):": "are_you_currently_taking_any_medication_if_yes_please_describe",
        "Describe your medical concerns (symptoms, diagnoses, etc):": "describe_your_medical_concerns_symptoms_diagnoses_etc",
    }

    for key, value in string_map.items():
        assert document._bigquery_column_name(key) == value


def test_document_from_document_path_with_single_shard():
    actual = document.Document.from_document_path(
        document_path="tests/unit/resources/0/toolbox_invoice_test-0.json"
    )
    assert len(actual.pages) == 1


def test_document_from_documentai_document_with_single_shard():
    with open(
        "tests/unit/resources/0/toolbox_invoice_test-0.json", "r", encoding="utf-8"
    ) as f:
        doc = documentai.Document.from_json(f.read())

    actual = document.Document.from_documentai_document(documentai_document=doc)
    assert len(actual.pages) == 1


def test_document_from_gcs_with_single_shard(get_bytes_single_file_mock):
    actual = document.Document.from_gcs(
        gcs_bucket_name="test-directory", gcs_prefix="documentai/output/123456789/0/"
    )

    get_bytes_single_file_mock.assert_called_once()
    assert len(actual.pages) == 1


def test_document_from_gcs_with_multiple_shards(get_bytes_multiple_files_mock):
    actual = document.Document.from_gcs(
        gcs_bucket_name="test-directory", gcs_prefix="documentai/output/123456789/1/"
    )
    get_bytes_multiple_files_mock.assert_called_once()

    assert len(actual.pages) == 48


def test_document_from_gcs_with_unordered_shards(get_bytes_unordered_files_mock):
    actual = document.Document.from_gcs(
        gcs_bucket_name="test-directory", gcs_prefix="documentai/output/123456789/2/"
    )
    get_bytes_unordered_files_mock.assert_called_once()

    expected_shard_count = len(actual.shards)
    current_text_offset = 0
    for expected_shard_index, shard in enumerate(actual.shards):
        assert int(shard.shard_info.shard_index) == expected_shard_index
        assert int(shard.shard_info.shard_count) == expected_shard_count
        assert int(shard.shard_info.text_offset) == current_text_offset
        current_text_offset += len(shard.text)

    for page_index, page in enumerate(actual.pages):
        assert page.documentai_page.page_number == page_index + 1


def test_document_from_batch_process_metadata_with_multiple_input_files(
    get_bytes_multiple_directories_mock,
):
    mock_metadata = mock.Mock(
        state=documentai.BatchProcessMetadata.State.SUCCEEDED,
        individual_process_statuses=[
            mock.Mock(
                input_gcs_source="gs://test-directory/documentai/input.pdf",
                output_gcs_destination="gs://test-directory/documentai/output/123456789/1/",
            ),
            mock.Mock(
                input_gcs_source="gs://test-directory/documentai/input2.pdf",
                output_gcs_destination="gs://test-directory/documentai/output/123456789/2/",
            ),
        ],
    )
    documents = document.Document.from_batch_process_metadata(mock_metadata)

    get_bytes_multiple_directories_mock.assert_called()
    assert get_bytes_multiple_directories_mock.call_count == 2
    assert len(documents) == 2

    assert documents[0].gcs_bucket_name == "test-directory"
    assert documents[0].gcs_prefix == "documentai/output/123456789/1/"
    assert documents[0].gcs_input_uri == "gs://test-directory/documentai/input.pdf"

    assert documents[1].gcs_bucket_name == "test-directory"
    assert documents[1].gcs_prefix == "documentai/output/123456789/2/"
    assert documents[1].gcs_input_uri == "gs://test-directory/documentai/input2.pdf"


def test_document_from_batch_process_metadata_with_failed_operation():
    with pytest.raises(
        ValueError,
        match="Batch Process Failed: Internal Error Occured",
    ):
        mock_metadata = mock.Mock(
            state=documentai.BatchProcessMetadata.State.FAILED,
            state_message="Internal Error Occured",
        )
        document.Document.from_batch_process_metadata(mock_metadata)


def test_search_page_with_target_string(get_bytes_single_file_mock):
    doc = document.Document.from_gcs(
        gcs_bucket_name="test-directory", gcs_prefix="documentai/output/123456789/0/"
    )

    actual_pages = doc.search_pages(target_string="contract")

    get_bytes_single_file_mock.assert_called_once()
    assert len(actual_pages) == 1


def test_search_page_with_target_pattern(get_bytes_single_file_mock):
    doc = document.Document.from_gcs(
        gcs_bucket_name="test-directory", gcs_prefix="documentai/output/123456789/0/"
    )

    actual_regex = doc.search_pages(pattern=r"\$\d+(?:\.\d+)?")

    get_bytes_single_file_mock.assert_called_once()
    assert len(actual_regex) == 1


def test_search_page_with_multiple_pages(get_bytes_multiple_files_mock):
    doc = document.Document.from_gcs(
        gcs_bucket_name="test-directory", gcs_prefix="documentai/output/123456789/0/"
    )

    actual_pages = doc.search_pages(target_string="Invoice")

    get_bytes_multiple_files_mock.assert_called_once()
    assert len(actual_pages) == 48


def test_search_page_with_no_results(get_bytes_single_file_mock):
    doc = document.Document.from_gcs(
        gcs_bucket_name="test-directory", gcs_prefix="documentai/output/123456789/0/"
    )

    actual_pages = doc.search_pages(target_string="Google")

    get_bytes_single_file_mock.assert_called_once()
    assert len(actual_pages) == 0


def test_search_page_with_regex_and_str(get_bytes_single_file_mock):
    with pytest.raises(
        ValueError,
        match="Exactly one of target_string and pattern must be specified.",
    ):
        doc = document.Document.from_gcs(
            gcs_bucket_name="test-directory",
            gcs_prefix="documentai/output/123456789/0/",
        )
        doc.search_pages(pattern=r"^\$?(\d*(\d\.?|\.\d{1,2}))$", target_string="hello")

        get_bytes_single_file_mock.assert_called_once()


def test_search_page_with_none(get_bytes_single_file_mock):
    with pytest.raises(
        ValueError,
        match="Exactly one of target_string and pattern must be specified.",
    ):
        doc = document.Document.from_gcs(
            gcs_bucket_name="test-directory",
            gcs_prefix="documentai/output/123456789/0/",
        )
        doc.search_pages()

        get_bytes_single_file_mock.assert_called_once()


def test_get_entity_by_type(get_bytes_single_file_mock):
    doc = document.Document.from_gcs(
        gcs_bucket_name="test-directory", gcs_prefix="documentai/output/123456789/0"
    )

    actual = doc.get_entity_by_type(target_type="receiver_address")

    get_bytes_single_file_mock.assert_called_once()

    assert len(actual) == 1
    assert actual[0].type_ == "receiver_address"
    assert actual[0].mention_text == "222 Main Street\nAnytown, USA"


def test_get_form_field_by_name(get_bytes_form_parser_mock):
    doc = document.Document.from_gcs(
        gcs_bucket_name="test-directory", gcs_prefix="documentai/output/123456789/0"
    )
    actual = doc.get_form_field_by_name(target_field="Phone #:")

    get_bytes_form_parser_mock.assert_called_once()

    assert len(actual) == 1
    assert actual[0].field_name == "Phone #:"
    assert actual[0].field_value == "(906) 917-3486"


def test_form_fields_to_dict(get_bytes_form_parser_mock):
    doc = document.Document.from_gcs(
        gcs_bucket_name="test-directory", gcs_prefix="documentai/output/123456789/0"
    )
    actual = doc.form_fields_to_dict()

    get_bytes_form_parser_mock.assert_called_once()

    assert len(actual) == 17
    assert actual.get("address") == "24 Barney Lane"
    assert actual.get("city") == "Towaco"


@mock.patch("google.cloud.documentai_toolbox.wrappers.document.bigquery")
def test_form_fields_to_bigquery(mock_bigquery, get_bytes_form_parser_mock):
    client = mock_bigquery.Client.return_value

    mock_table = mock.Mock()
    client.dataset.table.return_value = mock_table

    mock_load_job = mock.Mock()
    client.load_table_from_json.return_value = mock_load_job

    doc = document.Document.from_gcs(
        gcs_bucket_name="test-directory", gcs_prefix="documentai/output/123456789/0"
    )

    actual = doc.form_fields_to_bigquery(
        dataset_name="test_dataset", table_name="test_table", project_id="test_project"
    )

    get_bytes_form_parser_mock.assert_called_once()
    mock_bigquery.Client.assert_called_once()

    assert actual


def test_entities_to_dict(get_bytes_single_file_mock):
    doc = document.Document.from_gcs(
        gcs_bucket_name="test-directory", gcs_prefix="documentai/output/123456789/0"
    )
    actual = doc.entities_to_dict()

    get_bytes_single_file_mock.assert_called_once()

    assert len(actual) == 25
    assert actual.get("vat") == "$140.00"
    assert actual.get("vat_tax_amount") == "$140.00"


@mock.patch("google.cloud.documentai_toolbox.wrappers.document.bigquery")
def test_entities_to_bigquery(mock_bigquery, get_bytes_single_file_mock):
    client = mock_bigquery.Client.return_value

    mock_table = mock.Mock()
    client.dataset.table.return_value = mock_table

    mock_load_job = mock.Mock()
    client.load_table_from_json.return_value = mock_load_job

    doc = document.Document.from_gcs(
        gcs_bucket_name="test-directory", gcs_prefix="documentai/output/123456789/0"
    )

    actual = doc.entities_to_bigquery(
        dataset_name="test_dataset", table_name="test_table", project_id="test_project"
    )

    get_bytes_single_file_mock.assert_called_once()
    mock_bigquery.Client.assert_called_once()

    assert actual


@mock.patch("google.cloud.documentai_toolbox.wrappers.document.Pdf")
def test_split_pdf(mock_Pdf, get_bytes_splitter_mock):
    doc = document.Document.from_gcs(
        gcs_bucket_name="test-directory", gcs_prefix="documentai/output/123456789/0"
    )
    mock_input_file = mock.Mock()
    mock_Pdf.open.return_value.__enter__.return_value.name = mock_input_file

    mock_output_file = mock.Mock()
    mock_Pdf.new.return_value = mock_output_file

    actual = doc.split_pdf(
        pdf_path="procurement_multi_document.pdf", output_path="splitter/output/"
    )

    get_bytes_splitter_mock.assert_called_once()

    assert actual == [
        "procurement_multi_document_pg1_invoice_statement.pdf",
        "procurement_multi_document_pg2_receipt_statement.pdf",
        "procurement_multi_document_pg3_other.pdf",
        "procurement_multi_document_pg4_utility_statement.pdf",
        "procurement_multi_document_pg5_restaurant_statement.pdf",
        "procurement_multi_document_pg6-7_other.pdf",
    ]


def test_convert_document_to_annotate_file_response():
    doc = document.Document.from_document_path(
        document_path="tests/unit/resources/0/toolbox_invoice_test-0.json"
    )

    actual = doc.convert_document_to_annotate_file_response()

    with open("tests/unit/resources/toolbox_invoice_test-0-vision.json", "r") as f:
        invoice_json = f.read()

    expected = AnnotateFileResponse.from_json(invoice_json)

    assert actual.responses[0].text_annotations[0].description == "Invoice"
    assert len(actual.responses[0].text_annotations) == 86

    assert len(actual.responses[0].full_text_annotation.pages) == 1
    assert actual.responses[0].full_text_annotation.text is not None

    assert actual == expected


def test_export_images(get_bytes_images_mock):
    doc = document.Document.from_gcs(
        gcs_bucket_name="test-directory", gcs_prefix="documentai/output/123456789/0"
    )
    output_path = "resources/output/"

    os.makedirs(output_path)

    actual = doc.export_images(
        output_path=output_path,
        output_file_prefix="exported_photo",
        output_file_extension="png",
    )
    get_bytes_images_mock.assert_called_once()

    assert os.path.exists(output_path)
    shutil.rmtree(output_path)

    assert actual == [
        "exported_photo_0_Portrait.png",
    ]
