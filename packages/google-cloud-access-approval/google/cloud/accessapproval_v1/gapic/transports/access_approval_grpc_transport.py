# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
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

from google.cloud.accessapproval_v1.proto import accessapproval_pb2_grpc


class AccessApprovalGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.cloud.accessapproval.v1 AccessApproval API.

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
        address="accessapproval.googleapis.com:443",
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
            channel = self.create_channel(
                address=address,
                credentials=credentials,
                options={
                    "grpc.max_send_message_length": -1,
                    "grpc.max_receive_message_length": -1,
                }.items(),
            )

        self._channel = channel

        # gRPC uses objects called "stubs" that are bound to the
        # channel and provide a basic method for each RPC.
        self._stubs = {
            "access_approval_stub": accessapproval_pb2_grpc.AccessApprovalStub(channel)
        }

    @classmethod
    def create_channel(
        cls, address="accessapproval.googleapis.com:443", credentials=None, **kwargs
    ):
        """Create and return a gRPC channel object.

        Args:
            address (str): The host for the channel to use.
            credentials (~.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            kwargs (dict): Keyword arguments, which are passed to the
                channel creation.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return google.api_core.grpc_helpers.create_channel(
            address, credentials=credentials, scopes=cls._OAUTH_SCOPES, **kwargs
        )

    @property
    def channel(self):
        """The gRPC channel used by the transport.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return self._channel

    @property
    def list_approval_requests(self):
        """Return the gRPC stub for :meth:`AccessApprovalClient.list_approval_requests`.

        Lists approval requests associated with a project, folder, or organization.
        Approval requests can be filtered by state (pending, active, dismissed).
        The order is reverse chronological.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["access_approval_stub"].ListApprovalRequests

    @property
    def get_approval_request(self):
        """Return the gRPC stub for :meth:`AccessApprovalClient.get_approval_request`.

        Gets an approval request. Returns NOT_FOUND if the request does not
        exist.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["access_approval_stub"].GetApprovalRequest

    @property
    def approve_approval_request(self):
        """Return the gRPC stub for :meth:`AccessApprovalClient.approve_approval_request`.

        Approves a request and returns the updated ApprovalRequest.

        Returns NOT_FOUND if the request does not exist. Returns
        FAILED_PRECONDITION if the request exists but is not in a pending state.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["access_approval_stub"].ApproveApprovalRequest

    @property
    def dismiss_approval_request(self):
        """Return the gRPC stub for :meth:`AccessApprovalClient.dismiss_approval_request`.

        Dismisses a request. Returns the updated ApprovalRequest.

        NOTE: This does not deny access to the resource if another request has
        been made and approved. It is equivalent in effect to ignoring the
        request altogether.

        Returns NOT_FOUND if the request does not exist.

        Returns FAILED_PRECONDITION if the request exists but is not in a
        pending state.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["access_approval_stub"].DismissApprovalRequest

    @property
    def get_access_approval_settings(self):
        """Return the gRPC stub for :meth:`AccessApprovalClient.get_access_approval_settings`.

        Gets the settings associated with a project, folder, or organization.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["access_approval_stub"].GetAccessApprovalSettings

    @property
    def update_access_approval_settings(self):
        """Return the gRPC stub for :meth:`AccessApprovalClient.update_access_approval_settings`.

        Updates the settings associated with a project, folder, or
        organization. Settings to update are determined by the value of
        field_mask.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["access_approval_stub"].UpdateAccessApprovalSettings

    @property
    def delete_access_approval_settings(self):
        """Return the gRPC stub for :meth:`AccessApprovalClient.delete_access_approval_settings`.

        Deletes the settings associated with a project, folder, or organization.
        This will have the effect of disabling Access Approval for the project,
        folder, or organization, but only if all ancestors also have Access
        Approval disabled. If Access Approval is enabled at a higher level of the
        hierarchy, then Access Approval will still be enabled at this level as
        the settings are inherited.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["access_approval_stub"].DeleteAccessApprovalSettings
