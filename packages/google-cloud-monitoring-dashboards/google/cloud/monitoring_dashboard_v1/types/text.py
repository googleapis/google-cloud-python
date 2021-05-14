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
    package="google.monitoring.dashboard.v1", manifest={"Text",},
)


class Text(proto.Message):
    r"""A widget that displays textual content.
    Attributes:
        content (str):
            The text content to be displayed.
        format_ (google.cloud.monitoring_dashboard_v1.types.Text.Format):
            How the text content is formatted.
    """

    class Format(proto.Enum):
        r"""The format type of the text content."""
        FORMAT_UNSPECIFIED = 0
        MARKDOWN = 1
        RAW = 2

    content = proto.Field(proto.STRING, number=1,)
    format_ = proto.Field(proto.ENUM, number=2, enum=Format,)


__all__ = tuple(sorted(__protobuf__.manifest))
