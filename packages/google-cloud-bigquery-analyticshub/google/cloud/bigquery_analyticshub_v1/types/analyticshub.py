# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.bigquery.analyticshub.v1",
    manifest={
        "DiscoveryType",
        "DataExchange",
        "SharingEnvironmentConfig",
        "DataProvider",
        "Publisher",
        "DestinationDatasetReference",
        "DestinationDataset",
        "Listing",
        "Subscription",
        "ListDataExchangesRequest",
        "ListDataExchangesResponse",
        "ListOrgDataExchangesRequest",
        "ListOrgDataExchangesResponse",
        "GetDataExchangeRequest",
        "CreateDataExchangeRequest",
        "UpdateDataExchangeRequest",
        "DeleteDataExchangeRequest",
        "ListListingsRequest",
        "ListListingsResponse",
        "GetListingRequest",
        "CreateListingRequest",
        "UpdateListingRequest",
        "DeleteListingRequest",
        "SubscribeListingRequest",
        "SubscribeListingResponse",
        "SubscribeDataExchangeRequest",
        "SubscribeDataExchangeResponse",
        "RefreshSubscriptionRequest",
        "RefreshSubscriptionResponse",
        "GetSubscriptionRequest",
        "ListSubscriptionsRequest",
        "ListSubscriptionsResponse",
        "ListSharedResourceSubscriptionsRequest",
        "ListSharedResourceSubscriptionsResponse",
        "RevokeSubscriptionRequest",
        "RevokeSubscriptionResponse",
        "DeleteSubscriptionRequest",
        "OperationMetadata",
    },
)


class DiscoveryType(proto.Enum):
    r"""Specifies the type of discovery on the discovery page. Note
    that this does not control the visibility of the
    exchange/listing which is defined by IAM permission.

    Values:
        DISCOVERY_TYPE_UNSPECIFIED (0):
            Unspecified. Defaults to DISCOVERY_TYPE_PRIVATE.
        DISCOVERY_TYPE_PRIVATE (1):
            The Data exchange/listing can be discovered
            in the 'Private' results list.
        DISCOVERY_TYPE_PUBLIC (2):
            The Data exchange/listing can be discovered
            in the 'Public' results list.
    """
    DISCOVERY_TYPE_UNSPECIFIED = 0
    DISCOVERY_TYPE_PRIVATE = 1
    DISCOVERY_TYPE_PUBLIC = 2


