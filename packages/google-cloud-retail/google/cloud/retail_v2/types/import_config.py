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

from google.cloud.retail_v2.types import product
from google.cloud.retail_v2.types import user_event
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.retail.v2",
    manifest={
        "GcsSource",
        "BigQuerySource",
        "ProductInlineSource",
        "UserEventInlineSource",
        "ImportErrorsConfig",
        "ImportProductsRequest",
        "ImportUserEventsRequest",
        "ProductInputConfig",
        "UserEventInputConfig",
        "ImportMetadata",
        "ImportProductsResponse",
        "ImportUserEventsResponse",
        "UserEventImportSummary",
    },
)


class GcsSource(proto.Message):
    r"""Google Cloud Storage location for input content.
    format.

    Attributes:
        input_uris (Sequence[str]):
            Required. Google Cloud Storage URIs to input files. URI can
            be up to 2000 characters long. URIs can match the full
            object path (for example,
            ``gs://bucket/directory/object.json``) or a pattern matching
            one or more files, such as ``gs://bucket/directory/*.json``.
            A request can contain at most 100 files, and each file can
            be up to 2 GB. See `Importing product
            information <https://cloud.google.com/recommendations-ai/docs/upload-catalog>`__
            for the expected file format and setup instructions.
        data_schema (str):
            The schema to use when parsing the data from the source.

            Supported values for product imports:

            -  ``product`` (default): One JSON
               [Product][google.cloud.retail.v2.Product] per line. Each
               product must have a valid
               [Product.id][google.cloud.retail.v2.Product.id].
            -  ``product_merchant_center``: See `Importing catalog data
               from Merchant
               Center <https://cloud.google.com/retail/recommendations-ai/docs/upload-catalog#mc>`__.

            Supported values for user events imports:

            -  ``user_event`` (default): One JSON
               [UserEvent][google.cloud.retail.v2.UserEvent] per line.
            -  ``user_event_ga360``: Using
               https://support.google.com/analytics/answer/3437719?hl=en.
    """

    input_uris = proto.RepeatedField(proto.STRING, number=1,)
    data_schema = proto.Field(proto.STRING, number=2,)


class BigQuerySource(proto.Message):
    r"""BigQuery source import data from.
    Attributes:
        project_id (str):
            The project id (can be project # or id) that
            the BigQuery source is in with a length limit of
            128 characters. If not specified, inherits the
            project id from the parent request.
        dataset_id (str):
            Required. The BigQuery data set to copy the
            data from with a length limit of 1,024
            characters.
        table_id (str):
            Required. The BigQuery table to copy the data
            from with a length limit of 1,024 characters.
        gcs_staging_dir (str):
            Intermediate Cloud Storage directory used for
            the import with a length limit of 2,000
            characters. Can be specified if one wants to
            have the BigQuery export to a specific Cloud
            Storage directory.
        data_schema (str):
            The schema to use when parsing the data from the source.

            Supported values for product imports:

            -  ``product`` (default): One JSON
               [Product][google.cloud.retail.v2.Product] per line. Each
               product must have a valid
               [Product.id][google.cloud.retail.v2.Product.id].
            -  ``product_merchant_center``: See `Importing catalog data
               from Merchant
               Center <https://cloud.google.com/retail/recommendations-ai/docs/upload-catalog#mc>`__.

            Supported values for user events imports:

            -  ``user_event`` (default): One JSON
               [UserEvent][google.cloud.retail.v2.UserEvent] per line.
            -  ``user_event_ga360``: Using
               https://support.google.com/analytics/answer/3437719?hl=en.
    """

    project_id = proto.Field(proto.STRING, number=5,)
    dataset_id = proto.Field(proto.STRING, number=1,)
    table_id = proto.Field(proto.STRING, number=2,)
    gcs_staging_dir = proto.Field(proto.STRING, number=3,)
    data_schema = proto.Field(proto.STRING, number=4,)


