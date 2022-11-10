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
from google.apps.script.type import script_manifest_pb2  # type: ignore
from google.apps.script.type.calendar import calendar_addon_manifest_pb2  # type: ignore
from google.apps.script.type.docs import docs_addon_manifest_pb2  # type: ignore
from google.apps.script.type.drive import drive_addon_manifest_pb2  # type: ignore
from google.apps.script.type.gmail import gmail_addon_manifest_pb2  # type: ignore
from google.apps.script.type.sheets import sheets_addon_manifest_pb2  # type: ignore
from google.apps.script.type.slides import slides_addon_manifest_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.gsuiteaddons.v1",
    manifest={
        "GetAuthorizationRequest",
        "Authorization",
        "CreateDeploymentRequest",
        "ReplaceDeploymentRequest",
        "GetDeploymentRequest",
        "ListDeploymentsRequest",
        "ListDeploymentsResponse",
        "DeleteDeploymentRequest",
        "InstallDeploymentRequest",
        "UninstallDeploymentRequest",
        "GetInstallStatusRequest",
        "InstallStatus",
        "Deployment",
        "AddOns",
    },
)


class GetAuthorizationRequest(proto.Message):
    r"""Request message to get Google Workspace Add-ons authorization
    information.

    Attributes:
        name (str):
            Required. Name of the project for which to get the Google
            Workspace Add-ons authorization information.

            Example: ``projects/my_project/authorization``.
    """

    name = proto.Field(
        proto.STRING,
        number=2,
    )


class Authorization(proto.Message):
    r"""The authorization information used when invoking deployment
    endpoints.

    Attributes:
        name (str):
            The canonical full name of this resource. Example:
            ``projects/123/authorization``
        service_account_email (str):
            The email address of the service account used
            to authenticate requests to add-on callback
            endpoints.
        oauth_client_id (str):
            The OAuth client ID used to obtain OAuth
            access tokens for a user on the add-on's behalf.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    service_account_email = proto.Field(
        proto.STRING,
        number=2,
    )
    oauth_client_id = proto.Field(
        proto.STRING,
        number=3,
    )


class CreateDeploymentRequest(proto.Message):
    r"""Request message to create a deployment.

    Attributes:
        parent (str):
            Required. Name of the project in which to create the
            deployment.

            Example: ``projects/my_project``.
        deployment_id (str):
            Required. The id to use for this deployment. The full name
            of the created resource will be
            ``projects/<project_number>/deployments/<deployment_id>``.
        deployment (google.cloud.gsuiteaddons_v1.types.Deployment):
            Required. The deployment to create
            (deployment.name cannot be set).
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    deployment_id = proto.Field(
        proto.STRING,
        number=2,
    )
    deployment = proto.Field(
        proto.MESSAGE,
        number=3,
        message="Deployment",
    )


class ReplaceDeploymentRequest(proto.Message):
    r"""Request message to create or replace a deployment.

    Attributes:
        deployment (google.cloud.gsuiteaddons_v1.types.Deployment):
            Required. The deployment to create or
            replace.
    """

    deployment = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Deployment",
    )


class GetDeploymentRequest(proto.Message):
    r"""Request message to get a deployment.

    Attributes:
        name (str):
            Required. The full resource name of the deployment to get.

            Example: ``projects/my_project/deployments/my_deployment``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class ListDeploymentsRequest(proto.Message):
    r"""Request message to list deployments for a project.

    Attributes:
        parent (str):
            Required. Name of the project in which to create the
            deployment.

            Example: ``projects/my_project``.
        page_size (int):
            The maximum number of deployments to return.
            The service may return fewer than this value. If
            unspecified, at most 1000 deployments will be
            returned. The maximum value is 1000; values
            above 1000 will be coerced to 1000.
        page_token (str):
            A page token, received from a previous ``ListDeployments``
            call. Provide this to retrieve the subsequent page.

            When paginating, all other parameters provided to
            ``ListDeployments`` must match the call that provided the
            page token.
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


class ListDeploymentsResponse(proto.Message):
    r"""Response message to list deployments.

    Attributes:
        deployments (Sequence[google.cloud.gsuiteaddons_v1.types.Deployment]):
            The list of deployments for the given
            project.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    deployments = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Deployment",
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )


class DeleteDeploymentRequest(proto.Message):
    r"""Request message to delete a deployment.

    Attributes:
        name (str):
            Required. The full resource name of the deployment to
            delete.

            Example: ``projects/my_project/deployments/my_deployment``.
        etag (str):
            The etag of the deployment to delete.
            If this is provided, it must match the server's
            etag.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    etag = proto.Field(
        proto.STRING,
        number=2,
    )


