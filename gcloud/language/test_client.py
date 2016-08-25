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

import unittest


class TestClient(unittest.TestCase):

    def _getTargetClass(self):
        from gcloud.language.client import Client
        return Client

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor(self):
        from gcloud.language.connection import Connection

        creds = _Credentials()
        http = object()
        client = self._makeOne(credentials=creds, http=http)
        self.assertIsInstance(client.connection, Connection)
        self.assertTrue(client.connection.credentials is creds)
        self.assertTrue(client.connection.http is http)

    def test_document_from_text_factory(self):
        from gcloud.language.document import Document

        creds = _Credentials()
        client = self._makeOne(credentials=creds, http=object())

        content = 'abc'
        language = 'es'
        document = client.document_from_text(content, language=language)
        self.assertIsInstance(document, Document)
        self.assertIs(document.client, client)
        self.assertEqual(document.content, content)
        # Test the default arg.
        self.assertEqual(document.doc_type, Document.PLAIN_TEXT)
        # Test the kwargs as well.
        self.assertEqual(document.language, language)

    def test_document_from_text_factory_failure(self):
        creds = _Credentials()
        client = self._makeOne(credentials=creds, http=object())

        with self.assertRaises(TypeError):
            client.document_from_text('abc', doc_type='foo')

    def test_document_from_html_factory(self):
        from gcloud.language.document import Document

        creds = _Credentials()
        client = self._makeOne(credentials=creds, http=object())

        content = '<html>abc</html>'
        language = 'ja'
        document = client.document_from_html(content, language=language)
        self.assertIsInstance(document, Document)
        self.assertIs(document.client, client)
        self.assertEqual(document.content, content)
        # Test the default arg.
        self.assertEqual(document.doc_type, Document.HTML)
        # Test the kwargs as well.
        self.assertEqual(document.language, language)

    def test_document_from_html_factory_failure(self):
        creds = _Credentials()
        client = self._makeOne(credentials=creds, http=object())

        with self.assertRaises(TypeError):
            client.document_from_html('abc', doc_type='foo')

    def test_document_from_url_factory(self):
        from gcloud.language.document import Document

        creds = _Credentials()
        client = self._makeOne(credentials=creds, http=object())

        gcs_url = 'gs://my-text-bucket/sentiment-me.txt'
        document = client.document_from_url(gcs_url)
        self.assertIsInstance(document, Document)
        self.assertIs(document.client, client)
        self.assertIsNone(document.content)
        self.assertEqual(document.gcs_url, gcs_url)
        self.assertEqual(document.doc_type, Document.PLAIN_TEXT)

    def test_document_from_url_factory_explicit(self):
        from gcloud.language.document import Document
        from gcloud.language.document import Encoding

        creds = _Credentials()
        client = self._makeOne(credentials=creds, http=object())

        encoding = Encoding.UTF32
        gcs_url = 'gs://my-text-bucket/sentiment-me.txt'
        document = client.document_from_url(gcs_url, doc_type=Document.HTML,
                                            encoding=encoding)
        self.assertIsInstance(document, Document)
        self.assertIs(document.client, client)
        self.assertIsNone(document.content)
        self.assertEqual(document.gcs_url, gcs_url)
        self.assertEqual(document.doc_type, Document.HTML)
        self.assertEqual(document.encoding, encoding)


class _Credentials(object):

    _scopes = None

    @staticmethod
    def create_scoped_required():
        return True

    def create_scoped(self, scope):
        self._scopes = scope
        return self
