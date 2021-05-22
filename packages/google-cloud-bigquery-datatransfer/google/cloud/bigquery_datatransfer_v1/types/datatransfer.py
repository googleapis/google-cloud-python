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

from google.cloud.bigquery_datatransfer_v1.types import transfer
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.bigquery.datatransfer.v1",
    manifest={
        "DataSourceParameter",
        "DataSource",
        "GetDataSourceRequest",
        "ListDataSourcesRequest",
        "ListDataSourcesResponse",
        "CreateTransferConfigRequest",
        "UpdateTransferConfigRequest",
        "GetTransferConfigRequest",
        "DeleteTransferConfigRequest",
        "GetTransferRunRequest",
        "DeleteTransferRunRequest",
        "ListTransferConfigsRequest",
        "ListTransferConfigsResponse",
        "ListTransferRunsRequest",
        "ListTransferRunsResponse",
        "ListTransferLogsRequest",
        "ListTransferLogsResponse",
        "CheckValidCredsRequest",
        "CheckValidCredsResponse",
        "ScheduleTransferRunsRequest",
        "ScheduleTransferRunsResponse",
        "StartManualTransferRunsRequest",
        "StartManualTransferRunsResponse",
    },
)


class DataSourceParameter(proto.Message):
    r"""Represents a data source parameter with validation rules, so
    that parameters can be rendered in the UI. These parameters are
    given to us by supported data sources, and include all needed
    information for rendering and validation.
    Thus, whoever uses this api can decide to generate either
    generic ui, or custom data source specific forms.

    Attributes:
        param_id (str):
            Parameter identifier.
        display_name (str):
            Parameter display name in the user interface.
        description (str):
            Parameter description.
        type_ (google.cloud.bigquery_datatransfer_v1.types.DataSourceParameter.Type):
            Parameter type.
        required (bool):
            Is parameter required.
        repeated (bool):
            Deprecated. This field has no effect.
        validation_regex (str):
            Regular expression which can be used for
            parameter validation.
        allowed_values (Sequence[str]):
            All possible values for the parameter.
        min_value (google.protobuf.wrappers_pb2.DoubleValue):
            For integer and double values specifies
            minimum allowed value.
        max_value (google.protobuf.wrappers_pb2.DoubleValue):
            For integer and double values specifies
            maxminum allowed value.
        fields (Sequence[google.cloud.bigquery_datatransfer_v1.types.DataSourceParameter]):
            Deprecated. This field has no effect.
        validation_description (str):
            Description of the requirements for this
            field, in case the user input does not fulfill
            the regex pattern or min/max values.
        validation_help_url (str):
            URL to a help document to further explain the
            naming requirements.
        immutable (bool):
            Cannot be changed after initial creation.
        recurse (bool):
            Deprecated. This field has no effect.
        deprecated (bool):
            If true, it should not be used in new
            transfers, and it should not be visible to
            users.
    """

    class Type(proto.Enum):
        r"""Parameter type."""
        TYPE_UNSPECIFIED = 0
        STRING = 1
        INTEGER = 2
        DOUBLE = 3
        BOOLEAN = 4
        RECORD = 5
        PLUS_PAGE = 6

    param_id = proto.Field(proto.STRING, number=1,)
    display_name = proto.Field(proto.STRING, number=2,)
    description = proto.Field(proto.STRING, number=3,)
    type_ = proto.Field(proto.ENUM, number=4, enum=Type,)
    required = proto.Field(proto.BOOL, number=5,)
    repeated = proto.Field(proto.BOOL, number=6,)
    validation_regex = proto.Field(proto.STRING, number=7,)
    allowed_values = proto.RepeatedField(proto.STRING, number=8,)
    min_value = proto.Field(proto.MESSAGE, number=9, message=wrappers_pb2.DoubleValue,)
    max_value = proto.Field(proto.MESSAGE, number=10, message=wrappers_pb2.DoubleValue,)
    fields = proto.RepeatedField(
        proto.MESSAGE, number=11, message="DataSourceParameter",
    )
    validation_description = proto.Field(proto.STRING, number=12,)
    validation_help_url = proto.Field(proto.STRING, number=13,)
    immutable = proto.Field(proto.BOOL, number=14,)
    recurse = proto.Field(proto.BOOL, number=15,)
    deprecated = proto.Field(proto.BOOL, number=20,)


