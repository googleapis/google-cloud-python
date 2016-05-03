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
    # pylint: disable=no-name-in-module
    from gcloud.pubsub._gax import _HAVE_GAX
    # pylint: enable=no-name-in-module
except ImportError:  # pragma: NO COVER
    _HAVE_GAX = False


@unittest2.skipUnless(_HAVE_GAX, 'No gax-python')
class Test_PublisherAPI(unittest2.TestCase):
    PROJECT = 'PROJECT'
    PROJECT_PATH = 'projects/%s' % (PROJECT,)
    LIST_TOPICS_PATH = '%s/topics' % (PROJECT_PATH,)
    TOPIC_NAME = 'topic_name'
    TOPIC_PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)
    LIST_TOPIC_SUBSCRIPTIONS_PATH = '%s/subscriptions' % (TOPIC_PATH,)
    SUB_NAME = 'sub_name'
    SUB_PATH = '%s/subscriptions/%s' % (TOPIC_PATH, SUB_NAME)

    def _getTargetClass(self):
        from gcloud.pubsub._gax import _PublisherAPI
        return _PublisherAPI

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

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


class _GAXPublisherAPI(object):

    _create_topic_conflict = False

    def __init__(self, **kw):
        self.__dict__.update(kw)

    def list_topics(self, name, options):
        self._list_topics_called_with = name, options
        return self._list_topics_response

    def create_topic(self, name, options=None):
        # pylint: disable=no-name-in-module
        from google.gax.errors import GaxError
        self._create_topic_called_with = name, options
        if self._create_topic_conflict:
            raise GaxError('conflict')
        return self._create_topic_response

    def get_topic(self, name, options=None):
        # pylint: disable=no-name-in-module
        from google.gax.errors import GaxError
        self._get_topic_called_with = name, options
        try:
            return self._get_topic_response
        except AttributeError:
            raise GaxError('miss')

    def delete_topic(self, name, options=None):
        # pylint: disable=no-name-in-module
        from google.gax.errors import GaxError
        self._delete_topic_called_with = name, options
        if not self._delete_topic_ok:
            raise GaxError('miss')

    def publish(self, topic, messages, options=None):
        # pylint: disable=no-name-in-module
        from google.gax.errors import GaxError
        self._publish_called_with = topic, messages, options
        try:
            return self._publish_response
        except AttributeError:
            raise GaxError('miss')

    def list_topic_subscriptions(self, topic, options=None):
        # pylint: disable=no-name-in-module
        from google.gax.errors import GaxError
        self._list_topic_subscriptions_called_with = topic, options
        try:
            return self._list_topic_subscriptions_response
        except AttributeError:
            raise GaxError('miss')


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
