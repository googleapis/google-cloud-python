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


from google.protobuf import field_mask_pb2 as field_mask  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.datacatalog.v1beta1",
    manifest={
        "Taxonomy",
        "PolicyTag",
        "CreateTaxonomyRequest",
        "DeleteTaxonomyRequest",
        "UpdateTaxonomyRequest",
        "ListTaxonomiesRequest",
        "ListTaxonomiesResponse",
        "GetTaxonomyRequest",
        "CreatePolicyTagRequest",
        "DeletePolicyTagRequest",
        "UpdatePolicyTagRequest",
        "ListPolicyTagsRequest",
        "ListPolicyTagsResponse",
        "GetPolicyTagRequest",
    },
)


class Taxonomy(proto.Message):
    r"""A taxonomy is a collection of policy tags that classify data along a
    common axis. For instance a data *sensitivity* taxonomy could
    contain policy tags denoting PII such as age, zipcode, and SSN. A
    data *origin* taxonomy could contain policy tags to distinguish user
    data, employee data, partner data, public data.

    Attributes:
        name (str):
            Output only. Resource name of this taxonomy, whose format
            is:
            "projects/{project_number}/locations/{location_id}/taxonomies/{id}".
        display_name (str):
            Required. User defined name of this taxonomy.
            It must: contain only unicode letters, numbers,
            underscores, dashes and spaces; not start or end
            with spaces; and be at most 200 bytes long when
            encoded in UTF-8.
        description (str):
            Optional. Description of this taxonomy. It
            must: contain only unicode characters, tabs,
            newlines, carriage returns and page breaks; and
            be at most 2000 bytes long when encoded in
            UTF-8. If not set, defaults to an empty
            description.
        activated_policy_types (Sequence[~.policytagmanager.Taxonomy.PolicyType]):
            Optional. A list of policy types that are
            activated for this taxonomy. If not set,
            defaults to an empty list.
    """

    class PolicyType(proto.Enum):
        r"""Defines policy types where policy tag can be used for."""
        POLICY_TYPE_UNSPECIFIED = 0
        FINE_GRAINED_ACCESS_CONTROL = 1

    name = proto.Field(proto.STRING, number=1)

    display_name = proto.Field(proto.STRING, number=2)

    description = proto.Field(proto.STRING, number=3)

    activated_policy_types = proto.RepeatedField(proto.ENUM, number=6, enum=PolicyType,)


class PolicyTag(proto.Message):
    r"""Denotes one policy tag in a taxonomy (e.g. ssn). Policy Tags
    can be defined in a hierarchy. For example, consider the
    following hierarchy: Geolocation -&gt; (LatLong, City, ZipCode).
    PolicyTag "Geolocation" contains three child policy tags:
    "LatLong", "City", and "ZipCode".

    Attributes:
        name (str):
            Output only. Resource name of this policy tag, whose format
            is:
            "projects/{project_number}/locations/{location_id}/taxonomies/{taxonomy_id}/policyTags/{id}".
        display_name (str):
            Required. User defined name of this policy
            tag. It must: be unique within the parent
            taxonomy; contain only unicode letters, numbers,
            underscores, dashes and spaces; not start or end
            with spaces; and be at most 200 bytes long when
            encoded in UTF-8.
        description (str):
            Description of this policy tag. It must:
            contain only unicode characters, tabs, newlines,
            carriage returns and page breaks; and be at most
            2000 bytes long when encoded in UTF-8. If not
            set, defaults to an empty description. If not
            set, defaults to an empty description.
        parent_policy_tag (str):
            Resource name of this policy tag's parent
            policy tag (e.g. for the "LatLong" policy tag in
            the example above, this field contains the
            resource name of the "Geolocation" policy tag).
            If empty, it means this policy tag is a top
            level policy tag (e.g. this field is empty for
            the "Geolocation" policy tag in the example
            above). If not set, defaults to an empty string.
        child_policy_tags (Sequence[str]):
            Output only. Resource names of child policy
            tags of this policy tag.
    """

    name = proto.Field(proto.STRING, number=1)

    display_name = proto.Field(proto.STRING, number=2)

    description = proto.Field(proto.STRING, number=3)

    parent_policy_tag = proto.Field(proto.STRING, number=4)

    child_policy_tags = proto.RepeatedField(proto.STRING, number=5)


class CreateTaxonomyRequest(proto.Message):
    r"""Request message for
    [CreateTaxonomy][google.cloud.datacatalog.v1beta1.PolicyTagManager.CreateTaxonomy].

    Attributes:
        parent (str):
            Required. Resource name of the project that
            the taxonomy will belong to.
        taxonomy (~.policytagmanager.Taxonomy):
            The taxonomy to be created.
    """

    parent = proto.Field(proto.STRING, number=1)

    taxonomy = proto.Field(proto.MESSAGE, number=2, message="Taxonomy",)


class DeleteTaxonomyRequest(proto.Message):
    r"""Request message for
    [DeleteTaxonomy][google.cloud.datacatalog.v1beta1.PolicyTagManager.DeleteTaxonomy].

    Attributes:
        name (str):
            Required. Resource name of the taxonomy to be
            deleted. All policy tags in this taxonomy will
            also be deleted.
    """

    name = proto.Field(proto.STRING, number=1)


class UpdateTaxonomyRequest(proto.Message):
    r"""Request message for
    [UpdateTaxonomy][google.cloud.datacatalog.v1beta1.PolicyTagManager.UpdateTaxonomy].

    Attributes:
        taxonomy (~.policytagmanager.Taxonomy):
            The taxonomy to update. Only description, display_name, and
            activated policy types can be updated.
        update_mask (~.field_mask.FieldMask):
            The update mask applies to the resource. For the
            ``FieldMask`` definition, see
            https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#fieldmask
            If not set, defaults to all of the fields that are allowed
            to update.
    """

    taxonomy = proto.Field(proto.MESSAGE, number=1, message="Taxonomy",)

    update_mask = proto.Field(proto.MESSAGE, number=2, message=field_mask.FieldMask,)


