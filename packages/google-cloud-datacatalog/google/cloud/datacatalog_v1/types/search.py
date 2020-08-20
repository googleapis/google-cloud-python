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


from google.cloud.datacatalog_v1.types import common


__protobuf__ = proto.module(
    package="google.cloud.datacatalog.v1",
    manifest={"SearchResultType", "SearchCatalogResult",},
)


class SearchResultType(proto.Enum):
    r"""The different types of resources that can be returned in
    search.
    """
    SEARCH_RESULT_TYPE_UNSPECIFIED = 0
    ENTRY = 1
    TAG_TEMPLATE = 2
    ENTRY_GROUP = 3


class SearchCatalogResult(proto.Message):
    r"""A result that appears in the response of a search request.
    Each result captures details of one entry that matches the
    search.

    Attributes:
        search_result_type (~.search.SearchResultType):
            Type of the search result. This field can be
            used to determine which Get method to call to
            fetch the full resource.
        search_result_subtype (str):
            Sub-type of the search result. This is a dot-delimited
            description of the resource's full type, and is the same as
            the value callers would provide in the "type" search facet.
            Examples: ``entry.table``, ``entry.dataStream``,
            ``tagTemplate``.
        relative_resource_name (str):
            The relative resource name of the resource in URL format.
            Examples:

            -  ``projects/{project_id}/locations/{location_id}/entryGroups/{entry_group_id}/entries/{entry_id}``
            -  ``projects/{project_id}/tagTemplates/{tag_template_id}``
        linked_resource (str):
            The full name of the cloud resource the entry belongs to.
            See:
            https://cloud.google.com/apis/design/resource_names#full_resource_name.
            Example:

            -  ``//bigquery.googleapis.com/projects/projectId/datasets/datasetId/tables/tableId``
        integrated_system (~.common.IntegratedSystem):
            Output only. This field indicates the entry's
            source system that Data Catalog integrates with,
            such as BigQuery or Cloud Pub/Sub.
        user_specified_system (str):
            This field indicates the entry's source
            system that Data Catalog does not integrate
            with.
    """

    search_result_type = proto.Field(proto.ENUM, number=1, enum="SearchResultType",)

    search_result_subtype = proto.Field(proto.STRING, number=2)

    relative_resource_name = proto.Field(proto.STRING, number=3)

    linked_resource = proto.Field(proto.STRING, number=4)

    integrated_system = proto.Field(
        proto.ENUM, number=8, oneof="system", enum=common.IntegratedSystem,
    )

    user_specified_system = proto.Field(proto.STRING, number=9, oneof="system")


__all__ = tuple(sorted(__protobuf__.manifest))