class DataSource(proto.Message):
    r"""Represents data source metadata. Metadata is sufficient to
    render UI and request proper OAuth tokens.

    Attributes:
        name (str):
            Output only. Data source resource name.
        data_source_id (str):
            Data source id.
        display_name (str):
            User friendly data source name.
        description (str):
            User friendly data source description string.
        client_id (str):
            Data source client id which should be used to
            receive refresh token.
        scopes (Sequence[str]):
            Api auth scopes for which refresh token needs
            to be obtained. These are scopes needed by a
            data source to prepare data and ingest them into
            BigQuery, e.g.,
            https://www.googleapis.com/auth/bigquery
        transfer_type (google.cloud.bigquery_datatransfer_v1.types.TransferType):
            Deprecated. This field has no effect.
        supports_multiple_transfers (bool):
            Deprecated. This field has no effect.
        update_deadline_seconds (int):
            The number of seconds to wait for an update
            from the data source before the Data Transfer
            Service marks the transfer as FAILED.
        default_schedule (str):
            Default data transfer schedule. Examples of valid schedules
            include: ``1st,3rd monday of month 15:30``,
            ``every wed,fri of jan,jun 13:15``, and
            ``first sunday of quarter 00:00``.
        supports_custom_schedule (bool):
            Specifies whether the data source supports a user defined
            schedule, or operates on the default schedule. When set to
            ``true``, user can override default schedule.
        parameters (Sequence[google.cloud.bigquery_datatransfer_v1.types.DataSourceParameter]):
            Data source parameters.
        help_url (str):
            Url for the help document for this data
            source.
        authorization_type (google.cloud.bigquery_datatransfer_v1.types.DataSource.AuthorizationType):
            Indicates the type of authorization.
        data_refresh_type (google.cloud.bigquery_datatransfer_v1.types.DataSource.DataRefreshType):
            Specifies whether the data source supports
            automatic data refresh for the past few days,
            and how it's supported. For some data sources,
            data might not be complete until a few days
            later, so it's useful to refresh data
            automatically.
        default_data_refresh_window_days (int):
            Default data refresh window on days. Only meaningful when
            ``data_refresh_type`` = ``SLIDING_WINDOW``.
        manual_runs_disabled (bool):
            Disables backfilling and manual run
            scheduling for the data source.
        minimum_schedule_interval (google.protobuf.duration_pb2.Duration):
            The minimum interval for scheduler to
            schedule runs.
    """

    class AuthorizationType(proto.Enum):
        r"""The type of authorization needed for this data source."""
        AUTHORIZATION_TYPE_UNSPECIFIED = 0
        AUTHORIZATION_CODE = 1
        GOOGLE_PLUS_AUTHORIZATION_CODE = 2
        FIRST_PARTY_OAUTH = 3

    class DataRefreshType(proto.Enum):
        r"""Represents how the data source supports data auto refresh."""
        DATA_REFRESH_TYPE_UNSPECIFIED = 0
        SLIDING_WINDOW = 1
        CUSTOM_SLIDING_WINDOW = 2

    name = proto.Field(proto.STRING, number=1,)
    data_source_id = proto.Field(proto.STRING, number=2,)
    display_name = proto.Field(proto.STRING, number=3,)
    description = proto.Field(proto.STRING, number=4,)
    client_id = proto.Field(proto.STRING, number=5,)
    scopes = proto.RepeatedField(proto.STRING, number=6,)
    transfer_type = proto.Field(proto.ENUM, number=7, enum=transfer.TransferType,)
    supports_multiple_transfers = proto.Field(proto.BOOL, number=8,)
    update_deadline_seconds = proto.Field(proto.INT32, number=9,)
    default_schedule = proto.Field(proto.STRING, number=10,)
    supports_custom_schedule = proto.Field(proto.BOOL, number=11,)
    parameters = proto.RepeatedField(
        proto.MESSAGE, number=12, message="DataSourceParameter",
    )
    help_url = proto.Field(proto.STRING, number=13,)
    authorization_type = proto.Field(proto.ENUM, number=14, enum=AuthorizationType,)
    data_refresh_type = proto.Field(proto.ENUM, number=15, enum=DataRefreshType,)
    default_data_refresh_window_days = proto.Field(proto.INT32, number=16,)
    manual_runs_disabled = proto.Field(proto.BOOL, number=17,)
    minimum_schedule_interval = proto.Field(
        proto.MESSAGE, number=18, message=duration_pb2.Duration,
    )


