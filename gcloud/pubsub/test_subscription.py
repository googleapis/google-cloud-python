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
    PROJECT = 'PROJECT'
    TOPIC_NAME = 'topic_name'
    TOPIC_PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
    SUB_NAME = 'sub_name'
    SUB_PATH = 'projects/%s/subscriptions/%s' % (PROJECT, SUB_NAME)
    DEADLINE = 42
    ENDPOINT = 'https://api.example.com/push'

    def _getTargetClass(self):
        from gcloud.pubsub.subscription import Subscription
        return Subscription

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_defaults(self):
        client = _Client(project=self.PROJECT)
        topic = _Topic(self.TOPIC_NAME, client=client)
        subscription = self._makeOne(self.SUB_NAME, topic)
        self.assertEqual(subscription.name, self.SUB_NAME)
        self.assertTrue(subscription.topic is topic)
        self.assertEqual(subscription.ack_deadline, None)
        self.assertEqual(subscription.push_endpoint, None)

    def test_ctor_explicit(self):
        client = _Client(project=self.PROJECT)
        topic = _Topic(self.TOPIC_NAME, client=client)
        subscription = self._makeOne(self.SUB_NAME, topic,
                                     self.DEADLINE, self.ENDPOINT)
        self.assertEqual(subscription.name, self.SUB_NAME)
        self.assertTrue(subscription.topic is topic)
        self.assertEqual(subscription.ack_deadline, self.DEADLINE)
        self.assertEqual(subscription.push_endpoint, self.ENDPOINT)

    def test_ctor_w_client_wo_topic(self):
        client = _Client(project=self.PROJECT)
        subscription = self._makeOne(self.SUB_NAME, client=client)
        self.assertEqual(subscription.name, self.SUB_NAME)
        self.assertTrue(subscription.topic is None)

    def test_ctor_w_both_topic_and_client(self):
        client1 = _Client(project=self.PROJECT)
        client2 = _Client(project=self.PROJECT)
        topic = _Topic(self.TOPIC_NAME, client=client1)
        with self.assertRaises(TypeError):
            self._makeOne(self.SUB_NAME, topic, client=client2)

    def test_ctor_w_neither_topic_nor_client(self):
        with self.assertRaises(TypeError):
            self._makeOne(self.SUB_NAME)

    def test_from_api_repr_no_topics(self):
        from gcloud.pubsub.topic import Topic
        resource = {'topic': self.TOPIC_PATH,
                    'name': self.SUB_PATH,
                    'ackDeadlineSeconds': self.DEADLINE,
                    'pushConfig': {'pushEndpoint': self.ENDPOINT}}
        klass = self._getTargetClass()
        client = _Client(project=self.PROJECT)
        subscription = klass.from_api_repr(resource, client)
        self.assertEqual(subscription.name, self.SUB_NAME)
        topic = subscription.topic
        self.assertIsInstance(topic, Topic)
        self.assertEqual(topic.name, self.TOPIC_NAME)
        self.assertEqual(topic.project, self.PROJECT)
        self.assertEqual(subscription.ack_deadline, self.DEADLINE)
        self.assertEqual(subscription.push_endpoint, self.ENDPOINT)

    def test_from_api_repr_w_deleted_topic(self):
        klass = self._getTargetClass()
        resource = {'topic': klass._DELETED_TOPIC_PATH,
                    'name': self.SUB_PATH,
                    'ackDeadlineSeconds': self.DEADLINE,
                    'pushConfig': {'pushEndpoint': self.ENDPOINT}}
        klass = self._getTargetClass()
        client = _Client(project=self.PROJECT)
        subscription = klass.from_api_repr(resource, client)
        self.assertEqual(subscription.name, self.SUB_NAME)
        self.assertTrue(subscription.topic is None)
        self.assertEqual(subscription.ack_deadline, self.DEADLINE)
        self.assertEqual(subscription.push_endpoint, self.ENDPOINT)

    def test_from_api_repr_w_topics_no_topic_match(self):
        from gcloud.pubsub.topic import Topic
        resource = {'topic': self.TOPIC_PATH,
                    'name': self.SUB_PATH,
                    'ackDeadlineSeconds': self.DEADLINE,
                    'pushConfig': {'pushEndpoint': self.ENDPOINT}}
        topics = {}
        klass = self._getTargetClass()
        client = _Client(project=self.PROJECT)
        subscription = klass.from_api_repr(resource, client, topics=topics)
        self.assertEqual(subscription.name, self.SUB_NAME)
        topic = subscription.topic
        self.assertIsInstance(topic, Topic)
        self.assertTrue(topic is topics[self.TOPIC_PATH])
        self.assertEqual(topic.name, self.TOPIC_NAME)
        self.assertEqual(topic.project, self.PROJECT)
        self.assertEqual(subscription.ack_deadline, self.DEADLINE)
        self.assertEqual(subscription.push_endpoint, self.ENDPOINT)

    def test_from_api_repr_w_topics_w_topic_match(self):
        resource = {'topic': self.TOPIC_PATH,
                    'name': self.SUB_PATH,
                    'ackDeadlineSeconds': self.DEADLINE,
                    'pushConfig': {'pushEndpoint': self.ENDPOINT}}
        client = _Client(project=self.PROJECT)
        topic = _Topic(self.TOPIC_NAME, client=client)
        topics = {self.TOPIC_PATH: topic}
        klass = self._getTargetClass()
        subscription = klass.from_api_repr(resource, client, topics=topics)
        self.assertEqual(subscription.name, self.SUB_NAME)
        self.assertTrue(subscription.topic is topic)
        self.assertEqual(subscription.ack_deadline, self.DEADLINE)
        self.assertEqual(subscription.push_endpoint, self.ENDPOINT)

    def test_full_name_and_path(self):
        PROJECT = 'PROJECT'
        SUB_FULL = 'projects/%s/subscriptions/%s' % (PROJECT, self.SUB_NAME)
        SUB_PATH = '/%s' % (SUB_FULL,)
        TOPIC_NAME = 'topic_name'
        CLIENT = _Client(project=PROJECT)
        topic = _Topic(TOPIC_NAME, client=CLIENT)
        subscription = self._makeOne(self.SUB_NAME, topic)
        self.assertEqual(subscription.full_name, SUB_FULL)
        self.assertEqual(subscription.path, SUB_PATH)

    def test_autoack_defaults(self):
        from gcloud.pubsub.subscription import AutoAck
        client = _Client(project=self.PROJECT)
        topic = _Topic(self.TOPIC_NAME, client=client)
        subscription = self._makeOne(self.SUB_NAME, topic)
        auto_ack = subscription.auto_ack()
        self.assertTrue(isinstance(auto_ack, AutoAck))
        self.assertTrue(auto_ack._subscription is subscription)
        self.assertEqual(auto_ack._return_immediately, False)
        self.assertEqual(auto_ack._max_messages, 1)
        self.assertTrue(auto_ack._client is None)

    def test_autoack_explicit(self):
        from gcloud.pubsub.subscription import AutoAck
        client1 = _Client(project=self.PROJECT)
        client2 = _Client(project=self.PROJECT)
        topic = _Topic(self.TOPIC_NAME, client=client1)
        subscription = self._makeOne(self.SUB_NAME, topic)
        auto_ack = subscription.auto_ack(True, 10, client2)
        self.assertTrue(isinstance(auto_ack, AutoAck))
        self.assertTrue(auto_ack._subscription is subscription)
        self.assertEqual(auto_ack._return_immediately, True)
        self.assertEqual(auto_ack._max_messages, 10)
        self.assertTrue(auto_ack._client is client2)

    def test_create_pull_wo_ack_deadline_w_bound_client(self):
        RESPONSE = {
            'topic': self.TOPIC_PATH,
            'name': self.SUB_PATH,
        }
        client = _Client(project=self.PROJECT)
        api = client.subscriber_api = _FauxSubscribererAPI()
        api._subscription_create_response = RESPONSE
        topic = _Topic(self.TOPIC_NAME, client=client)
        subscription = self._makeOne(self.SUB_NAME, topic)

        subscription.create()

        self.assertEqual(api._subscription_created,
                         (self.SUB_PATH, self.TOPIC_PATH, None, None))

    def test_create_push_w_ack_deadline_w_alternate_client(self):
        RESPONSE = {
            'topic': self.TOPIC_PATH,
            'name': self.SUB_PATH,
            'ackDeadlineSeconds': self.DEADLINE,
            'pushConfig': {'pushEndpoint': self.ENDPOINT}
        }
        client1 = _Client(project=self.PROJECT)
        client2 = _Client(project=self.PROJECT)
        api = client2.subscriber_api = _FauxSubscribererAPI()
        api._subscription_create_response = RESPONSE
        topic = _Topic(self.TOPIC_NAME, client=client1)
        subscription = self._makeOne(self.SUB_NAME, topic,
                                     self.DEADLINE, self.ENDPOINT)

        subscription.create(client=client2)

        self.assertEqual(
            api._subscription_created,
            (self.SUB_PATH, self.TOPIC_PATH, self.DEADLINE, self.ENDPOINT))

    def test_exists_miss_w_bound_client(self):
        client = _Client(project=self.PROJECT)
        api = client.subscriber_api = _FauxSubscribererAPI()
        topic = _Topic(self.TOPIC_NAME, client=client)
        subscription = self._makeOne(self.SUB_NAME, topic)

        self.assertFalse(subscription.exists())

        self.assertEqual(api._subscription_got, self.SUB_PATH)

    def test_exists_hit_w_alternate_client(self):
        RESPONSE = {'name': self.SUB_PATH, 'topic': self.TOPIC_PATH}
        client1 = _Client(project=self.PROJECT)
        client2 = _Client(project=self.PROJECT)
        api = client2.subscriber_api = _FauxSubscribererAPI()
        api._subscription_get_response = RESPONSE
        topic = _Topic(self.TOPIC_NAME, client=client1)
        subscription = self._makeOne(self.SUB_NAME, topic)

        self.assertTrue(subscription.exists(client=client2))

        self.assertEqual(api._subscription_got, self.SUB_PATH)

    def test_reload_w_bound_client(self):
        RESPONSE = {
            'name': self.SUB_PATH,
            'topic': self.TOPIC_PATH,
            'ackDeadlineSeconds': self.DEADLINE,
            'pushConfig': {'pushEndpoint': self.ENDPOINT},
        }
        client = _Client(project=self.PROJECT)
        api = client.subscriber_api = _FauxSubscribererAPI()
        api._subscription_get_response = RESPONSE
        topic = _Topic(self.TOPIC_NAME, client=client)
        subscription = self._makeOne(self.SUB_NAME, topic)

        subscription.reload()

        self.assertEqual(subscription.ack_deadline, self.DEADLINE)
        self.assertEqual(subscription.push_endpoint, self.ENDPOINT)
        self.assertEqual(api._subscription_got, self.SUB_PATH)

    def test_reload_w_alternate_client(self):
        RESPONSE = {
            'name': self.SUB_PATH,
            'topic': self.TOPIC_PATH,
        }
        client1 = _Client(project=self.PROJECT)
        client2 = _Client(project=self.PROJECT)
        api = client2.subscriber_api = _FauxSubscribererAPI()
        api._subscription_get_response = RESPONSE
        topic = _Topic(self.TOPIC_NAME, client=client1)
        subscription = self._makeOne(self.SUB_NAME, topic,
                                     self.DEADLINE, self.ENDPOINT)

        subscription.reload(client=client2)

        self.assertEqual(subscription.ack_deadline, None)
        self.assertEqual(subscription.push_endpoint, None)
        self.assertEqual(api._subscription_got, self.SUB_PATH)

    def test_delete_w_bound_client(self):
        RESPONSE = {}
        client = _Client(project=self.PROJECT)
        api = client.subscriber_api = _FauxSubscribererAPI()
        api._subscription_delete_response = RESPONSE
        topic = _Topic(self.TOPIC_NAME, client=client)
        subscription = self._makeOne(self.SUB_NAME, topic)

        subscription.delete()

        self.assertEqual(api._subscription_deleted, self.SUB_PATH)

    def test_delete_w_alternate_client(self):
        RESPONSE = {}
        client1 = _Client(project=self.PROJECT)
        client2 = _Client(project=self.PROJECT)
        api = client2.subscriber_api = _FauxSubscribererAPI()
        api._subscription_delete_response = RESPONSE
        topic = _Topic(self.TOPIC_NAME, client=client1)
        subscription = self._makeOne(self.SUB_NAME, topic,
                                     self.DEADLINE, self.ENDPOINT)

        subscription.delete(client=client2)

        self.assertEqual(api._subscription_deleted, self.SUB_PATH)

    def test_modify_push_config_w_endpoint_w_bound_client(self):
        client = _Client(project=self.PROJECT)
        api = client.subscriber_api = _FauxSubscribererAPI()
        api._subscription_modify_push_config_response = {}
        topic = _Topic(self.TOPIC_NAME, client=client)
        subscription = self._makeOne(self.SUB_NAME, topic)

        subscription.modify_push_configuration(push_endpoint=self.ENDPOINT)

        self.assertEqual(subscription.push_endpoint, self.ENDPOINT)
        self.assertEqual(api._subscription_modified_push_config,
                         (self.SUB_PATH, self.ENDPOINT))

    def test_modify_push_config_wo_endpoint_w_alternate_client(self):
        client1 = _Client(project=self.PROJECT)
        client2 = _Client(project=self.PROJECT)
        api = client2.subscriber_api = _FauxSubscribererAPI()
        api._subscription_modify_push_config_response = {}
        topic = _Topic(self.TOPIC_NAME, client=client1)
        subscription = self._makeOne(self.SUB_NAME, topic,
                                     push_endpoint=self.ENDPOINT)

        subscription.modify_push_configuration(push_endpoint=None,
                                               client=client2)

        self.assertEqual(subscription.push_endpoint, None)
        self.assertEqual(api._subscription_modified_push_config,
                         (self.SUB_PATH, None))

    def test_pull_wo_return_immediately_max_messages_w_bound_client(self):
        import base64
        from gcloud.pubsub.message import Message
        ACK_ID = 'DEADBEEF'
        MSG_ID = 'BEADCAFE'
        PAYLOAD = b'This is the message text'
        B64 = base64.b64encode(PAYLOAD)
        MESSAGE = {'messageId': MSG_ID, 'data': B64}
        REC_MESSAGE = {'ackId': ACK_ID, 'message': MESSAGE}
        client = _Client(project=self.PROJECT)
        api = client.subscriber_api = _FauxSubscribererAPI()
        api._subscription_pull_response = [REC_MESSAGE]
        topic = _Topic(self.TOPIC_NAME, client=client)
        subscription = self._makeOne(self.SUB_NAME, topic)

        pulled = subscription.pull()

        self.assertEqual(len(pulled), 1)
        ack_id, message = pulled[0]
        self.assertEqual(ack_id, ACK_ID)
        self.assertIsInstance(message, Message)
        self.assertEqual(message.data, PAYLOAD)
        self.assertEqual(message.message_id, MSG_ID)
        self.assertEqual(message.attributes, {})
        self.assertEqual(api._subscription_pulled,
                         (self.SUB_PATH, False, 1))

    def test_pull_w_return_immediately_w_max_messages_w_alt_client(self):
        import base64
        from gcloud.pubsub.message import Message
        ACK_ID = 'DEADBEEF'
        MSG_ID = 'BEADCAFE'
        PAYLOAD = b'This is the message text'
        B64 = base64.b64encode(PAYLOAD)
        MESSAGE = {'messageId': MSG_ID, 'data': B64, 'attributes': {'a': 'b'}}
        REC_MESSAGE = {'ackId': ACK_ID, 'message': MESSAGE}
        client1 = _Client(project=self.PROJECT)
        client2 = _Client(project=self.PROJECT)
        api = client2.subscriber_api = _FauxSubscribererAPI()
        api._subscription_pull_response = [REC_MESSAGE]
        topic = _Topic(self.TOPIC_NAME, client=client1)
        subscription = self._makeOne(self.SUB_NAME, topic)

        pulled = subscription.pull(return_immediately=True, max_messages=3,
                                   client=client2)

        self.assertEqual(len(pulled), 1)
        ack_id, message = pulled[0]
        self.assertEqual(ack_id, ACK_ID)
        self.assertIsInstance(message, Message)
        self.assertEqual(message.data, PAYLOAD)
        self.assertEqual(message.message_id, MSG_ID)
        self.assertEqual(message.attributes, {'a': 'b'})
        self.assertEqual(api._subscription_pulled,
                         (self.SUB_PATH, True, 3))

    def test_pull_wo_receivedMessages(self):
        client = _Client(project=self.PROJECT)
        api = client.subscriber_api = _FauxSubscribererAPI()
        api._subscription_pull_response = {}
        topic = _Topic(self.TOPIC_NAME, client=client)
        subscription = self._makeOne(self.SUB_NAME, topic)

        pulled = subscription.pull(return_immediately=False)

        self.assertEqual(len(pulled), 0)
        self.assertEqual(api._subscription_pulled,
                         (self.SUB_PATH, False, 1))

    def test_acknowledge_w_bound_client(self):
        ACK_ID1 = 'DEADBEEF'
        ACK_ID2 = 'BEADCAFE'
        client = _Client(project=self.PROJECT)
        api = client.subscriber_api = _FauxSubscribererAPI()
        api._subscription_acknowlege_response = {}
        topic = _Topic(self.TOPIC_NAME, client=client)
        subscription = self._makeOne(self.SUB_NAME, topic)

        subscription.acknowledge([ACK_ID1, ACK_ID2])

        self.assertEqual(api._subscription_acked,
                         (self.SUB_PATH, [ACK_ID1, ACK_ID2]))

    def test_acknowledge_w_alternate_client(self):
        ACK_ID1 = 'DEADBEEF'
        ACK_ID2 = 'BEADCAFE'
        client1 = _Client(project=self.PROJECT)
        client2 = _Client(project=self.PROJECT)
        api = client2.subscriber_api = _FauxSubscribererAPI()
        api._subscription_acknowlege_response = {}
        topic = _Topic(self.TOPIC_NAME, client=client1)
        subscription = self._makeOne(self.SUB_NAME, topic)

        subscription.acknowledge([ACK_ID1, ACK_ID2], client=client2)

        self.assertEqual(api._subscription_acked,
                         (self.SUB_PATH, [ACK_ID1, ACK_ID2]))

    def test_modify_ack_deadline_w_bound_client(self):
        ACK_ID1 = 'DEADBEEF'
        ACK_ID2 = 'BEADCAFE'
        client = _Client(project=self.PROJECT)
        api = client.subscriber_api = _FauxSubscribererAPI()
        api._subscription_modify_ack_deadline_response = {}
        topic = _Topic(self.TOPIC_NAME, client=client)
        subscription = self._makeOne(self.SUB_NAME, topic)

        subscription.modify_ack_deadline([ACK_ID1, ACK_ID2], self.DEADLINE)

        self.assertEqual(api._subscription_modified_ack_deadline,
                         (self.SUB_PATH, [ACK_ID1, ACK_ID2], self.DEADLINE))

    def test_modify_ack_deadline_w_alternate_client(self):
        ACK_ID1 = 'DEADBEEF'
        ACK_ID2 = 'BEADCAFE'
        client1 = _Client(project=self.PROJECT)
        client2 = _Client(project=self.PROJECT)
        api = client2.subscriber_api = _FauxSubscribererAPI()
        api._subscription_modify_ack_deadline_response = {}
        topic = _Topic(self.TOPIC_NAME, client=client1)
        subscription = self._makeOne(self.SUB_NAME, topic)

        subscription.modify_ack_deadline(
            [ACK_ID1, ACK_ID2], self.DEADLINE, client=client2)

        self.assertEqual(api._subscription_modified_ack_deadline,
                         (self.SUB_PATH, [ACK_ID1, ACK_ID2], self.DEADLINE))

    def test_get_iam_policy_w_bound_client(self):
        from gcloud.pubsub.iam import (
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
        topic = _Topic(self.TOPIC_NAME, client=client)
        subscription = self._makeOne(self.SUB_NAME, topic)

        policy = subscription.get_iam_policy()

        self.assertEqual(policy.etag, 'DEADBEEF')
        self.assertEqual(policy.version, 17)
        self.assertEqual(sorted(policy.owners), [OWNER2, OWNER1])
        self.assertEqual(sorted(policy.editors), [EDITOR1, EDITOR2])
        self.assertEqual(sorted(policy.viewers), [VIEWER1, VIEWER2])
        self.assertEqual(sorted(policy.publishers), [PUBLISHER])
        self.assertEqual(sorted(policy.subscribers), [SUBSCRIBER])
        self.assertEqual(api._got_iam_policy, self.SUB_PATH)

    def test_get_iam_policy_w_alternate_client(self):
        POLICY = {
            'etag': 'ACAB',
        }
        client1 = _Client(project=self.PROJECT)
        client2 = _Client(project=self.PROJECT)
        api = client2.iam_policy_api = _FauxIAMPolicy()
        api._get_iam_policy_response = POLICY
        topic = _Topic(self.TOPIC_NAME, client=client1)
        subscription = self._makeOne(self.SUB_NAME, topic)

        policy = subscription.get_iam_policy(client=client2)

        self.assertEqual(policy.etag, 'ACAB')
        self.assertEqual(policy.version, None)
        self.assertEqual(sorted(policy.owners), [])
        self.assertEqual(sorted(policy.editors), [])
        self.assertEqual(sorted(policy.viewers), [])

        self.assertEqual(api._got_iam_policy, self.SUB_PATH)

    def test_set_iam_policy_w_bound_client(self):
        from gcloud.pubsub.iam import Policy
        from gcloud.pubsub.iam import (
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
                {'role': PUBSUB_ADMIN_ROLE, 'members': [OWNER1, OWNER2]},
                {'role': PUBSUB_EDITOR_ROLE, 'members': [EDITOR1, EDITOR2]},
                {'role': PUBSUB_VIEWER_ROLE, 'members': [VIEWER1, VIEWER2]},
                {'role': PUBSUB_PUBLISHER_ROLE, 'members': [PUBLISHER]},
                {'role': PUBSUB_SUBSCRIBER_ROLE, 'members': [SUBSCRIBER]},
            ],
        }
        RESPONSE = POLICY.copy()
        RESPONSE['etag'] = 'ABACABAF'
        RESPONSE['version'] = 18
        client = _Client(project=self.PROJECT)
        api = client.iam_policy_api = _FauxIAMPolicy()
        api._set_iam_policy_response = RESPONSE
        topic = _Topic(self.TOPIC_NAME, client=client)
        subscription = self._makeOne(self.SUB_NAME, topic)
        policy = Policy('DEADBEEF', 17)
        policy.owners.add(OWNER1)
        policy.owners.add(OWNER2)
        policy.editors.add(EDITOR1)
        policy.editors.add(EDITOR2)
        policy.viewers.add(VIEWER1)
        policy.viewers.add(VIEWER2)
        policy.publishers.add(PUBLISHER)
        policy.subscribers.add(SUBSCRIBER)

        new_policy = subscription.set_iam_policy(policy)

        self.assertEqual(new_policy.etag, 'ABACABAF')
        self.assertEqual(new_policy.version, 18)
        self.assertEqual(sorted(new_policy.owners), [OWNER1, OWNER2])
        self.assertEqual(sorted(new_policy.editors), [EDITOR1, EDITOR2])
        self.assertEqual(sorted(new_policy.viewers), [VIEWER1, VIEWER2])
        self.assertEqual(sorted(new_policy.publishers), [PUBLISHER])
        self.assertEqual(sorted(new_policy.subscribers), [SUBSCRIBER])
        self.assertEqual(api._set_iam_policy, (self.SUB_PATH, POLICY))

    def test_set_iam_policy_w_alternate_client(self):
        from gcloud.pubsub.iam import Policy
        RESPONSE = {'etag': 'ACAB'}
        client1 = _Client(project=self.PROJECT)
        client2 = _Client(project=self.PROJECT)
        api = client2.iam_policy_api = _FauxIAMPolicy()
        api._set_iam_policy_response = RESPONSE
        topic = _Topic(self.TOPIC_NAME, client=client1)
        subscription = self._makeOne(self.SUB_NAME, topic)

        policy = Policy()
        new_policy = subscription.set_iam_policy(policy, client=client2)

        self.assertEqual(new_policy.etag, 'ACAB')
        self.assertEqual(new_policy.version, None)
        self.assertEqual(sorted(new_policy.owners), [])
        self.assertEqual(sorted(new_policy.editors), [])
        self.assertEqual(sorted(new_policy.viewers), [])
        self.assertEqual(api._set_iam_policy, (self.SUB_PATH, {}))

    def test_check_iam_permissions_w_bound_client(self):
        from gcloud.pubsub.iam import OWNER_ROLE, EDITOR_ROLE, VIEWER_ROLE
        ROLES = [VIEWER_ROLE, EDITOR_ROLE, OWNER_ROLE]
        client = _Client(project=self.PROJECT)
        api = client.iam_policy_api = _FauxIAMPolicy()
        api._test_iam_permissions_response = ROLES[:-1]
        topic = _Topic(self.TOPIC_NAME, client=client)
        subscription = self._makeOne(self.SUB_NAME, topic)

        allowed = subscription.check_iam_permissions(ROLES)

        self.assertEqual(allowed, ROLES[:-1])
        self.assertEqual(api._tested_iam_permissions,
                         (self.SUB_PATH, ROLES))

    def test_check_iam_permissions_w_alternate_client(self):
        from gcloud.pubsub.iam import OWNER_ROLE, EDITOR_ROLE, VIEWER_ROLE
        ROLES = [VIEWER_ROLE, EDITOR_ROLE, OWNER_ROLE]
        client1 = _Client(project=self.PROJECT)
        client2 = _Client(project=self.PROJECT)
        api = client2.iam_policy_api = _FauxIAMPolicy()
        api._test_iam_permissions_response = []
        topic = _Topic(self.TOPIC_NAME, client=client1)
        subscription = self._makeOne(self.SUB_NAME, topic)

        allowed = subscription.check_iam_permissions(ROLES, client=client2)

        self.assertEqual(len(allowed), 0)
        self.assertEqual(api._tested_iam_permissions,
                         (self.SUB_PATH, ROLES))


