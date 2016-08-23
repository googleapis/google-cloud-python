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

"""Definition for Google Cloud Natural Language API documents.

A document is used to hold text to be analyzed and annotated.
"""

from gcloud.language.entity import Entity


DEFAULT_LANGUAGE = 'en-US'
"""Default document language, English."""


class Encoding(object):
    """Document text encoding types."""

    NONE = 'NONE'
    """Unspecified encoding type."""

    UTF8 = 'UTF8'
    """UTF-8 encoding type."""

    UTF16 = 'UTF16'
    """UTF-16 encoding type."""

    UTF32 = 'UTF32'
    """UTF-32 encoding type."""


class Document(object):
    """Document to send to Google Cloud Natural Language API.

    Represents either plain text or HTML, and the content is either
    stored on the document or referred to in a Google Cloud Storage
    object.

    :type client: :class:`~gcloud.language.client.Client`
    :param client: A client which holds credentials and project
                   configuration.

    :type content: str
    :param content: (Optional) The document text content (either plain
                    text or HTML).

    :type gcs_url: str
    :param gcs_url: (Optional) The URL of the Google Cloud Storage object
                    holding the content. Of the form
                    ``gs://{bucket}/{blob-name}``.

    :type doc_type: str
    :param doc_type: (Optional) The type of text in the document.
                     Defaults to plain text. Can be one of
                     :attr:`~.Document.PLAIN_TEXT` or
                     or :attr:`~.Document.HTML`.

    :type language: str
    :param language: (Optional) The language of the document text.
                     Defaults to :data:`DEFAULT_LANGUAGE`.

    :type encoding: str
    :param encoding: (Optional) The encoding of the document text.
                     Defaults to UTF-8. Can be one of
                     :attr:`~.Encoding.UTF8`, :attr:`~.Encoding.UTF16`
                     or :attr:`~.Encoding.UTF32`.

    :raises: :class:`~exceptions.ValueError` both ``content`` and ``gcs_url``
             are specified or if neither are specified.
    """

    TYPE_UNSPECIFIED = 'TYPE_UNSPECIFIED'
    """Unspecified document type."""

    PLAIN_TEXT = 'PLAIN_TEXT'
    """Plain text document type."""

    HTML = 'HTML'
    """HTML document type."""

    def __init__(self, client, content=None, gcs_url=None, doc_type=PLAIN_TEXT,
                 language=DEFAULT_LANGUAGE, encoding=Encoding.UTF8):
        if content is not None and gcs_url is not None:
            raise ValueError('A Document cannot contain both local text and '
                             'a link to text in a Google Cloud Storage object')
        if content is None and gcs_url is None:
            raise ValueError('A Document must contain either local text or a '
                             'link to text in a Google Cloud Storage object')
        self.client = client
        self.content = content
        self.gcs_url = gcs_url
        self.doc_type = doc_type
        self.language = language
        self.encoding = encoding

    def _to_dict(self):
        """Helper to convert the current document into a dictionary.

        To be used when constructing requests.

        :rtype: dict
        :returns: The Document value as a JSON dictionary.
        """
        info = {
            'type': self.doc_type,
            'language': self.language,
        }
        if self.content is not None:
            info['content'] = self.content
        elif self.gcs_url is not None:
            info['gcsContentUri'] = self.gcs_url
        return info

    def analyze_entities(self):
        """Analyze the entities in the current document.

        Finds named entities (currently finds proper names as of August 2016)
        in the text, entity types, salience, mentions for each entity, and
        other properties.

        .. _analyzeEntities: https://cloud.google.com/natural-language/\
                             reference/rest/v1beta1/documents/analyzeEntities

        See `analyzeEntities`_.

        :rtype: list
        :returns: A list of :class:`~.language.entity.Entity` returned from
                  the API.
        """
        data = {
            'document': self._to_dict(),
            'encodingType': self.encoding,
        }
        api_response = self.client.connection.api_request(
            method='POST', path='analyzeEntities', data=data)
        return [Entity.from_api_repr(entity)
                for entity in api_response['entities']]
