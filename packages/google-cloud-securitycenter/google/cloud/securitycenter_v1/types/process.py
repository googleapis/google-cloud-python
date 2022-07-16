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

from google.cloud.securitycenter_v1.types import file

__protobuf__ = proto.module(
    package="google.cloud.securitycenter.v1",
    manifest={
        "Process",
        "EnvironmentVariable",
    },
)


class Process(proto.Message):
    r"""Represents an operating system process.

    Attributes:
        name (str):
            The process name visible in utilities like ``top`` and
            ``ps``; it can be accessed via ``/proc/[pid]/comm`` and
            changed with ``prctl(PR_SET_NAME)``.
        binary (google.cloud.securitycenter_v1.types.File):
            File information for the process executable.
        libraries (Sequence[google.cloud.securitycenter_v1.types.File]):
            File information for libraries loaded by the
            process.
        script (google.cloud.securitycenter_v1.types.File):
            When the process represents the invocation of a script,
            ``binary`` provides information about the interpreter while
            ``script`` provides information about the script file
            provided to the interpreter.
        args (Sequence[str]):
            Process arguments as JSON encoded strings.
        arguments_truncated (bool):
            True if ``args`` is incomplete.
        env_variables (Sequence[google.cloud.securitycenter_v1.types.EnvironmentVariable]):
            Process environment variables.
        env_variables_truncated (bool):
            True if ``env_variables`` is incomplete.
        pid (int):
            The process id.
        parent_pid (int):
            The parent process id.
    """

    name = proto.Field(
        proto.STRING,
        number=12,
    )
    binary = proto.Field(
        proto.MESSAGE,
        number=3,
        message=file.File,
    )
    libraries = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message=file.File,
    )
    script = proto.Field(
        proto.MESSAGE,
        number=5,
        message=file.File,
    )
    args = proto.RepeatedField(
        proto.STRING,
        number=6,
    )
    arguments_truncated = proto.Field(
        proto.BOOL,
        number=7,
    )
    env_variables = proto.RepeatedField(
        proto.MESSAGE,
        number=8,
        message="EnvironmentVariable",
    )
    env_variables_truncated = proto.Field(
        proto.BOOL,
        number=9,
    )
    pid = proto.Field(
        proto.INT64,
        number=10,
    )
    parent_pid = proto.Field(
        proto.INT64,
        number=11,
    )


class EnvironmentVariable(proto.Message):
    r"""EnvironmentVariable is a name-value pair to store environment
    variables for Process.

    Attributes:
        name (str):
            Environment variable name as a JSON encoded
            string.
        val (str):
            Environment variable value as a JSON encoded
            string.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    val = proto.Field(
        proto.STRING,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
