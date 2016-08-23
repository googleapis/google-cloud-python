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

    def test__to_dict_with_content(self):
        klass = self._getTargetClass()
        content = 'Hello World'
        document = self._makeOne(None, content=content)
        info = document._to_dict()
        self.assertEqual(info, {
            'content': content,
            'language': document.language,
            'type': klass.PLAIN_TEXT,
        })

    def test__to_dict_with_gcs(self):
        klass = self._getTargetClass()
        gcs_url = 'gs://some-bucket/some-obj.html'
        document = self._makeOne(None, gcs_url=gcs_url)
        info = document._to_dict()
        self.assertEqual(info, {
            'gcsContentUri': gcs_url,
            'language': document.language,
            'type': klass.PLAIN_TEXT,
        })

    def test__to_dict_with_no_content(self):
        klass = self._getTargetClass()
        document = self._makeOne(None, content='')
        document.content = None  # Manually unset the content.
        info = document._to_dict()
        self.assertEqual(info, {
            'language': document.language,
            'type': klass.PLAIN_TEXT,
        })

    def test_analyze_entities(self):
        from gcloud.language.entity import Entity
        from gcloud.language.entity import EntityType

        name1 = 'R-O-C-K'
        name2 = 'USA'
        content = name1 + ' in the ' + name2
        wiki2 = 'http://en.wikipedia.org/wiki/United_States'
        salience1 = 0.91391456
        salience2 = 0.086085409
        response = {
            'entities': [
                {
                    'name': name1,
                    'type': EntityType.OTHER,
                    'metadata': {},
                    'salience': salience1,
                    'mentions': [
                        {
                            'text': {
                                'content': name1,
                                'beginOffset': -1
                            }
                        }
                    ]
                },
                {
                    'name': name2,
                    'type': EntityType.LOCATION,
                    'metadata': {'wikipedia_url': wiki2},
                    'salience': salience2,
                    'mentions': [
                        {
                            'text': {
                                'content': name2,
                                'beginOffset': -1,
                            },
                        },
                    ],
                },
            ],
            'language': 'en',
        }
        connection = _Connection(response)
        client = _Client(connection=connection)
        document = self._makeOne(client, content)

        entities = document.analyze_entities()
        self.assertEqual(len(entities), 2)
        entity1 = entities[0]
        self.assertIsInstance(entity1, Entity)
        self.assertEqual(entity1.name, name1)
        self.assertEqual(entity1.entity_type, EntityType.OTHER)
        self.assertEqual(entity1.wikipedia_url, None)
        self.assertEqual(entity1.metadata, {})
        self.assertEqual(entity1.salience, salience1)
        self.assertEqual(entity1.mentions, [name1])
        entity2 = entities[1]
        self.assertIsInstance(entity2, Entity)
        self.assertEqual(entity2.name, name2)
        self.assertEqual(entity2.entity_type, EntityType.LOCATION)
        self.assertEqual(entity2.wikipedia_url, wiki2)
        self.assertEqual(entity2.metadata, {})
        self.assertEqual(entity2.salience, salience2)
        self.assertEqual(entity2.mentions, [name2])

        # Verify the request.
        self.assertEqual(len(connection._requested), 1)
        req = connection._requested[0]
        self.assertEqual(req['path'], 'analyzeEntities')
        self.assertEqual(req['method'], 'POST')


class _Connection(object):

    def __init__(self, response):
        self._response = response
        self._requested = []

    def api_request(self, **kwargs):
        self._requested.append(kwargs)
        return self._response


class _Client(object):

    def __init__(self, connection=None):
        self.connection = connection
