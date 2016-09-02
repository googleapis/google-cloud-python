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

import os
import unittest

from google.gax.errors import GaxError
from grpc import StatusCode
from grpc._channel import _Rendezvous
import httplib2

from gcloud import _helpers
from gcloud.environment_vars import PUBSUB_EMULATOR
from gcloud.environment_vars import TESTS_PROJECT
from gcloud import pubsub

from retry import RetryInstanceState
from retry import RetryResult
from retry import RetryErrors
from system_test_utils import EmulatorCreds
from system_test_utils import unique_resource_id


def _unavailable(exc):
    return _helpers.exc_to_code(exc) == StatusCode.UNAVAILABLE


retry_unavailable = RetryErrors((GaxError, _Rendezvous), _unavailable)


class Config(object):
    """Run-time configuration to be modified at set-up.

    This is a mutable stand-in to allow test set-up to modify
    global state.
    """
    CLIENT = None


def setUpModule():
    _helpers.PROJECT = TESTS_PROJECT
    if os.getenv(PUBSUB_EMULATOR) is None:
        Config.CLIENT = pubsub.Client()
    else:
        credentials = EmulatorCreds()
        http = httplib2.Http()  # Un-authorized.
        Config.CLIENT = pubsub.Client(credentials=credentials,
                                      http=http)


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

    def test_list_topics(self):
        before, _ = Config.CLIENT.list_topics()
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
            return len(result[0]) == len(before) + len(topics_to_create)

        retry = RetryResult(_all_created)
        after, _ = retry(Config.CLIENT.list_topics)()

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
        self.assertTrue(subscription.topic is topic)

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
        self.assertTrue(subscription.topic is topic)

    def test_list_subscriptions(self):
        TOPIC_NAME = 'list-sub' + unique_resource_id('-')
        topic = Config.CLIENT.topic(TOPIC_NAME)
        topic.create()
        self.to_delete.append(topic)
        empty, _ = topic.list_subscriptions()
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
            return len(result[0]) == len(subscriptions_to_create)

        retry = RetryResult(_all_created)
        all_subscriptions, _ = retry(topic.list_subscriptions)()

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
        self.assertEqual(message2.data, MESSAGE_2)
        self.assertEqual(message2.attributes['extra'], EXTRA_2)

    def _maybe_emulator_skip(self):
        # NOTE: We check at run-time rather than using the @unittest.skipIf
        #       decorator. This matches the philosophy behind using
        #       setUpModule to determine the environment at run-time
        #       rather than at import time.
        if os.getenv(PUBSUB_EMULATOR) is not None:
            self.skipTest('IAM not supported by Pub/Sub emulator')

    def test_topic_iam_policy(self):
        from gcloud.pubsub.iam import PUBSUB_TOPICS_GET_IAM_POLICY
        self._maybe_emulator_skip()
        topic_name = 'test-topic-iam-policy-topic' + unique_resource_id('-')
        topic = Config.CLIENT.topic(topic_name)
        topic.create()

        # Retry / backoff up to 7 seconds (1 + 2 + 4)
        retry = RetryResult(lambda result: result, max_tries=4)
        retry(topic.exists)()

        self.assertTrue(topic.exists())
        self.to_delete.append(topic)

        if topic.check_iam_permissions([PUBSUB_TOPICS_GET_IAM_POLICY]):
            policy = topic.get_iam_policy()
            policy.viewers.add(policy.user('jjg@google.com'))
            new_policy = topic.set_iam_policy(policy)
            self.assertEqual(new_policy.viewers, policy.viewers)

    def test_subscription_iam_policy(self):
        from gcloud.pubsub.iam import PUBSUB_SUBSCRIPTIONS_GET_IAM_POLICY
        self._maybe_emulator_skip()
        topic_name = 'test-sub-iam-policy-topic' + unique_resource_id('-')
        topic = Config.CLIENT.topic(topic_name)
        topic.create()

        # Retry / backoff up to 7 seconds (1 + 2 + 4)
        retry = RetryResult(lambda result: result, max_tries=4)
        retry(topic.exists)()

        self.assertTrue(topic.exists())
        self.to_delete.append(topic)
        SUB_NAME = 'test-sub-iam-policy-sub' + unique_resource_id('-')
        subscription = topic.subscription(SUB_NAME)
        subscription.create()

        # Retry / backoff up to 7 seconds (1 + 2 + 4)
        retry = RetryResult(lambda result: result, max_tries=4)
        retry(subscription.exists)()

        self.assertTrue(subscription.exists())
        self.to_delete.insert(0, subscription)

        if subscription.check_iam_permissions(
                [PUBSUB_SUBSCRIPTIONS_GET_IAM_POLICY]):
            policy = subscription.get_iam_policy()
            policy.viewers.add(policy.user('jjg@google.com'))
            new_policy = subscription.set_iam_policy(policy)
            self.assertEqual(new_policy.viewers, policy.viewers)

    # This test is ultra-flaky.  See:
    # https://github.com/GoogleCloudPlatform/gcloud-python/issues/2080
    @unittest.expectedFailure
    def test_fetch_delete_subscription_w_deleted_topic(self):
        from gcloud.iterator import MethodIterator
        TO_DELETE = 'delete-me' + unique_resource_id('-')
        ORPHANED = 'orphaned' + unique_resource_id('-')
        topic = Config.CLIENT.topic(TO_DELETE)
        topic.create()
        subscription = topic.subscription(ORPHANED)
        subscription.create()
        topic.delete()

        def _fetch():
            return list(MethodIterator(Config.CLIENT.list_subscriptions))

        def _found_orphan(result):
            names = [subscription.name for subscription in result]
            return ORPHANED in names

        retry_until_found_orphan = RetryResult(_found_orphan)
        all_subs = retry_until_found_orphan(_fetch)()

        created = [subscription for subscription in all_subs
                   if subscription.name == ORPHANED]
        self.assertEqual(len(created), 1)
        orphaned = created[0]

        def _no_topic(instance):
            return instance.topic is None

        retry_until_no_topic = RetryInstanceState(_no_topic)
        retry_until_no_topic(orphaned.reload)()

        self.assertTrue(orphaned.topic is None)
        orphaned.delete()
