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

from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

from google.analytics.data_v1alpha.types import data

__protobuf__ = proto.module(
    package="google.analytics.data.v1alpha",
    manifest={
        "CreateRecurringAudienceListRequest",
        "RecurringAudienceList",
        "WebhookNotification",
        "GetRecurringAudienceListRequest",
        "ListRecurringAudienceListsRequest",
        "ListRecurringAudienceListsResponse",
        "GetAudienceListRequest",
        "ListAudienceListsRequest",
        "ListAudienceListsResponse",
        "CreateAudienceListRequest",
        "AudienceList",
        "AudienceListMetadata",
        "QueryAudienceListRequest",
        "QueryAudienceListResponse",
        "SheetExportAudienceListRequest",
        "SheetExportAudienceListResponse",
        "AudienceRow",
        "AudienceDimension",
        "AudienceDimensionValue",
        "RunFunnelReportRequest",
        "RunFunnelReportResponse",
    },
)


class CreateRecurringAudienceListRequest(proto.Message):
    r"""A request to create a new recurring audience list.

    Attributes:
        parent (str):
            Required. The parent resource where this recurring audience
            list will be created. Format: ``properties/{property}``
        recurring_audience_list (google.analytics.data_v1alpha.types.RecurringAudienceList):
            Required. The recurring audience list to
            create.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    recurring_audience_list: "RecurringAudienceList" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="RecurringAudienceList",
    )


class RecurringAudienceList(proto.Message):
    r"""A recurring audience list produces new audience lists each
    day. Audience lists are users in an audience at the time of the
    list's creation. A recurring audience list ensures that you have
    audience list based on the most recent data available for use
    each day.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Output only. Identifier. The recurring audience list
            resource name assigned during creation. This resource name
            identifies this ``RecurringAudienceList``.

            Format:
            ``properties/{property}/recurringAudienceLists/{recurring_audience_list}``
        audience (str):
            Required. The audience resource name. This resource name
            identifies the audience being listed and is shared between
            the Analytics Data & Admin APIs.

            Format: ``properties/{property}/audiences/{audience}``
        audience_display_name (str):
            Output only. The descriptive display name for
            this audience. For example, "Purchasers".
        dimensions (MutableSequence[google.analytics.data_v1alpha.types.AudienceDimension]):
            Required. The dimensions requested and
            displayed in the audience list response.
        active_days_remaining (int):
            Optional. The number of remaining days that a
            recurring audience export will produce an
            audience list instance. This counter decreases
            by one each day, and when it reaches zero, no
            new audience lists will be created.

            Recurring audience list request for Analytics
            360 properties default to 180 days and have a
            maximum of 365 days. Requests for standard
            Analytics properties default to 14 days and have
            a maximum of 30 days.

            The minimum value allowed during creation is 1.
            Requests above their respective maximum will be
            coerced to their maximum.

            This field is a member of `oneof`_ ``_active_days_remaining``.
        audience_lists (MutableSequence[str]):
            Output only. Audience list resource names for
            audience list instances created for this
            recurring audience list. One audience list is
            created for each day, and the audience list will
            be listed here.

            This list is ordered with the most recently
            created audience list first.
        webhook_notification (google.analytics.data_v1alpha.types.WebhookNotification):
            Optional. Configures webhook notifications to
            be sent from the Google Analytics Data API to
            your webhook server. Use of webhooks is
            optional. If unused, you'll need to poll this
            API to determine when a recurring audience list
            creates new audience lists. Webhooks allow a
            notification to be sent to your servers & avoid
            the need for polling.

            Two POST requests will be sent each time a
            recurring audience list creates an audience
            list. This happens once per day until a
            recurring audience list reaches 0 active days
            remaining. The first request will be sent
            showing a newly created audience list in its
            CREATING state. The second request will be sent
            after the audience list completes creation
            (either the ACTIVE or FAILED state).

            This field is a member of `oneof`_ ``_webhook_notification``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    audience: str = proto.Field(
        proto.STRING,
        number=2,
    )
    audience_display_name: str = proto.Field(
        proto.STRING,
        number=3,
    )
    dimensions: MutableSequence["AudienceDimension"] = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message="AudienceDimension",
    )
    active_days_remaining: int = proto.Field(
        proto.INT32,
        number=5,
        optional=True,
    )
    audience_lists: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=6,
    )
    webhook_notification: "WebhookNotification" = proto.Field(
        proto.MESSAGE,
        number=8,
        optional=True,
        message="WebhookNotification",
    )


