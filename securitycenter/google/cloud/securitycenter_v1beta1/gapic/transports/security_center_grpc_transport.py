# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import google.api_core.grpc_helpers
import google.api_core.operations_v1

from google.cloud.securitycenter_v1beta1.proto import securitycenter_service_pb2_grpc


class SecurityCenterGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.cloud.securitycenter.v1beta1 SecurityCenter API.

    The transport provides access to the raw gRPC stubs,
    which can be used to take advantage of advanced
    features of gRPC.
    """

    # The scopes needed to make gRPC calls to all of the methods defined
    # in this service.
    _OAUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    def __init__(
        self,
        channel=None,
        credentials=None,
        address="securitycenter.googleapis.com:443",
    ):
        """Instantiate the transport class.

        Args:
            channel (grpc.Channel): A ``Channel`` instance through
                which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            address (str): The address where the service is hosted.
        """
        # If both `channel` and `credentials` are specified, raise an
        # exception (channels come with credentials baked in already).
        if channel is not None and credentials is not None:
            raise ValueError(
                "The `channel` and `credentials` arguments are mutually " "exclusive."
            )

        # Create the channel.
        if channel is None:
            channel = self.create_channel(address=address, credentials=credentials)

        self._channel = channel

        # gRPC uses objects called "stubs" that are bound to the
        # channel and provide a basic method for each RPC.
        self._stubs = {
            "security_center_stub": securitycenter_service_pb2_grpc.SecurityCenterStub(
                channel
            )
        }

        # Because this API includes a method that returns a
        # long-running operation (proto: google.longrunning.Operation),
        # instantiate an LRO client.
        self._operations_client = google.api_core.operations_v1.OperationsClient(
            channel
        )

    @classmethod
    def create_channel(
        cls, address="securitycenter.googleapis.com:443", credentials=None
    ):
        """Create and return a gRPC channel object.

        Args:
            address (str): The host for the channel to use.
            credentials (~.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return google.api_core.grpc_helpers.create_channel(
            address, credentials=credentials, scopes=cls._OAUTH_SCOPES
        )

    @property
    def channel(self):
        """The gRPC channel used by the transport.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return self._channel

    @property
    def create_source(self):
        """Return the gRPC stub for :meth:`SecurityCenterClient.create_source`.

        Creates a source.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["security_center_stub"].CreateSource

    @property
    def create_finding(self):
        """Return the gRPC stub for :meth:`SecurityCenterClient.create_finding`.

        Creates a finding. The corresponding source must exist for finding creation
        to succeed.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["security_center_stub"].CreateFinding

    @property
    def get_iam_policy(self):
        """Return the gRPC stub for :meth:`SecurityCenterClient.get_iam_policy`.

        Gets the access control policy on the specified Source.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["security_center_stub"].GetIamPolicy

    @property
    def get_organization_settings(self):
        """Return the gRPC stub for :meth:`SecurityCenterClient.get_organization_settings`.

        Gets the settings for an organization.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["security_center_stub"].GetOrganizationSettings

    @property
    def get_source(self):
        """Return the gRPC stub for :meth:`SecurityCenterClient.get_source`.

        Gets a source.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["security_center_stub"].GetSource

    @property
    def group_assets(self):
        """Return the gRPC stub for :meth:`SecurityCenterClient.group_assets`.

        Filters an organization's assets and  groups them by their specified
        properties.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["security_center_stub"].GroupAssets

    @property
    def group_findings(self):
        """Return the gRPC stub for :meth:`SecurityCenterClient.group_findings`.

        Filters an organization or source's findings and groups them by their
        specified properties.

        To group across all sources provide a ``-`` as the source id. Example:
        /v1beta1/organizations/123/sources/-/findings

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["security_center_stub"].GroupFindings

    @property
    def list_assets(self):
        """Return the gRPC stub for :meth:`SecurityCenterClient.list_assets`.

        Lists an organization's assets.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["security_center_stub"].ListAssets

    @property
    def list_findings(self):
        """Return the gRPC stub for :meth:`SecurityCenterClient.list_findings`.

        Lists an organization or source's findings.

        To list across all sources provide a ``-`` as the source id. Example:
        /v1beta1/organizations/123/sources/-/findings

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["security_center_stub"].ListFindings

    @property
    def list_sources(self):
        """Return the gRPC stub for :meth:`SecurityCenterClient.list_sources`.

        Lists all sources belonging to an organization.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["security_center_stub"].ListSources

    @property
    def run_asset_discovery(self):
        """Return the gRPC stub for :meth:`SecurityCenterClient.run_asset_discovery`.

        Runs asset discovery. The discovery is tracked with a long-running
        operation.

        This API can only be called with limited frequency for an organization.
        If it is called too frequently the caller will receive a
        TOO\_MANY\_REQUESTS error.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["security_center_stub"].RunAssetDiscovery

    @property
    def set_finding_state(self):
        """Return the gRPC stub for :meth:`SecurityCenterClient.set_finding_state`.

        Updates the state of a finding.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["security_center_stub"].SetFindingState

    @property
    def set_iam_policy(self):
        """Return the gRPC stub for :meth:`SecurityCenterClient.set_iam_policy`.

        Sets the access control policy on the specified Source.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["security_center_stub"].SetIamPolicy

    @property
    def test_iam_permissions(self):
        """Return the gRPC stub for :meth:`SecurityCenterClient.test_iam_permissions`.

        Returns the permissions that a caller has on the specified source.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["security_center_stub"].TestIamPermissions

    @property
    def update_finding(self):
        """Return the gRPC stub for :meth:`SecurityCenterClient.update_finding`.

        Creates or updates a finding. The corresponding source must exist for a
        finding creation to succeed.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["security_center_stub"].UpdateFinding

    @property
    def update_organization_settings(self):
        """Return the gRPC stub for :meth:`SecurityCenterClient.update_organization_settings`.

        Updates an organization's settings.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["security_center_stub"].UpdateOrganizationSettings

    @property
    def update_source(self):
        """Return the gRPC stub for :meth:`SecurityCenterClient.update_source`.

        Updates a source.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["security_center_stub"].UpdateSource

    @property
    def update_security_marks(self):
        """Return the gRPC stub for :meth:`SecurityCenterClient.update_security_marks`.

        Updates security marks.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["security_center_stub"].UpdateSecurityMarks
