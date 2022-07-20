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
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

from google.analytics.admin_v1beta.types import resources

__protobuf__ = proto.module(
    package="google.analytics.admin.v1beta",
    manifest={
        "GetAccountRequest",
        "ListAccountsRequest",
        "ListAccountsResponse",
        "DeleteAccountRequest",
        "UpdateAccountRequest",
        "ProvisionAccountTicketRequest",
        "ProvisionAccountTicketResponse",
        "GetPropertyRequest",
        "ListPropertiesRequest",
        "ListPropertiesResponse",
        "UpdatePropertyRequest",
        "CreatePropertyRequest",
        "DeletePropertyRequest",
        "CreateFirebaseLinkRequest",
        "DeleteFirebaseLinkRequest",
        "ListFirebaseLinksRequest",
        "ListFirebaseLinksResponse",
        "CreateGoogleAdsLinkRequest",
        "UpdateGoogleAdsLinkRequest",
        "DeleteGoogleAdsLinkRequest",
        "ListGoogleAdsLinksRequest",
        "ListGoogleAdsLinksResponse",
        "GetDataSharingSettingsRequest",
        "ListAccountSummariesRequest",
        "ListAccountSummariesResponse",
        "AcknowledgeUserDataCollectionRequest",
        "AcknowledgeUserDataCollectionResponse",
        "SearchChangeHistoryEventsRequest",
        "SearchChangeHistoryEventsResponse",
        "GetMeasurementProtocolSecretRequest",
        "CreateMeasurementProtocolSecretRequest",
        "DeleteMeasurementProtocolSecretRequest",
        "UpdateMeasurementProtocolSecretRequest",
        "ListMeasurementProtocolSecretsRequest",
        "ListMeasurementProtocolSecretsResponse",
        "CreateConversionEventRequest",
        "GetConversionEventRequest",
        "DeleteConversionEventRequest",
        "ListConversionEventsRequest",
        "ListConversionEventsResponse",
        "CreateCustomDimensionRequest",
        "UpdateCustomDimensionRequest",
        "ListCustomDimensionsRequest",
        "ListCustomDimensionsResponse",
        "ArchiveCustomDimensionRequest",
        "GetCustomDimensionRequest",
        "CreateCustomMetricRequest",
        "UpdateCustomMetricRequest",
        "ListCustomMetricsRequest",
        "ListCustomMetricsResponse",
        "ArchiveCustomMetricRequest",
        "GetCustomMetricRequest",
        "GetDataRetentionSettingsRequest",
        "UpdateDataRetentionSettingsRequest",
        "CreateDataStreamRequest",
        "DeleteDataStreamRequest",
        "UpdateDataStreamRequest",
        "ListDataStreamsRequest",
        "ListDataStreamsResponse",
        "GetDataStreamRequest",
    },
)


class GetAccountRequest(proto.Message):
    r"""Request message for GetAccount RPC.

    Attributes:
        name (str):
            Required. The name of the account to lookup.
            Format: accounts/{account}
            Example: "accounts/100".
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class ListAccountsRequest(proto.Message):
    r"""Request message for ListAccounts RPC.

    Attributes:
        page_size (int):
            The maximum number of resources to return.
            The service may return fewer than this value,
            even if there are additional pages. If
            unspecified, at most 50 resources will be
            returned. The maximum value is 200; (higher
            values will be coerced to the maximum)
        page_token (str):
            A page token, received from a previous ``ListAccounts``
            call. Provide this to retrieve the subsequent page. When
            paginating, all other parameters provided to
            ``ListAccounts`` must match the call that provided the page
            token.
        show_deleted (bool):
            Whether to include soft-deleted (ie:
            "trashed") Accounts in the results. Accounts can
            be inspected to determine whether they are
            deleted or not.
    """

    page_size = proto.Field(
        proto.INT32,
        number=1,
    )
    page_token = proto.Field(
        proto.STRING,
        number=2,
    )
    show_deleted = proto.Field(
        proto.BOOL,
        number=3,
    )


class ListAccountsResponse(proto.Message):
    r"""Request message for ListAccounts RPC.

    Attributes:
        accounts (Sequence[google.analytics.admin_v1beta.types.Account]):
            Results that were accessible to the caller.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    accounts = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=resources.Account,
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )


