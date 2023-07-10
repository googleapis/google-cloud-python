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

from google.protobuf import field_mask_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.apigee_registry_v1.types import registry_models

__protobuf__ = proto.module(
    package="google.cloud.apigeeregistry.v1",
    manifest={
        "ListApisRequest",
        "ListApisResponse",
        "GetApiRequest",
        "CreateApiRequest",
        "UpdateApiRequest",
        "DeleteApiRequest",
        "ListApiVersionsRequest",
        "ListApiVersionsResponse",
        "GetApiVersionRequest",
        "CreateApiVersionRequest",
        "UpdateApiVersionRequest",
        "DeleteApiVersionRequest",
        "ListApiSpecsRequest",
        "ListApiSpecsResponse",
        "GetApiSpecRequest",
        "GetApiSpecContentsRequest",
        "CreateApiSpecRequest",
        "UpdateApiSpecRequest",
        "DeleteApiSpecRequest",
        "TagApiSpecRevisionRequest",
        "ListApiSpecRevisionsRequest",
        "ListApiSpecRevisionsResponse",
        "RollbackApiSpecRequest",
        "DeleteApiSpecRevisionRequest",
        "ListApiDeploymentsRequest",
        "ListApiDeploymentsResponse",
        "GetApiDeploymentRequest",
        "CreateApiDeploymentRequest",
        "UpdateApiDeploymentRequest",
        "DeleteApiDeploymentRequest",
        "TagApiDeploymentRevisionRequest",
        "ListApiDeploymentRevisionsRequest",
        "ListApiDeploymentRevisionsResponse",
        "RollbackApiDeploymentRequest",
        "DeleteApiDeploymentRevisionRequest",
        "ListArtifactsRequest",
        "ListArtifactsResponse",
        "GetArtifactRequest",
        "GetArtifactContentsRequest",
        "CreateArtifactRequest",
        "ReplaceArtifactRequest",
        "DeleteArtifactRequest",
    },
)


