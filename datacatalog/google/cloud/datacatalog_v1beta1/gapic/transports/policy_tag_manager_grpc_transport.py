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

from google.cloud.datacatalog_v1beta1.proto import policytagmanager_pb2_grpc


class PolicyTagManagerGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.cloud.datacatalog.v1beta1 PolicyTagManager API.

    The transport provides access to the raw gRPC stubs,
    which can be used to take advantage of advanced
    features of gRPC.
    """

    # The scopes needed to make gRPC calls to all of the methods defined
    # in this service.
    _OAUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    def __init__(
        self, channel=None, credentials=None, address="datacatalog.googleapis.com:443"
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
            "policy_tag_manager_stub": policytagmanager_pb2_grpc.PolicyTagManagerStub(
                channel
            )
        }

    @classmethod
    def create_channel(
        cls, address="datacatalog.googleapis.com:443", credentials=None, **kwargs
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
    def create_taxonomy(self):
        """Return the gRPC stub for :meth:`PolicyTagManagerClient.create_taxonomy`.

        Creates a taxonomy in the specified project.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["policy_tag_manager_stub"].CreateTaxonomy

    @property
    def delete_taxonomy(self):
        """Return the gRPC stub for :meth:`PolicyTagManagerClient.delete_taxonomy`.

        Deletes a taxonomy. This operation will also delete all
        policy tags in this taxonomy along with their associated policies.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["policy_tag_manager_stub"].DeleteTaxonomy

    @property
    def update_taxonomy(self):
        """Return the gRPC stub for :meth:`PolicyTagManagerClient.update_taxonomy`.

        Updates a taxonomy.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["policy_tag_manager_stub"].UpdateTaxonomy

    @property
    def list_taxonomies(self):
        """Return the gRPC stub for :meth:`PolicyTagManagerClient.list_taxonomies`.

        Lists all taxonomies in a project in a particular location that the caller
        has permission to view.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["policy_tag_manager_stub"].ListTaxonomies

    @property
    def get_taxonomy(self):
        """Return the gRPC stub for :meth:`PolicyTagManagerClient.get_taxonomy`.

        Gets a taxonomy.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["policy_tag_manager_stub"].GetTaxonomy

    @property
    def create_policy_tag(self):
        """Return the gRPC stub for :meth:`PolicyTagManagerClient.create_policy_tag`.

        Creates a policy tag in the specified taxonomy.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["policy_tag_manager_stub"].CreatePolicyTag

    @property
    def delete_policy_tag(self):
        """Return the gRPC stub for :meth:`PolicyTagManagerClient.delete_policy_tag`.

        Deletes a policy tag. Also deletes all of its descendant policy tags.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["policy_tag_manager_stub"].DeletePolicyTag

    @property
    def update_policy_tag(self):
        """Return the gRPC stub for :meth:`PolicyTagManagerClient.update_policy_tag`.

        Updates a policy tag.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["policy_tag_manager_stub"].UpdatePolicyTag

    @property
    def list_policy_tags(self):
        """Return the gRPC stub for :meth:`PolicyTagManagerClient.list_policy_tags`.

        Lists all policy tags in a taxonomy.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["policy_tag_manager_stub"].ListPolicyTags

    @property
    def get_policy_tag(self):
        """Return the gRPC stub for :meth:`PolicyTagManagerClient.get_policy_tag`.

        Gets a policy tag.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["policy_tag_manager_stub"].GetPolicyTag

    @property
    def get_iam_policy(self):
        """Return the gRPC stub for :meth:`PolicyTagManagerClient.get_iam_policy`.

        Gets the IAM policy for a taxonomy or a policy tag.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["policy_tag_manager_stub"].GetIamPolicy

    @property
    def set_iam_policy(self):
        """Return the gRPC stub for :meth:`PolicyTagManagerClient.set_iam_policy`.

        Sets the IAM policy for a taxonomy or a policy tag.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["policy_tag_manager_stub"].SetIamPolicy

    @property
    def test_iam_permissions(self):
        """Return the gRPC stub for :meth:`PolicyTagManagerClient.test_iam_permissions`.

        Returns the permissions that a caller has on the specified taxonomy or
        policy tag.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["policy_tag_manager_stub"].TestIamPermissions