class GetDataSourceRequest(proto.Message):
    r"""A request to get data source info.
    Attributes:
        name (str):
            Required. The field will contain name of the resource
            requested, for example:
            ``projects/{project_id}/dataSources/{data_source_id}`` or
            ``projects/{project_id}/locations/{location_id}/dataSources/{data_source_id}``
    """

    name = proto.Field(proto.STRING, number=1,)


class ListDataSourcesRequest(proto.Message):
    r"""Request to list supported data sources and their data
    transfer settings.

    Attributes:
        parent (str):
            Required. The BigQuery project id for which data sources
            should be returned. Must be in the form:
            ``projects/{project_id}`` or
            \`projects/{project_id}/locations/{location_id}
        page_token (str):
            Pagination token, which can be used to request a specific
            page of ``ListDataSourcesRequest`` list results. For
            multiple-page results, ``ListDataSourcesResponse`` outputs a
            ``next_page`` token, which can be used as the ``page_token``
            value to request the next page of list results.
        page_size (int):
            Page size. The default page size is the
            maximum value of 1000 results.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_token = proto.Field(proto.STRING, number=3,)
    page_size = proto.Field(proto.INT32, number=4,)


class ListDataSourcesResponse(proto.Message):
    r"""Returns list of supported data sources and their metadata.
    Attributes:
        data_sources (Sequence[google.cloud.bigquery_datatransfer_v1.types.DataSource]):
            List of supported data sources and their
            transfer settings.
        next_page_token (str):
            Output only. The next-pagination token. For multiple-page
            list results, this token can be used as the
            ``ListDataSourcesRequest.page_token`` to request the next
            page of list results.
    """

    @property
    def raw_page(self):
        return self

    data_sources = proto.RepeatedField(proto.MESSAGE, number=1, message="DataSource",)
    next_page_token = proto.Field(proto.STRING, number=2,)


class CreateTransferConfigRequest(proto.Message):
    r"""A request to create a data transfer configuration. If new
    credentials are needed for this transfer configuration, an
    authorization code must be provided. If an authorization code is
    provided, the transfer configuration will be associated with the
    user id corresponding to the authorization code. Otherwise, the
    transfer configuration will be associated with the calling user.

    Attributes:
        parent (str):
            Required. The BigQuery project id where the transfer
            configuration should be created. Must be in the format
            projects/{project_id}/locations/{location_id} or
            projects/{project_id}. If specified location and location of
            the destination bigquery dataset do not match - the request
            will fail.
        transfer_config (google.cloud.bigquery_datatransfer_v1.types.TransferConfig):
            Required. Data transfer configuration to
            create.
        authorization_code (str):
            Optional OAuth2 authorization code to use with this transfer
            configuration. This is required if new credentials are
            needed, as indicated by ``CheckValidCreds``. In order to
            obtain authorization_code, please make a request to
            https://www.gstatic.com/bigquerydatatransfer/oauthz/auth?client_id=&scope=<data_source_scopes>&redirect_uri=<redirect_uri>

            -  client_id should be OAuth client_id of BigQuery DTS API
               for the given data source returned by ListDataSources
               method.
            -  data_source_scopes are the scopes returned by
               ListDataSources method.
            -  redirect_uri is an optional parameter. If not specified,
               then authorization code is posted to the opener of
               authorization flow window. Otherwise it will be sent to
               the redirect uri. A special value of
               urn:ietf:wg:oauth:2.0:oob means that authorization code
               should be returned in the title bar of the browser, with
               the page text prompting the user to copy the code and
               paste it in the application.
        version_info (str):
            Optional version info. If users want to find a very recent
            access token, that is, immediately after approving access,
            users have to set the version_info claim in the token
            request. To obtain the version_info, users must use the
            "none+gsession" response type. which be return a
            version_info back in the authorization response which be be
            put in a JWT claim in the token request.
        service_account_name (str):
            Optional service account name. If this field
            is set, transfer config will be created with
            this service account credentials. It requires
            that requesting user calling this API has
            permissions to act as this service account.
    """

    parent = proto.Field(proto.STRING, number=1,)
    transfer_config = proto.Field(
        proto.MESSAGE, number=2, message=transfer.TransferConfig,
    )
    authorization_code = proto.Field(proto.STRING, number=3,)
    version_info = proto.Field(proto.STRING, number=5,)
    service_account_name = proto.Field(proto.STRING, number=6,)


class UpdateTransferConfigRequest(proto.Message):
    r"""A request to update a transfer configuration. To update the
    user id of the transfer configuration, an authorization code
    needs to be provided.

    Attributes:
        transfer_config (google.cloud.bigquery_datatransfer_v1.types.TransferConfig):
            Required. Data transfer configuration to
            create.
        authorization_code (str):
            Optional OAuth2 authorization code to use with this transfer
            configuration. If it is provided, the transfer configuration
            will be associated with the authorizing user. In order to
            obtain authorization_code, please make a request to
            https://www.gstatic.com/bigquerydatatransfer/oauthz/auth?client_id=&scope=<data_source_scopes>&redirect_uri=<redirect_uri>

            -  client_id should be OAuth client_id of BigQuery DTS API
               for the given data source returned by ListDataSources
               method.
            -  data_source_scopes are the scopes returned by
               ListDataSources method.
            -  redirect_uri is an optional parameter. If not specified,
               then authorization code is posted to the opener of
               authorization flow window. Otherwise it will be sent to
               the redirect uri. A special value of
               urn:ietf:wg:oauth:2.0:oob means that authorization code
               should be returned in the title bar of the browser, with
               the page text prompting the user to copy the code and
               paste it in the application.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Required list of fields to be
            updated in this request.
        version_info (str):
            Optional version info. If users want to find a very recent
            access token, that is, immediately after approving access,
            users have to set the version_info claim in the token
            request. To obtain the version_info, users must use the
            "none+gsession" response type. which be return a
            version_info back in the authorization response which be be
            put in a JWT claim in the token request.
        service_account_name (str):
            Optional service account name. If this field is set and
            "service_account_name" is set in update_mask, transfer
            config will be updated to use this service account
            credentials. It requires that requesting user calling this
            API has permissions to act as this service account.
    """

    transfer_config = proto.Field(
        proto.MESSAGE, number=1, message=transfer.TransferConfig,
    )
    authorization_code = proto.Field(proto.STRING, number=3,)
    update_mask = proto.Field(
        proto.MESSAGE, number=4, message=field_mask_pb2.FieldMask,
    )
    version_info = proto.Field(proto.STRING, number=5,)
    service_account_name = proto.Field(proto.STRING, number=6,)


class GetTransferConfigRequest(proto.Message):
    r"""A request to get data transfer information.
    Attributes:
        name (str):
            Required. The field will contain name of the resource
            requested, for example:
            ``projects/{project_id}/transferConfigs/{config_id}`` or
            ``projects/{project_id}/locations/{location_id}/transferConfigs/{config_id}``
    """

    name = proto.Field(proto.STRING, number=1,)


class DeleteTransferConfigRequest(proto.Message):
    r"""A request to delete data transfer information. All associated
    transfer runs and log messages will be deleted as well.

    Attributes:
        name (str):
            Required. The field will contain name of the resource
            requested, for example:
            ``projects/{project_id}/transferConfigs/{config_id}`` or
            ``projects/{project_id}/locations/{location_id}/transferConfigs/{config_id}``
    """

    name = proto.Field(proto.STRING, number=1,)


class GetTransferRunRequest(proto.Message):
    r"""A request to get data transfer run information.
    Attributes:
        name (str):
            Required. The field will contain name of the resource
            requested, for example:
            ``projects/{project_id}/transferConfigs/{config_id}/runs/{run_id}``
            or
            ``projects/{project_id}/locations/{location_id}/transferConfigs/{config_id}/runs/{run_id}``
    """

    name = proto.Field(proto.STRING, number=1,)


class DeleteTransferRunRequest(proto.Message):
    r"""A request to delete data transfer run information.
    Attributes:
        name (str):
            Required. The field will contain name of the resource
            requested, for example:
            ``projects/{project_id}/transferConfigs/{config_id}/runs/{run_id}``
            or
            ``projects/{project_id}/locations/{location_id}/transferConfigs/{config_id}/runs/{run_id}``
    """

    name = proto.Field(proto.STRING, number=1,)


class ListTransferConfigsRequest(proto.Message):
    r"""A request to list data transfers configured for a BigQuery
    project.

    Attributes:
        parent (str):
            Required. The BigQuery project id for which data sources
            should be returned: ``projects/{project_id}`` or
            ``projects/{project_id}/locations/{location_id}``
        data_source_ids (Sequence[str]):
            When specified, only configurations of
            requested data sources are returned.
        page_token (str):
            Pagination token, which can be used to request a specific
            page of ``ListTransfersRequest`` list results. For
            multiple-page results, ``ListTransfersResponse`` outputs a
            ``next_page`` token, which can be used as the ``page_token``
            value to request the next page of list results.
        page_size (int):
            Page size. The default page size is the
            maximum value of 1000 results.
    """

    parent = proto.Field(proto.STRING, number=1,)
    data_source_ids = proto.RepeatedField(proto.STRING, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)
    page_size = proto.Field(proto.INT32, number=4,)


class ListTransferConfigsResponse(proto.Message):
    r"""The returned list of pipelines in the project.
    Attributes:
        transfer_configs (Sequence[google.cloud.bigquery_datatransfer_v1.types.TransferConfig]):
            Output only. The stored pipeline transfer
            configurations.
        next_page_token (str):
            Output only. The next-pagination token. For multiple-page
            list results, this token can be used as the
            ``ListTransferConfigsRequest.page_token`` to request the
            next page of list results.
    """

    @property
    def raw_page(self):
        return self

    transfer_configs = proto.RepeatedField(
        proto.MESSAGE, number=1, message=transfer.TransferConfig,
    )
    next_page_token = proto.Field(proto.STRING, number=2,)


class ListTransferRunsRequest(proto.Message):
    r"""A request to list data transfer runs. UI can use this method
    to show/filter specific data transfer runs. The data source can
    use this method to request all scheduled transfer runs.

    Attributes:
        parent (str):
            Required. Name of transfer configuration for which transfer
            runs should be retrieved. Format of transfer configuration
            resource name is:
            ``projects/{project_id}/transferConfigs/{config_id}`` or
            ``projects/{project_id}/locations/{location_id}/transferConfigs/{config_id}``.
        states (Sequence[google.cloud.bigquery_datatransfer_v1.types.TransferState]):
            When specified, only transfer runs with
            requested states are returned.
        page_token (str):
            Pagination token, which can be used to request a specific
            page of ``ListTransferRunsRequest`` list results. For
            multiple-page results, ``ListTransferRunsResponse`` outputs
            a ``next_page`` token, which can be used as the
            ``page_token`` value to request the next page of list
            results.
        page_size (int):
            Page size. The default page size is the
            maximum value of 1000 results.
        run_attempt (google.cloud.bigquery_datatransfer_v1.types.ListTransferRunsRequest.RunAttempt):
            Indicates how run attempts are to be pulled.
    """

    class RunAttempt(proto.Enum):
        r"""Represents which runs should be pulled."""
        RUN_ATTEMPT_UNSPECIFIED = 0
        LATEST = 1

    parent = proto.Field(proto.STRING, number=1,)
    states = proto.RepeatedField(proto.ENUM, number=2, enum=transfer.TransferState,)
    page_token = proto.Field(proto.STRING, number=3,)
    page_size = proto.Field(proto.INT32, number=4,)
    run_attempt = proto.Field(proto.ENUM, number=5, enum=RunAttempt,)


class ListTransferRunsResponse(proto.Message):
    r"""The returned list of pipelines in the project.
    Attributes:
        transfer_runs (Sequence[google.cloud.bigquery_datatransfer_v1.types.TransferRun]):
            Output only. The stored pipeline transfer
            runs.
        next_page_token (str):
            Output only. The next-pagination token. For multiple-page
            list results, this token can be used as the
            ``ListTransferRunsRequest.page_token`` to request the next
            page of list results.
    """

    @property
    def raw_page(self):
        return self

    transfer_runs = proto.RepeatedField(
        proto.MESSAGE, number=1, message=transfer.TransferRun,
    )
    next_page_token = proto.Field(proto.STRING, number=2,)


class ListTransferLogsRequest(proto.Message):
    r"""A request to get user facing log messages associated with
    data transfer run.

    Attributes:
        parent (str):
            Required. Transfer run name in the form:
            ``projects/{project_id}/transferConfigs/{config_id}/runs/{run_id}``
            or
            ``projects/{project_id}/locations/{location_id}/transferConfigs/{config_id}/runs/{run_id}``
        page_token (str):
            Pagination token, which can be used to request a specific
            page of ``ListTransferLogsRequest`` list results. For
            multiple-page results, ``ListTransferLogsResponse`` outputs
            a ``next_page`` token, which can be used as the
            ``page_token`` value to request the next page of list
            results.
        page_size (int):
            Page size. The default page size is the
            maximum value of 1000 results.
        message_types (Sequence[google.cloud.bigquery_datatransfer_v1.types.TransferMessage.MessageSeverity]):
            Message types to return. If not populated -
            INFO, WARNING and ERROR messages are returned.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_token = proto.Field(proto.STRING, number=4,)
    page_size = proto.Field(proto.INT32, number=5,)
    message_types = proto.RepeatedField(
        proto.ENUM, number=6, enum=transfer.TransferMessage.MessageSeverity,
    )


