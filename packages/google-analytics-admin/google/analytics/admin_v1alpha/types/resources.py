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

from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.analytics.admin.v1alpha",
    manifest={
        "MaximumUserAccess",
        "IndustryCategory",
        "ActorType",
        "ActionType",
        "ChangeHistoryResourceType",
        "GoogleSignalsState",
        "GoogleSignalsConsent",
        "Account",
        "Property",
        "AndroidAppDataStream",
        "IosAppDataStream",
        "WebDataStream",
        "UserLink",
        "AuditUserLink",
        "EnhancedMeasurementSettings",
        "FirebaseLink",
        "GlobalSiteTag",
        "GoogleAdsLink",
        "DataSharingSettings",
        "AccountSummary",
        "PropertySummary",
        "MeasurementProtocolSecret",
        "ChangeHistoryEvent",
        "ChangeHistoryChange",
        "ConversionEvent",
        "GoogleSignalsSettings",
        "CustomDimension",
        "CustomMetric",
    },
)


class MaximumUserAccess(proto.Enum):
    r"""Maximum access settings that Firebase user receive on the
    linked Analytics property.
    """
    MAXIMUM_USER_ACCESS_UNSPECIFIED = 0
    NO_ACCESS = 1
    READ_AND_ANALYZE = 2
    EDITOR_WITHOUT_LINK_MANAGEMENT = 3
    EDITOR_INCLUDING_LINK_MANAGEMENT = 4


class IndustryCategory(proto.Enum):
    r"""The category selected for this property, used for industry
    benchmarking.
    """
    INDUSTRY_CATEGORY_UNSPECIFIED = 0
    AUTOMOTIVE = 1
    BUSINESS_AND_INDUSTRIAL_MARKETS = 2
    FINANCE = 3
    HEALTHCARE = 4
    TECHNOLOGY = 5
    TRAVEL = 6
    OTHER = 7
    ARTS_AND_ENTERTAINMENT = 8
    BEAUTY_AND_FITNESS = 9
    BOOKS_AND_LITERATURE = 10
    FOOD_AND_DRINK = 11
    GAMES = 12
    HOBBIES_AND_LEISURE = 13
    HOME_AND_GARDEN = 14
    INTERNET_AND_TELECOM = 15
    LAW_AND_GOVERNMENT = 16
    NEWS = 17
    ONLINE_COMMUNITIES = 18
    PEOPLE_AND_SOCIETY = 19
    PETS_AND_ANIMALS = 20
    REAL_ESTATE = 21
    REFERENCE = 22
    SCIENCE = 23
    SPORTS = 24
    JOBS_AND_EDUCATION = 25
    SHOPPING = 26


class ActorType(proto.Enum):
    r"""Different kinds of actors that can make changes to Google
    Analytics resources.
    """
    ACTOR_TYPE_UNSPECIFIED = 0
    USER = 1
    SYSTEM = 2
    SUPPORT = 3


class ActionType(proto.Enum):
    r"""Types of actions that may change a resource."""
    ACTION_TYPE_UNSPECIFIED = 0
    CREATED = 1
    UPDATED = 2
    DELETED = 3


class ChangeHistoryResourceType(proto.Enum):
    r"""Types of resources whose changes may be returned from change
    history.
    """
    CHANGE_HISTORY_RESOURCE_TYPE_UNSPECIFIED = 0
    ACCOUNT = 1
    PROPERTY = 2
    WEB_DATA_STREAM = 3
    ANDROID_APP_DATA_STREAM = 4
    IOS_APP_DATA_STREAM = 5
    FIREBASE_LINK = 6
    GOOGLE_ADS_LINK = 7
    GOOGLE_SIGNALS_SETTINGS = 8
    CONVERSION_EVENT = 9
    MEASUREMENT_PROTOCOL_SECRET = 10
    CUSTOM_DIMENSION = 11
    CUSTOM_METRIC = 12


class GoogleSignalsState(proto.Enum):
    r"""Status of the Google Signals settings (i.e., whether this
    feature has been enabled for the property).
    """
    GOOGLE_SIGNALS_STATE_UNSPECIFIED = 0
    GOOGLE_SIGNALS_ENABLED = 1
    GOOGLE_SIGNALS_DISABLED = 2


