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
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.analytics.admin.v1alpha",
    manifest={
        "IndustryCategory",
        "ServiceLevel",
        "ActorType",
        "ActionType",
        "ChangeHistoryResourceType",
        "GoogleSignalsState",
        "GoogleSignalsConsent",
        "LinkProposalInitiatingProduct",
        "LinkProposalState",
        "PropertyType",
        "Account",
        "Property",
        "DataStream",
        "UserLink",
        "AuditUserLink",
        "FirebaseLink",
        "GlobalSiteTag",
        "GoogleAdsLink",
        "DataSharingSettings",
        "AccountSummary",
        "PropertySummary",
        "MeasurementProtocolSecret",
        "ChangeHistoryEvent",
        "ChangeHistoryChange",
        "DisplayVideo360AdvertiserLink",
        "DisplayVideo360AdvertiserLinkProposal",
        "LinkProposalStatusDetails",
        "ConversionEvent",
        "GoogleSignalsSettings",
        "CustomDimension",
        "CustomMetric",
        "DataRetentionSettings",
        "AttributionSettings",
    },
)


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


class ServiceLevel(proto.Enum):
    r"""Various levels of service for Google Analytics."""
    SERVICE_LEVEL_UNSPECIFIED = 0
    GOOGLE_ANALYTICS_STANDARD = 1
    GOOGLE_ANALYTICS_360 = 2


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
    FIREBASE_LINK = 6
    GOOGLE_ADS_LINK = 7
    GOOGLE_SIGNALS_SETTINGS = 8
    CONVERSION_EVENT = 9
    MEASUREMENT_PROTOCOL_SECRET = 10
    CUSTOM_DIMENSION = 11
    CUSTOM_METRIC = 12
    DATA_RETENTION_SETTINGS = 13
    DISPLAY_VIDEO_360_ADVERTISER_LINK = 14
    DISPLAY_VIDEO_360_ADVERTISER_LINK_PROPOSAL = 15
    SEARCH_ADS_360_LINK = 16
    DATA_STREAM = 18
    ATTRIBUTION_SETTINGS = 20


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


class LinkProposalInitiatingProduct(proto.Enum):
    r"""An indication of which product the user initiated a link
    proposal from.
    """
    LINK_PROPOSAL_INITIATING_PRODUCT_UNSPECIFIED = 0
    GOOGLE_ANALYTICS = 1
    LINKED_PRODUCT = 2


class LinkProposalState(proto.Enum):
    r"""The state of a link proposal resource."""
    LINK_PROPOSAL_STATE_UNSPECIFIED = 0
    AWAITING_REVIEW_FROM_GOOGLE_ANALYTICS = 1
    AWAITING_REVIEW_FROM_LINKED_PRODUCT = 2
    WITHDRAWN = 3
    DECLINED = 4
    EXPIRED = 5
    OBSOLETE = 6


class PropertyType(proto.Enum):
    r"""Types of Property resources."""
    PROPERTY_TYPE_UNSPECIFIED = 0
    PROPERTY_TYPE_ORDINARY = 1
    PROPERTY_TYPE_SUBPROPERTY = 2
    PROPERTY_TYPE_ROLLUP = 3


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

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    create_time = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    update_time = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    display_name = proto.Field(
        proto.STRING,
        number=4,
    )
    region_code = proto.Field(
        proto.STRING,
        number=5,
    )
    deleted = proto.Field(
        proto.BOOL,
        number=6,
    )


