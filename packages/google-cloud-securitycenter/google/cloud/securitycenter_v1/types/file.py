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
#
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.securitycenter.v1",
    manifest={
        "File",
    },
)


class File(proto.Message):
    r"""File information about the related binary/library used by an
    executable, or the script used by a script interpreter

    Attributes:
        path (str):
            Absolute path of the file as a JSON encoded
            string.
        size (int):
            Size of the file in bytes.
        sha256 (str):
            SHA256 hash of the first hashed_size bytes of the file
            encoded as a hex string. If hashed_size == size, sha256
            represents the SHA256 hash of the entire file.
        hashed_size (int):
            The length in bytes of the file prefix that was hashed. If
            hashed_size == size, any hashes reported represent the
            entire file.
        partially_hashed (bool):
            True when the hash covers only a prefix of
            the file.
        contents (str):
            Prefix of the file contents as a JSON encoded
            string. (Currently only populated for Malicious
            Script Executed findings.)
    """

    path = proto.Field(
        proto.STRING,
        number=1,
    )
    size = proto.Field(
        proto.INT64,
        number=2,
    )
    sha256 = proto.Field(
        proto.STRING,
        number=3,
    )
    hashed_size = proto.Field(
        proto.INT64,
        number=4,
    )
    partially_hashed = proto.Field(
        proto.BOOL,
        number=5,
    )
    contents = proto.Field(
        proto.STRING,
        number=6,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