class GoogleSignalsConsent(proto.Enum):
    r"""Consent field of the Google Signals settings (i.e., whether
    the user has consented to the Google Signals terms of service.)
    """
    GOOGLE_SIGNALS_CONSENT_UNSPECIFIED = 0
    GOOGLE_SIGNALS_CONSENT_CONSENTED = 2
    GOOGLE_SIGNALS_CONSENT_NOT_CONSENTED = 1


class Account(proto.Message):
    r"""A resource message representing a Google Analytics account.
    Attributes:
        name (str):
            Output only. Resource name of this account.
            Format: accounts/{account}
            Example: "accounts/100".
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when this account was
            originally created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when account payload fields
            were last updated.
        display_name (str):
            Required. Human-readable display name for
            this account.
        region_code (str):
            Country of business. Must be a Unicode CLDR
            region code.
        deleted (bool):
            Output only. Indicates whether this Account
            is soft-deleted or not. Deleted accounts are
            excluded from List results unless specifically
            requested.
    """

    name = proto.Field(proto.STRING, number=1,)
    create_time = proto.Field(proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,)
    update_time = proto.Field(proto.MESSAGE, number=3, message=timestamp_pb2.Timestamp,)
    display_name = proto.Field(proto.STRING, number=4,)
    region_code = proto.Field(proto.STRING, number=5,)
    deleted = proto.Field(proto.BOOL, number=6,)


class Property(proto.Message):
    r"""A resource message representing a Google Analytics GA4
    property.

    Attributes:
        name (str):
            Output only. Resource name of this property. Format:
            properties/{property_id} Example: "properties/1000".
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when the entity was
            originally created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when entity payload fields
            were last updated.
        parent (str):
            Immutable. Resource name of this property's
            logical parent.
            Note: The Property-Moving UI can be used to
            change the parent. Format: accounts/{account}
            Example: "accounts/100".
        display_name (str):
            Required. Human-readable display name for
            this property.
            The max allowed display name length is 100
            UTF-16 code units.
        industry_category (google.analytics.admin_v1alpha.types.IndustryCategory):
            Industry associated with this property Example: AUTOMOTIVE,
            FOOD_AND_DRINK
        time_zone (str):
            Required. Reporting Time Zone, used as the day boundary for
            reports, regardless of where the data originates. If the
            time zone honors DST, Analytics will automatically adjust
            for the changes.

            NOTE: Changing the time zone only affects data going
            forward, and is not applied retroactively.

            Format: https://www.iana.org/time-zones Example:
            "America/Los_Angeles".
        currency_code (str):
            The currency type used in reports involving monetary values.

            Format: https://en.wikipedia.org/wiki/ISO_4217 Examples:
            "USD", "EUR", "JPY".
        delete_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. If set, the time at which this
            property was trashed. If not set, then this
            property is not currently in the trash can.
        expire_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. If set, the time at which this
            trashed property will be permanently deleted. If
            not set, then this property is not currently in
            the trash can and is not slated to be deleted.
    """

    name = proto.Field(proto.STRING, number=1,)
    create_time = proto.Field(proto.MESSAGE, number=3, message=timestamp_pb2.Timestamp,)
    update_time = proto.Field(proto.MESSAGE, number=4, message=timestamp_pb2.Timestamp,)
    parent = proto.Field(proto.STRING, number=2,)
    display_name = proto.Field(proto.STRING, number=5,)
    industry_category = proto.Field(proto.ENUM, number=6, enum="IndustryCategory",)
    time_zone = proto.Field(proto.STRING, number=7,)
    currency_code = proto.Field(proto.STRING, number=8,)
    delete_time = proto.Field(
        proto.MESSAGE, number=11, message=timestamp_pb2.Timestamp,
    )
    expire_time = proto.Field(
        proto.MESSAGE, number=12, message=timestamp_pb2.Timestamp,
    )


class AndroidAppDataStream(proto.Message):
    r"""A resource message representing a Google Analytics Android
    app stream.

    Attributes:
        name (str):
            Output only. Resource name of this Data Stream. Format:
            properties/{property_id}/androidAppDataStreams/{stream_id}
            Example: "properties/1000/androidAppDataStreams/2000".
        firebase_app_id (str):
            Output only. ID of the corresponding Android
            app in Firebase, if any. This ID can change if
            the Android app is deleted and recreated.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when this stream was
            originally created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when stream payload fields
            were last updated.
        package_name (str):
            Immutable. The package name for the app being
            measured. Example: "com.example.myandroidapp".
        display_name (str):
            Human-readable display name for the Data
            Stream.
            The max allowed display name length is 255
            UTF-16 code units.
    """

    name = proto.Field(proto.STRING, number=1,)
    firebase_app_id = proto.Field(proto.STRING, number=2,)
    create_time = proto.Field(proto.MESSAGE, number=3, message=timestamp_pb2.Timestamp,)
    update_time = proto.Field(proto.MESSAGE, number=4, message=timestamp_pb2.Timestamp,)
    package_name = proto.Field(proto.STRING, number=5,)
    display_name = proto.Field(proto.STRING, number=6,)


