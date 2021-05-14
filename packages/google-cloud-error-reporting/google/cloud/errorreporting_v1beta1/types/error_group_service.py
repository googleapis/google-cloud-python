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

from google.cloud.errorreporting_v1beta1.types import common


__protobuf__ = proto.module(
    package="google.devtools.clouderrorreporting.v1beta1",
    manifest={"GetGroupRequest", "UpdateGroupRequest",},
)


class GetGroupRequest(proto.Message):
    r"""A request to return an individual group.
    Attributes:
        group_name (str):
            Required. The group resource name. Written as
            ``projects/{projectID}/groups/{group_name}``. Call
            ```groupStats.list`` <https://cloud.google.com/error-reporting/reference/rest/v1beta1/projects.groupStats/list>`__
            to return a list of groups belonging to this project.

            Example: ``projects/my-project-123/groups/my-group``
    """

    group_name = proto.Field(proto.STRING, number=1,)


class UpdateGroupRequest(proto.Message):
    r"""A request to replace the existing data for the given group.
    Attributes:
        group (google.cloud.errorreporting_v1beta1.types.ErrorGroup):
            Required. The group which replaces the
            resource on the server.
    """

    group = proto.Field(proto.MESSAGE, number=1, message=common.ErrorGroup,)


__all__ = tuple(sorted(__protobuf__.manifest))