class ListTransferLogsResponse(proto.Message):
    r"""The returned list transfer run messages.
    Attributes:
        transfer_messages (Sequence[google.cloud.bigquery_datatransfer_v1.types.TransferMessage]):
            Output only. The stored pipeline transfer
            messages.
        next_page_token (str):
            Output only. The next-pagination token. For multiple-page
            list results, this token can be used as the
            ``GetTransferRunLogRequest.page_token`` to request the next
            page of list results.
    """

    @property
    def raw_page(self):
        return self

    transfer_messages = proto.RepeatedField(
        proto.MESSAGE, number=1, message=transfer.TransferMessage,
    )
    next_page_token = proto.Field(proto.STRING, number=2,)


class CheckValidCredsRequest(proto.Message):
    r"""A request to determine whether the user has valid
    credentials. This method is used to limit the number of OAuth
    popups in the user interface. The user id is inferred from the
    API call context.
    If the data source has the Google+ authorization type, this
    method returns false, as it cannot be determined whether the
    credentials are already valid merely based on the user id.

    Attributes:
        name (str):
            Required. The data source in the form:
            ``projects/{project_id}/dataSources/{data_source_id}`` or
            ``projects/{project_id}/locations/{location_id}/dataSources/{data_source_id}``.
    """

    name = proto.Field(proto.STRING, number=1,)