class IosAppDataStream(proto.Message):
    r"""A resource message representing a Google Analytics IOS app
    stream.

    Attributes:
        name (str):
            Output only. Resource name of this Data Stream. Format:
            properties/{property_id}/iosAppDataStreams/{stream_id}
            Example: "properties/1000/iosAppDataStreams/2000".
        firebase_app_id (str):
            Output only. ID of the corresponding iOS app
            in Firebase, if any. This ID can change if the
            iOS app is deleted and recreated.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when this stream was
            originally created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when stream payload fields
            were last updated.
        bundle_id (str):
            Required. Immutable. The Apple App Store
            Bundle ID for the app Example:
            "com.example.myiosapp".
        display_name (str):
            Human-readable display name for the Data
            Stream.
            The max allowed display name length is 255
            UTF-16 code units.
    """

    name = proto.Field(proto.STRING, number=1,)
    firebase_app_id = proto.Field(proto.STRING, number=2,)
    create_time = proto.Field(proto.MESSAGE, number=3, message=timestamp_pb2.Timestamp,)
    update_time = proto.Field(proto.MESSAGE, number=4, message=timestamp_pb2.Timestamp,)
    bundle_id = proto.Field(proto.STRING, number=5,)
    display_name = proto.Field(proto.STRING, number=6,)


class WebDataStream(proto.Message):
    r"""A resource message representing a Google Analytics web
    stream.

    Attributes:
        name (str):
            Output only. Resource name of this Data Stream. Format:
            properties/{property_id}/webDataStreams/{stream_id} Example:
            "properties/1000/webDataStreams/2000".
        measurement_id (str):
            Output only. Analytics "Measurement ID",
            without the "G-" prefix. Example: "G-1A2BCD345E"
            would just be "1A2BCD345E".
        firebase_app_id (str):
            Output only. ID of the corresponding web app
            in Firebase, if any. This ID can change if the
            web app is deleted and recreated.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when this stream was
            originally created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when stream payload fields
            were last updated.
        default_uri (str):
            Immutable. Domain name of the web app being
            measured, or empty. Example:
            "http://www.google.com",
            "https://www.google.com".
        display_name (str):
            Required. Human-readable display name for the
            Data Stream.
            The max allowed display name length is 100
            UTF-16 code units.
    """

    name = proto.Field(proto.STRING, number=1,)
    measurement_id = proto.Field(proto.STRING, number=2,)
    firebase_app_id = proto.Field(proto.STRING, number=3,)
    create_time = proto.Field(proto.MESSAGE, number=4, message=timestamp_pb2.Timestamp,)
    update_time = proto.Field(proto.MESSAGE, number=5, message=timestamp_pb2.Timestamp,)
    default_uri = proto.Field(proto.STRING, number=6,)
    display_name = proto.Field(proto.STRING, number=7,)


class UserLink(proto.Message):
    r"""A resource message representing a user's permissions on an
    Account or Property resource.

    Attributes:
        name (str):
            Output only. Example format:
            properties/1234/userLinks/5678
        email_address (str):
            Immutable. Email address of the user to link
        direct_roles (Sequence[str]):
            Roles directly assigned to this user for this account or
            property.

            Valid values: predefinedRoles/read
            predefinedRoles/collaborate predefinedRoles/edit
            predefinedRoles/manage-users

            Excludes roles that are inherited from a higher-level
            entity, group, or organization admin role.

            A UserLink that is updated to have an empty list of
            direct_roles will be deleted.
    """

    name = proto.Field(proto.STRING, number=1,)
    email_address = proto.Field(proto.STRING, number=2,)
    direct_roles = proto.RepeatedField(proto.STRING, number=3,)


