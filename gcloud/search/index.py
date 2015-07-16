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

"""Define Indexes for the Cloud Search API."""

from gcloud.exceptions import NotFound


class Index(object):
    """Indexes are sets of documents that you can search over.

    To create a new index::

        >>> from gcloud import search
        >>> client = search.Client()
        >>> index = client.index('my-new-index')
        >>> index.create()

    To get an existing index::

        >>> from gcloud import search
        >>> client = search.Client()
        >>> index = client.get_index('my-existing-index')
        >>> print index
        <Index: my-existing-index>

    See:
    https://cloud.google.com/search/reference/rest/v1/projects/indexes/list#google.cloudsearch.v1.IndexInfo

    :type index_id: string
    :param index_id: the unique ID of the index.

    :type client: :class:`gcloud.search.client.Client`
    :param client: Client which holds credentials and project
                   configuration.
    """
    def __init__(self, client, index_id):
        self.client = client
        self.index_id = index_id

    def __repr__(self):
        return '<Index: %s>' % (self.index_id,)

    @classmethod
    def from_api_repr(cls, resource, client):
        """Factory: construct an index given its API representation.

        :type resource: dict
        :param resource: the resource representation returned from the API

        :type client: :class:`gcloud.pubsub.client.Client`
        :param client: Client which holds credentials and project
                       configuration for the index.

        :rtype: :class:`gcloud.search.index.Index`
        """
        index = cls(index_id=resource['indexId'], client=client)
        index.set_properties_from_api_repr(resource)
        return index

    def set_properties_from_api_repr(self, resource):
        """Update specific properties from its API representation."""
        pass

    @property
    def project(self):
        """Project bound to the index."""
        return self.client.project

    @property
    def full_name(self):
        """Fully-qualified name."""
        if not self.project:
            raise ValueError('Missing project ID!')
        return 'projects/%s/indexes/%s' % (self.project, self.index_id)

    @property
    def path(self):
        """URL for the index."""
        return '/%s' % (self.full_name)

    def _require_client(self, client=None):
        """Get either a client or raise an exception.

        We need to use this as the various methods could accept a client as a
        parameter, which we need to evaluate. If the client provided is empty
        and there is no client set as an instance variable, we'll raise a
        ValueError.

        :type client: :class:`gcloud.search.client.Client`
        :param client: An optional client to test for existence.
        """
        client = client or self.client
        if not client:
            raise ValueError('Missing client.')
        return client

    def create(self, client=None):
        """API call: create the index via a ``POST`` request.

        Example::

            >>> from gcloud import search
            >>> client = search.Client()
            >>> index = client.index('my-new-index')
            >>> index.create()

        See
        https://cloud.google.com/search/reference/rest/v1/projects/indexes/create

        :type client: :class:`gcloud.search.client.Client` or None
        :param client: the client to use. If not passed, falls back to
                       the ``client`` attribute.
        """
        # Right now this is a no-op as indexes are implicitly created.
        # Later, this will be a PUT request to the API.
        # client = self._require_client(client=client)
        # resp = client.connection.api_request(method='POST', path=self.path)
        # self.set_properties_from_api_repr(resource=resp)

    def reload(self, client=None):
        """API call: reload the index via a ``GET`` request.

        This method will reload the freshest metadata for an index.

        .. warning::

            This will overwrite any local changes you've made and not saved!

        Example::

            >>> from gcloud import search
            >>> client = search.Client()
            >>> index = client.get_index('my-existing-index')
            >>> index.name = 'Locally changed name'
            >>> print index
            <Index: Locally changed name (my-existing-index)>
            >>> index.reload()
            >>> print index
            <Index: Purple Spaceship (my-existing-index)>

        See
        https://cloud.google.com/search/reference/rest/v1/projects/indexes/get

        :type client: :class:`gcloud.search.client.Client` or None
        :param client: the client to use. If not passed, falls back to
                       the ``client`` attribute.
        """
        # client = self._require_client(client=client)

        # We assume the index exists. If it doesn't it will raise a NotFound
        # exception.
        # Right now this is a no-op, as there's no extra data with an index.
        # resp = client.connection.api_request(method='GET', path=self.path)
        # self.set_properties_from_api_repr(resource=resp)

    def update(self, client=None):
        """API call: update the index via a ``PUT`` request.

        Example::

            >>> from gcloud import search
            >>> client = search.Client()
            >>> index = client.get_index('my-existing-index')
            >>> index.name = 'New Purple Spaceship'
            >>> index.labels['environment'] = 'prod'
            >>> index.update()

        See
        https://cloud.google.com/search/reference/rest/v1/projects/indexes/update

        :type client: :class:`gcloud.search.client.Client` or None
        :param client: the client to use. If not passed, falls back to
                       the ``client`` attribute.
        """
        client = self._require_client(client=client)

        # Right now this is a no-op, as indexes have no extra data.
        # data = {'name': self.name, 'labels': self.labels}
        # resp = client.connection.api_request(method='PUT', path=self.path,
        #                                      data=data)
        # self.set_properties_from_api_repr(resp)

    def exists(self, client=None):
        """API call: test the existence of an index via a ``GET`` request.

        Example::

            >>> from gcloud import search
            >>> client = search.Client()
            >>> index = client.index('missing-index-id')
            >>> index.exists()
            False

        You can also use the
        :func:`gcloud.search.client.Client.get_index`
        method to check whether an index exists, as it will return ``None``
        if the index doesn't exist::

            >>> from gcloud import search
            >>> client = search.Client()
            >>> print client.get_index('missing-index-id')
            None

        See
        https://cloud.google.com/search/reference/rest/v1/projects/indexes/get

        :type client: :class:`gcloud.search.client.Client` or None
        :param client: the client to use.  If not passed, falls back to
                       the ``client`` attribute.
        """
        # Currently there is no way to do this, so this is a no-op.
        # client = self._require_client(client=client)
        #
        # try:
        #     client.connection.api_request(method='GET', path=self.path)
        # except NotFound:
        #     return False
        # else:
        #     return True

    def delete(self, client=None, reload=True):
        """API call: delete the index via a ``DELETE`` request.

        See:
        https://cloud.google.com/search/reference/rest/v1/projects/indexes/delete

        This actually changes the status (``<TBD>``) from ``ACTIVE``
        to ``DELETING``.
        Later (it's not specified when), the index will move into the
        ``DELETE_IN_PROGRESS`` state, which means the deleting has actually
        begun.

        Example::

            >>> from gcloud import search
            >>> client = search.Client()
            >>> index = client.get_index('existing-index-id')
            >>> index.delete()

        :type client: :class:`gcloud.search.client.Client` or None
        :param client: the client to use.  If not passed,
                       falls back to the ``client`` attribute.

        :type reload: bool
        :param reload: Whether to reload the index with the latest state.
                       Default: ``True``.
        """
        # This currently is not possible.
        # client = self._require_client(client)
        # client.connection.api_request(method='DELETE', path=self.path)
        #
        # if reload:
        #     self.reload()

    def document(self, document_id):
        """Get a document instance without making an API call.

        :type document_id: string
        :param document_id: The unique ID for the document.

        :rtype: :class:`gcloud.search.document.Document`
        """
        pass

    def get_document(self, document_id, client=None):
        """API call: Retrieve a document via a ``GET`` request.

        See:
        https://cloud.google.com/search/reference/rest/v1/projects/indexes/documents/get

        :type document_id: string
        :param document_id: The unique ID for the document.

        :type client: :class:`gcloud.search.client.Client`
        :param client: Client which holds credentials and project
                       configuration for the index.

        :rtype: :class:`gcloud.search.document.Document`
        """
        client = self._require_client(client=client)
        document = self.document(document_id)
        try:
            document.reload()
        except NotFound:
            document = None
        return document

    def add_document(self, document, client=None):
        """API call: Add a document to this index.

        :type document: :class:`gcloud.search.document.Document`
        :param document: The document to add to the index.

        :type client: :class:`gcloud.search.client.Client`
        :param client: Client which holds credentials and project
                       configuration for the index.
        """
        self.add_document([document], client=client)

    def add_documents(self, documents, client=None):
        """API call: Add a list of documents to this index.

        :type documents: iterable of :class:`gcloud.search.document.Document`
        :param documents: The documents to add to the index.

        :type client: :class:`gcloud.search.client.Client`
        :param client: Client which holds credentials and project
                       configuration for the index.
        """
        pass

    def query(self):
        """Execute a query over this index."""
        pass