class WebhookNotification(proto.Message):
    r"""Configures a long-running operation resource to send a
    webhook notification from the Google Analytics Data API to your
    webhook server when the resource updates.

    Notification configurations contain private values & are only
    visible to your GCP project. Different GCP projects may attach
    different webhook notifications to the same long-running
    operation resource.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        uri (str):
            Optional. The web address that will receive the webhook
            notification. This address will receive POST requests as the
            state of the long running operation resource changes. The
            POST request will contain both a JSON version of the long
            running operation resource in the body and a
            ``sentTimestamp`` field. The sent timestamp will specify the
            unix microseconds since the epoch that the request was sent;
            this lets you identify replayed notifications.

            An example URI is
            ``https://us-central1-example-project-id.cloudfunctions.net/example-function-1``.

            The URI must use HTTPS and point to a site with a valid SSL
            certificate on the web server. The URI must have a maximum
            string length of 128 characters & use only the allowlisted
            characters from `RFC
            1738 <https://www.rfc-editor.org/rfc/rfc1738>`__.

            When your webhook server receives a notification, it is
            expected to reply with an HTTP response status code of 200
            within 5 seconds.

            A URI is required to use webhook notifications.

            Requests to this webhook server will contain an ID token
            authenticating the service account
            ``google-analytics-audience-export@system.gserviceaccount.com``.
            To learn more about ID tokens, see
            https://cloud.google.com/docs/authentication/token-types#id.
            For Google Cloud Functions, this lets you configure your
            function to require authentication. In Cloud IAM, you will
            need to grant the service account permissions to the Cloud
            Run Invoker (``roles/run.invoker``) & Cloud Functions
            Invoker (``roles/cloudfunctions.invoker``) roles for the
            webhook post request to pass Google Cloud Functions
            authentication. This API can send webhook notifications to
            arbitrary URIs; for webhook servers other than Google Cloud
            Functions, this ID token in the authorization bearer header
            should be ignored if it is not needed.

            This field is a member of `oneof`_ ``_uri``.
        channel_token (str):
            Optional. The channel token is an arbitrary string value and
            must have a maximum string length of 64 characters. Channel
            tokens allow you to verify the source of a webhook
            notification. This guards against the message being spoofed.
            The channel token will be specified in the
            ``X-Goog-Channel-Token`` HTTP header of the webhook POST
            request.

            A channel token is not required to use webhook
            notifications.

            This field is a member of `oneof`_ ``_channel_token``.
    """

    uri: str = proto.Field(
        proto.STRING,
        number=1,
        optional=True,
    )
    channel_token: str = proto.Field(
        proto.STRING,
        number=2,
        optional=True,
    )


class GetRecurringAudienceListRequest(proto.Message):
    r"""A request to retrieve configuration metadata about a specific
    recurring audience list.

    Attributes:
        name (str):
            Required. The recurring audience list resource name. Format:
            ``properties/{property}/recurringAudienceLists/{recurring_audience_list}``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListRecurringAudienceListsRequest(proto.Message):
    r"""A request to list all recurring audience lists for a
    property.

    Attributes:
        parent (str):
            Required. All recurring audience lists for this property
            will be listed in the response. Format:
            ``properties/{property}``
        page_size (int):
            Optional. The maximum number of recurring
            audience lists to return. The service may return
            fewer than this value. If unspecified, at most
            200 recurring audience lists will be returned.
            The maximum value is 1000 (higher values will be
            coerced to the maximum).
        page_token (str):
            Optional. A page token, received from a previous
            ``ListRecurringAudienceLists`` call. Provide this to
            retrieve the subsequent page.

            When paginating, all other parameters provided to
            ``ListRecurringAudienceLists`` must match the call that
            provided the page token.
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


class ListRecurringAudienceListsResponse(proto.Message):
    r"""A list of all recurring audience lists for a property.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        recurring_audience_lists (MutableSequence[google.analytics.data_v1alpha.types.RecurringAudienceList]):
            Each recurring audience list for a property.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.

            This field is a member of `oneof`_ ``_next_page_token``.
    """

    @property
    def raw_page(self):
        return self

    recurring_audience_lists: MutableSequence[
        "RecurringAudienceList"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="RecurringAudienceList",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
        optional=True,
    )


