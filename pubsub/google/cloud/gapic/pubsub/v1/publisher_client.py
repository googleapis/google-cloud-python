# Copyright 2017, Google LLC All rights reserved.
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
# EDITING INSTRUCTIONS
# This file was generated from the file
# https://github.com/google/googleapis/blob/master/google/pubsub/v1/pubsub.proto,
# and updates to that file get reflected here through a refresh process.
# For the short term, the refresh process will only be runnable by Google engineers.
#
# The only allowed edits are to method and file documentation. A 3-way
# merge preserves those additions if the generated source changes.
"""Accesses the google.pubsub.v1 Publisher API."""

import collections
import json
import os
import pkg_resources
import platform

from google.gax import api_callable
from google.gax import config
from google.gax import path_template
import google.gax

from google.cloud.proto.pubsub.v1 import pubsub_pb2
from google.iam.v1 import iam_policy_pb2
from google.iam.v1 import policy_pb2

_PageDesc = google.gax.PageDescriptor


class PublisherClient(object):
    """
    The service that an application uses to manipulate topics, and to send
    messages to a topic.
    """

    SERVICE_ADDRESS = 'pubsub.googleapis.com'
    """The default address of the service."""

    DEFAULT_SERVICE_PORT = 443
    """The default port of the service."""

    _PAGE_DESCRIPTORS = {
        'list_topics':
        _PageDesc('page_token', 'next_page_token', 'topics'),
        'list_topic_subscriptions':
        _PageDesc('page_token', 'next_page_token', 'subscriptions')
    }

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _ALL_SCOPES = ('https://www.googleapis.com/auth/cloud-platform',
                   'https://www.googleapis.com/auth/pubsub', )

    _PROJECT_PATH_TEMPLATE = path_template.PathTemplate('projects/{project}')
    _TOPIC_PATH_TEMPLATE = path_template.PathTemplate(
        'projects/{project}/topics/{topic}')

    @classmethod
    def project_path(cls, project):
        """Returns a fully-qualified project resource name string."""
        return cls._PROJECT_PATH_TEMPLATE.render({
            'project': project,
        })

    @classmethod
    def topic_path(cls, project, topic):
        """Returns a fully-qualified topic resource name string."""
        return cls._TOPIC_PATH_TEMPLATE.render({
            'project': project,
            'topic': topic,
        })

    @classmethod
    def match_project_from_project_name(cls, project_name):
        """Parses the project from a project resource.

        Args:
          project_name (string): A fully-qualified path representing a project
            resource.

        Returns:
          A string representing the project.
        """
        return cls._PROJECT_PATH_TEMPLATE.match(project_name).get('project')

    @classmethod
    def match_project_from_topic_name(cls, topic_name):
        """Parses the project from a topic resource.

        Args:
          topic_name (string): A fully-qualified path representing a topic
            resource.

        Returns:
          A string representing the project.
        """
        return cls._TOPIC_PATH_TEMPLATE.match(topic_name).get('project')

    @classmethod
    def match_topic_from_topic_name(cls, topic_name):
        """Parses the topic from a topic resource.

        Args:
          topic_name (string): A fully-qualified path representing a topic
            resource.

        Returns:
          A string representing the topic.
        """
        return cls._TOPIC_PATH_TEMPLATE.match(topic_name).get('topic')

    def __init__(self,
                 service_path=SERVICE_ADDRESS,
                 port=DEFAULT_SERVICE_PORT,
                 channel=None,
                 credentials=None,
                 ssl_credentials=None,
                 scopes=None,
                 client_config=None,
                 app_name=None,
                 app_version='',
                 lib_name=None,
                 lib_version='',
                 metrics_headers=()):
        """Constructor.

        Args:
          service_path (string): The domain name of the API remote host.
          port (int): The port on which to connect to the remote host.
          channel (:class:`grpc.Channel`): A ``Channel`` instance through
            which to make calls.
          credentials (object): The authorization credentials to attach to
            requests. These credentials identify this application to the
            service.
          ssl_credentials (:class:`grpc.ChannelCredentials`): A
            ``ChannelCredentials`` instance for use with an SSL-enabled
            channel.
          scopes (list[string]): A list of OAuth2 scopes to attach to requests.
          client_config (dict):
            A dictionary for call options for each method. See
            :func:`google.gax.construct_settings` for the structure of
            this data. Falls back to the default config if not specified
            or the specified config is missing data points.
          app_name (string): The name of the application calling
            the service. Recommended for analytics purposes.
          app_version (string): The version of the application calling
            the service. Recommended for analytics purposes.
          lib_name (string): The API library software used for calling
            the service. (Unless you are writing an API client itself,
            leave this as default.)
          lib_version (string): The API library software version used
            for calling the service. (Unless you are writing an API client
            itself, leave this as default.)
          metrics_headers (dict): A dictionary of values for tracking
            client library metrics. Ultimately serializes to a string
            (e.g. 'foo/1.2.3 bar/3.14.1'). This argument should be
            considered private.

        Returns:
          A PublisherClient object.
        """
        # Unless the calling application specifically requested
        # OAuth scopes, request everything.
        if scopes is None:
            scopes = self._ALL_SCOPES

        # Initialize an empty client config, if none is set.
        if client_config is None:
            client_config = {}

        # Initialize metrics_headers as an ordered dictionary
        # (cuts down on cardinality of the resulting string slightly).
        metrics_headers = collections.OrderedDict(metrics_headers)
        metrics_headers['gl-python'] = platform.python_version()

        # The library may or may not be set, depending on what is
        # calling this client. Newer client libraries set the library name
        # and version.
        if lib_name:
            metrics_headers[lib_name] = lib_version

        # Finally, track the GAPIC package version.
        metrics_headers['gapic'] = pkg_resources.get_distribution(
            'google-cloud-pubsub', ).version

        # Load the configuration defaults.
        default_client_config = json.loads(
            pkg_resources.resource_string(
                __name__, 'publisher_client_config.json').decode())
        defaults = api_callable.construct_settings(
            'google.pubsub.v1.Publisher',
            default_client_config,
            client_config,
            config.STATUS_CODE_NAMES,
            metrics_headers=metrics_headers,
            page_descriptors=self._PAGE_DESCRIPTORS, )
        self.iam_policy_stub = config.create_stub(
            iam_policy_pb2.IAMPolicyStub,
            channel=channel,
            service_path=service_path,
            service_port=port,
            credentials=credentials,
            scopes=scopes,
            ssl_credentials=ssl_credentials)
        self.publisher_stub = config.create_stub(
            pubsub_pb2.PublisherStub,
            channel=channel,
            service_path=service_path,
            service_port=port,
            credentials=credentials,
            scopes=scopes,
            ssl_credentials=ssl_credentials)

        self._create_topic = api_callable.create_api_call(
            self.publisher_stub.CreateTopic, settings=defaults['create_topic'])
        self._publish = api_callable.create_api_call(
            self.publisher_stub.Publish, settings=defaults['publish'])
        self._get_topic = api_callable.create_api_call(
            self.publisher_stub.GetTopic, settings=defaults['get_topic'])
        self._list_topics = api_callable.create_api_call(
            self.publisher_stub.ListTopics, settings=defaults['list_topics'])
        self._list_topic_subscriptions = api_callable.create_api_call(
            self.publisher_stub.ListTopicSubscriptions,
            settings=defaults['list_topic_subscriptions'])
        self._delete_topic = api_callable.create_api_call(
            self.publisher_stub.DeleteTopic, settings=defaults['delete_topic'])
        self._set_iam_policy = api_callable.create_api_call(
            self.iam_policy_stub.SetIamPolicy,
            settings=defaults['set_iam_policy'])
        self._get_iam_policy = api_callable.create_api_call(
            self.iam_policy_stub.GetIamPolicy,
            settings=defaults['get_iam_policy'])
        self._test_iam_permissions = api_callable.create_api_call(
            self.iam_policy_stub.TestIamPermissions,
            settings=defaults['test_iam_permissions'])

    # Service calls
    def create_topic(self, name, options=None):
        """
        Creates the given topic with the given name.

        Example:
          >>> from google.cloud.gapic.pubsub.v1 import publisher_client
          >>> client = publisher_client.PublisherClient()
          >>> name = client.topic_path('[PROJECT]', '[TOPIC]')
          >>> response = client.create_topic(name)

        Args:
          name (string): The name of the topic. It must have the format
            ``\"projects/{project}/topics/{topic}\"``. ``{topic}`` must start with a letter,
            and contain only letters (``[A-Za-z]``), numbers (``[0-9]``), dashes (``-``),
            underscores (``_``), periods (``.``), tildes (``~``), plus (``+``) or percent
            signs (``%``). It must be between 3 and 255 characters in length, and it
            must not start with ``\"goog\"``.
          options (:class:`google.gax.CallOptions`): Overrides the default
            settings for this call, e.g, timeout, retries etc.

        Returns:
          A :class:`google.cloud.proto.pubsub.v1.pubsub_pb2.Topic` instance.

        Raises:
          :exc:`google.gax.errors.GaxError` if the RPC is aborted.
          :exc:`ValueError` if the parameters are invalid.
        """
        # Create the request object.
        request = pubsub_pb2.Topic(name=name)
        return self._create_topic(request, options)

    def publish(self, topic, messages, options=None):
        """
        Adds one or more messages to the topic. Returns ``NOT_FOUND`` if the topic
        does not exist. The message payload must not be empty; it must contain
        either a non-empty data field, or at least one attribute.

        Example:
          >>> from google.cloud.gapic.pubsub.v1 import publisher_client
          >>> from google.cloud.proto.pubsub.v1 import pubsub_pb2
          >>> client = publisher_client.PublisherClient()
          >>> topic = client.topic_path('[PROJECT]', '[TOPIC]')
          >>> data = b''
          >>> messages_element = pubsub_pb2.PubsubMessage(data=data)
          >>> messages = [messages_element]
          >>> response = client.publish(topic, messages)

        Args:
          topic (string): The messages in the request will be published on this topic.
            Format is ``projects/{project}/topics/{topic}``.
          messages (list[:class:`google.cloud.proto.pubsub.v1.pubsub_pb2.PubsubMessage`]): The messages to publish.
          options (:class:`google.gax.CallOptions`): Overrides the default
            settings for this call, e.g, timeout, retries etc.

        Returns:
          A :class:`google.cloud.proto.pubsub.v1.pubsub_pb2.PublishResponse` instance.

        Raises:
          :exc:`google.gax.errors.GaxError` if the RPC is aborted.
          :exc:`ValueError` if the parameters are invalid.
        """
        # Create the request object.
        request = pubsub_pb2.PublishRequest(topic=topic, messages=messages)
        return self._publish(request, options)

    def get_topic(self, topic, options=None):
        """
        Gets the configuration of a topic.

        Example:
          >>> from google.cloud.gapic.pubsub.v1 import publisher_client
          >>> client = publisher_client.PublisherClient()
          >>> topic = client.topic_path('[PROJECT]', '[TOPIC]')
          >>> response = client.get_topic(topic)

        Args:
          topic (string): The name of the topic to get.
            Format is ``projects/{project}/topics/{topic}``.
          options (:class:`google.gax.CallOptions`): Overrides the default
            settings for this call, e.g, timeout, retries etc.

        Returns:
          A :class:`google.cloud.proto.pubsub.v1.pubsub_pb2.Topic` instance.

        Raises:
          :exc:`google.gax.errors.GaxError` if the RPC is aborted.
          :exc:`ValueError` if the parameters are invalid.
        """
        # Create the request object.
        request = pubsub_pb2.GetTopicRequest(topic=topic)
        return self._get_topic(request, options)

    def list_topics(self, project, page_size=None, options=None):
        """
        Lists matching topics.

        Example:
          >>> from google.cloud.gapic.pubsub.v1 import publisher_client
          >>> from google.gax import CallOptions, INITIAL_PAGE
          >>> client = publisher_client.PublisherClient()
          >>> project = client.project_path('[PROJECT]')
          >>>
          >>> # Iterate over all results
          >>> for element in client.list_topics(project):
          >>>     # process element
          >>>     pass
          >>>
          >>> # Or iterate over results one page at a time
          >>> for page in client.list_topics(project, options=CallOptions(page_token=INITIAL_PAGE)):
          >>>     for element in page:
          >>>         # process element
          >>>         pass

        Args:
          project (string): The name of the cloud project that topics belong to.
            Format is ``projects/{project}``.
          page_size (int): The maximum number of resources contained in the
            underlying API response. If page streaming is performed per-
            resource, this parameter does not affect the return value. If page
            streaming is performed per-page, this determines the maximum number
            of resources in a page.
          options (:class:`google.gax.CallOptions`): Overrides the default
            settings for this call, e.g, timeout, retries etc.

        Returns:
          A :class:`google.gax.PageIterator` instance. By default, this
          is an iterable of :class:`google.cloud.proto.pubsub.v1.pubsub_pb2.Topic` instances.
          This object can also be configured to iterate over the pages
          of the response through the `CallOptions` parameter.

        Raises:
          :exc:`google.gax.errors.GaxError` if the RPC is aborted.
          :exc:`ValueError` if the parameters are invalid.
        """
        # Create the request object.
        request = pubsub_pb2.ListTopicsRequest(
            project=project, page_size=page_size)
        return self._list_topics(request, options)

    def list_topic_subscriptions(self, topic, page_size=None, options=None):
        """
        Lists the name of the subscriptions for this topic.

        Example:
          >>> from google.cloud.gapic.pubsub.v1 import publisher_client
          >>> from google.gax import CallOptions, INITIAL_PAGE
          >>> client = publisher_client.PublisherClient()
          >>> topic = client.topic_path('[PROJECT]', '[TOPIC]')
          >>>
          >>> # Iterate over all results
          >>> for element in client.list_topic_subscriptions(topic):
          >>>     # process element
          >>>     pass
          >>>
          >>> # Or iterate over results one page at a time
          >>> for page in client.list_topic_subscriptions(topic, options=CallOptions(page_token=INITIAL_PAGE)):
          >>>     for element in page:
          >>>         # process element
          >>>         pass

        Args:
          topic (string): The name of the topic that subscriptions are attached to.
            Format is ``projects/{project}/topics/{topic}``.
          page_size (int): The maximum number of resources contained in the
            underlying API response. If page streaming is performed per-
            resource, this parameter does not affect the return value. If page
            streaming is performed per-page, this determines the maximum number
            of resources in a page.
          options (:class:`google.gax.CallOptions`): Overrides the default
            settings for this call, e.g, timeout, retries etc.

        Returns:
          A :class:`google.gax.PageIterator` instance. By default, this
          is an iterable of string instances.
          This object can also be configured to iterate over the pages
          of the response through the `CallOptions` parameter.

        Raises:
          :exc:`google.gax.errors.GaxError` if the RPC is aborted.
          :exc:`ValueError` if the parameters are invalid.
        """
        # Create the request object.
        request = pubsub_pb2.ListTopicSubscriptionsRequest(
            topic=topic, page_size=page_size)
        return self._list_topic_subscriptions(request, options)

    def delete_topic(self, topic, options=None):
        """
        Deletes the topic with the given name. Returns ``NOT_FOUND`` if the topic
        does not exist. After a topic is deleted, a new topic may be created with
        the same name; this is an entirely new topic with none of the old
        configuration or subscriptions. Existing subscriptions to this topic are
        not deleted, but their ``topic`` field is set to ``_deleted-topic_``.

        Example:
          >>> from google.cloud.gapic.pubsub.v1 import publisher_client
          >>> client = publisher_client.PublisherClient()
          >>> topic = client.topic_path('[PROJECT]', '[TOPIC]')
          >>> client.delete_topic(topic)

        Args:
          topic (string): Name of the topic to delete.
            Format is ``projects/{project}/topics/{topic}``.
          options (:class:`google.gax.CallOptions`): Overrides the default
            settings for this call, e.g, timeout, retries etc.

        Raises:
          :exc:`google.gax.errors.GaxError` if the RPC is aborted.
          :exc:`ValueError` if the parameters are invalid.
        """
        # Create the request object.
        request = pubsub_pb2.DeleteTopicRequest(topic=topic)
        self._delete_topic(request, options)

    def set_iam_policy(self, resource, policy, options=None):
        """
        Sets the access control policy on the specified resource. Replaces any
        existing policy.

        Example:
          >>> from google.cloud.gapic.pubsub.v1 import publisher_client
          >>> from google.iam.v1 import policy_pb2
          >>> client = publisher_client.PublisherClient()
          >>> resource = client.topic_path('[PROJECT]', '[TOPIC]')
          >>> policy = policy_pb2.Policy()
          >>> response = client.set_iam_policy(resource, policy)

        Args:
          resource (string): REQUIRED: The resource for which the policy is being specified.
            ``resource`` is usually specified as a path. For example, a Project
            resource is specified as ``projects/{project}``.
          policy (:class:`google.iam.v1.policy_pb2.Policy`): REQUIRED: The complete policy to be applied to the ``resource``. The size of
            the policy is limited to a few 10s of KB. An empty policy is a
            valid policy but certain Cloud Platform services (such as Projects)
            might reject them.
          options (:class:`google.gax.CallOptions`): Overrides the default
            settings for this call, e.g, timeout, retries etc.

        Returns:
          A :class:`google.iam.v1.policy_pb2.Policy` instance.

        Raises:
          :exc:`google.gax.errors.GaxError` if the RPC is aborted.
          :exc:`ValueError` if the parameters are invalid.
        """
        # Create the request object.
        request = iam_policy_pb2.SetIamPolicyRequest(
            resource=resource, policy=policy)
        return self._set_iam_policy(request, options)

    def get_iam_policy(self, resource, options=None):
        """
        Gets the access control policy for a resource.
        Returns an empty policy if the resource exists and does not have a policy
        set.

        Example:
          >>> from google.cloud.gapic.pubsub.v1 import publisher_client
          >>> client = publisher_client.PublisherClient()
          >>> resource = client.topic_path('[PROJECT]', '[TOPIC]')
          >>> response = client.get_iam_policy(resource)

        Args:
          resource (string): REQUIRED: The resource for which the policy is being requested.
            ``resource`` is usually specified as a path. For example, a Project
            resource is specified as ``projects/{project}``.
          options (:class:`google.gax.CallOptions`): Overrides the default
            settings for this call, e.g, timeout, retries etc.

        Returns:
          A :class:`google.iam.v1.policy_pb2.Policy` instance.

        Raises:
          :exc:`google.gax.errors.GaxError` if the RPC is aborted.
          :exc:`ValueError` if the parameters are invalid.
        """
        # Create the request object.
        request = iam_policy_pb2.GetIamPolicyRequest(resource=resource)
        return self._get_iam_policy(request, options)

    def test_iam_permissions(self, resource, permissions, options=None):
        """
        Returns permissions that a caller has on the specified resource.
        If the resource does not exist, this will return an empty set of
        permissions, not a NOT_FOUND error.

        Example:
          >>> from google.cloud.gapic.pubsub.v1 import publisher_client
          >>> client = publisher_client.PublisherClient()
          >>> resource = client.topic_path('[PROJECT]', '[TOPIC]')
          >>> permissions = []
          >>> response = client.test_iam_permissions(resource, permissions)

        Args:
          resource (string): REQUIRED: The resource for which the policy detail is being requested.
            ``resource`` is usually specified as a path. For example, a Project
            resource is specified as ``projects/{project}``.
          permissions (list[string]): The set of permissions to check for the ``resource``. Permissions with
            wildcards (such as '*' or 'storage.*') are not allowed. For more
            information see
            `IAM Overview <https://cloud.google.com/iam/docs/overview#permissions>`_.
          options (:class:`google.gax.CallOptions`): Overrides the default
            settings for this call, e.g, timeout, retries etc.

        Returns:
          A :class:`google.iam.v1.iam_policy_pb2.TestIamPermissionsResponse` instance.

        Raises:
          :exc:`google.gax.errors.GaxError` if the RPC is aborted.
          :exc:`ValueError` if the parameters are invalid.
        """
        # Create the request object.
        request = iam_policy_pb2.TestIamPermissionsRequest(
            resource=resource, permissions=permissions)
        return self._test_iam_permissions(request, options)