class DataExchange(proto.Message):
    r"""A data exchange is a container that lets you share data.
    Along with the descriptive information about the data exchange,
    it contains listings that reference shared datasets.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Output only. The resource name of the data exchange. e.g.
            ``projects/myproject/locations/US/dataExchanges/123``.
        display_name (str):
            Required. Human-readable display name of the data exchange.
            The display name must contain only Unicode letters, numbers
            (0-9), underscores (_), dashes (-), spaces ( ), ampersands
            (&) and must not start or end with spaces. Default value is
            an empty string. Max length: 63 bytes.
        description (str):
            Optional. Description of the data exchange.
            The description must not contain Unicode
            non-characters as well as C0 and C1 control
            codes except tabs (HT), new lines (LF), carriage
            returns (CR), and page breaks (FF). Default
            value is an empty string.
            Max length: 2000 bytes.
        primary_contact (str):
            Optional. Email or URL of the primary point
            of contact of the data exchange. Max Length:
            1000 bytes.
        documentation (str):
            Optional. Documentation describing the data
            exchange.
        listing_count (int):
            Output only. Number of listings contained in
            the data exchange.
        icon (bytes):
            Optional. Base64 encoded image representing
            the data exchange. Max Size: 3.0MiB Expected
            image dimensions are 512x512 pixels, however the
            API only performs validation on size of the
            encoded data. Note: For byte fields, the content
            of the fields are base64-encoded (which
            increases the size of the data by 33-36%) when
            using JSON on the wire.
        sharing_environment_config (google.cloud.bigquery_analyticshub_v1.types.SharingEnvironmentConfig):
            Optional. Configurable data sharing
            environment option for a data exchange.
        discovery_type (google.cloud.bigquery_analyticshub_v1.types.DiscoveryType):
            Optional. Type of discovery on the discovery page for all
            the listings under this exchange. Updating this field also
            updates (overwrites) the discovery_type field for all the
            listings under this exchange.

            This field is a member of `oneof`_ ``_discovery_type``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=2,
    )
    description: str = proto.Field(
        proto.STRING,
        number=3,
    )
    primary_contact: str = proto.Field(
        proto.STRING,
        number=4,
    )
    documentation: str = proto.Field(
        proto.STRING,
        number=5,
    )
    listing_count: int = proto.Field(
        proto.INT32,
        number=6,
    )
    icon: bytes = proto.Field(
        proto.BYTES,
        number=7,
    )
    sharing_environment_config: "SharingEnvironmentConfig" = proto.Field(
        proto.MESSAGE,
        number=8,
        message="SharingEnvironmentConfig",
    )
    discovery_type: "DiscoveryType" = proto.Field(
        proto.ENUM,
        number=9,
        optional=True,
        enum="DiscoveryType",
    )


class SharingEnvironmentConfig(proto.Message):
    r"""Sharing environment is a behavior model for sharing data
    within a data exchange. This option is configurable for a data
    exchange.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        default_exchange_config (google.cloud.bigquery_analyticshub_v1.types.SharingEnvironmentConfig.DefaultExchangeConfig):
            Default Analytics Hub data exchange, used for
            secured data sharing.

            This field is a member of `oneof`_ ``environment``.
        dcr_exchange_config (google.cloud.bigquery_analyticshub_v1.types.SharingEnvironmentConfig.DcrExchangeConfig):
            Data Clean Room (DCR), used for privacy-safe
            and secured data sharing.

            This field is a member of `oneof`_ ``environment``.
    """

    class DefaultExchangeConfig(proto.Message):
        r"""Default Analytics Hub data exchange, used for secured data
        sharing.

        """

    class DcrExchangeConfig(proto.Message):
        r"""Data Clean Room (DCR), used for privacy-safe and secured data
        sharing.


        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            single_selected_resource_sharing_restriction (bool):
                Output only. If True, this DCR restricts the
                contributors to sharing only a single resource
                in a Listing. And no two resources should have
                the same IDs. So if a contributor adds a view
                with a conflicting name, the CreateListing API
                will reject the request. if False, the data
                contributor can publish an entire dataset (as
                before). This is not configurable, and by
                default, all new DCRs will have the restriction
                set to True.

                This field is a member of `oneof`_ ``_single_selected_resource_sharing_restriction``.
            single_linked_dataset_per_cleanroom (bool):
                Output only. If True, when subscribing to
                this DCR, it will create only one linked dataset
                containing all resources shared within the
                cleanroom. If False, when subscribing to this
                DCR, it will create 1 linked dataset per
                listing. This is not configurable, and by
                default, all new DCRs will have the restriction
                set to True.

                This field is a member of `oneof`_ ``_single_linked_dataset_per_cleanroom``.
        """

        single_selected_resource_sharing_restriction: bool = proto.Field(
            proto.BOOL,
            number=1,
            optional=True,
        )
        single_linked_dataset_per_cleanroom: bool = proto.Field(
            proto.BOOL,
            number=2,
            optional=True,
        )

    default_exchange_config: DefaultExchangeConfig = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="environment",
        message=DefaultExchangeConfig,
    )
    dcr_exchange_config: DcrExchangeConfig = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="environment",
        message=DcrExchangeConfig,
    )


class DataProvider(proto.Message):
    r"""Contains details of the data provider.

    Attributes:
        name (str):
            Optional. Name of the data provider.
        primary_contact (str):
            Optional. Email or URL of the data provider.
            Max Length: 1000 bytes.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    primary_contact: str = proto.Field(
        proto.STRING,
        number=2,
    )