class Property(proto.Message):
    r"""A resource message representing a Google Analytics GA4
    property.

    Attributes:
        name (str):
            Output only. Resource name of this property. Format:
            properties/{property_id} Example: "properties/1000".
        property_type (google.analytics.admin_v1alpha.types.PropertyType):
            Immutable. The property type for this Property resource.
            When creating a property, if the type is
            "PROPERTY_TYPE_UNSPECIFIED", then "ORDINARY_PROPERTY" will
            be implied. "SUBPROPERTY" and "ROLLUP_PROPERTY" types cannot
            yet be created via Google Analytics Admin API.
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
            change the parent. Format: accounts/{account},
            properties/{property} Example: "accounts/100",
            "properties/101".
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
        service_level (google.analytics.admin_v1alpha.types.ServiceLevel):
            Output only. The Google Analytics service
            level that applies to this property.
        delete_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. If set, the time at which this
            property was trashed. If not set, then this
            property is not currently in the trash can.
        expire_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. If set, the time at which this
            trashed property will be permanently deleted. If
            not set, then this property is not currently in
            the trash can and is not slated to be deleted.
        account (str):
            Immutable. The resource name of the parent account Format:
            accounts/{account_id} Example: "accounts/123".
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    property_type = proto.Field(
        proto.ENUM,
        number=14,
        enum="PropertyType",
    )
    create_time = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    update_time = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    parent = proto.Field(
        proto.STRING,
        number=2,
    )
    display_name = proto.Field(
        proto.STRING,
        number=5,
    )
    industry_category = proto.Field(
        proto.ENUM,
        number=6,
        enum="IndustryCategory",
    )
    time_zone = proto.Field(
        proto.STRING,
        number=7,
    )
    currency_code = proto.Field(
        proto.STRING,
        number=8,
    )
    service_level = proto.Field(
        proto.ENUM,
        number=10,
        enum="ServiceLevel",
    )
    delete_time = proto.Field(
        proto.MESSAGE,
        number=11,
        message=timestamp_pb2.Timestamp,
    )
    expire_time = proto.Field(
        proto.MESSAGE,
        number=12,
        message=timestamp_pb2.Timestamp,
    )
    account = proto.Field(
        proto.STRING,
        number=13,
    )


class DataStream(proto.Message):
    r"""A resource message representing a data stream.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        web_stream_data (google.analytics.admin_v1alpha.types.DataStream.WebStreamData):
            Data specific to web streams. Must be populated if type is
            WEB_DATA_STREAM.

            This field is a member of `oneof`_ ``stream_data``.
        android_app_stream_data (google.analytics.admin_v1alpha.types.DataStream.AndroidAppStreamData):
            Data specific to Android app streams. Must be populated if
            type is ANDROID_APP_DATA_STREAM.

            This field is a member of `oneof`_ ``stream_data``.
        ios_app_stream_data (google.analytics.admin_v1alpha.types.DataStream.IosAppStreamData):
            Data specific to iOS app streams. Must be populated if type
            is IOS_APP_DATA_STREAM.

            This field is a member of `oneof`_ ``stream_data``.
        name (str):
            Output only. Resource name of this Data Stream. Format:
            properties/{property_id}/dataStreams/{stream_id} Example:
            "properties/1000/dataStreams/2000".
        type_ (google.analytics.admin_v1alpha.types.DataStream.DataStreamType):
            Required. Immutable. The type of this
            DataStream resource.
        display_name (str):
            Human-readable display name for the Data
            Stream.
            Required for web data streams.

            The max allowed display name length is 255
            UTF-16 code units.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when this stream was
            originally created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when stream payload fields
            were last updated.
    """

    class DataStreamType(proto.Enum):
        r"""The type of the data stream."""
        DATA_STREAM_TYPE_UNSPECIFIED = 0
        WEB_DATA_STREAM = 1
        ANDROID_APP_DATA_STREAM = 2
        IOS_APP_DATA_STREAM = 3

    class WebStreamData(proto.Message):
        r"""Data specific to web streams.

        Attributes:
            measurement_id (str):
                Output only. Analytics "Measurement ID",
                without the "G-" prefix. Example: "G-1A2BCD345E"
                would just be "1A2BCD345E".
            firebase_app_id (str):
                Output only. ID of the corresponding web app
                in Firebase, if any. This ID can change if the
                web app is deleted and recreated.
            default_uri (str):
                Immutable. Domain name of the web app being
                measured, or empty. Example:
                "http://www.google.com",
                "https://www.google.com".
        """

        measurement_id = proto.Field(
            proto.STRING,
            number=1,
        )
        firebase_app_id = proto.Field(
            proto.STRING,
            number=2,
        )
        default_uri = proto.Field(
            proto.STRING,
            number=3,
        )

    class AndroidAppStreamData(proto.Message):
        r"""Data specific to Android app streams.

        Attributes:
            firebase_app_id (str):
                Output only. ID of the corresponding Android
                app in Firebase, if any. This ID can change if
                the Android app is deleted and recreated.
            package_name (str):
                Immutable. The package name for the app being
                measured. Example: "com.example.myandroidapp".
        """

        firebase_app_id = proto.Field(
            proto.STRING,
            number=1,
        )
        package_name = proto.Field(
            proto.STRING,
            number=2,
        )

    class IosAppStreamData(proto.Message):
        r"""Data specific to iOS app streams.

        Attributes:
            firebase_app_id (str):
                Output only. ID of the corresponding iOS app
                in Firebase, if any. This ID can change if the
                iOS app is deleted and recreated.
            bundle_id (str):
                Required. Immutable. The Apple App Store
                Bundle ID for the app Example:
                "com.example.myiosapp".
        """

        firebase_app_id = proto.Field(
            proto.STRING,
            number=1,
        )
        bundle_id = proto.Field(
            proto.STRING,
            number=2,
        )

    web_stream_data = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="stream_data",
        message=WebStreamData,
    )
    android_app_stream_data = proto.Field(
        proto.MESSAGE,
        number=7,
        oneof="stream_data",
        message=AndroidAppStreamData,
    )
    ios_app_stream_data = proto.Field(
        proto.MESSAGE,
        number=8,
        oneof="stream_data",
        message=IosAppStreamData,
    )
    name = proto.Field(
        proto.STRING,
        number=1,
    )
    type_ = proto.Field(
        proto.ENUM,
        number=2,
        enum=DataStreamType,
    )
    display_name = proto.Field(
        proto.STRING,
        number=3,
    )
    create_time = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    update_time = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )


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

            Valid values: predefinedRoles/viewer predefinedRoles/analyst
            predefinedRoles/editor predefinedRoles/admin
            predefinedRoles/no-cost-data predefinedRoles/no-revenue-data

            Excludes roles that are inherited from a higher-level
            entity, group, or organization admin role.

            A UserLink that is updated to have an empty list of
            direct_roles will be deleted.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    email_address = proto.Field(
        proto.STRING,
        number=2,
    )
    direct_roles = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


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
            Format: predefinedRoles/viewer

            Excludes roles that are inherited from an
            account (if this is for a property), group, or
            organization admin role.
        effective_roles (Sequence[str]):
            Union of all permissions a user has at this
            account or property (includes direct
            permissions, group-inherited permissions, etc.).
            Format: predefinedRoles/viewer
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    email_address = proto.Field(
        proto.STRING,
        number=2,
    )
    direct_roles = proto.RepeatedField(
        proto.STRING,
        number=3,
    )
    effective_roles = proto.RepeatedField(
        proto.STRING,
        number=4,
    )


class FirebaseLink(proto.Message):
    r"""A link between a GA4 property and a Firebase project.

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
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    project = proto.Field(
        proto.STRING,
        number=2,
    )
    create_time = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )


