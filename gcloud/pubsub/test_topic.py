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


class TestTopic(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.pubsub.topic import Topic
        return Topic

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_wo_inferred_project_or_connection(self):
        from gcloud._testing import _monkey_defaults as _monkey_base_defaults
        from gcloud.pubsub._testing import _monkey_defaults
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        conn = _Connection()
        with _monkey_base_defaults(project=PROJECT):
            with _monkey_defaults(connection=conn):
                topic = self._makeOne(TOPIC_NAME)
        self.assertEqual(topic.name, TOPIC_NAME)
        self.assertEqual(topic.project, PROJECT)
        self.assertEqual(topic.full_name,
                         'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME))
        self.assertTrue(topic.connection is conn)
        self.assertFalse(topic.timestamp_messages)

    def test_ctor_w_explicit_project_connection_and_timestamp(self):
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        conn = _Connection()
        topic = self._makeOne(TOPIC_NAME,
                              project=PROJECT,
                              connection=conn,
                              timestamp_messages=True)
        self.assertEqual(topic.name, TOPIC_NAME)
        self.assertEqual(topic.project, PROJECT)
        self.assertEqual(topic.full_name,
                         'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME))
        self.assertTrue(topic.connection is conn)
        self.assertTrue(topic.timestamp_messages)

    def test_from_api_repr_wo_connection(self):
        from gcloud.pubsub._testing import _monkey_defaults
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
        resource = {'name': PATH}
        klass = self._getTargetClass()
        conn = _Connection()
        with _monkey_defaults(connection=conn):
            topic = klass.from_api_repr(resource)
        self.assertEqual(topic.name, TOPIC_NAME)
        self.assertEqual(topic.project, PROJECT)
        self.assertEqual(topic.full_name, PATH)
        self.assertTrue(topic.connection is conn)

    def test_from_api_repr_w_connection(self):
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
        resource = {'name': PATH}
        conn = object()
        klass = self._getTargetClass()
        topic = klass.from_api_repr(resource, connection=conn)
        self.assertEqual(topic.name, TOPIC_NAME)
        self.assertEqual(topic.project, PROJECT)
        self.assertEqual(topic.full_name, PATH)
        self.assertTrue(topic.connection is conn)

    def test_create_w_connection_attr(self):
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
        conn = _Connection({'name': PATH})
        topic = self._makeOne(TOPIC_NAME, project=PROJECT, connection=conn)
        topic.create()
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'PUT')
        self.assertEqual(req['path'], '/%s' % PATH)

    def test_create_w_passed_connection(self):
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
        conn = _Connection({'name': PATH})
        topic = self._makeOne(TOPIC_NAME, project=PROJECT)
        topic.create(connection=conn)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'PUT')
        self.assertEqual(req['path'], '/%s' % PATH)

    def test_exists_miss_w_connection_attr(self):
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
        conn = _Connection()
        topic = self._makeOne(TOPIC_NAME, project=PROJECT, connection=conn)
        self.assertFalse(topic.exists())
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)

    def test_exists_hit_w_passed_connection(self):
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
        conn = _Connection({'name': PATH})
        topic = self._makeOne(TOPIC_NAME, project=PROJECT)
        self.assertTrue(topic.exists(connection=conn))
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)

    def test_publish_single_bytes_wo_attrs_w_connection_attr(self):
        import base64
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        PAYLOAD = b'This is the message text'
        B64 = base64.b64encode(PAYLOAD).decode('ascii')
        MSGID = 'DEADBEEF'
        MESSAGE = {'data': B64,
                   'attributes': {}}
        PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
        conn = _Connection({'messageIds': [MSGID]})
        topic = self._makeOne(TOPIC_NAME, project=PROJECT, connection=conn)
        msgid = topic.publish(PAYLOAD)
        self.assertEqual(msgid, MSGID)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s:publish' % PATH)
        self.assertEqual(req['data'], {'messages': [MESSAGE]})

    def test_publish_single_bytes_wo_attrs_w_add_timestamp_passed_conn(self):
        import base64
        import datetime
        from gcloud.pubsub import topic as MUT
        from gcloud._helpers import _RFC3339_MICROS
        from gcloud._testing import _Monkey
        NOW = datetime.datetime.utcnow()

        def _utcnow():
            return NOW

        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        PAYLOAD = b'This is the message text'
        B64 = base64.b64encode(PAYLOAD).decode('ascii')
        MSGID = 'DEADBEEF'
        MESSAGE = {'data': B64,
                   'attributes': {'timestamp': NOW.strftime(_RFC3339_MICROS)}}
        PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
        conn = _Connection({'messageIds': [MSGID]})
        topic = self._makeOne(TOPIC_NAME, project=PROJECT,
                              timestamp_messages=True)
        with _Monkey(MUT, _NOW=_utcnow):
            msgid = topic.publish(PAYLOAD, connection=conn)
        self.assertEqual(msgid, MSGID)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s:publish' % PATH)
        self.assertEqual(req['data'], {'messages': [MESSAGE]})

    def test_publish_single_bytes_w_add_timestamp_w_ts_in_attrs(self):
        import base64

        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        PAYLOAD = b'This is the message text'
        B64 = base64.b64encode(PAYLOAD).decode('ascii')
        MSGID = 'DEADBEEF'
        OVERRIDE = '2015-04-10T16:46:22.868399Z'
        MESSAGE = {'data': B64,
                   'attributes': {'timestamp': OVERRIDE}}
        PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
        conn = _Connection({'messageIds': [MSGID]})
        topic = self._makeOne(TOPIC_NAME, project=PROJECT, connection=conn,
                              timestamp_messages=True)
        msgid = topic.publish(PAYLOAD, timestamp=OVERRIDE)
        self.assertEqual(msgid, MSGID)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s:publish' % PATH)
        self.assertEqual(req['data'], {'messages': [MESSAGE]})

    def test_publish_single_w_attrs(self):
        import base64
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        PAYLOAD = b'This is the message text'
        B64 = base64.b64encode(PAYLOAD).decode('ascii')
        MSGID = 'DEADBEEF'
        MESSAGE = {'data': B64,
                   'attributes': {'attr1': 'value1', 'attr2': 'value2'}}
        PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
        conn = _Connection({'messageIds': [MSGID]})
        topic = self._makeOne(TOPIC_NAME, project=PROJECT, connection=conn)
        msgid = topic.publish(PAYLOAD, attr1='value1', attr2='value2')
        self.assertEqual(msgid, MSGID)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s:publish' % PATH)
        self.assertEqual(req['data'], {'messages': [MESSAGE]})

    def test_publish_multiple_w_connection_attr(self):
        import base64
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        PAYLOAD1 = b'This is the first message text'
        PAYLOAD2 = b'This is the second message text'
        B64_1 = base64.b64encode(PAYLOAD1)
        B64_2 = base64.b64encode(PAYLOAD2)
        MSGID1 = 'DEADBEEF'
        MSGID2 = 'BEADCAFE'
        MESSAGE1 = {'data': B64_1.decode('ascii'),
                    'attributes': {}}
        MESSAGE2 = {'data': B64_2.decode('ascii'),
                    'attributes': {'attr1': 'value1', 'attr2': 'value2'}}
        PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
        conn = _Connection({'messageIds': [MSGID1, MSGID2]})
        topic = self._makeOne(TOPIC_NAME, project=PROJECT, connection=conn)
        with topic.batch() as batch:
            batch.publish(PAYLOAD1)
            batch.publish(PAYLOAD2, attr1='value1', attr2='value2')
        self.assertEqual(list(batch), [MSGID1, MSGID2])
        self.assertEqual(list(batch.messages), [])
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s:publish' % PATH)
        self.assertEqual(req['data'], {'messages': [MESSAGE1, MESSAGE2]})

    def test_publish_multiple_w_passed_connection(self):
        import base64
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        PAYLOAD1 = b'This is the first message text'
        PAYLOAD2 = b'This is the second message text'
        B64_1 = base64.b64encode(PAYLOAD1)
        B64_2 = base64.b64encode(PAYLOAD2)
        MSGID1 = 'DEADBEEF'
        MSGID2 = 'BEADCAFE'
        MESSAGE1 = {'data': B64_1.decode('ascii'),
                    'attributes': {}}
        MESSAGE2 = {'data': B64_2.decode('ascii'),
                    'attributes': {'attr1': 'value1', 'attr2': 'value2'}}
        PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
        conn = _Connection({'messageIds': [MSGID1, MSGID2]})
        topic = self._makeOne(TOPIC_NAME, project=PROJECT)
        with topic.batch(connection=conn) as batch:
            batch.publish(PAYLOAD1)
            batch.publish(PAYLOAD2, attr1='value1', attr2='value2')
        self.assertEqual(list(batch), [MSGID1, MSGID2])
        self.assertEqual(list(batch.messages), [])
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s:publish' % PATH)
        self.assertEqual(req['data'], {'messages': [MESSAGE1, MESSAGE2]})

    def test_publish_multiple_error(self):

        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        PAYLOAD1 = b'This is the first message text'
        PAYLOAD2 = b'This is the second message text'
        MSGID1 = 'DEADBEEF'
        MSGID2 = 'BEADCAFE'
        conn = _Connection({'messageIds': [MSGID1, MSGID2]})
        topic = self._makeOne(TOPIC_NAME, project=PROJECT, connection=conn)
        try:
            with topic.batch() as batch:
                batch.publish(PAYLOAD1)
                batch.publish(PAYLOAD2, attr1='value1', attr2='value2')
                raise _Bugout()
        except _Bugout:
            pass
        self.assertEqual(list(batch), [])
        self.assertEqual(len(conn._requested), 0)

    def test_delete_w_connection_attr(self):
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
        conn = _Connection({})
        topic = self._makeOne(TOPIC_NAME, project=PROJECT, connection=conn)
        topic.delete()
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'DELETE')
        self.assertEqual(req['path'], '/%s' % PATH)

    def test_delete_w_passed_connection(self):
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
        conn = _Connection({})
        topic = self._makeOne(TOPIC_NAME, project=PROJECT)
        topic.delete(connection=conn)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'DELETE')
        self.assertEqual(req['path'], '/%s' % PATH)