class Publisher(proto.Message):
    r"""Contains details of the listing publisher.

    Attributes:
        name (str):
            Optional. Name of the listing publisher.
        primary_contact (str):
            Optional. Email or URL of the listing
            publisher. Max Length: 1000 bytes.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    primary_contact: str = proto.Field(
        proto.STRING,
        number=2,
    )


class DestinationDatasetReference(proto.Message):
    r"""Contains the reference that identifies a destination bigquery
    dataset.

    Attributes:
        dataset_id (str):
            Required. A unique ID for this dataset, without the project
            name. The ID must contain only letters (a-z, A-Z), numbers
            (0-9), or underscores (_). The maximum length is 1,024
            characters.
        project_id (str):
            Required. The ID of the project containing
            this dataset.
    """

    dataset_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    project_id: str = proto.Field(
        proto.STRING,
        number=2,
    )


class DestinationDataset(proto.Message):
    r"""Defines the destination bigquery dataset.

    Attributes:
        dataset_reference (google.cloud.bigquery_analyticshub_v1.types.DestinationDatasetReference):
            Required. A reference that identifies the
            destination dataset.
        friendly_name (google.protobuf.wrappers_pb2.StringValue):
            Optional. A descriptive name for the dataset.
        description (google.protobuf.wrappers_pb2.StringValue):
            Optional. A user-friendly description of the
            dataset.
        labels (MutableMapping[str, str]):
            Optional. The labels associated with this
            dataset. You can use these to organize and group
            your datasets. You can set this property when
            inserting or updating a dataset. See
            https://cloud.google.com/resource-manager/docs/creating-managing-labels
            for more information.
        location (str):
            Required. The geographic location where the
            dataset should reside. See
            https://cloud.google.com/bigquery/docs/locations
            for supported locations.
    """

    dataset_reference: "DestinationDatasetReference" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="DestinationDatasetReference",
    )
    friendly_name: wrappers_pb2.StringValue = proto.Field(
        proto.MESSAGE,
        number=2,
        message=wrappers_pb2.StringValue,
    )
    description: wrappers_pb2.StringValue = proto.Field(
        proto.MESSAGE,
        number=3,
        message=wrappers_pb2.StringValue,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=4,
    )
    location: str = proto.Field(
        proto.STRING,
        number=5,
    )


class Listing(proto.Message):
    r"""A listing is what gets published into a data exchange that a
    subscriber can subscribe to. It contains a reference to the data
    source along with descriptive information that will help
    subscribers find and subscribe the data.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        bigquery_dataset (google.cloud.bigquery_analyticshub_v1.types.Listing.BigQueryDatasetSource):
            Required. Shared dataset i.e. BigQuery
            dataset source.

            This field is a member of `oneof`_ ``source``.
        name (str):
            Output only. The resource name of the listing. e.g.
            ``projects/myproject/locations/US/dataExchanges/123/listings/456``
        display_name (str):
            Required. Human-readable display name of the listing. The
            display name must contain only Unicode letters, numbers
            (0-9), underscores (_), dashes (-), spaces ( ), ampersands
            (&) and can't start or end with spaces. Default value is an
            empty string. Max length: 63 bytes.
        description (str):
            Optional. Short description of the listing.
            The description must not contain Unicode
            non-characters and C0 and C1 control codes
            except tabs (HT), new lines (LF), carriage
            returns (CR), and page breaks (FF). Default
            value is an empty string. Max length: 2000
            bytes.
        primary_contact (str):
            Optional. Email or URL of the primary point
            of contact of the listing. Max Length: 1000
            bytes.
        documentation (str):
            Optional. Documentation describing the
            listing.
        state (google.cloud.bigquery_analyticshub_v1.types.Listing.State):
            Output only. Current state of the listing.
        icon (bytes):
            Optional. Base64 encoded image representing
            the listing. Max Size: 3.0MiB Expected image
            dimensions are 512x512 pixels, however the API
            only performs validation on size of the encoded
            data. Note: For byte fields, the contents of the
            field are base64-encoded (which increases the
            size of the data by 33-36%) when using JSON on
            the wire.
        data_provider (google.cloud.bigquery_analyticshub_v1.types.DataProvider):
            Optional. Details of the data provider who
            owns the source data.
        categories (MutableSequence[google.cloud.bigquery_analyticshub_v1.types.Listing.Category]):
            Optional. Categories of the listing. Up to
            two categories are allowed.
        publisher (google.cloud.bigquery_analyticshub_v1.types.Publisher):
            Optional. Details of the publisher who owns
            the listing and who can share the source data.
        request_access (str):
            Optional. Email or URL of the request access
            of the listing. Subscribers can use this
            reference to request access. Max Length: 1000
            bytes.
        restricted_export_config (google.cloud.bigquery_analyticshub_v1.types.Listing.RestrictedExportConfig):
            Optional. If set, restricted export
            configuration will be propagated and enforced on
            the linked dataset.
        discovery_type (google.cloud.bigquery_analyticshub_v1.types.DiscoveryType):
            Optional. Type of discovery of the listing on
            the discovery page.

            This field is a member of `oneof`_ ``_discovery_type``.
    """

    class State(proto.Enum):
        r"""State of the listing.

        Values:
            STATE_UNSPECIFIED (0):
                Default value. This value is unused.
            ACTIVE (1):
                Subscribable state. Users with
                dataexchange.listings.subscribe permission can
                subscribe to this listing.
        """
        STATE_UNSPECIFIED = 0
        ACTIVE = 1

    class Category(proto.Enum):
        r"""Listing categories.

        Values:
            CATEGORY_UNSPECIFIED (0):
                No description available.
            CATEGORY_OTHERS (1):
                No description available.
            CATEGORY_ADVERTISING_AND_MARKETING (2):
                No description available.
            CATEGORY_COMMERCE (3):
                No description available.
            CATEGORY_CLIMATE_AND_ENVIRONMENT (4):
                No description available.
            CATEGORY_DEMOGRAPHICS (5):
                No description available.
            CATEGORY_ECONOMICS (6):
                No description available.
            CATEGORY_EDUCATION (7):
                No description available.
            CATEGORY_ENERGY (8):
                No description available.
            CATEGORY_FINANCIAL (9):
                No description available.
            CATEGORY_GAMING (10):
                No description available.
            CATEGORY_GEOSPATIAL (11):
                No description available.
            CATEGORY_HEALTHCARE_AND_LIFE_SCIENCE (12):
                No description available.
            CATEGORY_MEDIA (13):
                No description available.
            CATEGORY_PUBLIC_SECTOR (14):
                No description available.
            CATEGORY_RETAIL (15):
                No description available.
            CATEGORY_SPORTS (16):
                No description available.
            CATEGORY_SCIENCE_AND_RESEARCH (17):
                No description available.
            CATEGORY_TRANSPORTATION_AND_LOGISTICS (18):
                No description available.
            CATEGORY_TRAVEL_AND_TOURISM (19):
                No description available.
        """
        CATEGORY_UNSPECIFIED = 0
        CATEGORY_OTHERS = 1
        CATEGORY_ADVERTISING_AND_MARKETING = 2
        CATEGORY_COMMERCE = 3
        CATEGORY_CLIMATE_AND_ENVIRONMENT = 4
        CATEGORY_DEMOGRAPHICS = 5
        CATEGORY_ECONOMICS = 6
        CATEGORY_EDUCATION = 7
        CATEGORY_ENERGY = 8
        CATEGORY_FINANCIAL = 9
        CATEGORY_GAMING = 10
        CATEGORY_GEOSPATIAL = 11
        CATEGORY_HEALTHCARE_AND_LIFE_SCIENCE = 12
        CATEGORY_MEDIA = 13
        CATEGORY_PUBLIC_SECTOR = 14
        CATEGORY_RETAIL = 15
        CATEGORY_SPORTS = 16
        CATEGORY_SCIENCE_AND_RESEARCH = 17
        CATEGORY_TRANSPORTATION_AND_LOGISTICS = 18
        CATEGORY_TRAVEL_AND_TOURISM = 19

    class BigQueryDatasetSource(proto.Message):
        r"""A reference to a shared dataset. It is an existing BigQuery dataset
        with a collection of objects such as tables and views that you want
        to share with subscribers. When subscriber's subscribe to a listing,
        Analytics Hub creates a linked dataset in the subscriber's project.
        A Linked dataset is an opaque, read-only BigQuery dataset that
        serves as a *symbolic link* to a shared dataset.

        Attributes:
            dataset (str):
                Resource name of the dataset source for this listing. e.g.
                ``projects/myproject/datasets/123``
            selected_resources (MutableSequence[google.cloud.bigquery_analyticshub_v1.types.Listing.BigQueryDatasetSource.SelectedResource]):
                Optional. Resources in this dataset that are
                selectively shared. If this field is empty, then
                the entire dataset (all resources) are shared.
                This field is only valid for data clean room
                exchanges.
            restricted_export_policy (google.cloud.bigquery_analyticshub_v1.types.Listing.BigQueryDatasetSource.RestrictedExportPolicy):
                Optional. If set, restricted export policy
                will be propagated and enforced on the linked
                dataset.
        """

        class SelectedResource(proto.Message):
            r"""Resource in this dataset that are selectively shared.

            .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

            Attributes:
                table (str):
                    Optional. Format: For table:
                    ``projects/{projectId}/datasets/{datasetId}/tables/{tableId}``
                    Example:"projects/test_project/datasets/test_dataset/tables/test_table".

                    This field is a member of `oneof`_ ``resource``.
            """

            table: str = proto.Field(
                proto.STRING,
                number=1,
                oneof="resource",
            )

        class RestrictedExportPolicy(proto.Message):
            r"""Restricted export policy used to configure restricted export
            on linked dataset.

            Attributes:
                enabled (google.protobuf.wrappers_pb2.BoolValue):
                    Optional. If true, enable restricted export.
                restrict_direct_table_access (google.protobuf.wrappers_pb2.BoolValue):
                    Optional. If true, restrict direct table
                    access (read api/tabledata.list) on linked
                    table.
                restrict_query_result (google.protobuf.wrappers_pb2.BoolValue):
                    Optional. If true, restrict export of query
                    result derived from restricted linked dataset
                    table.
            """

            enabled: wrappers_pb2.BoolValue = proto.Field(
                proto.MESSAGE,
                number=1,
                message=wrappers_pb2.BoolValue,
            )
            restrict_direct_table_access: wrappers_pb2.BoolValue = proto.Field(
                proto.MESSAGE,
                number=2,
                message=wrappers_pb2.BoolValue,
            )
            restrict_query_result: wrappers_pb2.BoolValue = proto.Field(
                proto.MESSAGE,
                number=3,
                message=wrappers_pb2.BoolValue,
            )

        dataset: str = proto.Field(
            proto.STRING,
            number=1,
        )
        selected_resources: MutableSequence[
            "Listing.BigQueryDatasetSource.SelectedResource"
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=2,
            message="Listing.BigQueryDatasetSource.SelectedResource",
        )
        restricted_export_policy: "Listing.BigQueryDatasetSource.RestrictedExportPolicy" = proto.Field(
            proto.MESSAGE,
            number=3,
            message="Listing.BigQueryDatasetSource.RestrictedExportPolicy",
        )

    class RestrictedExportConfig(proto.Message):
        r"""Restricted export config, used to configure restricted export
        on linked dataset.

        Attributes:
            enabled (bool):
                Optional. If true, enable restricted export.
            restrict_direct_table_access (bool):
                Output only. If true, restrict direct table
                access(read api/tabledata.list) on linked table.
            restrict_query_result (bool):
                Optional. If true, restrict export of query
                result derived from restricted linked dataset
                table.
        """

        enabled: bool = proto.Field(
            proto.BOOL,
            number=3,
        )
        restrict_direct_table_access: bool = proto.Field(
            proto.BOOL,
            number=1,
        )
        restrict_query_result: bool = proto.Field(
            proto.BOOL,
            number=2,
        )

    bigquery_dataset: BigQueryDatasetSource = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="source",
        message=BigQueryDatasetSource,
    )
    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=2,
    )
    description: str = proto.Field(
        proto.STRING,
        number=3,
    )
    primary_contact: str = proto.Field(
        proto.STRING,
        number=4,
    )
    documentation: str = proto.Field(
        proto.STRING,
        number=5,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=7,
        enum=State,
    )
    icon: bytes = proto.Field(
        proto.BYTES,
        number=8,
    )
    data_provider: "DataProvider" = proto.Field(
        proto.MESSAGE,
        number=9,
        message="DataProvider",
    )
    categories: MutableSequence[Category] = proto.RepeatedField(
        proto.ENUM,
        number=10,
        enum=Category,
    )
    publisher: "Publisher" = proto.Field(
        proto.MESSAGE,
        number=11,
        message="Publisher",
    )
    request_access: str = proto.Field(
        proto.STRING,
        number=12,
    )
    restricted_export_config: RestrictedExportConfig = proto.Field(
        proto.MESSAGE,
        number=13,
        message=RestrictedExportConfig,
    )
    discovery_type: "DiscoveryType" = proto.Field(
        proto.ENUM,
        number=14,
        optional=True,
        enum="DiscoveryType",
    )


class Subscription(proto.Message):
    r"""A subscription represents a subscribers' access to a
    particular set of published data. It contains references to
    associated listings, data exchanges, and linked datasets.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        listing (str):
            Output only. Resource name of the source
            Listing. e.g.
            projects/123/locations/US/dataExchanges/456/listings/789

            This field is a member of `oneof`_ ``resource_name``.
        data_exchange (str):
            Output only. Resource name of the source Data
            Exchange. e.g.
            projects/123/locations/US/dataExchanges/456

            This field is a member of `oneof`_ ``resource_name``.
        name (str):
            Output only. The resource name of the subscription. e.g.
            ``projects/myproject/locations/US/subscriptions/123``.
        creation_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Timestamp when the subscription
            was created.
        last_modify_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Timestamp when the subscription
            was last modified.
        organization_id (str):
            Output only. Organization of the project this
            subscription belongs to.
        organization_display_name (str):
            Output only. Display name of the project of
            this subscription.
        state (google.cloud.bigquery_analyticshub_v1.types.Subscription.State):
            Output only. Current state of the
            subscription.
        linked_dataset_map (MutableMapping[str, google.cloud.bigquery_analyticshub_v1.types.Subscription.LinkedResource]):
            Output only. Map of listing resource names to associated
            linked resource, e.g.
            projects/123/locations/US/dataExchanges/456/listings/789 ->
            projects/123/datasets/my_dataset

            For listing-level subscriptions, this is a map of size 1.
            Only contains values if state == STATE_ACTIVE.
        subscriber_contact (str):
            Output only. Email of the subscriber.
    """

    class State(proto.Enum):
        r"""State of the subscription.

        Values:
            STATE_UNSPECIFIED (0):
                Default value. This value is unused.
            STATE_ACTIVE (1):
                This subscription is active and the data is
                accessible.
            STATE_STALE (2):
                The data referenced by this subscription is
                out of date and should be refreshed. This can
                happen when a data provider adds or removes
                datasets.
            STATE_INACTIVE (3):
                This subscription has been cancelled or
                revoked and the data is no longer accessible.
        """
        STATE_UNSPECIFIED = 0
        STATE_ACTIVE = 1
        STATE_STALE = 2
        STATE_INACTIVE = 3

    class LinkedResource(proto.Message):
        r"""Reference to a linked resource tracked by this Subscription.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            linked_dataset (str):
                Output only. Name of the linked dataset, e.g.
                projects/subscriberproject/datasets/linked_dataset

                This field is a member of `oneof`_ ``reference``.
        """

        linked_dataset: str = proto.Field(
            proto.STRING,
            number=1,
            oneof="reference",
        )

    listing: str = proto.Field(
        proto.STRING,
        number=5,
        oneof="resource_name",
    )
    data_exchange: str = proto.Field(
        proto.STRING,
        number=6,
        oneof="resource_name",
    )
    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    creation_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    last_modify_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    organization_id: str = proto.Field(
        proto.STRING,
        number=4,
    )
    organization_display_name: str = proto.Field(
        proto.STRING,
        number=10,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=7,
        enum=State,
    )
    linked_dataset_map: MutableMapping[str, LinkedResource] = proto.MapField(
        proto.STRING,
        proto.MESSAGE,
        number=8,
        message=LinkedResource,
    )
    subscriber_contact: str = proto.Field(
        proto.STRING,
        number=9,
    )


class ListDataExchangesRequest(proto.Message):
    r"""Message for requesting the list of data exchanges.

    Attributes:
        parent (str):
            Required. The parent resource path of the data exchanges.
            e.g. ``projects/myproject/locations/US``.
        page_size (int):
            The maximum number of results to return in a
            single response page. Leverage the page tokens
            to iterate through the entire collection.
        page_token (str):
            Page token, returned by a previous call, to
            request the next page of results.
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


