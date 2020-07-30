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


from google.monitoring.dashboard_v1.types import layouts


__protobuf__ = proto.module(
    package="google.monitoring.dashboard.v1", manifest={"Dashboard",},
)


class Dashboard(proto.Message):
    r"""A Google Stackdriver dashboard. Dashboards define the content
    and layout of pages in the Stackdriver web application.

    Attributes:
        name (str):
            Immutable. The resource name of the
            dashboard.
        display_name (str):
            Required. The mutable, human-readable name.
        etag (str):
            ``etag`` is used for optimistic concurrency control as a way
            to help prevent simultaneous updates of a policy from
            overwriting each other. An ``etag`` is returned in the
            response to ``GetDashboard``, and users are expected to put
            that etag in the request to ``UpdateDashboard`` to ensure
            that their change will be applied to the same version of the
            Dashboard configuration. The field should not be passed
            during dashboard creation.
        grid_layout (~.layouts.GridLayout):
            Content is arranged with a basic layout that
            re-flows a simple list of informational elements
            like widgets or tiles.
        row_layout (~.layouts.RowLayout):
            The content is divided into equally spaced
            rows and the widgets are arranged horizontally.
        column_layout (~.layouts.ColumnLayout):
            The content is divided into equally spaced
            columns and the widgets are arranged vertically.
    """

    name = proto.Field(proto.STRING, number=1)

    display_name = proto.Field(proto.STRING, number=2)

    etag = proto.Field(proto.STRING, number=4)

    grid_layout = proto.Field(
        proto.MESSAGE, number=5, oneof="layout", message=layouts.GridLayout,
    )

    row_layout = proto.Field(
        proto.MESSAGE, number=8, oneof="layout", message=layouts.RowLayout,
    )

    column_layout = proto.Field(
        proto.MESSAGE, number=9, oneof="layout", message=layouts.ColumnLayout,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
