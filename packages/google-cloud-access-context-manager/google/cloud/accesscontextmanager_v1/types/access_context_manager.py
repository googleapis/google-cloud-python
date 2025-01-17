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
import proto  # type: ignore

from google.cloud.accesscontextmanager_v1.types import access_level as gia_access_level
from google.cloud.accesscontextmanager_v1.types import (
    gcp_user_access_binding as gia_gcp_user_access_binding,
)
from google.cloud.accesscontextmanager_v1.types import (
    service_perimeter as gia_service_perimeter,
)
from google.cloud.accesscontextmanager_v1.types import access_policy

__protobuf__ = proto.module(
    package="google.cloud.accesscontextmanager.v1",
    manifest={
        "LevelFormat",
        "ListAccessPoliciesRequest",
        "ListAccessPoliciesResponse",
        "GetAccessPolicyRequest",
        "UpdateAccessPolicyRequest",
        "DeleteAccessPolicyRequest",
        "ListAccessLevelsRequest",
        "ListAccessLevelsResponse",
        "GetAccessLevelRequest",
        "CreateAccessLevelRequest",
        "UpdateAccessLevelRequest",
        "DeleteAccessLevelRequest",
        "ReplaceAccessLevelsRequest",
        "ReplaceAccessLevelsResponse",
        "ListServicePerimetersRequest",
        "ListServicePerimetersResponse",
        "GetServicePerimeterRequest",
        "CreateServicePerimeterRequest",
        "UpdateServicePerimeterRequest",
        "DeleteServicePerimeterRequest",
        "ReplaceServicePerimetersRequest",
        "ReplaceServicePerimetersResponse",
        "CommitServicePerimetersRequest",
        "CommitServicePerimetersResponse",
        "ListGcpUserAccessBindingsRequest",
        "ListGcpUserAccessBindingsResponse",
        "GetGcpUserAccessBindingRequest",
        "CreateGcpUserAccessBindingRequest",
        "UpdateGcpUserAccessBindingRequest",
        "DeleteGcpUserAccessBindingRequest",
        "GcpUserAccessBindingOperationMetadata",
        "AccessContextManagerOperationMetadata",
    },
)


class LevelFormat(proto.Enum):
    r"""The format used in an ``AccessLevel``.

    Values:
        LEVEL_FORMAT_UNSPECIFIED (0):
            The format was not specified.
        AS_DEFINED (1):
            Uses the format the resource was defined in.
            BasicLevels are returned as BasicLevels,
            CustomLevels are returned as CustomLevels.
        CEL (2):
            Use Cloud Common Expression Language when
            returning the resource.  Both BasicLevels and
            CustomLevels are returned as CustomLevels.
    """
    LEVEL_FORMAT_UNSPECIFIED = 0
    AS_DEFINED = 1
    CEL = 2


