# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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

import proto  # type: ignore

from google.cloud.databasecenter_v1beta.types import (
    machine_config as gcd_machine_config,
)
from google.cloud.databasecenter_v1beta.types import maintenance, metric_data
from google.cloud.databasecenter_v1beta.types import product as gcd_product
from google.cloud.databasecenter_v1beta.types import signals

__protobuf__ = proto.module(
    package="google.cloud.databasecenter.v1beta",
    manifest={
        "ResourceCategory",
        "Edition",
        "SubResourceType",
        "QueryProductsRequest",
        "QueryProductsResponse",
        "QueryDatabaseResourceGroupsRequest",
        "QueryDatabaseResourceGroupsResponse",
        "DatabaseResourceGroup",
        "DatabaseResource",
        "Label",
        "BackupDRConfig",
        "Tag",
    },
)


class ResourceCategory(proto.Enum):
    r"""The enum value corresponds to 'type' suffix in the resource_type
    field.

    Values:
        RESOURCE_CATEGORY_UNSPECIFIED (0):
            Unspecified.
        INSTANCE (1):
            A resource that is an Instance.
        CLUSTER (2):
            A resource that is a Cluster.
        DATABASE (3):
            A resource that is a Database.
    """
    RESOURCE_CATEGORY_UNSPECIFIED = 0
    INSTANCE = 1
    CLUSTER = 2
    DATABASE = 3


class Edition(proto.Enum):
    r"""Proto representing the edition of the instance.
    NextId: 4.

    Values:
        EDITION_UNSPECIFIED (0):
            Default, to make it consistent with instance
            edition enum.
        EDITION_ENTERPRISE (1):
            Represents the enterprise edition.
        EDITION_ENTERPRISE_PLUS (2):
            Represents the enterprise plus edition.
        EDITION_STANDARD (3):
            Represents the standard edition.
    """
    EDITION_UNSPECIFIED = 0
    EDITION_ENTERPRISE = 1
    EDITION_ENTERPRISE_PLUS = 2
    EDITION_STANDARD = 3


class SubResourceType(proto.Enum):
    r"""SubResourceType refers to the sub-type of database resource.

    Values:
        SUB_RESOURCE_TYPE_UNSPECIFIED (0):
            Unspecified.
        SUB_RESOURCE_TYPE_PRIMARY (1):
            A resource acting as a primary.
        SUB_RESOURCE_TYPE_SECONDARY (2):
            A resource acting as a secondary.
        SUB_RESOURCE_TYPE_READ_REPLICA (3):
            A resource acting as a read-replica.
        SUB_RESOURCE_TYPE_EXTERNAL_PRIMARY (5):
            A resource acting as an external primary.
        SUB_RESOURCE_TYPE_OTHER (4):
            For the rest of the categories.
    """
    SUB_RESOURCE_TYPE_UNSPECIFIED = 0
    SUB_RESOURCE_TYPE_PRIMARY = 1
    SUB_RESOURCE_TYPE_SECONDARY = 2
    SUB_RESOURCE_TYPE_READ_REPLICA = 3
    SUB_RESOURCE_TYPE_EXTERNAL_PRIMARY = 5
    SUB_RESOURCE_TYPE_OTHER = 4


