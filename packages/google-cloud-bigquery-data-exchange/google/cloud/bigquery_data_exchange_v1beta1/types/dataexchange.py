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
import proto  # type: ignore

from google.cloud.bigquery_data_exchange_v1beta1 import common  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.bigquery.dataexchange.v1beta1",
    manifest={
        "DataExchange",
        "DataProvider",
        "Publisher",
        "DestinationDatasetReference",
        "DestinationDataset",
        "Listing",
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
    },
)


class DataExchange(proto.Message):
    r"""A data exchange is a container that enables data sharing.
    It contains a set of listings of the data sources along with
    descriptive information of the data exchange.

    Attributes:
        name (str):
            Output only. The resource name of the data exchange. e.g.
            ``projects/myproject/locations/US/dataExchanges/123``.
        display_name (str):
            Required. Human-readable display name of the data exchange.
            The display name must contain only Unicode letters, numbers
            (0-9), underscores (_), dashes (-), spaces ( ), and can't
            start or end with spaces. Default value is an empty string.
            Max length: 63 bytes.
        description (str):
            Optional. Short description of the data
            exchange that can consist of sentences or
            paragraphs. The description must not contain
            Unicode non-characters as well as C0 and C1
            control codes except tabs (HT), new lines (LF),
            carriage returns (CR), and page breaks (FF).
            Default value is an empty string.
            Max length: 2000 bytes.
        primary_contact (str):
            Optional. Email, URL or other reference of
            the primary point of contact of the data
            exchange Max Length: 1000 bytes.
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
            encoded data. Note: For byte fields, the
            contents of the field are base64-encoded (which
            increases the size of the data by 33-36%) when
            using JSON on the wire.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name = proto.Field(
        proto.STRING,
        number=2,
    )
    description = proto.Field(
        proto.STRING,
        number=3,
    )
    primary_contact = proto.Field(
        proto.STRING,
        number=4,
    )
    documentation = proto.Field(
        proto.STRING,
        number=5,
    )
    listing_count = proto.Field(
        proto.INT32,
        number=6,
    )
    icon = proto.Field(
        proto.BYTES,
        number=7,
    )


class DataProvider(proto.Message):
    r"""Contains details of the Data Provider.

    Attributes:
        name (str):
            Optional. Name of the Data Provider.
        primary_contact (str):
            Optional. Email or URL of the Data Provider.
            Max Length: 1000 bytes.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    primary_contact = proto.Field(
        proto.STRING,
        number=2,
    )


class Publisher(proto.Message):
    r"""Contains details of the Publisher.

    Attributes:
        name (str):
            Optional. Name of the listing Publisher.
        primary_contact (str):
            Optional. Email or URL of the listing
            Publisher. Max Length: 1000 bytes.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    primary_contact = proto.Field(
        proto.STRING,
        number=2,
    )


class DestinationDatasetReference(proto.Message):
    r"""Defines the Destination BigQuery Dataset Reference.

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

    dataset_id = proto.Field(
        proto.STRING,
        number=1,
    )
    project_id = proto.Field(
        proto.STRING,
        number=2,
    )


