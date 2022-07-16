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
        "Compliance",
    },
)


class Compliance(proto.Message):
    r"""Contains compliance information about a security standard
    indicating unmet recommendations.

    Attributes:
        standard (str):
            Refers to industry wide standards or
            benchmarks e.g. "cis", "pci", "owasp", etc.
        version (str):
            Version of the standard/benchmark e.g. 1.1
        ids (Sequence[str]):
            Policies within the standard/benchmark e.g.
            A.12.4.1
    """

    standard = proto.Field(
        proto.STRING,
        number=1,
    )
    version = proto.Field(
        proto.STRING,
        number=2,
    )
    ids = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