class ListAccessPoliciesRequest(proto.Message):
    r"""A request to list all ``AccessPolicies`` for a container.

    Attributes:
        parent (str):
            Required. Resource name for the container to list
            AccessPolicy instances from.

            Format: ``organizations/{org_id}``
        page_size (int):
            Number of AccessPolicy instances to include
            in the list. Default 100.
        page_token (str):
            Next page token for the next batch of
            AccessPolicy instances. Defaults to the first
            page of results.
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


class ListAccessPoliciesResponse(proto.Message):
    r"""A response to ``ListAccessPoliciesRequest``.

    Attributes:
        access_policies (MutableSequence[google.cloud.accesscontextmanager_v1.types.AccessPolicy]):
            List of the AccessPolicy instances.
        next_page_token (str):
            The pagination token to retrieve the next
            page of results. If the value is empty, no
            further results remain.
    """

    @property
    def raw_page(self):
        return self

    access_policies: MutableSequence[access_policy.AccessPolicy] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=access_policy.AccessPolicy,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetAccessPolicyRequest(proto.Message):
    r"""A request to get a particular ``AccessPolicy``.

    Attributes:
        name (str):
            Required. Resource name for the access policy to get.

            Format ``accessPolicies/{policy_id}``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class UpdateAccessPolicyRequest(proto.Message):
    r"""A request to update an ``AccessPolicy``.

    Attributes:
        policy (google.cloud.accesscontextmanager_v1.types.AccessPolicy):
            Required. The updated AccessPolicy.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Mask to control which fields get
            updated. Must be non-empty.
    """

    policy: access_policy.AccessPolicy = proto.Field(
        proto.MESSAGE,
        number=1,
        message=access_policy.AccessPolicy,
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class DeleteAccessPolicyRequest(proto.Message):
    r"""A request to delete an ``AccessPolicy``.

    Attributes:
        name (str):
            Required. Resource name for the access policy to delete.

            Format ``accessPolicies/{policy_id}``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListAccessLevelsRequest(proto.Message):
    r"""A request to list all ``AccessLevels`` in an ``AccessPolicy``.

    Attributes:
        parent (str):
            Required. Resource name for the access policy to list
            [Access Levels]
            [google.identity.accesscontextmanager.v1.AccessLevel] from.

            Format: ``accessPolicies/{policy_id}``
        page_size (int):
            Number of [Access Levels]
            [google.identity.accesscontextmanager.v1.AccessLevel] to
            include in the list. Default 100.
        page_token (str):
            Next page token for the next batch of [Access Level]
            [google.identity.accesscontextmanager.v1.AccessLevel]
            instances. Defaults to the first page of results.
        access_level_format (google.cloud.accesscontextmanager_v1.types.LevelFormat):
            Whether to return ``BasicLevels`` in the Cloud Common
            Expression language, as ``CustomLevels``, rather than as
            ``BasicLevels``. Defaults to returning ``AccessLevels`` in
            the format they were defined.
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
    access_level_format: "LevelFormat" = proto.Field(
        proto.ENUM,
        number=4,
        enum="LevelFormat",
    )


class ListAccessLevelsResponse(proto.Message):
    r"""A response to ``ListAccessLevelsRequest``.

    Attributes:
        access_levels (MutableSequence[google.cloud.accesscontextmanager_v1.types.AccessLevel]):
            List of the [Access Level]
            [google.identity.accesscontextmanager.v1.AccessLevel]
            instances.
        next_page_token (str):
            The pagination token to retrieve the next
            page of results. If the value is empty, no
            further results remain.
    """

    @property
    def raw_page(self):
        return self

    access_levels: MutableSequence[gia_access_level.AccessLevel] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=gia_access_level.AccessLevel,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetAccessLevelRequest(proto.Message):
    r"""A request to get a particular ``AccessLevel``.

    Attributes:
        name (str):
            Required. Resource name for the [Access Level]
            [google.identity.accesscontextmanager.v1.AccessLevel].

            Format:
            ``accessPolicies/{policy_id}/accessLevels/{access_level_id}``
        access_level_format (google.cloud.accesscontextmanager_v1.types.LevelFormat):
            Whether to return ``BasicLevels`` in the Cloud Common
            Expression Language rather than as ``BasicLevels``. Defaults
            to AS_DEFINED, where [Access Levels]
            [google.identity.accesscontextmanager.v1.AccessLevel] are
            returned as ``BasicLevels`` or ``CustomLevels`` based on how
            they were created. If set to CEL, all [Access Levels]
            [google.identity.accesscontextmanager.v1.AccessLevel] are
            returned as ``CustomLevels``. In the CEL case,
            ``BasicLevels`` are translated to equivalent
            ``CustomLevels``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    access_level_format: "LevelFormat" = proto.Field(
        proto.ENUM,
        number=2,
        enum="LevelFormat",
    )


class CreateAccessLevelRequest(proto.Message):
    r"""A request to create an ``AccessLevel``.

    Attributes:
        parent (str):
            Required. Resource name for the access policy which owns
            this [Access Level]
            [google.identity.accesscontextmanager.v1.AccessLevel].

            Format: ``accessPolicies/{policy_id}``
        access_level (google.cloud.accesscontextmanager_v1.types.AccessLevel):
            Required. The [Access Level]
            [google.identity.accesscontextmanager.v1.AccessLevel] to
            create. Syntactic correctness of the [Access Level]
            [google.identity.accesscontextmanager.v1.AccessLevel] is a
            precondition for creation.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    access_level: gia_access_level.AccessLevel = proto.Field(
        proto.MESSAGE,
        number=2,
        message=gia_access_level.AccessLevel,
    )


class UpdateAccessLevelRequest(proto.Message):
    r"""A request to update an ``AccessLevel``.

    Attributes:
        access_level (google.cloud.accesscontextmanager_v1.types.AccessLevel):
            Required. The updated [Access Level]
            [google.identity.accesscontextmanager.v1.AccessLevel].
            Syntactic correctness of the [Access Level]
            [google.identity.accesscontextmanager.v1.AccessLevel] is a
            precondition for creation.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Mask to control which fields get
            updated. Must be non-empty.
    """

    access_level: gia_access_level.AccessLevel = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gia_access_level.AccessLevel,
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class DeleteAccessLevelRequest(proto.Message):
    r"""A request to delete an ``AccessLevel``.

    Attributes:
        name (str):
            Required. Resource name for the [Access Level]
            [google.identity.accesscontextmanager.v1.AccessLevel].

            Format:
            ``accessPolicies/{policy_id}/accessLevels/{access_level_id}``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ReplaceAccessLevelsRequest(proto.Message):
    r"""A request to replace all existing Access Levels in an Access
    Policy with the Access Levels provided. This is done atomically.

    Attributes:
        parent (str):
            Required. Resource name for the access policy which owns
            these [Access Levels]
            [google.identity.accesscontextmanager.v1.AccessLevel].

            Format: ``accessPolicies/{policy_id}``
        access_levels (MutableSequence[google.cloud.accesscontextmanager_v1.types.AccessLevel]):
            Required. The desired [Access Levels]
            [google.identity.accesscontextmanager.v1.AccessLevel] that
            should replace all existing [Access Levels]
            [google.identity.accesscontextmanager.v1.AccessLevel] in the
            [Access Policy]
            [google.identity.accesscontextmanager.v1.AccessPolicy].
        etag (str):
            Optional. The etag for the version of the [Access Policy]
            [google.identity.accesscontextmanager.v1.AccessPolicy] that
            this replace operation is to be performed on. If, at the
            time of replace, the etag for the Access Policy stored in
            Access Context Manager is different from the specified etag,
            then the replace operation will not be performed and the
            call will fail. This field is not required. If etag is not
            provided, the operation will be performed as if a valid etag
            is provided.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    access_levels: MutableSequence[gia_access_level.AccessLevel] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message=gia_access_level.AccessLevel,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=4,
    )