class CheckValidCredsResponse(proto.Message):
    r"""A response indicating whether the credentials exist and are
    valid.

    Attributes:
        has_valid_creds (bool):
            If set to ``true``, the credentials exist and are valid.
    """

    has_valid_creds = proto.Field(proto.BOOL, number=1,)


class ScheduleTransferRunsRequest(proto.Message):
    r"""A request to schedule transfer runs for a time range.
    Attributes:
        parent (str):
            Required. Transfer configuration name in the form:
            ``projects/{project_id}/transferConfigs/{config_id}`` or
            ``projects/{project_id}/locations/{location_id}/transferConfigs/{config_id}``.
        start_time (google.protobuf.timestamp_pb2.Timestamp):
            Required. Start time of the range of transfer runs. For
            example, ``"2017-05-25T00:00:00+00:00"``.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Required. End time of the range of transfer runs. For
            example, ``"2017-05-30T00:00:00+00:00"``.
    """

    parent = proto.Field(proto.STRING, number=1,)
    start_time = proto.Field(proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,)
    end_time = proto.Field(proto.MESSAGE, number=3, message=timestamp_pb2.Timestamp,)


class ScheduleTransferRunsResponse(proto.Message):
    r"""A response to schedule transfer runs for a time range.
    Attributes:
        runs (Sequence[google.cloud.bigquery_datatransfer_v1.types.TransferRun]):
            The transfer runs that were scheduled.
    """

    runs = proto.RepeatedField(proto.MESSAGE, number=1, message=transfer.TransferRun,)