class ListApisRequest(proto.Message):
    r"""Request message for ListApis.

    Attributes:
        parent (str):
            Required. The parent, which owns this collection of APIs.
            Format: ``projects/*/locations/*``
        page_size (int):
            The maximum number of APIs to return.
            The service may return fewer than this value. If
            unspecified, at most 50 values will be returned.
            The maximum is 1000; values above 1000 will be
            coerced to 1000.
        page_token (str):
            A page token, received from a previous ``ListApis`` call.
            Provide this to retrieve the subsequent page.

            When paginating, all other parameters provided to
            ``ListApis`` must match the call that provided the page
            token.
        filter (str):
            An expression that can be used to filter the
            list. Filters use the Common Expression Language
            and can refer to all message fields.
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
    filter: str = proto.Field(
        proto.STRING,
        number=4,
    )


class ListApisResponse(proto.Message):
    r"""Response message for ListApis.

    Attributes:
        apis (MutableSequence[google.cloud.apigee_registry_v1.types.Api]):
            The APIs from the specified publisher.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    apis: MutableSequence[registry_models.Api] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=registry_models.Api,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetApiRequest(proto.Message):
    r"""Request message for GetApi.

    Attributes:
        name (str):
            Required. The name of the API to retrieve. Format:
            ``projects/*/locations/*/apis/*``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateApiRequest(proto.Message):
    r"""Request message for CreateApi.

    Attributes:
        parent (str):
            Required. The parent, which owns this collection of APIs.
            Format: ``projects/*/locations/*``
        api (google.cloud.apigee_registry_v1.types.Api):
            Required. The API to create.
        api_id (str):
            Required. The ID to use for the API, which will become the
            final component of the API's resource name.

            This value should be 4-63 characters, and valid characters
            are /[a-z][0-9]-/.

            Following AIP-162, IDs must not have the form of a UUID.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    api: registry_models.Api = proto.Field(
        proto.MESSAGE,
        number=2,
        message=registry_models.Api,
    )
    api_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class UpdateApiRequest(proto.Message):
    r"""Request message for UpdateApi.

    Attributes:
        api (google.cloud.apigee_registry_v1.types.Api):
            Required. The API to update.

            The ``name`` field is used to identify the API to update.
            Format: ``projects/*/locations/*/apis/*``
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            The list of fields to be updated. If omitted, all fields are
            updated that are set in the request message (fields set to
            default values are ignored). If an asterisk "*" is
            specified, all fields are updated, including fields that are
            unspecified/default in the request.
        allow_missing (bool):
            If set to true, and the API is not found, a new API will be
            created. In this situation, ``update_mask`` is ignored.
    """

    api: registry_models.Api = proto.Field(
        proto.MESSAGE,
        number=1,
        message=registry_models.Api,
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )
    allow_missing: bool = proto.Field(
        proto.BOOL,
        number=3,
    )


class DeleteApiRequest(proto.Message):
    r"""Request message for DeleteApi.

    Attributes:
        name (str):
            Required. The name of the API to delete. Format:
            ``projects/*/locations/*/apis/*``
        force (bool):
            If set to true, any child resources will also
            be deleted. (Otherwise, the request will only
            work if there are no child resources.)
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    force: bool = proto.Field(
        proto.BOOL,
        number=2,
    )


class ListApiVersionsRequest(proto.Message):
    r"""Request message for ListApiVersions.

    Attributes:
        parent (str):
            Required. The parent, which owns this collection of
            versions. Format: ``projects/*/locations/*/apis/*``
        page_size (int):
            The maximum number of versions to return.
            The service may return fewer than this value. If
            unspecified, at most 50 values will be returned.
            The maximum is 1000; values above 1000 will be
            coerced to 1000.
        page_token (str):
            A page token, received from a previous ``ListApiVersions``
            call. Provide this to retrieve the subsequent page.

            When paginating, all other parameters provided to
            ``ListApiVersions`` must match the call that provided the
            page token.
        filter (str):
            An expression that can be used to filter the
            list. Filters use the Common Expression Language
            and can refer to all message fields.
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
    filter: str = proto.Field(
        proto.STRING,
        number=4,
    )


class ListApiVersionsResponse(proto.Message):
    r"""Response message for ListApiVersions.

    Attributes:
        api_versions (MutableSequence[google.cloud.apigee_registry_v1.types.ApiVersion]):
            The versions from the specified publisher.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    api_versions: MutableSequence[registry_models.ApiVersion] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=registry_models.ApiVersion,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetApiVersionRequest(proto.Message):
    r"""Request message for GetApiVersion.

    Attributes:
        name (str):
            Required. The name of the version to retrieve. Format:
            ``projects/*/locations/*/apis/*/versions/*``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateApiVersionRequest(proto.Message):
    r"""Request message for CreateApiVersion.

    Attributes:
        parent (str):
            Required. The parent, which owns this collection of
            versions. Format: ``projects/*/locations/*/apis/*``
        api_version (google.cloud.apigee_registry_v1.types.ApiVersion):
            Required. The version to create.
        api_version_id (str):
            Required. The ID to use for the version, which will become
            the final component of the version's resource name.

            This value should be 1-63 characters, and valid characters
            are /[a-z][0-9]-/.

            Following AIP-162, IDs must not have the form of a UUID.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    api_version: registry_models.ApiVersion = proto.Field(
        proto.MESSAGE,
        number=2,
        message=registry_models.ApiVersion,
    )
    api_version_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class UpdateApiVersionRequest(proto.Message):
    r"""Request message for UpdateApiVersion.

    Attributes:
        api_version (google.cloud.apigee_registry_v1.types.ApiVersion):
            Required. The version to update.

            The ``name`` field is used to identify the version to
            update. Format: ``projects/*/locations/*/apis/*/versions/*``
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            The list of fields to be updated. If omitted, all fields are
            updated that are set in the request message (fields set to
            default values are ignored). If an asterisk "*" is
            specified, all fields are updated, including fields that are
            unspecified/default in the request.
        allow_missing (bool):
            If set to true, and the version is not found, a new version
            will be created. In this situation, ``update_mask`` is
            ignored.
    """

    api_version: registry_models.ApiVersion = proto.Field(
        proto.MESSAGE,
        number=1,
        message=registry_models.ApiVersion,
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )
    allow_missing: bool = proto.Field(
        proto.BOOL,
        number=3,
    )


class DeleteApiVersionRequest(proto.Message):
    r"""Request message for DeleteApiVersion.

    Attributes:
        name (str):
            Required. The name of the version to delete. Format:
            ``projects/*/locations/*/apis/*/versions/*``
        force (bool):
            If set to true, any child resources will also
            be deleted. (Otherwise, the request will only
            work if there are no child resources.)
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    force: bool = proto.Field(
        proto.BOOL,
        number=2,
    )


class ListApiSpecsRequest(proto.Message):
    r"""Request message for ListApiSpecs.

    Attributes:
        parent (str):
            Required. The parent, which owns this collection of specs.
            Format: ``projects/*/locations/*/apis/*/versions/*``
        page_size (int):
            The maximum number of specs to return.
            The service may return fewer than this value. If
            unspecified, at most 50 values will be returned.
            The maximum is 1000; values above 1000 will be
            coerced to 1000.
        page_token (str):
            A page token, received from a previous ``ListApiSpecs``
            call. Provide this to retrieve the subsequent page.

            When paginating, all other parameters provided to
            ``ListApiSpecs`` must match the call that provided the page
            token.
        filter (str):
            An expression that can be used to filter the
            list. Filters use the Common Expression Language
            and can refer to all message fields except
            contents.
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
    filter: str = proto.Field(
        proto.STRING,
        number=4,
    )


class ListApiSpecsResponse(proto.Message):
    r"""Response message for ListApiSpecs.

    Attributes:
        api_specs (MutableSequence[google.cloud.apigee_registry_v1.types.ApiSpec]):
            The specs from the specified publisher.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    api_specs: MutableSequence[registry_models.ApiSpec] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=registry_models.ApiSpec,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetApiSpecRequest(proto.Message):
    r"""Request message for GetApiSpec.

    Attributes:
        name (str):
            Required. The name of the spec to retrieve. Format:
            ``projects/*/locations/*/apis/*/versions/*/specs/*``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class GetApiSpecContentsRequest(proto.Message):
    r"""Request message for GetApiSpecContents.

    Attributes:
        name (str):
            Required. The name of the spec whose contents should be
            retrieved. Format:
            ``projects/*/locations/*/apis/*/versions/*/specs/*``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateApiSpecRequest(proto.Message):
    r"""Request message for CreateApiSpec.

    Attributes:
        parent (str):
            Required. The parent, which owns this collection of specs.
            Format: ``projects/*/locations/*/apis/*/versions/*``
        api_spec (google.cloud.apigee_registry_v1.types.ApiSpec):
            Required. The spec to create.
        api_spec_id (str):
            Required. The ID to use for the spec, which will become the
            final component of the spec's resource name.

            This value should be 4-63 characters, and valid characters
            are /[a-z][0-9]-/.

            Following AIP-162, IDs must not have the form of a UUID.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    api_spec: registry_models.ApiSpec = proto.Field(
        proto.MESSAGE,
        number=2,
        message=registry_models.ApiSpec,
    )
    api_spec_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class UpdateApiSpecRequest(proto.Message):
    r"""Request message for UpdateApiSpec.

    Attributes:
        api_spec (google.cloud.apigee_registry_v1.types.ApiSpec):
            Required. The spec to update.

            The ``name`` field is used to identify the spec to update.
            Format: ``projects/*/locations/*/apis/*/versions/*/specs/*``
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            The list of fields to be updated. If omitted, all fields are
            updated that are set in the request message (fields set to
            default values are ignored). If an asterisk "*" is
            specified, all fields are updated, including fields that are
            unspecified/default in the request.
        allow_missing (bool):
            If set to true, and the spec is not found, a new spec will
            be created. In this situation, ``update_mask`` is ignored.
    """

    api_spec: registry_models.ApiSpec = proto.Field(
        proto.MESSAGE,
        number=1,
        message=registry_models.ApiSpec,
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )
    allow_missing: bool = proto.Field(
        proto.BOOL,
        number=3,
    )


class DeleteApiSpecRequest(proto.Message):
    r"""Request message for DeleteApiSpec.

    Attributes:
        name (str):
            Required. The name of the spec to delete. Format:
            ``projects/*/locations/*/apis/*/versions/*/specs/*``
        force (bool):
            If set to true, any child resources will also
            be deleted. (Otherwise, the request will only
            work if there are no child resources.)
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    force: bool = proto.Field(
        proto.BOOL,
        number=2,
    )


class TagApiSpecRevisionRequest(proto.Message):
    r"""Request message for TagApiSpecRevision.

    Attributes:
        name (str):
            Required. The name of the spec to be tagged,
            including the revision ID.
        tag (str):
            Required. The tag to apply. The tag should be at most 40
            characters, and match ``[a-z][a-z0-9-]{3,39}``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    tag: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ListApiSpecRevisionsRequest(proto.Message):
    r"""Request message for ListApiSpecRevisions.

    Attributes:
        name (str):
            Required. The name of the spec to list
            revisions for.
        page_size (int):
            The maximum number of revisions to return per
            page.
        page_token (str):
            The page token, received from a previous
            ListApiSpecRevisions call. Provide this to
            retrieve the subsequent page.
    """

    name: str = proto.Field(
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


class ListApiSpecRevisionsResponse(proto.Message):
    r"""Response message for ListApiSpecRevisionsResponse.

    Attributes:
        api_specs (MutableSequence[google.cloud.apigee_registry_v1.types.ApiSpec]):
            The revisions of the spec.
        next_page_token (str):
            A token that can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    api_specs: MutableSequence[registry_models.ApiSpec] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=registry_models.ApiSpec,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class RollbackApiSpecRequest(proto.Message):
    r"""Request message for RollbackApiSpec.

    Attributes:
        name (str):
            Required. The spec being rolled back.
        revision_id (str):
            Required. The revision ID to roll back to. It must be a
            revision of the same spec.

            Example: ``c7cfa2a8``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    revision_id: str = proto.Field(
        proto.STRING,
        number=2,
    )


class DeleteApiSpecRevisionRequest(proto.Message):
    r"""Request message for DeleteApiSpecRevision.

    Attributes:
        name (str):
            Required. The name of the spec revision to be deleted, with
            a revision ID explicitly included.

            Example:
            ``projects/sample/locations/global/apis/petstore/versions/1.0.0/specs/openapi.yaml@c7cfa2a8``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListApiDeploymentsRequest(proto.Message):
    r"""Request message for ListApiDeployments.

    Attributes:
        parent (str):
            Required. The parent, which owns this collection of
            deployments. Format: ``projects/*/locations/*/apis/*``
        page_size (int):
            The maximum number of deployments to return.
            The service may return fewer than this value. If
            unspecified, at most 50 values will be returned.
            The maximum is 1000; values above 1000 will be
            coerced to 1000.
        page_token (str):
            A page token, received from a previous
            ``ListApiDeployments`` call. Provide this to retrieve the
            subsequent page.

            When paginating, all other parameters provided to
            ``ListApiDeployments`` must match the call that provided the
            page token.
        filter (str):
            An expression that can be used to filter the
            list. Filters use the Common Expression Language
            and can refer to all message fields.
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
    filter: str = proto.Field(
        proto.STRING,
        number=4,
    )


class ListApiDeploymentsResponse(proto.Message):
    r"""Response message for ListApiDeployments.

    Attributes:
        api_deployments (MutableSequence[google.cloud.apigee_registry_v1.types.ApiDeployment]):
            The deployments from the specified publisher.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    api_deployments: MutableSequence[
        registry_models.ApiDeployment
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=registry_models.ApiDeployment,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetApiDeploymentRequest(proto.Message):
    r"""Request message for GetApiDeployment.

    Attributes:
        name (str):
            Required. The name of the deployment to retrieve. Format:
            ``projects/*/locations/*/apis/*/deployments/*``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateApiDeploymentRequest(proto.Message):
    r"""Request message for CreateApiDeployment.

    Attributes:
        parent (str):
            Required. The parent, which owns this collection of
            deployments. Format: ``projects/*/locations/*/apis/*``
        api_deployment (google.cloud.apigee_registry_v1.types.ApiDeployment):
            Required. The deployment to create.
        api_deployment_id (str):
            Required. The ID to use for the deployment, which will
            become the final component of the deployment's resource
            name.

            This value should be 4-63 characters, and valid characters
            are /[a-z][0-9]-/.

            Following AIP-162, IDs must not have the form of a UUID.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    api_deployment: registry_models.ApiDeployment = proto.Field(
        proto.MESSAGE,
        number=2,
        message=registry_models.ApiDeployment,
    )
    api_deployment_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class UpdateApiDeploymentRequest(proto.Message):
    r"""Request message for UpdateApiDeployment.

    Attributes:
        api_deployment (google.cloud.apigee_registry_v1.types.ApiDeployment):
            Required. The deployment to update.

            The ``name`` field is used to identify the deployment to
            update. Format:
            ``projects/*/locations/*/apis/*/deployments/*``
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            The list of fields to be updated. If omitted, all fields are
            updated that are set in the request message (fields set to
            default values are ignored). If an asterisk "*" is
            specified, all fields are updated, including fields that are
            unspecified/default in the request.
        allow_missing (bool):
            If set to true, and the deployment is not found, a new
            deployment will be created. In this situation,
            ``update_mask`` is ignored.
    """

    api_deployment: registry_models.ApiDeployment = proto.Field(
        proto.MESSAGE,
        number=1,
        message=registry_models.ApiDeployment,
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )
    allow_missing: bool = proto.Field(
        proto.BOOL,
        number=3,
    )


class DeleteApiDeploymentRequest(proto.Message):
    r"""Request message for DeleteApiDeployment.

    Attributes:
        name (str):
            Required. The name of the deployment to delete. Format:
            ``projects/*/locations/*/apis/*/deployments/*``
        force (bool):
            If set to true, any child resources will also
            be deleted. (Otherwise, the request will only
            work if there are no child resources.)
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    force: bool = proto.Field(
        proto.BOOL,
        number=2,
    )


class TagApiDeploymentRevisionRequest(proto.Message):
    r"""Request message for TagApiDeploymentRevision.

    Attributes:
        name (str):
            Required. The name of the deployment to be
            tagged, including the revision ID.
        tag (str):
            Required. The tag to apply. The tag should be at most 40
            characters, and match ``[a-z][a-z0-9-]{3,39}``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    tag: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ListApiDeploymentRevisionsRequest(proto.Message):
    r"""Request message for ListApiDeploymentRevisions.

    Attributes:
        name (str):
            Required. The name of the deployment to list
            revisions for.
        page_size (int):
            The maximum number of revisions to return per
            page.
        page_token (str):
            The page token, received from a previous
            ListApiDeploymentRevisions call. Provide this to
            retrieve the subsequent page.
    """

    name: str = proto.Field(
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


class ListApiDeploymentRevisionsResponse(proto.Message):
    r"""Response message for ListApiDeploymentRevisionsResponse.

    Attributes:
        api_deployments (MutableSequence[google.cloud.apigee_registry_v1.types.ApiDeployment]):
            The revisions of the deployment.
        next_page_token (str):
            A token that can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    api_deployments: MutableSequence[
        registry_models.ApiDeployment
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=registry_models.ApiDeployment,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class RollbackApiDeploymentRequest(proto.Message):
    r"""Request message for RollbackApiDeployment.

    Attributes:
        name (str):
            Required. The deployment being rolled back.
        revision_id (str):
            Required. The revision ID to roll back to. It must be a
            revision of the same deployment.

            Example: ``c7cfa2a8``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    revision_id: str = proto.Field(
        proto.STRING,
        number=2,
    )


class DeleteApiDeploymentRevisionRequest(proto.Message):
    r"""Request message for DeleteApiDeploymentRevision.

    Attributes:
        name (str):
            Required. The name of the deployment revision to be deleted,
            with a revision ID explicitly included.

            Example:
            ``projects/sample/locations/global/apis/petstore/deployments/prod@c7cfa2a8``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListArtifactsRequest(proto.Message):
    r"""Request message for ListArtifacts.

    Attributes:
        parent (str):
            Required. The parent, which owns this collection of
            artifacts. Format: ``{parent}``
        page_size (int):
            The maximum number of artifacts to return.
            The service may return fewer than this value. If
            unspecified, at most 50 values will be returned.
            The maximum is 1000; values above 1000 will be
            coerced to 1000.
        page_token (str):
            A page token, received from a previous ``ListArtifacts``
            call. Provide this to retrieve the subsequent page.

            When paginating, all other parameters provided to
            ``ListArtifacts`` must match the call that provided the page
            token.
        filter (str):
            An expression that can be used to filter the
            list. Filters use the Common Expression Language
            and can refer to all message fields except
            contents.
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
    filter: str = proto.Field(
        proto.STRING,
        number=4,
    )


class ListArtifactsResponse(proto.Message):
    r"""Response message for ListArtifacts.

    Attributes:
        artifacts (MutableSequence[google.cloud.apigee_registry_v1.types.Artifact]):
            The artifacts from the specified publisher.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    artifacts: MutableSequence[registry_models.Artifact] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=registry_models.Artifact,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetArtifactRequest(proto.Message):
    r"""Request message for GetArtifact.

    Attributes:
        name (str):
            Required. The name of the artifact to retrieve. Format:
            ``{parent}/artifacts/*``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class GetArtifactContentsRequest(proto.Message):
    r"""Request message for GetArtifactContents.

    Attributes:
        name (str):
            Required. The name of the artifact whose contents should be
            retrieved. Format: ``{parent}/artifacts/*``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateArtifactRequest(proto.Message):
    r"""Request message for CreateArtifact.

    Attributes:
        parent (str):
            Required. The parent, which owns this collection of
            artifacts. Format: ``{parent}``
        artifact (google.cloud.apigee_registry_v1.types.Artifact):
            Required. The artifact to create.
        artifact_id (str):
            Required. The ID to use for the artifact, which will become
            the final component of the artifact's resource name.

            This value should be 4-63 characters, and valid characters
            are /[a-z][0-9]-/.

            Following AIP-162, IDs must not have the form of a UUID.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    artifact: registry_models.Artifact = proto.Field(
        proto.MESSAGE,
        number=2,
        message=registry_models.Artifact,
    )
    artifact_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ReplaceArtifactRequest(proto.Message):
    r"""Request message for ReplaceArtifact.

    Attributes:
        artifact (google.cloud.apigee_registry_v1.types.Artifact):
            Required. The artifact to replace.

            The ``name`` field is used to identify the artifact to
            replace. Format: ``{parent}/artifacts/*``
    """

    artifact: registry_models.Artifact = proto.Field(
        proto.MESSAGE,
        number=1,
        message=registry_models.Artifact,
    )


class DeleteArtifactRequest(proto.Message):
    r"""Request message for DeleteArtifact.

    Attributes:
        name (str):
            Required. The name of the artifact to delete. Format:
            ``{parent}/artifacts/*``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
