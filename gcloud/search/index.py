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

"""Define API Indexes."""

from gcloud.search.document import Document


class Index(object):
    """Indexes are containers for documents.

    See:
    https://cloud.google.com/search/reference/rest/v1/indexes

    :type name: string
    :param name: the name of the index

    :type client: :class:`gcloud.dns.client.Client`
    :param client: A client which holds credentials and project configuration
                   for the index (which requires a project).
    """

    def __init__(self, name, client):
        self.name = name
        self._client = client
        self._properties = {}

    @classmethod
    def from_api_repr(cls, resource, client):
        """Factory:  construct an index given its API representation

        :type resource: dict
        :param resource: index resource representation returned from the API

        :type client: :class:`gcloud.dns.client.Client`
        :param client: Client which holds credentials and project
                       configuration for the index.

        :rtype: :class:`gcloud.dns.index.Index`
        :returns: Index parsed from ``resource``.
        """
        name = resource.get('indexId')
        if name is None:
            raise KeyError(
                'Resource lacks required identity information: ["indexId"]')
        index = cls(name, client=client)
        index._set_properties(resource)
        return index

    @property
    def project(self):
        """Project bound to the index.

        :rtype: string
        :returns: the project (derived from the client).
        """
        return self._client.project

    @property
    def path(self):
        """URL path for the index's APIs.

        :rtype: string
        :returns: the path based on project and dataste name.
        """
        return '/projects/%s/indexes/%s' % (self.project, self.name)

    def _list_field_names(self, field_type):
        """Helper for 'text_fields', etc.
        """
        fields = self._properties.get('indexedField', {})
        return fields.get(field_type)

    @property
    def text_fields(self):
        """Names of text fields in the index.

        :rtype: list of string, or None
        :returns: names of text fields in the index, or None if no
                  resource information is available.
        """
        return self._list_field_names('textFields')

    @property
    def atom_fields(self):
        """Names of atom fields in the index.

        :rtype: list of string, or None
        :returns: names of atom fields in the index, or None if no
                  resource information is available.
        """
        return self._list_field_names('atomFields')

    @property
    def html_fields(self):
        """Names of html fields in the index.

        :rtype: list of string, or None
        :returns: names of html fields in the index, or None if no
                  resource information is available.
        """
        return self._list_field_names('htmlFields')

    @property
    def date_fields(self):
        """Names of date fields in the index.

        :rtype: list of string, or None
        :returns: names of date fields in the index, or None if no
                  resource information is available.
        """
        return self._list_field_names('dateFields')

    @property
    def number_fields(self):
        """Names of number fields in the index.

        :rtype: list of string, or None
        :returns: names of number fields in the index, or None if no
                  resource information is available.
        """
        return self._list_field_names('numberFields')

    @property
    def geo_fields(self):
        """Names of geo fields in the index.

        :rtype: list of string, or None
        :returns: names of geo fields in the index, or None if no
                  resource information is available.
        """
        return self._list_field_names('geoFields')

    def _set_properties(self, api_response):
        """Update properties from resource in body of ``api_response``

        :type api_response: httplib2.Response
        :param api_response: response returned from an API call
        """
        self._properties.clear()
        self._properties.update(api_response)

    def list_documents(self, max_results=None, page_token=None,
                       view=None):
        """List documents created within this index.

        See:
        https://cloud.google.com/search/reference/rest/v1/projects/indexes/documents/list

        :type max_results: int
        :param max_results: maximum number of indexes to return, If not
                            passed, defaults to a value set by the API.

        :type page_token: string
        :param page_token: opaque marker for the next "page" of indexes. If
                           not passed, the API will return the first page of
                           indexes.

        :type view: string
        :param view: One of 'ID_ONLY' (return only the document ID; the
                     default) or 'FULL' (return the full resource
                     representation for the document, including field
                     values)

        :rtype: tuple, (list, str)
        :returns: list of :class:`gcloud.dns.document.Document`, plus a
                  "next page token" string:  if the token is not None,
                  indicates that more indexes can be retrieved with another
                  call (pass that value as ``page_token``).
        """
        params = {}

        if max_results is not None:
            params['pageSize'] = max_results

        if page_token is not None:
            params['pageToken'] = page_token

        if view is not None:
            params['view'] = view

        path = '%s/documents' % (self.path,)
        connection = self._client.connection
        resp = connection.api_request(method='GET', path=path,
                                      query_params=params)
        indexes = [Document.from_api_repr(resource, self)
                   for resource in resp['documents']]
        return indexes, resp.get('nextPageToken')

    def document(self, name, rank=None):
        """Construct a document bound to this index.

        :type name: string
        :param name: Name of the document.

        :type rank: integer
        :param rank: Rank of the document (defaults to a server-assigned
                     value based on timestamp).

        :rtype: :class:`gcloud.search.document.Document`
        :returns: a new ``Document`` instance
        """
        return Document(name, index=self, rank=rank)

    def search(self,
               query,
               max_results=None,
               page_token=None,
               field_expressions=None,
               order_by=None,
               matched_count_accuracy=None,
               scorer=None,
               scorer_size=None,
               return_fields=None):
        """Search documents created within this index.

        See:
        https://cloud.google.com/search/reference/rest/v1/projects/indexes/search

        :type query: string
        :param query: query string (see https://cloud.google.com/search/query).

        :type max_results: int
        :param max_results: maximum number of indexes to return, If not
                            passed, defaults to a value set by the API.

        :type page_token: string
        :param page_token: opaque marker for the next "page" of indexes. If
                           not passed, the API will return the first page of
                           indexes.

        :type field_expressions: dict, or ``NoneType``
        :param field_expressions: mapping of field name -> expression
                                  for use in 'order_by' or 'return_fields'

        :type order_by: sequence of string, or ``NoneType``
        :param order_by: list of field names (plus optional ' desc' suffix)
                         specifying ordering of results.

        :type matched_count_accuracy: integer or ``NoneType``
        :param matched_count_accuracy: minimum accuracy for matched count
                                       returned

        :type return_fields: sequence of string, or ``NoneType``
        :param return_fields: list of field names to be returned.

        :type scorer: string or ``NoneType``
        :param scorer: name of scorer function (e.g., "generic").

        :type scorer_size: integer or ``NoneType``
        :param scorer_size: max number of top results pass to scorer function.

        :rtype: tuple, (list, str, int)
        :returns: list of :class:`gcloud.dns.document.Document`, plus a
                  "next page token" string, and a "matched count".  If the
                  token is not None, indicates that more indexes can be
                  retrieved with another call (pass that value as
                  ``page_token``).  The "matched count" indicates the total
                  number of documents matching the query string.
        """
        params = {'query': query}

        if max_results is not None:
            params['pageSize'] = max_results

        if page_token is not None:
            params['pageToken'] = page_token

        if field_expressions is not None:
            params['fieldExpressions'] = field_expressions

        if order_by is not None:
            params['orderBy'] = order_by

        if matched_count_accuracy is not None:
            params['matchedCountAccuracy'] = matched_count_accuracy

        if scorer is not None:
            params['scorer'] = scorer

        if scorer_size is not None:
            params['scorerSize'] = scorer_size

        if return_fields is not None:
            params['returnFields'] = return_fields

        path = '%s/search' % (self.path,)
        connection = self._client.connection
        resp = connection.api_request(method='GET', path=path,
                                      query_params=params)
        indexes = [Document.from_api_repr(resource, self)
                   for resource in resp['results']]
        return indexes, resp.get('nextPageToken'), resp.get('matchedCount')
