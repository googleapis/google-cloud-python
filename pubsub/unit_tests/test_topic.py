# Copyright 2015 Google Inc.
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


def _make_credentials():
    import google.auth.credentials

    return mock.Mock(spec=google.auth.credentials.Credentials)


class TestTopic(unittest.TestCase):
    PROJECT = 'PROJECT'
    TOPIC_NAME = 'topic_name'
    TOPIC_PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)

    @staticmethod
    def _get_target_class():
        from google.cloud.pubsub.topic import Topic

        return Topic

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor_w_explicit_timestamp(self):
        client = _Client(project=self.PROJECT)
        topic = self._make_one(self.TOPIC_NAME,
                               client=client,
                               timestamp_messages=True)
        self.assertEqual(topic.name, self.TOPIC_NAME)
        self.assertEqual(topic.project, self.PROJECT)
        self.assertEqual(topic.full_name, self.TOPIC_PATH)
        self.assertTrue(topic.timestamp_messages)

    def test_from_api_repr(self):
        client = _Client(project=self.PROJECT)
        resource = {'name': self.TOPIC_PATH}
        klass = self._get_target_class()
        topic = klass.from_api_repr(resource, client=client)
        self.assertEqual(topic.name, self.TOPIC_NAME)
        self.assertIs(topic._client, client)
        self.assertEqual(topic.project, self.PROJECT)
        self.assertEqual(topic.full_name, self.TOPIC_PATH)

    def test_from_api_repr_with_bad_client(self):
        PROJECT1 = 'PROJECT1'
        PROJECT2 = 'PROJECT2'
        client = _Client(project=PROJECT1)
        PATH = 'projects/%s/topics/%s' % (PROJECT2, self.TOPIC_NAME)
        resource = {'name': PATH}
        klass = self._get_target_class()
        self.assertRaises(ValueError, klass.from_api_repr,
                          resource, client=client)

    def test_create_w_bound_client(self):
        client = _Client(project=self.PROJECT)
        api = client.publisher_api = _FauxPublisherAPI()
        api._topic_create_response = {'name': self.TOPIC_PATH}
        topic = self._make_one(self.TOPIC_NAME, client=client)

        topic.create()

        self.assertEqual(api._topic_created, self.TOPIC_PATH)

    def test_create_w_alternate_client(self):
        client1 = _Client(project=self.PROJECT)
        client2 = _Client(project=self.PROJECT)
        api = client2.publisher_api = _FauxPublisherAPI()
        api._topic_create_response = {'name': self.TOPIC_PATH}
        topic = self._make_one(self.TOPIC_NAME, client=client1)

        topic.create(client=client2)

        self.assertEqual(api._topic_created, self.TOPIC_PATH)

    def test_exists_miss_w_bound_client(self):
        client = _Client(project=self.PROJECT)
        api = client.publisher_api = _FauxPublisherAPI()
        topic = self._make_one(self.TOPIC_NAME, client=client)

        self.assertFalse(topic.exists())

        self.assertEqual(api._topic_got, self.TOPIC_PATH)

    def test_exists_hit_w_alternate_client(self):
        client1 = _Client(project=self.PROJECT)
        client2 = _Client(project=self.PROJECT)
        api = client2.publisher_api = _FauxPublisherAPI()
        api._topic_get_response = {'name': self.TOPIC_PATH}
        topic = self._make_one(self.TOPIC_NAME, client=client1)

        self.assertTrue(topic.exists(client=client2))

        self.assertEqual(api._topic_got, self.TOPIC_PATH)

    def test_delete_w_bound_client(self):
        client = _Client(project=self.PROJECT)
        api = client.publisher_api = _FauxPublisherAPI()
        api._topic_delete_response = {}
        topic = self._make_one(self.TOPIC_NAME, client=client)

        topic.delete()

        self.assertEqual(api._topic_deleted, self.TOPIC_PATH)

    def test_delete_w_alternate_client(self):
        client1 = _Client(project=self.PROJECT)
        client2 = _Client(project=self.PROJECT)
        api = client2.publisher_api = _FauxPublisherAPI()
        api._topic_delete_response = {}
        topic = self._make_one(self.TOPIC_NAME, client=client1)

        topic.delete(client=client2)

        self.assertEqual(api._topic_deleted, self.TOPIC_PATH)

    def test_publish_single_bytes_wo_attrs_w_bound_client(self):
        PAYLOAD = 'This is the message text'
        MSGID = 'DEADBEEF'
        MESSAGE = {'data': PAYLOAD, 'attributes': {}}
        client = _Client(project=self.PROJECT)
        api = client.publisher_api = _FauxPublisherAPI()
        api._topic_publish_response = [MSGID]
        topic = self._make_one(self.TOPIC_NAME, client=client)

        msgid = topic.publish(PAYLOAD)

        self.assertEqual(msgid, MSGID)
        self.assertEqual(api._topic_published, (self.TOPIC_PATH, [MESSAGE]))

    def test_publish_single_bytes_wo_attrs_w_add_timestamp_alt_client(self):
        import datetime
        from google.cloud._helpers import _RFC3339_MICROS

        NOW = datetime.datetime.utcnow()

        def _utcnow():
            return NOW

        PAYLOAD = 'This is the message text'
        MSGID = 'DEADBEEF'
        MESSAGE = {
            'data': PAYLOAD,
            'attributes': {'timestamp': NOW.strftime(_RFC3339_MICROS)},
        }
        client1 = _Client(project=self.PROJECT)
        client2 = _Client(project=self.PROJECT)
        api = client2.publisher_api = _FauxPublisherAPI()
        api._topic_publish_response = [MSGID]

        topic = self._make_one(self.TOPIC_NAME, client=client1,
                               timestamp_messages=True)
        with mock.patch('google.cloud.pubsub.topic._NOW', new=_utcnow):
            msgid = topic.publish(PAYLOAD, client=client2)

        self.assertEqual(msgid, MSGID)
        self.assertEqual(api._topic_published, (self.TOPIC_PATH, [MESSAGE]))

    def test_publish_single_bytes_w_add_timestamp_w_ts_in_attrs(self):
        PAYLOAD = 'This is the message text'
        MSGID = 'DEADBEEF'
        OVERRIDE = '2015-04-10T16:46:22.868399Z'
        MESSAGE = {'data': PAYLOAD,
                   'attributes': {'timestamp': OVERRIDE}}
        client = _Client(project=self.PROJECT)
        api = client.publisher_api = _FauxPublisherAPI()
        api._topic_publish_response = [MSGID]
        topic = self._make_one(self.TOPIC_NAME, client=client,
                               timestamp_messages=True)

        msgid = topic.publish(PAYLOAD, timestamp=OVERRIDE)

        self.assertEqual(msgid, MSGID)
        self.assertEqual(api._topic_published, (self.TOPIC_PATH, [MESSAGE]))

    def test_publish_single_w_attrs(self):
        PAYLOAD = 'This is the message text'
        MSGID = 'DEADBEEF'
        MESSAGE = {'data': PAYLOAD,
                   'attributes': {'attr1': 'value1', 'attr2': 'value2'}}
        client = _Client(project=self.PROJECT)
        api = client.publisher_api = _FauxPublisherAPI()
        api._topic_publish_response = [MSGID]
        topic = self._make_one(self.TOPIC_NAME, client=client)

        msgid = topic.publish(PAYLOAD, attr1='value1', attr2='value2')

        self.assertEqual(msgid, MSGID)
        self.assertEqual(api._topic_published, (self.TOPIC_PATH, [MESSAGE]))

    def test_publish_with_gax(self):
        PAYLOAD = 'This is the message text'
        MSGID = 'DEADBEEF'
        MESSAGE = {'data': PAYLOAD, 'attributes': {}}
        client = _Client(project=self.PROJECT)
        api = client.publisher_api = _FauxPublisherAPI()
        api._topic_publish_response = [MSGID]
        topic = self._make_one(self.TOPIC_NAME, client=client)
        msgid = topic.publish(PAYLOAD)

        self.assertEqual(msgid, MSGID)
        self.assertEqual(api._topic_published, (self.TOPIC_PATH, [MESSAGE]))

    def test_publish_without_gax(self):
        PAYLOAD = 'This is the message text'
        MSGID = 'DEADBEEF'
        MESSAGE = {'data': PAYLOAD, 'attributes': {}}
        client = _Client(project=self.PROJECT)
        api = client.publisher_api = _FauxPublisherAPI()
        api._topic_publish_response = [MSGID]
        topic = self._make_one(self.TOPIC_NAME, client=client)
        msgid = topic.publish(PAYLOAD)

        self.assertEqual(msgid, MSGID)
        self.assertEqual(api._topic_published, (self.TOPIC_PATH, [MESSAGE]))

    def test_publish_multiple_w_bound_client(self):
        PAYLOAD1 = 'This is the first message text'
        PAYLOAD2 = 'This is the second message text'
        MSGID1 = 'DEADBEEF'
        MSGID2 = 'BEADCAFE'
        MESSAGE1 = {'data': PAYLOAD1, 'attributes': {}}
        MESSAGE2 = {'data': PAYLOAD2,
                    'attributes': {'attr1': 'value1', 'attr2': 'value2'}}
        client = _Client(project=self.PROJECT)
        api = client.publisher_api = _FauxPublisherAPI()
        api._topic_publish_response = [MSGID1, MSGID2]
        topic = self._make_one(self.TOPIC_NAME, client=client)

        with topic.batch() as batch:
            batch.publish(PAYLOAD1)
            batch.publish(PAYLOAD2, attr1='value1', attr2='value2')

        self.assertEqual(list(batch), [MSGID1, MSGID2])
        self.assertEqual(list(batch.messages), [])
        self.assertEqual(api._topic_published,
                         (self.TOPIC_PATH, [MESSAGE1, MESSAGE2]))

    def test_publish_w_no_messages(self):
        client = _Client(project=self.PROJECT)
        api = client.publisher_api = _FauxPublisherAPI()
        api._topic_publish_response = []
        topic = self._make_one(self.TOPIC_NAME, client=client)

        with topic.batch() as batch:
            pass

        self.assertEqual(list(batch.messages), [])
        self.assertEqual(api._api_called, 0)

    def test_publish_multiple_w_alternate_client(self):
        PAYLOAD1 = 'This is the first message text'
        PAYLOAD2 = 'This is the second message text'
        MSGID1 = 'DEADBEEF'
        MSGID2 = 'BEADCAFE'
        MESSAGE1 = {'data': PAYLOAD1, 'attributes': {}}
        MESSAGE2 = {
            'data': PAYLOAD2,
            'attributes': {'attr1': 'value1', 'attr2': 'value2'},
        }
        client1 = _Client(project=self.PROJECT)
        client2 = _Client(project=self.PROJECT)
        api = client2.publisher_api = _FauxPublisherAPI()
        api._topic_publish_response = [MSGID1, MSGID2]
        topic = self._make_one(self.TOPIC_NAME, client=client1)

        with topic.batch(client=client2) as batch:
            batch.publish(PAYLOAD1)
            batch.publish(PAYLOAD2, attr1='value1', attr2='value2')

        self.assertEqual(list(batch), [MSGID1, MSGID2])
        self.assertEqual(list(batch.messages), [])
        self.assertEqual(api._topic_published,
                         (self.TOPIC_PATH, [MESSAGE1, MESSAGE2]))

    def test_publish_multiple_error(self):
        PAYLOAD1 = b'This is the first message text'
        PAYLOAD2 = b'This is the second message text'
        client = _Client(project=self.PROJECT)
        api = client.publisher_api = _FauxPublisherAPI()
        topic = self._make_one(self.TOPIC_NAME, client=client)

        try:
            with topic.batch() as batch:
                batch.publish(PAYLOAD1)
                batch.publish(PAYLOAD2, attr1='value1', attr2='value2')
                raise _Bugout()
        except _Bugout:
            pass

        self.assertEqual(list(batch), [])
        self.assertEqual(getattr(api, '_topic_published', self), self)

    def test_subscription(self):
        from google.cloud.pubsub.subscription import Subscription

        client = _Client(project=self.PROJECT)
        topic = self._make_one(self.TOPIC_NAME, client=client)

        SUBSCRIPTION_NAME = 'subscription_name'
        subscription = topic.subscription(SUBSCRIPTION_NAME)
        self.assertIsInstance(subscription, Subscription)
        self.assertEqual(subscription.name, SUBSCRIPTION_NAME)
        self.assertIs(subscription.topic, topic)

    def test_list_subscriptions_no_paging(self):
        import six
        from google.cloud.pubsub.client import Client
        from google.cloud.pubsub.subscription import Subscription

        client = Client(project=self.PROJECT,
                        credentials=_make_credentials(), use_gax=False)

        SUB_NAME_1 = 'subscription_1'
        SUB_PATH_1 = 'projects/%s/subscriptions/%s' % (
            self.PROJECT, SUB_NAME_1)
        SUB_NAME_2 = 'subscription_2'
        SUB_PATH_2 = 'projects/%s/subscriptions/%s' % (
            self.PROJECT, SUB_NAME_2)
        SUBS_LIST = [SUB_PATH_1, SUB_PATH_2]
        TOKEN = 'TOKEN'

        returned = {
            'subscriptions': SUBS_LIST,
            'nextPageToken': TOKEN,
        }
        client._connection = _Connection(returned)

        topic = self._make_one(self.TOPIC_NAME, client=client)

        iterator = topic.list_subscriptions()
        page = six.next(iterator.pages)
        subscriptions = list(page)
        next_page_token = iterator.next_page_token

        self.assertEqual(len(subscriptions), 2)

        subscription = subscriptions[0]
        self.assertIsInstance(subscription, Subscription)
        self.assertEqual(subscriptions[0].name, SUB_NAME_1)
        self.assertIs(subscription.topic, topic)

        subscription = subscriptions[1]
        self.assertIsInstance(subscription, Subscription)
        self.assertEqual(subscriptions[1].name, SUB_NAME_2)
        self.assertIs(subscription.topic, topic)

        self.assertEqual(next_page_token, TOKEN)
        # Verify the mock.
        called_with = client._connection._called_with
        self.assertEqual(len(called_with), 3)
        self.assertEqual(called_with['method'], 'GET')
        path = '/%s/subscriptions' % (self.TOPIC_PATH,)
        self.assertEqual(called_with['path'], path)
        self.assertEqual(called_with['query_params'], {})

    def test_list_subscriptions_with_paging(self):
        from google.cloud.pubsub.client import Client
        from google.cloud.pubsub.subscription import Subscription

        client = Client(project=self.PROJECT,
                        credentials=_make_credentials(), use_gax=False)

        SUB_NAME_1 = 'subscription_1'
        SUB_PATH_1 = 'projects/%s/subscriptions/%s' % (
            self.PROJECT, SUB_NAME_1)
        SUB_NAME_2 = 'subscription_2'
        SUB_PATH_2 = 'projects/%s/subscriptions/%s' % (
            self.PROJECT, SUB_NAME_2)
        SUBS_LIST = [SUB_PATH_1, SUB_PATH_2]
        PAGE_SIZE = 10
        TOKEN = 'TOKEN'

        returned = {
            'subscriptions': SUBS_LIST,
        }
        client._connection = _Connection(returned)

        topic = self._make_one(self.TOPIC_NAME, client=client)

        iterator = topic.list_subscriptions(
            page_size=PAGE_SIZE, page_token=TOKEN)
        subscriptions = list(iterator)
        next_page_token = iterator.next_page_token

        self.assertEqual(len(subscriptions), 2)

        subscription = subscriptions[0]
        self.assertIsInstance(subscription, Subscription)
        self.assertEqual(subscriptions[0].name, SUB_NAME_1)
        self.assertIs(subscription.topic, topic)

        subscription = subscriptions[1]
        self.assertIsInstance(subscription, Subscription)
        self.assertEqual(subscriptions[1].name, SUB_NAME_2)
        self.assertIs(subscription.topic, topic)

        self.assertIsNone(next_page_token)
        # Verify the mock.
        called_with = client._connection._called_with
        self.assertEqual(len(called_with), 3)
        self.assertEqual(called_with['method'], 'GET')
        path = '/%s/subscriptions' % (self.TOPIC_PATH,)
        self.assertEqual(called_with['path'], path)
        self.assertEqual(called_with['query_params'],
                         {'pageSize': PAGE_SIZE, 'pageToken': TOKEN})

    def test_list_subscriptions_missing_key(self):
        from google.cloud.pubsub.client import Client

        client = Client(project=self.PROJECT,
                        credentials=_make_credentials(), use_gax=False)
        client._connection = _Connection({})
        topic = self._make_one(self.TOPIC_NAME, client=client)

        iterator = topic.list_subscriptions()
        subscriptions = list(iterator)
        next_page_token = iterator.next_page_token

        self.assertEqual(len(subscriptions), 0)
        self.assertIsNone(next_page_token)
        # Verify the mock.
        called_with = client._connection._called_with
        self.assertEqual(len(called_with), 3)
        self.assertEqual(called_with['method'], 'GET')
        path = '/%s/subscriptions' % (self.TOPIC_PATH,)
        self.assertEqual(called_with['path'], path)
        self.assertEqual(called_with['query_params'], {})

    def test_get_iam_policy_w_bound_client(self):
        from google.cloud.pubsub.iam import (
            PUBSUB_ADMIN_ROLE,
            PUBSUB_EDITOR_ROLE,
            PUBSUB_VIEWER_ROLE,
            PUBSUB_PUBLISHER_ROLE,
            PUBSUB_SUBSCRIBER_ROLE,
        )

        OWNER1 = 'user:phred@example.com'
        OWNER2 = 'group:cloud-logs@google.com'
        EDITOR1 = 'domain:google.com'
        EDITOR2 = 'user:phred@example.com'
        VIEWER1 = 'serviceAccount:1234-abcdef@service.example.com'
        VIEWER2 = 'user:phred@example.com'
        PUBLISHER = 'user:phred@example.com'
        SUBSCRIBER = 'serviceAccount:1234-abcdef@service.example.com'
        POLICY = {
            'etag': 'DEADBEEF',
            'version': 17,
            'bindings': [
                {'role': PUBSUB_ADMIN_ROLE, 'members': [OWNER1, OWNER2]},
                {'role': PUBSUB_EDITOR_ROLE, 'members': [EDITOR1, EDITOR2]},
                {'role': PUBSUB_VIEWER_ROLE, 'members': [VIEWER1, VIEWER2]},
                {'role': PUBSUB_PUBLISHER_ROLE, 'members': [PUBLISHER]},
                {'role': PUBSUB_SUBSCRIBER_ROLE, 'members': [SUBSCRIBER]},
            ],
        }

        client = _Client(project=self.PROJECT)
        api = client.iam_policy_api = _FauxIAMPolicy()
        api._get_iam_policy_response = POLICY
        topic = self._make_one(self.TOPIC_NAME, client=client)

        policy = topic.get_iam_policy()

        self.assertEqual(policy.etag, 'DEADBEEF')
        self.assertEqual(policy.version, 17)
        self.assertEqual(sorted(policy.owners), [OWNER2, OWNER1])
        self.assertEqual(sorted(policy.editors), [EDITOR1, EDITOR2])
        self.assertEqual(sorted(policy.viewers), [VIEWER1, VIEWER2])
        self.assertEqual(sorted(policy.publishers), [PUBLISHER])
        self.assertEqual(sorted(policy.subscribers), [SUBSCRIBER])
        self.assertEqual(api._got_iam_policy, self.TOPIC_PATH)

    def test_get_iam_policy_w_alternate_client(self):
        POLICY = {
            'etag': 'ACAB',
        }

        client1 = _Client(project=self.PROJECT)
        client2 = _Client(project=self.PROJECT)
        api = client2.iam_policy_api = _FauxIAMPolicy()
        api._get_iam_policy_response = POLICY
        topic = self._make_one(self.TOPIC_NAME, client=client1)

        policy = topic.get_iam_policy(client=client2)

        self.assertEqual(policy.etag, 'ACAB')
        self.assertIsNone(policy.version)
        self.assertEqual(sorted(policy.owners), [])
        self.assertEqual(sorted(policy.editors), [])
        self.assertEqual(sorted(policy.viewers), [])

        self.assertEqual(api._got_iam_policy, self.TOPIC_PATH)

    def test_set_iam_policy_w_bound_client(self):
        from google.cloud.pubsub.iam import Policy
        from google.cloud.pubsub.iam import (
            PUBSUB_ADMIN_ROLE,
            PUBSUB_EDITOR_ROLE,
            PUBSUB_VIEWER_ROLE,
            PUBSUB_PUBLISHER_ROLE,
            PUBSUB_SUBSCRIBER_ROLE,
        )

        OWNER1 = 'group:cloud-logs@google.com'
        OWNER2 = 'user:phred@example.com'
        EDITOR1 = 'domain:google.com'
        EDITOR2 = 'user:phred@example.com'
        VIEWER1 = 'serviceAccount:1234-abcdef@service.example.com'
        VIEWER2 = 'user:phred@example.com'
        PUBLISHER = 'user:phred@example.com'
        SUBSCRIBER = 'serviceAccount:1234-abcdef@service.example.com'
        POLICY = {
            'etag': 'DEADBEEF',
            'version': 17,
            'bindings': [
                {'role': PUBSUB_ADMIN_ROLE,
                 'members': [OWNER1, OWNER2]},
                {'role': PUBSUB_EDITOR_ROLE,
                 'members': [EDITOR1, EDITOR2]},
                {'role': PUBSUB_VIEWER_ROLE,
                 'members': [VIEWER1, VIEWER2]},
                {'role': PUBSUB_PUBLISHER_ROLE,
                 'members': [PUBLISHER]},
                {'role': PUBSUB_SUBSCRIBER_ROLE,
                 'members': [SUBSCRIBER]},
            ],
        }
        RESPONSE = POLICY.copy()
        RESPONSE['etag'] = 'ABACABAF'
        RESPONSE['version'] = 18

        client = _Client(project=self.PROJECT)
        api = client.iam_policy_api = _FauxIAMPolicy()
        api._set_iam_policy_response = RESPONSE
        topic = self._make_one(self.TOPIC_NAME, client=client)
        policy = Policy('DEADBEEF', 17)
        policy.owners.add(OWNER1)
        policy.owners.add(OWNER2)
        policy.editors.add(EDITOR1)
        policy.editors.add(EDITOR2)
        policy.viewers.add(VIEWER1)
        policy.viewers.add(VIEWER2)
        policy.publishers.add(PUBLISHER)
        policy.subscribers.add(SUBSCRIBER)

        new_policy = topic.set_iam_policy(policy)

        self.assertEqual(new_policy.etag, 'ABACABAF')
        self.assertEqual(new_policy.version, 18)
        self.assertEqual(sorted(new_policy.owners), [OWNER1, OWNER2])
        self.assertEqual(sorted(new_policy.editors), [EDITOR1, EDITOR2])
        self.assertEqual(sorted(new_policy.viewers), [VIEWER1, VIEWER2])
        self.assertEqual(sorted(new_policy.publishers), [PUBLISHER])
        self.assertEqual(sorted(new_policy.subscribers), [SUBSCRIBER])
        self.assertEqual(api._set_iam_policy, (self.TOPIC_PATH, POLICY))

    def test_set_iam_policy_w_alternate_client(self):
        from google.cloud.pubsub.iam import Policy

        RESPONSE = {'etag': 'ACAB'}

        client1 = _Client(project=self.PROJECT)
        client2 = _Client(project=self.PROJECT)
        api = client2.iam_policy_api = _FauxIAMPolicy()
        api._set_iam_policy_response = RESPONSE
        topic = self._make_one(self.TOPIC_NAME, client=client1)

        policy = Policy()
        new_policy = topic.set_iam_policy(policy, client=client2)

        self.assertEqual(new_policy.etag, 'ACAB')
        self.assertIsNone(new_policy.version)
        self.assertEqual(sorted(new_policy.owners), [])
        self.assertEqual(sorted(new_policy.editors), [])
        self.assertEqual(sorted(new_policy.viewers), [])

        self.assertEqual(api._set_iam_policy, (self.TOPIC_PATH, {}))

    def test_check_iam_permissions_w_bound_client(self):
        from google.cloud.pubsub.iam import OWNER_ROLE
        from google.cloud.pubsub.iam import EDITOR_ROLE
        from google.cloud.pubsub.iam import VIEWER_ROLE

        ROLES = [VIEWER_ROLE, EDITOR_ROLE, OWNER_ROLE]
        client = _Client(project=self.PROJECT)
        api = client.iam_policy_api = _FauxIAMPolicy()
        api._test_iam_permissions_response = ROLES[:-1]
        topic = self._make_one(self.TOPIC_NAME, client=client)

        allowed = topic.check_iam_permissions(ROLES)

        self.assertEqual(allowed, ROLES[:-1])
        self.assertEqual(api._tested_iam_permissions,
                         (self.TOPIC_PATH, ROLES))

    def test_check_iam_permissions_w_alternate_client(self):
        from google.cloud.pubsub.iam import OWNER_ROLE
        from google.cloud.pubsub.iam import EDITOR_ROLE
        from google.cloud.pubsub.iam import VIEWER_ROLE

        ROLES = [VIEWER_ROLE, EDITOR_ROLE, OWNER_ROLE]
        client1 = _Client(project=self.PROJECT)
        client2 = _Client(project=self.PROJECT)
        api = client2.iam_policy_api = _FauxIAMPolicy()
        api._test_iam_permissions_response = []
        topic = self._make_one(self.TOPIC_NAME, client=client1)

        allowed = topic.check_iam_permissions(ROLES, client=client2)

        self.assertEqual(len(allowed), 0)
        self.assertEqual(api._tested_iam_permissions,
                         (self.TOPIC_PATH, ROLES))