class DeleteAccountRequest(proto.Message):
    r"""Request message for DeleteAccount RPC.

    Attributes:
        name (str):
            Required. The name of the Account to
            soft-delete. Format: accounts/{account}
            Example: "accounts/100".
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class UpdateAccountRequest(proto.Message):
    r"""Request message for UpdateAccount RPC.

    Attributes:
        account (google.analytics.admin_v1beta.types.Account):
            Required. The account to update. The account's ``name``
            field is used to identify the account.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. The list of fields to be updated. Field names must
            be in snake case (e.g., "field_to_update"). Omitted fields
            will not be updated. To replace the entire entity, use one
            path with the string "*" to match all fields.
    """

    account = proto.Field(
        proto.MESSAGE,
        number=1,
        message=resources.Account,
    )
    update_mask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class ProvisionAccountTicketRequest(proto.Message):
    r"""Request message for ProvisionAccountTicket RPC.

    Attributes:
        account (google.analytics.admin_v1beta.types.Account):
            The account to create.
        redirect_uri (str):
            Redirect URI where the user will be sent
            after accepting Terms of Service. Must be
            configured in Developers Console as a Redirect
            URI
    """

    account = proto.Field(
        proto.MESSAGE,
        number=1,
        message=resources.Account,
    )
    redirect_uri = proto.Field(
        proto.STRING,
        number=2,
    )


class ProvisionAccountTicketResponse(proto.Message):
    r"""Response message for ProvisionAccountTicket RPC.

    Attributes:
        account_ticket_id (str):
            The param to be passed in the ToS link.
    """

    account_ticket_id = proto.Field(
        proto.STRING,
        number=1,
    )


class GetPropertyRequest(proto.Message):
    r"""Request message for GetProperty RPC.

    Attributes:
        name (str):
            Required. The name of the property to lookup. Format:
            properties/{property_id} Example: "properties/1000".
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class ListPropertiesRequest(proto.Message):
    r"""Request message for ListProperties RPC.

    Attributes:
        filter (str):
            Required. An expression for filtering the results of the
            request. Fields eligible for filtering are:
            ``parent:``\ (The resource name of the parent
            account/property) or ``ancestor:``\ (The resource name of
            the parent account) or ``firebase_project:``\ (The id or
            number of the linked firebase project). Some examples of
            filters:

            ::

               | Filter                      | Description                               |
               |-----------------------------|-------------------------------------------|
               | parent:accounts/123         | The account with account id: 123.       |
               | parent:properties/123       | The property with property id: 123.       |
               | ancestor:accounts/123       | The account with account id: 123.         |
               | firebase_project:project-id | The firebase project with id: project-id. |
               | firebase_project:123        | The firebase project with number: 123.    |
        page_size (int):
            The maximum number of resources to return.
            The service may return fewer than this value,
            even if there are additional pages. If
            unspecified, at most 50 resources will be
            returned. The maximum value is 200; (higher
            values will be coerced to the maximum)
        page_token (str):
            A page token, received from a previous ``ListProperties``
            call. Provide this to retrieve the subsequent page. When
            paginating, all other parameters provided to
            ``ListProperties`` must match the call that provided the
            page token.
        show_deleted (bool):
            Whether to include soft-deleted (ie:
            "trashed") Properties in the results. Properties
            can be inspected to determine whether they are
            deleted or not.
    """

    filter = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token = proto.Field(
        proto.STRING,
        number=3,
    )
    show_deleted = proto.Field(
        proto.BOOL,
        number=4,
    )