class GetAudienceListRequest(proto.Message):
    r"""A request to retrieve configuration metadata about a specific
    audience list.

    Attributes:
        name (str):
            Required. The audience list resource name. Format:
            ``properties/{property}/audienceLists/{audience_list}``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListAudienceListsRequest(proto.Message):
    r"""A request to list all audience lists for a property.

    Attributes:
        parent (str):
            Required. All audience lists for this property will be
            listed in the response. Format: ``properties/{property}``
        page_size (int):
            Optional. The maximum number of audience
            lists to return. The service may return fewer
            than this value. If unspecified, at most 200
            audience lists will be returned. The maximum
            value is 1000 (higher values will be coerced to
            the maximum).
        page_token (str):
            Optional. A page token, received from a previous
            ``ListAudienceLists`` call. Provide this to retrieve the
            subsequent page.

            When paginating, all other parameters provided to
            ``ListAudienceLists`` must match the call that provided the
            page token.
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


class ListAudienceListsResponse(proto.Message):
    r"""A list of all audience lists for a property.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        audience_lists (MutableSequence[google.analytics.data_v1alpha.types.AudienceList]):
            Each audience list for a property.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.

            This field is a member of `oneof`_ ``_next_page_token``.
    """

    @property
    def raw_page(self):
        return self

    audience_lists: MutableSequence["AudienceList"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="AudienceList",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
        optional=True,
    )