class QueryProductsRequest(proto.Message):
    r"""QueryProductsRequest is the request to get a list of
    products.

    Attributes:
        parent (str):
            Required. Parent can be a project, a folder, or an
            organization.

            The allowed values are:

            - projects/{PROJECT_ID}/locations/{LOCATION}
              (e.g.,"projects/foo-bar/locations/us-central1")
            - projects/{PROJECT_NUMBER}/locations/{LOCATION}
              (e.g.,"projects/12345678/locations/us-central1")
            - folders/{FOLDER_NUMBER}/locations/{LOCATION}
              (e.g.,"folders/1234567/locations/us-central1")
            - organizations/{ORGANIZATION_NUMBER}/locations/{LOCATION}
              (e.g.,"organizations/123456/locations/us-central1")
            - projects/{PROJECT_ID} (e.g., "projects/foo-bar")
            - projects/{PROJECT_NUMBER} (e.g., "projects/12345678")
            - folders/{FOLDER_NUMBER} (e.g., "folders/1234567")
            - organizations/{ORGANIZATION_NUMBER} (e.g.,
              "organizations/123456")
        page_size (int):
            Optional. If unspecified, at most 50 products
            will be returned. The maximum value is 1000;
            values above 1000 will be coerced to 1000.
        page_token (str):
            Optional. A page token, received from a previous
            ``ListLocations`` call. Provide this to retrieve the
            subsequent page. All other parameters except page size
            should match the call that provided the page page token.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=3,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=1,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class QueryProductsResponse(proto.Message):
    r"""QueryProductsResponse represents the response containing a
    list of products.

    Attributes:
        products (MutableSequence[google.cloud.databasecenter_v1beta.types.Product]):
            List of database products returned.
        next_page_token (str):
            A token that can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages
        unreachable (MutableSequence[str]):
            Unordered list. List of unreachable regions
            from where data could not be retrieved.
    """

    @property
    def raw_page(self):
        return self

    products: MutableSequence[gcd_product.Product] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=gcd_product.Product,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class QueryDatabaseResourceGroupsRequest(proto.Message):
    r"""QueryDatabaseResourceGroupsRequest is the request to get a
    list of database groups.

    Attributes:
        parent (str):
            Required. Parent can be a project, a folder, or an
            organization. The search is limited to the resources within
            the ``scope``.

            The allowed values are:

            - projects/{PROJECT_ID} (e.g., "projects/foo-bar")
            - projects/{PROJECT_NUMBER} (e.g., "projects/12345678")
            - folders/{FOLDER_NUMBER} (e.g., "folders/1234567")
            - organizations/{ORGANIZATION_NUMBER} (e.g.,
              "organizations/123456")
        filter (str):
            Optional. The expression to filter resources.

            The following fields are filterable:

            - full_resource_name
            - resource_type
            - container
            - product.type
            - product.engine
            - product.version
            - location
            - labels
            - resource_category
            - machine_config.cpu_count
            - machine_config.memory_size_bytes
            - machine_config.shard_count
            - resource_name
            - tags
            - backupdr_config.backupdr_managed
            - edition

            The expression is a list of zero or more restrictions
            combined via logical operators ``AND`` and ``OR``. When
            ``AND`` and ``OR`` are both used in the expression,
            parentheses must be appropriately used to group the
            combinations.

            Example: location="us-east1" Example:
            container="projects/123" OR container="projects/456"
            Example: (container="projects/123" OR
            container="projects/456") AND location="us-east1" Example:
            full_resource_name=~"test" Example:
            full_resource_name=~"test.*master".
        signal_type_groups (MutableSequence[google.cloud.databasecenter_v1beta.types.SignalTypeGroup]):
            Optional. Groups of signal types that are
            requested.
        signal_filters (MutableSequence[google.cloud.databasecenter_v1beta.types.SignalFilter]):
            Optional. Filters based on signals. The list will be ORed
            together and then ANDed with the ``filters`` field above.
        order_by (str):
            Optional. A field that specifies the sort order of the
            results.

            The following fields are sortable:

            - full_resource_name
            - product.type
            - product.engine
            - product.version
            - container
            - issue_count
            - machine_config.vcpu_count
            - machine_config.memory_size_bytes
            - machine_config.shard_count
            - resource_name
            - issue_severity
            - signal_type
            - location
            - resource_type
            - instance_type
            - edition
            - metrics.p99_cpu_utilization
            - metrics.p95_cpu_utilization
            - metrics.current_storage_used_bytes
            - metrics.node_count
            - metrics.processing_unit_count
            - metrics.current_memory_used_bytes
            - metrics.peak_storage_utilization
            - metrics.peak_number_connections
            - metrics.peak_memory_utilization

            The default order is ascending. Add "DESC" after the field
            name to indicate descending order. Add "ASC" after the field
            name to indicate ascending order. It only supports a single
            field at a time.

            For example: order_by = "full_resource_name" sorts response
            in ascending order order_by = "full_resource_name DESC"
            sorts response in descending order order_by = "issue_count
            DESC" sorts response in descending order of count of all
            issues associated with a resource.

            More explicitly, order_by = "full_resource_name, product" is
            not supported.
        page_size (int):
            Optional. If unspecified, at most 50 resource
            groups will be returned. The maximum value is
            1000; values above 1000 will be coerced to 1000.
        page_token (str):
            Optional. A page token, received from a previous
            ``QueryDatabaseResourceGroupsRequest`` call. Provide this to
            retrieve the subsequent page. All parameters except
            page_token should match the parameters in the call that
            provided the page page token.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    filter: str = proto.Field(
        proto.STRING,
        number=2,
    )
    signal_type_groups: MutableSequence[signals.SignalTypeGroup] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message=signals.SignalTypeGroup,
    )
    signal_filters: MutableSequence[signals.SignalFilter] = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message=signals.SignalFilter,
    )
    order_by: str = proto.Field(
        proto.STRING,
        number=5,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=6,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=7,
    )


