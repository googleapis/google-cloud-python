# Copyright 2015 Google Inc. All rights reserved.
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

"""Create / interact with gcloud pubsub connections."""

import os

from gcloud import connection as base_connection
from gcloud.environment_vars import PUBSUB_EMULATOR


class Connection(base_connection.JSONConnection):
    """A connection to Google Cloud Pubsub via the JSON REST API.

    :type credentials: :class:`oauth2client.client.OAuth2Credentials`
    :param credentials: (Optional) The OAuth2 Credentials to use for this
                        connection.

    :type http: :class:`httplib2.Http` or class that defines ``request()``.
    :param http: (Optional) HTTP object to make requests.

    :type api_base_url: string
    :param api_base_url: The base of the API call URL. Defaults to the value
                         :attr:`Connection.API_BASE_URL`.
    """

    API_BASE_URL = 'https://pubsub.googleapis.com'
    """The base of the API call URL."""

    API_VERSION = 'v1'
    """The version of the API, used in building the API call's URL."""

    API_URL_TEMPLATE = '{api_base_url}/{api_version}{path}'
    """A template for the URL of a particular API call."""

    SCOPE = ('https://www.googleapis.com/auth/pubsub',
             'https://www.googleapis.com/auth/cloud-platform')
    """The scopes required for authenticating as a Cloud Pub/Sub consumer."""

    def __init__(self, credentials=None, http=None, api_base_url=None):
        super(Connection, self).__init__(credentials=credentials, http=http)
        if api_base_url is None:
            emulator_host = os.getenv(PUBSUB_EMULATOR)
            if emulator_host is None:
                api_base_url = self.__class__.API_BASE_URL
            else:
                api_base_url = 'http://' + emulator_host
        self.api_base_url = api_base_url

    def build_api_url(self, path, query_params=None,
                      api_base_url=None, api_version=None):
        """Construct an API url given a few components, some optional.

        Typically, you shouldn't need to use this method.

        :type path: string
        :param path: The path to the resource.

        :type query_params: dict
        :param query_params: A dictionary of keys and values to insert into
                             the query string of the URL.

        :type api_base_url: string
        :param api_base_url: The base URL for the API endpoint.
                             Typically you won't have to provide this.

        :type api_version: string
        :param api_version: The version of the API to call.
                            Typically you shouldn't provide this and instead
                            use the default for the library.

        :rtype: string
        :returns: The URL assembled from the pieces provided.
        """
        if api_base_url is None:
            api_base_url = self.api_base_url
        return super(Connection, self.__class__).build_api_url(
            path, query_params=query_params,
            api_base_url=api_base_url, api_version=api_version)