class ListPropertiesResponse(proto.Message):
    r"""Response message for ListProperties RPC.

    Attributes:
        properties (Sequence[google.analytics.admin_v1beta.types.Property]):
            Results that matched the filter criteria and
            were accessible to the caller.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    properties = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=resources.Property,
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )


class UpdatePropertyRequest(proto.Message):
    r"""Request message for UpdateProperty RPC.

    Attributes:
        property (google.analytics.admin_v1beta.types.Property):
            Required. The property to update. The property's ``name``
            field is used to identify the property to be updated.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. The list of fields to be updated. Field names must
            be in snake case (e.g., "field_to_update"). Omitted fields
            will not be updated. To replace the entire entity, use one
            path with the string "*" to match all fields.
    """

    property = proto.Field(
        proto.MESSAGE,
        number=1,
        message=resources.Property,
    )
    update_mask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class CreatePropertyRequest(proto.Message):
    r"""Request message for CreateProperty RPC.

    Attributes:
        property (google.analytics.admin_v1beta.types.Property):
            Required. The property to create.
            Note: the supplied property must specify its
            parent.
    """

    property = proto.Field(
        proto.MESSAGE,
        number=1,
        message=resources.Property,
    )


class DeletePropertyRequest(proto.Message):
    r"""Request message for DeleteProperty RPC.

    Attributes:
        name (str):
            Required. The name of the Property to soft-delete. Format:
            properties/{property_id} Example: "properties/1000".
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateFirebaseLinkRequest(proto.Message):
    r"""Request message for CreateFirebaseLink RPC

    Attributes:
        parent (str):
            Required. Format: properties/{property_id} Example:
            properties/1234
        firebase_link (google.analytics.admin_v1beta.types.FirebaseLink):
            Required. The Firebase link to create.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    firebase_link = proto.Field(
        proto.MESSAGE,
        number=2,
        message=resources.FirebaseLink,
    )


class DeleteFirebaseLinkRequest(proto.Message):
    r"""Request message for DeleteFirebaseLink RPC

    Attributes:
        name (str):
            Required. Format:
            properties/{property_id}/firebaseLinks/{firebase_link_id}
            Example: properties/1234/firebaseLinks/5678
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class ListFirebaseLinksRequest(proto.Message):
    r"""Request message for ListFirebaseLinks RPC

    Attributes:
        parent (str):
            Required. Format: properties/{property_id} Example:
            properties/1234
        page_size (int):
            The maximum number of resources to return.
            The service may return fewer than this value,
            even if there are additional pages. If
            unspecified, at most 50 resources will be
            returned. The maximum value is 200; (higher
            values will be coerced to the maximum)
        page_token (str):
            A page token, received from a previous ``ListFirebaseLinks``
            call. Provide this to retrieve the subsequent page. When
            paginating, all other parameters provided to
            ``ListProperties`` must match the call that provided the
            page token.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token = proto.Field(
        proto.STRING,
        number=3,
    )


class ListFirebaseLinksResponse(proto.Message):
    r"""Response message for ListFirebaseLinks RPC

    Attributes:
        firebase_links (Sequence[google.analytics.admin_v1beta.types.FirebaseLink]):
            List of FirebaseLinks. This will have at most
            one value.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages. Currently, Google Analytics supports only one
            FirebaseLink per property, so this will never be populated.
    """

    @property
    def raw_page(self):
        return self

    firebase_links = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=resources.FirebaseLink,
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )


class CreateGoogleAdsLinkRequest(proto.Message):
    r"""Request message for CreateGoogleAdsLink RPC

    Attributes:
        parent (str):
            Required. Example format: properties/1234
        google_ads_link (google.analytics.admin_v1beta.types.GoogleAdsLink):
            Required. The GoogleAdsLink to create.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    google_ads_link = proto.Field(
        proto.MESSAGE,
        number=2,
        message=resources.GoogleAdsLink,
    )