class ListDataExchangesResponse(proto.Message):
    r"""Message for response to the list of data exchanges.

    Attributes:
        data_exchanges (MutableSequence[google.cloud.bigquery_analyticshub_v1.types.DataExchange]):
            The list of data exchanges.
        next_page_token (str):
            A token to request the next page of results.
    """

    @property
    def raw_page(self):
        return self

    data_exchanges: MutableSequence["DataExchange"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="DataExchange",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ListOrgDataExchangesRequest(proto.Message):
    r"""Message for requesting the list of data exchanges from
    projects in an organization and location.

    Attributes:
        organization (str):
            Required. The organization resource path of the projects
            containing DataExchanges. e.g.
            ``organizations/myorg/locations/US``.
        page_size (int):
            The maximum number of results to return in a
            single response page. Leverage the page tokens
            to iterate through the entire collection.
        page_token (str):
            Page token, returned by a previous call, to
            request the next page of results.
    """

    organization: str = proto.Field(
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


class ListOrgDataExchangesResponse(proto.Message):
    r"""Message for response to listing data exchanges in an
    organization and location.

    Attributes:
        data_exchanges (MutableSequence[google.cloud.bigquery_analyticshub_v1.types.DataExchange]):
            The list of data exchanges.
        next_page_token (str):
            A token to request the next page of results.
    """

    @property
    def raw_page(self):
        return self

    data_exchanges: MutableSequence["DataExchange"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="DataExchange",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetDataExchangeRequest(proto.Message):
    r"""Message for getting a data exchange.

    Attributes:
        name (str):
            Required. The resource name of the data exchange. e.g.
            ``projects/myproject/locations/US/dataExchanges/123``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateDataExchangeRequest(proto.Message):
    r"""Message for creating a data exchange.

    Attributes:
        parent (str):
            Required. The parent resource path of the data exchange.
            e.g. ``projects/myproject/locations/US``.
        data_exchange_id (str):
            Required. The ID of the data exchange. Must contain only
            Unicode letters, numbers (0-9), underscores (_). Should not
            use characters that require URL-escaping, or characters
            outside of ASCII, spaces. Max length: 100 bytes.
        data_exchange (google.cloud.bigquery_analyticshub_v1.types.DataExchange):
            Required. The data exchange to create.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    data_exchange_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    data_exchange: "DataExchange" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="DataExchange",
    )


class UpdateDataExchangeRequest(proto.Message):
    r"""Message for updating a data exchange.

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Field mask specifies the fields to update in the
            data exchange resource. The fields specified in the
            ``updateMask`` are relative to the resource and are not a
            full request.
        data_exchange (google.cloud.bigquery_analyticshub_v1.types.DataExchange):
            Required. The data exchange to update.
    """

    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=1,
        message=field_mask_pb2.FieldMask,
    )
    data_exchange: "DataExchange" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="DataExchange",
    )