class ListTaxonomiesRequest(proto.Message):
    r"""Request message for
    [ListTaxonomies][google.cloud.datacatalog.v1beta1.PolicyTagManager.ListTaxonomies].

    Attributes:
        parent (str):
            Required. Resource name of the project to
            list the taxonomies of.
        page_size (int):
            The maximum number of items to return. Must
            be a value between 1 and 1000. If not set,
            defaults to 50.
        page_token (str):
            The next_page_token value returned from a previous list
            request, if any. If not set, defaults to an empty string.
    """

    parent = proto.Field(proto.STRING, number=1)

    page_size = proto.Field(proto.INT32, number=2)

    page_token = proto.Field(proto.STRING, number=3)


class ListTaxonomiesResponse(proto.Message):
    r"""Response message for
    [ListTaxonomies][google.cloud.datacatalog.v1beta1.PolicyTagManager.ListTaxonomies].

    Attributes:
        taxonomies (Sequence[~.policytagmanager.Taxonomy]):
            Taxonomies that the project contains.
        next_page_token (str):
            Token used to retrieve the next page of
            results, or empty if there are no more results
            in the list.
    """

    @property
    def raw_page(self):
        return self

    taxonomies = proto.RepeatedField(proto.MESSAGE, number=1, message="Taxonomy",)

    next_page_token = proto.Field(proto.STRING, number=2)


class GetTaxonomyRequest(proto.Message):
    r"""Request message for
    [GetTaxonomy][google.cloud.datacatalog.v1beta1.PolicyTagManager.GetTaxonomy].

    Attributes:
        name (str):
            Required. Resource name of the requested
            taxonomy.
    """

    name = proto.Field(proto.STRING, number=1)


class CreatePolicyTagRequest(proto.Message):
    r"""Request message for
    [CreatePolicyTag][google.cloud.datacatalog.v1beta1.PolicyTagManager.CreatePolicyTag].

    Attributes:
        parent (str):
            Required. Resource name of the taxonomy that
            the policy tag will belong to.
        policy_tag (~.policytagmanager.PolicyTag):
            The policy tag to be created.
    """

    parent = proto.Field(proto.STRING, number=1)

    policy_tag = proto.Field(proto.MESSAGE, number=2, message="PolicyTag",)


class DeletePolicyTagRequest(proto.Message):
    r"""Request message for
    [DeletePolicyTag][google.cloud.datacatalog.v1beta1.PolicyTagManager.DeletePolicyTag].

    Attributes:
        name (str):
            Required. Resource name of the policy tag to
            be deleted. All of its descendant policy tags
            will also be deleted.
    """

    name = proto.Field(proto.STRING, number=1)


class UpdatePolicyTagRequest(proto.Message):
    r"""Request message for
    [UpdatePolicyTag][google.cloud.datacatalog.v1beta1.PolicyTagManager.UpdatePolicyTag].

    Attributes:
        policy_tag (~.policytagmanager.PolicyTag):
            The policy tag to update. Only the description,
            display_name, and parent_policy_tag fields can be updated.
        update_mask (~.field_mask.FieldMask):
            The update mask applies to the resource. Only display_name,
            description and parent_policy_tag can be updated and thus
            can be listed in the mask. If update_mask is not provided,
            all allowed fields (i.e. display_name, description and
            parent) will be updated. For more information including the
            ``FieldMask`` definition, see
            https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#fieldmask
            If not set, defaults to all of the fields that are allowed
            to update.
    """

    policy_tag = proto.Field(proto.MESSAGE, number=1, message="PolicyTag",)

    update_mask = proto.Field(proto.MESSAGE, number=2, message=field_mask.FieldMask,)


class ListPolicyTagsRequest(proto.Message):
    r"""Request message for
    [ListPolicyTags][google.cloud.datacatalog.v1beta1.PolicyTagManager.ListPolicyTags].

    Attributes:
        parent (str):
            Required. Resource name of the taxonomy to
            list the policy tags of.
        page_size (int):
            The maximum number of items to return. Must
            be a value between 1 and 1000. If not set,
            defaults to 50.
        page_token (str):
            The next_page_token value returned from a previous List
            request, if any. If not set, defaults to an empty string.
    """

    parent = proto.Field(proto.STRING, number=1)

    page_size = proto.Field(proto.INT32, number=2)

    page_token = proto.Field(proto.STRING, number=3)


class ListPolicyTagsResponse(proto.Message):
    r"""Response message for
    [ListPolicyTags][google.cloud.datacatalog.v1beta1.PolicyTagManager.ListPolicyTags].

    Attributes:
        policy_tags (Sequence[~.policytagmanager.PolicyTag]):
            The policy tags that are in the requested
            taxonomy.
        next_page_token (str):
            Token used to retrieve the next page of
            results, or empty if there are no more results
            in the list.
    """

    @property
    def raw_page(self):
        return self

    policy_tags = proto.RepeatedField(proto.MESSAGE, number=1, message="PolicyTag",)

    next_page_token = proto.Field(proto.STRING, number=2)


class GetPolicyTagRequest(proto.Message):
    r"""Request message for
    [GetPolicyTag][google.cloud.datacatalog.v1beta1.PolicyTagManager.GetPolicyTag].

    Attributes:
        name (str):
            Required. Resource name of the requested
            policy tag.
    """

    name = proto.Field(proto.STRING, number=1)


__all__ = tuple(sorted(__protobuf__.manifest))