class UpdateGoogleAdsLinkRequest(proto.Message):
    r"""Request message for UpdateGoogleAdsLink RPC

    Attributes:
        google_ads_link (google.analytics.admin_v1beta.types.GoogleAdsLink):
            The GoogleAdsLink to update
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. The list of fields to be updated. Field names must
            be in snake case (e.g., "field_to_update"). Omitted fields
            will not be updated. To replace the entire entity, use one
            path with the string "*" to match all fields.
    """

    google_ads_link = proto.Field(
        proto.MESSAGE,
        number=1,
        message=resources.GoogleAdsLink,
    )
    update_mask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class DeleteGoogleAdsLinkRequest(proto.Message):
    r"""Request message for DeleteGoogleAdsLink RPC.

    Attributes:
        name (str):
            Required. Example format:
            properties/1234/googleAdsLinks/5678
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class ListGoogleAdsLinksRequest(proto.Message):
    r"""Request message for ListGoogleAdsLinks RPC.

    Attributes:
        parent (str):
            Required. Example format: properties/1234
        page_size (int):
            The maximum number of resources to return.
            If unspecified, at most 50 resources will be
            returned. The maximum value is 200 (higher
            values will be coerced to the maximum).
        page_token (str):
            A page token, received from a previous
            ``ListGoogleAdsLinks`` call. Provide this to retrieve the
            subsequent page.

            When paginating, all other parameters provided to
            ``ListGoogleAdsLinks`` must match the call that provided the
            page token.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token = proto.Field(
        proto.STRING,
        number=3,
    )


class ListGoogleAdsLinksResponse(proto.Message):
    r"""Response message for ListGoogleAdsLinks RPC.

    Attributes:
        google_ads_links (Sequence[google.analytics.admin_v1beta.types.GoogleAdsLink]):
            List of GoogleAdsLinks.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    google_ads_links = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=resources.GoogleAdsLink,
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )


class GetDataSharingSettingsRequest(proto.Message):
    r"""Request message for GetDataSharingSettings RPC.

    Attributes:
        name (str):
            Required. The name of the settings to lookup.
            Format: accounts/{account}/dataSharingSettings
            Example: "accounts/1000/dataSharingSettings".
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class ListAccountSummariesRequest(proto.Message):
    r"""Request message for ListAccountSummaries RPC.

    Attributes:
        page_size (int):
            The maximum number of AccountSummary
            resources to return. The service may return
            fewer than this value, even if there are
            additional pages. If unspecified, at most 50
            resources will be returned. The maximum value is
            200; (higher values will be coerced to the
            maximum)
        page_token (str):
            A page token, received from a previous
            ``ListAccountSummaries`` call. Provide this to retrieve the
            subsequent page. When paginating, all other parameters
            provided to ``ListAccountSummaries`` must match the call
            that provided the page token.
    """

    page_size = proto.Field(
        proto.INT32,
        number=1,
    )
    page_token = proto.Field(
        proto.STRING,
        number=2,
    )