class InstallDeploymentRequest(proto.Message):
    r"""Request message to install a developer mode deployment.

    Attributes:
        name (str):
            Required. The full resource name of the deployment to
            install.

            Example: ``projects/my_project/deployments/my_deployment``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class UninstallDeploymentRequest(proto.Message):
    r"""Request message to uninstall a developer mode deployment.

    Attributes:
        name (str):
            Required. The full resource name of the deployment to
            install.

            Example: ``projects/my_project/deployments/my_deployment``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class GetInstallStatusRequest(proto.Message):
    r"""Request message to get the install status of a developer mode
    deployment.

    Attributes:
        name (str):
            Required. The full resource name of the deployment.

            Example:
            ``projects/my_project/deployments/my_deployment/installStatus``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class InstallStatus(proto.Message):
    r"""Developer mode install status of a deployment

    Attributes:
        name (str):
            The canonical full resource name of the deployment install
            status.

            Example:
            ``projects/123/deployments/my_deployment/installStatus``.
        installed (google.protobuf.wrappers_pb2.BoolValue):
            True if the deployment is installed for the
            user
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    installed = proto.Field(
        proto.MESSAGE,
        number=2,
        message=wrappers_pb2.BoolValue,
    )


class Deployment(proto.Message):
    r"""A Google Workspace Add-on deployment

    Attributes:
        name (str):
            The deployment resource name. Example:
            projects/123/deployments/my_deployment.
        oauth_scopes (Sequence[str]):
            The list of Google OAuth scopes for which to
            request consent from the end user before
            executing an add-on endpoint.
        add_ons (google.cloud.gsuiteaddons_v1.types.AddOns):
            The Google Workspace Add-on configuration.
        etag (str):
            This value is computed by the server based on
            the version of the deployment in storage, and
            may be sent on update and delete requests to
            ensure the client has an up-to-date value before
            proceeding.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    oauth_scopes = proto.RepeatedField(
        proto.STRING,
        number=2,
    )
    add_ons = proto.Field(
        proto.MESSAGE,
        number=3,
        message="AddOns",
    )
    etag = proto.Field(
        proto.STRING,
        number=5,
    )


class AddOns(proto.Message):
    r"""A Google Workspace Add-on configuration.

    Attributes:
        common (google.apps.script.type.script_manifest_pb2.CommonAddOnManifest):
            Configuration that is common across all
            Google Workspace Add-ons.
        gmail (google.apps.script.type.gmail.gmail_addon_manifest_pb2.GmailAddOnManifest):
            Gmail add-on configuration.
        drive (google.apps.script.type.drive.drive_addon_manifest_pb2.DriveAddOnManifest):
            Drive add-on configuration.
        calendar (google.apps.script.type.calendar.calendar_addon_manifest_pb2.CalendarAddOnManifest):
            Calendar add-on configuration.
        docs (google.apps.script.type.docs.docs_addon_manifest_pb2.DocsAddOnManifest):
            Docs add-on configuration.
        sheets (google.apps.script.type.sheets.sheets_addon_manifest_pb2.SheetsAddOnManifest):
            Sheets add-on configuration.
        slides (google.apps.script.type.slides.slides_addon_manifest_pb2.SlidesAddOnManifest):
            Slides add-on configuration.
        http_options (google.apps.script.type.script_manifest_pb2.HttpOptions):
            Options for sending requests to add-on HTTP
            endpoints
    """

    common = proto.Field(
        proto.MESSAGE,
        number=1,
        message=script_manifest_pb2.CommonAddOnManifest,
    )
    gmail = proto.Field(
        proto.MESSAGE,
        number=2,
        message=gmail_addon_manifest_pb2.GmailAddOnManifest,
    )
    drive = proto.Field(
        proto.MESSAGE,
        number=5,
        message=drive_addon_manifest_pb2.DriveAddOnManifest,
    )
    calendar = proto.Field(
        proto.MESSAGE,
        number=6,
        message=calendar_addon_manifest_pb2.CalendarAddOnManifest,
    )
    docs = proto.Field(
        proto.MESSAGE,
        number=7,
        message=docs_addon_manifest_pb2.DocsAddOnManifest,
    )
    sheets = proto.Field(
        proto.MESSAGE,
        number=8,
        message=sheets_addon_manifest_pb2.SheetsAddOnManifest,
    )
    slides = proto.Field(
        proto.MESSAGE,
        number=10,
        message=slides_addon_manifest_pb2.SlidesAddOnManifest,
    )
    http_options = proto.Field(
        proto.MESSAGE,
        number=15,
        message=script_manifest_pb2.HttpOptions,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