class AuditUserLink(proto.Message):
    r"""Read-only resource used to summarize a principal's effective
    roles.

    Attributes:
        name (str):
            Example format:
            properties/1234/userLinks/5678
        email_address (str):
            Email address of the linked user
        direct_roles (Sequence[str]):
            Roles directly assigned to this user for this
            entity.
            Format: predefinedRoles/read

            Excludes roles that are inherited from an
            account (if this is for a property), group, or
            organization admin role.
        effective_roles (Sequence[str]):
            Union of all permissions a user has at this
            account or property (includes direct
            permissions, group-inherited permissions, etc.).
            Format: predefinedRoles/read
    """

    name = proto.Field(proto.STRING, number=1,)
    email_address = proto.Field(proto.STRING, number=2,)
    direct_roles = proto.RepeatedField(proto.STRING, number=3,)
    effective_roles = proto.RepeatedField(proto.STRING, number=4,)


class EnhancedMeasurementSettings(proto.Message):
    r"""Singleton resource under a WebDataStream, configuring
    measurement of additional site interactions and content.

    Attributes:
        name (str):
            Output only. Resource name of this Data Stream. Format:
            properties/{property_id}/webDataStreams/{stream_id}/enhancedMeasurementSettings
            Example:
            "properties/1000/webDataStreams/2000/enhancedMeasurementSettings".
        stream_enabled (bool):
            Indicates whether Enhanced Measurement
            Settings will be used to automatically measure
            interactions and content on this web stream.
            Changing this value does not affect the settings
            themselves, but determines whether they are
            respected.
        page_views_enabled (bool):
            Output only. If enabled, capture a page view
            event each time a page loads or the website
            changes the browser history state.
        scrolls_enabled (bool):
            If enabled, capture scroll events each time a
            visitor gets to the bottom of a page.
        outbound_clicks_enabled (bool):
            If enabled, capture an outbound click event
            each time a visitor clicks a link that leads
            them away from your domain.
        site_search_enabled (bool):
            If enabled, capture a view search results
            event each time a visitor performs a search on
            your site (based on a query parameter).
        video_engagement_enabled (bool):
            If enabled, capture video play, progress, and
            complete events as visitors view embedded videos
            on your site.
        file_downloads_enabled (bool):
            If enabled, capture a file download event
            each time a link is clicked with a common
            document, compressed file, application, video,
            or audio extension.
        page_loads_enabled (bool):
            Output only. If enabled, capture a page view
            event each time a page loads.
        page_changes_enabled (bool):
            If enabled, capture a page view event each
            time the website changes the browser history
            state.
        search_query_parameter (str):
            Required. URL query parameters to interpret
            as site search parameters. Max length is 1024
            characters. Must not be empty.
        uri_query_parameter (str):
            Additional URL query parameters.
            Max length is 1024 characters.
    """

    name = proto.Field(proto.STRING, number=1,)
    stream_enabled = proto.Field(proto.BOOL, number=2,)
    page_views_enabled = proto.Field(proto.BOOL, number=3,)
    scrolls_enabled = proto.Field(proto.BOOL, number=4,)
    outbound_clicks_enabled = proto.Field(proto.BOOL, number=5,)
    site_search_enabled = proto.Field(proto.BOOL, number=7,)
    video_engagement_enabled = proto.Field(proto.BOOL, number=9,)
    file_downloads_enabled = proto.Field(proto.BOOL, number=10,)
    page_loads_enabled = proto.Field(proto.BOOL, number=12,)
    page_changes_enabled = proto.Field(proto.BOOL, number=13,)
    search_query_parameter = proto.Field(proto.STRING, number=16,)
    uri_query_parameter = proto.Field(proto.STRING, number=17,)


class FirebaseLink(proto.Message):
    r"""A link between an GA4 property and a Firebase project.
    Attributes:
        name (str):
            Output only. Example format:
            properties/1234/firebaseLinks/5678
        project (str):
            Immutable. Firebase project resource name. When creating a
            FirebaseLink, you may provide this resource name using
            either a project number or project ID. Once this resource
            has been created, returned FirebaseLinks will always have a
            project_name that contains a project number.

            Format: 'projects/{project number}' Example: 'projects/1234'
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when this FirebaseLink was
            originally created.
        maximum_user_access (google.analytics.admin_v1alpha.types.MaximumUserAccess):
            Maximum user access to the GA4 property
            allowed to admins of the linked Firebase
            project.
    """

    name = proto.Field(proto.STRING, number=1,)
    project = proto.Field(proto.STRING, number=2,)
    create_time = proto.Field(proto.MESSAGE, number=3, message=timestamp_pb2.Timestamp,)
    maximum_user_access = proto.Field(proto.ENUM, number=4, enum="MaximumUserAccess",)


