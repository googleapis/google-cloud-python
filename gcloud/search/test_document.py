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

import unittest2


class TestStringValue(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.search.document import StringValue
        return StringValue

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_defaults(self):
        sv = self._makeOne('abcde')
        self.assertEqual(sv.string_value, 'abcde')
        self.assertEqual(sv.string_format, None)
        self.assertEqual(sv.language, None)

    def test_ctor_explicit(self):
        sv = self._makeOne('abcde', 'text', 'en')
        self.assertEqual(sv.string_value, 'abcde')
        self.assertEqual(sv.string_format, 'text')
        self.assertEqual(sv.language, 'en')


class TestNumberValue(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.search.document import NumberValue
        return NumberValue

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor(self):
        nv = self._makeOne(42)
        self.assertEqual(nv.number_value, 42)


class TestTimestampValue(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.search.document import TimestampValue
        return TimestampValue

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor(self):
        import datetime
        from gcloud._helpers import UTC
        NOW = datetime.datetime.utcnow().replace(tzinfo=UTC)
        tv = self._makeOne(NOW)
        self.assertEqual(tv.timestamp_value, NOW)


class TestGeoValue(unittest2.TestCase):

    LATITUDE, LONGITUDE = 38.301931, -77.458722

    def _getTargetClass(self):
        from gcloud.search.document import GeoValue
        return GeoValue

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor(self):
        gv = self._makeOne((self.LATITUDE, self.LONGITUDE))
        self.assertEqual(gv.geo_value, (self.LATITUDE, self.LONGITUDE))


class TestField(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.search.document import Field
        return Field

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor(self):
        field = self._makeOne('field_name')
        self.assertEqual(field.name, 'field_name')
        self.assertEqual(len(field.values), 0)

    def test_add_value_unknown(self):
        field = self._makeOne('field_name')
        with self.assertRaises(ValueError):
            field.add_value(object())

    def test_add_value_string_defaults(self):
        from gcloud.search.document import StringValue
        field = self._makeOne('field_name')
        field.add_value('this is a string')
        self.assertEqual(len(field.values), 1)
        value = field.values[0]
        self.assertTrue(isinstance(value, StringValue))
        self.assertEqual(value.string_value, 'this is a string')
        self.assertEqual(value.string_format, None)
        self.assertEqual(value.language, None)

    def test_add_value_string_explicit(self):
        from gcloud.search.document import StringValue
        field = self._makeOne('field_name')
        field.add_value('this is a string',
                        string_format='text', language='en')
        self.assertEqual(len(field.values), 1)
        value = field.values[0]
        self.assertTrue(isinstance(value, StringValue))
        self.assertEqual(value.string_value, 'this is a string')
        self.assertEqual(value.string_format, 'text')
        self.assertEqual(value.language, 'en')

    def test_add_value_integer(self):
        from gcloud.search.document import NumberValue
        field = self._makeOne('field_name')
        field.add_value(42)
        self.assertEqual(len(field.values), 1)
        value = field.values[0]
        self.assertTrue(isinstance(value, NumberValue))
        self.assertEqual(value.number_value, 42)

    def test_add_value_datetime(self):
        import datetime
        from gcloud._helpers import UTC
        from gcloud.search.document import TimestampValue
        NOW = datetime.datetime.utcnow().replace(tzinfo=UTC)
        field = self._makeOne('field_name')
        field.add_value(NOW)
        self.assertEqual(len(field.values), 1)
        value = field.values[0]
        self.assertTrue(isinstance(value, TimestampValue))
        self.assertEqual(value.timestamp_value, NOW)

    def test_add_value_geo(self):
        from gcloud.search.document import GeoValue
        LATITUDE, LONGITUDE = 38.301931, -77.458722
        field = self._makeOne('field_name')
        field.add_value((LATITUDE, LONGITUDE))
        self.assertEqual(len(field.values), 1)
        value = field.values[0]
        self.assertTrue(isinstance(value, GeoValue))
        self.assertEqual(value.geo_value, (LATITUDE, LONGITUDE))


class TestDocument(unittest2.TestCase):

    PROJECT = 'PROJECT'
    DOC_NAME = 'doc_name'
    INDEX_NAME = 'index_name'
    DOC_PATH = 'projects/%s/indexes/%s/documents/%s' % (
        PROJECT, INDEX_NAME, DOC_NAME)
    RANK = 42

    def _getTargetClass(self):
        from gcloud.search.document import Document
        return Document

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_defaults(self):
        index = object()
        document = self._makeOne(self.DOC_NAME, index)
        self.assertEqual(document.name, self.DOC_NAME)
        self.assertTrue(document.index is index)
        self.assertEqual(document.rank, None)
        self.assertEqual(document.fields, {})

    def test_ctor_explicit(self):
        index = object()
        document = self._makeOne(self.DOC_NAME, index, self.RANK)
        self.assertEqual(document.name, self.DOC_NAME)
        self.assertTrue(document.index is index)
        self.assertEqual(document.rank, self.RANK)
        self.assertEqual(document.fields, {})

    def test_from_api_repr_invalid(self):
        klass = self._getTargetClass()
        index = object()
        with self.assertRaises(KeyError):
            klass.from_api_repr({}, index)

    def test_from_api_repr(self):
        import datetime
        from gcloud._helpers import UTC, _RFC3339_MICROS
        VALUE = 'The quick brown fox'
        HTML_VALUE = 'jumped <em>over</em> the lazy fence.'
        NOW = datetime.datetime.utcnow().replace(tzinfo=UTC)
        NOW_STR = NOW.strftime(_RFC3339_MICROS)
        LATITUDE, LONGITUDE = 38.301931, -77.458722
        resource = {
            'docId': self.DOC_NAME,
            'rank': self.RANK,
            'fields': {
                'title': {
                    'values': [
                        {'stringFormat': 'text',
                         'lang': 'en',
                         'stringValue': VALUE},
                        {'stringFormat': 'html',
                         'lang': 'en',
                         'stringValue': HTML_VALUE},
                        {'numberValue': 42},
                        {'numberValue': '42'},
                        {'numberValue': '3.1415926'},
                        {'timestampValue': NOW_STR},
                        {'geoValue': '%s, %s' % (LATITUDE, LONGITUDE)},
                    ],
                }
            }
        }
        klass = self._getTargetClass()
        index = object()

        document = klass.from_api_repr(resource, index)

        self.assertEqual(document.name, self.DOC_NAME)
        self.assertTrue(document.index is index)
        self.assertEqual(document.rank, self.RANK)

        self.assertEqual(list(document.fields), ['title'])
        field = document.fields['title']
        self.assertEqual(field.name, 'title')
        self.assertEqual(len(field.values), 7)

        value = field.values[0]
        self.assertEqual(value.value_type, 'string')
        self.assertEqual(value.language, 'en')
        self.assertEqual(value.string_format, 'text')
        self.assertEqual(value.string_value, VALUE)

        value = field.values[1]
        self.assertEqual(value.value_type, 'string')
        self.assertEqual(value.language, 'en')
        self.assertEqual(value.string_format, 'html')
        self.assertEqual(value.string_value,
                         'jumped <em>over</em> the lazy fence.')

        value = field.values[2]
        self.assertEqual(value.value_type, 'number')
        self.assertEqual(value.number_value, 42)

        value = field.values[3]
        self.assertEqual(value.value_type, 'number')
        self.assertEqual(value.number_value, 42)

        value = field.values[4]
        self.assertEqual(value.value_type, 'number')
        self.assertEqual(value.number_value, 3.1415926)

        value = field.values[5]
        self.assertEqual(value.value_type, 'timestamp')
        self.assertEqual(value.timestamp_value, NOW)

        value = field.values[6]
        self.assertEqual(value.value_type, 'geo')
        self.assertEqual(value.geo_value, (LATITUDE, LONGITUDE))

    def test__parse_value_resource_invalid(self):
        conn = _Connection()
        client = _Client(project=self.PROJECT, connection=conn)
        index = _Index(self.INDEX_NAME, client=client)
        document = self._makeOne(self.DOC_NAME, index)
        with self.assertRaises(ValueError):
            document._parse_value_resource({})

    def test__build_value_resource_invalid(self):
        class _UnknownValue(object):
            value_type = 'nonesuch'
        conn = _Connection()
        client = _Client(project=self.PROJECT, connection=conn)
        index = _Index(self.INDEX_NAME, client=client)
        document = self._makeOne(self.DOC_NAME, index)
        with self.assertRaises(ValueError):
            document._build_value_resource(_UnknownValue())

    def test__build_field_resources_field_wo_values(self):
        conn = _Connection()
        client = _Client(project=self.PROJECT, connection=conn)
        index = _Index(self.INDEX_NAME, client=client)
        document = self._makeOne(self.DOC_NAME, index)
        _ = document.field('testing')  # no values
        self.assertEqual(document._build_fields_resource(), {})

    def test_create_wo_fields(self):
        import copy
        BODY = {'docId': self.DOC_NAME}
        RESPONSE = copy.deepcopy(BODY)
        RESPONSE['rank'] = self.RANK
        conn = _Connection(RESPONSE)
        client = _Client(project=self.PROJECT, connection=conn)
        index = _Index(self.INDEX_NAME, client=client)
        document = self._makeOne(self.DOC_NAME, index)

        document.create()

        self.assertEqual(list(document.fields), [])

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'PUT')
        self.assertEqual(req['path'], '/%s' % self.DOC_PATH)
        self.assertEqual(req['data'], BODY)

    def test_create_wo_rank_w_bound_client(self):
        import copy
        VALUE = 'The quick brown fox'
        BODY = {
            'docId': self.DOC_NAME,
            'fields': {
                'testing': {
                    'values': [
                        {'stringValue': VALUE},
                    ],
                }
            }
        }
        RESPONSE = copy.deepcopy(BODY)
        RESPONSE['rank'] = self.RANK
        response_value = RESPONSE['fields']['testing']['values'][0]
        response_value['stringFormat'] = 'auto'
        conn = _Connection(RESPONSE)
        client = _Client(project=self.PROJECT, connection=conn)
        index = _Index(self.INDEX_NAME, client=client)
        document = self._makeOne(self.DOC_NAME, index)
        field = document.field('testing')
        field.add_value(VALUE)

        document.create()

        self.assertEqual(list(document.fields), ['testing'])
        field = document.fields['testing']
        self.assertEqual(len(field.values), 1)

        value = field.values[0]
        self.assertEqual(value.value_type, 'string')
        self.assertEqual(value.string_format, 'auto')
        self.assertEqual(value.string_value, VALUE)
        self.assertEqual(value.language, None)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'PUT')
        self.assertEqual(req['path'], '/%s' % self.DOC_PATH)
        self.assertEqual(req['data'], BODY)

    def test_create_w_rank_w_alternate_client(self):
        import datetime
        from gcloud._helpers import UTC, _RFC3339_MICROS
        VALUE = 'The quick brown fox'
        NOW = datetime.datetime.utcnow().replace(tzinfo=UTC)
        NOW_STR = NOW.strftime(_RFC3339_MICROS)
        LATITUDE, LONGITUDE = 38.301931, -77.458722
        BODY = {
            'docId': self.DOC_NAME,
            'rank': self.RANK,
            'fields': {
                'title': {
                    'values': [
                        {'stringValue': VALUE,
                         'stringFormat': 'text',
                         'lang': 'en'},
                        {'numberValue': 17.5},
                        {'timestampValue': NOW_STR},
                        {'geoValue': '%s, %s' % (LATITUDE, LONGITUDE)},
                    ],
                }
            }
        }
        RESPONSE = BODY.copy()
        RESPONSE['rank'] = self.RANK
        conn1 = _Connection()
        client1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection(BODY)
        client2 = _Client(project=self.PROJECT, connection=conn2)
        index = _Index(self.INDEX_NAME, client=client1)
        document = self._makeOne(self.DOC_NAME, index, rank=self.RANK)
        field = document.field('title')
        field.add_value(VALUE, string_format='text', language='en')
        field.add_value(17.5)
        field.add_value(NOW)
        field.add_value((LATITUDE, LONGITUDE))

        document.create(client=client2)

        self.assertEqual(list(document.fields), ['title'])
        field = document.fields['title']
        self.assertEqual(len(field.values), 4)

        value = field.values[0]
        self.assertEqual(value.value_type, 'string')
        self.assertEqual(value.string_format, 'text')
        self.assertEqual(value.string_value, VALUE)
        self.assertEqual(value.language, 'en')

        value = field.values[1]
        self.assertEqual(value.value_type, 'number')
        self.assertEqual(value.number_value, 17.5)

        value = field.values[2]
        self.assertEqual(value.value_type, 'timestamp')
        self.assertEqual(value.timestamp_value, NOW)

        value = field.values[3]
        self.assertEqual(value.value_type, 'geo')
        self.assertEqual(value.geo_value, (LATITUDE, LONGITUDE))

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)

        req = conn2._requested[0]
        self.assertEqual(req['method'], 'PUT')
        self.assertEqual(req['path'], '/%s' % self.DOC_PATH)
        self.assertEqual(req['data'], BODY)

    def test_exists_miss_w_bound_client(self):
        conn = _Connection()
        client = _Client(project=self.PROJECT, connection=conn)
        index = _Index(self.INDEX_NAME, client=client)
        document = self._makeOne(self.DOC_NAME, index)

        self.assertFalse(document.exists())

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % self.DOC_PATH)
        self.assertEqual(req.get('query_params'), None)

    def test_exists_hit_w_alternate_client(self):
        BODY = {'docId': self.DOC_NAME, 'rank': self.RANK}
        conn1 = _Connection()
        client1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection(BODY)
        client2 = _Client(project=self.PROJECT, connection=conn2)
        index = _Index(self.INDEX_NAME, client=client1)
        document = self._makeOne(self.DOC_NAME, index)

        self.assertTrue(document.exists(client=client2))

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % self.DOC_PATH)
        self.assertEqual(req.get('query_params'), None)

    def test_reload_w_bound_client(self):
        VALUE = 'The quick brown fox'
        BODY = {
            'docId': self.DOC_NAME,
            'rank': self.RANK,
            'fields': {
                'title': {
                    'values': [
                        {'stringFormat': 'text',
                         'lang': 'en',
                         'stringValue': VALUE},
                    ],
                }
            }
        }
        conn = _Connection(BODY)
        client = _Client(project=self.PROJECT, connection=conn)
        index = _Index(self.INDEX_NAME, client=client)
        document = self._makeOne(self.DOC_NAME, index)

        document.reload()

        self.assertEqual(document.rank, self.RANK)

        self.assertEqual(list(document.fields), ['title'])
        field = document.fields['title']
        self.assertEqual(len(field.values), 1)
        self.assertEqual(field.name, 'title')
        self.assertEqual(len(field.values), 1)

        value = field.values[0]
        self.assertEqual(value.value_type, 'string')
        self.assertEqual(value.language, 'en')
        self.assertEqual(value.string_format, 'text')
        self.assertEqual(value.string_value, VALUE)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % self.DOC_PATH)

    def test_reload_w_alternate_client(self):
        VALUE = 'The quick brown fox'
        BODY = {
            'docId': self.DOC_NAME,
            'rank': self.RANK,
            'fields': {
                'title': {
                    'values': [
                        {'stringFormat': 'text',
                         'lang': 'en',
                         'stringValue': VALUE},
                    ],
                }
            }
        }
        conn1 = _Connection()
        client1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection(BODY)
        client2 = _Client(project=self.PROJECT, connection=conn2)
        index = _Index(self.INDEX_NAME, client=client1)
        document = self._makeOne(self.DOC_NAME, index)

        document.reload(client=client2)

        self.assertEqual(document.rank, self.RANK)

        self.assertEqual(list(document.fields), ['title'])
        field = document.fields['title']
        self.assertEqual(field.name, 'title')
        self.assertEqual(len(field.values), 1)

        value = field.values[0]
        self.assertEqual(value.value_type, 'string')
        self.assertEqual(value.language, 'en')
        self.assertEqual(value.string_format, 'text')
        self.assertEqual(value.string_value, VALUE)

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % self.DOC_PATH)

    def test_delete_w_bound_client(self):
        conn = _Connection({})
        client = _Client(project=self.PROJECT, connection=conn)
        index = _Index(self.INDEX_NAME, client=client)
        document = self._makeOne(self.DOC_NAME, index)

        document.delete()

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'DELETE')
        self.assertEqual(req['path'], '/%s' % self.DOC_PATH)

    def test_delete_w_alternate_client(self):
        conn1 = _Connection({})
        client1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection({})
        client2 = _Client(project=self.PROJECT, connection=conn2)
        index = _Index(self.INDEX_NAME, client=client1)
        document = self._makeOne(self.DOC_NAME, index)

        document.delete(client=client2)

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'DELETE')
        self.assertEqual(req['path'], '/%s' % self.DOC_PATH)


class _Connection(object):

    def __init__(self, *responses):
        self._responses = responses
        self._requested = []

    def api_request(self, **kw):
        from gcloud.exceptions import NotFound
        self._requested.append(kw)

        try:
            response, self._responses = self._responses[0], self._responses[1:]
        except:
            raise NotFound('miss')
        else:
            return response


class _Index(object):

    def __init__(self, name, client):
        self.name = name
        self._client = client
        self.project = client.project
        self.path = '/projects/%s/indexes/%s' % (client.project, name)


class _Client(object):

    def __init__(self, project, connection=None):
        self.project = project
        self.connection = connection
