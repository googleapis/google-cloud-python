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
    package="google.cloud.alloydb.v1beta",
    manifest={
        "CloudSQLBackupRunSource",
    },
)


class CloudSQLBackupRunSource(proto.Message):
    r"""The source CloudSQL backup resource.

    Attributes:
        project (str):
            The project ID of the source CloudSQL
            instance. This should be the same as the AlloyDB
            cluster's project.
        instance_id (str):
            Required. The CloudSQL instance ID.
        backup_run_id (int):
            Required. The CloudSQL backup run ID.
    """

    project: str = proto.Field(
        proto.STRING,
        number=1,
    )
    instance_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    backup_run_id: int = proto.Field(
        proto.INT64,
        number=3,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
