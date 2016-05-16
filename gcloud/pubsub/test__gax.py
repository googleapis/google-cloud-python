# Copyright 2016 Google Inc. All rights reserved.
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


try:
    # pylint: disable=unused-import
    import gcloud.pubsub._gax
    # pylint: enable=unused-import
except ImportError:  # pragma: NO COVER
    _HAVE_GAX = False
else:
    _HAVE_GAX = True


class _Base(object):
    PROJECT = 'PROJECT'
    PROJECT_PATH = 'projects/%s' % (PROJECT,)
    LIST_TOPICS_PATH = '%s/topics' % (PROJECT_PATH,)
    TOPIC_NAME = 'topic_name'
    TOPIC_PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
    LIST_TOPIC_SUBSCRIPTIONS_PATH = '%s/subscriptions' % (TOPIC_PATH,)
    SUB_NAME = 'sub_name'
    SUB_PATH = '%s/subscriptions/%s' % (TOPIC_PATH, SUB_NAME)

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)


@unittest2.skipUnless(_HAVE_GAX, 'No gax-python')
class Test_PublisherAPI(_Base, unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.pubsub._gax import _PublisherAPI
        return _PublisherAPI

    def test_ctor(self):
        gax_api = _GAXPublisherAPI()
        api = self._makeOne(gax_api)
        self.assertTrue(api._gax_api is gax_api)

    def test_list_topics_no_paging(self):
        response = _ListTopicsResponsePB([_TopicPB(self.TOPIC_PATH)])
        gax_api = _GAXPublisherAPI(_list_topics_response=response)
        api = self._makeOne(gax_api)

        topics, next_token = api.list_topics(self.PROJECT)

        self.assertEqual(len(topics), 1)
        topic = topics[0]
        self.assertIsInstance(topic, dict)
        self.assertEqual(topic['name'], self.TOPIC_PATH)
        self.assertEqual(next_token, None)

        name, options = gax_api._list_topics_called_with
        self.assertEqual(name, self.PROJECT_PATH)
        self.assertFalse(options.is_page_streaming)

    def test_topic_create(self):
        topic_pb = _TopicPB(self.TOPIC_PATH)
        gax_api = _GAXPublisherAPI(_create_topic_response=topic_pb)
        api = self._makeOne(gax_api)

        resource = api.topic_create(self.TOPIC_PATH)

        self.assertEqual(resource, {'name': self.TOPIC_PATH})
        topic_path, options = gax_api._create_topic_called_with
        self.assertEqual(topic_path, self.TOPIC_PATH)
        self.assertEqual(options, None)

    def test_topic_create_already_exists(self):
        from gcloud.exceptions import Conflict
        gax_api = _GAXPublisherAPI(_create_topic_conflict=True)
        api = self._makeOne(gax_api)

        with self.assertRaises(Conflict):
            api.topic_create(self.TOPIC_PATH)

        topic_path, options = gax_api._create_topic_called_with
        self.assertEqual(topic_path, self.TOPIC_PATH)
        self.assertEqual(options, None)

    def test_topic_create_error(self):
        from google.gax.errors import GaxError
        gax_api = _GAXPublisherAPI(_random_gax_error=True)
        api = self._makeOne(gax_api)

        with self.assertRaises(GaxError):
            api.topic_create(self.TOPIC_PATH)

        topic_path, options = gax_api._create_topic_called_with
        self.assertEqual(topic_path, self.TOPIC_PATH)
        self.assertEqual(options, None)

    def test_topic_get_hit(self):
        topic_pb = _TopicPB(self.TOPIC_PATH)
        gax_api = _GAXPublisherAPI(_get_topic_response=topic_pb)
        api = self._makeOne(gax_api)

        resource = api.topic_get(self.TOPIC_PATH)

        self.assertEqual(resource, {'name': self.TOPIC_PATH})
        topic_path, options = gax_api._get_topic_called_with
        self.assertEqual(topic_path, self.TOPIC_PATH)
        self.assertEqual(options, None)

    def test_topic_get_miss(self):
        from gcloud.exceptions import NotFound
        gax_api = _GAXPublisherAPI()
        api = self._makeOne(gax_api)

        with self.assertRaises(NotFound):
            api.topic_get(self.TOPIC_PATH)

        topic_path, options = gax_api._get_topic_called_with
        self.assertEqual(topic_path, self.TOPIC_PATH)
        self.assertEqual(options, None)

    def test_topic_get_error(self):
        from google.gax.errors import GaxError
        gax_api = _GAXPublisherAPI(_random_gax_error=True)
        api = self._makeOne(gax_api)

        with self.assertRaises(GaxError):
            api.topic_get(self.TOPIC_PATH)

        topic_path, options = gax_api._get_topic_called_with
        self.assertEqual(topic_path, self.TOPIC_PATH)
        self.assertEqual(options, None)

    def test_topic_delete_hit(self):
        gax_api = _GAXPublisherAPI(_delete_topic_ok=True)
        api = self._makeOne(gax_api)

        api.topic_delete(self.TOPIC_PATH)

        topic_path, options = gax_api._delete_topic_called_with
        self.assertEqual(topic_path, self.TOPIC_PATH)
        self.assertEqual(options, None)

    def test_topic_delete_miss(self):
        from gcloud.exceptions import NotFound
        gax_api = _GAXPublisherAPI(_delete_topic_ok=False)
        api = self._makeOne(gax_api)

        with self.assertRaises(NotFound):
            api.topic_delete(self.TOPIC_PATH)

        topic_path, options = gax_api._delete_topic_called_with
        self.assertEqual(topic_path, self.TOPIC_PATH)
        self.assertEqual(options, None)

    def test_topic_delete_error(self):
        from google.gax.errors import GaxError
        gax_api = _GAXPublisherAPI(_random_gax_error=True)
        api = self._makeOne(gax_api)

        with self.assertRaises(GaxError):
            api.topic_delete(self.TOPIC_PATH)

        topic_path, options = gax_api._delete_topic_called_with
        self.assertEqual(topic_path, self.TOPIC_PATH)
        self.assertEqual(options, None)

    def test_topic_publish_hit(self):
        import base64
        PAYLOAD = b'This is the message text'
        B64 = base64.b64encode(PAYLOAD).decode('ascii')
        MSGID = 'DEADBEEF'
        MESSAGE = {'data': B64, 'attributes': {}}
        response = _PublishResponsePB([MSGID])
        gax_api = _GAXPublisherAPI(_publish_response=response)
        api = self._makeOne(gax_api)

        resource = api.topic_publish(self.TOPIC_PATH, [MESSAGE])

        self.assertEqual(resource, [MSGID])
        topic_path, message_pbs, options = gax_api._publish_called_with
        self.assertEqual(topic_path, self.TOPIC_PATH)
        message_pb, = message_pbs
        self.assertEqual(message_pb.data, B64)
        self.assertEqual(message_pb.attributes, {})
        self.assertEqual(options, None)

    def test_topic_publish_miss_w_attrs_w_bytes_payload(self):
        import base64
        from gcloud.exceptions import NotFound
        PAYLOAD = u'This is the message text'
        B64 = base64.b64encode(PAYLOAD)
        MESSAGE = {'data': B64, 'attributes': {'foo': 'bar'}}
        gax_api = _GAXPublisherAPI()
        api = self._makeOne(gax_api)

        with self.assertRaises(NotFound):
            api.topic_publish(self.TOPIC_PATH, [MESSAGE])

        topic_path, message_pbs, options = gax_api._publish_called_with
        self.assertEqual(topic_path, self.TOPIC_PATH)
        message_pb, = message_pbs
        self.assertEqual(message_pb.data, B64)
        self.assertEqual(message_pb.attributes, {'foo': 'bar'})
        self.assertEqual(options, None)

    def test_topic_publish_error(self):
        import base64
        from google.gax.errors import GaxError
        PAYLOAD = b'This is the message text'
        B64 = base64.b64encode(PAYLOAD).decode('ascii')
        MESSAGE = {'data': B64, 'attributes': {}}
        gax_api = _GAXPublisherAPI(_random_gax_error=True)
        api = self._makeOne(gax_api)

        with self.assertRaises(GaxError):
            api.topic_publish(self.TOPIC_PATH, [MESSAGE])

        topic_path, message_pbs, options = gax_api._publish_called_with
        self.assertEqual(topic_path, self.TOPIC_PATH)
        message_pb, = message_pbs
        self.assertEqual(message_pb.data, B64)
        self.assertEqual(message_pb.attributes, {})
        self.assertEqual(options, None)

    def test_topic_list_subscriptions_no_paging(self):
        response = _ListTopicSubscriptionsResponsePB([self.SUB_PATH])
        gax_api = _GAXPublisherAPI(_list_topic_subscriptions_response=response)
        api = self._makeOne(gax_api)

        subscriptions, next_token = api.topic_list_subscriptions(
            self.TOPIC_PATH)

        self.assertEqual(len(subscriptions), 1)
        subscription = subscriptions[0]
        self.assertIsInstance(subscription, dict)
        self.assertEqual(subscription['name'], self.SUB_PATH)
        self.assertEqual(subscription['topic'], self.TOPIC_PATH)
        self.assertEqual(next_token, None)

        topic_path, options = gax_api._list_topic_subscriptions_called_with
        self.assertEqual(topic_path, self.TOPIC_PATH)
        self.assertFalse(options.is_page_streaming)

    def test_topic_list_subscriptions_miss(self):
        from gcloud.exceptions import NotFound
        gax_api = _GAXPublisherAPI()
        api = self._makeOne(gax_api)

        with self.assertRaises(NotFound):
            api.topic_list_subscriptions(self.TOPIC_PATH)

        topic_path, options = gax_api._list_topic_subscriptions_called_with
        self.assertEqual(topic_path, self.TOPIC_PATH)
        self.assertFalse(options.is_page_streaming)

    def test_topic_list_subscriptions_error(self):
        from google.gax.errors import GaxError
        gax_api = _GAXPublisherAPI(_random_gax_error=True)
        api = self._makeOne(gax_api)

        with self.assertRaises(GaxError):
            api.topic_list_subscriptions(self.TOPIC_PATH)

        topic_path, options = gax_api._list_topic_subscriptions_called_with
        self.assertEqual(topic_path, self.TOPIC_PATH)
        self.assertFalse(options.is_page_streaming)


@unittest2.skipUnless(_HAVE_GAX, 'No gax-python')
class Test_SubscriberAPI(_Base, unittest2.TestCase):

    PUSH_ENDPOINT = 'https://api.example.com/push'

    def _getTargetClass(self):
        from gcloud.pubsub._gax import _SubscriberAPI
        return _SubscriberAPI

    def test_ctor(self):
        gax_api = _GAXSubscriberAPI()
        api = self._makeOne(gax_api)
        self.assertTrue(api._gax_api is gax_api)

    def test_list_subscriptions_no_paging(self):
        response = _ListSubscriptionsResponsePB([_SubscriptionPB(
            self.SUB_PATH, self.TOPIC_PATH, self.PUSH_ENDPOINT, 0)])
        gax_api = _GAXSubscriberAPI(_list_subscriptions_response=response)
        api = self._makeOne(gax_api)

        subscriptions, next_token = api.list_subscriptions(self.PROJECT)

        self.assertEqual(len(subscriptions), 1)
        subscription = subscriptions[0]
        self.assertIsInstance(subscription, dict)
        self.assertEqual(subscription['name'], self.SUB_PATH)
        self.assertEqual(subscription['topic'], self.TOPIC_PATH)
        self.assertEqual(subscription['pushConfig'],
                         {'pushEndpoint': self.PUSH_ENDPOINT})
        self.assertEqual(subscription['ackDeadlineSeconds'], 0)
        self.assertEqual(next_token, None)

        name, options = gax_api._list_subscriptions_called_with
        self.assertEqual(name, self.PROJECT_PATH)
        self.assertFalse(options.is_page_streaming)

    def test_subscription_create(self):
        sub_pb = _SubscriptionPB(self.SUB_PATH, self.TOPIC_PATH, '', 0)
        gax_api = _GAXSubscriberAPI(_create_subscription_response=sub_pb)
        api = self._makeOne(gax_api)

        resource = api.subscription_create(self.SUB_PATH, self.TOPIC_PATH)

        expected = {
            'name': self.SUB_PATH,
            'topic': self.TOPIC_PATH,
            'ackDeadlineSeconds': 0,
        }
        self.assertEqual(resource, expected)
        name, topic, push_config, ack_deadline, options = (
            gax_api._create_subscription_called_with)
        self.assertEqual(name, self.SUB_PATH)
        self.assertEqual(topic, self.TOPIC_PATH)
        self.assertEqual(push_config, None)
        self.assertEqual(ack_deadline, 0)
        self.assertEqual(options, None)

    def test_subscription_create_already_exists(self):
        from gcloud.exceptions import Conflict
        DEADLINE = 600
        gax_api = _GAXSubscriberAPI(_create_subscription_conflict=True)
        api = self._makeOne(gax_api)

        with self.assertRaises(Conflict):
            api.subscription_create(
                self.SUB_PATH, self.TOPIC_PATH, DEADLINE, self.PUSH_ENDPOINT)

        name, topic, push_config, ack_deadline, options = (
            gax_api._create_subscription_called_with)
        self.assertEqual(name, self.SUB_PATH)
        self.assertEqual(topic, self.TOPIC_PATH)
        self.assertEqual(push_config.push_endpoint, self.PUSH_ENDPOINT)
        self.assertEqual(ack_deadline, DEADLINE)
        self.assertEqual(options, None)

    def test_subscription_create_error(self):
        from google.gax.errors import GaxError
        gax_api = _GAXSubscriberAPI(_random_gax_error=True)
        api = self._makeOne(gax_api)

        with self.assertRaises(GaxError):
            api.subscription_create(self.SUB_PATH, self.TOPIC_PATH)

        name, topic, push_config, ack_deadline, options = (
            gax_api._create_subscription_called_with)
        self.assertEqual(name, self.SUB_PATH)
        self.assertEqual(topic, self.TOPIC_PATH)
        self.assertEqual(push_config, None)
        self.assertEqual(ack_deadline, 0)
        self.assertEqual(options, None)

    def test_subscription_get_hit(self):
        sub_pb = _SubscriptionPB(
            self.SUB_PATH, self.TOPIC_PATH, self.PUSH_ENDPOINT, 0)
        gax_api = _GAXSubscriberAPI(_get_subscription_response=sub_pb)
        api = self._makeOne(gax_api)

        resource = api.subscription_get(self.SUB_PATH)

        expected = {
            'name': self.SUB_PATH,
            'topic': self.TOPIC_PATH,
            'ackDeadlineSeconds': 0,
            'pushConfig': {
                'pushEndpoint': self.PUSH_ENDPOINT,
            },
        }
        self.assertEqual(resource, expected)
        sub_path, options = gax_api._get_subscription_called_with
        self.assertEqual(sub_path, self.SUB_PATH)
        self.assertEqual(options, None)

    def test_subscription_get_miss(self):
        from gcloud.exceptions import NotFound
        gax_api = _GAXSubscriberAPI()
        api = self._makeOne(gax_api)

        with self.assertRaises(NotFound):
            api.subscription_get(self.SUB_PATH)

        sub_path, options = gax_api._get_subscription_called_with
        self.assertEqual(sub_path, self.SUB_PATH)
        self.assertEqual(options, None)

    def test_subscription_get_error(self):
        from google.gax.errors import GaxError
        gax_api = _GAXSubscriberAPI(_random_gax_error=True)
        api = self._makeOne(gax_api)

        with self.assertRaises(GaxError):
            api.subscription_get(self.SUB_PATH)

        sub_path, options = gax_api._get_subscription_called_with
        self.assertEqual(sub_path, self.SUB_PATH)
        self.assertEqual(options, None)

    def test_subscription_delete_hit(self):
        gax_api = _GAXSubscriberAPI(_delete_subscription_ok=True)
        api = self._makeOne(gax_api)

        api.subscription_delete(self.TOPIC_PATH)

        sub_path, options = gax_api._delete_subscription_called_with
        self.assertEqual(sub_path, self.TOPIC_PATH)
        self.assertEqual(options, None)

    def test_subscription_delete_miss(self):
        from gcloud.exceptions import NotFound
        gax_api = _GAXSubscriberAPI(_delete_subscription_ok=False)
        api = self._makeOne(gax_api)

        with self.assertRaises(NotFound):
            api.subscription_delete(self.TOPIC_PATH)

        sub_path, options = gax_api._delete_subscription_called_with
        self.assertEqual(sub_path, self.TOPIC_PATH)
        self.assertEqual(options, None)

    def test_subscription_delete_error(self):
        from google.gax.errors import GaxError
        gax_api = _GAXSubscriberAPI(_random_gax_error=True)
        api = self._makeOne(gax_api)

        with self.assertRaises(GaxError):
            api.subscription_delete(self.TOPIC_PATH)

        sub_path, options = gax_api._delete_subscription_called_with
        self.assertEqual(sub_path, self.TOPIC_PATH)
        self.assertEqual(options, None)

    def test_subscription_modify_push_config_hit(self):
        gax_api = _GAXSubscriberAPI(_modify_push_config_ok=True)
        api = self._makeOne(gax_api)

        api.subscription_modify_push_config(self.SUB_PATH, self.PUSH_ENDPOINT)

        sub_path, config, options = gax_api._modify_push_config_called_with
        self.assertEqual(sub_path, self.SUB_PATH)
        self.assertEqual(config.push_endpoint, self.PUSH_ENDPOINT)
        self.assertEqual(options, None)

    def test_subscription_modify_push_config_miss(self):
        from gcloud.exceptions import NotFound
        gax_api = _GAXSubscriberAPI()
        api = self._makeOne(gax_api)

        with self.assertRaises(NotFound):
            api.subscription_modify_push_config(
                self.SUB_PATH, self.PUSH_ENDPOINT)

        sub_path, config, options = gax_api._modify_push_config_called_with
        self.assertEqual(sub_path, self.SUB_PATH)
        self.assertEqual(config.push_endpoint, self.PUSH_ENDPOINT)
        self.assertEqual(options, None)

    def test_subscription_modify_push_config_error(self):
        from google.gax.errors import GaxError
        gax_api = _GAXSubscriberAPI(_random_gax_error=True)
        api = self._makeOne(gax_api)

        with self.assertRaises(GaxError):
            api.subscription_modify_push_config(
                self.SUB_PATH, self.PUSH_ENDPOINT)

        sub_path, config, options = gax_api._modify_push_config_called_with
        self.assertEqual(sub_path, self.SUB_PATH)
        self.assertEqual(config.push_endpoint, self.PUSH_ENDPOINT)
        self.assertEqual(options, None)

    def test_subscription_pull_explicit(self):
        import base64
        PAYLOAD = b'This is the message text'
        B64 = base64.b64encode(PAYLOAD).decode('ascii')
        ACK_ID = 'DEADBEEF'
        MSG_ID = 'BEADCAFE'
        MESSAGE = {'messageId': MSG_ID, 'data': B64, 'attributes': {'a': 'b'}}
        RECEIVED = [{'ackId': ACK_ID, 'message': MESSAGE}]
        message_pb = _PubsubMessagePB(MSG_ID, B64, {'a': 'b'})
        response_pb = _PullResponsePB([_ReceivedMessagePB(ACK_ID, message_pb)])
        gax_api = _GAXSubscriberAPI(_pull_response=response_pb)
        api = self._makeOne(gax_api)
        MAX_MESSAGES = 10

        received = api.subscription_pull(
            self.SUB_PATH, return_immediately=True, max_messages=MAX_MESSAGES)

        self.assertEqual(received, RECEIVED)
        sub_path, max_messages, return_immediately, options = (
            gax_api._pull_called_with)
        self.assertEqual(sub_path, self.SUB_PATH)
        self.assertEqual(max_messages, MAX_MESSAGES)
        self.assertTrue(return_immediately)
        self.assertEqual(options, None)

    def test_subscription_pull_defaults_miss(self):
        from gcloud.exceptions import NotFound
        gax_api = _GAXSubscriberAPI()
        api = self._makeOne(gax_api)

        with self.assertRaises(NotFound):
            api.subscription_pull(self.SUB_PATH)

        sub_path, max_messages, return_immediately, options = (
            gax_api._pull_called_with)
        self.assertEqual(sub_path, self.SUB_PATH)
        self.assertEqual(max_messages, 1)
        self.assertFalse(return_immediately)
        self.assertEqual(options, None)

    def test_subscription_pull_defaults_error(self):
        from google.gax.errors import GaxError
        gax_api = _GAXSubscriberAPI(_random_gax_error=True)
        api = self._makeOne(gax_api)

        with self.assertRaises(GaxError):
            api.subscription_pull(self.SUB_PATH)

        sub_path, max_messages, return_immediately, options = (
            gax_api._pull_called_with)
        self.assertEqual(sub_path, self.SUB_PATH)
        self.assertEqual(max_messages, 1)
        self.assertFalse(return_immediately)
        self.assertEqual(options, None)

    def test_subscription_acknowledge_hit(self):
        ACK_ID1 = 'DEADBEEF'
        ACK_ID2 = 'BEADCAFE'
        gax_api = _GAXSubscriberAPI(_acknowledge_ok=True)
        api = self._makeOne(gax_api)

        api.subscription_acknowledge(self.SUB_PATH, [ACK_ID1, ACK_ID2])

        sub_path, ack_ids, options = gax_api._acknowledge_called_with
        self.assertEqual(sub_path, self.SUB_PATH)
        self.assertEqual(ack_ids, [ACK_ID1, ACK_ID2])
        self.assertEqual(options, None)

    def test_subscription_acknowledge_miss(self):
        from gcloud.exceptions import NotFound
        ACK_ID1 = 'DEADBEEF'
        ACK_ID2 = 'BEADCAFE'
        gax_api = _GAXSubscriberAPI()
        api = self._makeOne(gax_api)

        with self.assertRaises(NotFound):
            api.subscription_acknowledge(self.SUB_PATH, [ACK_ID1, ACK_ID2])

        sub_path, ack_ids, options = gax_api._acknowledge_called_with
        self.assertEqual(sub_path, self.SUB_PATH)
        self.assertEqual(ack_ids, [ACK_ID1, ACK_ID2])
        self.assertEqual(options, None)

    def test_subscription_acknowledge_error(self):
        from google.gax.errors import GaxError
        ACK_ID1 = 'DEADBEEF'
        ACK_ID2 = 'BEADCAFE'
        gax_api = _GAXSubscriberAPI(_random_gax_error=True)
        api = self._makeOne(gax_api)

        with self.assertRaises(GaxError):
            api.subscription_acknowledge(self.SUB_PATH, [ACK_ID1, ACK_ID2])

        sub_path, ack_ids, options = gax_api._acknowledge_called_with
        self.assertEqual(sub_path, self.SUB_PATH)
        self.assertEqual(ack_ids, [ACK_ID1, ACK_ID2])
        self.assertEqual(options, None)

    def test_subscription_modify_ack_deadline_hit(self):
        ACK_ID1 = 'DEADBEEF'
        ACK_ID2 = 'BEADCAFE'
        NEW_DEADLINE = 90
        gax_api = _GAXSubscriberAPI(_modify_ack_deadline_ok=True)
        api = self._makeOne(gax_api)

        api.subscription_modify_ack_deadline(
            self.SUB_PATH, [ACK_ID1, ACK_ID2], NEW_DEADLINE)

        sub_path, ack_ids, deadline, options = (
            gax_api._modify_ack_deadline_called_with)
        self.assertEqual(sub_path, self.SUB_PATH)
        self.assertEqual(ack_ids, [ACK_ID1, ACK_ID2])
        self.assertEqual(deadline, NEW_DEADLINE)
        self.assertEqual(options, None)

    def test_subscription_modify_ack_deadline_miss(self):
        from gcloud.exceptions import NotFound
        ACK_ID1 = 'DEADBEEF'
        ACK_ID2 = 'BEADCAFE'
        NEW_DEADLINE = 90
        gax_api = _GAXSubscriberAPI()
        api = self._makeOne(gax_api)

        with self.assertRaises(NotFound):
            api.subscription_modify_ack_deadline(
                self.SUB_PATH, [ACK_ID1, ACK_ID2], NEW_DEADLINE)

        sub_path, ack_ids, deadline, options = (
            gax_api._modify_ack_deadline_called_with)
        self.assertEqual(sub_path, self.SUB_PATH)
        self.assertEqual(ack_ids, [ACK_ID1, ACK_ID2])
        self.assertEqual(deadline, NEW_DEADLINE)
        self.assertEqual(options, None)

    def test_subscription_modify_ack_deadline_error(self):
        from google.gax.errors import GaxError
        ACK_ID1 = 'DEADBEEF'
        ACK_ID2 = 'BEADCAFE'
        NEW_DEADLINE = 90
        gax_api = _GAXSubscriberAPI(_random_gax_error=True)
        api = self._makeOne(gax_api)

        with self.assertRaises(GaxError):
            api.subscription_modify_ack_deadline(
                self.SUB_PATH, [ACK_ID1, ACK_ID2], NEW_DEADLINE)

        sub_path, ack_ids, deadline, options = (
            gax_api._modify_ack_deadline_called_with)
        self.assertEqual(sub_path, self.SUB_PATH)
        self.assertEqual(ack_ids, [ACK_ID1, ACK_ID2])
        self.assertEqual(deadline, NEW_DEADLINE)
        self.assertEqual(options, None)


class _GaxAPIBase(object):

    _random_gax_error = False

    def __init__(self, **kw):
        self.__dict__.update(kw)

    def _make_grpc_error(self, status_code):
        from grpc.framework.interfaces.face.face import AbortionError

        class _DummyException(AbortionError):
            code = status_code

            def __init__(self):
                pass

        return _DummyException()

    def _make_grpc_not_found(self):
        from grpc.beta.interfaces import StatusCode
        return self._make_grpc_error(StatusCode.NOT_FOUND)

    def _make_grpc_failed_precondition(self):
        from grpc.beta.interfaces import StatusCode
        return self._make_grpc_error(StatusCode.FAILED_PRECONDITION)


class _GAXPublisherAPI(_GaxAPIBase):

    _create_topic_conflict = False

    def list_topics(self, name, options):
        self._list_topics_called_with = name, options
        return self._list_topics_response

    def create_topic(self, name, options=None):
        from google.gax.errors import GaxError
        self._create_topic_called_with = name, options
        if self._random_gax_error:
            raise GaxError('error')
        if self._create_topic_conflict:
            raise GaxError('conflict', self._make_grpc_failed_precondition())
        return self._create_topic_response

    def get_topic(self, name, options=None):
        from google.gax.errors import GaxError
        self._get_topic_called_with = name, options
        if self._random_gax_error:
            raise GaxError('error')
        try:
            return self._get_topic_response
        except AttributeError:
            raise GaxError('miss', self._make_grpc_not_found())

    def delete_topic(self, name, options=None):
        from google.gax.errors import GaxError
        self._delete_topic_called_with = name, options
        if self._random_gax_error:
            raise GaxError('error')
        if not self._delete_topic_ok:
            raise GaxError('miss', self._make_grpc_not_found())

    def publish(self, topic, messages, options=None):
        from google.gax.errors import GaxError
        self._publish_called_with = topic, messages, options
        if self._random_gax_error:
            raise GaxError('error')
        try:
            return self._publish_response
        except AttributeError:
            raise GaxError('miss', self._make_grpc_not_found())

    def list_topic_subscriptions(self, topic, options=None):
        from google.gax.errors import GaxError
        self._list_topic_subscriptions_called_with = topic, options
        if self._random_gax_error:
            raise GaxError('error')
        try:
            return self._list_topic_subscriptions_response
        except AttributeError:
            raise GaxError('miss', self._make_grpc_not_found())


class _GAXSubscriberAPI(_GaxAPIBase):

    _create_subscription_conflict = False
    _modify_push_config_ok = False
    _acknowledge_ok = False
    _modify_ack_deadline_ok = False

    def list_subscriptions(self, project, options=None):
        self._list_subscriptions_called_with = (project, options)
        return self._list_subscriptions_response

    def create_subscription(self, name, topic,
                            push_config, ack_deadline_seconds,
                            options=None):
        from google.gax.errors import GaxError
        self._create_subscription_called_with = (
            name, topic, push_config, ack_deadline_seconds, options)
        if self._random_gax_error:
            raise GaxError('error')
        if self._create_subscription_conflict:
            raise GaxError('conflict', self._make_grpc_failed_precondition())
        return self._create_subscription_response

    def get_subscription(self, name, options=None):
        from google.gax.errors import GaxError
        self._get_subscription_called_with = name, options
        if self._random_gax_error:
            raise GaxError('error')
        try:
            return self._get_subscription_response
        except AttributeError:
            raise GaxError('miss', self._make_grpc_not_found())

    def delete_subscription(self, name, options=None):
        from google.gax.errors import GaxError
        self._delete_subscription_called_with = name, options
        if self._random_gax_error:
            raise GaxError('error')
        if not self._delete_subscription_ok:
            raise GaxError('miss', self._make_grpc_not_found())

    def modify_push_config(self, name, push_config, options=None):
        from google.gax.errors import GaxError
        self._modify_push_config_called_with = name, push_config, options
        if self._random_gax_error:
            raise GaxError('error')
        if not self._modify_push_config_ok:
            raise GaxError('miss', self._make_grpc_not_found())

    def pull(self, name, max_messages, return_immediately, options=None):
        from google.gax.errors import GaxError
        self._pull_called_with = (
            name, max_messages, return_immediately, options)
        if self._random_gax_error:
            raise GaxError('error')
        try:
            return self._pull_response
        except AttributeError:
            raise GaxError('miss', self._make_grpc_not_found())

    def acknowledge(self, name, ack_ids, options=None):
        from google.gax.errors import GaxError
        self._acknowledge_called_with = name, ack_ids, options
        if self._random_gax_error:
            raise GaxError('error')
        if not self._acknowledge_ok:
            raise GaxError('miss', self._make_grpc_not_found())

    def modify_ack_deadline(self, name, ack_ids, deadline, options=None):
        from google.gax.errors import GaxError
        self._modify_ack_deadline_called_with = (
            name, ack_ids, deadline, options)
        if self._random_gax_error:
            raise GaxError('error')
        if not self._modify_ack_deadline_ok:
            raise GaxError('miss', self._make_grpc_not_found())


class _TopicPB(object):

    def __init__(self, name):
        self.name = name


class _PublishResponsePB(object):

    def __init__(self, message_ids):
        self.message_ids = message_ids


class _ListTopicsResponsePB(object):

    def __init__(self, topic_pbs, next_page_token=None):
        self.topics = topic_pbs
        self.next_page_token = next_page_token


class _ListTopicSubscriptionsResponsePB(object):

    def __init__(self, subscriptions, next_page_token=None):
        self.subscriptions = subscriptions
        self.next_page_token = next_page_token


class _PushConfigPB(object):

    def __init__(self, push_endpoint):
        self.push_endpoint = push_endpoint


class _PubsubMessagePB(object):

    def __init__(self, message_id, data, attributes):
        self.message_id = message_id
        self.data = data
        self.attributes = attributes


class _ReceivedMessagePB(object):

    def __init__(self, ack_id, message):
        self.ack_id = ack_id
        self.message = message


class _PullResponsePB(object):

    def __init__(self, received_messages):
        self.received_messages = received_messages


class _SubscriptionPB(object):

    def __init__(self, name, topic, push_endpoint, ack_deadline_seconds):
        self.name = name
        self.topic = topic
        self.push_config = _PushConfigPB(push_endpoint)
        self.ack_deadline_seconds = ack_deadline_seconds


class _ListSubscriptionsResponsePB(object):

    def __init__(self, subscription_pbs, next_page_token=None):
        self.subscriptions = subscription_pbs
        self.next_page_token = next_page_token
