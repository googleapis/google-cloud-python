# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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

from google.protobuf import field_mask_pb2  # type: ignore


__protobuf__ = proto.module(
    package='google.iam.v1beta',
    manifest={
        'WorkloadIdentityPool',
        'WorkloadIdentityPoolProvider',
        'ListWorkloadIdentityPoolsRequest',
        'ListWorkloadIdentityPoolsResponse',
        'GetWorkloadIdentityPoolRequest',
        'CreateWorkloadIdentityPoolRequest',
        'UpdateWorkloadIdentityPoolRequest',
        'DeleteWorkloadIdentityPoolRequest',
        'UndeleteWorkloadIdentityPoolRequest',
        'ListWorkloadIdentityPoolProvidersRequest',
        'ListWorkloadIdentityPoolProvidersResponse',
        'GetWorkloadIdentityPoolProviderRequest',
        'CreateWorkloadIdentityPoolProviderRequest',
        'UpdateWorkloadIdentityPoolProviderRequest',
        'DeleteWorkloadIdentityPoolProviderRequest',
        'UndeleteWorkloadIdentityPoolProviderRequest',
        'WorkloadIdentityPoolOperationMetadata',
        'WorkloadIdentityPoolProviderOperationMetadata',
    },
)


class WorkloadIdentityPool(proto.Message):
    r"""Represents a collection of external workload identities. You
    can define IAM policies to grant these identities access to
    Google Cloud resources.

    Attributes:
        name (str):
            Output only. The resource name of the pool.
        display_name (str):
            A display name for the pool. Cannot exceed 32
            characters.
        description (str):
            A description of the pool. Cannot exceed 256
            characters.
        state (google.iam_v1beta.types.WorkloadIdentityPool.State):
            Output only. The state of the pool.
        disabled (bool):
            Whether the pool is disabled. You cannot use
            a disabled pool to exchange tokens, or use
            existing tokens to access resources. If the pool
            is re-enabled, existing tokens grant access
            again.
    """
    class State(proto.Enum):
        r"""The current state of the pool.

        Values:
            STATE_UNSPECIFIED (0):
                State unspecified.
            ACTIVE (1):
                The pool is active, and may be used in Google
                Cloud policies.
            DELETED (2):
                The pool is soft-deleted. Soft-deleted pools are permanently
                deleted after approximately 30 days. You can restore a
                soft-deleted pool using
                [UndeleteWorkloadIdentityPool][google.iam.v1beta.WorkloadIdentityPools.UndeleteWorkloadIdentityPool].

                You cannot reuse the ID of a soft-deleted pool until it is
                permanently deleted.

                While a pool is deleted, you cannot use it to exchange
                tokens, or use existing tokens to access resources. If the
                pool is undeleted, existing tokens grant access again.
        """
        STATE_UNSPECIFIED = 0
        ACTIVE = 1
        DELETED = 2

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
    state: State = proto.Field(
        proto.ENUM,
        number=4,
        enum=State,
    )
    disabled: bool = proto.Field(
        proto.BOOL,
        number=5,
    )


