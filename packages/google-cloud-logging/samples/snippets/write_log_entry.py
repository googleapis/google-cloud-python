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

import sys

from google.api import monitored_resource_pb2
from google.cloud.logging_v2.services.logging_service_v2 import LoggingServiceV2Client
from google.cloud.logging_v2.types import LogEntry
from google.cloud.logging_v2.types import WriteLogEntriesRequest
from google.logging.type import log_severity_pb2


# [START logging_write_log_entry]
def write_log_entry(project_id: str) -> None:
    """Writes text and structured log entries to Cloud Logging."""

    client = LoggingServiceV2Client()
    log_name = f"projects/{project_id}/logs/python-example-log"
    resource = monitored_resource_pb2.MonitoredResource(type="global")
    labels = {"sample": "write-log-entry"}

    text_entry = LogEntry(
        log_name=log_name,
        resource=resource,
        severity=log_severity_pb2.INFO,
        labels=labels,
        text_payload="Text log entry written from Python.",
    )

    struct_entry = LogEntry(
        log_name=log_name,
        resource=resource,
        severity=log_severity_pb2.WARNING,
        labels=labels,
        json_payload={
            "message": "Structured log entry written from Python.",
            "component": "sample",
        },
    )

    client.write_log_entries(
        request=WriteLogEntriesRequest(
            entries=[text_entry],
        )
    )
    print("Wrote one text log entry.")

    client.write_log_entries(
        request=WriteLogEntriesRequest(
            entries=[text_entry, struct_entry],
        )
    )
    print("Wrote a batch of text and structured log entries.")


# [END logging_write_log_entry]


if __name__ == "__main__":
    write_log_entry(project_id=sys.argv[1])