class GlobalSiteTag(proto.Message):
    r"""Read-only resource with the tag for sending data from a
    website to a DataStream. Only present for web DataStream
    resources.

    Attributes:
        name (str):
            Output only. Resource name for this GlobalSiteTag resource.
            Format:
            properties/{property_id}/dataStreams/{stream_id}/globalSiteTag
            Example: "properties/123/dataStreams/456/globalSiteTag".
        snippet (str):
            Immutable. JavaScript code snippet to be
            pasted as the first item into the head tag of
            every webpage to measure.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    snippet = proto.Field(
        proto.STRING,
        number=2,
    )


class GoogleAdsLink(proto.Message):
    r"""A link between a GA4 property and a Google Ads account.

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
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when this link was
            originally created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time when this link was last
            updated.
        creator_email_address (str):
            Output only. Email address of the user that
            created the link. An empty string will be
            returned if the email address can't be
            retrieved.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    customer_id = proto.Field(
        proto.STRING,
        number=3,
    )
    can_manage_clients = proto.Field(
        proto.BOOL,
        number=4,
    )
    ads_personalization_enabled = proto.Field(
        proto.MESSAGE,
        number=5,
        message=wrappers_pb2.BoolValue,
    )
    create_time = proto.Field(
        proto.MESSAGE,
        number=7,
        message=timestamp_pb2.Timestamp,
    )
    update_time = proto.Field(
        proto.MESSAGE,
        number=8,
        message=timestamp_pb2.Timestamp,
    )
    creator_email_address = proto.Field(
        proto.STRING,
        number=9,
    )


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

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    sharing_with_google_support_enabled = proto.Field(
        proto.BOOL,
        number=2,
    )
    sharing_with_google_assigned_sales_enabled = proto.Field(
        proto.BOOL,
        number=3,
    )
    sharing_with_google_any_sales_enabled = proto.Field(
        proto.BOOL,
        number=4,
    )
    sharing_with_google_products_enabled = proto.Field(
        proto.BOOL,
        number=5,
    )
    sharing_with_others_enabled = proto.Field(
        proto.BOOL,
        number=6,
    )


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

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    account = proto.Field(
        proto.STRING,
        number=2,
    )
    display_name = proto.Field(
        proto.STRING,
        number=3,
    )
    property_summaries = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message="PropertySummary",
    )