class ListAccountSummariesResponse(proto.Message):
    r"""Response message for ListAccountSummaries RPC.

    Attributes:
        account_summaries (Sequence[google.analytics.admin_v1beta.types.AccountSummary]):
            Account summaries of all accounts the caller
            has access to.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    account_summaries = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=resources.AccountSummary,
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )


class AcknowledgeUserDataCollectionRequest(proto.Message):
    r"""Request message for AcknowledgeUserDataCollection RPC.

    Attributes:
        property (str):
            Required. The property for which to
            acknowledge user data collection.
        acknowledgement (str):
            Required. An acknowledgement that the caller
            of this method understands the terms of user
            data collection.
            This field must contain the exact value:
            "I acknowledge that I have the necessary privacy
            disclosures and rights from my end users for the
            collection and processing of their data,
            including the association of such data with the
            visitation information Google Analytics collects
            from my site and/or app property.".
    """

    property = proto.Field(
        proto.STRING,
        number=1,
    )
    acknowledgement = proto.Field(
        proto.STRING,
        number=2,
    )


class AcknowledgeUserDataCollectionResponse(proto.Message):
    r"""Response message for AcknowledgeUserDataCollection RPC."""


class SearchChangeHistoryEventsRequest(proto.Message):
    r"""Request message for SearchChangeHistoryEvents RPC.

    Attributes:
        account (str):
            Required. The account resource for which to
            return change history resources.
        property (str):
            Optional. Resource name for a child property.
            If set, only return changes made to this
            property or its child resources.
        resource_type (Sequence[google.analytics.admin_v1beta.types.ChangeHistoryResourceType]):
            Optional. If set, only return changes if they
            are for a resource that matches at least one of
            these types.
        action (Sequence[google.analytics.admin_v1beta.types.ActionType]):
            Optional. If set, only return changes that
            match one or more of these types of actions.
        actor_email (Sequence[str]):
            Optional. If set, only return changes if they
            are made by a user in this list.
        earliest_change_time (google.protobuf.timestamp_pb2.Timestamp):
            Optional. If set, only return changes made
            after this time (inclusive).
        latest_change_time (google.protobuf.timestamp_pb2.Timestamp):
            Optional. If set, only return changes made
            before this time (inclusive).
        page_size (int):
            Optional. The maximum number of
            ChangeHistoryEvent items to return. The service
            may return fewer than this value, even if there
            are additional pages. If unspecified, at most 50
            items will be returned. The maximum value is 200
            (higher values will be coerced to the maximum).
        page_token (str):
            Optional. A page token, received from a previous
            ``SearchChangeHistoryEvents`` call. Provide this to retrieve
            the subsequent page. When paginating, all other parameters
            provided to ``SearchChangeHistoryEvents`` must match the
            call that provided the page token.
    """

    account = proto.Field(
        proto.STRING,
        number=1,
    )
    property = proto.Field(
        proto.STRING,
        number=2,
    )
    resource_type = proto.RepeatedField(
        proto.ENUM,
        number=3,
        enum=resources.ChangeHistoryResourceType,
    )
    action = proto.RepeatedField(
        proto.ENUM,
        number=4,
        enum=resources.ActionType,
    )
    actor_email = proto.RepeatedField(
        proto.STRING,
        number=5,
    )
    earliest_change_time = proto.Field(
        proto.MESSAGE,
        number=6,
        message=timestamp_pb2.Timestamp,
    )
    latest_change_time = proto.Field(
        proto.MESSAGE,
        number=7,
        message=timestamp_pb2.Timestamp,
    )
    page_size = proto.Field(
        proto.INT32,
        number=8,
    )
    page_token = proto.Field(
        proto.STRING,
        number=9,
    )


class SearchChangeHistoryEventsResponse(proto.Message):
    r"""Response message for SearchAccounts RPC.

    Attributes:
        change_history_events (Sequence[google.analytics.admin_v1beta.types.ChangeHistoryEvent]):
            Results that were accessible to the caller.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    change_history_events = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=resources.ChangeHistoryEvent,
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )


class GetMeasurementProtocolSecretRequest(proto.Message):
    r"""Request message for GetMeasurementProtocolSecret RPC.

    Attributes:
        name (str):
            Required. The name of the measurement
            protocol secret to lookup. Format:
            properties/{property}/dataStreams/{dataStream}/measurementProtocolSecrets/{measurementProtocolSecret}
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateMeasurementProtocolSecretRequest(proto.Message):
    r"""Request message for CreateMeasurementProtocolSecret RPC

    Attributes:
        parent (str):
            Required. The parent resource where this
            secret will be created. Format:
            properties/{property}/dataStreams/{dataStream}
        measurement_protocol_secret (google.analytics.admin_v1beta.types.MeasurementProtocolSecret):
            Required. The measurement protocol secret to
            create.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    measurement_protocol_secret = proto.Field(
        proto.MESSAGE,
        number=2,
        message=resources.MeasurementProtocolSecret,
    )


