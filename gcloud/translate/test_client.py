# Copyright 2016 Google Inc. All rights reserved.
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

import unittest2


class TestClient(unittest2.TestCase):

    KEY = 'abc-123-my-key'

    def _getTargetClass(self):
        from gcloud.translate.client import Client
        return Client

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor(self):
        from gcloud.translate.connection import Connection
        from gcloud.translate.client import ENGLISH_ISO_639

        http = object()
        client = self._makeOne(self.KEY, http=http)
        self.assertTrue(isinstance(client.connection, Connection))
        self.assertIsNone(client.connection.credentials)
        self.assertTrue(client.connection.http is http)
        self.assertEqual(client.target_language, ENGLISH_ISO_639)

    def test_ctor_non_default(self):
        from gcloud.translate.connection import Connection

        http = object()
        target = 'es'
        client = self._makeOne(self.KEY, http=http, target_language=target)
        self.assertTrue(isinstance(client.connection, Connection))
        self.assertIsNone(client.connection.credentials)
        self.assertTrue(client.connection.http is http)
        self.assertEqual(client.target_language, target)

    def test_get_languages(self):
        from gcloud.translate.client import ENGLISH_ISO_639

        client = self._makeOne(self.KEY)
        supported = [
            {'language': 'en', 'name': 'English'},
            {'language': 'af', 'name': 'Afrikaans'},
            {'language': 'am', 'name': 'Amharic'},
        ]
        data = {
            'data': {
                'languages': supported,
            },
        }
        conn = client.connection = _Connection(data)

        result = client.get_languages()
        self.assertEqual(result, supported)

        # Verify requested.
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/languages')
        self.assertEqual(req['query_params'],
                         {'key': self.KEY, 'target': ENGLISH_ISO_639})

    def test_get_languages_no_target(self):
        client = self._makeOne(self.KEY, target_language=None)
        supported = [
            {'language': 'en'},
            {'language': 'af'},
            {'language': 'am'},
        ]
        data = {
            'data': {
                'languages': supported,
            },
        }
        conn = client.connection = _Connection(data)

        result = client.get_languages()
        self.assertEqual(result, supported)

        # Verify requested.
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/languages')
        self.assertEqual(req['query_params'], {'key': self.KEY})

    def test_get_languages_explicit_target(self):
        client = self._makeOne(self.KEY)
        target_language = 'en'
        supported = [
            {'language': 'en', 'name': 'Spanish'},
            {'language': 'af', 'name': 'Afrikaans'},
            {'language': 'am', 'name': 'Amharic'},
        ]
        data = {
            'data': {
                'languages': supported,
            },
        }
        conn = client.connection = _Connection(data)

        result = client.get_languages(target_language)
        self.assertEqual(result, supported)

        # Verify requested.
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/languages')
        self.assertEqual(req['query_params'],
                         {'key': self.KEY, 'target': target_language})

    def test_detect_language_bad_result(self):
        client = self._makeOne(self.KEY)
        value = 'takoy'
        conn = client.connection = _Connection({})

        with self.assertRaises(ValueError):
            client.detect_language(value)

        # Verify requested.
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/detect')
        query_params = [
            ('key', self.KEY),
            ('q', value.encode('utf-8')),
        ]
        self.assertEqual(req['query_params'], query_params)

    def test_detect_language_single_value(self):
        client = self._makeOne(self.KEY)
        value = 'takoy'
        detection = {
            'confidence': 1.0,
            'input': value,
            'language': 'ru',
            'isReliable': False,
        }
        data = {
            'data': {
                'detections': [[detection]],
            },
        }
        conn = client.connection = _Connection(data)

        result = client.detect_language(value)
        self.assertEqual(result, detection)

        # Verify requested.
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/detect')
        query_params = [
            ('key', self.KEY),
            ('q', value.encode('utf-8')),
        ]
        self.assertEqual(req['query_params'], query_params)

    def test_detect_language_multiple_values(self):
        client = self._makeOne(self.KEY)
        value1 = u'fa\xe7ade'  # facade (with a cedilla)
        detection1 = {
            'confidence': 0.6166008,
            'input': value1,
            'isReliable': False,
            'language': 'en',
        }
        value2 = 's\'il vous plait'
        detection2 = {
            'confidence': 0.29728225,
            'input': value2,
            'isReliable': False,
            'language': 'fr',
        }
        data = {
            'data': {
                'detections': [
                    [detection1],
                    [detection2],
                ],
            },
        }
        conn = client.connection = _Connection(data)

        result = client.detect_language([value1, value2])
        self.assertEqual(result, [detection1, detection2])

        # Verify requested.
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/detect')
        query_params = [
            ('key', self.KEY),
            ('q', value1.encode('utf-8')),
            ('q', value2.encode('utf-8')),
        ]
        self.assertEqual(req['query_params'], query_params)

    def test_detect_language_multiple_results(self):
        client = self._makeOne(self.KEY)
        value = 'soy'
        detection1 = {
            'confidence': 0.81496066,
            'input': value,
            'language': 'es',
            'isReliable': False,
        }
        detection2 = {
            'confidence': 0.222,
            'input': value,
            'language': 'en',
            'isReliable': False,
        }
        data = {
            'data': {
                'detections': [[detection1, detection2]],
            },
        }
        client.connection = _Connection(data)

        with self.assertRaises(ValueError):
            client.detect_language(value)

    def test_translate_bad_result(self):
        client = self._makeOne(self.KEY)
        value = 'hvala ti'
        conn = client.connection = _Connection({})

        with self.assertRaises(ValueError):
            client.translate(value)

        # Verify requested.
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '')
        query_params = [
            ('key', self.KEY),
            ('target', 'en'),
            ('q', value.encode('utf-8')),
        ]
        self.assertEqual(req['query_params'], query_params)

    def test_translate_defaults(self):
        client = self._makeOne(self.KEY)
        value = 'hvala ti'
        translation = {
            'detectedSourceLanguage': 'hr',
            'translatedText': 'thank you',
            'input': value,
        }
        data = {
            'data': {
                'translations': [translation],
            },
        }
        conn = client.connection = _Connection(data)

        result = client.translate(value)
        self.assertEqual(result, translation)

        # Verify requested.
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '')
        query_params = [
            ('key', self.KEY),
            ('target', 'en'),
            ('q', value.encode('utf-8')),
        ]
        self.assertEqual(req['query_params'], query_params)

    def test_translate_multiple(self):
        client = self._makeOne(self.KEY)
        value1 = 'hvala ti'
        translation1 = {
            'detectedSourceLanguage': 'hr',
            'translatedText': 'thank you',
            'input': value1,
        }
        value2 = 'Dankon'
        translation2 = {
            'detectedSourceLanguage': 'eo',
            'translatedText': 'thank you',
            'input': value2,
        }
        data = {
            'data': {
                'translations': [translation1, translation2],
            },
        }
        conn = client.connection = _Connection(data)

        result = client.translate([value1, value2])
        self.assertEqual(result, [translation1, translation2])

        # Verify requested.
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '')
        query_params = [
            ('key', self.KEY),
            ('target', 'en'),
            ('q', value1.encode('utf-8')),
            ('q', value2.encode('utf-8')),
        ]
        self.assertEqual(req['query_params'], query_params)

    def test_translate_explicit(self):
        client = self._makeOne(self.KEY)
        value = 'thank you'
        target_language = 'eo'
        source_language = 'en'
        translation = {
            'translatedText': 'Dankon',
            'input': value,
        }
        data = {
            'data': {
                'translations': [translation],
            },
        }
        conn = client.connection = _Connection(data)

        cid = '123'
        format_ = 'text'
        result = client.translate(value, target_language=target_language,
                                  source_language=source_language,
                                  format_=format_, customization_ids=cid)
        self.assertEqual(result, translation)

        # Verify requested.
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '')
        query_params = [
            ('key', self.KEY),
            ('target', target_language),
            ('q', value.encode('utf-8')),
            ('cid', cid),
            ('format', format_),
            ('source', source_language),
        ]
        self.assertEqual(req['query_params'], query_params)


class _Connection(object):

    def __init__(self, *responses):
        self._responses = responses
        self._requested = []

    def api_request(self, **kw):
        self._requested.append(kw)
        response, self._responses = self._responses[0], self._responses[1:]
        return response