class QueryDatabaseResourceGroupsResponse(proto.Message):
    r"""QueryDatabaseResourceGroupsResponse represents the response
    message containing a list of resource groups.

    Attributes:
        resource_groups (MutableSequence[google.cloud.databasecenter_v1beta.types.DatabaseResourceGroup]):
            List of database resource groups that pass
            the filter.
        next_page_token (str):
            A token that can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
        unreachable (MutableSequence[str]):
            Unordered list. List of unreachable regions
            from where data could not be retrieved.
    """

    @property
    def raw_page(self):
        return self

    resource_groups: MutableSequence["DatabaseResourceGroup"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="DatabaseResourceGroup",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class DatabaseResourceGroup(proto.Message):
    r"""DatabaseResourceGroup represents all resources that serve a
    common data set. It is considered notionally as a single entity,
    powered by any number of units of compute and storage.

    Attributes:
        root_resources (MutableSequence[google.cloud.databasecenter_v1beta.types.DatabaseResource]):
            A database resource that serves as a root of
            the group of database resources. It is repeated
            just in case we have the concept of multiple
            roots in the future, however, it will only be
            populated with a single value for now.
        signal_groups (MutableSequence[google.cloud.databasecenter_v1beta.types.IssueCount]):
            The filtered signal groups and the count of
            issues associated with the resources that have
            been filtered in.
    """

    root_resources: MutableSequence["DatabaseResource"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="DatabaseResource",
    )
    signal_groups: MutableSequence[signals.IssueCount] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message=signals.IssueCount,
    )


class DatabaseResource(proto.Message):
    r"""DatabaseResource represents every individually configured
    database unit representing compute and/or storage.
    NextId: 20

    Attributes:
        child_resources (MutableSequence[google.cloud.databasecenter_v1beta.types.DatabaseResource]):
            List of children associated with a database
            group.
        full_resource_name (str):
            The full resource name, based on CAIS resource name format
            https://cloud.google.com/asset-inventory/docs/resource-name-format

            Example:

            ``//cloudsql.googleapis.com/projects/project-number/instances/mysql-1``
            ``//cloudsql.googleapis.com/projects/project-number/instances/postgres-1``
            ``//spanner.googleapis.com/projects/project-number/instances/spanner-instance-1``
            ``//alloydb.googleapis.com/projects/project-number/locations/us-central1/clusters/c1``
            ``//alloydb.googleapis.com/projects/project-number/locations/us-central1/clusters/c1/instances/i1``
        container (str):
            Specifies where the resource is created. For
            GCP, it is the full name of the project.
        product (google.cloud.databasecenter_v1beta.types.Product):
            The product this resource represents.
        location (str):
            The location of the resources. It supports
            returning only regional locations in GCP. These
            are of the form: "us-central1", "us-east1", etc.
            See https://cloud.google.com/about/locations for
            a list of such regions.
        labels (MutableSequence[google.cloud.databasecenter_v1beta.types.Label]):
            Labels applied on the resource. The
            requirements for labels assigned to Google Cloud
            resources may be found at
            https://cloud.google.com/resource-manager/docs/labels-overview#requirements
        tags (MutableSequence[google.cloud.databasecenter_v1beta.types.Tag]):
            Tags applied on the resource. The
            requirements for tags assigned to Google Cloud
            resources may be found at
            https://cloud.google.com/resource-manager/docs/tags/tags-overview
        resource_type (str):
            The type of resource defined according to the
            pattern: {Service Name}/{Type}. Ex:

            sqladmin.googleapis.com/Instance
            alloydb.googleapis.com/Cluster
            alloydb.googleapis.com/Instance
            spanner.googleapis.com/Instance
        sub_resource_type (google.cloud.databasecenter_v1beta.types.SubResourceType):
            Subtype of the resource specified at creation
            time.
        machine_config (google.cloud.databasecenter_v1beta.types.MachineConfig):
            Machine configuration like CPU, memory, etc
            for the resource.
        signal_groups (MutableSequence[google.cloud.databasecenter_v1beta.types.SignalGroup]):
            The list of signal groups and count of issues
            related to the resource. Only those signals
            which have been requested would be included.
        metrics (google.cloud.databasecenter_v1beta.types.Metrics):
            Observable metrics for the resource e.g. CPU
            utilization, memory utilization, etc.
        resource_category (google.cloud.databasecenter_v1beta.types.ResourceCategory):
            The category of the resource.
        resource_name (str):
            The name of the resource(The last part of the full resource
            name). Example: For full resource name -
            ``//cloudsql.googleapis.com/projects/project-number/instances/mysql-1``,
            resource name - ``mysql-1`` For full resource name -
            ``//cloudsql.googleapis.com/projects/project-number/instances/postgres-1``
            , resource name - ``postgres-1`` Note: In some cases, there
            might be more than one resource with the same resource name.
        backupdr_config (google.cloud.databasecenter_v1beta.types.BackupDRConfig):
            Optional. Backup and disaster recovery
            details for the resource.
        edition (google.cloud.databasecenter_v1beta.types.Edition):
            The edition of the resource.
        maintenance_info (google.cloud.databasecenter_v1beta.types.MaintenanceInfo):
            Optional. The maintenance information of the
            resource.
    """

    child_resources: MutableSequence["DatabaseResource"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="DatabaseResource",
    )
    full_resource_name: str = proto.Field(
        proto.STRING,
        number=3,
    )
    container: str = proto.Field(
        proto.STRING,
        number=4,
    )
    product: gcd_product.Product = proto.Field(
        proto.MESSAGE,
        number=5,
        message=gcd_product.Product,
    )
    location: str = proto.Field(
        proto.STRING,
        number=6,
    )
    labels: MutableSequence["Label"] = proto.RepeatedField(
        proto.MESSAGE,
        number=7,
        message="Label",
    )
    tags: MutableSequence["Tag"] = proto.RepeatedField(
        proto.MESSAGE,
        number=16,
        message="Tag",
    )
    resource_type: str = proto.Field(
        proto.STRING,
        number=8,
    )
    sub_resource_type: "SubResourceType" = proto.Field(
        proto.ENUM,
        number=9,
        enum="SubResourceType",
    )
    machine_config: gcd_machine_config.MachineConfig = proto.Field(
        proto.MESSAGE,
        number=12,
        message=gcd_machine_config.MachineConfig,
    )
    signal_groups: MutableSequence[signals.SignalGroup] = proto.RepeatedField(
        proto.MESSAGE,
        number=10,
        message=signals.SignalGroup,
    )
    metrics: metric_data.Metrics = proto.Field(
        proto.MESSAGE,
        number=13,
        message=metric_data.Metrics,
    )
    resource_category: "ResourceCategory" = proto.Field(
        proto.ENUM,
        number=14,
        enum="ResourceCategory",
    )
    resource_name: str = proto.Field(
        proto.STRING,
        number=15,
    )
    backupdr_config: "BackupDRConfig" = proto.Field(
        proto.MESSAGE,
        number=17,
        message="BackupDRConfig",
    )
    edition: "Edition" = proto.Field(
        proto.ENUM,
        number=18,
        enum="Edition",
    )
    maintenance_info: maintenance.MaintenanceInfo = proto.Field(
        proto.MESSAGE,
        number=19,
        message=maintenance.MaintenanceInfo,
    )