class _FauxSubscribererAPI(object):

    def subscription_create(self, subscription_path, topic_path,
                            ack_deadline=None, push_endpoint=None):
        self._subscription_created = (
            subscription_path, topic_path, ack_deadline, push_endpoint)
        return self._subscription_create_response

    def subscription_get(self, subscription_path):
        from gcloud.exceptions import NotFound
        self._subscription_got = subscription_path
        try:
            return self._subscription_get_response
        except AttributeError:
            raise NotFound(subscription_path)

    def subscription_delete(self, subscription_path):
        self._subscription_deleted = subscription_path
        return self._subscription_delete_response

    def subscription_modify_push_config(
            self, subscription_path, push_endpoint):
        self._subscription_modified_push_config = (
            subscription_path, push_endpoint)
        return self._subscription_modify_push_config_response

    def subscription_pull(self, subscription_path, return_immediately,
                          max_messages):
        self._subscription_pulled = (
            subscription_path, return_immediately, max_messages)
        return self._subscription_pull_response

    def subscription_acknowledge(self, subscription_path, ack_ids):
        self._subscription_acked = (subscription_path, ack_ids)
        return self._subscription_acknowlege_response

    def subscription_modify_ack_deadline(self, subscription_path, ack_ids,
                                         ack_deadline):
        self._subscription_modified_ack_deadline = (
            subscription_path, ack_ids, ack_deadline)
        return self._subscription_modify_ack_deadline_response


