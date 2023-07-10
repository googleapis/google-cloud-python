# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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

from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import struct_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.area120.tables.v1alpha1",
    manifest={
        "View",
        "GetTableRequest",
        "ListTablesRequest",
        "ListTablesResponse",
        "GetWorkspaceRequest",
        "ListWorkspacesRequest",
        "ListWorkspacesResponse",
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
        "BatchDeleteRowsRequest",
        "Table",
        "ColumnDescription",
        "LabeledItem",
        "RelationshipDetails",
        "LookupDetails",
        "Row",
        "Workspace",
    },
)


class View(proto.Enum):
    r"""Column identifier used for the values in the row.

    Values:
        VIEW_UNSPECIFIED (0):
            Defaults to user entered text.
        COLUMN_ID_VIEW (1):
            Uses internally generated column id to
            identify values.
    """
    VIEW_UNSPECIFIED = 0
    COLUMN_ID_VIEW = 1


class GetTableRequest(proto.Message):
    r"""Request message for TablesService.GetTable.

    Attributes:
        name (str):
            Required. The name of the table to retrieve.
            Format: tables/{table}
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


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

    page_size: int = proto.Field(
        proto.INT32,
        number=1,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ListTablesResponse(proto.Message):
    r"""Response message for TablesService.ListTables.

    Attributes:
        tables (MutableSequence[google.area120.tables_v1alpha1.types.Table]):
            The list of tables.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is empty, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    tables: MutableSequence["Table"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Table",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetWorkspaceRequest(proto.Message):
    r"""Request message for TablesService.GetWorkspace.

    Attributes:
        name (str):
            Required. The name of the workspace to
            retrieve. Format: workspaces/{workspace}
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListWorkspacesRequest(proto.Message):
    r"""Request message for TablesService.ListWorkspaces.

    Attributes:
        page_size (int):
            The maximum number of workspaces to return.
            The service may return fewer than this value.
            If unspecified, at most 10 workspaces are
            returned. The maximum value is 25; values above
            25 are coerced to 25.
        page_token (str):
            A page token, received from a previous ``ListWorkspaces``
            call. Provide this to retrieve the subsequent page.

            When paginating, all other parameters provided to
            ``ListWorkspaces`` must match the call that provided the
            page token.
    """

    page_size: int = proto.Field(
        proto.INT32,
        number=1,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ListWorkspacesResponse(proto.Message):
    r"""Response message for TablesService.ListWorkspaces.

    Attributes:
        workspaces (MutableSequence[google.area120.tables_v1alpha1.types.Workspace]):
            The list of workspaces.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is empty, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    workspaces: MutableSequence["Workspace"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Workspace",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetRowRequest(proto.Message):
    r"""Request message for TablesService.GetRow.

    Attributes:
        name (str):
            Required. The name of the row to retrieve.
            Format: tables/{table}/rows/{row}
        view (google.area120.tables_v1alpha1.types.View):
            Optional. Column key to use for values in the
            row. Defaults to user entered name.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    view: "View" = proto.Field(
        proto.ENUM,
        number=2,
        enum="View",
    )


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
        view (google.area120.tables_v1alpha1.types.View):
            Optional. Column key to use for values in the
            row. Defaults to user entered name.
        filter (str):
            Optional. Raw text query to search for in
            rows of the table. Special characters must be
            escaped. Logical operators and field specific
            filtering not supported.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )
    view: "View" = proto.Field(
        proto.ENUM,
        number=4,
        enum="View",
    )
    filter: str = proto.Field(
        proto.STRING,
        number=5,
    )


class ListRowsResponse(proto.Message):
    r"""Response message for TablesService.ListRows.

    Attributes:
        rows (MutableSequence[google.area120.tables_v1alpha1.types.Row]):
            The rows from the specified table.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is empty, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    rows: MutableSequence["Row"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Row",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class CreateRowRequest(proto.Message):
    r"""Request message for TablesService.CreateRow.

    Attributes:
        parent (str):
            Required. The parent table where this row
            will be created. Format: tables/{table}
        row (google.area120.tables_v1alpha1.types.Row):
            Required. The row to create.
        view (google.area120.tables_v1alpha1.types.View):
            Optional. Column key to use for values in the
            row. Defaults to user entered name.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    row: "Row" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Row",
    )
    view: "View" = proto.Field(
        proto.ENUM,
        number=3,
        enum="View",
    )


class BatchCreateRowsRequest(proto.Message):
    r"""Request message for TablesService.BatchCreateRows.

    Attributes:
        parent (str):
            Required. The parent table where the rows
            will be created. Format: tables/{table}
        requests (MutableSequence[google.area120.tables_v1alpha1.types.CreateRowRequest]):
            Required. The request message specifying the
            rows to create.
            A maximum of 500 rows can be created in a single
            batch.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    requests: MutableSequence["CreateRowRequest"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="CreateRowRequest",
    )


class BatchCreateRowsResponse(proto.Message):
    r"""Response message for TablesService.BatchCreateRows.

    Attributes:
        rows (MutableSequence[google.area120.tables_v1alpha1.types.Row]):
            The created rows.
    """

    rows: MutableSequence["Row"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Row",
    )


class UpdateRowRequest(proto.Message):
    r"""Request message for TablesService.UpdateRow.

    Attributes:
        row (google.area120.tables_v1alpha1.types.Row):
            Required. The row to update.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            The list of fields to update.
        view (google.area120.tables_v1alpha1.types.View):
            Optional. Column key to use for values in the
            row. Defaults to user entered name.
    """

    row: "Row" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="Row",
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )
    view: "View" = proto.Field(
        proto.ENUM,
        number=3,
        enum="View",
    )


class BatchUpdateRowsRequest(proto.Message):
    r"""Request message for TablesService.BatchUpdateRows.

    Attributes:
        parent (str):
            Required. The parent table shared by all rows
            being updated. Format: tables/{table}
        requests (MutableSequence[google.area120.tables_v1alpha1.types.UpdateRowRequest]):
            Required. The request messages specifying the
            rows to update.
            A maximum of 500 rows can be modified in a
            single batch.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    requests: MutableSequence["UpdateRowRequest"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="UpdateRowRequest",
    )


class BatchUpdateRowsResponse(proto.Message):
    r"""Response message for TablesService.BatchUpdateRows.

    Attributes:
        rows (MutableSequence[google.area120.tables_v1alpha1.types.Row]):
            The updated rows.
    """

    rows: MutableSequence["Row"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Row",
    )


class DeleteRowRequest(proto.Message):
    r"""Request message for TablesService.DeleteRow

    Attributes:
        name (str):
            Required. The name of the row to delete.
            Format: tables/{table}/rows/{row}
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class BatchDeleteRowsRequest(proto.Message):
    r"""Request message for TablesService.BatchDeleteRows

    Attributes:
        parent (str):
            Required. The parent table shared by all rows
            being deleted. Format: tables/{table}
        names (MutableSequence[str]):
            Required. The names of the rows to delete.
            All rows must belong to the parent table or else
            the entire batch will fail. A maximum of 500
            rows can be deleted in a batch.
            Format: tables/{table}/rows/{row}
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    names: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )


class Table(proto.Message):
    r"""A single table.

    Attributes:
        name (str):
            The resource name of the table. Table names have the form
            ``tables/{table}``.
        display_name (str):
            The human readable title of the table.
        columns (MutableSequence[google.area120.tables_v1alpha1.types.ColumnDescription]):
            List of columns in this table.
            Order of columns matches the display order.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=2,
    )
    columns: MutableSequence["ColumnDescription"] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message="ColumnDescription",
    )