class DeleteDataExchangeRequest(proto.Message):
    r"""Message for deleting a data exchange.

    Attributes:
        name (str):
            Required. The full name of the data exchange resource that
            you want to delete. For example,
            ``projects/myproject/locations/US/dataExchanges/123``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListListingsRequest(proto.Message):
    r"""Message for requesting the list of listings.

    Attributes:
        parent (str):
            Required. The parent resource path of the listing. e.g.
            ``projects/myproject/locations/US/dataExchanges/123``.
        page_size (int):
            The maximum number of results to return in a
            single response page. Leverage the page tokens
            to iterate through the entire collection.
        page_token (str):
            Page token, returned by a previous call, to
            request the next page of results.
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


class ListListingsResponse(proto.Message):
    r"""Message for response to the list of Listings.

    Attributes:
        listings (MutableSequence[google.cloud.bigquery_analyticshub_v1.types.Listing]):
            The list of Listing.
        next_page_token (str):
            A token to request the next page of results.
    """

    @property
    def raw_page(self):
        return self

    listings: MutableSequence["Listing"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Listing",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetListingRequest(proto.Message):
    r"""Message for getting a listing.

    Attributes:
        name (str):
            Required. The resource name of the listing. e.g.
            ``projects/myproject/locations/US/dataExchanges/123/listings/456``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateListingRequest(proto.Message):
    r"""Message for creating a listing.

    Attributes:
        parent (str):
            Required. The parent resource path of the listing. e.g.
            ``projects/myproject/locations/US/dataExchanges/123``.
        listing_id (str):
            Required. The ID of the listing to create. Must contain only
            Unicode letters, numbers (0-9), underscores (_). Should not
            use characters that require URL-escaping, or characters
            outside of ASCII, spaces. Max length: 100 bytes.
        listing (google.cloud.bigquery_analyticshub_v1.types.Listing):
            Required. The listing to create.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    listing_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    listing: "Listing" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="Listing",
    )