class DeleteMeasurementProtocolSecretRequest(proto.Message):
    r"""Request message for DeleteMeasurementProtocolSecret RPC

    Attributes:
        name (str):
            Required. The name of the
            MeasurementProtocolSecret to delete. Format:
            properties/{property}/dataStreams/{dataStream}/measurementProtocolSecrets/{measurementProtocolSecret}
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class UpdateMeasurementProtocolSecretRequest(proto.Message):
    r"""Request message for UpdateMeasurementProtocolSecret RPC

    Attributes:
        measurement_protocol_secret (google.analytics.admin_v1beta.types.MeasurementProtocolSecret):
            Required. The measurement protocol secret to
            update.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            The list of fields to be updated. Omitted
            fields will not be updated.
    """

    measurement_protocol_secret = proto.Field(
        proto.MESSAGE,
        number=1,
        message=resources.MeasurementProtocolSecret,
    )
    update_mask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class ListMeasurementProtocolSecretsRequest(proto.Message):
    r"""Request message for ListMeasurementProtocolSecret RPC

    Attributes:
        parent (str):
            Required. The resource name of the parent
            stream. Format:
            properties/{property}/dataStreams/{dataStream}/measurementProtocolSecrets
        page_size (int):
            The maximum number of resources to return.
            If unspecified, at most 10 resources will be
            returned. The maximum value is 10. Higher values
            will be coerced to the maximum.
        page_token (str):
            A page token, received from a previous
            ``ListMeasurementProtocolSecrets`` call. Provide this to
            retrieve the subsequent page. When paginating, all other
            parameters provided to ``ListMeasurementProtocolSecrets``
            must match the call that provided the page token.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token = proto.Field(
        proto.STRING,
        number=3,
    )


class ListMeasurementProtocolSecretsResponse(proto.Message):
    r"""Response message for ListMeasurementProtocolSecret RPC

    Attributes:
        measurement_protocol_secrets (Sequence[google.analytics.admin_v1beta.types.MeasurementProtocolSecret]):
            A list of secrets for the parent stream
            specified in the request.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    measurement_protocol_secrets = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=resources.MeasurementProtocolSecret,
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )


class CreateConversionEventRequest(proto.Message):
    r"""Request message for CreateConversionEvent RPC

    Attributes:
        conversion_event (google.analytics.admin_v1beta.types.ConversionEvent):
            Required. The conversion event to create.
        parent (str):
            Required. The resource name of the parent
            property where this conversion event will be
            created. Format: properties/123
    """

    conversion_event = proto.Field(
        proto.MESSAGE,
        number=1,
        message=resources.ConversionEvent,
    )
    parent = proto.Field(
        proto.STRING,
        number=2,
    )


class GetConversionEventRequest(proto.Message):
    r"""Request message for GetConversionEvent RPC

    Attributes:
        name (str):
            Required. The resource name of the conversion event to
            retrieve. Format:
            properties/{property}/conversionEvents/{conversion_event}
            Example: "properties/123/conversionEvents/456".
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class DeleteConversionEventRequest(proto.Message):
    r"""Request message for DeleteConversionEvent RPC

    Attributes:
        name (str):
            Required. The resource name of the conversion event to
            delete. Format:
            properties/{property}/conversionEvents/{conversion_event}
            Example: "properties/123/conversionEvents/456".
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class ListConversionEventsRequest(proto.Message):
    r"""Request message for ListConversionEvents RPC

    Attributes:
        parent (str):
            Required. The resource name of the parent
            property. Example: 'properties/123'
        page_size (int):
            The maximum number of resources to return.
            If unspecified, at most 50 resources will be
            returned. The maximum value is 200; (higher
            values will be coerced to the maximum)
        page_token (str):
            A page token, received from a previous
            ``ListConversionEvents`` call. Provide this to retrieve the
            subsequent page. When paginating, all other parameters
            provided to ``ListConversionEvents`` must match the call
            that provided the page token.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token = proto.Field(
        proto.STRING,
        number=3,
    )


class ListConversionEventsResponse(proto.Message):
    r"""Response message for ListConversionEvents RPC.

    Attributes:
        conversion_events (Sequence[google.analytics.admin_v1beta.types.ConversionEvent]):
            The requested conversion events
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    conversion_events = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=resources.ConversionEvent,
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )


class CreateCustomDimensionRequest(proto.Message):
    r"""Request message for CreateCustomDimension RPC.

    Attributes:
        parent (str):
            Required. Example format: properties/1234
        custom_dimension (google.analytics.admin_v1beta.types.CustomDimension):
            Required. The CustomDimension to create.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    custom_dimension = proto.Field(
        proto.MESSAGE,
        number=2,
        message=resources.CustomDimension,
    )


