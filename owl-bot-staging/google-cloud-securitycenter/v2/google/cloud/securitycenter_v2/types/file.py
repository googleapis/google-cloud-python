# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
from __future__ import annotations

from typing import MutableMapping, MutableSequence

import proto  # type: ignore


__protobuf__ = proto.module(
    package='google.cloud.securitycenter.v2',
    manifest={
        'File',
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
            Prefix of the file contents as a JSON-encoded
            string.
        disk_path (google.cloud.securitycenter_v2.types.File.DiskPath):
            Path of the file in terms of underlying
            disk/partition identifiers.
    """

    class DiskPath(proto.Message):
        r"""Path of the file in terms of underlying disk/partition
        identifiers.

        Attributes:
            partition_uuid (str):
                UUID of the partition (format
                https://wiki.archlinux.org/title/persistent_block_device_naming#by-uuid)
            relative_path (str):
                Relative path of the file in the partition as a JSON encoded
                string. Example: /home/user1/executable_file.sh
        """

        partition_uuid: str = proto.Field(
            proto.STRING,
            number=1,
        )
        relative_path: str = proto.Field(
            proto.STRING,
            number=2,
        )

    path: str = proto.Field(
        proto.STRING,
        number=1,
    )
    size: int = proto.Field(
        proto.INT64,
        number=2,
    )
    sha256: str = proto.Field(
        proto.STRING,
        number=3,
    )
    hashed_size: int = proto.Field(
        proto.INT64,
        number=4,
    )
    partially_hashed: bool = proto.Field(
        proto.BOOL,
        number=5,
    )
    contents: str = proto.Field(
        proto.STRING,
        number=6,
    )
    disk_path: DiskPath = proto.Field(
        proto.MESSAGE,
        number=7,
        message=DiskPath,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