class WorkloadIdentityPoolProvider(proto.Message):
    r"""A configuration for an external identity provider.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Output only. The resource name of the
            provider.
        display_name (str):
            A display name for the provider. Cannot
            exceed 32 characters.
        description (str):
            A description for the provider. Cannot exceed
            256 characters.
        state (google.iam_v1beta.types.WorkloadIdentityPoolProvider.State):
            Output only. The state of the provider.
        disabled (bool):
            Whether the provider is disabled. You cannot
            use a disabled provider to exchange tokens.
            However, existing tokens still grant access.
        attribute_mapping (MutableMapping[str, str]):
            Maps attributes from authentication credentials issued by an
            external identity provider to Google Cloud attributes, such
            as ``subject`` and ``segment``.

            Each key must be a string specifying the Google Cloud IAM
            attribute to map to.

            The following keys are supported:

            -  ``google.subject``: The principal IAM is authenticating.
               You can reference this value in IAM bindings. This is
               also the subject that appears in Cloud Logging logs.
               Cannot exceed 127 characters.

            -  ``google.groups``: Groups the external identity belongs
               to. You can grant groups access to resources using an IAM
               ``principalSet`` binding; access applies to all members
               of the group.

            You can also provide custom attributes by specifying
            ``attribute.{custom_attribute}``, where
            ``{custom_attribute}`` is the name of the custom attribute
            to be mapped. You can define a maximum of 50 custom
            attributes. The maximum length of a mapped attribute key is
            100 characters, and the key may only contain the characters
            [a-z0-9_].

            You can reference these attributes in IAM policies to define
            fine-grained access for a workload to Google Cloud
            resources. For example:

            -  ``google.subject``:
               ``principal://iam.googleapis.com/projects/{project}/locations/{location}/workloadIdentityPools/{pool}/subject/{value}``

            -  ``google.groups``:
               ``principalSet://iam.googleapis.com/projects/{project}/locations/{location}/workloadIdentityPools/{pool}/group/{value}``

            -  ``attribute.{custom_attribute}``:
               ``principalSet://iam.googleapis.com/projects/{project}/locations/{location}/workloadIdentityPools/{pool}/attribute.{custom_attribute}/{value}``

            Each value must be a [Common Expression Language]
            (https://opensource.google/projects/cel) function that maps
            an identity provider credential to the normalized attribute
            specified by the corresponding map key.

            You can use the ``assertion`` keyword in the expression to
            access a JSON representation of the authentication
            credential issued by the provider.

            The maximum length of an attribute mapping expression is
            2048 characters. When evaluated, the total size of all
            mapped attributes must not exceed 8KB.

            For AWS providers, the following rules apply:

            -  If no attribute mapping is defined, the following default
               mapping applies:

               ::

                  {
                    "google.subject":"assertion.arn",
                    "attribute.aws_role":
                        "assertion.arn.contains('assumed-role')"
                        " ? assertion.arn.extract('{account_arn}assumed-role/')"
                        "   + 'assumed-role/'"
                        "   + assertion.arn.extract('assumed-role/{role_name}/')"
                        " : assertion.arn",
                  }

            -  If any custom attribute mappings are defined, they must
               include a mapping to the ``google.subject`` attribute.

            For OIDC providers, the following rules apply:

            -  Custom attribute mappings must be defined, and must
               include a mapping to the ``google.subject`` attribute.
               For example, the following maps the ``sub`` claim of the
               incoming credential to the ``subject`` attribute on a
               Google token.

               ::

                  {"google.subject": "assertion.sub"}
        attribute_condition (str):
            `A Common Expression
            Language <https://opensource.google/projects/cel>`__
            expression, in plain text, to restrict what otherwise valid
            authentication credentials issued by the provider should not
            be accepted.

            The expression must output a boolean representing whether to
            allow the federation.

            The following keywords may be referenced in the expressions:

            -  ``assertion``: JSON representing the authentication
               credential issued by the provider.
            -  ``google``: The Google attributes mapped from the
               assertion in the ``attribute_mappings``.
            -  ``attribute``: The custom attributes mapped from the
               assertion in the ``attribute_mappings``.

            The maximum length of the attribute condition expression is
            4096 characters. If unspecified, all valid authentication
            credential are accepted.

            The following example shows how to only allow credentials
            with a mapped ``google.groups`` value of ``admins``:

            ::

               "'admins' in google.groups".
        aws (google.iam_v1beta.types.WorkloadIdentityPoolProvider.Aws):
            An Amazon Web Services identity provider.

            This field is a member of `oneof`_ ``provider_config``.
        oidc (google.iam_v1beta.types.WorkloadIdentityPoolProvider.Oidc):
            An OpenId Connect 1.0 identity provider.

            This field is a member of `oneof`_ ``provider_config``.
    """
    class State(proto.Enum):
        r"""The current state of the provider.

        Values:
            STATE_UNSPECIFIED (0):
                State unspecified.
            ACTIVE (1):
                The provider is active, and may be used to
                validate authentication credentials.
            DELETED (2):
                The provider is soft-deleted. Soft-deleted providers are
                permanently deleted after approximately 30 days. You can
                restore a soft-deleted provider using
                [UndeleteWorkloadIdentityPoolProvider][google.iam.v1beta.WorkloadIdentityPools.UndeleteWorkloadIdentityPoolProvider].

                You cannot reuse the ID of a soft-deleted provider until it
                is permanently deleted.
        """
        STATE_UNSPECIFIED = 0
        ACTIVE = 1
        DELETED = 2

    class Aws(proto.Message):
        r"""Represents an Amazon Web Services identity provider.

        Attributes:
            account_id (str):
                Required. The AWS account ID.
        """

        account_id: str = proto.Field(
            proto.STRING,
            number=1,
        )

    class Oidc(proto.Message):
        r"""Represents an OpenId Connect 1.0 identity provider.

        Attributes:
            issuer_uri (str):
                Required. The OIDC issuer URL.
            allowed_audiences (MutableSequence[str]):
                Acceptable values for the ``aud`` field (audience) in the
                OIDC token. Token exchange requests are rejected if the
                token audience does not match one of the configured values.
                Each audience may be at most 256 characters. A maximum of 10
                audiences may be configured.

                If this list is empty, the OIDC token audience must be equal
                to the full canonical resource name of the
                WorkloadIdentityPoolProvider, with or without the HTTPS
                prefix. For example:

                ::

                   //iam.googleapis.com/projects/<project-number>/locations/<location>/workloadIdentityPools/<pool-id>/providers/<provider-id>
                   https://iam.googleapis.com/projects/<project-number>/locations/<location>/workloadIdentityPools/<pool-id>/providers/<provider-id>
        """

        issuer_uri: str = proto.Field(
            proto.STRING,
            number=1,
        )
        allowed_audiences: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=2,
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
    state: State = proto.Field(
        proto.ENUM,
        number=4,
        enum=State,
    )
    disabled: bool = proto.Field(
        proto.BOOL,
        number=5,
    )
    attribute_mapping: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=6,
    )
    attribute_condition: str = proto.Field(
        proto.STRING,
        number=7,
    )
    aws: Aws = proto.Field(
        proto.MESSAGE,
        number=8,
        oneof='provider_config',
        message=Aws,
    )
    oidc: Oidc = proto.Field(
        proto.MESSAGE,
        number=9,
        oneof='provider_config',
        message=Oidc,
    )