class DestinationDataset(proto.Message):
    r"""Defines the Destination BigQuery Dataset.

    Attributes:
        dataset_reference (google.cloud.bigquery_data_exchange_v1beta1.types.DestinationDatasetReference):
            Required. A reference that identifies the
            destination dataset.
        friendly_name (google.protobuf.wrappers_pb2.StringValue):
            Optional. A descriptive name for the dataset.
        description (google.protobuf.wrappers_pb2.StringValue):
            Optional. A user-friendly description of the
            dataset.
        labels (Mapping[str, str]):
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

    dataset_reference = proto.Field(
        proto.MESSAGE,
        number=1,
        message="DestinationDatasetReference",
    )
    friendly_name = proto.Field(
        proto.MESSAGE,
        number=2,
        message=wrappers_pb2.StringValue,
    )
    description = proto.Field(
        proto.MESSAGE,
        number=3,
        message=wrappers_pb2.StringValue,
    )
    labels = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=4,
    )
    location = proto.Field(
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
        name (str):
            Output only. The resource name of the listing. e.g.
            ``projects/myproject/locations/US/dataExchanges/123/listings/456``
        display_name (str):
            Required. Human-readable display name of the listing. The
            display name must contain only Unicode letters, numbers
            (0-9), underscores (_), dashes (-), spaces ( ), and can't
            start or end with spaces. Default value is an empty string.
            Max length: 63 bytes.
        description (str):
            Optional. Short description of the listing
            that can consist of sentences or paragraphs. The
            description must not contain Unicode
            non-characters as well as C0 and C1 control
            codes except tabs (HT), new lines (LF), carriage
            returns (CR), and page breaks (FF).
            Default value is an empty string.
            Max length: 2000 bytes.
        primary_contact (str):
            Optional. Email or URL of the primary point
            of contact of the listing. Max Length: 1000
            bytes.
        documentation (str):
            Optional. Documentation describing the
            listing.
        bigquery_dataset (google.cloud.bigquery_data_exchange_v1beta1.types.Listing.BigQueryDatasetSource):
            Required. Shared dataset i.e. BigQuery
            dataset source.

            This field is a member of `oneof`_ ``source``.
        state (google.cloud.bigquery_data_exchange_v1beta1.types.Listing.State):
            Output only. Current state of the Listing.
        icon (bytes):
            Optional. Base64 encoded image representing
            the listing. Max Size: 3.0MiB Expected image
            dimensions are 512x512 pixels, however the API
            only performs validation on size of the encoded
            data. Note: For byte fields, the contents of the
            field are base64-encoded (which increases the
            size of the data by 33-36%) when using JSON on
            the wire.
        data_provider (google.cloud.bigquery_data_exchange_v1beta1.types.DataProvider):
            Optional. The details of the Data Provider
            who owns the source data.
        categories (Sequence[google.cloud.bigquery_data_exchange_v1beta1.common.Category]):
            Optional. Categories of the Listing. Up to
            two categories are allowed.
        publisher (google.cloud.bigquery_data_exchange_v1beta1.types.Publisher):
            Optional. The details of the Publisher who
            owns the listing and has rights to share the
            source data.
        request_access (str):
            Optional. Email or URL of the request access
            of the listing. Subscribers can use this
            reference to request access. Max Length: 1000
            bytes.
    """

    class State(proto.Enum):
        r"""State of the Listing"""
        STATE_UNSPECIFIED = 0
        ACTIVE = 1

    class BigQueryDatasetSource(proto.Message):
        r"""A reference to a Shared dataset. It's an existing BigQuery
        dataset with a collection of objects, such as tables and views,
        that you want to share with subscribers.
        Upon subscription to a Listing, Data Exchange creates a Linked
        dataset in the subscriber's project. A Linked dataset is an
        opaque, read-only BigQuery dataset that serves as a "symbolic
        link" to a shared dataset.

        Attributes:
            dataset (str):
                Resource name of the dataset source for this listing. e.g.
                ``projects/myproject/datasets/123``
        """

        dataset = proto.Field(
            proto.STRING,
            number=1,
        )

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name = proto.Field(
        proto.STRING,
        number=2,
    )
    description = proto.Field(
        proto.STRING,
        number=3,
    )
    primary_contact = proto.Field(
        proto.STRING,
        number=4,
    )
    documentation = proto.Field(
        proto.STRING,
        number=5,
    )
    bigquery_dataset = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="source",
        message=BigQueryDatasetSource,
    )
    state = proto.Field(
        proto.ENUM,
        number=7,
        enum=State,
    )
    icon = proto.Field(
        proto.BYTES,
        number=8,
    )
    data_provider = proto.Field(
        proto.MESSAGE,
        number=9,
        message="DataProvider",
    )
    categories = proto.RepeatedField(
        proto.ENUM,
        number=10,
        enum=common.Category,
    )
    publisher = proto.Field(
        proto.MESSAGE,
        number=11,
        message="Publisher",
    )
    request_access = proto.Field(
        proto.STRING,
        number=12,
    )


class ListDataExchangesRequest(proto.Message):
    r"""Message for requesting list of DataExchanges.

    Attributes:
        parent (str):
            Required. The parent resource path of the DataExchanges.
            e.g. ``projects/myproject/locations/US``.
        page_size (int):
            The maximum number of results to return in a
            single response page. Leverage the page tokens
            to iterate through the entire collection.
        page_token (str):
            Page token, returned by a previous call, to
            request the next page of results.
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


class ListDataExchangesResponse(proto.Message):
    r"""Message for response to listing DataExchanges.

    Attributes:
        data_exchanges (Sequence[google.cloud.bigquery_data_exchange_v1beta1.types.DataExchange]):
            The list of DataExchange.
        next_page_token (str):
            A token to request the next page of results.
    """

    @property
    def raw_page(self):
        return self

    data_exchanges = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="DataExchange",
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )


class ListOrgDataExchangesRequest(proto.Message):
    r"""Message for requesting list of DataExchanges from projects in
    an organization and location.

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

    organization = proto.Field(
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


class ListOrgDataExchangesResponse(proto.Message):
    r"""Message for response to listing DataExchanges in an
    organization and location.

    Attributes:
        data_exchanges (Sequence[google.cloud.bigquery_data_exchange_v1beta1.types.DataExchange]):
            The list of DataExchange.
        next_page_token (str):
            A token to request the next page of results.
    """

    @property
    def raw_page(self):
        return self

    data_exchanges = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="DataExchange",
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )


