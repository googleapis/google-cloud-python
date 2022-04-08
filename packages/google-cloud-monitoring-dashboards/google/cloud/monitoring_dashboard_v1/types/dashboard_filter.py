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
    package="google.monitoring.dashboard.v1",
    manifest={
        "DashboardFilter",
    },
)


class DashboardFilter(proto.Message):
    r"""A filter to reduce the amount of data charted in relevant
    widgets.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        label_key (str):
            Required. The key for the label
        template_variable (str):
            The placeholder text that can be referenced
            in a filter string or MQL query. If omitted, the
            dashboard filter will be applied to all relevant
            widgets in the dashboard.
        string_value (str):
            A variable-length string value.

            This field is a member of `oneof`_ ``default_value``.
        filter_type (google.cloud.monitoring_dashboard_v1.types.DashboardFilter.FilterType):
            The specified filter type
    """

    class FilterType(proto.Enum):
        r"""The type for the dashboard filter"""
        FILTER_TYPE_UNSPECIFIED = 0
        RESOURCE_LABEL = 1
        METRIC_LABEL = 2
        USER_METADATA_LABEL = 3
        SYSTEM_METADATA_LABEL = 4
        GROUP = 5

    label_key = proto.Field(
        proto.STRING,
        number=1,
    )
    template_variable = proto.Field(
        proto.STRING,
        number=3,
    )
    string_value = proto.Field(
        proto.STRING,
        number=4,
        oneof="default_value",
    )
    filter_type = proto.Field(
        proto.ENUM,
        number=5,
        enum=FilterType,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
