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

"""gcloud pubsub client for interacting with API."""


from gcloud._helpers import _get_production_project
from gcloud.credentials import get_credentials
from gcloud.credentials import get_for_service_account_json
from gcloud.credentials import get_for_service_account_p12
from gcloud.pubsub.connection import Connection
from gcloud.pubsub.subscription import Subscription
from gcloud.pubsub.topic import Topic


class Client(object):
    """Client to bundle configuration needed for API requests.

    :type project: string
    :param project: the project which the client acts on behalf of. Will be
                    passed when creating a topic.  If not passed,
                    falls back to the default inferred from the environment.

    :type credentials: :class:`oauth2client.client.OAuth2Credentials` or
                       :class:`NoneType`
    :param credentials: The OAuth2 Credentials to use for the connection
                        owned by this client. If not passed (and if no ``http``
                        object is passed), falls back to the default inferred
                        from the environment.

    :type http: :class:`httplib2.Http` or class that defines ``request()``.
    :param http: An optional HTTP object to make requests.

    :raises: :class:`ValueError` if the project is neither passed in nor
             set in the environment.
    """
    def __init__(self, project=None, credentials=None, http=None):
        if project is None:
            project = _get_production_project()
        if project is None:
            raise ValueError('Project was not passed and could not be '
                             'determined from the environment.')
        self.project = project

        if credentials is None and http is None:
            credentials = get_credentials()
        self.connection = Connection(credentials=credentials, http=http)

    @classmethod
    def with_service_account_json(cls, json_credentials_path, project=None):
        """Factory to retrieve JSON credentials while creating client.

        :type json_credentials_path: string
        :param json_credentials_path: The path to a private key file (this file
                                      was given to you when you created the
                                      service account). This file must contain
                                      a JSON object with a private key and
                                      other credentials information (downloaded
                                      from the Google APIs console).

        :type project: string
        :param project: the project which the client acts on behalf of. Will be
                        passed when creating a topic.  If not passed, falls
                        back to the default inferred from the environment.

        :rtype: :class:`gcloud.pubsub.client.Client`
        :returns: The client created with the retrieved JSON credentials.
        """
        credentials = get_for_service_account_json(json_credentials_path)
        return cls(project=project, credentials=credentials)

    @classmethod
    def with_service_account_p12(cls, client_email, private_key_path,
                                 project=None):
        """Factory to retrieve P12 credentials while creating client.

        .. note::
          Unless you have an explicit reason to use a PKCS12 key for your
          service account, we recommend using a JSON key.

        :type client_email: string
        :param client_email: The e-mail attached to the service account.

        :type private_key_path: string
        :param private_key_path: The path to a private key file (this file was
                                 given to you when you created the service
                                 account). This file must be in P12 format.

        :type project: string
        :param project: the project which the client acts on behalf of. Will be
                        passed when creating a topic.  If not passed, falls
                        back to the default inferred from the environment.

        :rtype: :class:`gcloud.pubsub.client.Client`
        :returns: The client created with the retrieved P12 credentials.
        """
        credentials = get_for_service_account_p12(client_email,
                                                  private_key_path)
        return cls(project=project, credentials=credentials)

    def list_topics(self, page_size=None, page_token=None):
        """List topics for the project associated with this client.

        See:
        https://cloud.google.com/pubsub/reference/rest/v1beta2/projects/topics/list

        :type page_size: int
        :param page_size: maximum number of topics to return, If not passed,
                          defaults to a value set by the API.

        :type page_token: string
        :param page_token: opaque marker for the next "page" of topics. If not
                           passed, the API will return the first page of
                           topics.

        :rtype: tuple, (list, str)
        :returns: list of :class:`gcloud.pubsub.topic.Topic`, plus a
                  "next page token" string:  if not None, indicates that
                  more topics can be retrieved with another call (pass that
                  value as ``page_token``).
        """
        params = {}

        if page_size is not None:
            params['pageSize'] = page_size

        if page_token is not None:
            params['pageToken'] = page_token

        path = '/projects/%s/topics' % (self.project,)
        resp = self.connection.api_request(method='GET', path=path,
                                           query_params=params)
        topics = [Topic.from_api_repr(resource) for resource in resp['topics']]
        return topics, resp.get('nextPageToken')

    def list_subscriptions(self, page_size=None, page_token=None,
                           topic_name=None):
        """List subscriptions for the project associated with this client.

        See:
        https://cloud.google.com/pubsub/reference/rest/v1beta2/projects/topics/list

        and (where ``topic_name`` is passed):
        https://cloud.google.com/pubsub/reference/rest/v1beta2/projects/topics/subscriptions/list

        :type page_size: int
        :param page_size: maximum number of topics to return, If not passed,
                          defaults to a value set by the API.

        :type page_token: string
        :param page_token: opaque marker for the next "page" of topics. If not
                           passed, the API will return the first page of
                           topics.

        :type topic_name: string
        :param topic_name: limit results to subscriptions bound to the given
                           topic.

        :rtype: tuple, (list, str)
        :returns: list of :class:`gcloud.pubsub.subscription.Subscription`,
                  plus a "next page token" string:  if not None, indicates that
                  more topics can be retrieved with another call (pass that
                  value as ``page_token``).
        """
        params = {}

        if page_size is not None:
            params['pageSize'] = page_size

        if page_token is not None:
            params['pageToken'] = page_token

        if topic_name is None:
            path = '/projects/%s/subscriptions' % (self.project,)
        else:
            path = '/projects/%s/topics/%s/subscriptions' % (self.project,
                                                             topic_name)

        resp = self.connection.api_request(method='GET', path=path,
                                           query_params=params)
        topics = {}
        subscriptions = [Subscription.from_api_repr(resource, topics=topics)
                         for resource in resp['subscriptions']]
        return subscriptions, resp.get('nextPageToken')