class UpdateListingRequest(proto.Message):
    r"""Message for updating a Listing.

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Field mask specifies the fields to update in the
            listing resource. The fields specified in the ``updateMask``
            are relative to the resource and are not a full request.
        listing (google.cloud.bigquery_analyticshub_v1.types.Listing):
            Required. The listing to update.
    """

    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=1,
        message=field_mask_pb2.FieldMask,
    )
    listing: "Listing" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Listing",
    )


class DeleteListingRequest(proto.Message):
    r"""Message for deleting a listing.

    Attributes:
        name (str):
            Required. Resource name of the listing to delete. e.g.
            ``projects/myproject/locations/US/dataExchanges/123/listings/456``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class SubscribeListingRequest(proto.Message):
    r"""Message for subscribing to a listing.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        destination_dataset (google.cloud.bigquery_analyticshub_v1.types.DestinationDataset):
            Input only. BigQuery destination dataset to
            create for the subscriber.

            This field is a member of `oneof`_ ``destination``.
        name (str):
            Required. Resource name of the listing that you want to
            subscribe to. e.g.
            ``projects/myproject/locations/US/dataExchanges/123/listings/456``.
    """

    destination_dataset: "DestinationDataset" = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="destination",
        message="DestinationDataset",
    )
    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class SubscribeListingResponse(proto.Message):
    r"""Message for response when you subscribe to a listing.

    Attributes:
        subscription (google.cloud.bigquery_analyticshub_v1.types.Subscription):
            Subscription object created from this
            subscribe action.
    """

    subscription: "Subscription" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="Subscription",
    )


class SubscribeDataExchangeRequest(proto.Message):
    r"""Message for subscribing to a Data Exchange.

    Attributes:
        name (str):
            Required. Resource name of the Data Exchange. e.g.
            ``projects/publisherproject/locations/US/dataExchanges/123``
        destination (str):
            Required. The parent resource path of the Subscription. e.g.
            ``projects/subscriberproject/locations/US``
        subscription (str):
            Required. Name of the subscription to create. e.g.
            ``subscription1``
        subscriber_contact (str):
            Email of the subscriber.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    destination: str = proto.Field(
        proto.STRING,
        number=2,
    )
    subscription: str = proto.Field(
        proto.STRING,
        number=4,
    )
    subscriber_contact: str = proto.Field(
        proto.STRING,
        number=3,
    )