class ReplaceAccessLevelsResponse(proto.Message):
    r"""A response to ReplaceAccessLevelsRequest. This will be put
    inside of Operation.response field.

    Attributes:
        access_levels (MutableSequence[google.cloud.accesscontextmanager_v1.types.AccessLevel]):
            List of the [Access Level]
            [google.identity.accesscontextmanager.v1.AccessLevel]
            instances.
    """

    access_levels: MutableSequence[gia_access_level.AccessLevel] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=gia_access_level.AccessLevel,
    )


class ListServicePerimetersRequest(proto.Message):
    r"""A request to list all ``ServicePerimeters`` in an ``AccessPolicy``.

    Attributes:
        parent (str):
            Required. Resource name for the access policy to list
            [Service Perimeters]
            [google.identity.accesscontextmanager.v1.ServicePerimeter]
            from.

            Format: ``accessPolicies/{policy_id}``
        page_size (int):
            Number of [Service Perimeters]
            [google.identity.accesscontextmanager.v1.ServicePerimeter]
            to include in the list. Default 100.
        page_token (str):
            Next page token for the next batch of [Service Perimeter]
            [google.identity.accesscontextmanager.v1.ServicePerimeter]
            instances. Defaults to the first page of results.
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


class ListServicePerimetersResponse(proto.Message):
    r"""A response to ``ListServicePerimetersRequest``.

    Attributes:
        service_perimeters (MutableSequence[google.cloud.accesscontextmanager_v1.types.ServicePerimeter]):
            List of the [Service Perimeter]
            [google.identity.accesscontextmanager.v1.ServicePerimeter]
            instances.
        next_page_token (str):
            The pagination token to retrieve the next
            page of results. If the value is empty, no
            further results remain.
    """

    @property
    def raw_page(self):
        return self

    service_perimeters: MutableSequence[
        gia_service_perimeter.ServicePerimeter
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=gia_service_perimeter.ServicePerimeter,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetServicePerimeterRequest(proto.Message):
    r"""A request to get a particular ``ServicePerimeter``.

    Attributes:
        name (str):
            Required. Resource name for the [Service Perimeter]
            [google.identity.accesscontextmanager.v1.ServicePerimeter].

            Format:
            ``accessPolicies/{policy_id}/servicePerimeters/{service_perimeters_id}``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateServicePerimeterRequest(proto.Message):
    r"""A request to create a ``ServicePerimeter``.

    Attributes:
        parent (str):
            Required. Resource name for the access policy which owns
            this [Service Perimeter]
            [google.identity.accesscontextmanager.v1.ServicePerimeter].

            Format: ``accessPolicies/{policy_id}``
        service_perimeter (google.cloud.accesscontextmanager_v1.types.ServicePerimeter):
            Required. The [Service Perimeter]
            [google.identity.accesscontextmanager.v1.ServicePerimeter]
            to create. Syntactic correctness of the [Service Perimeter]
            [google.identity.accesscontextmanager.v1.ServicePerimeter]
            is a precondition for creation.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    service_perimeter: gia_service_perimeter.ServicePerimeter = proto.Field(
        proto.MESSAGE,
        number=2,
        message=gia_service_perimeter.ServicePerimeter,
    )


class UpdateServicePerimeterRequest(proto.Message):
    r"""A request to update a ``ServicePerimeter``.

    Attributes:
        service_perimeter (google.cloud.accesscontextmanager_v1.types.ServicePerimeter):
            Required. The updated ``ServicePerimeter``. Syntactic
            correctness of the ``ServicePerimeter`` is a precondition
            for creation.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Mask to control which fields get
            updated. Must be non-empty.
    """

    service_perimeter: gia_service_perimeter.ServicePerimeter = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gia_service_perimeter.ServicePerimeter,
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class DeleteServicePerimeterRequest(proto.Message):
    r"""A request to delete a ``ServicePerimeter``.

    Attributes:
        name (str):
            Required. Resource name for the [Service Perimeter]
            [google.identity.accesscontextmanager.v1.ServicePerimeter].

            Format:
            ``accessPolicies/{policy_id}/servicePerimeters/{service_perimeter_id}``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ReplaceServicePerimetersRequest(proto.Message):
    r"""A request to replace all existing Service Perimeters in an
    Access Policy with the Service Perimeters provided. This is done
    atomically.

    Attributes:
        parent (str):
            Required. Resource name for the access policy which owns
            these [Service Perimeters]
            [google.identity.accesscontextmanager.v1.ServicePerimeter].

            Format: ``accessPolicies/{policy_id}``
        service_perimeters (MutableSequence[google.cloud.accesscontextmanager_v1.types.ServicePerimeter]):
            Required. The desired [Service Perimeters]
            [google.identity.accesscontextmanager.v1.ServicePerimeter]
            that should replace all existing [Service Perimeters]
            [google.identity.accesscontextmanager.v1.ServicePerimeter]
            in the [Access Policy]
            [google.identity.accesscontextmanager.v1.AccessPolicy].
        etag (str):
            Optional. The etag for the version of the [Access Policy]
            [google.identity.accesscontextmanager.v1.AccessPolicy] that
            this replace operation is to be performed on. If, at the
            time of replace, the etag for the Access Policy stored in
            Access Context Manager is different from the specified etag,
            then the replace operation will not be performed and the
            call will fail. This field is not required. If etag is not
            provided, the operation will be performed as if a valid etag
            is provided.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    service_perimeters: MutableSequence[
        gia_service_perimeter.ServicePerimeter
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message=gia_service_perimeter.ServicePerimeter,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ReplaceServicePerimetersResponse(proto.Message):
    r"""A response to ReplaceServicePerimetersRequest. This will be
    put inside of Operation.response field.

    Attributes:
        service_perimeters (MutableSequence[google.cloud.accesscontextmanager_v1.types.ServicePerimeter]):
            List of the [Service Perimeter]
            [google.identity.accesscontextmanager.v1.ServicePerimeter]
            instances.
    """

    service_perimeters: MutableSequence[
        gia_service_perimeter.ServicePerimeter
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=gia_service_perimeter.ServicePerimeter,
    )


class CommitServicePerimetersRequest(proto.Message):
    r"""A request to commit dry-run specs in all [Service Perimeters]
    [google.identity.accesscontextmanager.v1.ServicePerimeter] belonging
    to an [Access
    Policy][google.identity.accesscontextmanager.v1.AccessPolicy].

    Attributes:
        parent (str):
            Required. Resource name for the parent [Access Policy]
            [google.identity.accesscontextmanager.v1.AccessPolicy] which
            owns all [Service Perimeters]
            [google.identity.accesscontextmanager.v1.ServicePerimeter]
            in scope for the commit operation.

            Format: ``accessPolicies/{policy_id}``
        etag (str):
            Optional. The etag for the version of the [Access Policy]
            [google.identity.accesscontextmanager.v1.AccessPolicy] that
            this commit operation is to be performed on. If, at the time
            of commit, the etag for the Access Policy stored in Access
            Context Manager is different from the specified etag, then
            the commit operation will not be performed and the call will
            fail. This field is not required. If etag is not provided,
            the operation will be performed as if a valid etag is
            provided.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    etag: str = proto.Field(
        proto.STRING,
        number=2,
    )


