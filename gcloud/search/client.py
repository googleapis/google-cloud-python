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

"""Client for interacting with the Cloud Search API."""


from gcloud.client import JSONClient
from gcloud.exceptions import NotFound
from gcloud.iterator import Iterator
from gcloud.search.connection import Connection
from gcloud.search.index import Index


class Client(JSONClient):
    """Client to bundle configuration needed for API requests."""

    _connection_class = Connection

    def list_indexes(self, page_size=None):
        """List topics for the project associated with this client.

        See:
        https://cloud.google.com/search/reference/rest/v1/projects/indexes/list

        :type page_size: int
        :param page_size: maximum number of indexes to return, If not passed,
                          defaults to a value set by the API.

        :rtype: :class:`gcloud.iterator.Iterator`
        :returns: an :class:`gcloud.iterator.Iterator` of
                  :class:`gcloud.search.index.Index`
        """
        params = {}

        if page_size is not None:
            params['pageSize'] = page_size

        path = '/projects/%s/indexes' % (self.project,)

        client = self

        class IndexIterator(Iterator):
            """An iterator over a list of Index resources."""

            def get_items_from_response(self, response):
                """Get :class:`gcloud.search.index.Index` items from response.

                :type response: dict
                :param response: The JSON API response for a page of indexes.
                """
                for resource in response.get('indexes', []):
                    item = Index.from_api_repr(resource, client=client)
                    yield item

        return IndexIterator(connection=self.connection, extra_params=params,
                             path=path)

    def index(self, index_id):
        """Creates an index bound to the current client.

        :type index_id: string
        :param index_id: the ID of the index to be constructed.

        :rtype: :class:`gcloud.search.index.Index`
        :returns: the index created with the current client.
        """
        return Index(index_id=index_id, client=self)

    def get_index(self, index_id):
        """Retrieves an index from the Cloud Search API.

        :type index_id: string
        :param index_id: the ID of the index to be retrieved.

        :rtype: :class:`gcloud.search.index.Index`
        :returns: the index retrieved via the current client or ``None`` if
                  the index with that ID doesn't exist.
        """
        try:
            index = self.index(index_id)
            index.reload()
        except NotFound:
            index = None
        return index
