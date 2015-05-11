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

"""Define a Cloud Search Document."""


class Document(object):
    """Documents are the entities that are searchable via the Cloud Search API

    See:
    https://cloud.google.com/search/reference/rest/v1/projects/indexes/documents#resource_representation.google.cloudsearch.v1.Document

    :type document_id: string
    :param document_id: the id of the document

    :type fields: list of :class:`gcloud.search.field.Field`
    :param fields: the fields attached to the document

    :type client: :class:`gcloud.search.client.Client`
    :param client: Client which holds credentials and project
                   configuration.

    :type index: :class:`gcloud.search.index.Index`
    :param index: the index that the document belongs to.
    """
    def __init__(self, document_id, fields=None, client=None, index=None):
        self.document_id = document_id
        self.fields = fields or []
        self._client = client
        self.index = index

    @classmethod
    def from_api_repr(cls, resource, client=None):
        """Factory:  construct a document given its API representation

        :type resource: dict
        :param resource: the resource representation returned from the API

        :type client: :class:`gcloud.search.client.Client`
        :param client: Client which holds credentials and project
                       configuration.

        :rtype: :class:`gcloud.search.document.Document`
        :returns: a document parsed from ``resource``.
        """
        return cls(document_id=resource['id'], client=client)

    @property
    def client(self):
        """The client associated with this document.

        This first checks the client set directly, then checks the client set
        on the index. If no client is found, returns ``None``.

        :rtype: :class:`gcloud.search.client.Client` or ``None``
        :returns: The client associated with this document.
        """
        if self._client:
            return self._client
        elif self._index:
            return self._index.client

    @property
    def path(self):
        """URL path for the document's API calls"""
        if not self.index:
            raise ValueError('Missing Index.')
        return '%s/documents/%s' % (self.index.path, self.document_id)

    def _require_client(self, client=None):
        """Get either a client or raise an exception.

        We need to use this as the various methods could accept a client as a
        parameter, which we need to evaluate. If the client provided is empty
        and there is no client set as an instance variable, we'll raise a
        :class:`ValueError`.

        :type client: :class:`gcloud.search.client.Client`
        :param client: An optional client to test for existence.
        """
        client = client or self.client
        if not client:
            raise ValueError('Missing client. You can set the client '
                             'directly on the document, or indirectly on the '
                             'index.')
        return client

    def add_field(self, field):
        """Add a field to this document.

        :type field: :class:`gcloud.search.field.Field`
        :param field: The field to add to the document.
        """
        pass

    def reload(self, client=None):
        """API call: sync this document's data via a GET request.

        See
        https://cloud.google.com/search/reference/rest/v1/projects/indexes/documents

        :type client: :class:`gcloud.search.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current document's index.
        """
        # client = self._require_client(client)
        # data = client.connection.api_request(method='GET', path=self.path)

    def delete(self, client=None):
        """API call: delete the document via a DELETE request.

        See:
        https://cloud.google.com/search/reference/rest/v1/projects/indexes/documents/delete

        :type client: :class:`gcloud.search.client.Client` or ``None``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored.
        """
        client = self._require_client(client)
        client.connection.api_request(method='DELETE', path=self.path)
