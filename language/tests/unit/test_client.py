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

import unittest

import mock


def make_mock_credentials():
    from google.auth import credentials

    credentials = mock.Mock(spec=credentials.Credentials)
    return credentials


class TestClient(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.language.client import Client

        return Client

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor(self):
        from google.cloud.language._http import Connection

        creds = make_mock_credentials()
        http = object()
        client = self._make_one(credentials=creds, http=http)
        self.assertIsInstance(client._connection, Connection)
        self.assertIs(client._connection.credentials, creds)
        self.assertIs(client._connection.http, http)

    def test_document_from_text_factory(self):
        from google.cloud.language.document import Document

        creds = make_mock_credentials()
        client = self._make_one(credentials=creds, http=object())

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
        creds = make_mock_credentials()
        client = self._make_one(credentials=creds, http=object())

        with self.assertRaises(TypeError):
            client.document_from_text('abc', doc_type='foo')

    def test_document_from_html_factory(self):
        from google.cloud.language.document import Document

        creds = make_mock_credentials()
        client = self._make_one(credentials=creds, http=object())

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
        creds = make_mock_credentials()
        client = self._make_one(credentials=creds, http=object())

        with self.assertRaises(TypeError):
            client.document_from_html('abc', doc_type='foo')

    def test_document_from_gcs_url_factory(self):
        from google.cloud.language.document import Document

        creds = make_mock_credentials()
        client = self._make_one(credentials=creds, http=object())

        gcs_url = 'gs://my-text-bucket/sentiment-me.txt'
        document = client.document_from_gcs_url(gcs_url)
        self.assertIsInstance(document, Document)
        self.assertIs(document.client, client)
        self.assertIsNone(document.content)
        self.assertEqual(document.gcs_url, gcs_url)
        self.assertEqual(document.doc_type, Document.PLAIN_TEXT)

    def test_document_from_gcs_url_factory_explicit(self):
        from google.cloud.language.document import Document
        from google.cloud.language.document import Encoding

        creds = make_mock_credentials()
        client = self._make_one(credentials=creds, http=object())

        encoding = Encoding.UTF32
        gcs_url = 'gs://my-text-bucket/sentiment-me.txt'
        document = client.document_from_gcs_url(gcs_url,
                                                doc_type=Document.HTML,
                                                encoding=encoding)
        self.assertIsInstance(document, Document)
        self.assertIs(document.client, client)
        self.assertIsNone(document.content)
        self.assertEqual(document.gcs_url, gcs_url)
        self.assertEqual(document.doc_type, Document.HTML)
        self.assertEqual(document.encoding, encoding)

    def test_document_from_url_deprecation(self):
        import warnings

        creds = make_mock_credentials()
        client = self._make_one(credentials=creds, http=object())

        Client = self._get_target_class()
        with mock.patch.object(Client, 'document_from_gcs_url') as dfgu:
            with mock.patch.object(warnings, 'warn') as warn:
                client.document_from_url(gcs_url='gs://bogus')

                # Establish that the warning happened and sent a
                # DeprecationWarning.
                self.assertEqual(warn.call_count, 1)
                self.assertEqual(warn.mock_calls[0][1][1], DeprecationWarning)

                # Establish that the new (renamed) method is called.
                dfgu.assert_called_once_with(gcs_url='gs://bogus')