class SubscribeDataExchangeResponse(proto.Message):
    r"""Message for response when you subscribe to a Data Exchange.

    Attributes:
        subscription (google.cloud.bigquery_analyticshub_v1.types.Subscription):
            Subscription object created from this
            subscribe action.
    """

    subscription: "Subscription" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="Subscription",
    )


class RefreshSubscriptionRequest(proto.Message):
    r"""Message for refreshing a subscription.

    Attributes:
        name (str):
            Required. Resource name of the Subscription to refresh. e.g.
            ``projects/subscriberproject/locations/US/subscriptions/123``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class RefreshSubscriptionResponse(proto.Message):
    r"""Message for response when you refresh a subscription.

    Attributes:
        subscription (google.cloud.bigquery_analyticshub_v1.types.Subscription):
            The refreshed subscription resource.
    """

    subscription: "Subscription" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="Subscription",
    )


class GetSubscriptionRequest(proto.Message):
    r"""Message for getting a subscription.

    Attributes:
        name (str):
            Required. Resource name of the subscription.
            e.g. projects/123/locations/US/subscriptions/456
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListSubscriptionsRequest(proto.Message):
    r"""Message for listing subscriptions.

    Attributes:
        parent (str):
            Required. The parent resource path of the
            subscription. e.g.
            projects/myproject/locations/US
        filter (str):
            An expression for filtering the results of the request.
            Eligible fields for filtering are:

            -  ``listing``
            -  ``data_exchange``

            Alternatively, a literal wrapped in double quotes may be
            provided. This will be checked for an exact match against
            both fields above.

            In all cases, the full Data Exchange or Listing resource
            name must be provided. Some example of using filters:

            -  data_exchange="projects/myproject/locations/us/dataExchanges/123"
            -  listing="projects/123/locations/us/dataExchanges/456/listings/789"
            -  "projects/myproject/locations/us/dataExchanges/123".
        page_size (int):
            The maximum number of results to return in a
            single response page.
        page_token (str):
            Page token, returned by a previous call.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    filter: str = proto.Field(
        proto.STRING,
        number=2,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=3,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=4,
    )


class ListSubscriptionsResponse(proto.Message):
    r"""Message for response to the listing of subscriptions.

    Attributes:
        subscriptions (MutableSequence[google.cloud.bigquery_analyticshub_v1.types.Subscription]):
            The list of subscriptions.
        next_page_token (str):
            Next page token.
    """

    @property
    def raw_page(self):
        return self

    subscriptions: MutableSequence["Subscription"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Subscription",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ListSharedResourceSubscriptionsRequest(proto.Message):
    r"""Message for listing subscriptions of a shared resource.

    Attributes:
        resource (str):
            Required. Resource name of the requested
            target. This resource may be either a Listing or
            a DataExchange. e.g.
            projects/123/locations/US/dataExchanges/456 OR
            e.g.
            projects/123/locations/US/dataExchanges/456/listings/789
        include_deleted_subscriptions (bool):
            If selected, includes deleted subscriptions
            in the response (up to 63 days after deletion).
        page_size (int):
            The maximum number of results to return in a
            single response page.
        page_token (str):
            Page token, returned by a previous call.
    """

    resource: str = proto.Field(
        proto.STRING,
        number=1,
    )
    include_deleted_subscriptions: bool = proto.Field(
        proto.BOOL,
        number=2,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=3,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=4,
    )


class ListSharedResourceSubscriptionsResponse(proto.Message):
    r"""Message for response to the listing of shared resource
    subscriptions.

    Attributes:
        shared_resource_subscriptions (MutableSequence[google.cloud.bigquery_analyticshub_v1.types.Subscription]):
            The list of subscriptions.
        next_page_token (str):
            Next page token.
    """

    @property
    def raw_page(self):
        return self

    shared_resource_subscriptions: MutableSequence[
        "Subscription"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Subscription",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class RevokeSubscriptionRequest(proto.Message):
    r"""Message for revoking a subscription.

    Attributes:
        name (str):
            Required. Resource name of the subscription
            to revoke. e.g.
            projects/123/locations/US/subscriptions/456
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class RevokeSubscriptionResponse(proto.Message):
    r"""Message for response when you revoke a subscription."""


