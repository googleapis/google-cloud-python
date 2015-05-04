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


class TestSubscription(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.pubsub.subscription import Subscription
        return Subscription

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_defaults(self):
        SUB_NAME = 'sub_name'
        topic = object()
        subscription = self._makeOne(SUB_NAME, topic)
        self.assertEqual(subscription.name, SUB_NAME)
        self.assertTrue(subscription.topic is topic)
        self.assertEqual(subscription.ack_deadline, None)
        self.assertEqual(subscription.push_endpoint, None)

    def test_ctor_explicit(self):
        SUB_NAME = 'sub_name'
        DEADLINE = 42
        ENDPOINT = 'https://api.example.com/push'
        topic = object()
        subscription = self._makeOne(SUB_NAME, topic, DEADLINE, ENDPOINT)
        self.assertEqual(subscription.name, SUB_NAME)
        self.assertTrue(subscription.topic is topic)
        self.assertEqual(subscription.ack_deadline, DEADLINE)
        self.assertEqual(subscription.push_endpoint, ENDPOINT)

    def test_from_api_repr_no_topics_no_connection(self):
        from gcloud.pubsub.topic import Topic
        from gcloud.pubsub._testing import _monkey_defaults
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        TOPIC_PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
        SUB_NAME = 'sub_name'
        SUB_PATH = 'projects/%s/subscriptions/%s' % (PROJECT, SUB_NAME)
        DEADLINE = 42
        ENDPOINT = 'https://api.example.com/push'
        resource = {'topic': TOPIC_PATH,
                    'name': SUB_PATH,
                    'ackDeadlineSeconds': DEADLINE,
                    'pushConfig': {'pushEndpoint': ENDPOINT}}
        conn = _Connection()
        klass = self._getTargetClass()
        with _monkey_defaults(connection=conn):
            subscription = klass.from_api_repr(resource, connection=conn)
        self.assertEqual(subscription.name, SUB_NAME)
        topic = subscription.topic
        self.assertTrue(isinstance(topic, Topic))
        self.assertEqual(topic.name, TOPIC_NAME)
        self.assertEqual(topic.project, PROJECT)
        self.assertTrue(topic.connection is conn)
        self.assertEqual(subscription.ack_deadline, DEADLINE)
        self.assertEqual(subscription.push_endpoint, ENDPOINT)

    def test_from_api_repr_w_topics_no_topic_match(self):
        from gcloud.pubsub.topic import Topic
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        TOPIC_PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
        SUB_NAME = 'sub_name'
        SUB_PATH = 'projects/%s/subscriptions/%s' % (PROJECT, SUB_NAME)
        DEADLINE = 42
        ENDPOINT = 'https://api.example.com/push'
        resource = {'topic': TOPIC_PATH,
                    'name': SUB_PATH,
                    'ackDeadlineSeconds': DEADLINE,
                    'pushConfig': {'pushEndpoint': ENDPOINT}}
        conn = _Connection()
        topics = {}
        klass = self._getTargetClass()
        subscription = klass.from_api_repr(resource, connection=conn,
                                           topics=topics)
        self.assertEqual(subscription.name, SUB_NAME)
        topic = subscription.topic
        self.assertTrue(isinstance(topic, Topic))
        self.assertTrue(topic is topics[TOPIC_PATH])
        self.assertEqual(topic.name, TOPIC_NAME)
        self.assertEqual(topic.project, PROJECT)
        self.assertTrue(topic.connection is conn)
        self.assertEqual(subscription.ack_deadline, DEADLINE)
        self.assertEqual(subscription.push_endpoint, ENDPOINT)

    def test_from_api_repr_w_topics_w_topic_match(self):
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        TOPIC_PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
        SUB_NAME = 'sub_name'
        SUB_PATH = 'projects/%s/subscriptions/%s' % (PROJECT, SUB_NAME)
        DEADLINE = 42
        ENDPOINT = 'https://api.example.com/push'
        resource = {'topic': TOPIC_PATH,
                    'name': SUB_PATH,
                    'ackDeadlineSeconds': DEADLINE,
                    'pushConfig': {'pushEndpoint': ENDPOINT}}
        topic = object()
        topics = {TOPIC_PATH: topic}
        klass = self._getTargetClass()
        subscription = klass.from_api_repr(resource, topics=topics)
        self.assertEqual(subscription.name, SUB_NAME)
        self.assertTrue(subscription.topic is topic)
        self.assertEqual(subscription.ack_deadline, DEADLINE)
        self.assertEqual(subscription.push_endpoint, ENDPOINT)

    def test_create_pull_wo_ack_deadline_w_connection_attr(self):
        PROJECT = 'PROJECT'
        SUB_NAME = 'sub_name'
        SUB_PATH = 'projects/%s/subscriptions/%s' % (PROJECT, SUB_NAME)
        TOPIC_NAME = 'topic_name'
        TOPIC_PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
        BODY = {'topic': TOPIC_PATH}
        conn = _Connection({'name': SUB_PATH})
        topic = _Topic(TOPIC_NAME, project=PROJECT, connection=conn)
        subscription = self._makeOne(SUB_NAME, topic)
        subscription.create()
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'PUT')
        self.assertEqual(req['path'], '/%s' % SUB_PATH)
        self.assertEqual(req['data'], BODY)

    def test_create_push_w_ack_deadline_w_passed_connection(self):
        PROJECT = 'PROJECT'
        SUB_NAME = 'sub_name'
        SUB_PATH = 'projects/%s/subscriptions/%s' % (PROJECT, SUB_NAME)
        TOPIC_NAME = 'topic_name'
        TOPIC_PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
        DEADLINE = 42
        ENDPOINT = 'https://api.example.com/push'
        BODY = {'topic': TOPIC_PATH,
                'ackDeadline': DEADLINE,
                'pushConfig': {'pushEndpoint': ENDPOINT}}
        conn = _Connection({'name': SUB_PATH})
        topic = _Topic(TOPIC_NAME, project=PROJECT)
        subscription = self._makeOne(SUB_NAME, topic, DEADLINE, ENDPOINT)
        subscription.create(connection=conn)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'PUT')
        self.assertEqual(req['path'], '/%s' % SUB_PATH)
        self.assertEqual(req['data'], BODY)

    def test_exists_miss_w_connection_attr(self):
        PROJECT = 'PROJECT'
        SUB_NAME = 'sub_name'
        SUB_PATH = 'projects/%s/subscriptions/%s' % (PROJECT, SUB_NAME)
        TOPIC_NAME = 'topic_name'
        conn = _Connection()
        topic = _Topic(TOPIC_NAME, project=PROJECT, connection=conn)
        subscription = self._makeOne(SUB_NAME, topic)
        self.assertFalse(subscription.exists())
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % SUB_PATH)
        self.assertEqual(req.get('query_params'), None)

    def test_exists_hit_w_passed_connection(self):
        PROJECT = 'PROJECT'
        SUB_NAME = 'sub_name'
        SUB_PATH = 'projects/%s/subscriptions/%s' % (PROJECT, SUB_NAME)
        TOPIC_NAME = 'topic_name'
        TOPIC_PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
        conn = _Connection({'name': SUB_PATH, 'topic': TOPIC_PATH})
        topic = _Topic(TOPIC_NAME, project=PROJECT)
        subscription = self._makeOne(SUB_NAME, topic)
        self.assertTrue(subscription.exists(connection=conn))
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % SUB_PATH)
        self.assertEqual(req.get('query_params'), None)

    def test_reload_w_connection_attr(self):
        PROJECT = 'PROJECT'
        SUB_NAME = 'sub_name'
        SUB_PATH = 'projects/%s/subscriptions/%s' % (PROJECT, SUB_NAME)
        TOPIC_NAME = 'topic_name'
        TOPIC_PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
        DEADLINE = 42
        ENDPOINT = 'https://api.example.com/push'
        conn = _Connection({'name': SUB_PATH,
                            'topic': TOPIC_PATH,
                            'ackDeadline': DEADLINE,
                            'pushConfig': {'pushEndpoint': ENDPOINT}})
        topic = _Topic(TOPIC_NAME, project=PROJECT, connection=conn)
        subscription = self._makeOne(SUB_NAME, topic)
        subscription.reload()
        self.assertEqual(subscription.ack_deadline, DEADLINE)
        self.assertEqual(subscription.push_endpoint, ENDPOINT)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % SUB_PATH)

    def test_reload_w_passed_connection(self):
        PROJECT = 'PROJECT'
        SUB_NAME = 'sub_name'
        SUB_PATH = 'projects/%s/subscriptions/%s' % (PROJECT, SUB_NAME)
        TOPIC_NAME = 'topic_name'
        TOPIC_PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
        DEADLINE = 42
        ENDPOINT = 'https://api.example.com/push'
        conn = _Connection({'name': SUB_PATH,
                            'topic': TOPIC_PATH,
                            'ackDeadline': DEADLINE,
                            'pushConfig': {'pushEndpoint': ENDPOINT}})
        topic = _Topic(TOPIC_NAME, project=PROJECT)
        subscription = self._makeOne(SUB_NAME, topic)
        subscription.reload(connection=conn)
        self.assertEqual(subscription.ack_deadline, DEADLINE)
        self.assertEqual(subscription.push_endpoint, ENDPOINT)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % SUB_PATH)

    def test_modify_push_config_w_endpoint_w_connection_attr(self):
        PROJECT = 'PROJECT'
        SUB_NAME = 'sub_name'
        SUB_PATH = 'projects/%s/subscriptions/%s' % (PROJECT, SUB_NAME)
        TOPIC_NAME = 'topic_name'
        ENDPOINT = 'https://api.example.com/push'
        conn = _Connection({})
        topic = _Topic(TOPIC_NAME, project=PROJECT, connection=conn)
        subscription = self._makeOne(SUB_NAME, topic)
        subscription.modify_push_configuration(push_endpoint=ENDPOINT)
        self.assertEqual(subscription.push_endpoint, ENDPOINT)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s:modifyPushConfig' % SUB_PATH)
        self.assertEqual(req['data'],
                         {'pushConfig': {'pushEndpoint': ENDPOINT}})

    def test_modify_push_config_wo_endpoint_w_passed_connection(self):
        PROJECT = 'PROJECT'
        SUB_NAME = 'sub_name'
        SUB_PATH = 'projects/%s/subscriptions/%s' % (PROJECT, SUB_NAME)
        TOPIC_NAME = 'topic_name'
        ENDPOINT = 'https://api.example.com/push'
        conn = _Connection({})
        topic = _Topic(TOPIC_NAME, project=PROJECT)
        subscription = self._makeOne(SUB_NAME, topic, push_endpoint=ENDPOINT)
        subscription.modify_push_configuration(push_endpoint=None,
                                               connection=conn)
        self.assertEqual(subscription.push_endpoint, None)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s:modifyPushConfig' % SUB_PATH)
        self.assertEqual(req['data'], {'pushConfig': {}})

    def test_pull_wo_return_immediately_wo_max_messages_w_conn_attr(self):
        import base64
        from gcloud.pubsub.message import Message
        PROJECT = 'PROJECT'
        SUB_NAME = 'sub_name'
        SUB_PATH = 'projects/%s/subscriptions/%s' % (PROJECT, SUB_NAME)
        TOPIC_NAME = 'topic_name'
        ACK_ID = 'DEADBEEF'
        MSG_ID = 'BEADCAFE'
        PAYLOAD = b'This is the message text'
        B64 = base64.b64encode(PAYLOAD)
        MESSAGE = {'messageId': MSG_ID, 'data': B64}
        REC_MESSAGE = {'ackId': ACK_ID, 'message': MESSAGE}
        conn = _Connection({'receivedMessages': [REC_MESSAGE]})
        topic = _Topic(TOPIC_NAME, project=PROJECT, connection=conn)
        subscription = self._makeOne(SUB_NAME, topic)
        pulled = subscription.pull()
        self.assertEqual(len(pulled), 1)
        ack_id, message = pulled[0]
        self.assertEqual(ack_id, ACK_ID)
        self.assertTrue(isinstance(message, Message))
        self.assertEqual(message.data, PAYLOAD)
        self.assertEqual(message.message_id, MSG_ID)
        self.assertEqual(message.attributes, {})
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s:pull' % SUB_PATH)
        self.assertEqual(req['data'],
                         {'returnImmediately': False, 'maxMessages': 1})

    def test_pull_w_return_immediately_w_max_messages_w_passed_conn(self):
        import base64
        from gcloud.pubsub.message import Message
        PROJECT = 'PROJECT'
        SUB_NAME = 'sub_name'
        SUB_PATH = 'projects/%s/subscriptions/%s' % (PROJECT, SUB_NAME)
        TOPIC_NAME = 'topic_name'
        ACK_ID = 'DEADBEEF'
        MSG_ID = 'BEADCAFE'
        PAYLOAD = b'This is the message text'
        B64 = base64.b64encode(PAYLOAD)
        MESSAGE = {'messageId': MSG_ID, 'data': B64, 'attributes': {'a': 'b'}}
        REC_MESSAGE = {'ackId': ACK_ID, 'message': MESSAGE}
        conn = _Connection({'receivedMessages': [REC_MESSAGE]})
        topic = _Topic(TOPIC_NAME, project=PROJECT)
        subscription = self._makeOne(SUB_NAME, topic)
        pulled = subscription.pull(return_immediately=True, max_messages=3,
                                   connection=conn)
        self.assertEqual(len(pulled), 1)
        ack_id, message = pulled[0]
        self.assertEqual(ack_id, ACK_ID)
        self.assertTrue(isinstance(message, Message))
        self.assertEqual(message.data, PAYLOAD)
        self.assertEqual(message.message_id, MSG_ID)
        self.assertEqual(message.attributes, {'a': 'b'})
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s:pull' % SUB_PATH)
        self.assertEqual(req['data'],
                         {'returnImmediately': True, 'maxMessages': 3})

    def test_acknowledge_w_connection_attr(self):
        PROJECT = 'PROJECT'
        SUB_NAME = 'sub_name'
        SUB_PATH = 'projects/%s/subscriptions/%s' % (PROJECT, SUB_NAME)
        TOPIC_NAME = 'topic_name'
        ACK_ID1 = 'DEADBEEF'
        ACK_ID2 = 'BEADCAFE'
        conn = _Connection({})
        topic = _Topic(TOPIC_NAME, project=PROJECT, connection=conn)
        subscription = self._makeOne(SUB_NAME, topic)
        subscription.acknowledge([ACK_ID1, ACK_ID2])
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s:acknowledge' % SUB_PATH)
        self.assertEqual(req['data'], {'ackIds': [ACK_ID1, ACK_ID2]})

    def test_acknowledge_w_passed_connection(self):
        PROJECT = 'PROJECT'
        SUB_NAME = 'sub_name'
        SUB_PATH = 'projects/%s/subscriptions/%s' % (PROJECT, SUB_NAME)
        TOPIC_NAME = 'topic_name'
        ACK_ID1 = 'DEADBEEF'
        ACK_ID2 = 'BEADCAFE'
        conn = _Connection({})
        topic = _Topic(TOPIC_NAME, project=PROJECT)
        subscription = self._makeOne(SUB_NAME, topic)
        subscription.acknowledge([ACK_ID1, ACK_ID2], connection=conn)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s:acknowledge' % SUB_PATH)
        self.assertEqual(req['data'], {'ackIds': [ACK_ID1, ACK_ID2]})

    def test_modify_ack_deadline_w_connection_attr(self):
        PROJECT = 'PROJECT'
        SUB_NAME = 'sub_name'
        SUB_PATH = 'projects/%s/subscriptions/%s' % (PROJECT, SUB_NAME)
        TOPIC_NAME = 'topic_name'
        ACK_ID = 'DEADBEEF'
        DEADLINE = 42
        conn = _Connection({})
        topic = _Topic(TOPIC_NAME, project=PROJECT, connection=conn)
        subscription = self._makeOne(SUB_NAME, topic)
        subscription.modify_ack_deadline(ACK_ID, DEADLINE)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s:modifyAckDeadline' % SUB_PATH)
        self.assertEqual(req['data'],
                         {'ackId': ACK_ID, 'ackDeadlineSeconds': DEADLINE})

    def test_modify_ack_deadline_w_passed_connection(self):
        PROJECT = 'PROJECT'
        SUB_NAME = 'sub_name'
        SUB_PATH = 'projects/%s/subscriptions/%s' % (PROJECT, SUB_NAME)
        TOPIC_NAME = 'topic_name'
        ACK_ID = 'DEADBEEF'
        DEADLINE = 42
        conn = _Connection({})
        topic = _Topic(TOPIC_NAME, project=PROJECT)
        subscription = self._makeOne(SUB_NAME, topic)
        subscription.modify_ack_deadline(ACK_ID, DEADLINE, connection=conn)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s:modifyAckDeadline' % SUB_PATH)
        self.assertEqual(req['data'],
                         {'ackId': ACK_ID, 'ackDeadlineSeconds': DEADLINE})

    def test_delete_w_connection_attr(self):
        PROJECT = 'PROJECT'
        SUB_NAME = 'sub_name'
        SUB_PATH = 'projects/%s/subscriptions/%s' % (PROJECT, SUB_NAME)
        TOPIC_NAME = 'topic_name'
        conn = _Connection({})
        topic = _Topic(TOPIC_NAME, project=PROJECT, connection=conn)
        subscription = self._makeOne(SUB_NAME, topic)
        subscription.delete()
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'DELETE')
        self.assertEqual(req['path'], '/%s' % SUB_PATH)

    def test_delete_w_passed_connection(self):
        PROJECT = 'PROJECT'
        SUB_NAME = 'sub_name'
        SUB_PATH = 'projects/%s/subscriptions/%s' % (PROJECT, SUB_NAME)
        TOPIC_NAME = 'topic_name'
        conn = _Connection({})
        topic = _Topic(TOPIC_NAME, project=PROJECT)
        subscription = self._makeOne(SUB_NAME, topic)
        subscription.delete(connection=conn)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'DELETE')
        self.assertEqual(req['path'], '/%s' % SUB_PATH)


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

    def __init__(self, name, project, connection=None):
        self.name = name
        self.project = project
        self.connection = connection
        self.full_name = 'projects/%s/topics/%s' % (project, name)
        self.path = '/projects/%s/topics/%s' % (project, name)
