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

""" Define API functions (not bound to classes)."""


def list_topics(page_size=None, page_token=None,
                project=None, connection=None):
    """List topics for a given project.

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

    :rtype: dict
    :returns: keys include ``topics`` (a list of topic mappings) and
              ``nextPageToken`` (a string:  if non-empty, indicates that
              more topics can be retrieved with another call (pass that
              value as ``page_token``).
    """
    params = {}

    if page_size is not None:
        params['pageSize'] = page_size

    if page_token is not None:
        params['pageToken'] = page_token

    path = '/projects/%s/topics' % project
    return connection.api_request(method='GET', path=path, query_params=params)
