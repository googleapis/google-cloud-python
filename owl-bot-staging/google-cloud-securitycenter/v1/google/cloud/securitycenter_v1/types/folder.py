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
    package='google.cloud.securitycenter.v1',
    manifest={
        'Folder',
    },
)


class Folder(proto.Message):
    r"""Message that contains the resource name and display name of a
    folder resource.

    Attributes:
        resource_folder (str):
            Full resource name of this folder. See:
            https://cloud.google.com/apis/design/resource_names#full_resource_name
        resource_folder_display_name (str):
            The user defined display name for this
            folder.
    """

    resource_folder: str = proto.Field(
        proto.STRING,
        number=1,
    )
    resource_folder_display_name: str = proto.Field(
        proto.STRING,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