class TestAutoAck(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.pubsub.subscription import AutoAck
        return AutoAck

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_defaults(self):
        subscription = _FauxSubscription(())
        auto_ack = self._makeOne(subscription)
        self.assertEqual(auto_ack._return_immediately, False)
        self.assertEqual(auto_ack._max_messages, 1)
        self.assertTrue(auto_ack._client is None)

    def test_ctor_explicit(self):
        CLIENT = object()
        subscription = _FauxSubscription(())
        auto_ack = self._makeOne(
            subscription, return_immediately=True, max_messages=10,
            client=CLIENT)
        self.assertTrue(auto_ack._subscription is subscription)
        self.assertEqual(auto_ack._return_immediately, True)
        self.assertEqual(auto_ack._max_messages, 10)
        self.assertTrue(auto_ack._client is CLIENT)

    def test___enter___w_defaults(self):
        subscription = _FauxSubscription(())
        auto_ack = self._makeOne(subscription)

        with auto_ack as returned:
            pass

        self.assertTrue(returned is auto_ack)
        self.assertEqual(subscription._return_immediately, False)
        self.assertEqual(subscription._max_messages, 1)
        self.assertTrue(subscription._client is None)

    def test___enter___w_explicit(self):
        CLIENT = object()
        subscription = _FauxSubscription(())
        auto_ack = self._makeOne(
            subscription, return_immediately=True, max_messages=10,
            client=CLIENT)

        with auto_ack as returned:
            pass

        self.assertTrue(returned is auto_ack)
        self.assertEqual(subscription._return_immediately, True)
        self.assertEqual(subscription._max_messages, 10)
        self.assertTrue(subscription._client is CLIENT)

    def test___exit___(self):
        CLIENT = object()
        ACK_ID1, MESSAGE1 = 'ACK_ID1', _FallibleMessage()
        ACK_ID2, MESSAGE2 = 'ACK_ID2', _FallibleMessage()
        ACK_ID3, MESSAGE3 = 'ACK_ID3', _FallibleMessage(True)
        ITEMS = [
            (ACK_ID1, MESSAGE1),
            (ACK_ID2, MESSAGE2),
            (ACK_ID3, MESSAGE3),
        ]
        subscription = _FauxSubscription(ITEMS)
        auto_ack = self._makeOne(subscription, client=CLIENT)
        with auto_ack:
            for ack_id, message in list(auto_ack.items()):
                if message.fail:
                    del auto_ack[ack_id]
        self.assertEqual(sorted(subscription._acknowledged),
                         [ACK_ID1, ACK_ID2])
        self.assertTrue(subscription._ack_client is CLIENT)


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

    def __init__(self, name, client):
        self.name = name
        self._client = client
        self.project = client.project
        self.full_name = 'projects/%s/topics/%s' % (client.project, name)
        self.path = '/projects/%s/topics/%s' % (client.project, name)


class _Client(object):

    connection = None

    def __init__(self, project):
        self.project = project

    def topic(self, name, timestamp_messages=False):
        from gcloud.pubsub.topic import Topic
        return Topic(name, client=self, timestamp_messages=timestamp_messages)


class _FallibleMessage(object):

    def __init__(self, fail=False):
        self.fail = fail


class _FauxSubscription(object):

    def __init__(self, items):
        self._items = items
        self._mapping = dict(items)
        self._acknowledged = set()

    def pull(self, return_immediately=False, max_messages=1, client=None):
        self._return_immediately = return_immediately
        self._max_messages = max_messages
        self._client = client
        return self._items

    def acknowledge(self, ack_ids, client=None):
        self._ack_client = client
        for ack_id in ack_ids:
            message = self._mapping[ack_id]
            assert not message.fail
            self._acknowledged.add(ack_id)