class GlobalSiteTag(proto.Message):
    r"""Read-only resource with the tag for sending data from a
    website to a WebDataStream.

    Attributes:
        name (str):
            Output only. Resource name for this
            GlobalSiteTag resource. Format:
            properties/{propertyId}/globalSiteTag
        snippet (str):
            Immutable. JavaScript code snippet to be
            pasted as the first item into the head tag of
            every webpage to measure.
    """

    name = proto.Field(proto.STRING, number=1,)
    snippet = proto.Field(proto.STRING, number=2,)


class GoogleAdsLink(proto.Message):
    r"""A link between an GA4 property and a Google Ads account.
    Attributes:
        name (str):
            Output only. Format:
            properties/{propertyId}/googleAdsLinks/{googleAdsLinkId}
            Note: googleAdsLinkId is not the Google Ads
            customer ID.
        customer_id (str):
            Immutable. Google Ads customer ID.
        can_manage_clients (bool):
            Output only. If true, this link is for a
            Google Ads manager account.
        ads_personalization_enabled (google.protobuf.wrappers_pb2.BoolValue):
            Enable personalized advertising features with
            this integration. Automatically publish my
            Google Analytics audience lists and Google
            Analytics remarketing events/parameters to the
            linked Google Ads account. If this field is not
            set on create/update, it will be defaulted to
            true.
        email_address (str):
            Output only. Email address of the user that
            created the link. An empty string will be
            returned if the email address can't be
            retrieved.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when this link was
            originally created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when this link was last
            updated.
    """

    name = proto.Field(proto.STRING, number=1,)
    customer_id = proto.Field(proto.STRING, number=3,)
    can_manage_clients = proto.Field(proto.BOOL, number=4,)
    ads_personalization_enabled = proto.Field(
        proto.MESSAGE, number=5, message=wrappers_pb2.BoolValue,
    )
    email_address = proto.Field(proto.STRING, number=6,)
    create_time = proto.Field(proto.MESSAGE, number=7, message=timestamp_pb2.Timestamp,)
    update_time = proto.Field(proto.MESSAGE, number=8, message=timestamp_pb2.Timestamp,)


class DataSharingSettings(proto.Message):
    r"""A resource message representing data sharing settings of a
    Google Analytics account.

    Attributes:
        name (str):
            Output only. Resource name.
            Format: accounts/{account}/dataSharingSettings
            Example: "accounts/1000/dataSharingSettings".
        sharing_with_google_support_enabled (bool):
            Allows Google support to access the data in
            order to help troubleshoot issues.
        sharing_with_google_assigned_sales_enabled (bool):
            Allows Google sales teams that are assigned
            to the customer to access the data in order to
            suggest configuration changes to improve
            results. Sales team restrictions still apply
            when enabled.
        sharing_with_google_any_sales_enabled (bool):
            Allows any of Google sales to access the data
            in order to suggest configuration changes to
            improve results.
        sharing_with_google_products_enabled (bool):
            Allows Google to use the data to improve
            other Google products or services.
        sharing_with_others_enabled (bool):
            Allows Google to share the data anonymously
            in aggregate form with others.
    """

    name = proto.Field(proto.STRING, number=1,)
    sharing_with_google_support_enabled = proto.Field(proto.BOOL, number=2,)
    sharing_with_google_assigned_sales_enabled = proto.Field(proto.BOOL, number=3,)
    sharing_with_google_any_sales_enabled = proto.Field(proto.BOOL, number=4,)
    sharing_with_google_products_enabled = proto.Field(proto.BOOL, number=5,)
    sharing_with_others_enabled = proto.Field(proto.BOOL, number=6,)


class AccountSummary(proto.Message):
    r"""A virtual resource representing an overview of an account and
    all its child GA4 properties.

    Attributes:
        name (str):
            Resource name for this account summary. Format:
            accountSummaries/{account_id} Example:
            "accountSummaries/1000".
        account (str):
            Resource name of account referred to by this account summary
            Format: accounts/{account_id} Example: "accounts/1000".
        display_name (str):
            Display name for the account referred to in
            this account summary.
        property_summaries (Sequence[google.analytics.admin_v1alpha.types.PropertySummary]):
            List of summaries for child accounts of this
            account.
    """

    name = proto.Field(proto.STRING, number=1,)
    account = proto.Field(proto.STRING, number=2,)
    display_name = proto.Field(proto.STRING, number=3,)
    property_summaries = proto.RepeatedField(
        proto.MESSAGE, number=4, message="PropertySummary",
    )


