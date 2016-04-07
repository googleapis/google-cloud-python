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

    def list_topics(self, project, page_size=None, page_token=None):
        """List topics for the project associated with this client.

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
        params = {}

        if page_size is not None:
            params['pageSize'] = page_size

        if page_token is not None:
            params['pageToken'] = page_token

        path = '/projects/%s/topics' % (project,)
        resp = self.api_request(method='GET', path=path, query_params=params)
        return resp.get('topics', ()), resp.get('nextPageToken')

    def list_subscriptions(self, project, page_size=None, page_token=None):
        """List subscriptions for the project associated with this client.

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
        params = {}

        if page_size is not None:
            params['pageSize'] = page_size

        if page_token is not None:
            params['pageToken'] = page_token

        path = '/projects/%s/subscriptions' % (project,)
        resp = self.api_request(method='GET', path=path, query_params=params)
        return resp.get('subscriptions', ()), resp.get('nextPageToken')

    def topic_create(self, topic_path):
        """API call:  create a topic via a PUT request

        See:
        https://cloud.google.com/pubsub/reference/rest/v1/projects.topics/create

        :type topic_path: string
        :param topic_path: the fully-qualfied path of the new topic, in format
                           ``projects/<PROJECT>/topics/<TOPIC_NAME>``.
        """
        return self.api_request(method='PUT', path='/%s' % (topic_path,))

    def topic_get(self, topic_path):
        """API call:  retrieve a topic via a GET request

        See:
        https://cloud.google.com/pubsub/reference/rest/v1/projects.topics/get

        :type topic_path: string
        :param topic_path: the fully-qualfied path of the topic, in format
                           ``projects/<PROJECT>/topics/<TOPIC_NAME>``.
        """
        return self.api_request(method='GET', path='/%s' % (topic_path,))

    def topic_delete(self, topic_path):
        """API call:  delete a topic via a DELETE request

        See:
        https://cloud.google.com/pubsub/reference/rest/v1/projects.topics/delete

        :type topic_path: string
        :param topic_path: the fully-qualfied path of the topic, in format
                           ``projects/<PROJECT>/topics/<TOPIC_NAME>``.
        """
        return self.api_request(method='DELETE', path='/%s' % (topic_path,))

    def topic_publish(self, topic_path, messages):
        """API call:  publish a message to a topic via a POST request

        See:
        https://cloud.google.com/pubsub/reference/rest/v1/projects.topics/publish

        :type topic_path: string
        :param topic_path: the fully-qualfied path of the topic, in format
                           ``projects/<PROJECT>/topics/<TOPIC_NAME>``.

        :type messages: list of dict
        :param messages: messages to be published.
        """
        data = {'messages': messages}
        return self.api_request(
            method='POST', path='/%s:publish' % (topic_path,), data=data)

    def topic_list_subscriptions(self, topic_path, page_size=None,
                                 page_token=None):
        """API call:  list subscriptions bound to a topic via a GET request

        See:
        https://cloud.google.com/pubsub/reference/rest/v1/projects.topics.subscriptions/list

        :type topic_path: string
        :param topic_path: the fully-qualfied path of the topic, in format
                           ``projects/<PROJECT>/topics/<TOPIC_NAME>``.

        :type page_size: int
        :param page_size: maximum number of topics to return, If not passed,
                          defaults to a value set by the API.

        :type page_token: string
        :param page_token: opaque marker for the next "page" of topics. If not
                           passed, the API will return the first page of
                           topics.
        """
        params = {}

        if page_size is not None:
            params['pageSize'] = page_size

        if page_token is not None:
            params['pageToken'] = page_token

        path = '/%s/subscriptions' % (topic_path,)
        resp = self.api_request(method='GET', path=path, query_params=params)
        return resp.get('subscriptions', ()), resp.get('nextPageToken')

    def get_iam_policy(self, target_path):
        """Fetch the IAM policy for the target.

        See:
        https://cloud.google.com/pubsub/reference/rest/v1/projects.topics/getIamPolicy
        https://cloud.google.com/pubsub/reference/rest/v1/projects.subscriptions/getIamPolicy

        :type target_path: string
        :param target_path: the path of the target object.

        :rtype: dict
        :returns: the resource returned by the ``getIamPolicy`` API request.
        """
        return self.api_request(method='GET', path='/%s:getIamPolicy' % (
            target_path,))

    def set_iam_policy(self, target_path, policy):
        """Update the IAM policy for the target.

        See:
        https://cloud.google.com/pubsub/reference/rest/v1/projects.topics/setIamPolicy
        https://cloud.google.com/pubsub/reference/rest/v1/projects.subscriptions/setIamPolicy

        :type target_path: string
        :param target_path: the path of the target object.

        :type policy: dict
        :param policy: the new policy resource.

        :rtype: dict
        :returns: the resource returned by the ``getIamPolicy`` API request.
        """
        wrapped = {'policy': policy}
        return self.api_request(method='POST', path='/%s:setIamPolicy' % (
            target_path,), data=wrapped)

    def test_iam_permissions(self, target_path, permissions):
        """Update the IAM policy for the target.

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
        wrapped = {'permissions': permissions}
        path = '/%s:testIamPermissions' % (target_path,)
        resp = self.api_request(method='POST', path=path, data=wrapped)
        return resp.get('permissions', [])

    def subscription_create(self, subscription_path, topic_path,
                            ack_deadline=None, push_endpoint=None):
        """API call:  create a subscription via a PUT request

        See:
        https://cloud.google.com/pubsub/reference/rest/v1/projects.subscriptions/create

        :type subscription_path: string
        :param subscription_path: the fully-qualfied path of the new
                                  subscription, in format
                                  ``projects/<PROJECT>/subscriptions/<TOPIC_NAME>``.

        :type topic_path: string
        :param topic_path: the fully-qualfied path of the topic being
                           subscribed, in format
                           ``projects/<PROJECT>/topics/<TOPIC_NAME>``.

        :type ack_deadline: int, or ``NoneType``
        :param ack_deadline: the deadline (in seconds) by which messages pulled
                            from the back-end must be acknowledged.

        :type push_endpoint: string, or ``NoneType``
        :param push_endpoint: URL to which messages will be pushed by the
                              back-end.  If not set, the application must pull
                              messages.
        """
        path = '/%s' % (subscription_path,)
        resource = {'topic': topic_path}

        if ack_deadline is not None:
            resource['ackDeadlineSeconds'] = ack_deadline

        if push_endpoint is not None:
            resource['pushConfig'] = {'pushEndpoint': push_endpoint}

        return self.api_request(method='PUT', path=path, data=resource)

    def subscription_get(self, subscription_path):
        """API call:  retrieve a subscription via a GET request

        See:
        https://cloud.google.com/pubsub/reference/rest/v1/projects.subscriptions/get

        :type subscription_path: string
        :param subscription_path: the fully-qualfied path of the subscription,
                                  in format
                                  ``projects/<PROJECT>/subscriptions/<SUB_NAME>``.
        """
        path = '/%s' % (subscription_path,)
        return self.api_request(method='GET', path=path)

    def subscription_delete(self, subscription_path):
        """API call:  delete a subscription via a DELETE request

        See:
        https://cloud.google.com/pubsub/reference/rest/v1/projects.subscriptions/delete

        :type subscription_path: string
        :param subscription_path: the fully-qualfied path of the subscription,
                                  in format
                                  ``projects/<PROJECT>/subscriptions/<SUB_NAME>``.
        """
        path = '/%s' % (subscription_path,)
        return self.api_request(method='DELETE', path=path)

    def subscription_modify_push_config(self, subscription_path,
                                        push_endpoint):
        """API call:  update push config of a subscription via a POST request

        See:
        https://cloud.google.com/pubsub/reference/rest/v1/projects.subscriptions/modifyPushConfig

        :type subscription_path: string
        :param subscription_path: the fully-qualfied path of the new
                                  subscription, in format
                                  ``projects/<PROJECT>/subscriptions/<TOPIC_NAME>``.
        :type push_endpoint: string, or ``NoneType``
        :param push_endpoint: URL to which messages will be pushed by the
                              back-end.  If not set, the application must pull
                              messages.
        """
        path = '/%s:modifyPushConfig' % (subscription_path,)
        resource = {'pushConfig': {'pushEndpoint': push_endpoint}}
        return self.api_request(method='POST', path=path, data=resource)
