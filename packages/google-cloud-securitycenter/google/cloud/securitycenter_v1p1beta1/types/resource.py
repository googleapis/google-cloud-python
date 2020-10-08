# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
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
    package="google.cloud.securitycenter.v1p1beta1", manifest={"Resource",},
)


class Resource(proto.Message):
    r"""Information related to the Google Cloud resource.

    Attributes:
        name (str):
            The full resource name of the resource. See:
            https://cloud.google.com/apis/design/resource_names#full_resource_name
        project (str):
            The full resource name of project that the
            resource belongs to.
        project_display_name (str):
            The human readable name of project that the
            resource belongs to.
        parent (str):
            The full resource name of resource's parent.
        parent_display_name (str):
            The human readable name of resource's parent.
    """

    name = proto.Field(proto.STRING, number=1)

    project = proto.Field(proto.STRING, number=2)

    project_display_name = proto.Field(proto.STRING, number=3)

    parent = proto.Field(proto.STRING, number=4)

    parent_display_name = proto.Field(proto.STRING, number=5)


__all__ = tuple(sorted(__protobuf__.manifest))
