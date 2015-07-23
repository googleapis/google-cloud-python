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

import time

import unittest2

from gcloud import _helpers
from gcloud.environment_vars import TESTS_PROJECT
from gcloud import pubsub


_helpers.PROJECT = TESTS_PROJECT
CLIENT = pubsub.Client()


class TestPubsub(unittest2.TestCase):

    def setUp(self):
        self.to_delete = []

    def tearDown(self):
        for doomed in self.to_delete:
            doomed.delete()

    def test_create_topic(self):
        TOPIC_NAME = 'a-new-topic'
        topic = CLIENT.topic(TOPIC_NAME)
        self.assertFalse(topic.exists())
        topic.create()
        self.to_delete.append(topic)
        self.assertTrue(topic.exists())
        self.assertEqual(topic.name, TOPIC_NAME)

    def test_list_topics(self):
        topics_to_create = [
            'new%d' % (1000 * time.time(),),
            'newer%d' % (1000 * time.time(),),
            'newest%d' % (1000 * time.time(),),
        ]
        for topic_name in topics_to_create:
            topic = CLIENT.topic(topic_name)
            topic.create()
            self.to_delete.append(topic)

        # Retrieve the topics.
        all_topics, _ = CLIENT.list_topics()
        created = [topic for topic in all_topics
                   if topic.name in topics_to_create and
                   topic.project == CLIENT.project]
        self.assertEqual(len(created), len(topics_to_create))

    def test_create_subscription(self):
        TOPIC_NAME = 'subscribe-me'
        topic = CLIENT.topic(TOPIC_NAME)
        self.assertFalse(topic.exists())
        topic.create()
        self.to_delete.append(topic)
        SUBSCRIPTION_NAME = 'subscribing-now'
        subscription = topic.subscription(SUBSCRIPTION_NAME)
        self.assertFalse(subscription.exists())
        subscription.create()
        self.to_delete.append(subscription)
        self.assertTrue(subscription.exists())
        self.assertEqual(subscription.name, SUBSCRIPTION_NAME)
        self.assertTrue(subscription.topic is topic)

    def test_list_subscriptions(self):
        TOPIC_NAME = 'subscribe-me'
        topic = CLIENT.topic(TOPIC_NAME)
        self.assertFalse(topic.exists())
        topic.create()
        self.to_delete.append(topic)
        subscriptions_to_create = [
            'new%d' % (1000 * time.time(),),
            'newer%d' % (1000 * time.time(),),
            'newest%d' % (1000 * time.time(),),
        ]
        for subscription_name in subscriptions_to_create:
            subscription = topic.subscription(subscription_name)
            subscription.create()
            self.to_delete.append(subscription)

        # Retrieve the subscriptions.
        all_subscriptions, _ = CLIENT.list_subscriptions()
        created = [subscription for subscription in all_subscriptions
                   if subscription.name in subscriptions_to_create and
                   subscription.topic.name == TOPIC_NAME]
        self.assertEqual(len(created), len(subscriptions_to_create))

    def test_message_pull_mode_e2e(self):
        TOPIC_NAME = 'subscribe-me'
        topic = CLIENT.topic(TOPIC_NAME, timestamp_messages=True)
        self.assertFalse(topic.exists())
        topic.create()
        self.to_delete.append(topic)
        SUBSCRIPTION_NAME = 'subscribing-now'
        subscription = topic.subscription(SUBSCRIPTION_NAME)
        self.assertFalse(subscription.exists())
        subscription.create()
        self.to_delete.append(subscription)

        MESSAGE_1 = b'MESSAGE ONE'
        MESSAGE_2 = b'MESSAGE ONE'
        EXTRA_1 = 'EXTRA 1'
        EXTRA_2 = 'EXTRA 2'
        topic.publish(MESSAGE_1, extra=EXTRA_1)
        topic.publish(MESSAGE_2, extra=EXTRA_2)

        received = subscription.pull(max_messages=2)
        ack_ids = [recv[0] for recv in received]
        subscription.acknowledge(ack_ids)
        messages = [recv[1] for recv in received]

        def _by_timestamp(message):
            return message.timestamp

        message1, message2 = sorted(messages, key=_by_timestamp)
        self.assertEqual(message1.data, MESSAGE_1)
        self.assertEqual(message1.attributes['extra'], EXTRA_1)
        self.assertEqual(message2.data, MESSAGE_2)
        self.assertEqual(message2.attributes['extra'], EXTRA_2)
