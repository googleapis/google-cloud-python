# -*- coding: utf-8 -*-
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
#
# Generated code. DO NOT EDIT!
#
# Snippet for UploadMedia
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-showcase


# [START localhost_v1beta1_generated_ResumableUploadService_UploadMedia_sync]
# This snippet has been automatically generated and should be regarded as a
# code template only.
# It will require modifications to work:
# - It may require correct/in-range values for request initialization.
# - It may require specifying regional endpoints when creating the service
#   client as shown in:
#   https://googleapis.dev/python/google-api-core/latest/client_options.html
from google import showcase_v1beta1
from google.api_core.resumable_transfer import ResumableUploadConfig
import io


def sample_upload_media():
    # Option 1: Upload a stream directly from start to completion.
    # Create a client
    client = showcase_v1beta1.ResumableUploadServiceClient()

    # Initialize request argument(s)
    request = showcase_v1beta1.UploadMediaRequest(
    )

    # Configure optional transfer settings such as chunk size and stall detection
    config = ResumableUploadConfig(
        chunk_size=8 * 1024 * 1024,  # 8 MB
        stall_minimum_rate=64 * 1024,
        stall_timeout=120,
    )

    # Create an upload session for the request
    upload_session = client.upload_media(request=request, config=config)

    # Upload the entire stream directly and return the final response
    stream = io.BytesIO(b"Example upload data")
    response = upload_session.upload(stream)

    # Handle the response
    print(response)


def sample_upload_media_with_progress():
    # Option 2: Upload a stream while receiving progress updates per chunk.
    # Create a client
    client = showcase_v1beta1.ResumableUploadServiceClient()

    # Initialize request argument(s)
    request = showcase_v1beta1.UploadMediaRequest(
    )

    # Configure optional transfer settings such as chunk size and stall detection
    config = ResumableUploadConfig(
        chunk_size=8 * 1024 * 1024,  # 8 MB
        stall_minimum_rate=64 * 1024,
        stall_timeout=120,
    )

    # Create an upload session for the request
    upload_session = client.upload_media(request=request, config=config)

    # Iterate over the upload to receive progress updates as each chunk is transmitted
    stream = io.BytesIO(b"Example upload data")
    for progress in upload_session.iter_upload(stream):
        print(
            f"Uploaded {progress.bytes_uploaded} bytes | State: {progress.state.name}"
        )
        print(f"Session URL: {progress.upload_url}")

    # After iteration completes, the final response is available on the session
    response = upload_session.response

    # Handle the response
    print(response)


def sample_upload_media_resume():
    # Option 3: Resume an interrupted upload using a previously saved session URL.
    # Create a client
    client = showcase_v1beta1.ResumableUploadServiceClient()

    # Initialize request argument(s)
    request = showcase_v1beta1.UploadMediaRequest(
    )

    # Create an upload session for the request
    upload_session = client.upload_media(request=request)

    # Resume the interrupted upload from the saved session URL and chunk size
    stream = io.BytesIO(b"Example upload data")
    upload_url = "https://..."
    chunk_size = 8 * 1024 * 1024
    response = upload_session.resume(upload_url, stream, chunk_size=chunk_size)

    # Handle the response
    print(response)


def sample_upload_media_resume_with_progress():
    # Option 4: Resume an interrupted upload while receiving progress updates.
    # Create a client
    client = showcase_v1beta1.ResumableUploadServiceClient()

    # Initialize request argument(s)
    request = showcase_v1beta1.UploadMediaRequest(
    )

    # Create an upload session for the request
    upload_session = client.upload_media(request=request)

    # Resume the interrupted upload while iterating over progress updates
    stream = io.BytesIO(b"Example upload data")
    upload_url = "https://..."
    chunk_size = 8 * 1024 * 1024
    for progress in upload_session.iter_resume(upload_url, stream, chunk_size=chunk_size):
        print(
            f"Resumed {progress.bytes_uploaded} bytes | State: {progress.state.name}"
        )
        print(f"Session URL: {progress.upload_url}")
        print(f"Chunk size: {progress.chunk_size}")

    # After iteration completes, the final response is available on the session
    response = upload_session.response

    # Handle the response
    print(response)


# [END localhost_v1beta1_generated_ResumableUploadService_UploadMedia_sync]
