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

    def test_ctor_w_explicit_timestamp(self):
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        CLIENT = _Client(project=PROJECT)
        topic = self._makeOne(TOPIC_NAME,
                              client=CLIENT,
                              timestamp_messages=True)
        self.assertEqual(topic.name, TOPIC_NAME)
        self.assertEqual(topic.project, PROJECT)
        self.assertEqual(topic.full_name,
                         'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME))
        self.assertTrue(topic.timestamp_messages)

    def test_from_api_repr(self):
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        CLIENT = _Client(project=PROJECT)
        PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
        resource = {'name': PATH}
        klass = self._getTargetClass()
        topic = klass.from_api_repr(resource, client=CLIENT)
        self.assertEqual(topic.name, TOPIC_NAME)
        self.assertTrue(topic._client is CLIENT)
        self.assertEqual(topic.project, PROJECT)
        self.assertEqual(topic.full_name, PATH)

    def test_from_api_repr_with_bad_client(self):
        TOPIC_NAME = 'topic_name'
        PROJECT1 = 'PROJECT1'
        PROJECT2 = 'PROJECT2'
        CLIENT = _Client(project=PROJECT1)
        PATH = 'projects/%s/topics/%s' % (PROJECT2, TOPIC_NAME)
        resource = {'name': PATH}
        klass = self._getTargetClass()
        self.assertRaises(ValueError, klass.from_api_repr,
                          resource, client=CLIENT)

    def test_create_w_bound_client(self):
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
        conn = _Connection({'name': PATH})
        CLIENT = _Client(project=PROJECT, connection=conn)
        topic = self._makeOne(TOPIC_NAME, client=CLIENT)
        topic.create()
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'PUT')
        self.assertEqual(req['path'], '/%s' % PATH)

    def test_create_w_alternate_client(self):
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
        conn1 = _Connection({'name': PATH})
        CLIENT1 = _Client(project=PROJECT, connection=conn1)
        conn2 = _Connection({'name': PATH})
        CLIENT2 = _Client(project=PROJECT, connection=conn2)
        topic = self._makeOne(TOPIC_NAME, client=CLIENT1)
        topic.create(client=CLIENT2)
        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'PUT')
        self.assertEqual(req['path'], '/%s' % PATH)

    def test_exists_miss_w_bound_client(self):
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
        conn = _Connection()
        CLIENT = _Client(project=PROJECT, connection=conn)
        topic = self._makeOne(TOPIC_NAME, client=CLIENT)
        self.assertFalse(topic.exists())
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)

    def test_exists_hit_w_alternate_client(self):
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
        conn1 = _Connection({'name': PATH})
        CLIENT1 = _Client(project=PROJECT, connection=conn1)
        conn2 = _Connection({'name': PATH})
        CLIENT2 = _Client(project=PROJECT, connection=conn2)
        topic = self._makeOne(TOPIC_NAME, client=CLIENT1)
        self.assertTrue(topic.exists(client=CLIENT2))
        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)

    def test_publish_single_bytes_wo_attrs_w_bound_client(self):
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
        CLIENT = _Client(project=PROJECT, connection=conn)
        topic = self._makeOne(TOPIC_NAME, client=CLIENT)
        msgid = topic.publish(PAYLOAD)
        self.assertEqual(msgid, MSGID)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s:publish' % PATH)
        self.assertEqual(req['data'], {'messages': [MESSAGE]})

    def test_publish_single_bytes_wo_attrs_w_add_timestamp_alt_client(self):
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
        conn1 = _Connection({'messageIds': [MSGID]})
        CLIENT1 = _Client(project=PROJECT, connection=conn1)
        conn2 = _Connection({'messageIds': [MSGID]})
        CLIENT2 = _Client(project=PROJECT, connection=conn2)

        topic = self._makeOne(TOPIC_NAME, client=CLIENT1,
                              timestamp_messages=True)
        with _Monkey(MUT, _NOW=_utcnow):
            msgid = topic.publish(PAYLOAD, client=CLIENT2)

        self.assertEqual(msgid, MSGID)
        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
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
        CLIENT = _Client(project=PROJECT, connection=conn)
        topic = self._makeOne(TOPIC_NAME, client=CLIENT,
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
        CLIENT = _Client(project=PROJECT, connection=conn)
        topic = self._makeOne(TOPIC_NAME, client=CLIENT)
        msgid = topic.publish(PAYLOAD, attr1='value1', attr2='value2')
        self.assertEqual(msgid, MSGID)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s:publish' % PATH)
        self.assertEqual(req['data'], {'messages': [MESSAGE]})

    def test_publish_multiple_w_bound_client(self):
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
        CLIENT = _Client(project=PROJECT, connection=conn)
        topic = self._makeOne(TOPIC_NAME, client=CLIENT)
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

    def test_publish_multiple_w_alternate_client(self):
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
        conn1 = _Connection({'messageIds': [MSGID1, MSGID2]})
        CLIENT1 = _Client(project=PROJECT, connection=conn1)
        conn2 = _Connection({'messageIds': [MSGID1, MSGID2]})
        CLIENT2 = _Client(project=PROJECT, connection=conn2)
        topic = self._makeOne(TOPIC_NAME, client=CLIENT1)
        with topic.batch(client=CLIENT2) as batch:
            batch.publish(PAYLOAD1)
            batch.publish(PAYLOAD2, attr1='value1', attr2='value2')
        self.assertEqual(list(batch), [MSGID1, MSGID2])
        self.assertEqual(list(batch.messages), [])
        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
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
        CLIENT = _Client(project=PROJECT)
        topic = self._makeOne(TOPIC_NAME, client=CLIENT)
        try:
            with topic.batch() as batch:
                batch.publish(PAYLOAD1)
                batch.publish(PAYLOAD2, attr1='value1', attr2='value2')
                raise _Bugout()
        except _Bugout:
            pass
        self.assertEqual(list(batch), [])
        self.assertEqual(len(conn._requested), 0)

    def test_delete_w_bound_client(self):
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
        conn = _Connection({})
        CLIENT = _Client(project=PROJECT, connection=conn)
        topic = self._makeOne(TOPIC_NAME, client=CLIENT)
        topic.delete()
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'DELETE')
        self.assertEqual(req['path'], '/%s' % PATH)

    def test_delete_w_alternate_client(self):
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
        conn1 = _Connection({})
        CLIENT1 = _Client(project=PROJECT, connection=conn1)
        conn2 = _Connection({})
        CLIENT2 = _Client(project=PROJECT, connection=conn2)
        topic = self._makeOne(TOPIC_NAME, client=CLIENT1)
        topic.delete(client=CLIENT2)
        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'DELETE')
        self.assertEqual(req['path'], '/%s' % PATH)

    def test_subscription(self):
        from gcloud.pubsub.subscription import Subscription
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        CLIENT = _Client(project=PROJECT)
        topic = self._makeOne(TOPIC_NAME, client=CLIENT)

        SUBSCRIPTION_NAME = 'subscription_name'
        subscription = topic.subscription(SUBSCRIPTION_NAME)
        self.assertTrue(isinstance(subscription, Subscription))
        self.assertEqual(subscription.name, SUBSCRIPTION_NAME)
        self.assertTrue(subscription.topic is topic)

    def test_list_subscriptions_no_paging(self):
        from gcloud.pubsub.subscription import Subscription
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        SUB_NAME_1 = 'subscription_1'
        SUB_PATH_1 = 'projects/%s/subscriptions/%s' % (PROJECT, SUB_NAME_1)
        SUB_NAME_2 = 'subscription_2'
        SUB_PATH_2 = 'projects/%s/subscriptions/%s' % (PROJECT, SUB_NAME_2)
        TOPIC_NAME = 'topic_name'
        SUBS_LIST = [SUB_PATH_1, SUB_PATH_2]
        TOKEN = 'TOKEN'
        RETURNED = {'subscriptions': SUBS_LIST, 'nextPageToken': TOKEN}

        conn = _Connection(RETURNED)
        CLIENT = _Client(project=PROJECT, connection=conn)
        topic = self._makeOne(TOPIC_NAME, client=CLIENT)

        # Execute request.
        subscriptions, next_page_token = topic.list_subscriptions()
        # Test values are correct.
        self.assertEqual(len(subscriptions), 2)

        subscription = subscriptions[0]
        self.assertTrue(isinstance(subscription, Subscription))
        self.assertEqual(subscriptions[0].name, SUB_NAME_1)
        self.assertTrue(subscription.topic is topic)

        subscription = subscriptions[1]
        self.assertTrue(isinstance(subscription, Subscription))
        self.assertEqual(subscriptions[1].name, SUB_NAME_2)
        self.assertTrue(subscription.topic is topic)

        self.assertEqual(next_page_token, TOKEN)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'],
                         '/projects/%s/topics/%s/subscriptions'
                         % (PROJECT, TOPIC_NAME))
        self.assertEqual(req['query_params'], {})

    def test_list_subscriptions_with_paging(self):
        from gcloud.pubsub.subscription import Subscription
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        SUB_NAME_1 = 'subscription_1'
        SUB_PATH_1 = 'projects/%s/subscriptions/%s' % (PROJECT, SUB_NAME_1)
        SUB_NAME_2 = 'subscription_2'
        SUB_PATH_2 = 'projects/%s/subscriptions/%s' % (PROJECT, SUB_NAME_2)
        TOPIC_NAME = 'topic_name'
        SUBS_LIST = [SUB_PATH_1, SUB_PATH_2]
        PAGE_SIZE = 10
        TOKEN = 'TOKEN'
        RETURNED = {'subscriptions': SUBS_LIST}

        conn = _Connection(RETURNED)
        CLIENT = _Client(project=PROJECT, connection=conn)
        topic = self._makeOne(TOPIC_NAME, client=CLIENT)

        # Execute request.
        subscriptions, next_page_token = topic.list_subscriptions(
            page_size=PAGE_SIZE, page_token=TOKEN)
        # Test values are correct.
        self.assertEqual(len(subscriptions), 2)

        subscription = subscriptions[0]
        self.assertTrue(isinstance(subscription, Subscription))
        self.assertEqual(subscriptions[0].name, SUB_NAME_1)
        self.assertTrue(subscription.topic is topic)

        subscription = subscriptions[1]
        self.assertTrue(isinstance(subscription, Subscription))
        self.assertEqual(subscriptions[1].name, SUB_NAME_2)
        self.assertTrue(subscription.topic is topic)

        self.assertEqual(next_page_token, None)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'],
                         '/projects/%s/topics/%s/subscriptions'
                         % (PROJECT, TOPIC_NAME))
        self.assertEqual(req['query_params'],
                         {'pageSize': PAGE_SIZE, 'pageToken': TOKEN})

    def test_list_subscriptions_missing_key(self):
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        TOPIC_NAME = 'topic_name'

        conn = _Connection({})
        CLIENT = _Client(project=PROJECT, connection=conn)
        topic = self._makeOne(TOPIC_NAME, client=CLIENT)

        # Execute request.
        subscriptions, next_page_token = topic.list_subscriptions()
        # Test values are correct.
        self.assertEqual(len(subscriptions), 0)
        self.assertEqual(next_page_token, None)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'],
                         '/projects/%s/topics/%s/subscriptions'
                         % (PROJECT, TOPIC_NAME))
        self.assertEqual(req['query_params'], {})

    def test_get_iam_policy_w_bound_client(self):
        from gcloud.pubsub.iam import OWNER_ROLE, EDITOR_ROLE, VIEWER_ROLE
        OWNER1 = 'user:phred@example.com'
        OWNER2 = 'group:cloud-logs@google.com'
        EDITOR1 = 'domain:google.com'
        EDITOR2 = 'user:phred@example.com'
        VIEWER1 = 'serviceAccount:1234-abcdef@service.example.com'
        VIEWER2 = 'user:phred@example.com'
        POLICY = {
            'etag': 'DEADBEEF',
            'version': 17,
            'bindings': [
                {'role': OWNER_ROLE, 'members': [OWNER1, OWNER2]},
                {'role': EDITOR_ROLE, 'members': [EDITOR1, EDITOR2]},
                {'role': VIEWER_ROLE, 'members': [VIEWER1, VIEWER2]},
            ],
        }
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        TOPIC_NAME = 'topic_name'
        PATH = 'projects/%s/topics/%s:getIamPolicy' % (PROJECT, TOPIC_NAME)

        conn = _Connection(POLICY)
        CLIENT = _Client(project=PROJECT, connection=conn)
        topic = self._makeOne(TOPIC_NAME, client=CLIENT)

        policy = topic.get_iam_policy()

        self.assertEqual(policy.etag, 'DEADBEEF')
        self.assertEqual(policy.version, 17)
        self.assertEqual(sorted(policy.owners), [OWNER2, OWNER1])
        self.assertEqual(sorted(policy.editors), [EDITOR1, EDITOR2])
        self.assertEqual(sorted(policy.viewers), [VIEWER1, VIEWER2])

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)

    def test_get_iam_policy_w_alternate_client(self):
        POLICY = {
            'etag': 'ACAB',
        }
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        TOPIC_NAME = 'topic_name'
        PATH = 'projects/%s/topics/%s:getIamPolicy' % (PROJECT, TOPIC_NAME)

        conn1 = _Connection()
        conn2 = _Connection(POLICY)
        CLIENT1 = _Client(project=PROJECT, connection=conn1)
        CLIENT2 = _Client(project=PROJECT, connection=conn2)
        topic = self._makeOne(TOPIC_NAME, client=CLIENT1)

        policy = topic.get_iam_policy(client=CLIENT2)

        self.assertEqual(policy.etag, 'ACAB')
        self.assertEqual(policy.version, None)
        self.assertEqual(sorted(policy.owners), [])
        self.assertEqual(sorted(policy.editors), [])
        self.assertEqual(sorted(policy.viewers), [])

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)

    def test_set_iam_policy_w_bound_client(self):
        from gcloud.pubsub.iam import Policy
        from gcloud.pubsub.iam import OWNER_ROLE, EDITOR_ROLE, VIEWER_ROLE
        OWNER1 = 'group:cloud-logs@google.com'
        OWNER2 = 'user:phred@example.com'
        EDITOR1 = 'domain:google.com'
        EDITOR2 = 'user:phred@example.com'
        VIEWER1 = 'serviceAccount:1234-abcdef@service.example.com'
        VIEWER2 = 'user:phred@example.com'
        POLICY = {
            'etag': 'DEADBEEF',
            'version': 17,
            'bindings': [
                {'role': OWNER_ROLE, 'members': [OWNER1, OWNER2]},
                {'role': EDITOR_ROLE, 'members': [EDITOR1, EDITOR2]},
                {'role': VIEWER_ROLE, 'members': [VIEWER1, VIEWER2]},
            ],
        }
        RESPONSE = POLICY.copy()
        RESPONSE['etag'] = 'ABACABAF'
        RESPONSE['version'] = 18
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        TOPIC_NAME = 'topic_name'
        PATH = 'projects/%s/topics/%s:setIamPolicy' % (PROJECT, TOPIC_NAME)

        conn = _Connection(RESPONSE)
        CLIENT = _Client(project=PROJECT, connection=conn)
        topic = self._makeOne(TOPIC_NAME, client=CLIENT)
        policy = Policy('DEADBEEF', 17)
        policy.owners.add(OWNER1)
        policy.owners.add(OWNER2)
        policy.editors.add(EDITOR1)
        policy.editors.add(EDITOR2)
        policy.viewers.add(VIEWER1)
        policy.viewers.add(VIEWER2)

        new_policy = topic.set_iam_policy(policy)

        self.assertEqual(new_policy.etag, 'ABACABAF')
        self.assertEqual(new_policy.version, 18)
        self.assertEqual(sorted(new_policy.owners), [OWNER1, OWNER2])
        self.assertEqual(sorted(new_policy.editors), [EDITOR1, EDITOR2])
        self.assertEqual(sorted(new_policy.viewers), [VIEWER1, VIEWER2])

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % PATH)
        self.assertEqual(req['data'], {'policy': POLICY})

    def test_set_iam_policy_w_alternate_client(self):
        from gcloud.pubsub.iam import Policy
        RESPONSE = {'etag': 'ACAB'}
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        TOPIC_NAME = 'topic_name'
        PATH = 'projects/%s/topics/%s:setIamPolicy' % (PROJECT, TOPIC_NAME)

        conn1 = _Connection()
        conn2 = _Connection(RESPONSE)
        CLIENT1 = _Client(project=PROJECT, connection=conn1)
        CLIENT2 = _Client(project=PROJECT, connection=conn2)
        topic = self._makeOne(TOPIC_NAME, client=CLIENT1)

        policy = Policy()
        new_policy = topic.set_iam_policy(policy, client=CLIENT2)

        self.assertEqual(new_policy.etag, 'ACAB')
        self.assertEqual(new_policy.version, None)
        self.assertEqual(sorted(new_policy.owners), [])
        self.assertEqual(sorted(new_policy.editors), [])
        self.assertEqual(sorted(new_policy.viewers), [])

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % PATH)
        self.assertEqual(req['data'], {'policy': {}})

    def test_check_iam_permissions_w_bound_client(self):
        from gcloud.pubsub.iam import OWNER_ROLE, EDITOR_ROLE, VIEWER_ROLE
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        PATH = 'projects/%s/topics/%s:testIamPermissions' % (
            PROJECT, TOPIC_NAME)
        ROLES = [VIEWER_ROLE, EDITOR_ROLE, OWNER_ROLE]
        REQUESTED = {
            'permissions': ROLES,
        }
        RESPONSE = {
            'permissions': ROLES[:-1],
        }
        conn = _Connection(RESPONSE)
        CLIENT = _Client(project=PROJECT, connection=conn)
        topic = self._makeOne(TOPIC_NAME, client=CLIENT)

        allowed = topic.check_iam_permissions(ROLES)

        self.assertEqual(allowed, ROLES[:-1])
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % PATH)
        self.assertEqual(req['data'], REQUESTED)

    def test_check_iam_permissions_w_alternate_client(self):
        from gcloud.pubsub.iam import OWNER_ROLE, EDITOR_ROLE, VIEWER_ROLE
        TOPIC_NAME = 'topic_name'
        PROJECT = 'PROJECT'
        PATH = 'projects/%s/topics/%s:testIamPermissions' % (
            PROJECT, TOPIC_NAME)
        ROLES = [VIEWER_ROLE, EDITOR_ROLE, OWNER_ROLE]
        REQUESTED = {
            'permissions': ROLES,
        }
        RESPONSE = {}
        conn1 = _Connection()
        CLIENT1 = _Client(project=PROJECT, connection=conn1)
        conn2 = _Connection(RESPONSE)
        CLIENT2 = _Client(project=PROJECT, connection=conn2)
        topic = self._makeOne(TOPIC_NAME, client=CLIENT1)

        allowed = topic.check_iam_permissions(ROLES, client=CLIENT2)

        self.assertEqual(len(allowed), 0)
        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % PATH)
        self.assertEqual(req['data'], REQUESTED)


