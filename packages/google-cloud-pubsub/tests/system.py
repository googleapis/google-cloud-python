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

import datetime
import os
import unittest

from google.gax.errors import GaxError
from google.gax.grpc import exc_to_code
from grpc import StatusCode
import httplib2

from google.cloud.environment_vars import PUBSUB_EMULATOR
from google.cloud.exceptions import Conflict
from google.cloud.pubsub import client

from test_utils.retry import RetryInstanceState
from test_utils.retry import RetryResult
from test_utils.retry import RetryErrors
from test_utils.system import EmulatorCreds
from test_utils.system import unique_resource_id


def _unavailable(exc):
    return exc_to_code(exc) == StatusCode.UNAVAILABLE


retry_unavailable = RetryErrors(GaxError, _unavailable)


class Config(object):
    """Run-time configuration to be modified at set-up.

    This is a mutable stand-in to allow test set-up to modify
    global state.
    """
    CLIENT = None
    IN_EMULATOR = False


def setUpModule():
    Config.IN_EMULATOR = os.getenv(PUBSUB_EMULATOR) is not None
    if Config.IN_EMULATOR:
        credentials = EmulatorCreds()
        http = httplib2.Http()  # Un-authorized.
        Config.CLIENT = client.Client(credentials=credentials,
                                      _http=http)
    else:
        Config.CLIENT = client.Client()


def _consume_topics(pubsub_client):
    """Consume entire iterator.

    :type pubsub_client: :class:`~google.cloud.pubsub.client.Client`
    :param pubsub_client: Client to use to retrieve topics.

    :rtype: list
    :returns: List of all topics encountered.
    """
    return list(pubsub_client.list_topics())


def _consume_snapshots(pubsub_client):
    """Consume entire iterator.

    :type pubsub_client: :class:`~google.cloud.pubsub.client.Client`
    :param pubsub_client: Client to use to retrieve snapshots.

    :rtype: list
    :returns: List of all snapshots encountered.
    """
    return list(pubsub_client.list_snapshots())


def _consume_subscriptions(topic):
    """Consume entire iterator.

    :type topic: :class:`~google.cloud.pubsub.topic.Topic`
    :param topic: Topic to use to retrieve subscriptions.

    :rtype: list
    :returns: List of all subscriptions encountered.
    """
    return list(topic.list_subscriptions())