class _PublisherAPI(object):
    """Helper mapping publisher-related APIs.

    :type connection: :class:`Connection`
    :param connection: the connection used to make API requests.
    """

    def __init__(self, connection):
        self._connection = connection

    def list_topics(self, project, page_size=None, page_token=None):
        """API call:  list topics for a given project

        See:
        https://cloud.google.com/pubsub/reference/rest/v1/projects.topics/list

        :type project: string
        :param project: project ID

        :type page_size: int
        :param page_size: maximum number of topics to return, If not passed,
                          defaults to a value set by the API.

        :type page_token: string
        :param page_token: opaque marker for the next "page" of topics. If not
                           passed, the API will return the first page of
                           topics.

        :rtype: tuple, (list, str)
        :returns: list of ``Topic`` resource dicts, plus a
                  "next page token" string:  if not None, indicates that
                  more topics can be retrieved with another call (pass that
                  value as ``page_token``).
        """
        conn = self._connection
        params = {}

        if page_size is not None:
            params['pageSize'] = page_size

        if page_token is not None:
            params['pageToken'] = page_token

        path = '/projects/%s/topics' % (project,)
        resp = conn.api_request(method='GET', path=path, query_params=params)
        return resp.get('topics', ()), resp.get('nextPageToken')

    def topic_create(self, topic_path):
        """API call:  create a topic

        See:
        https://cloud.google.com/pubsub/reference/rest/v1/projects.topics/create

        :type topic_path: string
        :param topic_path: the fully-qualified path of the new topic, in format
                           ``projects/<PROJECT>/topics/<TOPIC_NAME>``.

        :rtype: dict
        :returns: ``Topic`` resource returned from the API.
        """
        conn = self._connection
        return conn.api_request(method='PUT', path='/%s' % (topic_path,))

    def topic_get(self, topic_path):
        """API call:  retrieve a topic

        See:
        https://cloud.google.com/pubsub/reference/rest/v1/projects.topics/get

        :type topic_path: string
        :param topic_path: the fully-qualified path of the topic, in format
                           ``projects/<PROJECT>/topics/<TOPIC_NAME>``.

        :rtype: dict
        :returns: ``Topic`` resource returned from the API.
        """
        conn = self._connection
        return conn.api_request(method='GET', path='/%s' % (topic_path,))

    def topic_delete(self, topic_path):
        """API call:  delete a topic

        See:
        https://cloud.google.com/pubsub/reference/rest/v1/projects.topics/delete

        :type topic_path: string
        :param topic_path: the fully-qualified path of the topic, in format
                           ``projects/<PROJECT>/topics/<TOPIC_NAME>``.
        """
        conn = self._connection
        conn.api_request(method='DELETE', path='/%s' % (topic_path,))

    def topic_publish(self, topic_path, messages):
        """API call:  publish one or more messages to a topic

        See:
        https://cloud.google.com/pubsub/reference/rest/v1/projects.topics/publish

        :type topic_path: string
        :param topic_path: the fully-qualified path of the topic, in format
                           ``projects/<PROJECT>/topics/<TOPIC_NAME>``.

        :type messages: list of dict
        :param messages: messages to be published.

        :rtype: list of string
        :returns: list of opaque IDs for published messages.
        """
        conn = self._connection
        data = {'messages': messages}
        response = conn.api_request(
            method='POST', path='/%s:publish' % (topic_path,), data=data)
        return response['messageIds']

    def topic_list_subscriptions(self, topic_path, page_size=None,
                                 page_token=None):
        """API call:  list subscriptions bound to a topic

        See:
        https://cloud.google.com/pubsub/reference/rest/v1/projects.topics.subscriptions/list

        :type topic_path: string
        :param topic_path: the fully-qualified path of the topic, in format
                           ``projects/<PROJECT>/topics/<TOPIC_NAME>``.

        :type page_size: int
        :param page_size: maximum number of topics to return, If not passed,
                          defaults to a value set by the API.

        :type page_token: string
        :param page_token: opaque marker for the next "page" of topics. If not
                           passed, the API will return the first page of
                           topics.

        :rtype: list of strings
        :returns: fully-qualified names of subscriptions for the supplied
                  topic.
        """
        conn = self._connection
        params = {}

        if page_size is not None:
            params['pageSize'] = page_size

        if page_token is not None:
            params['pageToken'] = page_token

        path = '/%s/subscriptions' % (topic_path,)
        resp = conn.api_request(method='GET', path=path, query_params=params)
        return resp.get('subscriptions', ()), resp.get('nextPageToken')


