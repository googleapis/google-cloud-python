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


from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
from google.protobuf import struct_pb2 as struct  # type: ignore


__protobuf__ = proto.module(
    package="google.area120.tables.v1alpha1",
    manifest={
        "View",
        "GetTableRequest",
        "ListTablesRequest",
        "ListTablesResponse",
        "GetRowRequest",
        "ListRowsRequest",
        "ListRowsResponse",
        "CreateRowRequest",
        "BatchCreateRowsRequest",
        "BatchCreateRowsResponse",
        "UpdateRowRequest",
        "BatchUpdateRowsRequest",
        "BatchUpdateRowsResponse",
        "DeleteRowRequest",
        "Table",
        "ColumnDescription",
        "Row",
    },
)


class View(proto.Enum):
    r"""Column identifier used for the values in the row."""
    VIEW_UNSPECIFIED = 0
    COLUMN_ID_VIEW = 1


class GetTableRequest(proto.Message):
    r"""Request message for TablesService.GetTable.

    Attributes:
        name (str):
            Required. The name of the table to retrieve.
            Format: tables/{table}
    """

    name = proto.Field(proto.STRING, number=1)


class ListTablesRequest(proto.Message):
    r"""Request message for TablesService.ListTables.

    Attributes:
        page_size (int):
            The maximum number of tables to return. The
            service may return fewer than this value.

            If unspecified, at most 20 tables are returned.
            The maximum value is 100; values above 100 are
            coerced to 100.
        page_token (str):
            A page token, received from a previous ``ListTables`` call.
            Provide this to retrieve the subsequent page.

            When paginating, all other parameters provided to
            ``ListTables`` must match the call that provided the page
            token.
    """

    page_size = proto.Field(proto.INT32, number=1)

    page_token = proto.Field(proto.STRING, number=2)


class ListTablesResponse(proto.Message):
    r"""Response message for TablesService.ListTables.

    Attributes:
        tables (Sequence[~.gat_tables.Table]):
            The list of tables.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is empty, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    tables = proto.RepeatedField(proto.MESSAGE, number=1, message="Table",)

    next_page_token = proto.Field(proto.STRING, number=2)


class GetRowRequest(proto.Message):
    r"""Request message for TablesService.GetRow.

    Attributes:
        name (str):
            Required. The name of the row to retrieve.
            Format: tables/{table}/rows/{row}
        view (~.gat_tables.View):
            Optional. Column key to use for values in the
            row. Defaults to user entered name.
    """

    name = proto.Field(proto.STRING, number=1)

    view = proto.Field(proto.ENUM, number=2, enum="View",)


class ListRowsRequest(proto.Message):
    r"""Request message for TablesService.ListRows.

    Attributes:
        parent (str):
            Required. The parent table.
            Format: tables/{table}
        page_size (int):
            The maximum number of rows to return. The
            service may return fewer than this value.

            If unspecified, at most 50 rows are returned.
            The maximum value is 1,000; values above 1,000
            are coerced to 1,000.
        page_token (str):
            A page token, received from a previous ``ListRows`` call.
            Provide this to retrieve the subsequent page.

            When paginating, all other parameters provided to
            ``ListRows`` must match the call that provided the page
            token.
        view (~.gat_tables.View):
            Optional. Column key to use for values in the
            row. Defaults to user entered name.
    """

    parent = proto.Field(proto.STRING, number=1)

    page_size = proto.Field(proto.INT32, number=2)

    page_token = proto.Field(proto.STRING, number=3)

    view = proto.Field(proto.ENUM, number=4, enum="View",)


class ListRowsResponse(proto.Message):
    r"""Response message for TablesService.ListRows.

    Attributes:
        rows (Sequence[~.gat_tables.Row]):
            The rows from the specified table.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is empty, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    rows = proto.RepeatedField(proto.MESSAGE, number=1, message="Row",)

    next_page_token = proto.Field(proto.STRING, number=2)


class CreateRowRequest(proto.Message):
    r"""Request message for TablesService.CreateRow.

    Attributes:
        parent (str):
            Required. The parent table where this row
            will be created. Format: tables/{table}
        row (~.gat_tables.Row):
            Required. The row to create.
        view (~.gat_tables.View):
            Optional. Column key to use for values in the
            row. Defaults to user entered name.
    """

    parent = proto.Field(proto.STRING, number=1)

    row = proto.Field(proto.MESSAGE, number=2, message="Row",)

    view = proto.Field(proto.ENUM, number=3, enum="View",)