class PropertySummary(proto.Message):
    r"""A virtual resource representing metadata for a GA4 property.

    Attributes:
        property (str):
            Resource name of property referred to by this property
            summary Format: properties/{property_id} Example:
            "properties/1000".
        display_name (str):
            Display name for the property referred to in
            this property summary.
        property_type (google.analytics.admin_v1alpha.types.PropertyType):
            The property's property type.
        parent (str):
            Resource name of this property's logical
            parent.
            Note: The Property-Moving UI can be used to
            change the parent. Format: accounts/{account},
            properties/{property} Example: "accounts/100",
            "properties/200".
    """

    property = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name = proto.Field(
        proto.STRING,
        number=2,
    )
    property_type = proto.Field(
        proto.ENUM,
        number=3,
        enum="PropertyType",
    )
    parent = proto.Field(
        proto.STRING,
        number=4,
    )


class MeasurementProtocolSecret(proto.Message):
    r"""A secret value used for sending hits to Measurement Protocol.

    Attributes:
        name (str):
            Output only. Resource name of this secret.
            This secret may be a child of any type of
            stream. Format:
            properties/{property}/dataStreams/{dataStream}/measurementProtocolSecrets/{measurementProtocolSecret}
        display_name (str):
            Required. Human-readable display name for
            this secret.
        secret_value (str):
            Output only. The measurement protocol secret value. Pass
            this value to the api_secret field of the Measurement
            Protocol API when sending hits to this secret's parent
            property.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name = proto.Field(
        proto.STRING,
        number=2,
    )
    secret_value = proto.Field(
        proto.STRING,
        number=3,
    )


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

    id = proto.Field(
        proto.STRING,
        number=1,
    )
    change_time = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    actor_type = proto.Field(
        proto.ENUM,
        number=3,
        enum="ActorType",
    )
    user_actor_email = proto.Field(
        proto.STRING,
        number=4,
    )
    changes_filtered = proto.Field(
        proto.BOOL,
        number=5,
    )
    changes = proto.RepeatedField(
        proto.MESSAGE,
        number=6,
        message="ChangeHistoryChange",
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

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            account (google.analytics.admin_v1alpha.types.Account):
                A snapshot of an Account resource in change
                history.

                This field is a member of `oneof`_ ``resource``.
            property (google.analytics.admin_v1alpha.types.Property):
                A snapshot of a Property resource in change
                history.

                This field is a member of `oneof`_ ``resource``.
            firebase_link (google.analytics.admin_v1alpha.types.FirebaseLink):
                A snapshot of a FirebaseLink resource in
                change history.

                This field is a member of `oneof`_ ``resource``.
            google_ads_link (google.analytics.admin_v1alpha.types.GoogleAdsLink):
                A snapshot of a GoogleAdsLink resource in
                change history.

                This field is a member of `oneof`_ ``resource``.
            google_signals_settings (google.analytics.admin_v1alpha.types.GoogleSignalsSettings):
                A snapshot of a GoogleSignalsSettings
                resource in change history.

                This field is a member of `oneof`_ ``resource``.
            display_video_360_advertiser_link (google.analytics.admin_v1alpha.types.DisplayVideo360AdvertiserLink):
                A snapshot of a DisplayVideo360AdvertiserLink
                resource in change history.

                This field is a member of `oneof`_ ``resource``.
            display_video_360_advertiser_link_proposal (google.analytics.admin_v1alpha.types.DisplayVideo360AdvertiserLinkProposal):
                A snapshot of a
                DisplayVideo360AdvertiserLinkProposal resource
                in change history.

                This field is a member of `oneof`_ ``resource``.
            conversion_event (google.analytics.admin_v1alpha.types.ConversionEvent):
                A snapshot of a ConversionEvent resource in
                change history.

                This field is a member of `oneof`_ ``resource``.
            measurement_protocol_secret (google.analytics.admin_v1alpha.types.MeasurementProtocolSecret):
                A snapshot of a MeasurementProtocolSecret
                resource in change history.

                This field is a member of `oneof`_ ``resource``.
            custom_dimension (google.analytics.admin_v1alpha.types.CustomDimension):
                A snapshot of a CustomDimension resource in
                change history.

                This field is a member of `oneof`_ ``resource``.
            custom_metric (google.analytics.admin_v1alpha.types.CustomMetric):
                A snapshot of a CustomMetric resource in
                change history.

                This field is a member of `oneof`_ ``resource``.
            data_retention_settings (google.analytics.admin_v1alpha.types.DataRetentionSettings):
                A snapshot of a data retention settings
                resource in change history.

                This field is a member of `oneof`_ ``resource``.
            data_stream (google.analytics.admin_v1alpha.types.DataStream):
                A snapshot of a DataStream resource in change
                history.

                This field is a member of `oneof`_ ``resource``.
            attribution_settings (google.analytics.admin_v1alpha.types.AttributionSettings):
                A snapshot of AttributionSettings resource in
                change history.

                This field is a member of `oneof`_ ``resource``.
        """

        account = proto.Field(
            proto.MESSAGE,
            number=1,
            oneof="resource",
            message="Account",
        )
        property = proto.Field(
            proto.MESSAGE,
            number=2,
            oneof="resource",
            message="Property",
        )
        firebase_link = proto.Field(
            proto.MESSAGE,
            number=6,
            oneof="resource",
            message="FirebaseLink",
        )
        google_ads_link = proto.Field(
            proto.MESSAGE,
            number=7,
            oneof="resource",
            message="GoogleAdsLink",
        )
        google_signals_settings = proto.Field(
            proto.MESSAGE,
            number=8,
            oneof="resource",
            message="GoogleSignalsSettings",
        )
        display_video_360_advertiser_link = proto.Field(
            proto.MESSAGE,
            number=9,
            oneof="resource",
            message="DisplayVideo360AdvertiserLink",
        )
        display_video_360_advertiser_link_proposal = proto.Field(
            proto.MESSAGE,
            number=10,
            oneof="resource",
            message="DisplayVideo360AdvertiserLinkProposal",
        )
        conversion_event = proto.Field(
            proto.MESSAGE,
            number=11,
            oneof="resource",
            message="ConversionEvent",
        )
        measurement_protocol_secret = proto.Field(
            proto.MESSAGE,
            number=12,
            oneof="resource",
            message="MeasurementProtocolSecret",
        )
        custom_dimension = proto.Field(
            proto.MESSAGE,
            number=13,
            oneof="resource",
            message="CustomDimension",
        )
        custom_metric = proto.Field(
            proto.MESSAGE,
            number=14,
            oneof="resource",
            message="CustomMetric",
        )
        data_retention_settings = proto.Field(
            proto.MESSAGE,
            number=15,
            oneof="resource",
            message="DataRetentionSettings",
        )
        data_stream = proto.Field(
            proto.MESSAGE,
            number=18,
            oneof="resource",
            message="DataStream",
        )
        attribution_settings = proto.Field(
            proto.MESSAGE,
            number=20,
            oneof="resource",
            message="AttributionSettings",
        )

    resource = proto.Field(
        proto.STRING,
        number=1,
    )
    action = proto.Field(
        proto.ENUM,
        number=2,
        enum="ActionType",
    )
    resource_before_change = proto.Field(
        proto.MESSAGE,
        number=3,
        message=ChangeHistoryResource,
    )
    resource_after_change = proto.Field(
        proto.MESSAGE,
        number=4,
        message=ChangeHistoryResource,
    )


