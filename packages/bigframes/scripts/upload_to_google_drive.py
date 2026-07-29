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

"""
Upload latest wheel to Google Drive.

Based on
https://github.com/googleapis/google-resumable-media-python/blob/main/google/resumable_media/requests/__init__.py

Before running, execute the following to make sure you can use the Google Drive API:

gcloud auth application-default login --scopes=openid,https://www.googleapis.com/auth/userinfo.email,https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/sqlservice.login,https://www.googleapis.com/auth/drive
"""

import pathlib

import google.auth
import google.auth.transport.requests
import google.resumable_media._upload
import google.resumable_media.requests as resumable_requests

repo_root = pathlib.Path(__file__).parent.parent

# Use PATCH instead of POST to replace existing files.
google.resumable_media._upload._POST = "PATCH"

credentials, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/drive"])
transport = google.auth.transport.requests.AuthorizedSession(credentials)

wheel_id = "15fZ1DkrFDk4ibMNTzms4akpxmf2pzeAR"
wheel_path = next(iter((repo_root / "dist").glob("bigframes-*.whl")))

uploads = (
    (wheel_id, wheel_path, "application/octet-stream"),
    # (pdf_id, pdf_path, "application/pdf"),
)

upload_template = (
    "https://www.googleapis.com/upload/drive/v3/files/{file_id}?uploadType=resumable"
)
chunk_size = 1024 * 1024  # 1MB

for file_id, file_path, content_type in uploads:
    print(f"Uploading {file_path}")
    transport = google.auth.transport.requests.AuthorizedSession(credentials)
    upload = resumable_requests.ResumableUpload(
        upload_template.format(file_id=file_id), chunk_size
    )

    with open(file_path, "rb") as stream:
        response = upload.initiate(
            transport, stream, metadata={}, content_type=content_type
        )
        print(response)
        while not upload.finished:
            response = upload.transmit_next_chunk(transport)
            print(response)
