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

"""Client for interacting with the Google Cloud search API."""


from gcloud.client import JSONClient
from gcloud.search.connection import Connection
from gcloud.search.index import Index


class Client(JSONClient):
    """Client to bundle configuration needed for API requests.

    :type project: string
    :param project: the project which the client acts on behalf of. Will be
                    passed when creating a zone.  If not passed,
                    falls back to the default inferred from the environment.

    :type credentials: :class:`oauth2client.client.OAuth2Credentials` or
                       :class:`NoneType`
    :param credentials: The OAuth2 Credentials to use for the connection
                        owned by this client. If not passed (and if no ``http``
                        object is passed), falls back to the default inferred
                        from the environment.

    :type http: :class:`httplib2.Http` or class that defines ``request()``.
    :param http: An optional HTTP object to make requests. If not passed, an
                 ``http`` object is created that is bound to the
                 ``credentials`` for the current object.
    """

    _connection_class = Connection

    def list_indexes(self, max_results=None, page_token=None,
                     view=None, prefix=None):
        """List zones for the project associated with this client.

        See:
        https://cloud.google.com/search/reference/rest/v1/indexes/list

        :type max_results: int
        :param max_results: maximum number of zones to return, If not
                            passed, defaults to a value set by the API.

        :type page_token: string
        :param page_token: opaque marker for the next "page" of zones. If
                           not passed, the API will return the first page of
                           zones.

        :type view: string
        :param view: One of 'ID_ONLY' (return only the index ID; the default)
                     or 'FULL' (return information on indexed fields).

        :type prefix: string
        :param prefix: return only indexes whose ID starts with ``prefix``.

        :rtype: tuple, (list, str)
        :returns: list of :class:`gcloud.dns.index.Index`, plus a
                  "next page token" string:  if the token is not None,
                  indicates that more zones can be retrieved with another
                  call (pass that value as ``page_token``).
        """
        params = {}

        if max_results is not None:
            params['pageSize'] = max_results

        if page_token is not None:
            params['pageToken'] = page_token

        if view is not None:
            params['view'] = view

        if prefix is not None:
            params['indexNamePrefix'] = prefix

        path = '/projects/%s/indexes' % (self.project,)
        resp = self.connection.api_request(method='GET', path=path,
                                           query_params=params)
        zones = [Index.from_api_repr(resource, self)
                 for resource in resp['indexes']]
        return zones, resp.get('nextPageToken')

    def index(self, name):
        """Construct an index bound to this client.

        :type name: string
        :param name: Name of the zone.

        :rtype: :class:`gcloud.search.index.Index`
        :returns: a new ``Index`` instance
        """
        return Index(name, client=self)