class ListWorkloadIdentityPoolsRequest(proto.Message):
    r"""Request message for ListWorkloadIdentityPools.

    Attributes:
        parent (str):
            Required. The parent resource to list pools
            for.
        page_size (int):
            The maximum number of pools to return.
            If unspecified, at most 50 pools are returned.
            The maximum value is 1000; values above are 1000
            truncated to 1000.
        page_token (str):
            A page token, received from a previous
            ``ListWorkloadIdentityPools`` call. Provide this to retrieve
            the subsequent page.
        show_deleted (bool):
            Whether to return soft-deleted pools.
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
    show_deleted: bool = proto.Field(
        proto.BOOL,
        number=4,
    )


class ListWorkloadIdentityPoolsResponse(proto.Message):
    r"""Response message for ListWorkloadIdentityPools.

    Attributes:
        workload_identity_pools (MutableSequence[google.iam_v1beta.types.WorkloadIdentityPool]):
            A list of pools.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    workload_identity_pools: MutableSequence['WorkloadIdentityPool'] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message='WorkloadIdentityPool',
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetWorkloadIdentityPoolRequest(proto.Message):
    r"""Request message for GetWorkloadIdentityPool.

    Attributes:
        name (str):
            Required. The name of the pool to retrieve.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateWorkloadIdentityPoolRequest(proto.Message):
    r"""Request message for CreateWorkloadIdentityPool.

    Attributes:
        parent (str):
            Required. The parent resource to create the pool in. The
            only supported location is ``global``.
        workload_identity_pool (google.iam_v1beta.types.WorkloadIdentityPool):
            Required. The pool to create.
        workload_identity_pool_id (str):
            Required. The ID to use for the pool, which becomes the
            final component of the resource name. This value should be
            4-32 characters, and may contain the characters [a-z0-9-].
            The prefix ``gcp-`` is reserved for use by Google, and may
            not be specified.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    workload_identity_pool: 'WorkloadIdentityPool' = proto.Field(
        proto.MESSAGE,
        number=2,
        message='WorkloadIdentityPool',
    )
    workload_identity_pool_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class UpdateWorkloadIdentityPoolRequest(proto.Message):
    r"""Request message for UpdateWorkloadIdentityPool.

    Attributes:
        workload_identity_pool (google.iam_v1beta.types.WorkloadIdentityPool):
            Required. The pool to update. The ``name`` field is used to
            identify the pool.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. The list of fields update.
    """

    workload_identity_pool: 'WorkloadIdentityPool' = proto.Field(
        proto.MESSAGE,
        number=1,
        message='WorkloadIdentityPool',
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class DeleteWorkloadIdentityPoolRequest(proto.Message):
    r"""Request message for DeleteWorkloadIdentityPool.

    Attributes:
        name (str):
            Required. The name of the pool to delete.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class UndeleteWorkloadIdentityPoolRequest(proto.Message):
    r"""Request message for UndeleteWorkloadIdentityPool.

    Attributes:
        name (str):
            Required. The name of the pool to undelete.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListWorkloadIdentityPoolProvidersRequest(proto.Message):
    r"""Request message for ListWorkloadIdentityPoolProviders.

    Attributes:
        parent (str):
            Required. The pool to list providers for.
        page_size (int):
            The maximum number of providers to return.
            If unspecified, at most 50 providers are
            returned. The maximum value is 100; values above
            100 are truncated to 100.
        page_token (str):
            A page token, received from a previous
            ``ListWorkloadIdentityPoolProviders`` call. Provide this to
            retrieve the subsequent page.
        show_deleted (bool):
            Whether to return soft-deleted providers.
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
    show_deleted: bool = proto.Field(
        proto.BOOL,
        number=4,
    )


class ListWorkloadIdentityPoolProvidersResponse(proto.Message):
    r"""Response message for ListWorkloadIdentityPoolProviders.

    Attributes:
        workload_identity_pool_providers (MutableSequence[google.iam_v1beta.types.WorkloadIdentityPoolProvider]):
            A list of providers.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    workload_identity_pool_providers: MutableSequence['WorkloadIdentityPoolProvider'] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message='WorkloadIdentityPoolProvider',
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetWorkloadIdentityPoolProviderRequest(proto.Message):
    r"""Request message for GetWorkloadIdentityPoolProvider.

    Attributes:
        name (str):
            Required. The name of the provider to
            retrieve.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateWorkloadIdentityPoolProviderRequest(proto.Message):
    r"""Request message for CreateWorkloadIdentityPoolProvider.

    Attributes:
        parent (str):
            Required. The pool to create this provider
            in.
        workload_identity_pool_provider (google.iam_v1beta.types.WorkloadIdentityPoolProvider):
            Required. The provider to create.
        workload_identity_pool_provider_id (str):
            Required. The ID for the provider, which becomes the final
            component of the resource name. This value must be 4-32
            characters, and may contain the characters [a-z0-9-]. The
            prefix ``gcp-`` is reserved for use by Google, and may not
            be specified.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    workload_identity_pool_provider: 'WorkloadIdentityPoolProvider' = proto.Field(
        proto.MESSAGE,
        number=2,
        message='WorkloadIdentityPoolProvider',
    )
    workload_identity_pool_provider_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class UpdateWorkloadIdentityPoolProviderRequest(proto.Message):
    r"""Request message for UpdateWorkloadIdentityPoolProvider.

    Attributes:
        workload_identity_pool_provider (google.iam_v1beta.types.WorkloadIdentityPoolProvider):
            Required. The provider to update.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. The list of fields to update.
    """

    workload_identity_pool_provider: 'WorkloadIdentityPoolProvider' = proto.Field(
        proto.MESSAGE,
        number=1,
        message='WorkloadIdentityPoolProvider',
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class DeleteWorkloadIdentityPoolProviderRequest(proto.Message):
    r"""Request message for DeleteWorkloadIdentityPoolProvider.

    Attributes:
        name (str):
            Required. The name of the provider to delete.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class UndeleteWorkloadIdentityPoolProviderRequest(proto.Message):
    r"""Request message for UndeleteWorkloadIdentityPoolProvider.

    Attributes:
        name (str):
            Required. The name of the provider to
            undelete.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class WorkloadIdentityPoolOperationMetadata(proto.Message):
    r"""Metadata for long-running WorkloadIdentityPool operations.
    """


class WorkloadIdentityPoolProviderOperationMetadata(proto.Message):
    r"""Metadata for long-running WorkloadIdentityPoolProvider
    operations.

    """


__all__ = tuple(sorted(__protobuf__.manifest))