class TestBatch(unittest.TestCase):
    PROJECT = 'PROJECT'

    @staticmethod
    def _get_target_class():
        from google.cloud.pubsub.topic import Batch

        return Batch

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_ctor_defaults(self):
        topic = _Topic()
        client = _Client(project=self.PROJECT)
        batch = self._make_one(topic, client)
        self.assertIs(batch.topic, topic)
        self.assertIs(batch.client, client)
        self.assertEqual(len(batch.messages), 0)
        self.assertEqual(len(batch.message_ids), 0)

    def test___iter___empty(self):
        topic = _Topic()
        client = object()
        batch = self._make_one(topic, client)
        self.assertEqual(list(batch), [])

    def test___iter___non_empty(self):
        topic = _Topic()
        client = object()
        batch = self._make_one(topic, client)
        batch.message_ids[:] = ['ONE', 'TWO', 'THREE']
        self.assertEqual(list(batch), ['ONE', 'TWO', 'THREE'])

    def test_publish_bytes_wo_attrs(self):
        PAYLOAD = 'This is the message text'
        MESSAGE = {'data': PAYLOAD,
                   'attributes': {}}
        client = _Client(project=self.PROJECT)
        topic = _Topic()
        batch = self._make_one(topic, client=client)
        batch.publish(PAYLOAD)
        self.assertEqual(batch.messages, [MESSAGE])

    def test_publish_bytes_w_add_timestamp(self):
        PAYLOAD = 'This is the message text'
        MESSAGE = {'data': PAYLOAD,
                   'attributes': {'timestamp': 'TIMESTAMP'}}
        client = _Client(project=self.PROJECT)
        topic = _Topic(timestamp_messages=True)
        batch = self._make_one(topic, client=client)
        batch.publish(PAYLOAD)
        self.assertEqual(batch.messages, [MESSAGE])

    def test_commit_w_bound_client(self):
        PAYLOAD1 = 'This is the first message text'
        PAYLOAD2 = 'This is the second message text'
        MSGID1 = 'DEADBEEF'
        MSGID2 = 'BEADCAFE'
        MESSAGE1 = {'data': PAYLOAD1,
                    'attributes': {}}
        MESSAGE2 = {'data': PAYLOAD2,
                    'attributes': {'attr1': 'value1', 'attr2': 'value2'}}
        client = _Client(project='PROJECT')
        api = client.publisher_api = _FauxPublisherAPI()
        api._topic_publish_response = [MSGID1, MSGID2]
        topic = _Topic()
        batch = self._make_one(topic, client=client)

        batch.publish(PAYLOAD1)
        batch.publish(PAYLOAD2, attr1='value1', attr2='value2')
        batch.commit()

        self.assertEqual(list(batch), [MSGID1, MSGID2])
        self.assertEqual(list(batch.messages), [])
        self.assertEqual(api._topic_published,
                         (topic.full_name, [MESSAGE1, MESSAGE2]))

    def test_commit_w_alternate_client(self):
        PAYLOAD1 = 'This is the first message text'
        PAYLOAD2 = 'This is the second message text'
        MSGID1 = 'DEADBEEF'
        MSGID2 = 'BEADCAFE'
        MESSAGE1 = {'data': PAYLOAD1, 'attributes': {}}
        MESSAGE2 = {'data': PAYLOAD2,
                    'attributes': {'attr1': 'value1', 'attr2': 'value2'}}
        client1 = _Client(project='PROJECT')
        client2 = _Client(project='PROJECT')
        api = client2.publisher_api = _FauxPublisherAPI()
        api._topic_publish_response = [MSGID1, MSGID2]
        topic = _Topic()
        batch = self._make_one(topic, client=client1)

        batch.publish(PAYLOAD1)
        batch.publish(PAYLOAD2, attr1='value1', attr2='value2')
        batch.commit(client=client2)

        self.assertEqual(list(batch), [MSGID1, MSGID2])
        self.assertEqual(list(batch.messages), [])
        self.assertEqual(api._topic_published,
                         (topic.full_name, [MESSAGE1, MESSAGE2]))

    def test_context_mgr_success(self):
        PAYLOAD1 = 'This is the first message text'
        PAYLOAD2 = 'This is the second message text'
        MSGID1 = 'DEADBEEF'
        MSGID2 = 'BEADCAFE'
        MESSAGE1 = {'data': PAYLOAD1, 'attributes': {}}
        MESSAGE2 = {'data': PAYLOAD2,
                    'attributes': {'attr1': 'value1', 'attr2': 'value2'}}
        client = _Client(project='PROJECT')
        api = client.publisher_api = _FauxPublisherAPI()
        api._topic_publish_response = [MSGID1, MSGID2]
        topic = _Topic()
        batch = self._make_one(topic, client=client)

        with batch as other:
            batch.publish(PAYLOAD1)
            batch.publish(PAYLOAD2, attr1='value1', attr2='value2')

        self.assertIs(other, batch)
        self.assertEqual(list(batch), [MSGID1, MSGID2])
        self.assertEqual(list(batch.messages), [])
        self.assertEqual(api._topic_published,
                         (topic.full_name, [MESSAGE1, MESSAGE2]))

    def test_context_mgr_failure(self):
        PAYLOAD1 = 'This is the first message text'
        PAYLOAD2 = 'This is the second message text'
        MESSAGE1 = {'data': PAYLOAD1, 'attributes': {}}
        MESSAGE2 = {'data': PAYLOAD2,
                    'attributes': {'attr1': 'value1', 'attr2': 'value2'}}
        client = _Client(project='PROJECT')
        api = client.publisher_api = _FauxPublisherAPI()
        topic = _Topic()
        batch = self._make_one(topic, client=client)

        try:
            with batch as other:
                batch.publish(PAYLOAD1)
                batch.publish(PAYLOAD2, attr1='value1', attr2='value2')
                raise _Bugout()
        except _Bugout:
            pass

        self.assertIs(other, batch)
        self.assertEqual(list(batch), [])
        self.assertEqual(list(batch.messages), [MESSAGE1, MESSAGE2])
        self.assertEqual(getattr(api, '_topic_published', self), self)

    def test_message_count_autocommit(self):
        """Establish that if the batch is assigned to take a maximum
        number of messages, that it commits when it reaches that maximum.
        """
        client = _Client(project='PROJECT')
        topic = _Topic(name='TOPIC')

        # Track commits, but do not perform them.
        Batch = self._get_target_class()
        with mock.patch.object(Batch, 'commit') as commit:
            with self._make_one(topic, client=client, max_messages=5) as batch:
                self.assertIsInstance(batch, Batch)

                # Publish four messages and establish that the batch does
                # not commit.
                for i in range(0, 4):
                    batch.publish({
                        'attributes': {},
                        'data': 'Batch message %d.' % (i,),
                    })
                    commit.assert_not_called()

                # Publish a fifth message and observe the commit.
                batch.publish({
                    'attributes': {},
                    'data': 'The final call to trigger a commit!',
                })
                commit.assert_called_once_with()

            # There should be a second commit after the context manager
            # exits.
            self.assertEqual(commit.call_count, 2)

    @mock.patch('time.time')
    def test_message_time_autocommit(self, mock_time):
        """Establish that if the batch is sufficiently old, that it commits
        the next time it receives a publish.
        """
        client = _Client(project='PROJECT')
        topic = _Topic(name='TOPIC')

        # Track commits, but do not perform them.
        Batch = self._get_target_class()
        with mock.patch.object(Batch, 'commit') as commit:
            mock_time.return_value = 0.0
            with self._make_one(topic, client=client, max_interval=5) as batch:
                self.assertIsInstance(batch, Batch)

                # Publish some messages and establish that the batch does
                # not commit.
                for i in range(0, 10):
                    batch.publish({
                        'attributes': {},
                        'data': 'Batch message %d.' % (i,),
                    })
                    commit.assert_not_called()

                # Move time ahead so that this batch is too old.
                mock_time.return_value = 10.0

                # Publish another message and observe the commit.
                batch.publish({
                    'attributes': {},
                    'data': 'The final call to trigger a commit!',
                })
                commit.assert_called_once_with()

            # There should be a second commit after the context manager
            # exits.
            self.assertEqual(commit.call_count, 2)


