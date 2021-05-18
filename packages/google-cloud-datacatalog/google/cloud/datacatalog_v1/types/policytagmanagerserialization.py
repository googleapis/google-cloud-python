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

from google.cloud.datacatalog_v1.types import policytagmanager


__protobuf__ = proto.module(
    package="google.cloud.datacatalog.v1",
    manifest={
        "SerializedTaxonomy",
        "SerializedPolicyTag",
        "ImportTaxonomiesRequest",
        "InlineSource",
        "CrossRegionalSource",
        "ImportTaxonomiesResponse",
        "ExportTaxonomiesRequest",
        "ExportTaxonomiesResponse",
    },
)


class SerializedTaxonomy(proto.Message):
    r"""Message representing a taxonomy, including its policy tags in
    hierarchy, as a nested proto. Used for taxonomy replacement,
    import, and export.

    Attributes:
        display_name (str):
            Required. Display name of the taxonomy. At
            most 200 bytes when encoded in UTF-8.
        description (str):
            Description of the serialized taxonomy. At
            most 2000 bytes when encoded in UTF-8. If not
            set, defaults to an empty description.
        policy_tags (Sequence[google.cloud.datacatalog_v1.types.SerializedPolicyTag]):
            Top level policy tags associated with the
            taxonomy, if any.
        activated_policy_types (Sequence[google.cloud.datacatalog_v1.types.Taxonomy.PolicyType]):
            A list of policy types that are activated per
            taxonomy.
    """

    display_name = proto.Field(proto.STRING, number=1,)
    description = proto.Field(proto.STRING, number=2,)
    policy_tags = proto.RepeatedField(
        proto.MESSAGE, number=3, message="SerializedPolicyTag",
    )
    activated_policy_types = proto.RepeatedField(
        proto.ENUM, number=4, enum=policytagmanager.Taxonomy.PolicyType,
    )


class SerializedPolicyTag(proto.Message):
    r"""Message representing one policy tag, including all its
    descendant policy tags, as a nested proto.

    Attributes:
        policy_tag (str):
            Resource name of the policy tag.
            This field will be ignored when calling
            ImportTaxonomies.
        display_name (str):
            Required. Display name of the policy tag. At
            most 200 bytes when encoded in UTF-8.
        description (str):
            Description of the serialized policy tag. The
            length of the description is limited to 2000
            bytes when encoded in UTF-8. If not set,
            defaults to an empty description.
        child_policy_tags (Sequence[google.cloud.datacatalog_v1.types.SerializedPolicyTag]):
            Children of the policy tag, if any.
    """

    policy_tag = proto.Field(proto.STRING, number=1,)
    display_name = proto.Field(proto.STRING, number=2,)
    description = proto.Field(proto.STRING, number=3,)
    child_policy_tags = proto.RepeatedField(
        proto.MESSAGE, number=4, message="SerializedPolicyTag",
    )


class ImportTaxonomiesRequest(proto.Message):
    r"""Request message for
    [ImportTaxonomies][google.cloud.datacatalog.v1.PolicyTagManagerSerialization.ImportTaxonomies].

    Attributes:
        parent (str):
            Required. Resource name of project that the
            imported taxonomies will belong to.
        inline_source (google.cloud.datacatalog_v1.types.InlineSource):
            Inline source used for taxonomies import.
        cross_regional_source (google.cloud.datacatalog_v1.types.CrossRegionalSource):
            Cross-regional source taxonomy to be
            imported.
    """

    parent = proto.Field(proto.STRING, number=1,)
    inline_source = proto.Field(
        proto.MESSAGE, number=2, oneof="source", message="InlineSource",
    )
    cross_regional_source = proto.Field(
        proto.MESSAGE, number=3, oneof="source", message="CrossRegionalSource",
    )


class InlineSource(proto.Message):
    r"""Inline source containing taxonomies to import.
    Attributes:
        taxonomies (Sequence[google.cloud.datacatalog_v1.types.SerializedTaxonomy]):
            Required. Taxonomies to be imported.
    """

    taxonomies = proto.RepeatedField(
        proto.MESSAGE, number=1, message="SerializedTaxonomy",
    )


class CrossRegionalSource(proto.Message):
    r"""Cross-regional source used to import an existing taxonomy
    into a different region.

    Attributes:
        taxonomy (str):
            Required. The resource name of the source
            taxonomy to be imported.
    """

    taxonomy = proto.Field(proto.STRING, number=1,)


class ImportTaxonomiesResponse(proto.Message):
    r"""Response message for
    [ImportTaxonomies][google.cloud.datacatalog.v1.PolicyTagManagerSerialization.ImportTaxonomies].

    Attributes:
        taxonomies (Sequence[google.cloud.datacatalog_v1.types.Taxonomy]):
            Taxonomies that were imported.
    """

    taxonomies = proto.RepeatedField(
        proto.MESSAGE, number=1, message=policytagmanager.Taxonomy,
    )


class ExportTaxonomiesRequest(proto.Message):
    r"""Request message for
    [ExportTaxonomies][google.cloud.datacatalog.v1.PolicyTagManagerSerialization.ExportTaxonomies].

    Attributes:
        parent (str):
            Required. Resource name of the project that
            the exported taxonomies belong to.
        taxonomies (Sequence[str]):
            Required. Resource names of the taxonomies to
            be exported.
        serialized_taxonomies (bool):
            Export taxonomies as serialized taxonomies,
            which contain all the policy tags as nested
            protos.
    """

    parent = proto.Field(proto.STRING, number=1,)
    taxonomies = proto.RepeatedField(proto.STRING, number=2,)
    serialized_taxonomies = proto.Field(proto.BOOL, number=3, oneof="destination",)


class ExportTaxonomiesResponse(proto.Message):
    r"""Response message for
    [ExportTaxonomies][google.cloud.datacatalog.v1.PolicyTagManagerSerialization.ExportTaxonomies].

    Attributes:
        taxonomies (Sequence[google.cloud.datacatalog_v1.types.SerializedTaxonomy]):
            List of taxonomies and policy tags as nested
            protos.
    """

    taxonomies = proto.RepeatedField(
        proto.MESSAGE, number=1, message="SerializedTaxonomy",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