class GetDataExchangeRequest(proto.Message):
    r"""Message for getting a DataExchange.

    Attributes:
        name (str):
            Required. The resource name of the DataExchange. e.g.
            ``projects/myproject/locations/US/dataExchanges/123``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateDataExchangeRequest(proto.Message):
    r"""Message for creating a DataExchange.

    Attributes:
        parent (str):
            Required. The parent resource path of the DataExchange. e.g.
            ``projects/myproject/locations/US``.
        data_exchange_id (str):
            Required. The ID of the DataExchange to create. Must contain
            only Unicode letters, numbers (0-9), underscores (_). Should
            not use characters that require URL-escaping, or characters
            outside of ASCII, spaces. Max length: 100 bytes.
        data_exchange (google.cloud.bigquery_data_exchange_v1beta1.types.DataExchange):
            Required. The DataExchange to create.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    data_exchange_id = proto.Field(
        proto.STRING,
        number=2,
    )
    data_exchange = proto.Field(
        proto.MESSAGE,
        number=3,
        message="DataExchange",
    )


class UpdateDataExchangeRequest(proto.Message):
    r"""Message for updating a DataExchange.

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Field mask is used to specify the fields to be
            overwritten in the DataExchange resource by the update. The
            fields specified in the update_mask are relative to the
            resource, not the full request.
        data_exchange (google.cloud.bigquery_data_exchange_v1beta1.types.DataExchange):
            Required. The DataExchange to update.
    """

    update_mask = proto.Field(
        proto.MESSAGE,
        number=1,
        message=field_mask_pb2.FieldMask,
    )
    data_exchange = proto.Field(
        proto.MESSAGE,
        number=2,
        message="DataExchange",
    )


class DeleteDataExchangeRequest(proto.Message):
    r"""Message for deleting a DataExchange.

    Attributes:
        name (str):
            Required. Resource name of the DataExchange to delete. e.g.
            ``projects/myproject/locations/US/dataExchanges/123``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class ListListingsRequest(proto.Message):
    r"""Message for requesting list of Listings.

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


class ListListingsResponse(proto.Message):
    r"""Message for response to listing Listings.

    Attributes:
        listings (Sequence[google.cloud.bigquery_data_exchange_v1beta1.types.Listing]):
            The list of Listing.
        next_page_token (str):
            A token to request the next page of results.
    """

    @property
    def raw_page(self):
        return self

    listings = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Listing",
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )


class GetListingRequest(proto.Message):
    r"""Message for getting a Listing.

    Attributes:
        name (str):
            Required. The resource name of the listing. e.g.
            ``projects/myproject/locations/US/dataExchanges/123/listings/456``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateListingRequest(proto.Message):
    r"""Message for creating a Listing.

    Attributes:
        parent (str):
            Required. The parent resource path of the listing. e.g.
            ``projects/myproject/locations/US/dataExchanges/123``.
        listing_id (str):
            Required. The ID of the Listing to create. Must contain only
            Unicode letters, numbers (0-9), underscores (_). Should not
            use characters that require URL-escaping, or characters
            outside of ASCII, spaces. Max length: 100 bytes.
        listing (google.cloud.bigquery_data_exchange_v1beta1.types.Listing):
            Required. The listing to create.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    listing_id = proto.Field(
        proto.STRING,
        number=2,
    )
    listing = proto.Field(
        proto.MESSAGE,
        number=3,
        message="Listing",
    )


class UpdateListingRequest(proto.Message):
    r"""Message for updating a Listing.

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Field mask is used to specify the fields to be
            overwritten in the Listing resource by the update. The
            fields specified in the update_mask are relative to the
            resource, not the full request.
        listing (google.cloud.bigquery_data_exchange_v1beta1.types.Listing):
            Required. The listing to update.
    """

    update_mask = proto.Field(
        proto.MESSAGE,
        number=1,
        message=field_mask_pb2.FieldMask,
    )
    listing = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Listing",
    )


class DeleteListingRequest(proto.Message):
    r"""Message for deleting a Listing.

    Attributes:
        name (str):
            Required. Resource name of the listing to delete. e.g.
            ``projects/myproject/locations/US/dataExchanges/123/listings/456``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class SubscribeListingRequest(proto.Message):
    r"""Message for subscribing a Listing.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Required. Resource name of the listing to subscribe to. e.g.
            ``projects/myproject/locations/US/dataExchanges/123/listings/456``.
        destination_dataset (google.cloud.bigquery_data_exchange_v1beta1.types.DestinationDataset):
            BigQuery destination dataset to create for
            the subscriber.

            This field is a member of `oneof`_ ``destination``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    destination_dataset = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="destination",
        message="DestinationDataset",
    )


class SubscribeListingResponse(proto.Message):
    r"""Message for response to subscribing a Listing.
    Empty for now.

    """


__all__ = tuple(sorted(__protobuf__.manifest))
