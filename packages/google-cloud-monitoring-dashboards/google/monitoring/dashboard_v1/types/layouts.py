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


from google.monitoring.dashboard_v1.types import widget


__protobuf__ = proto.module(
    package="google.monitoring.dashboard.v1",
    manifest={"GridLayout", "RowLayout", "ColumnLayout",},
)


class GridLayout(proto.Message):
    r"""A basic layout divides the available space into vertical
    columns of equal width and arranges a list of widgets using a
    row-first strategy.

    Attributes:
        columns (int):
            The number of columns into which the view's
            width is divided. If omitted or set to zero, a
            system default will be used while rendering.
        widgets (Sequence[~.widget.Widget]):
            The informational elements that are arranged
            into the columns row-first.
    """

    columns = proto.Field(proto.INT64, number=1)

    widgets = proto.RepeatedField(proto.MESSAGE, number=2, message=widget.Widget,)


class RowLayout(proto.Message):
    r"""A simplified layout that divides the available space into
    rows and arranges a set of widgets horizontally in each row.

    Attributes:
        rows (Sequence[~.layouts.RowLayout.Row]):
            The rows of content to display.
    """

    class Row(proto.Message):
        r"""Defines the layout properties and content for a row.

        Attributes:
            weight (int):
                The relative weight of this row. The row
                weight is used to adjust the height of rows on
                the screen (relative to peers). Greater the
                weight, greater the height of the row on the
                screen. If omitted, a value of 1 is used while
                rendering.
            widgets (Sequence[~.widget.Widget]):
                The display widgets arranged horizontally in
                this row.
        """

        weight = proto.Field(proto.INT64, number=1)

        widgets = proto.RepeatedField(proto.MESSAGE, number=2, message=widget.Widget,)

    rows = proto.RepeatedField(proto.MESSAGE, number=1, message=Row,)


class ColumnLayout(proto.Message):
    r"""A simplified layout that divides the available space into
    vertical columns and arranges a set of widgets vertically in
    each column.

    Attributes:
        columns (Sequence[~.layouts.ColumnLayout.Column]):
            The columns of content to display.
    """

    class Column(proto.Message):
        r"""Defines the layout properties and content for a column.

        Attributes:
            weight (int):
                The relative weight of this column. The
                column weight is used to adjust the width of
                columns on the screen (relative to peers).
                Greater the weight, greater the width of the
                column on the screen. If omitted, a value of 1
                is used while rendering.
            widgets (Sequence[~.widget.Widget]):
                The display widgets arranged vertically in
                this column.
        """

        weight = proto.Field(proto.INT64, number=1)

        widgets = proto.RepeatedField(proto.MESSAGE, number=2, message=widget.Widget,)

    columns = proto.RepeatedField(proto.MESSAGE, number=1, message=Column,)


__all__ = tuple(sorted(__protobuf__.manifest))