class DeleteSubscriptionRequest(proto.Message):
    r"""Message for deleting a subscription.

    Attributes:
        name (str):
            Required. Resource name of the subscription
            to delete. e.g.
            projects/123/locations/US/subscriptions/456
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class OperationMetadata(proto.Message):
    r"""Represents the metadata of a long-running operation in
    Analytics Hub.

    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation was
            created.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the operation finished
            running.
        target (str):
            Output only. Server-defined resource path for
            the target of the operation.
        verb (str):
            Output only. Name of the verb executed by the
            operation.
        status_message (str):
            Output only. Human-readable status of the
            operation, if any.
        requested_cancellation (bool):
            Output only. Identifies whether the user has requested
            cancellation of the operation. Operations that have
            successfully been cancelled have [Operation.error][] value
            with a [google.rpc.Status.code][google.rpc.Status.code] of
            1, corresponding to ``Code.CANCELLED``.
        api_version (str):
            Output only. API version used to start the
            operation.
    """

    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    end_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    target: str = proto.Field(
        proto.STRING,
        number=3,
    )
    verb: str = proto.Field(
        proto.STRING,
        number=4,
    )
    status_message: str = proto.Field(
        proto.STRING,
        number=5,
    )
    requested_cancellation: bool = proto.Field(
        proto.BOOL,
        number=6,
    )
    api_version: str = proto.Field(
        proto.STRING,
        number=7,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