class DisplayVideo360AdvertiserLink(proto.Message):
    r"""A link between a GA4 property and a Display & Video 360
    advertiser.

    Attributes:
        name (str):
            Output only. The resource name for this
            DisplayVideo360AdvertiserLink resource. Format:
            properties/{propertyId}/displayVideo360AdvertiserLinks/{linkId}
            Note: linkId is not the Display & Video 360
            Advertiser ID
        advertiser_id (str):
            Immutable. The Display & Video 360
            Advertiser's advertiser ID.
        advertiser_display_name (str):
            Output only. The display name of the Display
            & Video 360 Advertiser.
        ads_personalization_enabled (google.protobuf.wrappers_pb2.BoolValue):
            Enables personalized advertising features
            with this integration. If this field is not set
            on create/update, it will be defaulted to true.
        campaign_data_sharing_enabled (google.protobuf.wrappers_pb2.BoolValue):
            Immutable. Enables the import of campaign
            data from Display & Video 360 into the GA4
            property. After link creation, this can only be
            updated from the Display & Video 360 product.
            If this field is not set on create, it will be
            defaulted to true.
        cost_data_sharing_enabled (google.protobuf.wrappers_pb2.BoolValue):
            Immutable. Enables the import of cost data from Display &
            Video 360 into the GA4 property. This can only be enabled if
            campaign_data_sharing_enabled is enabled. After link
            creation, this can only be updated from the Display & Video
            360 product. If this field is not set on create, it will be
            defaulted to true.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    advertiser_id = proto.Field(
        proto.STRING,
        number=2,
    )
    advertiser_display_name = proto.Field(
        proto.STRING,
        number=3,
    )
    ads_personalization_enabled = proto.Field(
        proto.MESSAGE,
        number=4,
        message=wrappers_pb2.BoolValue,
    )
    campaign_data_sharing_enabled = proto.Field(
        proto.MESSAGE,
        number=5,
        message=wrappers_pb2.BoolValue,
    )
    cost_data_sharing_enabled = proto.Field(
        proto.MESSAGE,
        number=6,
        message=wrappers_pb2.BoolValue,
    )


class DisplayVideo360AdvertiserLinkProposal(proto.Message):
    r"""A proposal for a link between a GA4 property and a Display &
    Video 360 advertiser.

    A proposal is converted to a DisplayVideo360AdvertiserLink once
    approved. Google Analytics admins approve inbound proposals
    while Display & Video 360 admins approve outbound proposals.

    Attributes:
        name (str):
            Output only. The resource name for this
            DisplayVideo360AdvertiserLinkProposal resource.
            Format:
            properties/{propertyId}/displayVideo360AdvertiserLinkProposals/{proposalId}
            Note: proposalId is not the Display & Video 360
            Advertiser ID
        advertiser_id (str):
            Immutable. The Display & Video 360
            Advertiser's advertiser ID.
        link_proposal_status_details (google.analytics.admin_v1alpha.types.LinkProposalStatusDetails):
            Output only. The status information for this
            link proposal.
        advertiser_display_name (str):
            Output only. The display name of the Display
            & Video Advertiser. Only populated for proposals
            that originated from Display & Video 360.
        validation_email (str):
            Input only. On a proposal being sent to
            Display & Video 360, this field must be set to
            the email address of an admin on the target
            advertiser. This is used to verify that the
            Google Analytics admin is aware of at least one
            admin on the Display & Video 360 Advertiser.
            This does not restrict approval of the proposal
            to a single user. Any admin on the Display &
            Video 360 Advertiser may approve the proposal.
        ads_personalization_enabled (google.protobuf.wrappers_pb2.BoolValue):
            Immutable. Enables personalized advertising
            features with this integration. If this field is
            not set on create, it will be defaulted to true.
        campaign_data_sharing_enabled (google.protobuf.wrappers_pb2.BoolValue):
            Immutable. Enables the import of campaign
            data from Display & Video 360. If this field is
            not set on create, it will be defaulted to true.
        cost_data_sharing_enabled (google.protobuf.wrappers_pb2.BoolValue):
            Immutable. Enables the import of cost data from Display &
            Video 360. This can only be enabled if
            campaign_data_sharing_enabled is enabled. If this field is
            not set on create, it will be defaulted to true.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    advertiser_id = proto.Field(
        proto.STRING,
        number=2,
    )
    link_proposal_status_details = proto.Field(
        proto.MESSAGE,
        number=3,
        message="LinkProposalStatusDetails",
    )
    advertiser_display_name = proto.Field(
        proto.STRING,
        number=4,
    )
    validation_email = proto.Field(
        proto.STRING,
        number=5,
    )
    ads_personalization_enabled = proto.Field(
        proto.MESSAGE,
        number=6,
        message=wrappers_pb2.BoolValue,
    )
    campaign_data_sharing_enabled = proto.Field(
        proto.MESSAGE,
        number=7,
        message=wrappers_pb2.BoolValue,
    )
    cost_data_sharing_enabled = proto.Field(
        proto.MESSAGE,
        number=8,
        message=wrappers_pb2.BoolValue,
    )