class PropertySummary(proto.Message):
    r"""A virtual resource representing metadata for an GA4 property.
    Attributes:
        property (str):
            Resource name of property referred to by this property
            summary Format: properties/{property_id} Example:
            "properties/1000".
        display_name (str):
            Display name for the property referred to in
            this account summary.
    """

    property = proto.Field(proto.STRING, number=1,)
    display_name = proto.Field(proto.STRING, number=2,)


class MeasurementProtocolSecret(proto.Message):
    r"""A secret value used for sending hits to Measurement Protocol.
    Attributes:
        name (str):
            Output only. Resource name of this secret.
            This secret may be a child of any type of
            stream. Format:
            properties/{property}/webDataStreams/{webDataStream}/measurementProtocolSecrets/{measurementProtocolSecret}
        display_name (str):
            Required. Human-readable display name for
            this secret.
        secret_value (str):
            Output only. The measurement protocol secret value. Pass
            this value to the api_secret field of the Measurement
            Protocol API when sending hits to this secret's parent
            property.
    """

    name = proto.Field(proto.STRING, number=1,)
    display_name = proto.Field(proto.STRING, number=2,)
    secret_value = proto.Field(proto.STRING, number=3,)


class ChangeHistoryEvent(proto.Message):
    r"""A set of changes within a Google Analytics account or its
    child properties that resulted from the same cause. Common
    causes would be updates made in the Google Analytics UI, changes
    from customer support, or automatic Google Analytics system
    changes.

    Attributes:
        id (str):
            ID of this change history event. This ID is
            unique across Google Analytics.
        change_time (google.protobuf.timestamp_pb2.Timestamp):
            Time when change was made.
        actor_type (google.analytics.admin_v1alpha.types.ActorType):
            The type of actor that made this change.
        user_actor_email (str):
            Email address of the Google account that made
            the change. This will be a valid email address
            if the actor field is set to USER, and empty
            otherwise. Google accounts that have been
            deleted will cause an error.
        changes_filtered (bool):
            If true, then the list of changes returned
            was filtered, and does not represent all changes
            that occurred in this event.
        changes (Sequence[google.analytics.admin_v1alpha.types.ChangeHistoryChange]):
            A list of changes made in this change history
            event that fit the filters specified in
            SearchChangeHistoryEventsRequest.
    """

    id = proto.Field(proto.STRING, number=1,)
    change_time = proto.Field(proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,)
    actor_type = proto.Field(proto.ENUM, number=3, enum="ActorType",)
    user_actor_email = proto.Field(proto.STRING, number=4,)
    changes_filtered = proto.Field(proto.BOOL, number=5,)
    changes = proto.RepeatedField(
        proto.MESSAGE, number=6, message="ChangeHistoryChange",
    )


