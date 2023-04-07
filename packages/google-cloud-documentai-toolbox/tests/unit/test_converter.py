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

try:
    from unittest import mock
except ImportError:  # pragma: NO COVER
    import mock

from google.cloud.documentai_toolbox.converters import converter


@mock.patch("google.cloud.documentai_toolbox.utilities.gcs_utilities.storage")
@mock.patch(
    "google.cloud.documentai_toolbox.converters.config.converter_helpers._get_docproto_files",
    return_value=(["file1"], ["test_label"], []),
)
@mock.patch(
    "google.cloud.documentai_toolbox.converters.config.converter_helpers._upload",
    return_value="Done",
)
def test__convert_documents_with_config(
    mock_storage, mock_get_docproto_files, mock_upload, capfd
):
    client = mock_storage.Client.return_value
    mock_bucket = mock.Mock()
    client.Bucket.return_value = mock_bucket

    mock_blob1 = mock.Mock(name="gs://test-directory/1/test-annotations.json")
    mock_blob1.download_as_bytes.return_value = (
        "gs://test-directory/1/test-annotations.json"
    )

    mock_blob2 = mock.Mock(name="gs://test-directory/1/test-config.json")
    mock_blob2.download_as_bytes.return_value = "gs://test-directory/1/test-config.json"

    mock_blob3 = mock.Mock(name="gs://test-directory/1/test.pdf")
    mock_blob3.download_as_bytes.return_value = "gs://test-directory/1/test.pdf"

    client.list_blobs.return_value = [mock_blob1, mock_blob2, mock_blob3]

    converter.convert_from_config(
        project_id="project-id",
        location="location",
        processor_id="project-id",
        gcs_input_path="gs://test-directory/1",
        gcs_output_path="gs://test-directory/1/output",
    )

    out, err = capfd.readouterr()
    assert "test_label" in out