class CreateAudienceListRequest(proto.Message):
    r"""A request to create a new audience list.

    Attributes:
        parent (str):
            Required. The parent resource where this audience list will
            be created. Format: ``properties/{property}``
        audience_list (google.analytics.data_v1alpha.types.AudienceList):
            Required. The audience list to create.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    audience_list: "AudienceList" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="AudienceList",
    )


class AudienceList(proto.Message):
    r"""An audience list is a list of users in an audience at the
    time of the list's creation. One audience may have multiple
    audience lists created for different days.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Output only. Identifier. The audience list resource name
            assigned during creation. This resource name identifies this
            ``AudienceList``.

            Format:
            ``properties/{property}/audienceLists/{audience_list}``
        audience (str):
            Required. The audience resource name. This resource name
            identifies the audience being listed and is shared between
            the Analytics Data & Admin APIs.

            Format: ``properties/{property}/audiences/{audience}``
        audience_display_name (str):
            Output only. The descriptive display name for
            this audience. For example, "Purchasers".
        dimensions (MutableSequence[google.analytics.data_v1alpha.types.AudienceDimension]):
            Required. The dimensions requested and
            displayed in the query response.
        state (google.analytics.data_v1alpha.types.AudienceList.State):
            Output only. The current state for this
            AudienceList.

            This field is a member of `oneof`_ ``_state``.
        begin_creating_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when CreateAudienceList was called and
            the AudienceList began the ``CREATING`` state.

            This field is a member of `oneof`_ ``_begin_creating_time``.
        creation_quota_tokens_charged (int):
            Output only. The total quota tokens charged during creation
            of the AudienceList. Because this token count is based on
            activity from the ``CREATING`` state, this tokens charged
            will be fixed once an AudienceList enters the ``ACTIVE`` or
            ``FAILED`` states.
        row_count (int):
            Output only. The total number of rows in the
            AudienceList result.

            This field is a member of `oneof`_ ``_row_count``.
        error_message (str):
            Output only. Error message is populated when
            an audience list fails during creation. A common
            reason for such a failure is quota exhaustion.

            This field is a member of `oneof`_ ``_error_message``.
        percentage_completed (float):
            Output only. The percentage completed for
            this audience export ranging between 0 to 100.

            This field is a member of `oneof`_ ``_percentage_completed``.
        recurring_audience_list (str):
            Output only. The recurring audience list that
            created this audience list. Recurring audience
            lists create audience lists daily.

            If audience lists are created directly, they
            will have no associated recurring audience list,
            and this field will be blank.

            This field is a member of `oneof`_ ``_recurring_audience_list``.
        webhook_notification (google.analytics.data_v1alpha.types.WebhookNotification):
            Optional. Configures webhook notifications to
            be sent from the Google Analytics Data API to
            your webhook server. Use of webhooks is
            optional. If unused, you'll need to poll this
            API to determine when an audience list is ready
            to be used. Webhooks allow a notification to be
            sent to your servers & avoid the need for
            polling.

            Either one or two POST requests will be sent to
            the webhook. The first POST request will be sent
            immediately showing the newly created audience
            list in its CREATING state. The second POST
            request will be sent after the audience list
            completes creation (either the ACTIVE or FAILED
            state).

            If identical audience lists are requested in
            quick succession, the second & subsequent
            audience lists can be served from cache. In that
            case, the audience list create method can return
            an audience list is already ACTIVE. In this
            scenario, only one POST request will be sent to
            the webhook.

            This field is a member of `oneof`_ ``_webhook_notification``.
    """

    class State(proto.Enum):
        r"""The AudienceList currently exists in this state.

        Values:
            STATE_UNSPECIFIED (0):
                Unspecified state will never be used.
            CREATING (1):
                The AudienceList is currently creating and
                will be available in the future. Creating occurs
                immediately after the CreateAudienceList call.
            ACTIVE (2):
                The AudienceList is fully created and ready
                for querying. An AudienceList is updated to
                active asynchronously from a request; this
                occurs some time (for example 15 minutes) after
                the initial create call.
            FAILED (3):
                The AudienceList failed to be created. It is
                possible that re-requesting this audience list
                will succeed.
        """
        STATE_UNSPECIFIED = 0
        CREATING = 1
        ACTIVE = 2
        FAILED = 3

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    audience: str = proto.Field(
        proto.STRING,
        number=2,
    )
    audience_display_name: str = proto.Field(
        proto.STRING,
        number=3,
    )
    dimensions: MutableSequence["AudienceDimension"] = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message="AudienceDimension",
    )
    state: State = proto.Field(
        proto.ENUM,
        number=5,
        optional=True,
        enum=State,
    )
    begin_creating_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=6,
        optional=True,
        message=timestamp_pb2.Timestamp,
    )
    creation_quota_tokens_charged: int = proto.Field(
        proto.INT32,
        number=7,
    )
    row_count: int = proto.Field(
        proto.INT32,
        number=8,
        optional=True,
    )
    error_message: str = proto.Field(
        proto.STRING,
        number=9,
        optional=True,
    )
    percentage_completed: float = proto.Field(
        proto.DOUBLE,
        number=11,
        optional=True,
    )
    recurring_audience_list: str = proto.Field(
        proto.STRING,
        number=12,
        optional=True,
    )
    webhook_notification: "WebhookNotification" = proto.Field(
        proto.MESSAGE,
        number=13,
        optional=True,
        message="WebhookNotification",
    )


class AudienceListMetadata(proto.Message):
    r"""This metadata is currently blank."""


class QueryAudienceListRequest(proto.Message):
    r"""A request to list users in an audience list.

    Attributes:
        name (str):
            Required. The name of the audience list to retrieve users
            from. Format:
            ``properties/{property}/audienceLists/{audience_list}``
        offset (int):
            Optional. The row count of the start row. The first row is
            counted as row 0.

            When paging, the first request does not specify offset; or
            equivalently, sets offset to 0; the first request returns
            the first ``limit`` of rows. The second request sets offset
            to the ``limit`` of the first request; the second request
            returns the second ``limit`` of rows.

            To learn more about this pagination parameter, see
            `Pagination <https://developers.google.com/analytics/devguides/reporting/data/v1/basics#pagination>`__.
        limit (int):
            Optional. The number of rows to return. If unspecified,
            10,000 rows are returned. The API returns a maximum of
            250,000 rows per request, no matter how many you ask for.
            ``limit`` must be positive.

            The API can also return fewer rows than the requested
            ``limit``, if there aren't as many dimension values as the
            ``limit``.

            To learn more about this pagination parameter, see
            `Pagination <https://developers.google.com/analytics/devguides/reporting/data/v1/basics#pagination>`__.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    offset: int = proto.Field(
        proto.INT64,
        number=2,
    )
    limit: int = proto.Field(
        proto.INT64,
        number=3,
    )