class UpdateCustomDimensionRequest(proto.Message):
    r"""Request message for UpdateCustomDimension RPC.

    Attributes:
        custom_dimension (google.analytics.admin_v1beta.types.CustomDimension):
            The CustomDimension to update
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. The list of fields to be updated. Omitted fields
            will not be updated. To replace the entire entity, use one
            path with the string "*" to match all fields.
    """

    custom_dimension = proto.Field(
        proto.MESSAGE,
        number=1,
        message=resources.CustomDimension,
    )
    update_mask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class ListCustomDimensionsRequest(proto.Message):
    r"""Request message for ListCustomDimensions RPC.

    Attributes:
        parent (str):
            Required. Example format: properties/1234
        page_size (int):
            The maximum number of resources to return.
            If unspecified, at most 50 resources will be
            returned. The maximum value is 200 (higher
            values will be coerced to the maximum).
        page_token (str):
            A page token, received from a previous
            ``ListCustomDimensions`` call. Provide this to retrieve the
            subsequent page.

            When paginating, all other parameters provided to
            ``ListCustomDimensions`` must match the call that provided
            the page token.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token = proto.Field(
        proto.STRING,
        number=3,
    )


class ListCustomDimensionsResponse(proto.Message):
    r"""Response message for ListCustomDimensions RPC.

    Attributes:
        custom_dimensions (Sequence[google.analytics.admin_v1beta.types.CustomDimension]):
            List of CustomDimensions.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    custom_dimensions = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=resources.CustomDimension,
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )


class ArchiveCustomDimensionRequest(proto.Message):
    r"""Request message for ArchiveCustomDimension RPC.

    Attributes:
        name (str):
            Required. The name of the CustomDimension to
            archive. Example format:
            properties/1234/customDimensions/5678
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class GetCustomDimensionRequest(proto.Message):
    r"""Request message for GetCustomDimension RPC.

    Attributes:
        name (str):
            Required. The name of the CustomDimension to
            get. Example format:
            properties/1234/customDimensions/5678
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateCustomMetricRequest(proto.Message):
    r"""Request message for CreateCustomMetric RPC.

    Attributes:
        parent (str):
            Required. Example format: properties/1234
        custom_metric (google.analytics.admin_v1beta.types.CustomMetric):
            Required. The CustomMetric to create.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    custom_metric = proto.Field(
        proto.MESSAGE,
        number=2,
        message=resources.CustomMetric,
    )


class UpdateCustomMetricRequest(proto.Message):
    r"""Request message for UpdateCustomMetric RPC.

    Attributes:
        custom_metric (google.analytics.admin_v1beta.types.CustomMetric):
            The CustomMetric to update
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. The list of fields to be updated. Omitted fields
            will not be updated. To replace the entire entity, use one
            path with the string "*" to match all fields.
    """

    custom_metric = proto.Field(
        proto.MESSAGE,
        number=1,
        message=resources.CustomMetric,
    )
    update_mask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class ListCustomMetricsRequest(proto.Message):
    r"""Request message for ListCustomMetrics RPC.

    Attributes:
        parent (str):
            Required. Example format: properties/1234
        page_size (int):
            The maximum number of resources to return.
            If unspecified, at most 50 resources will be
            returned. The maximum value is 200 (higher
            values will be coerced to the maximum).
        page_token (str):
            A page token, received from a previous ``ListCustomMetrics``
            call. Provide this to retrieve the subsequent page.

            When paginating, all other parameters provided to
            ``ListCustomMetrics`` must match the call that provided the
            page token.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token = proto.Field(
        proto.STRING,
        number=3,
    )