class LinkProposalStatusDetails(proto.Message):
    r"""Status information for a link proposal.

    Attributes:
        link_proposal_initiating_product (google.analytics.admin_v1alpha.types.LinkProposalInitiatingProduct):
            Output only. The source of this proposal.
        requestor_email (str):
            Output only. The email address of the user
            that proposed this linkage.
        link_proposal_state (google.analytics.admin_v1alpha.types.LinkProposalState):
            Output only. The state of this proposal.
    """

    link_proposal_initiating_product = proto.Field(
        proto.ENUM,
        number=1,
        enum="LinkProposalInitiatingProduct",
    )
    requestor_email = proto.Field(
        proto.STRING,
        number=2,
    )
    link_proposal_state = proto.Field(
        proto.ENUM,
        number=3,
        enum="LinkProposalState",
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
        deletable (bool):
            Output only. If set, this event can currently
            be deleted via DeleteConversionEvent.
        custom (bool):
            Output only. If set to true, this conversion
            event refers to a custom event.  If set to
            false, this conversion event refers to a default
            event in GA. Default events typically have
            special meaning in GA. Default events are
            usually created for you by the GA system, but in
            some cases can be created by property admins.
            Custom events count towards the maximum number
            of custom conversion events that may be created
            per property.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    event_name = proto.Field(
        proto.STRING,
        number=2,
    )
    create_time = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    deletable = proto.Field(
        proto.BOOL,
        number=4,
    )
    custom = proto.Field(
        proto.BOOL,
        number=5,
    )


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

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    state = proto.Field(
        proto.ENUM,
        number=3,
        enum="GoogleSignalsState",
    )
    consent = proto.Field(
        proto.ENUM,
        number=4,
        enum="GoogleSignalsConsent",
    )


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
            the user property name. If this is an
            event-scoped dimension, then this is the event
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

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    parameter_name = proto.Field(
        proto.STRING,
        number=2,
    )
    display_name = proto.Field(
        proto.STRING,
        number=3,
    )
    description = proto.Field(
        proto.STRING,
        number=4,
    )
    scope = proto.Field(
        proto.ENUM,
        number=5,
        enum=DimensionScope,
    )
    disallow_ads_personalization = proto.Field(
        proto.BOOL,
        number=6,
    )


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
            Required. The type for the custom metric's
            value.
        scope (google.analytics.admin_v1alpha.types.CustomMetric.MetricScope):
            Required. Immutable. The scope of this custom
            metric.
        restricted_metric_type (Sequence[google.analytics.admin_v1alpha.types.CustomMetric.RestrictedMetricType]):
            Optional. Types of restricted data that this
            metric may contain. Required for metrics with
            CURRENCY measurement unit. Must be empty for
            metrics with a non-CURRENCY measurement unit.
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

    class RestrictedMetricType(proto.Enum):
        r"""Labels that mark the data in this custom metric as data that
        should be restricted to specific users.
        """
        RESTRICTED_METRIC_TYPE_UNSPECIFIED = 0
        COST_DATA = 1
        REVENUE_DATA = 2

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    parameter_name = proto.Field(
        proto.STRING,
        number=2,
    )
    display_name = proto.Field(
        proto.STRING,
        number=3,
    )
    description = proto.Field(
        proto.STRING,
        number=4,
    )
    measurement_unit = proto.Field(
        proto.ENUM,
        number=5,
        enum=MeasurementUnit,
    )
    scope = proto.Field(
        proto.ENUM,
        number=6,
        enum=MetricScope,
    )
    restricted_metric_type = proto.RepeatedField(
        proto.ENUM,
        number=8,
        enum=RestrictedMetricType,
    )


class DataRetentionSettings(proto.Message):
    r"""Settings values for data retention. This is a singleton
    resource.

    Attributes:
        name (str):
            Output only. Resource name for this
            DataRetentionSetting resource. Format:
            properties/{property}/dataRetentionSettings
        event_data_retention (google.analytics.admin_v1alpha.types.DataRetentionSettings.RetentionDuration):
            The length of time that event-level data is
            retained.
        reset_user_data_on_new_activity (bool):
            If true, reset the retention period for the
            user identifier with every event from that user.
    """

    class RetentionDuration(proto.Enum):
        r"""Valid values for the data retention duration."""
        RETENTION_DURATION_UNSPECIFIED = 0
        TWO_MONTHS = 1
        FOURTEEN_MONTHS = 3
        TWENTY_SIX_MONTHS = 4
        THIRTY_EIGHT_MONTHS = 5
        FIFTY_MONTHS = 6

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    event_data_retention = proto.Field(
        proto.ENUM,
        number=2,
        enum=RetentionDuration,
    )
    reset_user_data_on_new_activity = proto.Field(
        proto.BOOL,
        number=3,
    )


class AttributionSettings(proto.Message):
    r"""The attribution settings used for a given property. This is a
    singleton resource.

    Attributes:
        name (str):
            Output only. Resource name of this attribution settings
            resource. Format:
            properties/{property_id}/attributionSettings Example:
            "properties/1000/attributionSettings".
        acquisition_conversion_event_lookback_window (google.analytics.admin_v1alpha.types.AttributionSettings.AcquisitionConversionEventLookbackWindow):
            Required. The lookback window configuration
            for acquisition conversion events. The default
            window size is 30 days.
        other_conversion_event_lookback_window (google.analytics.admin_v1alpha.types.AttributionSettings.OtherConversionEventLookbackWindow):
            Required. The lookback window for all other,
            non-acquisition conversion events. The default
            window size is 90 days.
        reporting_attribution_model (google.analytics.admin_v1alpha.types.AttributionSettings.ReportingAttributionModel):
            Required. The reporting attribution model
            used to calculate conversion credit in this
            property's reports.
            Changing the attribution model will apply to
            both historical and future data. These changes
            will be reflected in reports with conversion and
            revenue data. User and session data will be
            unaffected.
    """

    class AcquisitionConversionEventLookbackWindow(proto.Enum):
        r"""How far back in time events should be considered for
        inclusion in a converting path which leads to the first install
        of an app or the first visit to a site.
        """
        ACQUISITION_CONVERSION_EVENT_LOOKBACK_WINDOW_UNSPECIFIED = 0
        ACQUISITION_CONVERSION_EVENT_LOOKBACK_WINDOW_7_DAYS = 1
        ACQUISITION_CONVERSION_EVENT_LOOKBACK_WINDOW_30_DAYS = 2

    class OtherConversionEventLookbackWindow(proto.Enum):
        r"""How far back in time events should be considered for
        inclusion in a converting path for all conversions other than
        first app install/first site visit.
        """
        OTHER_CONVERSION_EVENT_LOOKBACK_WINDOW_UNSPECIFIED = 0
        OTHER_CONVERSION_EVENT_LOOKBACK_WINDOW_30_DAYS = 1
        OTHER_CONVERSION_EVENT_LOOKBACK_WINDOW_60_DAYS = 2
        OTHER_CONVERSION_EVENT_LOOKBACK_WINDOW_90_DAYS = 3

    class ReportingAttributionModel(proto.Enum):
        r"""The reporting attribution model used to calculate conversion
        credit in this property's reports.
        """
        REPORTING_ATTRIBUTION_MODEL_UNSPECIFIED = 0
        CROSS_CHANNEL_DATA_DRIVEN = 1
        CROSS_CHANNEL_LAST_CLICK = 2
        CROSS_CHANNEL_FIRST_CLICK = 3
        CROSS_CHANNEL_LINEAR = 4
        CROSS_CHANNEL_POSITION_BASED = 5
        CROSS_CHANNEL_TIME_DECAY = 6
        ADS_PREFERRED_LAST_CLICK = 7

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    acquisition_conversion_event_lookback_window = proto.Field(
        proto.ENUM,
        number=2,
        enum=AcquisitionConversionEventLookbackWindow,
    )
    other_conversion_event_lookback_window = proto.Field(
        proto.ENUM,
        number=3,
        enum=OtherConversionEventLookbackWindow,
    )
    reporting_attribution_model = proto.Field(
        proto.ENUM,
        number=4,
        enum=ReportingAttributionModel,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