class _SubscriberAPI(object):
    """Helper mapping subscriber-related APIs.

    :type connection: :class:`Connection`
    :param connection: the connection used to make API requests.
    """

    def __init__(self, connection):
        self._connection = connection

    def list_subscriptions(self, project, page_size=None, page_token=None):
        """API call:  list subscriptions for a given project

        See:
        https://cloud.google.com/pubsub/reference/rest/v1/projects.subscriptions/list

        :type project: string
        :param project: project ID

        :type page_size: int
        :param page_size: maximum number of subscriptions to return, If not
                          passed, defaults to a value set by the API.

        :type page_token: string
        :param page_token: opaque marker for the next "page" of subscriptions.
                           If not passed, the API will return the first page
                           of subscriptions.

        :rtype: tuple, (list, str)
        :returns: list of ``Subscription`` resource dicts, plus a
                  "next page token" string:  if not None, indicates that
                  more subscriptions can be retrieved with another call (pass
                  that value as ``page_token``).
        """
        conn = self._connection
        params = {}

        if page_size is not None:
            params['pageSize'] = page_size

        if page_token is not None:
            params['pageToken'] = page_token

        path = '/projects/%s/subscriptions' % (project,)
        resp = conn.api_request(method='GET', path=path, query_params=params)
        return resp.get('subscriptions', ()), resp.get('nextPageToken')

    def subscription_create(self, subscription_path, topic_path,
                            ack_deadline=None, push_endpoint=None):
        """API call:  create a subscription

        See:
        https://cloud.google.com/pubsub/reference/rest/v1/projects.subscriptions/create

        :type subscription_path: string
        :param subscription_path: the fully-qualified path of the new
                                  subscription, in format
                                  ``projects/<PROJECT>/subscriptions/<SUB_NAME>``.

        :type topic_path: string
        :param topic_path: the fully-qualified path of the topic being
                           subscribed, in format
                           ``projects/<PROJECT>/topics/<TOPIC_NAME>``.

        :type ack_deadline: int, or ``NoneType``
        :param ack_deadline: the deadline (in seconds) by which messages pulled
                            from the back-end must be acknowledged.

        :type push_endpoint: string, or ``NoneType``
        :param push_endpoint: URL to which messages will be pushed by the
                              back-end.  If not set, the application must pull
                              messages.

        :rtype: dict
        :returns: ``Subscription`` resource returned from the API.
        """
        conn = self._connection
        path = '/%s' % (subscription_path,)
        resource = {'topic': topic_path}

        if ack_deadline is not None:
            resource['ackDeadlineSeconds'] = ack_deadline

        if push_endpoint is not None:
            resource['pushConfig'] = {'pushEndpoint': push_endpoint}

        return conn.api_request(method='PUT', path=path, data=resource)

    def subscription_get(self, subscription_path):
        """API call:  retrieve a subscription

        See:
        https://cloud.google.com/pubsub/reference/rest/v1/projects.subscriptions/get

        :type subscription_path: string
        :param subscription_path: the fully-qualified path of the subscription,
                                  in format
                                  ``projects/<PROJECT>/subscriptions/<SUB_NAME>``.

        :rtype: dict
        :returns: ``Subscription`` resource returned from the API.
        """
        conn = self._connection
        path = '/%s' % (subscription_path,)
        return conn.api_request(method='GET', path=path)

    def subscription_delete(self, subscription_path):
        """API call:  delete a subscription

        See:
        https://cloud.google.com/pubsub/reference/rest/v1/projects.subscriptions/delete

        :type subscription_path: string
        :param subscription_path: the fully-qualified path of the subscription,
                                  in format
                                  ``projects/<PROJECT>/subscriptions/<SUB_NAME>``.
        """
        conn = self._connection
        path = '/%s' % (subscription_path,)
        conn.api_request(method='DELETE', path=path)

    def subscription_modify_push_config(self, subscription_path,
                                        push_endpoint):
        """API call:  update push config of a subscription

        See:
        https://cloud.google.com/pubsub/reference/rest/v1/projects.subscriptions/modifyPushConfig

        :type subscription_path: string
        :param subscription_path: the fully-qualified path of the new
                                  subscription, in format
                                  ``projects/<PROJECT>/subscriptions/<SUB_NAME>``.

        :type push_endpoint: string, or ``NoneType``
        :param push_endpoint: URL to which messages will be pushed by the
                              back-end.  If not set, the application must pull
                              messages.
        """
        conn = self._connection
        path = '/%s:modifyPushConfig' % (subscription_path,)
        resource = {'pushConfig': {'pushEndpoint': push_endpoint}}
        conn.api_request(method='POST', path=path, data=resource)

    def subscription_pull(self, subscription_path, return_immediately=False,
                          max_messages=1):
        """API call:  retrieve messages for a subscription

        See:
        https://cloud.google.com/pubsub/reference/rest/v1/projects.subscriptions/modifyPushConfig

        :type subscription_path: string
        :param subscription_path: the fully-qualified path of the new
                                  subscription, in format
                                  ``projects/<PROJECT>/subscriptions/<SUB_NAME>``.

        :type return_immediately: boolean
        :param return_immediately: if True, the back-end returns even if no
                                   messages are available;  if False, the API
                                   call blocks until one or more messages are
                                   available.

        :type max_messages: int
        :param max_messages: the maximum number of messages to return.

        :rtype: list of dict
        :returns:  the ``receivedMessages`` element of the response.
        """
        conn = self._connection
        path = '/%s:pull' % (subscription_path,)
        data = {
            'returnImmediately': return_immediately,
            'maxMessages': max_messages,
        }
        response = conn.api_request(method='POST', path=path, data=data)
        return response.get('receivedMessages', ())

    def subscription_acknowledge(self, subscription_path, ack_ids):
        """API call:  acknowledge retrieved messages

        See:
        https://cloud.google.com/pubsub/reference/rest/v1/projects.subscriptions/modifyPushConfig

        :type subscription_path: string
        :param subscription_path: the fully-qualified path of the new
                                  subscription, in format
                                  ``projects/<PROJECT>/subscriptions/<SUB_NAME>``.

        :type ack_ids: list of string
        :param ack_ids: ack IDs of messages being acknowledged
        """
        conn = self._connection
        path = '/%s:acknowledge' % (subscription_path,)
        data = {
            'ackIds': ack_ids,
        }
        conn.api_request(method='POST', path=path, data=data)

    def subscription_modify_ack_deadline(self, subscription_path, ack_ids,
                                         ack_deadline):
        """API call:  update ack deadline for retrieved messages

        See:
        https://cloud.google.com/pubsub/reference/rest/v1/projects.subscriptions/modifyAckDeadline

        :type subscription_path: string
        :param subscription_path: the fully-qualified path of the new
                                  subscription, in format
                                  ``projects/<PROJECT>/subscriptions/<SUB_NAME>``.

        :type ack_ids: list of string
        :param ack_ids: ack IDs of messages being acknowledged

        :type ack_deadline: int
        :param ack_deadline: the deadline (in seconds) by which messages pulled
                            from the back-end must be acknowledged.
        """
        conn = self._connection
        path = '/%s:modifyAckDeadline' % (subscription_path,)
        data = {
            'ackIds': ack_ids,
            'ackDeadlineSeconds': ack_deadline,
        }
        conn.api_request(method='POST', path=path, data=data)


