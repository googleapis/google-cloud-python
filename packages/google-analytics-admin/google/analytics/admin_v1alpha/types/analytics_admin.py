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


from google.analytics.admin_v1alpha.types import resources
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore


__protobuf__ = proto.module(
    package="google.analytics.admin.v1alpha",
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
        "GetUserLinkRequest",
        "BatchGetUserLinksRequest",
        "BatchGetUserLinksResponse",
        "ListUserLinksRequest",
        "ListUserLinksResponse",
        "AuditUserLinksRequest",
        "AuditUserLinksResponse",
        "CreateUserLinkRequest",
        "BatchCreateUserLinksRequest",
        "BatchCreateUserLinksResponse",
        "UpdateUserLinkRequest",
        "BatchUpdateUserLinksRequest",
        "BatchUpdateUserLinksResponse",
        "DeleteUserLinkRequest",
        "BatchDeleteUserLinksRequest",
        "GetWebDataStreamRequest",
        "DeleteWebDataStreamRequest",
        "UpdateWebDataStreamRequest",
        "CreateWebDataStreamRequest",
        "ListWebDataStreamsRequest",
        "ListWebDataStreamsResponse",
        "GetIosAppDataStreamRequest",
        "DeleteIosAppDataStreamRequest",
        "UpdateIosAppDataStreamRequest",
        "CreateIosAppDataStreamRequest",
        "ListIosAppDataStreamsRequest",
        "ListIosAppDataStreamsResponse",
        "GetAndroidAppDataStreamRequest",
        "DeleteAndroidAppDataStreamRequest",
        "UpdateAndroidAppDataStreamRequest",
        "CreateAndroidAppDataStreamRequest",
        "ListAndroidAppDataStreamsRequest",
        "ListAndroidAppDataStreamsResponse",
        "GetEnhancedMeasurementSettingsRequest",
        "UpdateEnhancedMeasurementSettingsRequest",
        "CreateFirebaseLinkRequest",
        "UpdateFirebaseLinkRequest",
        "DeleteFirebaseLinkRequest",
        "ListFirebaseLinksRequest",
        "ListFirebaseLinksResponse",
        "GetGlobalSiteTagRequest",
        "CreateGoogleAdsLinkRequest",
        "UpdateGoogleAdsLinkRequest",
        "DeleteGoogleAdsLinkRequest",
        "ListGoogleAdsLinksRequest",
        "ListGoogleAdsLinksResponse",
        "GetDataSharingSettingsRequest",
        "ListAccountSummariesRequest",
        "ListAccountSummariesResponse",
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

    name = proto.Field(proto.STRING, number=1)


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

    page_size = proto.Field(proto.INT32, number=1)

    page_token = proto.Field(proto.STRING, number=2)

    show_deleted = proto.Field(proto.BOOL, number=3)


class ListAccountsResponse(proto.Message):
    r"""Request message for ListAccounts RPC.

    Attributes:
        accounts (Sequence[google.analytics.admin_v1alpha.types.Account]):
            Results that were accessible to the caller.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    accounts = proto.RepeatedField(proto.MESSAGE, number=1, message=resources.Account,)

    next_page_token = proto.Field(proto.STRING, number=2)


class DeleteAccountRequest(proto.Message):
    r"""Request message for DeleteAccount RPC.

    Attributes:
        name (str):
            Required. The name of the Account to soft-
            elete. Format: accounts/{account}
            Example: "accounts/100".
    """

    name = proto.Field(proto.STRING, number=1)


class UpdateAccountRequest(proto.Message):
    r"""Request message for UpdateAccount RPC.

    Attributes:
        account (google.analytics.admin_v1alpha.types.Account):
            Required. The account to update. The account's ``name``
            field is used to identify the account.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. The list of fields to be updated. Field names must
            be in snake case (e.g., "field_to_update"). Omitted fields
            will not be updated. To replace the entire entity, use one
            path with the string "*" to match all fields.
    """

    account = proto.Field(proto.MESSAGE, number=1, message=resources.Account,)

    update_mask = proto.Field(proto.MESSAGE, number=2, message=field_mask.FieldMask,)


class ProvisionAccountTicketRequest(proto.Message):
    r"""Request message for ProvisionAccountTicket RPC.

    Attributes:
        account (google.analytics.admin_v1alpha.types.Account):
            The account to create.
        redirect_uri (str):
            Redirect URI where the user will be sent
            after accepting Terms of Service. Must be
            configured in Developers Console as a Redirect
            URI
    """

    account = proto.Field(proto.MESSAGE, number=1, message=resources.Account,)

    redirect_uri = proto.Field(proto.STRING, number=2)


class ProvisionAccountTicketResponse(proto.Message):
    r"""Response message for ProvisionAccountTicket RPC.

    Attributes:
        account_ticket_id (str):
            The param to be passed in the ToS link.
    """

    account_ticket_id = proto.Field(proto.STRING, number=1)


class GetPropertyRequest(proto.Message):
    r"""Request message for GetProperty RPC.

    Attributes:
        name (str):
            Required. The name of the property to lookup. Format:
            properties/{property_id} Example: "properties/1000".
    """

    name = proto.Field(proto.STRING, number=1)


class ListPropertiesRequest(proto.Message):
    r"""Request message for ListProperties RPC.

    Attributes:
        filter (str):
            Required. An expression for filtering the results of the
            request. Fields eligible for filtering are:
            ``parent:``\ (The resource name of the parent account) or
            ``firebase_project:``\ (The id or number of the linked
            firebase project). Some examples of filters:

            ::

               | Filter                      | Description                               |
               |-----------------------------|-------------------------------------------|
               | parent:accounts/123         | The account with account id: 123.         |
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

    filter = proto.Field(proto.STRING, number=1)

    page_size = proto.Field(proto.INT32, number=2)

    page_token = proto.Field(proto.STRING, number=3)

    show_deleted = proto.Field(proto.BOOL, number=4)


class ListPropertiesResponse(proto.Message):
    r"""Response message for ListProperties RPC.

    Attributes:
        properties (Sequence[google.analytics.admin_v1alpha.types.Property]):
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
        proto.MESSAGE, number=1, message=resources.Property,
    )

    next_page_token = proto.Field(proto.STRING, number=2)


class UpdatePropertyRequest(proto.Message):
    r"""Request message for UpdateProperty RPC.

    Attributes:
        property (google.analytics.admin_v1alpha.types.Property):
            Required. The property to update. The property's ``name``
            field is used to identify the property to be updated.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. The list of fields to be updated. Field names must
            be in snake case (e.g., "field_to_update"). Omitted fields
            will not be updated. To replace the entire entity, use one
            path with the string "*" to match all fields.
    """

    property = proto.Field(proto.MESSAGE, number=1, message=resources.Property,)

    update_mask = proto.Field(proto.MESSAGE, number=2, message=field_mask.FieldMask,)


class CreatePropertyRequest(proto.Message):
    r"""Request message for CreateProperty RPC.

    Attributes:
        property (google.analytics.admin_v1alpha.types.Property):
            Required. The property to create.
            Note: the supplied property must specify its
            parent.
    """

    property = proto.Field(proto.MESSAGE, number=1, message=resources.Property,)


class DeletePropertyRequest(proto.Message):
    r"""Request message for DeleteProperty RPC.

    Attributes:
        name (str):
            Required. The name of the Property to soft-delete. Format:
            properties/{property_id} Example: "properties/1000".
    """

    name = proto.Field(proto.STRING, number=1)


class GetUserLinkRequest(proto.Message):
    r"""Request message for GetUserLink RPC.

    Attributes:
        name (str):
            Required. Example format:
            accounts/1234/userLinks/5678
    """

    name = proto.Field(proto.STRING, number=1)


class BatchGetUserLinksRequest(proto.Message):
    r"""Request message for BatchGetUserLinks RPC.

    Attributes:
        parent (str):
            Required. The account or property that all
            user links in the request are for. The parent of
            all provided values for the 'names' field must
            match this field.
            Example format: accounts/1234
        names (Sequence[str]):
            Required. The names of the user links to
            retrieve. A maximum of 1000 user links can be
            retrieved in a batch. Format:
            accounts/{accountId}/userLinks/{userLinkId}
    """

    parent = proto.Field(proto.STRING, number=1)

    names = proto.RepeatedField(proto.STRING, number=2)


class BatchGetUserLinksResponse(proto.Message):
    r"""Response message for BatchGetUserLinks RPC.

    Attributes:
        user_links (Sequence[google.analytics.admin_v1alpha.types.UserLink]):
            The requested user links.
    """

    user_links = proto.RepeatedField(
        proto.MESSAGE, number=1, message=resources.UserLink,
    )


class ListUserLinksRequest(proto.Message):
    r"""Request message for ListUserLinks RPC.

    Attributes:
        parent (str):
            Required. Example format: accounts/1234
        page_size (int):
            The maximum number of user links to return.
            The service may return fewer than this value. If
            unspecified, at most 200 user links will be
            returned. The maximum value is 500; values above
            500 will be coerced to 500.
        page_token (str):
            A page token, received from a previous ``ListUserLinks``
            call. Provide this to retrieve the subsequent page. When
            paginating, all other parameters provided to
            ``ListUserLinks`` must match the call that provided the page
            token.
    """

    parent = proto.Field(proto.STRING, number=1)

    page_size = proto.Field(proto.INT32, number=2)

    page_token = proto.Field(proto.STRING, number=3)


class ListUserLinksResponse(proto.Message):
    r"""Response message for ListUserLinks RPC.

    Attributes:
        user_links (Sequence[google.analytics.admin_v1alpha.types.UserLink]):
            List of UserLinks. These will be ordered
            stably, but in an arbitrary order.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    user_links = proto.RepeatedField(
        proto.MESSAGE, number=1, message=resources.UserLink,
    )

    next_page_token = proto.Field(proto.STRING, number=2)


class AuditUserLinksRequest(proto.Message):
    r"""Request message for AuditUserLinks RPC.

    Attributes:
        parent (str):
            Required. Example format: accounts/1234
        page_size (int):
            The maximum number of user links to return.
            The service may return fewer than this value. If
            unspecified, at most 1000 user links will be
            returned. The maximum value is 5000; values
            above 5000 will be coerced to 5000.
        page_token (str):
            A page token, received from a previous ``AuditUserLinks``
            call. Provide this to retrieve the subsequent page. When
            paginating, all other parameters provided to
            ``AuditUserLinks`` must match the call that provided the
            page token.
    """

    parent = proto.Field(proto.STRING, number=1)

    page_size = proto.Field(proto.INT32, number=2)

    page_token = proto.Field(proto.STRING, number=3)


class AuditUserLinksResponse(proto.Message):
    r"""Response message for AuditUserLinks RPC.

    Attributes:
        user_links (Sequence[google.analytics.admin_v1alpha.types.AuditUserLink]):
            List of AuditUserLinks. These will be ordered
            stably, but in an arbitrary order.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    user_links = proto.RepeatedField(
        proto.MESSAGE, number=1, message=resources.AuditUserLink,
    )

    next_page_token = proto.Field(proto.STRING, number=2)


class CreateUserLinkRequest(proto.Message):
    r"""Request message for CreateUserLink RPC.
    Users can have multiple email addresses associated with their
    Google account, and one of these email addresses is the
    "primary" email address. Any of the email addresses associated
    with a Google account may be used for a new UserLink, but the
    returned UserLink will always contain the "primary" email
    address. As a result, the input and output email address for
    this request may differ.

    Attributes:
        parent (str):
            Required. Example format: accounts/1234
        notify_new_user (bool):
            Optional. If set, then email the new user
            notifying them that they've been granted
            permissions to the resource.
        user_link (google.analytics.admin_v1alpha.types.UserLink):
            Required. The user link to create.
    """

    parent = proto.Field(proto.STRING, number=1)

    notify_new_user = proto.Field(proto.BOOL, number=2)

    user_link = proto.Field(proto.MESSAGE, number=3, message=resources.UserLink,)


class BatchCreateUserLinksRequest(proto.Message):
    r"""Request message for BatchCreateUserLinks RPC.

    Attributes:
        parent (str):
            Required. The account or property that all
            user links in the request are for. This field is
            required. The parent field in the
            CreateUserLinkRequest messages must either be
            empty or match this field. Example format:
            accounts/1234
        notify_new_users (bool):
            Optional. If set, then email the new users notifying them
            that they've been granted permissions to the resource.
            Regardless of whether this is set or not, notify_new_user
            field inside each individual request is ignored.
        requests (Sequence[google.analytics.admin_v1alpha.types.CreateUserLinkRequest]):
            Required. The requests specifying the user
            links to create. A maximum of 1000 user links
            can be created in a batch.
    """

    parent = proto.Field(proto.STRING, number=1)

    notify_new_users = proto.Field(proto.BOOL, number=2)

    requests = proto.RepeatedField(
        proto.MESSAGE, number=3, message="CreateUserLinkRequest",
    )


class BatchCreateUserLinksResponse(proto.Message):
    r"""Response message for BatchCreateUserLinks RPC.

    Attributes:
        user_links (Sequence[google.analytics.admin_v1alpha.types.UserLink]):
            The user links created.
    """

    user_links = proto.RepeatedField(
        proto.MESSAGE, number=1, message=resources.UserLink,
    )


class UpdateUserLinkRequest(proto.Message):
    r"""Request message for UpdateUserLink RPC.

    Attributes:
        user_link (google.analytics.admin_v1alpha.types.UserLink):
            Required. The user link to update.
    """

    user_link = proto.Field(proto.MESSAGE, number=1, message=resources.UserLink,)


class BatchUpdateUserLinksRequest(proto.Message):
    r"""Request message for BatchUpdateUserLinks RPC.

    Attributes:
        parent (str):
            Required. The account or property that all
            user links in the request are for. The parent
            field in the UpdateUserLinkRequest messages must
            either be empty or match this field.
            Example format: accounts/1234
        requests (Sequence[google.analytics.admin_v1alpha.types.UpdateUserLinkRequest]):
            Required. The requests specifying the user
            links to update. A maximum of 1000 user links
            can be updated in a batch.
    """

    parent = proto.Field(proto.STRING, number=1)

    requests = proto.RepeatedField(
        proto.MESSAGE, number=2, message="UpdateUserLinkRequest",
    )


class BatchUpdateUserLinksResponse(proto.Message):
    r"""Response message for BatchUpdateUserLinks RPC.

    Attributes:
        user_links (Sequence[google.analytics.admin_v1alpha.types.UserLink]):
            The user links updated.
    """

    user_links = proto.RepeatedField(
        proto.MESSAGE, number=1, message=resources.UserLink,
    )


class DeleteUserLinkRequest(proto.Message):
    r"""Request message for DeleteUserLink RPC.

    Attributes:
        name (str):
            Required. Example format:
            accounts/1234/userLinks/5678
    """

    name = proto.Field(proto.STRING, number=1)


class BatchDeleteUserLinksRequest(proto.Message):
    r"""Request message for BatchDeleteUserLinks RPC.

    Attributes:
        parent (str):
            Required. The account or property that all
            user links in the request are for. The parent of
            all values for user link names to delete must
            match this field.
            Example format: accounts/1234
        requests (Sequence[google.analytics.admin_v1alpha.types.DeleteUserLinkRequest]):
            Required. The requests specifying the user
            links to update. A maximum of 1000 user links
            can be updated in a batch.
    """

    parent = proto.Field(proto.STRING, number=1)

    requests = proto.RepeatedField(
        proto.MESSAGE, number=2, message="DeleteUserLinkRequest",
    )


class GetWebDataStreamRequest(proto.Message):
    r"""Request message for GetWebDataStream RPC.

    Attributes:
        name (str):
            Required. The name of the web data stream to lookup. Format:
            properties/{property_id}/webDataStreams/{stream_id} Example:
            "properties/123/webDataStreams/456".
    """

    name = proto.Field(proto.STRING, number=1)


class DeleteWebDataStreamRequest(proto.Message):
    r"""Request message for DeleteWebDataStream RPC.

    Attributes:
        name (str):
            Required. The name of the web data stream to delete. Format:
            properties/{property_id}/webDataStreams/{stream_id} Example:
            "properties/123/webDataStreams/456".
    """

    name = proto.Field(proto.STRING, number=1)


class UpdateWebDataStreamRequest(proto.Message):
    r"""Request message for UpdateWebDataStream RPC.

    Attributes:
        web_data_stream (google.analytics.admin_v1alpha.types.WebDataStream):
            Required. The web stream to update. The ``name`` field is
            used to identify the web stream to be updated.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. The list of fields to be updated. Field names must
            be in snake case (e.g., "field_to_update"). Omitted fields
            will not be updated. To replace the entire entity, use one
            path with the string "*" to match all fields.
    """

    web_data_stream = proto.Field(
        proto.MESSAGE, number=1, message=resources.WebDataStream,
    )

    update_mask = proto.Field(proto.MESSAGE, number=2, message=field_mask.FieldMask,)


class CreateWebDataStreamRequest(proto.Message):
    r"""Request message for CreateWebDataStream RPC.

    Attributes:
        web_data_stream (google.analytics.admin_v1alpha.types.WebDataStream):
            Required. The web stream to create.
        parent (str):
            Required. The parent resource where this web
            data stream will be created. Format:
            properties/123
    """

    web_data_stream = proto.Field(
        proto.MESSAGE, number=1, message=resources.WebDataStream,
    )

    parent = proto.Field(proto.STRING, number=2)


class ListWebDataStreamsRequest(proto.Message):
    r"""Request message for ListWebDataStreams RPC.

    Attributes:
        parent (str):
            Required. The name of the parent property.
            For example, to list results of web streams
            under the property with Id 123: "properties/123".
        page_size (int):
            The maximum number of resources to return.
            If unspecified, at most 50 resources will be
            returned. The maximum value is 200; (higher
            values will be coerced to the maximum)
        page_token (str):
            A page token, received from a previous
            ``ListWebDataStreams`` call. Provide this to retrieve the
            subsequent page. When paginating, all other parameters
            provided to ``ListWebDataStreams`` must match the call that
            provided the page token.
    """

    parent = proto.Field(proto.STRING, number=1)

    page_size = proto.Field(proto.INT32, number=2)

    page_token = proto.Field(proto.STRING, number=3)


class ListWebDataStreamsResponse(proto.Message):
    r"""Request message for ListWebDataStreams RPC.

    Attributes:
        web_data_streams (Sequence[google.analytics.admin_v1alpha.types.WebDataStream]):
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

    web_data_streams = proto.RepeatedField(
        proto.MESSAGE, number=1, message=resources.WebDataStream,
    )

    next_page_token = proto.Field(proto.STRING, number=2)


class GetIosAppDataStreamRequest(proto.Message):
    r"""Request message for GetIosAppDataStream RPC.

    Attributes:
        name (str):
            Required. The name of the iOS app data stream to lookup.
            Format:
            properties/{property_id}/iosAppDataStreams/{stream_id}
            Example: "properties/123/iosAppDataStreams/456".
    """

    name = proto.Field(proto.STRING, number=1)


class DeleteIosAppDataStreamRequest(proto.Message):
    r"""Request message for DeleteIosAppDataStream RPC.

    Attributes:
        name (str):
            Required. The name of the iOS app data stream to delete.
            Format:
            properties/{property_id}/iosAppDataStreams/{stream_id}
            Example: "properties/123/iosAppDataStreams/456".
    """

    name = proto.Field(proto.STRING, number=1)


class UpdateIosAppDataStreamRequest(proto.Message):
    r"""Request message for UpdateIosAppDataStream RPC.

    Attributes:
        ios_app_data_stream (google.analytics.admin_v1alpha.types.IosAppDataStream):
            Required. The iOS app stream to update. The ``name`` field
            is used to identify the iOS app stream to be updated.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. The list of fields to be updated. Field names must
            be in snake case (e.g., "field_to_update"). Omitted fields
            will not be updated. To replace the entire entity, use one
            path with the string "*" to match all fields.
    """

    ios_app_data_stream = proto.Field(
        proto.MESSAGE, number=1, message=resources.IosAppDataStream,
    )

    update_mask = proto.Field(proto.MESSAGE, number=2, message=field_mask.FieldMask,)


class CreateIosAppDataStreamRequest(proto.Message):
    r"""Request message for CreateIosAppDataStream RPC.

    Attributes:
        ios_app_data_stream (google.analytics.admin_v1alpha.types.IosAppDataStream):
            Required. The iOS app data stream to create.
        parent (str):
            Required. The parent resource where this ios
            app data stream will be created. Format:
            properties/123
    """

    ios_app_data_stream = proto.Field(
        proto.MESSAGE, number=1, message=resources.IosAppDataStream,
    )

    parent = proto.Field(proto.STRING, number=2)


class ListIosAppDataStreamsRequest(proto.Message):
    r"""Request message for ListIosAppDataStreams RPC.

    Attributes:
        parent (str):
            Required. The name of the parent property.
            For example, to list results of app streams
            under the property with Id 123: "properties/123".
        page_size (int):
            The maximum number of resources to return.
            If unspecified, at most 50 resources will be
            returned. The maximum value is 200; (higher
            values will be coerced to the maximum)
        page_token (str):
            A page token, received from a previous
            ``ListIosAppDataStreams`` call. Provide this to retrieve the
            subsequent page. When paginating, all other parameters
            provided to ``ListIosAppDataStreams`` must match the call
            that provided the page token.
    """

    parent = proto.Field(proto.STRING, number=1)

    page_size = proto.Field(proto.INT32, number=2)

    page_token = proto.Field(proto.STRING, number=3)


class ListIosAppDataStreamsResponse(proto.Message):
    r"""Request message for ListIosAppDataStreams RPC.

    Attributes:
        ios_app_data_streams (Sequence[google.analytics.admin_v1alpha.types.IosAppDataStream]):
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

    ios_app_data_streams = proto.RepeatedField(
        proto.MESSAGE, number=1, message=resources.IosAppDataStream,
    )

    next_page_token = proto.Field(proto.STRING, number=2)


class GetAndroidAppDataStreamRequest(proto.Message):
    r"""Request message for GetAndroidAppDataStream RPC.

    Attributes:
        name (str):
            Required. The name of the android app data stream to lookup.
            Format:
            properties/{property_id}/androidAppDataStreams/{stream_id}
            Example: "properties/123/androidAppDataStreams/456".
    """

    name = proto.Field(proto.STRING, number=1)


class DeleteAndroidAppDataStreamRequest(proto.Message):
    r"""Request message for DeleteAndroidAppDataStream RPC.

    Attributes:
        name (str):
            Required. The name of the android app data stream to delete.
            Format:
            properties/{property_id}/androidAppDataStreams/{stream_id}
            Example: "properties/123/androidAppDataStreams/456".
    """

    name = proto.Field(proto.STRING, number=1)


class UpdateAndroidAppDataStreamRequest(proto.Message):
    r"""Request message for UpdateAndroidAppDataStream RPC.

    Attributes:
        android_app_data_stream (google.analytics.admin_v1alpha.types.AndroidAppDataStream):
            Required. The android app stream to update. The ``name``
            field is used to identify the android app stream to be
            updated.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. The list of fields to be updated. Field names must
            be in snake case (e.g., "field_to_update"). Omitted fields
            will not be updated. To replace the entire entity, use one
            path with the string "*" to match all fields.
    """

    android_app_data_stream = proto.Field(
        proto.MESSAGE, number=1, message=resources.AndroidAppDataStream,
    )

    update_mask = proto.Field(proto.MESSAGE, number=2, message=field_mask.FieldMask,)


class CreateAndroidAppDataStreamRequest(proto.Message):
    r"""Request message for CreateAndroidAppDataStream RPC.

    Attributes:
        android_app_data_stream (google.analytics.admin_v1alpha.types.AndroidAppDataStream):
            Required. The android app stream to create.
        parent (str):
            Required. The parent resource where this
            android app data stream will be created. Format:
            properties/123
    """

    android_app_data_stream = proto.Field(
        proto.MESSAGE, number=1, message=resources.AndroidAppDataStream,
    )

    parent = proto.Field(proto.STRING, number=2)


class ListAndroidAppDataStreamsRequest(proto.Message):
    r"""Request message for ListAndroidAppDataStreams RPC.

    Attributes:
        parent (str):
            Required. The name of the parent property.
            For example, to limit results to app streams
            under the property with Id 123: "properties/123".
        page_size (int):
            The maximum number of resources to return.
            If unspecified, at most 50 resources will be
            returned. The maximum value is 200; (higher
            values will be coerced to the maximum)
        page_token (str):
            A page token, received from a previous call. Provide this to
            retrieve the subsequent page. When paginating, all other
            parameters provided to ``ListAndroidAppDataStreams`` must
            match the call that provided the page token.
    """

    parent = proto.Field(proto.STRING, number=1)

    page_size = proto.Field(proto.INT32, number=2)

    page_token = proto.Field(proto.STRING, number=3)


class ListAndroidAppDataStreamsResponse(proto.Message):
    r"""Request message for ListAndroidDataStreams RPC.

    Attributes:
        android_app_data_streams (Sequence[google.analytics.admin_v1alpha.types.AndroidAppDataStream]):
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

    android_app_data_streams = proto.RepeatedField(
        proto.MESSAGE, number=1, message=resources.AndroidAppDataStream,
    )

    next_page_token = proto.Field(proto.STRING, number=2)


class GetEnhancedMeasurementSettingsRequest(proto.Message):
    r"""Request message for GetEnhancedMeasurementSettings RPC.

    Attributes:
        name (str):
            Required. The name of the settings to lookup. Format:
            properties/{property_id}/webDataStreams/{stream_id}/enhancedMeasurementSettings
            Example:
            "properties/1000/webDataStreams/2000/enhancedMeasurementSettings".
    """

    name = proto.Field(proto.STRING, number=1)


class UpdateEnhancedMeasurementSettingsRequest(proto.Message):
    r"""Request message for UpdateEnhancedMeasurementSettings RPC.

    Attributes:
        enhanced_measurement_settings (google.analytics.admin_v1alpha.types.EnhancedMeasurementSettings):
            Required. The settings to update. The ``name`` field is used
            to identify the settings to be updated.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. The list of fields to be updated. Field names must
            be in snake case (e.g., "field_to_update"). Omitted fields
            will not be updated. To replace the entire entity, use one
            path with the string "*" to match all fields.
    """

    enhanced_measurement_settings = proto.Field(
        proto.MESSAGE, number=1, message=resources.EnhancedMeasurementSettings,
    )

    update_mask = proto.Field(proto.MESSAGE, number=2, message=field_mask.FieldMask,)


class CreateFirebaseLinkRequest(proto.Message):
    r"""Request message for CreateFirebaseLink RPC

    Attributes:
        parent (str):
            Required. Format: properties/{property_id} Example:
            properties/1234
        firebase_link (google.analytics.admin_v1alpha.types.FirebaseLink):
            Required. The Firebase link to create.
    """

    parent = proto.Field(proto.STRING, number=1)

    firebase_link = proto.Field(
        proto.MESSAGE, number=2, message=resources.FirebaseLink,
    )


class UpdateFirebaseLinkRequest(proto.Message):
    r"""Request message for UpdateFirebaseLink RPC

    Attributes:
        firebase_link (google.analytics.admin_v1alpha.types.FirebaseLink):
            Required. The Firebase link to update.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. The list of fields to be updated. Field names must
            be in snake case (e.g., "field_to_update"). Omitted fields
            will not be updated. To replace the entire entity, use one
            path with the string "*" to match all fields.
    """

    firebase_link = proto.Field(
        proto.MESSAGE, number=1, message=resources.FirebaseLink,
    )

    update_mask = proto.Field(proto.MESSAGE, number=2, message=field_mask.FieldMask,)


class DeleteFirebaseLinkRequest(proto.Message):
    r"""Request message for DeleteFirebaseLink RPC

    Attributes:
        name (str):
            Required. Format:
            properties/{property_id}/firebaseLinks/{firebase_link_id}
            Example: properties/1234/firebaseLinks/5678
    """

    name = proto.Field(proto.STRING, number=1)


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

    parent = proto.Field(proto.STRING, number=1)

    page_size = proto.Field(proto.INT32, number=2)

    page_token = proto.Field(proto.STRING, number=3)


class ListFirebaseLinksResponse(proto.Message):
    r"""Response message for ListFirebaseLinks RPC

    Attributes:
        firebase_links (Sequence[google.analytics.admin_v1alpha.types.FirebaseLink]):
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
        proto.MESSAGE, number=1, message=resources.FirebaseLink,
    )

    next_page_token = proto.Field(proto.STRING, number=2)


class GetGlobalSiteTagRequest(proto.Message):
    r"""Request message for GetGlobalSiteTag RPC.

    Attributes:
        name (str):
            Required. The name of the site tag to lookup. Note that site
            tags are singletons and do not have unique IDs. Format:
            properties/{property_id}/webDataStreams/{stream_id}/globalSiteTag
            Example: "properties/123/webDataStreams/456/globalSiteTag".
    """

    name = proto.Field(proto.STRING, number=1)


class CreateGoogleAdsLinkRequest(proto.Message):
    r"""Request message for CreateGoogleAdsLink RPC

    Attributes:
        parent (str):
            Required. Example format: properties/1234
        google_ads_link (google.analytics.admin_v1alpha.types.GoogleAdsLink):
            Required. The GoogleAdsLink to create.
    """

    parent = proto.Field(proto.STRING, number=1)

    google_ads_link = proto.Field(
        proto.MESSAGE, number=2, message=resources.GoogleAdsLink,
    )


class UpdateGoogleAdsLinkRequest(proto.Message):
    r"""Request message for UpdateGoogleAdsLink RPC

    Attributes:
        google_ads_link (google.analytics.admin_v1alpha.types.GoogleAdsLink):
            The GoogleAdsLink to update
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. The list of fields to be updated. Field names must
            be in snake case (e.g., "field_to_update"). Omitted fields
            will not be updated. To replace the entire entity, use one
            path with the string "*" to match all fields.
    """

    google_ads_link = proto.Field(
        proto.MESSAGE, number=1, message=resources.GoogleAdsLink,
    )

    update_mask = proto.Field(proto.MESSAGE, number=2, message=field_mask.FieldMask,)


class DeleteGoogleAdsLinkRequest(proto.Message):
    r"""Request message for DeleteGoogleAdsLink RPC.

    Attributes:
        name (str):
            Required. Example format:
            properties/1234/googleAdsLinks/5678
    """

    name = proto.Field(proto.STRING, number=1)


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

    parent = proto.Field(proto.STRING, number=1)

    page_size = proto.Field(proto.INT32, number=2)

    page_token = proto.Field(proto.STRING, number=3)


class ListGoogleAdsLinksResponse(proto.Message):
    r"""Response message for ListGoogleAdsLinks RPC.

    Attributes:
        google_ads_links (Sequence[google.analytics.admin_v1alpha.types.GoogleAdsLink]):
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
        proto.MESSAGE, number=1, message=resources.GoogleAdsLink,
    )

    next_page_token = proto.Field(proto.STRING, number=2)


class GetDataSharingSettingsRequest(proto.Message):
    r"""Request message for GetDataSharingSettings RPC.

    Attributes:
        name (str):
            Required. The name of the settings to lookup.
            Format: accounts/{account}/dataSharingSettings
            Example: "accounts/1000/dataSharingSettings".
    """

    name = proto.Field(proto.STRING, number=1)


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

    page_size = proto.Field(proto.INT32, number=1)

    page_token = proto.Field(proto.STRING, number=2)


class ListAccountSummariesResponse(proto.Message):
    r"""Response message for ListAccountSummaries RPC.

    Attributes:
        account_summaries (Sequence[google.analytics.admin_v1alpha.types.AccountSummary]):
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
        proto.MESSAGE, number=1, message=resources.AccountSummary,
    )

    next_page_token = proto.Field(proto.STRING, number=2)


__all__ = tuple(sorted(__protobuf__.manifest))