class TestBatch(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.pubsub.topic import Batch
        return Batch

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_ctor_defaults(self):
        topic = _Topic()
        CLIENT = _Client(project='PROJECT')
        batch = self._makeOne(topic, CLIENT)
        self.assertTrue(batch.topic is topic)
        self.assertTrue(batch.client is CLIENT)
        self.assertEqual(len(batch.messages), 0)
        self.assertEqual(len(batch.message_ids), 0)

    def test___iter___empty(self):
        topic = _Topic()
        client = object()
        batch = self._makeOne(topic, client)
        self.assertEqual(list(batch), [])

    def test___iter___non_empty(self):
        topic = _Topic()
        client = object()
        batch = self._makeOne(topic, client)
        batch.message_ids[:] = ['ONE', 'TWO', 'THREE']
        self.assertEqual(list(batch), ['ONE', 'TWO', 'THREE'])

    def test_publish_bytes_wo_attrs(self):
        import base64
        PAYLOAD = b'This is the message text'
        B64 = base64.b64encode(PAYLOAD).decode('ascii')
        MESSAGE = {'data': B64,
                   'attributes': {}}
        connection = _Connection()
        CLIENT = _Client(project='PROJECT', connection=connection)
        topic = _Topic()
        batch = self._makeOne(topic, client=CLIENT)
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
        CLIENT = _Client(project='PROJECT', connection=connection)
        topic = _Topic(timestamp_messages=True)
        batch = self._makeOne(topic, client=CLIENT)
        batch.publish(PAYLOAD)
        self.assertEqual(len(connection._requested), 0)
        self.assertEqual(batch.messages, [MESSAGE])

    def test_commit_w_bound_client(self):
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
        CLIENT = _Client(project='PROJECT', connection=conn)
        topic = _Topic()
        batch = self._makeOne(topic, client=CLIENT)
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

    def test_commit_w_alternate_client(self):
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
        conn1 = _Connection({'messageIds': [MSGID1, MSGID2]})
        CLIENT1 = _Client(project='PROJECT', connection=conn1)
        conn2 = _Connection({'messageIds': [MSGID1, MSGID2]})
        CLIENT2 = _Client(project='PROJECT', connection=conn2)
        topic = _Topic()
        batch = self._makeOne(topic, client=CLIENT1)
        batch.publish(PAYLOAD1)
        batch.publish(PAYLOAD2, attr1='value1', attr2='value2')
        batch.commit(client=CLIENT2)
        self.assertEqual(list(batch), [MSGID1, MSGID2])
        self.assertEqual(list(batch.messages), [])
        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
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
        CLIENT = _Client(project='PROJECT', connection=conn)
        topic = _Topic()
        batch = self._makeOne(topic, client=CLIENT)

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
        CLIENT = _Client(project='PROJECT', connection=conn)
        topic = _Topic()
        batch = self._makeOne(topic, client=CLIENT)

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
                 timestamp_messages=False):
        self.path = '/projects/%s/topics/%s' % (project, name)
        self.timestamp_messages = timestamp_messages

    def _timestamp_message(self, attrs):
        if self.timestamp_messages:
            attrs['timestamp'] = 'TIMESTAMP'


class _Client(object):

    def __init__(self, project, connection=None):
        self.project = project
        self.connection = connection


class _Bugout(Exception):
    pass
