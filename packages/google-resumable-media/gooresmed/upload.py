# Copyright 2017 Google Inc.
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

"""Support for resumable uploads.

Also supported here are simple (media) uploads and multipart
uploads that contain both metadata and a small file as payload.
"""


class Upload(object):
    """Helper to manage uploading some a resource to a Google API.

    Basic support will

    * upload directly from a file on the host OS
    * upload from a stream or file-like object
    * upload content directly from a string or bytes

    For large files / content, the upload process will need to be
    split into smaller chunks as a resumable upload.
    """

    def __init__(self):
        self.total_bytes = None
        """Optional[int]: The total number of bytes to be uploaded."""
        self.bytes_transmitted = 0
        """int: The number of bytes that have been transmitted."""
        self.chunk_size = None
        """Optional[int]: The maximum size (in bytes) of a request."""

    def transmit(self):
        """Transmit the resource to be uploaded."""
        raise NotImplementedError

    def transmit_chunk(self):
        """Transmit a single chunk of the resource to be uploaded."""
        raise NotImplementedError