class BatchCreateRowsRequest(proto.Message):
    r"""Request message for TablesService.BatchCreateRows.

    Attributes:
        parent (str):
            Required. The parent table where the rows
            will be created. Format: tables/{table}
        requests (Sequence[~.gat_tables.CreateRowRequest]):
            Required. The request message specifying the
            rows to create.
            A maximum of 500 rows can be created in a single
            batch.
    """

    parent = proto.Field(proto.STRING, number=1)

    requests = proto.RepeatedField(proto.MESSAGE, number=2, message="CreateRowRequest",)


class BatchCreateRowsResponse(proto.Message):
    r"""Response message for TablesService.BatchCreateRows.

    Attributes:
        rows (Sequence[~.gat_tables.Row]):
            The created rows.
    """

    rows = proto.RepeatedField(proto.MESSAGE, number=1, message="Row",)


class UpdateRowRequest(proto.Message):
    r"""Request message for TablesService.UpdateRow.

    Attributes:
        row (~.gat_tables.Row):
            Required. The row to update.
        update_mask (~.field_mask.FieldMask):
            The list of fields to update.
        view (~.gat_tables.View):
            Optional. Column key to use for values in the
            row. Defaults to user entered name.
    """

    row = proto.Field(proto.MESSAGE, number=1, message="Row",)

    update_mask = proto.Field(proto.MESSAGE, number=2, message=field_mask.FieldMask,)

    view = proto.Field(proto.ENUM, number=3, enum="View",)


class BatchUpdateRowsRequest(proto.Message):
    r"""Request message for TablesService.BatchUpdateRows.

    Attributes:
        parent (str):
            Required. The parent table shared by all rows
            being updated. Format: tables/{table}
        requests (Sequence[~.gat_tables.UpdateRowRequest]):
            Required. The request messages specifying the
            rows to update.
            A maximum of 500 rows can be modified in a
            single batch.
    """

    parent = proto.Field(proto.STRING, number=1)

    requests = proto.RepeatedField(proto.MESSAGE, number=2, message="UpdateRowRequest",)


class BatchUpdateRowsResponse(proto.Message):
    r"""Response message for TablesService.BatchUpdateRows.

    Attributes:
        rows (Sequence[~.gat_tables.Row]):
            The updated rows.
    """

    rows = proto.RepeatedField(proto.MESSAGE, number=1, message="Row",)


class DeleteRowRequest(proto.Message):
    r"""Request message for TablesService.DeleteRow

    Attributes:
        name (str):
            Required. The name of the row to delete.
            Format: tables/{table}/rows/{row}
    """

    name = proto.Field(proto.STRING, number=1)


class Table(proto.Message):
    r"""A single table.

    Attributes:
        name (str):
            The resource name of the table. Table names have the form
            ``tables/{table}``.
        display_name (str):
            The human readable title of the table.
        columns (Sequence[~.gat_tables.ColumnDescription]):
            List of columns in this table.
            Order of columns matches the display order.
    """

    name = proto.Field(proto.STRING, number=1)

    display_name = proto.Field(proto.STRING, number=2)

    columns = proto.RepeatedField(proto.MESSAGE, number=3, message="ColumnDescription",)


class ColumnDescription(proto.Message):
    r"""Details on a column in the table.

    Attributes:
        name (str):
            column name
        data_type (str):
            Data type of the column Supported types are number, text,
            boolean, number_list, text_list, boolean_list.
        id (str):
            Internal id for a column.
    """

    name = proto.Field(proto.STRING, number=1)

    data_type = proto.Field(proto.STRING, number=2)

    id = proto.Field(proto.STRING, number=3)


class Row(proto.Message):
    r"""A single row in a table.

    Attributes:
        name (str):
            The resource name of the row. Row names have the form
            ``tables/{table}/rows/{row}``. The name is ignored when
            creating a row.
        values (Sequence[~.gat_tables.Row.ValuesEntry]):
            The values of the row. This is a map of
            column key to value. Key is user entered
            name(default) or the internal column id based on
            the view in the request.
    """

    name = proto.Field(proto.STRING, number=1)

    values = proto.MapField(
        proto.STRING, proto.MESSAGE, number=2, message=struct.Value,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
