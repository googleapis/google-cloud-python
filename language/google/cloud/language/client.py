# Copyright 2016 Google Inc.
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

"""Basic client for Google Cloud Natural Language API."""

import functools
import warnings

from google.cloud import client as client_module

from google.cloud.language._http import Connection
from google.cloud.language.document import Document


class Client(client_module.Client):
    """Client to bundle configuration needed for API requests.

    :type credentials: :class:`~google.auth.credentials.Credentials`
    :param credentials: (Optional) The OAuth2 Credentials to use for this
                        client. If not passed (and if no ``http`` object is
                        passed), falls back to the default inferred from the
                        environment.

    :type http: :class:`~httplib2.Http`
    :param http: (Optional) HTTP object to make requests. Can be any object
                 that defines ``request()`` with the same interface as
                 :meth:`~httplib2.Http.request`. If not passed, an
                 ``http`` object is created that is bound to the
                 ``credentials`` for the current object.
    """

    SCOPE = ('https://www.googleapis.com/auth/cloud-platform',)
    """The scopes required for authenticating as an API consumer."""

    def __init__(self, credentials=None, http=None):
        super(Client, self).__init__(
            credentials=credentials, http=http)
        self._connection = Connection(self)

    def document_from_text(self, content, **kwargs):
        """Create a plain text document bound to this client.

        :type content: str
        :param content: The document plain text content.

        :type kwargs: dict
        :param kwargs: Remaining keyword arguments to be passed along to the
                       :class:`~google.cloud.language.document.Document`
                       constructor.

        :rtype: :class:`~google.cloud.language.document.Document`
        :returns: A plain-text document bound to this client.
        :raises: :class:`~exceptions.TypeError` if ``doc_type`` is passed as a
                 keyword argument.
        """
        if 'doc_type' in kwargs:
            raise TypeError('Cannot pass doc_type')
        return Document(self, content=content,
                        doc_type=Document.PLAIN_TEXT, **kwargs)

    def document_from_html(self, content, **kwargs):
        """Create an HTML document bound to this client.

        :type content: str
        :param content: The document HTML text content.

        :type kwargs: dict
        :param kwargs: Remaining keyword arguments to be passed along to the
                       :class:`~google.cloud.language.document.Document`
                       constructor.

        :rtype: :class:`~google.cloud.language.document.Document`
        :returns: An HTML document bound to this client.
        :raises: :class:`~exceptions.TypeError` if ``doc_type`` is passed as a
                 keyword argument.
        """
        if 'doc_type' in kwargs:
            raise TypeError('Cannot pass doc_type')
        return Document(self, content=content,
                        doc_type=Document.HTML, **kwargs)

    def document_from_gcs_url(self, gcs_url,
                              doc_type=Document.PLAIN_TEXT, **kwargs):
        """Create a Cloud Storage document bound to this client.

        :type gcs_url: str
        :param gcs_url: The URL of the Google Cloud Storage object
                        holding the content. Of the form
                        ``gs://{bucket}/{blob-name}``.

        :type doc_type: str
        :param doc_type: (Optional) The type of text in the document.
                         Defaults to plain text. Can also be specified
                         as HTML via :attr:`~.Document.HTML`.

        :type kwargs: dict
        :param kwargs: Remaining keyword arguments to be passed along to the
                       :class:`~google.cloud.language.document.Document`
                       constructor.

        :rtype: :class:`~google.cloud.language.document.Document`
        :returns: A document bound to this client.
        """
        return Document(self, gcs_url=gcs_url, doc_type=doc_type, **kwargs)

    @functools.wraps(document_from_gcs_url)
    def document_from_url(self, *args, **kwargs):
        """Deprecated equivalent to document_from_gcs_url.

        DEPRECATED: 2017-02-06
        """
        warnings.warn('The `document_from_url` method is deprecated; use '
                      '`document_from_gcs_url` instead.', DeprecationWarning)
        return self.document_from_gcs_url(*args, **kwargs)