class ProductInlineSource(proto.Message):
    r"""The inline source for the input config for ImportProducts
    method.

    Attributes:
        products (Sequence[google.cloud.retail_v2.types.Product]):
            Required. A list of products to update/create. Each product
            must have a valid
            [Product.id][google.cloud.retail.v2.Product.id]. Recommended
            max of 10k items.
    """

    products = proto.RepeatedField(proto.MESSAGE, number=1, message=product.Product,)


class UserEventInlineSource(proto.Message):
    r"""The inline source for the input config for ImportUserEvents
    method.

    Attributes:
        user_events (Sequence[google.cloud.retail_v2.types.UserEvent]):
            Required. A list of user events to import.
            Recommended max of 10k items.
    """

    user_events = proto.RepeatedField(
        proto.MESSAGE, number=1, message=user_event.UserEvent,
    )


class ImportErrorsConfig(proto.Message):
    r"""Configuration of destination for Import related errors.
    Attributes:
        gcs_prefix (str):
            Google Cloud Storage path for import errors. This must be an
            empty, existing Cloud Storage bucket. Import errors will be
            written to a file in this bucket, one per line, as a
            JSON-encoded ``google.rpc.Status`` message.
    """

    gcs_prefix = proto.Field(proto.STRING, number=1, oneof="destination",)


class ImportProductsRequest(proto.Message):
    r"""Request message for Import methods.
    Attributes:
        parent (str):
            Required.
            ``projects/1234/locations/global/catalogs/default_catalog/branches/default_branch``

            If no updateMask is specified, requires products.create
            permission. If updateMask is specified, requires
            products.update permission.
        input_config (google.cloud.retail_v2.types.ProductInputConfig):
            Required. The desired input location of the
            data.
        errors_config (google.cloud.retail_v2.types.ImportErrorsConfig):
            The desired location of errors incurred
            during the Import.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Indicates which fields in the provided
            imported 'products' to update. If not set, will
            by default update all fields.
    """

    parent = proto.Field(proto.STRING, number=1,)
    input_config = proto.Field(proto.MESSAGE, number=2, message="ProductInputConfig",)
    errors_config = proto.Field(proto.MESSAGE, number=3, message="ImportErrorsConfig",)
    update_mask = proto.Field(
        proto.MESSAGE, number=4, message=field_mask_pb2.FieldMask,
    )


class ImportUserEventsRequest(proto.Message):
    r"""Request message for the ImportUserEvents request.
    Attributes:
        parent (str):
            Required.
            ``projects/1234/locations/global/catalogs/default_catalog``
        input_config (google.cloud.retail_v2.types.UserEventInputConfig):
            Required. The desired input location of the
            data.
        errors_config (google.cloud.retail_v2.types.ImportErrorsConfig):
            The desired location of errors incurred
            during the Import. Cannot be set for inline user
            event imports.
    """

    parent = proto.Field(proto.STRING, number=1,)
    input_config = proto.Field(proto.MESSAGE, number=2, message="UserEventInputConfig",)
    errors_config = proto.Field(proto.MESSAGE, number=3, message="ImportErrorsConfig",)


class ProductInputConfig(proto.Message):
    r"""The input config source for products.
    Attributes:
        product_inline_source (google.cloud.retail_v2.types.ProductInlineSource):
            The Inline source for the input content for
            products.
        gcs_source (google.cloud.retail_v2.types.GcsSource):
            Google Cloud Storage location for the input
            content.
        big_query_source (google.cloud.retail_v2.types.BigQuerySource):
            BigQuery input source.
    """

    product_inline_source = proto.Field(
        proto.MESSAGE, number=1, oneof="source", message="ProductInlineSource",
    )
    gcs_source = proto.Field(
        proto.MESSAGE, number=2, oneof="source", message="GcsSource",
    )
    big_query_source = proto.Field(
        proto.MESSAGE, number=3, oneof="source", message="BigQuerySource",
    )


