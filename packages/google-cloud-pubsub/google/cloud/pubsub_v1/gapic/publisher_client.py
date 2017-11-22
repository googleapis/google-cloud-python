# Copyright 2017, Google Inc. All rights reserved.
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

import functools
import pkg_resources

import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.grpc_helpers
import google.api_core.page_iterator
import google.api_core.path_template

from google.cloud.pubsub_v1.gapic import publisher_client_config
from google.cloud.pubsub_v1.proto import pubsub_pb2
from google.iam.v1 import iam_policy_pb2
from google.iam.v1 import policy_pb2
from google.protobuf import field_mask_pb2


_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    'google-cloud-pubsub').version


class PublisherClient(object):
    """
    The service that an application uses to manipulate topics, and to send
    messages to a topic.
    """

    SERVICE_ADDRESS = 'pubsub.googleapis.com:443'
    """The default address of the service."""

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _DEFAULT_SCOPES = (
        'https://www.googleapis.com/auth/cloud-platform',
        'https://www.googleapis.com/auth/pubsub', )

    # The name of the interface for this client. This is the key used to find
    # method configuration in the client_config dictionary
    _INTERFACE_NAME = ('google.pubsub.v1.Publisher')

    @classmethod
    def project_path(cls, project):
        """Returns a fully-qualified project resource name string."""
        return google.api_core.path_template.expand(
            'projects/{project}',
            project=project, )

    @classmethod
    def topic_path(cls, project, topic):
        """Returns a fully-qualified topic resource name string."""
        return google.api_core.path_template.expand(
            'projects/{project}/topics/{topic}',
            project=project,
            topic=topic, )

    def __init__(self,
                 channel=None,
                 credentials=None,
                 client_config=publisher_client_config.config,
                 client_info=None):
        """Constructor.

        Args:
            channel (grpc.Channel): A ``Channel`` instance through
                which to make calls. If specified, then the ``credentials``
                argument is ignored.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            client_config (dict):
                A dictionary of call options for each method. If not specified
                the default configuration is used. Generally, you only need
                to set this if you're developing your own client library.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
        """
        if channel is not None and credentials is not None:
            raise ValueError(
                'channel and credentials arguments to {} are mutually '
                'exclusive.'.format(self.__class__.__name__))

        if channel is None:
            channel = google.api_core.grpc_helpers.create_channel(
                self.SERVICE_ADDRESS,
                credentials=credentials,
                scopes=self._DEFAULT_SCOPES)

        self.iam_policy_stub = (iam_policy_pb2.IAMPolicyStub(channel))
        self.publisher_stub = (pubsub_pb2.PublisherStub(channel))

        if client_info is None:
            client_info = (
                google.api_core.gapic_v1.client_info.DEFAULT_CLIENT_INFO)

        client_info.gapic_version = _GAPIC_LIBRARY_VERSION

        interface_config = client_config['interfaces'][self._INTERFACE_NAME]
        method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            interface_config)

        self._create_topic = google.api_core.gapic_v1.method.wrap_method(
            self.publisher_stub.CreateTopic,
            default_retry=method_configs['CreateTopic'].retry,
            default_timeout=method_configs['CreateTopic'].timeout,
            client_info=client_info)
        self._update_topic = google.api_core.gapic_v1.method.wrap_method(
            self.publisher_stub.UpdateTopic,
            default_retry=method_configs['UpdateTopic'].retry,
            default_timeout=method_configs['UpdateTopic'].timeout,
            client_info=client_info)
        self._publish = google.api_core.gapic_v1.method.wrap_method(
            self.publisher_stub.Publish,
            default_retry=method_configs['Publish'].retry,
            default_timeout=method_configs['Publish'].timeout,
            client_info=client_info)
        self._get_topic = google.api_core.gapic_v1.method.wrap_method(
            self.publisher_stub.GetTopic,
            default_retry=method_configs['GetTopic'].retry,
            default_timeout=method_configs['GetTopic'].timeout,
            client_info=client_info)
        self._list_topics = google.api_core.gapic_v1.method.wrap_method(
            self.publisher_stub.ListTopics,
            default_retry=method_configs['ListTopics'].retry,
            default_timeout=method_configs['ListTopics'].timeout,
            client_info=client_info)
        self._list_topic_subscriptions = google.api_core.gapic_v1.method.wrap_method(
            self.publisher_stub.ListTopicSubscriptions,
            default_retry=method_configs['ListTopicSubscriptions'].retry,
            default_timeout=method_configs['ListTopicSubscriptions'].timeout,
            client_info=client_info)
        self._delete_topic = google.api_core.gapic_v1.method.wrap_method(
            self.publisher_stub.DeleteTopic,
            default_retry=method_configs['DeleteTopic'].retry,
            default_timeout=method_configs['DeleteTopic'].timeout,
            client_info=client_info)
        self._set_iam_policy = google.api_core.gapic_v1.method.wrap_method(
            self.iam_policy_stub.SetIamPolicy,
            default_retry=method_configs['SetIamPolicy'].retry,
            default_timeout=method_configs['SetIamPolicy'].timeout,
            client_info=client_info)
        self._get_iam_policy = google.api_core.gapic_v1.method.wrap_method(
            self.iam_policy_stub.GetIamPolicy,
            default_retry=method_configs['GetIamPolicy'].retry,
            default_timeout=method_configs['GetIamPolicy'].timeout,
            client_info=client_info)
        self._test_iam_permissions = google.api_core.gapic_v1.method.wrap_method(
            self.iam_policy_stub.TestIamPermissions,
            default_retry=method_configs['TestIamPermissions'].retry,
            default_timeout=method_configs['TestIamPermissions'].timeout,
            client_info=client_info)

    # Service calls
    def create_topic(self,
                     name,
                     labels=None,
                     retry=google.api_core.gapic_v1.method.DEFAULT,
                     timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Creates the given topic with the given name.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.PublisherClient()
            >>>
            >>> name = client.topic_path('[PROJECT]', '[TOPIC]')
            >>>
            >>> response = client.create_topic(name)

        Args:
            name (str): The name of the topic. It must have the format
                ``\"projects/{project}/topics/{topic}\"``. ``{topic}`` must start with a letter,
                and contain only letters (``[A-Za-z]``), numbers (``[0-9]``), dashes (``-``),
                underscores (``_``), periods (``.``), tildes (``~``), plus (``+``) or percent
                signs (``%``). It must be between 3 and 255 characters in length, and it
                must not start with ``\"goog\"``.
            labels (dict[str -> str]): User labels.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.pubsub_v1.types.Topic` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = pubsub_pb2.Topic(name=name, labels=labels)
        return self._create_topic(request, retry=retry, timeout=timeout)

    def update_topic(self,
                     topic,
                     update_mask,
                     retry=google.api_core.gapic_v1.method.DEFAULT,
                     timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Updates an existing topic. Note that certain properties of a topic are not
        modifiable.  Options settings follow the style guide:
        NOTE:  The style guide requires body: \"topic\" instead of body: \"*\".
        Keeping the latter for internal consistency in V1, however it should be
        corrected in V2.  See
        https://cloud.google.com/apis/design/standard_methods#update for details.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.PublisherClient()
            >>>
            >>> topic = {}
            >>> update_mask = {}
            >>>
            >>> response = client.update_topic(topic, update_mask)

        Args:
            topic (Union[dict, ~google.cloud.pubsub_v1.types.Topic]): The topic to update.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.pubsub_v1.types.Topic`
            update_mask (Union[dict, ~google.cloud.pubsub_v1.types.FieldMask]): Indicates which fields in the provided topic to update.
                Must be specified and non-empty.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.pubsub_v1.types.FieldMask`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.pubsub_v1.types.Topic` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = pubsub_pb2.UpdateTopicRequest(
            topic=topic, update_mask=update_mask)
        return self._update_topic(request, retry=retry, timeout=timeout)

    def publish(self,
                topic,
                messages,
                retry=google.api_core.gapic_v1.method.DEFAULT,
                timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Adds one or more messages to the topic. Returns ``NOT_FOUND`` if the topic
        does not exist. The message payload must not be empty; it must contain
        either a non-empty data field, or at least one attribute.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.PublisherClient()
            >>>
            >>> topic = client.topic_path('[PROJECT]', '[TOPIC]')
            >>> data = b''
            >>> messages_element = {'data': data}
            >>> messages = [messages_element]
            >>>
            >>> response = client.publish(topic, messages)

        Args:
            topic (str): The messages in the request will be published on this topic.
                Format is ``projects/{project}/topics/{topic}``.
            messages (list[Union[dict, ~google.cloud.pubsub_v1.types.PubsubMessage]]): The messages to publish.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.pubsub_v1.types.PubsubMessage`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.pubsub_v1.types.PublishResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = pubsub_pb2.PublishRequest(topic=topic, messages=messages)
        return self._publish(request, retry=retry, timeout=timeout)

    def get_topic(self,
                  topic,
                  retry=google.api_core.gapic_v1.method.DEFAULT,
                  timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Gets the configuration of a topic.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.PublisherClient()
            >>>
            >>> topic = client.topic_path('[PROJECT]', '[TOPIC]')
            >>>
            >>> response = client.get_topic(topic)

        Args:
            topic (str): The name of the topic to get.
                Format is ``projects/{project}/topics/{topic}``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.pubsub_v1.types.Topic` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = pubsub_pb2.GetTopicRequest(topic=topic)
        return self._get_topic(request, retry=retry, timeout=timeout)

    def list_topics(self,
                    project,
                    page_size=None,
                    retry=google.api_core.gapic_v1.method.DEFAULT,
                    timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Lists matching topics.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.PublisherClient()
            >>>
            >>> project = client.project_path('[PROJECT]')
            >>>
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_topics(project):
            ...     # process element
            ...     pass
            >>>
            >>> # Or iterate over results one page at a time
            >>> for page in client.list_topics(project, options=CallOptions(page_token=INITIAL_PAGE)):
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            project (str): The name of the cloud project that topics belong to.
                Format is ``projects/{project}``.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.gax.PageIterator` instance. By default, this
            is an iterable of :class:`~google.cloud.pubsub_v1.types.Topic` instances.
            This object can also be configured to iterate over the pages
            of the response through the `options` parameter.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = pubsub_pb2.ListTopicsRequest(
            project=project, page_size=page_size)
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._list_topics, retry=retry, timeout=timeout),
            request=request,
            items_field='topics',
            request_token_field='page_token',
            response_token_field='next_page_token')
        return iterator

    def list_topic_subscriptions(
            self,
            topic,
            page_size=None,
            retry=google.api_core.gapic_v1.method.DEFAULT,
            timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Lists the name of the subscriptions for this topic.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.PublisherClient()
            >>>
            >>> topic = client.topic_path('[PROJECT]', '[TOPIC]')
            >>>
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_topic_subscriptions(topic):
            ...     # process element
            ...     pass
            >>>
            >>> # Or iterate over results one page at a time
            >>> for page in client.list_topic_subscriptions(topic, options=CallOptions(page_token=INITIAL_PAGE)):
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            topic (str): The name of the topic that subscriptions are attached to.
                Format is ``projects/{project}/topics/{topic}``.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.gax.PageIterator` instance. By default, this
            is an iterable of :class:`str` instances.
            This object can also be configured to iterate over the pages
            of the response through the `options` parameter.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = pubsub_pb2.ListTopicSubscriptionsRequest(
            topic=topic, page_size=page_size)
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._list_topic_subscriptions, retry=retry, timeout=timeout),
            request=request,
            items_field='subscriptions',
            request_token_field='page_token',
            response_token_field='next_page_token')
        return iterator

    def delete_topic(self,
                     topic,
                     retry=google.api_core.gapic_v1.method.DEFAULT,
                     timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Deletes the topic with the given name. Returns ``NOT_FOUND`` if the topic
        does not exist. After a topic is deleted, a new topic may be created with
        the same name; this is an entirely new topic with none of the old
        configuration or subscriptions. Existing subscriptions to this topic are
        not deleted, but their ``topic`` field is set to ``_deleted-topic_``.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.PublisherClient()
            >>>
            >>> topic = client.topic_path('[PROJECT]', '[TOPIC]')
            >>>
            >>> client.delete_topic(topic)

        Args:
            topic (str): Name of the topic to delete.
                Format is ``projects/{project}/topics/{topic}``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = pubsub_pb2.DeleteTopicRequest(topic=topic)
        self._delete_topic(request, retry=retry, timeout=timeout)

    def set_iam_policy(self,
                       resource,
                       policy,
                       retry=google.api_core.gapic_v1.method.DEFAULT,
                       timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Sets the access control policy on the specified resource. Replaces any
        existing policy.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.PublisherClient()
            >>>
            >>> resource = client.topic_path('[PROJECT]', '[TOPIC]')
            >>> policy = {}
            >>>
            >>> response = client.set_iam_policy(resource, policy)

        Args:
            resource (str): REQUIRED: The resource for which the policy is being specified.
                ``resource`` is usually specified as a path. For example, a Project
                resource is specified as ``projects/{project}``.
            policy (Union[dict, ~google.cloud.pubsub_v1.types.Policy]): REQUIRED: The complete policy to be applied to the ``resource``. The size of
                the policy is limited to a few 10s of KB. An empty policy is a
                valid policy but certain Cloud Platform services (such as Projects)
                might reject them.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.pubsub_v1.types.Policy`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.pubsub_v1.types.Policy` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = iam_policy_pb2.SetIamPolicyRequest(
            resource=resource, policy=policy)
        return self._set_iam_policy(request, retry=retry, timeout=timeout)

    def get_iam_policy(self,
                       resource,
                       retry=google.api_core.gapic_v1.method.DEFAULT,
                       timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Gets the access control policy for a resource.
        Returns an empty policy if the resource exists and does not have a policy
        set.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.PublisherClient()
            >>>
            >>> resource = client.topic_path('[PROJECT]', '[TOPIC]')
            >>>
            >>> response = client.get_iam_policy(resource)

        Args:
            resource (str): REQUIRED: The resource for which the policy is being requested.
                ``resource`` is usually specified as a path. For example, a Project
                resource is specified as ``projects/{project}``.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.pubsub_v1.types.Policy` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = iam_policy_pb2.GetIamPolicyRequest(resource=resource)
        return self._get_iam_policy(request, retry=retry, timeout=timeout)

    def test_iam_permissions(self,
                             resource,
                             permissions,
                             retry=google.api_core.gapic_v1.method.DEFAULT,
                             timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Returns permissions that a caller has on the specified resource.
        If the resource does not exist, this will return an empty set of
        permissions, not a NOT_FOUND error.

        Example:
            >>> from google.cloud import pubsub_v1
            >>>
            >>> client = pubsub_v1.PublisherClient()
            >>>
            >>> resource = client.topic_path('[PROJECT]', '[TOPIC]')
            >>> permissions = []
            >>>
            >>> response = client.test_iam_permissions(resource, permissions)

        Args:
            resource (str): REQUIRED: The resource for which the policy detail is being requested.
                ``resource`` is usually specified as a path. For example, a Project
                resource is specified as ``projects/{project}``.
            permissions (list[str]): The set of permissions to check for the ``resource``. Permissions with
                wildcards (such as '*' or 'storage.*') are not allowed. For more
                information see
                `IAM Overview <https://cloud.google.com/iam/docs/overview#permissions>`_.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.pubsub_v1.types.TestIamPermissionsResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = iam_policy_pb2.TestIamPermissionsRequest(
            resource=resource, permissions=permissions)
        return self._test_iam_permissions(
            request, retry=retry, timeout=timeout)