class QueryAudienceListResponse(proto.Message):
    r"""A list of users in an audience list.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        audience_list (google.analytics.data_v1alpha.types.AudienceList):
            Configuration data about AudienceList being
            queried. Returned to help interpret the audience
            rows in this response. For example, the
            dimensions in this AudienceList correspond to
            the columns in the AudienceRows.

            This field is a member of `oneof`_ ``_audience_list``.
        audience_rows (MutableSequence[google.analytics.data_v1alpha.types.AudienceRow]):
            Rows for each user in an audience list. The
            number of rows in this response will be less
            than or equal to request's page size.
        row_count (int):
            The total number of rows in the AudienceList result.
            ``rowCount`` is independent of the number of rows returned
            in the response, the ``limit`` request parameter, and the
            ``offset`` request parameter. For example if a query returns
            175 rows and includes ``limit`` of 50 in the API request,
            the response will contain ``rowCount`` of 175 but only 50
            rows.

            To learn more about this pagination parameter, see
            `Pagination <https://developers.google.com/analytics/devguides/reporting/data/v1/basics#pagination>`__.

            This field is a member of `oneof`_ ``_row_count``.
    """

    audience_list: "AudienceList" = proto.Field(
        proto.MESSAGE,
        number=1,
        optional=True,
        message="AudienceList",
    )
    audience_rows: MutableSequence["AudienceRow"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="AudienceRow",
    )
    row_count: int = proto.Field(
        proto.INT32,
        number=3,
        optional=True,
    )