class TestPubsub(unittest.TestCase):

    def setUp(self):
        self.to_delete = []

    def tearDown(self):
        for doomed in self.to_delete:
            doomed.delete()

    def test_create_topic(self):
        topic_name = 'a-new-topic' + unique_resource_id('-')
        topic = Config.CLIENT.topic(topic_name)
        self.assertFalse(topic.exists())
        topic.create()
        self.to_delete.append(topic)
        self.assertTrue(topic.exists())
        self.assertEqual(topic.name, topic_name)

        with self.assertRaises(Conflict):
            topic.create()

    def test_list_topics(self):
        before = _consume_topics(Config.CLIENT)
        topics_to_create = [
            'new' + unique_resource_id(),
            'newer' + unique_resource_id(),
            'newest' + unique_resource_id(),
        ]
        for topic_name in topics_to_create:
            topic = Config.CLIENT.topic(topic_name)
            topic.create()
            self.to_delete.append(topic)

        # Retrieve the topics.
        def _all_created(result):
            return len(result) == len(before) + len(topics_to_create)

        retry = RetryResult(_all_created)
        after = retry(_consume_topics)(Config.CLIENT)

        created = [topic for topic in after
                   if topic.name in topics_to_create and
                   topic.project == Config.CLIENT.project]
        self.assertEqual(len(created), len(topics_to_create))

    def test_create_subscription_defaults(self):
        TOPIC_NAME = 'create-sub-def' + unique_resource_id('-')
        topic = Config.CLIENT.topic(TOPIC_NAME)
        self.assertFalse(topic.exists())
        topic.create()
        self.to_delete.append(topic)
        SUBSCRIPTION_NAME = 'subscribing-now' + unique_resource_id('-')
        subscription = topic.subscription(SUBSCRIPTION_NAME)
        self.assertFalse(subscription.exists())
        subscription.create()
        self.to_delete.append(subscription)
        self.assertTrue(subscription.exists())
        self.assertEqual(subscription.name, SUBSCRIPTION_NAME)
        self.assertIs(subscription.topic, topic)

        with self.assertRaises(Conflict):
            subscription.create()

    def test_create_subscription_w_ack_deadline(self):
        TOPIC_NAME = 'create-sub-ack' + unique_resource_id('-')
        topic = Config.CLIENT.topic(TOPIC_NAME)
        self.assertFalse(topic.exists())
        topic.create()
        self.to_delete.append(topic)
        SUBSCRIPTION_NAME = 'subscribing-now' + unique_resource_id()
        subscription = topic.subscription(SUBSCRIPTION_NAME, ack_deadline=120)
        self.assertFalse(subscription.exists())
        subscription.create()
        self.to_delete.append(subscription)
        self.assertTrue(subscription.exists())
        self.assertEqual(subscription.name, SUBSCRIPTION_NAME)
        self.assertEqual(subscription.ack_deadline, 120)
        self.assertIs(subscription.topic, topic)

    def test_create_subscription_w_message_retention(self):
        TOPIC_NAME = 'create-sub-ack' + unique_resource_id('-')
        topic = Config.CLIENT.topic(TOPIC_NAME)
        self.assertFalse(topic.exists())
        topic.create()
        self.to_delete.append(topic)
        SUBSCRIPTION_NAME = 'subscribing-now' + unique_resource_id()
        duration = datetime.timedelta(hours=12)
        subscription = topic.subscription(
            SUBSCRIPTION_NAME, retain_acked_messages=True,
            message_retention_duration=duration)
        self.assertFalse(subscription.exists())
        subscription.create()
        self.to_delete.append(subscription)
        self.assertTrue(subscription.exists())
        self.assertEqual(subscription.name, SUBSCRIPTION_NAME)
        self.assertTrue(subscription.retain_acked_messages)
        self.assertEqual(subscription.message_retention_duration, duration)
        self.assertIs(subscription.topic, topic)

    def test_list_subscriptions(self):
        TOPIC_NAME = 'list-sub' + unique_resource_id('-')
        topic = Config.CLIENT.topic(TOPIC_NAME)
        topic.create()
        self.to_delete.append(topic)
        empty = _consume_subscriptions(topic)
        self.assertEqual(len(empty), 0)
        subscriptions_to_create = [
            'new' + unique_resource_id(),
            'newer' + unique_resource_id(),
            'newest' + unique_resource_id(),
        ]
        for subscription_name in subscriptions_to_create:
            subscription = topic.subscription(subscription_name)
            subscription.create()
            self.to_delete.append(subscription)

        # Retrieve the subscriptions.
        def _all_created(result):
            return len(result) == len(subscriptions_to_create)

        retry = RetryResult(_all_created)
        all_subscriptions = retry(_consume_subscriptions)(topic)

        created = [subscription for subscription in all_subscriptions
                   if subscription.name in subscriptions_to_create]
        self.assertEqual(len(created), len(subscriptions_to_create))

    def test_message_pull_mode_e2e(self):
        import operator
        TOPIC_NAME = 'message-e2e' + unique_resource_id('-')
        topic = Config.CLIENT.topic(TOPIC_NAME,
                                    timestamp_messages=True)
        self.assertFalse(topic.exists())
        topic.create()
        self.to_delete.append(topic)
        SUBSCRIPTION_NAME = 'subscribing-now' + unique_resource_id('-')
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

        class Hoover(object):

            def __init__(self):
                self.received = []

            def done(self, *dummy):
                return len(self.received) == 2

            def suction(self):
                with subscription.auto_ack(max_messages=2) as ack:
                    self.received.extend(ack.values())

        hoover = Hoover()
        retry = RetryInstanceState(hoover.done)
        retry(hoover.suction)()

        message1, message2 = sorted(hoover.received,
                                    key=operator.attrgetter('timestamp'))

        self.assertEqual(message1.data, MESSAGE_1)
        self.assertEqual(message1.attributes['extra'], EXTRA_1)
        self.assertIsNotNone(message1.service_timestamp)

        self.assertEqual(message2.data, MESSAGE_2)
        self.assertEqual(message2.attributes['extra'], EXTRA_2)
        self.assertIsNotNone(message2.service_timestamp)

    def _maybe_emulator_skip(self):
        # NOTE: This method is necessary because ``Config.IN_EMULATOR``
        #       is set at runtime rather than import time, which means we
        #       can't use the @unittest.skipIf decorator.
        if Config.IN_EMULATOR:
            self.skipTest('IAM not supported by Pub/Sub emulator')

    def test_topic_iam_policy(self):
        from google.cloud.pubsub.iam import PUBSUB_TOPICS_GET_IAM_POLICY
        self._maybe_emulator_skip()
        topic_name = 'test-topic-iam-policy-topic' + unique_resource_id('-')
        topic = Config.CLIENT.topic(topic_name)
        topic.create()

        # Retry / backoff up to 7 seconds (1 + 2 + 4)
        retry = RetryResult(lambda result: result, max_tries=4)
        retry(topic.exists)()
        self.to_delete.append(topic)

        if topic.check_iam_permissions([PUBSUB_TOPICS_GET_IAM_POLICY]):
            policy = topic.get_iam_policy()
            viewers = set(policy.viewers)
            viewers.add(policy.user('jjg@google.com'))
            policy.viewers = viewers
            new_policy = topic.set_iam_policy(policy)
            self.assertEqual(new_policy.viewers, policy.viewers)

    def test_subscription_iam_policy(self):
        from google.cloud.pubsub.iam import PUBSUB_SUBSCRIPTIONS_GET_IAM_POLICY
        self._maybe_emulator_skip()
        topic_name = 'test-sub-iam-policy-topic' + unique_resource_id('-')
        topic = Config.CLIENT.topic(topic_name)
        topic.create()

        # Retry / backoff up to 7 seconds (1 + 2 + 4)
        retry = RetryResult(lambda result: result, max_tries=4)
        retry(topic.exists)()
        self.to_delete.append(topic)

        SUB_NAME = 'test-sub-iam-policy-sub' + unique_resource_id('-')
        subscription = topic.subscription(SUB_NAME)
        subscription.create()

        # Retry / backoff up to 7 seconds (1 + 2 + 4)
        retry = RetryResult(lambda result: result, max_tries=4)
        retry(subscription.exists)()
        self.to_delete.insert(0, subscription)

        if subscription.check_iam_permissions(
                [PUBSUB_SUBSCRIPTIONS_GET_IAM_POLICY]):
            policy = subscription.get_iam_policy()
            viewers = set(policy.viewers)
            viewers.add(policy.user('jjg@google.com'))
            policy.viewers = viewers
            new_policy = subscription.set_iam_policy(policy)
            self.assertEqual(new_policy.viewers, policy.viewers)

    def test_create_snapshot(self):
        TOPIC_NAME = 'create-snap-def' + unique_resource_id('-')
        topic = Config.CLIENT.topic(TOPIC_NAME)
        before_snapshots = _consume_snapshots(Config.CLIENT)

        self.assertFalse(topic.exists())
        topic.create()
        self.to_delete.append(topic)
        SUBSCRIPTION_NAME = 'subscribing-now' + unique_resource_id('-')
        subscription = topic.subscription(SUBSCRIPTION_NAME, ack_deadline=600)
        self.assertFalse(subscription.exists())
        subscription.create()
        self.to_delete.append(subscription)
        SNAPSHOT_NAME = 'new-snapshot' + unique_resource_id('-')
        snapshot = subscription.snapshot(SNAPSHOT_NAME)
        snapshot.create()
        self.to_delete.append(snapshot)

        # There is no GET method for snapshot, so check existence using
        # list
        after_snapshots = _consume_snapshots(Config.CLIENT)
        self.assertEqual(len(before_snapshots) + 1, len(after_snapshots))

        def full_name(obj):
            return obj.full_name

        self.assertIn(snapshot.full_name, map(full_name, after_snapshots))
        self.assertNotIn(snapshot.full_name, map(full_name, before_snapshots))

        with self.assertRaises(Conflict):
            snapshot.create()


    def test_seek(self):
        TOPIC_NAME = 'seek-e2e' + unique_resource_id('-')
        topic = Config.CLIENT.topic(TOPIC_NAME,
                                    timestamp_messages=True)
        self.assertFalse(topic.exists())
        topic.create()
        self.to_delete.append(topic)

        SUBSCRIPTION_NAME = 'subscribing-to-seek' + unique_resource_id('-')
        subscription = topic.subscription(
            SUBSCRIPTION_NAME, retain_acked_messages=True)
        self.assertFalse(subscription.exists())
        subscription.create()
        self.to_delete.append(subscription)

        SNAPSHOT_NAME = 'new-snapshot' + unique_resource_id('-')
        snapshot = subscription.snapshot(SNAPSHOT_NAME)
        snapshot.create()
        self.to_delete.append(snapshot)

        MESSAGE_1 = b'MESSAGE ONE'
        topic.publish(MESSAGE_1)
        MESSAGE_2 = b'MESSAGE TWO'
        topic.publish(MESSAGE_2)

        ((ack_id_1a, recvd_1a), ) = subscription.pull()
        ((ack_id_2a, recvd_2a), ) = subscription.pull()
        before_data = [obj.data for obj in (recvd_1a, recvd_2a)]
        self.assertIn(MESSAGE_1, before_data)
        self.assertIn(MESSAGE_2, before_data)
        subscription.acknowledge((ack_id_1a, ack_id_2a))

        self.assertFalse(subscription.pull(return_immediately=True))

        subscription.seek_snapshot(snapshot)

        ((_, recvd_1b), ) = subscription.pull()
        ((_, recvd_2b), ) = subscription.pull()
        after_data = [obj.data for obj in (recvd_1b, recvd_2b)]
        self.assertEqual(sorted(before_data), sorted(after_data))