class ListCustomMetricsResponse(proto.Message):
    r"""Response message for ListCustomMetrics RPC.

    Attributes:
        custom_metrics (Sequence[google.analytics.admin_v1beta.types.CustomMetric]):
            List of CustomMetrics.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    custom_metrics = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=resources.CustomMetric,
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )


class ArchiveCustomMetricRequest(proto.Message):
    r"""Request message for ArchiveCustomMetric RPC.

    Attributes:
        name (str):
            Required. The name of the CustomMetric to
            archive. Example format:
            properties/1234/customMetrics/5678
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class GetCustomMetricRequest(proto.Message):
    r"""Request message for GetCustomMetric RPC.

    Attributes:
        name (str):
            Required. The name of the CustomMetric to
            get. Example format:
            properties/1234/customMetrics/5678
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class GetDataRetentionSettingsRequest(proto.Message):
    r"""Request message for GetDataRetentionSettings RPC.

    Attributes:
        name (str):
            Required. The name of the settings to lookup.
            Format:
            properties/{property}/dataRetentionSettings
            Example: "properties/1000/dataRetentionSettings".
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class UpdateDataRetentionSettingsRequest(proto.Message):
    r"""Request message for UpdateDataRetentionSettings RPC.

    Attributes:
        data_retention_settings (google.analytics.admin_v1beta.types.DataRetentionSettings):
            Required. The settings to update. The ``name`` field is used
            to identify the settings to be updated.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. The list of fields to be updated. Field names must
            be in snake case (e.g., "field_to_update"). Omitted fields
            will not be updated. To replace the entire entity, use one
            path with the string "*" to match all fields.
    """

    data_retention_settings = proto.Field(
        proto.MESSAGE,
        number=1,
        message=resources.DataRetentionSettings,
    )
    update_mask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class CreateDataStreamRequest(proto.Message):
    r"""Request message for CreateDataStream RPC.

    Attributes:
        parent (str):
            Required. Example format: properties/1234
        data_stream (google.analytics.admin_v1beta.types.DataStream):
            Required. The DataStream to create.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    data_stream = proto.Field(
        proto.MESSAGE,
        number=2,
        message=resources.DataStream,
    )


class DeleteDataStreamRequest(proto.Message):
    r"""Request message for DeleteDataStream RPC.

    Attributes:
        name (str):
            Required. The name of the DataStream to
            delete. Example format:
            properties/1234/dataStreams/5678
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class UpdateDataStreamRequest(proto.Message):
    r"""Request message for UpdateDataStream RPC.

    Attributes:
        data_stream (google.analytics.admin_v1beta.types.DataStream):
            The DataStream to update
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. The list of fields to be updated. Omitted fields
            will not be updated. To replace the entire entity, use one
            path with the string "*" to match all fields.
    """

    data_stream = proto.Field(
        proto.MESSAGE,
        number=1,
        message=resources.DataStream,
    )
    update_mask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class ListDataStreamsRequest(proto.Message):
    r"""Request message for ListDataStreams RPC.

    Attributes:
        parent (str):
            Required. Example format: properties/1234
        page_size (int):
            The maximum number of resources to return.
            If unspecified, at most 50 resources will be
            returned. The maximum value is 200 (higher
            values will be coerced to the maximum).
        page_token (str):
            A page token, received from a previous ``ListDataStreams``
            call. Provide this to retrieve the subsequent page.

            When paginating, all other parameters provided to
            ``ListDataStreams`` must match the call that provided the
            page token.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token = proto.Field(
        proto.STRING,
        number=3,
    )


class ListDataStreamsResponse(proto.Message):
    r"""Response message for ListDataStreams RPC.

    Attributes:
        data_streams (Sequence[google.analytics.admin_v1beta.types.DataStream]):
            List of DataStreams.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    data_streams = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=resources.DataStream,
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )


class GetDataStreamRequest(proto.Message):
    r"""Request message for GetDataStream RPC.

    Attributes:
        name (str):
            Required. The name of the DataStream to get.
            Example format: properties/1234/dataStreams/5678
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