class TestBatch(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.pubsub.topic import Batch
        return Batch

    def _makeOne(self, topic, connection=None):
        if connection is None:
            return self._getTargetClass()(topic)
        return self._getTargetClass()(topic, connection)

    def test_ctor_defaults(self):
        connection = _Connection()
        topic = _Topic(connection=connection)
        batch = self._makeOne(topic)
        self.assertTrue(batch.topic is topic)
        self.assertTrue(batch.connection is connection)
        self.assertEqual(len(batch.messages), 0)
        self.assertEqual(len(batch.message_ids), 0)

    def test_ctor_explicit_connection(self):
        connection = _Connection()
        topic = _Topic()
        batch = self._makeOne(topic, connection=connection)
        self.assertTrue(batch.topic is topic)
        self.assertTrue(batch.connection is connection)
        self.assertEqual(len(batch.messages), 0)
        self.assertEqual(len(batch.message_ids), 0)

    def test___iter___empty(self):
        topic = _Topic()
        batch = self._makeOne(topic)
        self.assertEqual(list(batch), [])

    def test___iter___non_empty(self):
        topic = _Topic()
        batch = self._makeOne(topic)
        batch.message_ids[:] = ['ONE', 'TWO', 'THREE']
        self.assertEqual(list(batch), ['ONE', 'TWO', 'THREE'])

    def test_publish_bytes_wo_attrs(self):
        import base64
        PAYLOAD = b'This is the message text'
        B64 = base64.b64encode(PAYLOAD).decode('ascii')
        MESSAGE = {'data': B64,
                   'attributes': {}}
        connection = _Connection()
        topic = _Topic(connection=connection)
        batch = self._makeOne(topic)
        batch.publish(PAYLOAD)
        self.assertEqual(len(connection._requested), 0)
        self.assertEqual(batch.messages, [MESSAGE])

    def test_publish_bytes_w_add_timestamp(self):
        import base64

        PAYLOAD = b'This is the message text'
        B64 = base64.b64encode(PAYLOAD).decode('ascii')
        MESSAGE = {'data': B64,
                   'attributes': {'timestamp': 'TIMESTAMP'}}
        connection = _Connection()
        topic = _Topic(timestamp_messages=True, connection=connection)
        batch = self._makeOne(topic)
        batch.publish(PAYLOAD)
        self.assertEqual(len(connection._requested), 0)
        self.assertEqual(batch.messages, [MESSAGE])

    def test_commit_w_connection_attr(self):
        import base64
        PAYLOAD1 = b'This is the first message text'
        PAYLOAD2 = b'This is the second message text'
        B64_1 = base64.b64encode(PAYLOAD1)
        B64_2 = base64.b64encode(PAYLOAD2)
        MSGID1 = 'DEADBEEF'
        MSGID2 = 'BEADCAFE'
        MESSAGE1 = {'data': B64_1.decode('ascii'),
                    'attributes': {}}
        MESSAGE2 = {'data': B64_2.decode('ascii'),
                    'attributes': {'attr1': 'value1', 'attr2': 'value2'}}
        conn = _Connection({'messageIds': [MSGID1, MSGID2]})
        topic = _Topic(connection=conn)
        batch = self._makeOne(topic)
        batch.publish(PAYLOAD1)
        batch.publish(PAYLOAD2, attr1='value1', attr2='value2')
        batch.commit()
        self.assertEqual(list(batch), [MSGID1, MSGID2])
        self.assertEqual(list(batch.messages), [])
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '%s:publish' % topic.path)
        self.assertEqual(req['data'], {'messages': [MESSAGE1, MESSAGE2]})

    def test_context_mgr_success(self):
        import base64
        PAYLOAD1 = b'This is the first message text'
        PAYLOAD2 = b'This is the second message text'
        B64_1 = base64.b64encode(PAYLOAD1)
        B64_2 = base64.b64encode(PAYLOAD2)
        MSGID1 = 'DEADBEEF'
        MSGID2 = 'BEADCAFE'
        MESSAGE1 = {'data': B64_1.decode('ascii'),
                    'attributes': {}}
        MESSAGE2 = {'data': B64_2.decode('ascii'),
                    'attributes': {'attr1': 'value1', 'attr2': 'value2'}}
        conn = _Connection({'messageIds': [MSGID1, MSGID2]})
        topic = _Topic(connection=conn)
        batch = self._makeOne(topic)

        with batch as other:
            batch.publish(PAYLOAD1)
            batch.publish(PAYLOAD2, attr1='value1', attr2='value2')

        self.assertTrue(other is batch)
        self.assertEqual(list(batch), [MSGID1, MSGID2])
        self.assertEqual(list(batch.messages), [])
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '%s:publish' % topic.path)
        self.assertEqual(req['data'], {'messages': [MESSAGE1, MESSAGE2]})

    def test_context_mgr_failure(self):
        import base64
        PAYLOAD1 = b'This is the first message text'
        PAYLOAD2 = b'This is the second message text'
        B64_1 = base64.b64encode(PAYLOAD1)
        B64_2 = base64.b64encode(PAYLOAD2)
        MSGID1 = 'DEADBEEF'
        MSGID2 = 'BEADCAFE'
        MESSAGE1 = {'data': B64_1.decode('ascii'),
                    'attributes': {}}
        MESSAGE2 = {'data': B64_2.decode('ascii'),
                    'attributes': {'attr1': 'value1', 'attr2': 'value2'}}
        conn = _Connection({'messageIds': [MSGID1, MSGID2]})
        topic = _Topic(connection=conn)
        batch = self._makeOne(topic)

        try:
            with batch as other:
                batch.publish(PAYLOAD1)
                batch.publish(PAYLOAD2, attr1='value1', attr2='value2')
                raise _Bugout()
        except _Bugout:
            pass

        self.assertTrue(other is batch)
        self.assertEqual(list(batch), [])
        self.assertEqual(list(batch.messages), [MESSAGE1, MESSAGE2])
        self.assertEqual(len(conn._requested), 0)


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


class _Topic(object):

    def __init__(self, name="NAME", project="PROJECT",
                 timestamp_messages=False, connection=None):
        self.path = '/projects/%s/topics/%s' % (project, name)
        self.timestamp_messages = timestamp_messages
        self.connection = connection

    def _timestamp_message(self, attrs):
        if self.timestamp_messages:
            attrs['timestamp'] = 'TIMESTAMP'


class _Bugout(Exception):
    pass
