# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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

from google.cloud.geminidataanalytics_v1alpha.types import datasource

__protobuf__ = proto.module(
    package="google.cloud.geminidataanalytics.v1alpha",
    manifest={
        "Context",
        "ConversationOptions",
        "ChartOptions",
        "AnalysisOptions",
    },
)


class Context(proto.Message):
    r"""A collection of context to apply to this conversation

    Attributes:
        system_instruction (str):
            Optional. The basic entry point for data
            owners creating domain knowledge for Agent.

            Why: Business jargon (e.g., YTD revenue is
            calculated as…, Retirement Age is 65 in the USA,
            etc) and system instructions (e.g., answer like
            a Pirate) can help the model understand the
            business context around a user question.
        datasource_references (google.cloud.geminidataanalytics_v1alpha.types.DatasourceReferences):
            Required. Datasources available for answering
            the question.
        options (google.cloud.geminidataanalytics_v1alpha.types.ConversationOptions):
            Optional. Additional options for the
            conversation.
    """

    system_instruction: str = proto.Field(
        proto.STRING,
        number=1,
    )
    datasource_references: datasource.DatasourceReferences = proto.Field(
        proto.MESSAGE,
        number=7,
        message=datasource.DatasourceReferences,
    )
    options: "ConversationOptions" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="ConversationOptions",
    )


class ConversationOptions(proto.Message):
    r"""Options for the conversation.

    Attributes:
        chart (google.cloud.geminidataanalytics_v1alpha.types.ChartOptions):
            Optional. Options for chart generation.
        analysis (google.cloud.geminidataanalytics_v1alpha.types.AnalysisOptions):
            Optional. Options for analysis.
    """

    chart: "ChartOptions" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="ChartOptions",
    )
    analysis: "AnalysisOptions" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="AnalysisOptions",
    )


class ChartOptions(proto.Message):
    r"""Options for chart generation.

    Attributes:
        image (google.cloud.geminidataanalytics_v1alpha.types.ChartOptions.ImageOptions):
            Optional. When specified, the agent will
            render generated charts using the provided
            format. Defaults to no image.
    """

    class ImageOptions(proto.Message):
        r"""Options for rendering images of generated charts.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            no_image (google.cloud.geminidataanalytics_v1alpha.types.ChartOptions.ImageOptions.NoImage):
                No image.

                This field is a member of `oneof`_ ``kind``.
            svg (google.cloud.geminidataanalytics_v1alpha.types.ChartOptions.ImageOptions.SvgOptions):
                SVG format.

                This field is a member of `oneof`_ ``kind``.
        """

        class NoImage(proto.Message):
            r"""No image."""

        class SvgOptions(proto.Message):
            r"""SVG options."""

        no_image: "ChartOptions.ImageOptions.NoImage" = proto.Field(
            proto.MESSAGE,
            number=1,
            oneof="kind",
            message="ChartOptions.ImageOptions.NoImage",
        )
        svg: "ChartOptions.ImageOptions.SvgOptions" = proto.Field(
            proto.MESSAGE,
            number=2,
            oneof="kind",
            message="ChartOptions.ImageOptions.SvgOptions",
        )

    image: ImageOptions = proto.Field(
        proto.MESSAGE,
        number=1,
        message=ImageOptions,
    )


class AnalysisOptions(proto.Message):
    r"""Options for analysis.

    Attributes:
        python (google.cloud.geminidataanalytics_v1alpha.types.AnalysisOptions.Python):
            Optional. Options for Python analysis.
    """

    class Python(proto.Message):
        r"""Options for Python analysis.

        Attributes:
            enabled (bool):
                Optional. Whether to enable Python analysis.
                Defaults to false.
        """

        enabled: bool = proto.Field(
            proto.BOOL,
            number=1,
        )

    python: Python = proto.Field(
        proto.MESSAGE,
        number=1,
        message=Python,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