class UserEventInputConfig(proto.Message):
    r"""The input config source for user events.
    Attributes:
        user_event_inline_source (google.cloud.retail_v2.types.UserEventInlineSource):
            Required. The Inline source for the input
            content for UserEvents.
        gcs_source (google.cloud.retail_v2.types.GcsSource):
            Required. Google Cloud Storage location for
            the input content.
        big_query_source (google.cloud.retail_v2.types.BigQuerySource):
            Required. BigQuery input source.
    """

    user_event_inline_source = proto.Field(
        proto.MESSAGE, number=1, oneof="source", message="UserEventInlineSource",
    )
    gcs_source = proto.Field(
        proto.MESSAGE, number=2, oneof="source", message="GcsSource",
    )
    big_query_source = proto.Field(
        proto.MESSAGE, number=3, oneof="source", message="BigQuerySource",
    )


class ImportMetadata(proto.Message):
    r"""Metadata related to the progress of the Import operation.
    This will be returned by the
    google.longrunning.Operation.metadata field.

    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Operation create time.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Operation last update time. If the operation
            is done, this is also the finish time.
        success_count (int):
            Count of entries that were processed
            successfully.
        failure_count (int):
            Count of entries that encountered errors
            while processing.
    """

    create_time = proto.Field(proto.MESSAGE, number=1, message=timestamp_pb2.Timestamp,)
    update_time = proto.Field(proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,)
    success_count = proto.Field(proto.INT64, number=3,)
    failure_count = proto.Field(proto.INT64, number=4,)


class ImportProductsResponse(proto.Message):
    r"""Response of the
    [ImportProductsRequest][google.cloud.retail.v2.ImportProductsRequest].
    If the long running operation is done, then this message is returned
    by the google.longrunning.Operations.response field if the operation
    was successful.

    Attributes:
        error_samples (Sequence[google.rpc.status_pb2.Status]):
            A sample of errors encountered while
            processing the request.
        errors_config (google.cloud.retail_v2.types.ImportErrorsConfig):
            Echoes the destination for the complete
            errors in the request if set.
    """

    error_samples = proto.RepeatedField(
        proto.MESSAGE, number=1, message=status_pb2.Status,
    )
    errors_config = proto.Field(proto.MESSAGE, number=2, message="ImportErrorsConfig",)


class ImportUserEventsResponse(proto.Message):
    r"""Response of the ImportUserEventsRequest. If the long running
    operation was successful, then this message is returned by the
    google.longrunning.Operations.response field if the operation
    was successful.

    Attributes:
        error_samples (Sequence[google.rpc.status_pb2.Status]):
            A sample of errors encountered while
            processing the request.
        errors_config (google.cloud.retail_v2.types.ImportErrorsConfig):
            Echoes the destination for the complete
            errors if this field was set in the request.
        import_summary (google.cloud.retail_v2.types.UserEventImportSummary):
            Aggregated statistics of user event import
            status.
    """

    error_samples = proto.RepeatedField(
        proto.MESSAGE, number=1, message=status_pb2.Status,
    )
    errors_config = proto.Field(proto.MESSAGE, number=2, message="ImportErrorsConfig",)
    import_summary = proto.Field(
        proto.MESSAGE, number=3, message="UserEventImportSummary",
    )


class UserEventImportSummary(proto.Message):
    r"""A summary of import result. The UserEventImportSummary
    summarizes the import status for user events.

    Attributes:
        joined_events_count (int):
            Count of user events imported with complete
            existing catalog information.
        unjoined_events_count (int):
            Count of user events imported, but with
            catalog information not found in the imported
            catalog.
    """

    joined_events_count = proto.Field(proto.INT64, number=1,)
    unjoined_events_count = proto.Field(proto.INT64, number=2,)


__all__ = tuple(sorted(__protobuf__.manifest))
