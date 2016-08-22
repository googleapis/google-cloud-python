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


class TestDocument(unittest.TestCase):

    def _getTargetClass(self):
        from gcloud.language.document import Document
        return Document

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_constructor_defaults(self):
        import gcloud.language.document as MUT

        client = object()
        content = 'abc'
        document = self._makeOne(client, content)
        self.assertIs(document.client, client)
        self.assertEqual(document.content, content)
        self.assertIsNone(document.gcs_url)
        self.assertEqual(document.doc_type, MUT.Document.PLAIN_TEXT)
        self.assertEqual(document.language, MUT.DEFAULT_LANGUAGE)
        self.assertEqual(document.encoding, MUT.Encoding.UTF8)

    def test_constructor_explicit(self):
        import gcloud.language.document as MUT

        client = object()
        gcs_url = 'gs://some-bucket/some-obj.html'
        language = 'ja'
        document = self._makeOne(client, gcs_url=gcs_url,
                                 doc_type=MUT.Document.HTML,
                                 language=language,
                                 encoding=MUT.Encoding.UTF32)
        self.assertIs(document.client, client)
        self.assertIsNone(document.content)
        self.assertEqual(document.gcs_url, gcs_url)
        self.assertEqual(document.doc_type, MUT.Document.HTML)
        self.assertEqual(document.language, language)
        self.assertEqual(document.encoding, MUT.Encoding.UTF32)

    def test_constructor_no_text(self):
        with self.assertRaises(ValueError):
            self._makeOne(None, content=None, gcs_url=None)

    def test_constructor_text_and_gcs(self):
        with self.assertRaises(ValueError):
            self._makeOne(None, content='abc',
                          gcs_url='gs://some-bucket/some-obj.txt')