class ChangeHistoryChange(proto.Message):
    r"""A description of a change to a single Google Analytics
    resource.

    Attributes:
        resource (str):
            Resource name of the resource whose changes
            are described by this entry.
        action (google.analytics.admin_v1alpha.types.ActionType):
            The type of action that changed this
            resource.
        resource_before_change (google.analytics.admin_v1alpha.types.ChangeHistoryChange.ChangeHistoryResource):
            Resource contents from before the change was
            made. If this resource was created in this
            change, this field will be missing.
        resource_after_change (google.analytics.admin_v1alpha.types.ChangeHistoryChange.ChangeHistoryResource):
            Resource contents from after the change was
            made. If this resource was deleted in this
            change, this field will be missing.
    """

    class ChangeHistoryResource(proto.Message):
        r"""A snapshot of a resource as before or after the result of a
        change in change history.

        Attributes:
            account (google.analytics.admin_v1alpha.types.Account):
                A snapshot of an Account resource in change
                history.
            property (google.analytics.admin_v1alpha.types.Property):
                A snapshot of a Property resource in change
                history.
            web_data_stream (google.analytics.admin_v1alpha.types.WebDataStream):
                A snapshot of a WebDataStream resource in
                change history.
            android_app_data_stream (google.analytics.admin_v1alpha.types.AndroidAppDataStream):
                A snapshot of an AndroidAppDataStream
                resource in change history.
            ios_app_data_stream (google.analytics.admin_v1alpha.types.IosAppDataStream):
                A snapshot of an IosAppDataStream resource in
                change history.
            firebase_link (google.analytics.admin_v1alpha.types.FirebaseLink):
                A snapshot of a FirebaseLink resource in
                change history.
            google_ads_link (google.analytics.admin_v1alpha.types.GoogleAdsLink):
                A snapshot of a GoogleAdsLink resource in
                change history.
            google_signals_settings (google.analytics.admin_v1alpha.types.GoogleSignalsSettings):
                A snapshot of a GoogleSignalsSettings
                resource in change history.
            conversion_event (google.analytics.admin_v1alpha.types.ConversionEvent):
                A snapshot of a ConversionEvent resource in
                change history.
            measurement_protocol_secret (google.analytics.admin_v1alpha.types.MeasurementProtocolSecret):
                A snapshot of a MeasurementProtocolSecret
                resource in change history.
            custom_dimension (google.analytics.admin_v1alpha.types.CustomDimension):
                A snapshot of a CustomDimension resource in
                change history.
            custom_metric (google.analytics.admin_v1alpha.types.CustomMetric):
                A snapshot of a CustomMetric resource in
                change history.
        """

        account = proto.Field(
            proto.MESSAGE, number=1, oneof="resource", message="Account",
        )
        property = proto.Field(
            proto.MESSAGE, number=2, oneof="resource", message="Property",
        )
        web_data_stream = proto.Field(
            proto.MESSAGE, number=3, oneof="resource", message="WebDataStream",
        )
        android_app_data_stream = proto.Field(
            proto.MESSAGE, number=4, oneof="resource", message="AndroidAppDataStream",
        )
        ios_app_data_stream = proto.Field(
            proto.MESSAGE, number=5, oneof="resource", message="IosAppDataStream",
        )
        firebase_link = proto.Field(
            proto.MESSAGE, number=6, oneof="resource", message="FirebaseLink",
        )
        google_ads_link = proto.Field(
            proto.MESSAGE, number=7, oneof="resource", message="GoogleAdsLink",
        )
        google_signals_settings = proto.Field(
            proto.MESSAGE, number=8, oneof="resource", message="GoogleSignalsSettings",
        )
        conversion_event = proto.Field(
            proto.MESSAGE, number=11, oneof="resource", message="ConversionEvent",
        )
        measurement_protocol_secret = proto.Field(
            proto.MESSAGE,
            number=12,
            oneof="resource",
            message="MeasurementProtocolSecret",
        )
        custom_dimension = proto.Field(
            proto.MESSAGE, number=13, oneof="resource", message="CustomDimension",
        )
        custom_metric = proto.Field(
            proto.MESSAGE, number=14, oneof="resource", message="CustomMetric",
        )

    resource = proto.Field(proto.STRING, number=1,)
    action = proto.Field(proto.ENUM, number=2, enum="ActionType",)
    resource_before_change = proto.Field(
        proto.MESSAGE, number=3, message=ChangeHistoryResource,
    )
    resource_after_change = proto.Field(
        proto.MESSAGE, number=4, message=ChangeHistoryResource,
    )


class ConversionEvent(proto.Message):
    r"""A conversion event in a Google Analytics property.
    Attributes:
        name (str):
            Output only. Resource name of this conversion event. Format:
            properties/{property}/conversionEvents/{conversion_event}
        event_name (str):
            Immutable. The event name for this conversion
            event. Examples: 'click', 'purchase'
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when this conversion event
            was created in the property.
        is_deletable (bool):
            Output only. If set, this event can currently
            be deleted via DeleteConversionEvent.
    """

    name = proto.Field(proto.STRING, number=1,)
    event_name = proto.Field(proto.STRING, number=2,)
    create_time = proto.Field(proto.MESSAGE, number=3, message=timestamp_pb2.Timestamp,)
    is_deletable = proto.Field(proto.BOOL, number=4,)


class GoogleSignalsSettings(proto.Message):
    r"""Settings values for Google Signals.  This is a singleton
    resource.

    Attributes:
        name (str):
            Output only. Resource name of this setting. Format:
            properties/{property_id}/googleSignalsSettings Example:
            "properties/1000/googleSignalsSettings".
        state (google.analytics.admin_v1alpha.types.GoogleSignalsState):
            Status of this setting.
        consent (google.analytics.admin_v1alpha.types.GoogleSignalsConsent):
            Output only. Terms of Service acceptance.
    """

    name = proto.Field(proto.STRING, number=1,)
    state = proto.Field(proto.ENUM, number=3, enum="GoogleSignalsState",)
    consent = proto.Field(proto.ENUM, number=4, enum="GoogleSignalsConsent",)


