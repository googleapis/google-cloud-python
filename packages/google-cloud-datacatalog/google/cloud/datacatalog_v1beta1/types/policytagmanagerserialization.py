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

from google.cloud.datacatalog_v1beta1.types import policytagmanager


__protobuf__ = proto.module(
    package="google.cloud.datacatalog.v1beta1",
    manifest={
        "SerializedTaxonomy",
        "SerializedPolicyTag",
        "ImportTaxonomiesRequest",
        "InlineSource",
        "ImportTaxonomiesResponse",
        "ExportTaxonomiesRequest",
        "ExportTaxonomiesResponse",
    },
)


class SerializedTaxonomy(proto.Message):
    r"""Message capturing a taxonomy and its policy tag hierarchy as
    a nested proto. Used for taxonomy import/export and mutation.

    Attributes:
        display_name (str):
            Required. Display name of the taxonomy. Max
            200 bytes when encoded in UTF-8.
        description (str):
            Description of the serialized taxonomy. The
            length of the description is limited to 2000
            bytes when encoded in UTF-8. If not set,
            defaults to an empty description.
        policy_tags (Sequence[google.cloud.datacatalog_v1beta1.types.SerializedPolicyTag]):
            Top level policy tags associated with the
            taxonomy if any.
    """

    display_name = proto.Field(proto.STRING, number=1,)
    description = proto.Field(proto.STRING, number=2,)
    policy_tags = proto.RepeatedField(
        proto.MESSAGE, number=3, message="SerializedPolicyTag",
    )


class SerializedPolicyTag(proto.Message):
    r"""Message representing one policy tag when exported as a nested
    proto.

    Attributes:
        display_name (str):
            Required. Display name of the policy tag. Max
            200 bytes when encoded in UTF-8.
        description (str):
            Description of the serialized policy tag. The
            length of the description is limited to 2000
            bytes when encoded in UTF-8. If not set,
            defaults to an empty description.
        child_policy_tags (Sequence[google.cloud.datacatalog_v1beta1.types.SerializedPolicyTag]):
            Children of the policy tag if any.
    """

    display_name = proto.Field(proto.STRING, number=2,)
    description = proto.Field(proto.STRING, number=3,)
    child_policy_tags = proto.RepeatedField(
        proto.MESSAGE, number=4, message="SerializedPolicyTag",
    )


class ImportTaxonomiesRequest(proto.Message):
    r"""Request message for
    [ImportTaxonomies][google.cloud.datacatalog.v1beta1.PolicyTagManagerSerialization.ImportTaxonomies].

    Attributes:
        parent (str):
            Required. Resource name of project that the
            newly created taxonomies will belong to.
        inline_source (google.cloud.datacatalog_v1beta1.types.InlineSource):
            Inline source used for taxonomies import
    """

    parent = proto.Field(proto.STRING, number=1,)
    inline_source = proto.Field(
        proto.MESSAGE, number=2, oneof="source", message="InlineSource",
    )


class InlineSource(proto.Message):
    r"""Inline source used for taxonomies import.
    Attributes:
        taxonomies (Sequence[google.cloud.datacatalog_v1beta1.types.SerializedTaxonomy]):
            Required. Taxonomies to be imported.
    """

    taxonomies = proto.RepeatedField(
        proto.MESSAGE, number=1, message="SerializedTaxonomy",
    )


class ImportTaxonomiesResponse(proto.Message):
    r"""Response message for
    [ImportTaxonomies][google.cloud.datacatalog.v1beta1.PolicyTagManagerSerialization.ImportTaxonomies].

    Attributes:
        taxonomies (Sequence[google.cloud.datacatalog_v1beta1.types.Taxonomy]):
            Taxonomies that were imported.
    """

    taxonomies = proto.RepeatedField(
        proto.MESSAGE, number=1, message=policytagmanager.Taxonomy,
    )


class ExportTaxonomiesRequest(proto.Message):
    r"""Request message for
    [ExportTaxonomies][google.cloud.datacatalog.v1beta1.PolicyTagManagerSerialization.ExportTaxonomies].

    Attributes:
        parent (str):
            Required. Resource name of the project that
            taxonomies to be exported will share.
        taxonomies (Sequence[str]):
            Required. Resource names of the taxonomies to
            be exported.
        serialized_taxonomies (bool):
            Export taxonomies as serialized taxonomies.
    """

    parent = proto.Field(proto.STRING, number=1,)
    taxonomies = proto.RepeatedField(proto.STRING, number=2,)
    serialized_taxonomies = proto.Field(proto.BOOL, number=3, oneof="destination",)


class ExportTaxonomiesResponse(proto.Message):
    r"""Response message for
    [ExportTaxonomies][google.cloud.datacatalog.v1beta1.PolicyTagManagerSerialization.ExportTaxonomies].

    Attributes:
        taxonomies (Sequence[google.cloud.datacatalog_v1beta1.types.SerializedTaxonomy]):
            List of taxonomies and policy tags in a tree
            structure.
    """

    taxonomies = proto.RepeatedField(
        proto.MESSAGE, number=1, message="SerializedTaxonomy",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
