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

    def test_ctor_w_explicit_project_and_connection(self):
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        conn = _Connection()
        topic = self._makeOne(TOPIC_NAME, project=PROJECT, connection=conn)
        self.assertEqual(topic.name, TOPIC_NAME)
        self.assertEqual(topic.project, PROJECT)
        self.assertEqual(topic.full_name,
                         'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME))
        self.assertTrue(topic.connection is conn)

    def test_create(self):
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

    def test_exists_miss(self):
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

    def test_exists_hit(self):
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
        conn = _Connection({'name': PATH})
        topic = self._makeOne(TOPIC_NAME, project=PROJECT, connection=conn)
        self.assertTrue(topic.exists())
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)

    def test_delete(self):
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

    def test_publish_single_wo_attrs(self):
        import base64
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        PAYLOAD = b'This is the message text'
        B64 = base64.b64encode(PAYLOAD)
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

    def test_publish_single_w_attrs(self):
        import base64
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        PAYLOAD = b'This is the message text'
        B64 = base64.b64encode(PAYLOAD)
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

    def test_publish_multiple(self):
        import base64
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        PAYLOAD1 = b'This is the first message text'
        PAYLOAD2 = b'This is the second message text'
        B64_1 = base64.b64encode(PAYLOAD1)
        B64_2 = base64.b64encode(PAYLOAD2)
        MSGID1 = 'DEADBEEF'
        MSGID2 = 'BEADCAFE'
        MESSAGE1 = {'data': B64_1,
                    'attributes': {}}
        MESSAGE2 = {'data': B64_2,
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

    def test_publish_multiple_error(self):
        class Bugout(Exception):
            pass

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
                raise Bugout()
        except Bugout:
            pass
        self.assertEqual(list(batch), [])
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