class CustomDimension(proto.Message):
    r"""A definition for a CustomDimension.
    Attributes:
        name (str):
            Output only. Resource name for this
            CustomDimension resource. Format:
            properties/{property}/customDimensions/{customDimension}
        parameter_name (str):
            Required. Immutable. Tagging parameter name
            for this custom dimension.
            If this is a user-scoped dimension, then this is
            the user property name. If this is an event-
            scoped dimension, then this is the event
            parameter name.

            May only contain alphanumeric and underscore
            characters, starting with a letter. Max length
            of 24 characters for user-scoped dimensions, 40
            characters for event-scoped dimensions.
        display_name (str):
            Required. Display name for this custom
            dimension as shown in the Analytics UI. Max
            length of 82 characters, alphanumeric plus space
            and underscore starting with a letter. Legacy
            system-generated display names may contain
            square brackets, but updates to this field will
            never permit square brackets.
        description (str):
            Optional. Description for this custom
            dimension. Max length of 150 characters.
        scope (google.analytics.admin_v1alpha.types.CustomDimension.DimensionScope):
            Required. Immutable. The scope of this
            dimension.
        disallow_ads_personalization (bool):
            Optional. If set to true, sets this dimension
            as NPA and excludes it from ads personalization.
            This is currently only supported by user-scoped
            custom dimensions.
    """

    class DimensionScope(proto.Enum):
        r"""Valid values for the scope of this dimension."""
        DIMENSION_SCOPE_UNSPECIFIED = 0
        EVENT = 1
        USER = 2

    name = proto.Field(proto.STRING, number=1,)
    parameter_name = proto.Field(proto.STRING, number=2,)
    display_name = proto.Field(proto.STRING, number=3,)
    description = proto.Field(proto.STRING, number=4,)
    scope = proto.Field(proto.ENUM, number=5, enum=DimensionScope,)
    disallow_ads_personalization = proto.Field(proto.BOOL, number=6,)


class CustomMetric(proto.Message):
    r"""A definition for a custom metric.
    Attributes:
        name (str):
            Output only. Resource name for this
            CustomMetric resource. Format:
            properties/{property}/customMetrics/{customMetric}
        parameter_name (str):
            Required. Immutable. Tagging name for this
            custom metric.
            If this is an event-scoped metric, then this is
            the event parameter name.

            May only contain alphanumeric and underscore
            charactes, starting with a letter. Max length of
            40 characters for event-scoped metrics.
        display_name (str):
            Required. Display name for this custom metric
            as shown in the Analytics UI. Max length of 82
            characters, alphanumeric plus space and
            underscore starting with a letter. Legacy
            system-generated display names may contain
            square brackets, but updates to this field will
            never permit square brackets.
        description (str):
            Optional. Description for this custom
            dimension. Max length of 150 characters.
        measurement_unit (google.analytics.admin_v1alpha.types.CustomMetric.MeasurementUnit):
            Required. Immutable. The type for the custom
            metric's value.
        scope (google.analytics.admin_v1alpha.types.CustomMetric.MetricScope):
            Required. Immutable. The scope of this custom
            metric.
    """

    class MeasurementUnit(proto.Enum):
        r"""Possible types of representing the custom metric's value.
        Currency representation may change in the future, requiring a
        breaking API change.
        """
        MEASUREMENT_UNIT_UNSPECIFIED = 0
        STANDARD = 1
        CURRENCY = 2
        FEET = 3
        METERS = 4
        KILOMETERS = 5
        MILES = 6
        MILLISECONDS = 7
        SECONDS = 8
        MINUTES = 9
        HOURS = 10

    class MetricScope(proto.Enum):
        r"""The scope of this metric."""
        METRIC_SCOPE_UNSPECIFIED = 0
        EVENT = 1

    name = proto.Field(proto.STRING, number=1,)
    parameter_name = proto.Field(proto.STRING, number=2,)
    display_name = proto.Field(proto.STRING, number=3,)
    description = proto.Field(proto.STRING, number=4,)
    measurement_unit = proto.Field(proto.ENUM, number=5, enum=MeasurementUnit,)
    scope = proto.Field(proto.ENUM, number=6, enum=MetricScope,)


__all__ = tuple(sorted(__protobuf__.manifest))