class ColumnDescription(proto.Message):
    r"""Details on a column in the table.

    Attributes:
        name (str):
            column name
        data_type (str):
            Data type of the column Supported types are auto_id,
            boolean, boolean_list, creator, create_timestamp, date,
            dropdown, location, integer, integer_list, number,
            number_list, person, person_list, tags, check_list, text,
            text_list, update_timestamp, updater, relationship,
            file_attachment_list. These types directly map to the column
            types supported on Tables website.
        id (str):
            Internal id for a column.
        labels (MutableSequence[google.area120.tables_v1alpha1.types.LabeledItem]):
            Optional. Range of labeled values for the
            column. Some columns like tags and drop-downs
            limit the values to a set of possible values. We
            return the range of values in such cases to help
            clients implement better user data validation.
        relationship_details (google.area120.tables_v1alpha1.types.RelationshipDetails):
            Optional. Additional details about a relationship column.
            Specified when data_type is relationship.
        lookup_details (google.area120.tables_v1alpha1.types.LookupDetails):
            Optional. Indicates that this is a lookup
            column whose value is derived from the
            relationship column specified in the details.
            Lookup columns can not be updated directly. To
            change the value you must update the associated
            relationship column.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    data_type: str = proto.Field(
        proto.STRING,
        number=2,
    )
    id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    labels: MutableSequence["LabeledItem"] = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message="LabeledItem",
    )
    relationship_details: "RelationshipDetails" = proto.Field(
        proto.MESSAGE,
        number=5,
        message="RelationshipDetails",
    )
    lookup_details: "LookupDetails" = proto.Field(
        proto.MESSAGE,
        number=6,
        message="LookupDetails",
    )


class LabeledItem(proto.Message):
    r"""A single item in a labeled column.

    Attributes:
        name (str):
            Display string as entered by user.
        id (str):
            Internal id associated with the item.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    id: str = proto.Field(
        proto.STRING,
        number=2,
    )


class RelationshipDetails(proto.Message):
    r"""Details about a relationship column.

    Attributes:
        linked_table (str):
            The name of the table this relationship is
            linked to.
    """

    linked_table: str = proto.Field(
        proto.STRING,
        number=1,
    )


class LookupDetails(proto.Message):
    r"""Details about a lookup column whose value comes from the
    associated relationship.

    Attributes:
        relationship_column (str):
            The name of the relationship column
            associated with the lookup.
        relationship_column_id (str):
            The id of the relationship column.
    """

    relationship_column: str = proto.Field(
        proto.STRING,
        number=1,
    )
    relationship_column_id: str = proto.Field(
        proto.STRING,
        number=2,
    )


class Row(proto.Message):
    r"""A single row in a table.

    Attributes:
        name (str):
            The resource name of the row. Row names have the form
            ``tables/{table}/rows/{row}``. The name is ignored when
            creating a row.
        values (MutableMapping[str, google.protobuf.struct_pb2.Value]):
            The values of the row. This is a map of
            column key to value. Key is user entered
            name(default) or the internal column id based on
            the view in the request.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    values: MutableMapping[str, struct_pb2.Value] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=2,
        message=struct_pb2.Value,
    )


class Workspace(proto.Message):
    r"""A single workspace.

    Attributes:
        name (str):
            The resource name of the workspace. Workspace names have the
            form ``workspaces/{workspace}``.
        display_name (str):
            The human readable title of the workspace.
        tables (MutableSequence[google.area120.tables_v1alpha1.types.Table]):
            The list of tables in the workspace.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=2,
    )
    tables: MutableSequence["Table"] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message="Table",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