class Label(proto.Message):
    r"""Label is a key value pair applied to a resource.

    Attributes:
        key (str):
            The key part of the label.
        value (str):
            The value part of the label.
        source (str):
            The source of the Label. Source is empty if
            the label is directly attached to the resource
            and not inherited.
    """

    key: str = proto.Field(
        proto.STRING,
        number=1,
    )
    value: str = proto.Field(
        proto.STRING,
        number=2,
    )
    source: str = proto.Field(
        proto.STRING,
        number=3,
    )


class BackupDRConfig(proto.Message):
    r"""BackupDRConfig to capture the backup and disaster recovery
    details of database resource.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        backupdr_managed (bool):
            Indicates if the resource is managed by
            BackupDR.

            This field is a member of `oneof`_ ``_backupdr_managed``.
    """

    backupdr_managed: bool = proto.Field(
        proto.BOOL,
        number=1,
        optional=True,
    )


class Tag(proto.Message):
    r"""Tag is a key value pair attached to a resource.

    Attributes:
        key (str):

        value (str):
            The value part of the tag.
        source (str):
            The source of the tag. According to
            https://cloud.google.com/resource-manager/docs/tags/tags-overview#tags_and_labels,
            tags can be created only at the project or organization
            level. Tags can be inherited from different project as well
            not just the current project where the database resource is
            present. Format: "projects/{PROJECT_ID}",
            "projects/{PROJECT_NUMBER}",
            "organizations/{ORGANIZATION_ID}".
        inherited (bool):
            Indicates the inheritance status of a tag
            value attached to the given resource. If the tag
            value is inherited from one of the resource's
            ancestors, inherited will be true. If false,
            then the tag value is directly attached to the
            resource.
    """

    key: str = proto.Field(
        proto.STRING,
        number=1,
    )
    value: str = proto.Field(
        proto.STRING,
        number=2,
    )
    source: str = proto.Field(
        proto.STRING,
        number=3,
    )
    inherited: bool = proto.Field(
        proto.BOOL,
        number=4,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