class StartManualTransferRunsRequest(proto.Message):
    r"""A request to start manual transfer runs.
    Attributes:
        parent (str):
            Transfer configuration name in the form:
            ``projects/{project_id}/transferConfigs/{config_id}`` or
            ``projects/{project_id}/locations/{location_id}/transferConfigs/{config_id}``.
        requested_time_range (google.cloud.bigquery_datatransfer_v1.types.StartManualTransferRunsRequest.TimeRange):
            Time range for the transfer runs that should
            be started.
        requested_run_time (google.protobuf.timestamp_pb2.Timestamp):
            Specific run_time for a transfer run to be started. The
            requested_run_time must not be in the future.
    """

    class TimeRange(proto.Message):
        r"""A specification for a time range, this will request transfer runs
        with run_time between start_time (inclusive) and end_time
        (exclusive).

        Attributes:
            start_time (google.protobuf.timestamp_pb2.Timestamp):
                Start time of the range of transfer runs. For example,
                ``"2017-05-25T00:00:00+00:00"``. The start_time must be
                strictly less than the end_time. Creates transfer runs where
                run_time is in the range betwen start_time (inclusive) and
                end_time (exlusive).
            end_time (google.protobuf.timestamp_pb2.Timestamp):
                End time of the range of transfer runs. For example,
                ``"2017-05-30T00:00:00+00:00"``. The end_time must not be in
                the future. Creates transfer runs where run_time is in the
                range betwen start_time (inclusive) and end_time (exlusive).
        """

        start_time = proto.Field(
            proto.MESSAGE, number=1, message=timestamp_pb2.Timestamp,
        )
        end_time = proto.Field(
            proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,
        )

    parent = proto.Field(proto.STRING, number=1,)
    requested_time_range = proto.Field(
        proto.MESSAGE, number=3, oneof="time", message=TimeRange,
    )
    requested_run_time = proto.Field(
        proto.MESSAGE, number=4, oneof="time", message=timestamp_pb2.Timestamp,
    )


class StartManualTransferRunsResponse(proto.Message):
    r"""A response to start manual transfer runs.
    Attributes:
        runs (Sequence[google.cloud.bigquery_datatransfer_v1.types.TransferRun]):
            The transfer runs that were created.
    """

    runs = proto.RepeatedField(proto.MESSAGE, number=1, message=transfer.TransferRun,)


__all__ = tuple(sorted(__protobuf__.manifest))
