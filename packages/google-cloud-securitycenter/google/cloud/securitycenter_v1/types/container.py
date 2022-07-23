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

from google.cloud.securitycenter_v1.types import label

__protobuf__ = proto.module(
    package="google.cloud.securitycenter.v1",
    manifest={
        "Container",
    },
)


class Container(proto.Message):
    r"""Container associated with the finding.

    Attributes:
        name (str):
            Container name.
        uri (str):
            Container image URI provided when configuring
            a pod/container. May identify a container image
            version using mutable tags.
        image_id (str):
            Optional container image id, when provided by
            the container runtime. Uniquely identifies the
            container image launched using a container image
            digest.
        labels (Sequence[google.cloud.securitycenter_v1.types.Label]):
            Container labels, as provided by the
            container runtime.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    uri = proto.Field(
        proto.STRING,
        number=2,
    )
    image_id = proto.Field(
        proto.STRING,
        number=3,
    )
    labels = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message=label.Label,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
