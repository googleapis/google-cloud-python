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

import os

from google.cloud import documentai
from google.longrunning.operations_pb2 import \
    ListOperationsRequest  # type: ignore
import pytest

from samples.snippets import quickstart_sample

location = "us"
project_id = os.environ["GOOGLE_CLOUD_PROJECT"]


def test_quickstart_sample_gcs_bucket_prefix(capsys: pytest.CaptureFixture) -> None:
    gcs_bucket_name = "documentai_toolbox_samples"
    gcs_prefix = "output/123456789/0"
    quickstart_sample.quickstart_sample(
        gcs_bucket_name=gcs_bucket_name, gcs_prefix=gcs_prefix
    )
    out, _ = capsys.readouterr()

    assert "Document structure in Cloud Storage" in out
    assert "Number of Pages: 1" in out
    assert "Number of Entities: 35" in out


def test_quickstart_sample_gcs_uri(capsys: pytest.CaptureFixture) -> None:
    gcs_uri = (
        "gs://documentai_toolbox_samples/output/123456789/0/toolbox_invoice_test-0.json"
    )
    quickstart_sample.quickstart_sample(gcs_uri=gcs_uri)
    out, _ = capsys.readouterr()

    assert "Number of Pages: 1" in out
    assert "Number of Entities: 35" in out


def test_quickstart_sample_document_path(capsys: pytest.CaptureFixture) -> None:
    document_path = "resources/form_with_tables.json"
    quickstart_sample.quickstart_sample(document_path=document_path)
    out, _ = capsys.readouterr()

    assert "Number of Pages: 1" in out
    assert "Number of Entities: 0" in out
    assert "Form Date" in out


def test_quickstart_sample_documentai_document(capsys: pytest.CaptureFixture) -> None:
    with open("resources/form_with_tables.json", encoding="utf-8") as f:
        documentai_document = documentai.Document.from_json(
            f.read(), ignore_unknown_fields=True
        )

    quickstart_sample.quickstart_sample(documentai_document=documentai_document)
    out, _ = capsys.readouterr()

    assert "Number of Pages: 1" in out
    assert "Number of Entities: 0" in out
    assert "Form Date" in out


def test_quickstart_sample_batch_process_metadata(
    capsys: pytest.CaptureFixture,
) -> None:
    client = documentai.DocumentProcessorServiceClient()
    name = f"{client.common_location_path(project=project_id, location=location)}/operations"
    response = client.list_operations(
        request=ListOperationsRequest(
            name=name,
            filter="TYPE=BATCH_PROCESS_DOCUMENTS AND STATE=DONE",
            page_size=1,
        )
    )
    batch_process_metadata = documentai.BatchProcessMetadata.deserialize(
        response.operations[0].metadata.value
    )

    quickstart_sample.quickstart_sample(batch_process_metadata=batch_process_metadata)

    out, _ = capsys.readouterr()

    assert "Document Successfully Loaded!" in out


def test_quickstart_sample_batch_process_metadata_matching_prefixes(
    capsys: pytest.CaptureFixture,
) -> None:
    batch_process_metadata = documentai.BatchProcessMetadata(
        state=documentai.BatchProcessMetadata.State.SUCCEEDED,
        individual_process_statuses=[
            documentai.BatchProcessMetadata.IndividualProcessStatus(
                input_gcs_source="gs://test-directory/documentai/input.pdf",
                output_gcs_destination="gs://documentai_toolbox_samples/output/matching-prefixes/1",
            ),
            documentai.BatchProcessMetadata.IndividualProcessStatus(
                input_gcs_source="gs://test-directory/documentai/input.pdf",
                output_gcs_destination="gs://documentai_toolbox_samples/output/matching-prefixes/11",
            ),
        ],
    )
    wrapped_document = quickstart_sample.quickstart_sample(
        batch_process_metadata=batch_process_metadata
    )

    assert wrapped_document.gcs_prefix == "output/matching-prefixes/1/"
    out, _ = capsys.readouterr()

    assert "Document Successfully Loaded!" in out


def test_quickstart_sample_batch_process_operation(
    capsys: pytest.CaptureFixture,
) -> None:
    client = documentai.DocumentProcessorServiceClient()
    name = f"{client.common_location_path(project=project_id, location=location)}/operations"
    response = client.list_operations(
        request=ListOperationsRequest(
            name=name,
            filter="TYPE=BATCH_PROCESS_DOCUMENTS AND STATE=DONE",
            page_size=1,
        )
    )
    batch_process_operation = response.operations[0].name

    quickstart_sample.quickstart_sample(batch_process_operation=batch_process_operation)

    out, _ = capsys.readouterr()

    assert "Document Successfully Loaded!" in out


def test_quickstart_sample_no_input() -> None:
    with pytest.raises(ValueError, match="No document source provided."):
        quickstart_sample.quickstart_sample()
