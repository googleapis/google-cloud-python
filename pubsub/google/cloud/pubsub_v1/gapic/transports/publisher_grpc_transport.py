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

from google.cloud.pubsub_v1.proto import pubsub_pb2_grpc
from google.iam.v1 import iam_policy_pb2_grpc as iam_policy_pb2_grpc


class PublisherGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.pubsub.v1 Publisher API.

    The transport provides access to the raw gRPC stubs,
    which can be used to take advantage of advanced
    features of gRPC.
    """

    # The scopes needed to make gRPC calls to all of the methods defined
    # in this service.
    _OAUTH_SCOPES = (
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/pubsub",
    )

    def __init__(
        self, channel=None, credentials=None, address="pubsub.googleapis.com:443"
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
            "iam_policy_stub": iam_policy_pb2_grpc.IAMPolicyStub(channel),
            "publisher_stub": pubsub_pb2_grpc.PublisherStub(channel),
        }

    @classmethod
    def create_channel(
        cls, address="pubsub.googleapis.com:443", credentials=None, **kwargs
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
    def create_topic(self):
        """Return the gRPC stub for :meth:`PublisherClient.create_topic`.

        Creates the given topic with the given name. See the resource name
        rules.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["publisher_stub"].CreateTopic

    @property
    def update_topic(self):
        """Return the gRPC stub for :meth:`PublisherClient.update_topic`.

        Updates an existing topic. Note that certain properties of a
        topic are not modifiable.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["publisher_stub"].UpdateTopic

    @property
    def publish(self):
        """Return the gRPC stub for :meth:`PublisherClient.publish`.

        Adds one or more messages to the topic. Returns ``NOT_FOUND`` if the
        topic does not exist.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["publisher_stub"].Publish

    @property
    def get_topic(self):
        """Return the gRPC stub for :meth:`PublisherClient.get_topic`.

        Gets the configuration of a topic.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["publisher_stub"].GetTopic

    @property
    def list_topics(self):
        """Return the gRPC stub for :meth:`PublisherClient.list_topics`.

        Lists matching topics.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["publisher_stub"].ListTopics

    @property
    def list_topic_subscriptions(self):
        """Return the gRPC stub for :meth:`PublisherClient.list_topic_subscriptions`.

        Lists the names of the subscriptions on this topic.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["publisher_stub"].ListTopicSubscriptions

    @property
    def delete_topic(self):
        """Return the gRPC stub for :meth:`PublisherClient.delete_topic`.

        Deletes the topic with the given name. Returns ``NOT_FOUND`` if the
        topic does not exist. After a topic is deleted, a new topic may be
        created with the same name; this is an entirely new topic with none of
        the old configuration or subscriptions. Existing subscriptions to this
        topic are not deleted, but their ``topic`` field is set to
        ``_deleted-topic_``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["publisher_stub"].DeleteTopic

    @property
    def set_iam_policy(self):
        """Return the gRPC stub for :meth:`PublisherClient.set_iam_policy`.

        Sets the access control policy on the specified resource. Replaces any
        existing policy.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["iam_policy_stub"].SetIamPolicy

    @property
    def get_iam_policy(self):
        """Return the gRPC stub for :meth:`PublisherClient.get_iam_policy`.

        Gets the access control policy for a resource.
        Returns an empty policy if the resource exists and does not have a policy
        set.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["iam_policy_stub"].GetIamPolicy

    @property
    def test_iam_permissions(self):
        """Return the gRPC stub for :meth:`PublisherClient.test_iam_permissions`.

        Returns permissions that a caller has on the specified resource. If the
        resource does not exist, this will return an empty set of permissions,
        not a NOT\_FOUND error.

        Note: This operation is designed to be used for building
        permission-aware UIs and command-line tools, not for authorization
        checking. This operation may "fail open" without warning.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["iam_policy_stub"].TestIamPermissions
