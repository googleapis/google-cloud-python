# Copyright 2016 Google Inc. All Rights Reserved.
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


from gcloud.client import JSONClient
from gcloud.language.connection import Connection
from gcloud.language.document import Document


class Client(JSONClient):
    """Client to bundle configuration needed for API requests.

    :type project: str
    :param project: the project which the client acts on behalf of. If not
                    passed, falls back to the default inferred from the
                    environment.

    :type credentials: :class:`~oauth2client.client.OAuth2Credentials`
    :param credentials: (Optional) The OAuth2 Credentials to use for the
                        connection owned by this client. If not passed (and
                        if no ``http`` object is passed), falls back to the
                        default inferred from the environment.

    :type http: :class:`httplib2.Http` or class that defines ``request()``.
    :param http: An optional HTTP object to make requests. If not passed, an
                 ``http`` object is created that is bound to the
                 ``credentials`` for the current object.
    """

    _connection_class = Connection

    def document_from_text(self, content, **kwargs):
        """Create a plain text document bound to this client.

        :type content: str
        :param content: The document plain text content.

        :type kwargs: dict
        :param kwargs: Remaining keyword arguments to be passed along to the
                       :class:`Document` constructor.

        :rtype: :class:`Document`
        :returns: A plain-text document bound to this client.
        :raises: :class:`TypeError` if ``doc_type`` is passed as a
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
                       :class:`Document` constructor.

        :rtype: :class:`Document`
        :returns: An HTML document bound to this client.
        :raises: :class:`TypeError` if ``doc_type`` is passed as a
                 keyword argument.
        """
        if 'doc_type' in kwargs:
            raise TypeError('Cannot pass doc_type')
        return Document(self, content=content,
                        doc_type=Document.HTML, **kwargs)
