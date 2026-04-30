# Copyright 2026 Google LLC
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

from unittest import mock

from google.logging.type import log_severity_pb2

import write_log_entry


def test_write_log_entry(capsys):
    project_id = "my-project"

    with mock.patch.object(write_log_entry, "LoggingServiceV2Client") as client:
        write_log_entry.write_log_entry(project_id)

    logging_client = client.return_value
    assert logging_client.write_log_entries.call_count == 2

    single_request = logging_client.write_log_entries.call_args_list[0].kwargs["request"]
    assert len(single_request.entries) == 1

    text_entry = single_request.entries[0]
    assert text_entry.log_name == f"projects/{project_id}/logs/python-example-log"
    assert text_entry.resource.type == "global"
    assert text_entry.severity == log_severity_pb2.INFO
    assert text_entry.labels["sample"] == "write-log-entry"
    assert text_entry.text_payload == "Text log entry written from Python."

    batch_request = logging_client.write_log_entries.call_args_list[1].kwargs["request"]
    assert len(batch_request.entries) == 2
    assert batch_request.entries[0].text_payload == text_entry.text_payload

    struct_entry = batch_request.entries[1]
    assert struct_entry.resource.type == "global"
    assert struct_entry.severity == log_severity_pb2.WARNING
    assert struct_entry.labels["sample"] == "write-log-entry"
    assert (
        struct_entry.json_payload["message"]
        == "Structured log entry written from Python."
    )
    assert struct_entry.json_payload["component"] == "sample"

    out, _ = capsys.readouterr()
    assert "Wrote one text log entry." in out
    assert "Wrote a batch of text and structured log entries." in out