class _FauxPublisherAPI(object):
    _api_called = 0

    def topic_create(self, topic_path):
        self._topic_created = topic_path
        return self._topic_create_response

    def topic_get(self, topic_path):
        from google.cloud.exceptions import NotFound

        self._topic_got = topic_path
        try:
            return self._topic_get_response
        except AttributeError:
            raise NotFound(topic_path)

    def topic_delete(self, topic_path):
        self._topic_deleted = topic_path
        return self._topic_delete_response

    def topic_publish(self, topic_path, messages):
        self._topic_published = topic_path, messages
        self._api_called += 1
        return self._topic_publish_response


class _FauxIAMPolicy(object):

    def get_iam_policy(self, target_path):
        self._got_iam_policy = target_path
        return self._get_iam_policy_response

    def set_iam_policy(self, target_path, policy):
        self._set_iam_policy = target_path, policy
        return self._set_iam_policy_response

    def test_iam_permissions(self, target_path, permissions):
        self._tested_iam_permissions = target_path, permissions
        return self._test_iam_permissions_response


class _Topic(object):

    def __init__(self, name="NAME", project="PROJECT",
                 timestamp_messages=False):
        self.full_name = 'projects/%s/topics/%s' % (project, name)
        self.path = '/%s' % (self.full_name,)
        self.timestamp_messages = timestamp_messages

    def _timestamp_message(self, attrs):
        if self.timestamp_messages:
            attrs['timestamp'] = 'TIMESTAMP'


class _Client(object):

    connection = None

    def __init__(self, project):
        self.project = project


class _Bugout(Exception):
    pass


class _Connection(object):

    _called_with = None

    def __init__(self, *responses):
        self._responses = responses

    def api_request(self, **kw):
        self._called_with = kw
        response, self._responses = self._responses[0], self._responses[1:]
        return response