class _IAMPolicyAPI(object):
    """Helper mapping IAM policy-related APIs.

    :type connection: :class:`Connection`
    :param connection: the connection used to make API requests.
    """

    def __init__(self, connection):
        self._connection = connection

    def get_iam_policy(self, target_path):
        """API call:  fetch the IAM policy for the target

        See:
        https://cloud.google.com/pubsub/reference/rest/v1/projects.topics/getIamPolicy
        https://cloud.google.com/pubsub/reference/rest/v1/projects.subscriptions/getIamPolicy

        :type target_path: string
        :param target_path: the path of the target object.

        :rtype: dict
        :returns: the resource returned by the ``getIamPolicy`` API request.
        """
        conn = self._connection
        path = '/%s:getIamPolicy' % (target_path,)
        return conn.api_request(method='GET', path=path)

    def set_iam_policy(self, target_path, policy):
        """API call:  update the IAM policy for the target

        See:
        https://cloud.google.com/pubsub/reference/rest/v1/projects.topics/setIamPolicy
        https://cloud.google.com/pubsub/reference/rest/v1/projects.subscriptions/setIamPolicy

        :type target_path: string
        :param target_path: the path of the target object.

        :type policy: dict
        :param policy: the new policy resource.

        :rtype: dict
        :returns: the resource returned by the ``setIamPolicy`` API request.
        """
        conn = self._connection
        wrapped = {'policy': policy}
        path = '/%s:setIamPolicy' % (target_path,)
        return conn.api_request(method='POST', path=path, data=wrapped)

    def test_iam_permissions(self, target_path, permissions):
        """API call:  test permissions

        See:
        https://cloud.google.com/pubsub/reference/rest/v1/projects.topics/testIamPermissions
        https://cloud.google.com/pubsub/reference/rest/v1/projects.subscriptions/testIamPermissions

        :type target_path: string
        :param target_path: the path of the target object.

        :type permissions: list of string
        :param permissions: the permissions to check

        :rtype: dict
        :returns: the resource returned by the ``getIamPolicy`` API request.
        """
        conn = self._connection
        wrapped = {'permissions': permissions}
        path = '/%s:testIamPermissions' % (target_path,)
        resp = conn.api_request(method='POST', path=path, data=wrapped)
        return resp.get('permissions', [])