class CommitServicePerimetersResponse(proto.Message):
    r"""A response to CommitServicePerimetersRequest. This will be
    put inside of Operation.response field.

    Attributes:
        service_perimeters (MutableSequence[google.cloud.accesscontextmanager_v1.types.ServicePerimeter]):
            List of all the [Service Perimeter]
            [google.identity.accesscontextmanager.v1.ServicePerimeter]
            instances in the [Access Policy]
            [google.identity.accesscontextmanager.v1.AccessPolicy].
    """

    service_perimeters: MutableSequence[
        gia_service_perimeter.ServicePerimeter
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=gia_service_perimeter.ServicePerimeter,
    )


class ListGcpUserAccessBindingsRequest(proto.Message):
    r"""Request of [ListGcpUserAccessBindings]
    [google.identity.accesscontextmanager.v1.AccessContextManager.ListGcpUserAccessBindings].

    Attributes:
        parent (str):
            Required. Example: "organizations/256".
        page_size (int):
            Optional. Maximum number of items to return.
            The server may return fewer items. If left
            blank, the server may return any number of
            items.
        page_token (str):
            Optional. If left blank, returns the first page. To
            enumerate all items, use the [next_page_token]
            [google.identity.accesscontextmanager.v1.ListGcpUserAccessBindingsResponse.next_page_token]
            from your previous list operation.
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


class ListGcpUserAccessBindingsResponse(proto.Message):
    r"""Response of [ListGcpUserAccessBindings]
    [google.identity.accesscontextmanager.v1.AccessContextManager.ListGcpUserAccessBindings].

    Attributes:
        gcp_user_access_bindings (MutableSequence[google.cloud.accesscontextmanager_v1.types.GcpUserAccessBinding]):
            [GcpUserAccessBinding]
            [google.identity.accesscontextmanager.v1.GcpUserAccessBinding]
        next_page_token (str):
            Token to get the next page of items. If
            blank, there are no more items.
    """

    @property
    def raw_page(self):
        return self

    gcp_user_access_bindings: MutableSequence[
        gia_gcp_user_access_binding.GcpUserAccessBinding
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=gia_gcp_user_access_binding.GcpUserAccessBinding,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetGcpUserAccessBindingRequest(proto.Message):
    r"""Request of [GetGcpUserAccessBinding]
    [google.identity.accesscontextmanager.v1.AccessContextManager.GetGcpUserAccessBinding].

    Attributes:
        name (str):
            Required. Example:
            "organizations/256/gcpUserAccessBindings/b3-BhcX_Ud5N".
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateGcpUserAccessBindingRequest(proto.Message):
    r"""Request of [CreateGcpUserAccessBinding]
    [google.identity.accesscontextmanager.v1.AccessContextManager.CreateGcpUserAccessBinding].

    Attributes:
        parent (str):
            Required. Example: "organizations/256".
        gcp_user_access_binding (google.cloud.accesscontextmanager_v1.types.GcpUserAccessBinding):
            Required. [GcpUserAccessBinding]
            [google.identity.accesscontextmanager.v1.GcpUserAccessBinding]
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    gcp_user_access_binding: gia_gcp_user_access_binding.GcpUserAccessBinding = (
        proto.Field(
            proto.MESSAGE,
            number=2,
            message=gia_gcp_user_access_binding.GcpUserAccessBinding,
        )
    )


class UpdateGcpUserAccessBindingRequest(proto.Message):
    r"""Request of [UpdateGcpUserAccessBinding]
    [google.identity.accesscontextmanager.v1.AccessContextManager.UpdateGcpUserAccessBinding].

    Attributes:
        gcp_user_access_binding (google.cloud.accesscontextmanager_v1.types.GcpUserAccessBinding):
            Required. [GcpUserAccessBinding]
            [google.identity.accesscontextmanager.v1.GcpUserAccessBinding]
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Only the fields specified in this mask are
            updated. Because name and group_key cannot be changed,
            update_mask is required and must always be:

            update_mask { paths: "access_levels" }
    """

    gcp_user_access_binding: gia_gcp_user_access_binding.GcpUserAccessBinding = (
        proto.Field(
            proto.MESSAGE,
            number=1,
            message=gia_gcp_user_access_binding.GcpUserAccessBinding,
        )
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class DeleteGcpUserAccessBindingRequest(proto.Message):
    r"""Request of [DeleteGcpUserAccessBinding]
    [google.identity.accesscontextmanager.v1.AccessContextManager.DeleteGcpUserAccessBinding].

    Attributes:
        name (str):
            Required. Example:
            "organizations/256/gcpUserAccessBindings/b3-BhcX_Ud5N".
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class GcpUserAccessBindingOperationMetadata(proto.Message):
    r"""Currently, a completed operation means nothing. In the
    future, this metadata and a completed operation may indicate
    that the binding has taken effect and is affecting access
    decisions for all users.

    """


class AccessContextManagerOperationMetadata(proto.Message):
    r"""Metadata of Access Context Manager's Long Running Operations."""


__all__ = tuple(sorted(__protobuf__.manifest))