class SheetExportAudienceListRequest(proto.Message):
    r"""A request to export users in an audience list to a Google
    Sheet.

    Attributes:
        name (str):
            Required. The name of the audience list to retrieve users
            from. Format:
            ``properties/{property}/audienceLists/{audience_list}``
        offset (int):
            Optional. The row count of the start row. The first row is
            counted as row 0.

            When paging, the first request does not specify offset; or
            equivalently, sets offset to 0; the first request returns
            the first ``limit`` of rows. The second request sets offset
            to the ``limit`` of the first request; the second request
            returns the second ``limit`` of rows.

            To learn more about this pagination parameter, see
            `Pagination <https://developers.google.com/analytics/devguides/reporting/data/v1/basics#pagination>`__.
        limit (int):
            Optional. The number of rows to return. If unspecified,
            10,000 rows are returned. The API returns a maximum of
            250,000 rows per request, no matter how many you ask for.
            ``limit`` must be positive.

            The API can also return fewer rows than the requested
            ``limit``, if there aren't as many dimension values as the
            ``limit``.

            To learn more about this pagination parameter, see
            `Pagination <https://developers.google.com/analytics/devguides/reporting/data/v1/basics#pagination>`__.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    offset: int = proto.Field(
        proto.INT64,
        number=2,
    )
    limit: int = proto.Field(
        proto.INT64,
        number=3,
    )


class SheetExportAudienceListResponse(proto.Message):
    r"""The created Google Sheet with the list of users in an
    audience list.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        spreadsheet_uri (str):
            A uri for you to visit in your browser to
            view the Google Sheet.

            This field is a member of `oneof`_ ``_spreadsheet_uri``.
        spreadsheet_id (str):
            An ID that identifies the created Google
            Sheet resource.

            This field is a member of `oneof`_ ``_spreadsheet_id``.
        row_count (int):
            The total number of rows in the AudienceList result.
            ``rowCount`` is independent of the number of rows returned
            in the response, the ``limit`` request parameter, and the
            ``offset`` request parameter. For example if a query returns
            175 rows and includes ``limit`` of 50 in the API request,
            the response will contain ``rowCount`` of 175 but only 50
            rows.

            To learn more about this pagination parameter, see
            `Pagination <https://developers.google.com/analytics/devguides/reporting/data/v1/basics#pagination>`__.

            This field is a member of `oneof`_ ``_row_count``.
        audience_list (google.analytics.data_v1alpha.types.AudienceList):
            Configuration data about AudienceList being exported.
            Returned to help interpret the AudienceList in the Google
            Sheet of this response.

            For example, the AudienceList may have more rows than are
            present in the Google Sheet, and in that case, you may want
            to send an additional sheet export request with a different
            ``offset`` value to retrieve the next page of rows in an
            additional Google Sheet.

            This field is a member of `oneof`_ ``_audience_list``.
    """

    spreadsheet_uri: str = proto.Field(
        proto.STRING,
        number=1,
        optional=True,
    )
    spreadsheet_id: str = proto.Field(
        proto.STRING,
        number=2,
        optional=True,
    )
    row_count: int = proto.Field(
        proto.INT32,
        number=3,
        optional=True,
    )
    audience_list: "AudienceList" = proto.Field(
        proto.MESSAGE,
        number=4,
        optional=True,
        message="AudienceList",
    )


class AudienceRow(proto.Message):
    r"""Dimension value attributes for the audience user row.

    Attributes:
        dimension_values (MutableSequence[google.analytics.data_v1alpha.types.AudienceDimensionValue]):
            Each dimension value attribute for an
            audience user. One dimension value will be added
            for each dimension column requested.
    """

    dimension_values: MutableSequence["AudienceDimensionValue"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="AudienceDimensionValue",
    )


class AudienceDimension(proto.Message):
    r"""An audience dimension is a user attribute. Specific user attributed
    are requested and then later returned in the
    ``QueryAudienceListResponse``.

    Attributes:
        dimension_name (str):
            Optional. The API name of the dimension. See the `API
            Dimensions <https://developers.google.com/analytics/devguides/reporting/data/v1/audience-list-api-schema#dimensions>`__
            for the list of dimension names.
    """

    dimension_name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class AudienceDimensionValue(proto.Message):
    r"""The value of a dimension.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        value (str):
            Value as a string if the dimension type is a
            string.

            This field is a member of `oneof`_ ``one_value``.
    """

    value: str = proto.Field(
        proto.STRING,
        number=1,
        oneof="one_value",
    )


class RunFunnelReportRequest(proto.Message):
    r"""The request for a funnel report.

    Attributes:
        property (str):
            Optional. A Google Analytics GA4 property identifier whose
            events are tracked. Specified in the URL path and not the
            body. To learn more, see `where to find your Property
            ID <https://developers.google.com/analytics/devguides/reporting/data/v1/property-id>`__.
            Within a batch request, this property should either be
            unspecified or consistent with the batch-level property.

            Example: properties/1234
        date_ranges (MutableSequence[google.analytics.data_v1alpha.types.DateRange]):
            Optional. Date ranges of data to read. If
            multiple date ranges are requested, each
            response row will contain a zero based date
            range index. If two date ranges overlap, the
            event data for the overlapping days is included
            in the response rows for both date ranges.
        funnel (google.analytics.data_v1alpha.types.Funnel):
            Optional. The configuration of this request's
            funnel. This funnel configuration is required.
        funnel_breakdown (google.analytics.data_v1alpha.types.FunnelBreakdown):
            Optional. If specified, this breakdown adds a dimension to
            the funnel table sub report response. This breakdown
            dimension expands each funnel step to the unique values of
            the breakdown dimension. For example, a breakdown by the
            ``deviceCategory`` dimension will create rows for
            ``mobile``, ``tablet``, ``desktop``, and the total.
        funnel_next_action (google.analytics.data_v1alpha.types.FunnelNextAction):
            Optional. If specified, next action adds a dimension to the
            funnel visualization sub report response. This next action
            dimension expands each funnel step to the unique values of
            the next action. For example a next action of the
            ``eventName`` dimension will create rows for several events
            (for example ``session_start`` & ``click``) and the total.

            Next action only supports ``eventName`` and most Page /
            Screen dimensions like ``pageTitle`` and ``pagePath``.
        funnel_visualization_type (google.analytics.data_v1alpha.types.RunFunnelReportRequest.FunnelVisualizationType):
            Optional. The funnel visualization type controls the
            dimensions present in the funnel visualization sub report
            response. If not specified, ``STANDARD_FUNNEL`` is used.
        segments (MutableSequence[google.analytics.data_v1alpha.types.Segment]):
            Optional. The configurations of segments.
            Segments are subsets of a property's data. In a
            funnel report with segments, the funnel is
            evaluated in each segment.

            Each segment specified in this request
            produces a separate row in the response; in the
            response, each segment identified by its name.

            The segments parameter is optional. Requests are
            limited to 4 segments.
        limit (int):
            Optional. The number of rows to return. If unspecified,
            10,000 rows are returned. The API returns a maximum of
            250,000 rows per request, no matter how many you ask for.
            ``limit`` must be positive.

            The API can also return fewer rows than the requested
            ``limit``, if there aren't as many dimension values as the
            ``limit``.
        dimension_filter (google.analytics.data_v1alpha.types.FilterExpression):
            Optional. Dimension filters allow you to ask for only
            specific dimension values in the report. To learn more, see
            `Creating a Report: Dimension
            Filters <https://developers.google.com/analytics/devguides/reporting/data/v1/basics#dimension_filters>`__
            for examples. Metrics cannot be used in this filter.
        return_property_quota (bool):
            Optional. Toggles whether to return the current state of
            this Analytics Property's quota. Quota is returned in
            `PropertyQuota <#PropertyQuota>`__.
    """

    class FunnelVisualizationType(proto.Enum):
        r"""Controls the dimensions present in the funnel visualization
        sub report response.

        Values:
            FUNNEL_VISUALIZATION_TYPE_UNSPECIFIED (0):
                Unspecified type.
            STANDARD_FUNNEL (1):
                A standard (stepped) funnel. The funnel
                visualization sub report in the response will
                not contain date.
            TRENDED_FUNNEL (2):
                A trended (line chart) funnel. The funnel
                visualization sub report in the response will
                contain the date dimension.
        """
        FUNNEL_VISUALIZATION_TYPE_UNSPECIFIED = 0
        STANDARD_FUNNEL = 1
        TRENDED_FUNNEL = 2

    property: str = proto.Field(
        proto.STRING,
        number=1,
    )
    date_ranges: MutableSequence[data.DateRange] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message=data.DateRange,
    )
    funnel: data.Funnel = proto.Field(
        proto.MESSAGE,
        number=3,
        message=data.Funnel,
    )
    funnel_breakdown: data.FunnelBreakdown = proto.Field(
        proto.MESSAGE,
        number=4,
        message=data.FunnelBreakdown,
    )
    funnel_next_action: data.FunnelNextAction = proto.Field(
        proto.MESSAGE,
        number=5,
        message=data.FunnelNextAction,
    )
    funnel_visualization_type: FunnelVisualizationType = proto.Field(
        proto.ENUM,
        number=6,
        enum=FunnelVisualizationType,
    )
    segments: MutableSequence[data.Segment] = proto.RepeatedField(
        proto.MESSAGE,
        number=7,
        message=data.Segment,
    )
    limit: int = proto.Field(
        proto.INT64,
        number=9,
    )
    dimension_filter: data.FilterExpression = proto.Field(
        proto.MESSAGE,
        number=10,
        message=data.FilterExpression,
    )
    return_property_quota: bool = proto.Field(
        proto.BOOL,
        number=12,
    )


class RunFunnelReportResponse(proto.Message):
    r"""The funnel report response contains two sub reports. The two
    sub reports are different combinations of dimensions and
    metrics.

    Attributes:
        funnel_table (google.analytics.data_v1alpha.types.FunnelSubReport):
            The funnel table is a report with the funnel
            step, segment, breakdown dimension, active
            users, completion rate, abandonments, and
            abandonments rate.

            The segment dimension is only present in this
            response if a segment was requested. The
            breakdown dimension is only present in this
            response if it was requested.
        funnel_visualization (google.analytics.data_v1alpha.types.FunnelSubReport):
            The funnel visualization is a report with the funnel step,
            segment, date, next action dimension, and active users.

            The segment dimension is only present in this response if a
            segment was requested. The date dimension is only present in
            this response if it was requested through the
            ``TRENDED_FUNNEL`` funnel type. The next action dimension is
            only present in the response if it was requested.
        property_quota (google.analytics.data_v1alpha.types.PropertyQuota):
            This Analytics Property's quota state
            including this request.
        kind (str):
            Identifies what kind of resource this message is. This
            ``kind`` is always the fixed string
            "analyticsData#runFunnelReport". Useful to distinguish
            between response types in JSON.
    """

    funnel_table: data.FunnelSubReport = proto.Field(
        proto.MESSAGE,
        number=1,
        message=data.FunnelSubReport,
    )
    funnel_visualization: data.FunnelSubReport = proto.Field(
        proto.MESSAGE,
        number=2,
        message=data.FunnelSubReport,
    )
    property_quota: data.PropertyQuota = proto.Field(
        proto.MESSAGE,
        number=3,
        message=data.PropertyQuota,
    )
    kind: str = proto.Field(
        proto.STRING,
        number=4,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
