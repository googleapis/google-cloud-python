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

"""Define API functions (not bound to classes)."""

from gcloud._helpers import get_default_project
from gcloud.pubsub._implicit_environ import get_default_connection
from gcloud.pubsub.topic import Topic


def list_topics(page_size=None, page_token=None,
                project=None, connection=None):
    """List topics for a given project.

    See:
    https://cloud.google.com/pubsub/reference/rest/v1beta2/projects/topics/list

    :type page_size: int
    :param page_size: maximum number of topics to return, If not passed,
                      defaults to a value set by the API.

    :type page_token: string
    :param page_token: opaque marker for the next "page" of topics. If not
                       passed, the API will return the first page of topics.

    :type project: string
    :param project: project ID to query.  If not passed, defaults to the
                    project ID inferred from the environment.

    :type connection: :class:`gcloud.pubsub.connection.Connection`
    :param connection: connection to use for the query.  If not passed,
                       defaults to the connection inferred from the
                       environment.

    :rtype: tuple, (list, str)
    :returns: list of :class:`gcloud.pubsub.topic.Topic`, plus a
              "next page token" string:  if not None, indicates that
              more topics can be retrieved with another call (pass that
              value as ``page_token``).
    """
    if project is None:
        project = get_default_project()

    if connection is None:
        connection = get_default_connection()

    params = {}

    if page_size is not None:
        params['pageSize'] = page_size

    if page_token is not None:
        params['pageToken'] = page_token

    path = '/projects/%s/topics' % project
    resp = connection.api_request(method='GET', path=path, query_params=params)
    topics = []
    for full_name in [topic['name'] for topic in resp['topics']]:
        _, t_project, _, name = full_name.split('/')
        topics.append(Topic(name, t_project, connection))
    return topics, resp.get('nextPageToken')


def list_subscriptions(page_size=None, page_token=None, topic_name=None,
                       project=None, connection=None):
    """List subscriptions for a given project.

    See:
    https://cloud.google.com/pubsub/reference/rest/v1beta2/projects/topics/list

    and (where ``topic_name`` is passed):
    https://cloud.google.com/pubsub/reference/rest/v1beta2/projects/topics/subscriptions/list

    :type page_size: int
    :param page_size: maximum number of topics to return, If not passed,
                      defaults to a value set by the API.

    :type page_token: string
    :param page_token: opaque marker for the next "page" of topics. If not
                       passed, the API will return the first page of topics.

    :type topic_name: string
    :param topic_name: limit results to subscriptions bound to the given topic.

    :type project: string
    :param project: project ID to query.  If not passed, defaults to the
                    project ID inferred from the environment.

    :type connection: :class:`gcloud.pubsub.connection.Connection`
    :param connection: connection to use for the query.  If not passed,
                       defaults to the connection inferred from the
                       environment.

    :rtype: dict
    :returns: keys include ``subscriptions`` (a list of subscription mappings)
              and ``nextPageToken`` (a string:  if non-empty, indicates that
              more topics can be retrieved with another call (pass that
              value as ``page_token``).
    """
    if project is None:
        project = get_default_project()

    if connection is None:
        connection = get_default_connection()

    params = {}

    if page_size is not None:
        params['pageSize'] = page_size

    if page_token is not None:
        params['pageToken'] = page_token

    if topic_name is None:
        path = '/projects/%s/subscriptions' % project
    else:
        path = '/projects/%s/topics/%s/subscriptions' % (project, topic_name)

    return connection.api_request(method='GET', path=path, query_params=params)
