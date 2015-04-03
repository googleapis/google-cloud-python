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
from gcloud import pubsub
from gcloud.pubsub.subscription import Subscription
from gcloud.pubsub.topic import Topic


_helpers._PROJECT_ENV_VAR_NAME = 'GCLOUD_TESTS_PROJECT_ID'
pubsub.set_defaults()


class TestPubsub(unittest2.TestCase):

    def setUp(self):
        self.to_delete = []

    def tearDown(self):
        for doomed in self.to_delete:
            doomed.delete()

    def test_create_topic(self):
        TOPIC_NAME = 'a-new-topic'
        topic = Topic(TOPIC_NAME)
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
            topic = Topic(topic_name)
            topic.create()
            self.to_delete.append(topic)

        # Retrieve the topics.
        all_topics, _ = pubsub.list_topics()
        project_id = pubsub.get_default_project()
        created = [topic for topic in all_topics
                   if topic.name in topics_to_create and
                   topic.project == project_id]
        self.assertEqual(len(created), len(topics_to_create))

    def test_create_subscription(self):
        TOPIC_NAME = 'subscribe-me'
        topic = Topic(TOPIC_NAME)
        self.assertFalse(topic.exists())
        topic.create()
        self.to_delete.append(topic)
        SUBSCRIPTION_NAME = 'subscribing-now'
        subscription = Subscription(SUBSCRIPTION_NAME, topic)
        self.assertFalse(subscription.exists())
        subscription.create()
        self.to_delete.append(subscription)
        self.assertTrue(subscription.exists())
        self.assertEqual(subscription.name, SUBSCRIPTION_NAME)
        self.assertTrue(subscription.topic is topic)

    def test_list_subscriptions(self):
        TOPIC_NAME = 'subscribe-me'
        topic = Topic(TOPIC_NAME)
        self.assertFalse(topic.exists())
        topic.create()
        self.to_delete.append(topic)
        subscriptions_to_create = [
            'new%d' % (1000 * time.time(),),
            'newer%d' % (1000 * time.time(),),
            'newest%d' % (1000 * time.time(),),
        ]
        for subscription_name in subscriptions_to_create:
            subscription = Subscription(subscription_name, topic)
            subscription.create()
            self.to_delete.append(subscription)

        # Retrieve the subscriptions.
        all_subscriptions, _ = pubsub.list_subscriptions()
        created = [subscription for subscription in all_subscriptions
                   if subscription.name in subscriptions_to_create and
                   subscription.topic.name == TOPIC_NAME]
        self.assertEqual(len(created), len(subscriptions_to_create))

    def test_message_pull_mode_e2e(self):
        from base64 import b64encode as b64
        TOPIC_NAME = 'subscribe-me'
        topic = Topic(TOPIC_NAME)
        self.assertFalse(topic.exists())
        topic.create()
        self.to_delete.append(topic)
        SUBSCRIPTION_NAME = 'subscribing-now'
        subscription = Subscription(SUBSCRIPTION_NAME, topic)
        self.assertFalse(subscription.exists())
        subscription.create()
        self.to_delete.append(subscription)

        MESSAGE = b'MESSAGE'
        EXTRA = b'EXTRA TWO'
        topic.publish(MESSAGE, extra=EXTRA)

        received = subscription.pull()
        ack_ids = [msg['ackId'] for msg in received]
        subscription.acknowledge(ack_ids)
        one, = received
        self.assertEqual(one['message']['data'], b64(MESSAGE))
        self.assertEqual(one['message']['attributes'], {'extra': EXTRA})
