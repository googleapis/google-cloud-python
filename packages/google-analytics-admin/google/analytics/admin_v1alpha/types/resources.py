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


from google.protobuf import timestamp_pb2 as timestamp  # type: ignore
from google.protobuf import wrappers_pb2 as wrappers  # type: ignore


__protobuf__ = proto.module(
    package="google.analytics.admin.v1alpha",
    manifest={
        "MaximumUserAccess",
        "IndustryCategory",
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


class Account(proto.Message):
    r"""A resource message representing a Google Analytics account.

    Attributes:
        name (str):
            Output only. Resource name of this account.
            Format: accounts/{account}
            Example: "accounts/100".
        create_time (~.timestamp.Timestamp):
            Output only. Time when this account was
            originally created.
        update_time (~.timestamp.Timestamp):
            Output only. Time when account payload fields
            were last updated.
        display_name (str):
            Required. Human-readable display name for
            this account.
        country_code (str):
            Country of business. Must be a non-deprecated code for a UN
            M.49 region.

            https: //unicode.org/cldr/charts/latest/supplem //
            ental/territory_containment_un_m_49.html
        deleted (bool):
            Output only. Indicates whether this Account
            is soft-deleted or not. Deleted accounts are
            excluded from List results unless specifically
            requested.
    """

    name = proto.Field(proto.STRING, number=1)

    create_time = proto.Field(proto.MESSAGE, number=2, message=timestamp.Timestamp,)

    update_time = proto.Field(proto.MESSAGE, number=3, message=timestamp.Timestamp,)

    display_name = proto.Field(proto.STRING, number=4)

    country_code = proto.Field(proto.STRING, number=5)

    deleted = proto.Field(proto.BOOL, number=6)


class Property(proto.Message):
    r"""A resource message representing a Google Analytics GA4
    property.

    Attributes:
        name (str):
            Output only. Resource name of this property. Format:
            properties/{property_id} Example: "properties/1000".
        create_time (~.timestamp.Timestamp):
            Output only. Time when the entity was
            originally created.
        update_time (~.timestamp.Timestamp):
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
        industry_category (~.resources.IndustryCategory):
            Industry associated with this property Example: AUTOMOTIVE,
            FOOD_AND_DRINK
        time_zone (str):
            Reporting Time Zone, used as the day boundary for reports,
            regardless of where the data originates. If the time zone
            honors DST, Analytics will automatically adjust for the
            changes.

            NOTE: Changing the time zone only affects data going
            forward, and is not applied retroactively.

            Format: https://www.iana.org/time-zones Example:
            "America/Los_Angeles".
        currency_code (str):
            The currency type used in reports involving monetary values.

            Format: https://en.wikipedia.org/wiki/ISO_4217 Examples:
            "USD", "EUR", "JPY".
        deleted (bool):
            Output only. Indicates whether this Property
            is soft-deleted or not. Deleted properties are
            excluded from List results unless specifically
            requested.
    """

    name = proto.Field(proto.STRING, number=1)

    create_time = proto.Field(proto.MESSAGE, number=3, message=timestamp.Timestamp,)

    update_time = proto.Field(proto.MESSAGE, number=4, message=timestamp.Timestamp,)

    parent = proto.Field(proto.STRING, number=2)

    display_name = proto.Field(proto.STRING, number=5)

    industry_category = proto.Field(proto.ENUM, number=6, enum="IndustryCategory",)

    time_zone = proto.Field(proto.STRING, number=7)

    currency_code = proto.Field(proto.STRING, number=8)

    deleted = proto.Field(proto.BOOL, number=9)


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
        create_time (~.timestamp.Timestamp):
            Output only. Time when this stream was
            originally created.
        update_time (~.timestamp.Timestamp):
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

    name = proto.Field(proto.STRING, number=1)

    firebase_app_id = proto.Field(proto.STRING, number=2)

    create_time = proto.Field(proto.MESSAGE, number=3, message=timestamp.Timestamp,)

    update_time = proto.Field(proto.MESSAGE, number=4, message=timestamp.Timestamp,)

    package_name = proto.Field(proto.STRING, number=5)

    display_name = proto.Field(proto.STRING, number=6)


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
        create_time (~.timestamp.Timestamp):
            Output only. Time when this stream was
            originally created.
        update_time (~.timestamp.Timestamp):
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

    name = proto.Field(proto.STRING, number=1)

    firebase_app_id = proto.Field(proto.STRING, number=2)

    create_time = proto.Field(proto.MESSAGE, number=3, message=timestamp.Timestamp,)

    update_time = proto.Field(proto.MESSAGE, number=4, message=timestamp.Timestamp,)

    bundle_id = proto.Field(proto.STRING, number=5)

    display_name = proto.Field(proto.STRING, number=6)


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
        create_time (~.timestamp.Timestamp):
            Output only. Time when this stream was
            originally created.
        update_time (~.timestamp.Timestamp):
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

    name = proto.Field(proto.STRING, number=1)

    measurement_id = proto.Field(proto.STRING, number=2)

    firebase_app_id = proto.Field(proto.STRING, number=3)

    create_time = proto.Field(proto.MESSAGE, number=4, message=timestamp.Timestamp,)

    update_time = proto.Field(proto.MESSAGE, number=5, message=timestamp.Timestamp,)

    default_uri = proto.Field(proto.STRING, number=6)

    display_name = proto.Field(proto.STRING, number=7)


class UserLink(proto.Message):
    r"""A resource message representing a user's permissions on an
    Account or Property resource.

    Attributes:
        name (str):
            Example format:
            properties/1234/userLinks/5678
        email_address (str):
            Email address of the user to link
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

    name = proto.Field(proto.STRING, number=1)

    email_address = proto.Field(proto.STRING, number=2)

    direct_roles = proto.RepeatedField(proto.STRING, number=3)


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

    name = proto.Field(proto.STRING, number=1)

    email_address = proto.Field(proto.STRING, number=2)

    direct_roles = proto.RepeatedField(proto.STRING, number=3)

    effective_roles = proto.RepeatedField(proto.STRING, number=4)


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
        content_views_enabled (bool):
            Capture events when your visitors view
            content on your site that has structured data
            (eg, articles, blog posts, product details
            screens, etc.).
        site_search_enabled (bool):
            If enabled, capture a view search results
            event each time a visitor performs a search on
            your site (based on a query parameter).
        form_interactions_enabled (bool):
            If enabled, capture a view search results
            event each time a visitor interacts with a form
            on your site.
        video_engagement_enabled (bool):
            If enabled, capture video play, progress, and
            complete events as visitors view embedded videos
            on your site.
        file_downloads_enabled (bool):
            If enabled, capture a file download event
            each time a link is clicked with a common
            document, compressed file, application, video,
            or audio extension.
        data_tagged_element_clicks_enabled (bool):
            If enabled, capture a click event each time a
            visitor clicks a link or element that has data
            attributes beginning with "data-ga".
        page_loads_enabled (bool):
            If enabled, capture a page view event each
            time a page loads.
        page_changes_enabled (bool):
            If enabled, capture a page view event each
            time the website changes the browser history
            state.
        articles_and_blogs_enabled (bool):
            Capture events when your visitors view
            content on your site that has articles or blog
            posts.
        products_and_ecommerce_enabled (bool):
            Capture events when your visitors view
            content on your site that has product details
            screens, etc.
        search_query_parameter (str):
            Required. URL query parameters to interpret
            as site search parameters. Max length is 1024
            characters. Must not be empty.
        url_query_parameter (str):
            Additional URL query parameters.
            Max length is 1024 characters.
        excluded_domains (str):
            Domains to exclude from measurement. Max
            length is 1024 characters.
    """

    name = proto.Field(proto.STRING, number=1)

    stream_enabled = proto.Field(proto.BOOL, number=2)

    page_views_enabled = proto.Field(proto.BOOL, number=3)

    scrolls_enabled = proto.Field(proto.BOOL, number=4)

    outbound_clicks_enabled = proto.Field(proto.BOOL, number=5)

    content_views_enabled = proto.Field(proto.BOOL, number=6)

    site_search_enabled = proto.Field(proto.BOOL, number=7)

    form_interactions_enabled = proto.Field(proto.BOOL, number=8)

    video_engagement_enabled = proto.Field(proto.BOOL, number=9)

    file_downloads_enabled = proto.Field(proto.BOOL, number=10)

    data_tagged_element_clicks_enabled = proto.Field(proto.BOOL, number=11)

    page_loads_enabled = proto.Field(proto.BOOL, number=12)

    page_changes_enabled = proto.Field(proto.BOOL, number=13)

    articles_and_blogs_enabled = proto.Field(proto.BOOL, number=14)

    products_and_ecommerce_enabled = proto.Field(proto.BOOL, number=15)

    search_query_parameter = proto.Field(proto.STRING, number=16)

    url_query_parameter = proto.Field(proto.STRING, number=17)

    excluded_domains = proto.Field(proto.STRING, number=18)


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
        create_time (~.timestamp.Timestamp):
            Output only. Time when this FirebaseLink was
            originally created.
        maximum_user_access (~.resources.MaximumUserAccess):
            Maximum user access to the GA4 property
            allowed to admins of the linked Firebase
            project.
    """

    name = proto.Field(proto.STRING, number=1)

    project = proto.Field(proto.STRING, number=2)

    create_time = proto.Field(proto.MESSAGE, number=3, message=timestamp.Timestamp,)

    maximum_user_access = proto.Field(proto.ENUM, number=4, enum="MaximumUserAccess",)


class GlobalSiteTag(proto.Message):
    r"""Read-only resource with the tag for sending data from a
    website to a WebDataStream.

    Attributes:
        snippet (str):
            Immutable. JavaScript code snippet to be
            pasted as the first item into the head tag of
            every webpage to measure.
        name (str):
            The resource name of this tag.
    """

    snippet = proto.Field(proto.STRING, number=1)

    name = proto.Field(proto.STRING, number=2)


class GoogleAdsLink(proto.Message):
    r"""A link between an GA4 property and a Google Ads account.

    Attributes:
        name (str):
            Output only. Format:
            properties/{propertyId}/googleAdsLinks/{googleAdsLinkId}
            Note: googleAdsLinkId is not the Google Ads
            customer ID.
        parent (str):
            Immutable. Format: properties/{propertyId}
        customer_id (str):
            Immutable. Google Ads customer ID.
        can_manage_clients (bool):
            Output only. If true, this link is for a
            Google Ads manager account.
        ads_personalization_enabled (~.wrappers.BoolValue):
            Enable personalized advertising features with
            this integration. Automatically publish my
            Google Analytics audience lists and Google
            Analytics remarketing events/parameters to the
            linked Google Ads account. If this field is not
            set on create/update it will be defaulted to
            true.
        email_address (str):
            Output only. Email address of the user that
            created the link. An empty string will be
            returned if the email address can't be
            retrieved.
        create_time (~.timestamp.Timestamp):
            Output only. Time when this link was
            originally created.
        update_time (~.timestamp.Timestamp):
            Output only. Time when this link was last
            updated.
    """

    name = proto.Field(proto.STRING, number=1)

    parent = proto.Field(proto.STRING, number=2)

    customer_id = proto.Field(proto.STRING, number=3)

    can_manage_clients = proto.Field(proto.BOOL, number=4)

    ads_personalization_enabled = proto.Field(
        proto.MESSAGE, number=5, message=wrappers.BoolValue,
    )

    email_address = proto.Field(proto.STRING, number=6)

    create_time = proto.Field(proto.MESSAGE, number=7, message=timestamp.Timestamp,)

    update_time = proto.Field(proto.MESSAGE, number=8, message=timestamp.Timestamp,)


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

    name = proto.Field(proto.STRING, number=1)

    sharing_with_google_support_enabled = proto.Field(proto.BOOL, number=2)

    sharing_with_google_assigned_sales_enabled = proto.Field(proto.BOOL, number=3)

    sharing_with_google_any_sales_enabled = proto.Field(proto.BOOL, number=4)

    sharing_with_google_products_enabled = proto.Field(proto.BOOL, number=5)

    sharing_with_others_enabled = proto.Field(proto.BOOL, number=6)


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
        property_summaries (Sequence[~.resources.PropertySummary]):
            List of summaries for child accounts of this
            account.
    """

    name = proto.Field(proto.STRING, number=1)

    account = proto.Field(proto.STRING, number=2)

    display_name = proto.Field(proto.STRING, number=3)

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

    property = proto.Field(proto.STRING, number=1)

    display_name = proto.Field(proto.STRING, number=2)


__all__ = tuple(sorted(__protobuf__.manifest))
