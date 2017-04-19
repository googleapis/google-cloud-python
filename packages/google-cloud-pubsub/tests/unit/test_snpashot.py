# Copyright 2017 Google Inc.
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


class TestSnapshot(unittest.TestCase):
    PROJECT = 'PROJECT'
    SNAPSHOT_NAME = 'snapshot_name'
    SNAPSHOT_PATH = 'projects/%s/snapshots/%s' % (PROJECT, SNAPSHOT_NAME)
    SUB_NAME = 'subscription_name'
    SUB_PATH = 'projects/%s/subscriptions/%s' % (PROJECT, SUB_NAME)
    TOPIC_NAME = 'topic_name'
    TOPIC_PATH = 'projects/%s/topics/%s' % (PROJECT, TOPIC_NAME)

    @staticmethod
    def _get_target_class():
        from google.cloud.pubsub.snapshot import Snapshot

        return Snapshot

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor(self):
        client = _Client(project=self.PROJECT)
        snapshot = self._make_one(self.SNAPSHOT_NAME,
                               client=client)
        self.assertEqual(snapshot.name, self.SNAPSHOT_NAME)
        self.assertEqual(snapshot.project, self.PROJECT)
        self.assertEqual(snapshot.full_name, self.SNAPSHOT_PATH)
        self.assertEqual(snapshot.path, '/%s' % (self.SNAPSHOT_PATH, ))

    def test_ctor_w_subscription(self):
        client = _Client(project=self.PROJECT)
        subscription = _Subscription(name=self.SUB_NAME, client=client)
        snapshot = self._make_one(self.SNAPSHOT_NAME,
                               subscription=subscription)
        self.assertEqual(snapshot.name, self.SNAPSHOT_NAME)
        self.assertEqual(snapshot.project, self.PROJECT)
        self.assertEqual(snapshot.full_name, self.SNAPSHOT_PATH)
        self.assertEqual(snapshot.path, '/%s' % (self.SNAPSHOT_PATH, ))

    def test_ctor_error(self):
        client = _Client(project=self.PROJECT)
        subscription = _Subscription(name=self.SUB_NAME, client=client)
        with self.assertRaises(TypeError):
            snapshot = self._make_one(self.SNAPSHOT_NAME,
                                      client=client,
                                      subscription=subscription)

    def test_from_api_repr_no_topics(self):
        from google.cloud.pubsub.topic import Topic

        client = _Client(project=self.PROJECT)
        resource = {
            'name': self.SNAPSHOT_PATH,
            'topic': self.TOPIC_PATH
        }
        klass = self._get_target_class()
        snapshot = klass.from_api_repr(resource, client=client)
        self.assertEqual(snapshot.name, self.SNAPSHOT_NAME)
        self.assertIs(snapshot._client, client)
        self.assertEqual(snapshot.project, self.PROJECT)
        self.assertEqual(snapshot.full_name, self.SNAPSHOT_PATH)
        self.assertIsInstance(snapshot.topic, Topic)

    def test_from_api_repr_w_deleted_topic(self):
        client = _Client(project=self.PROJECT)
        klass = self._get_target_class()
        resource = {
            'name': self.SNAPSHOT_PATH,
            'topic': klass._DELETED_TOPIC_PATH
        }
        snapshot = klass.from_api_repr(resource, client=client)
        self.assertEqual(snapshot.name, self.SNAPSHOT_NAME)
        self.assertIs(snapshot._client, client)
        self.assertEqual(snapshot.project, self.PROJECT)
        self.assertEqual(snapshot.full_name, self.SNAPSHOT_PATH)
        self.assertIsNone(snapshot.topic)

    def test_from_api_repr_w_topics_w_no_topic_match(self):
        from google.cloud.pubsub.topic import Topic

        client = _Client(project=self.PROJECT)
        klass = self._get_target_class()
        resource = {
            'name': self.SNAPSHOT_PATH,
            'topic': self.TOPIC_PATH
        }
        topics = {}
        snapshot = klass.from_api_repr(resource, client=client, topics=topics)
        topic = snapshot.topic
        self.assertIsInstance(topic, Topic)
        self.assertIs(topic, topics[self.TOPIC_PATH])
        self.assertEqual(topic.name, self.TOPIC_NAME)
        self.assertEqual(topic.project, self.PROJECT)

    def test_from_api_repr_w_topics_w_topic_match(self):
        from google.cloud.pubsub.topic import Topic

        client = _Client(project=self.PROJECT)
        klass = self._get_target_class()
        resource = {
            'name': self.SNAPSHOT_PATH,
            'topic': self.TOPIC_PATH
        }
        topic = _Topic(self.TOPIC_NAME, client=client)
        topics = {self.TOPIC_PATH: topic}
        snapshot = klass.from_api_repr(resource, client=client, topics=topics)
        self.assertIs(snapshot.topic, topic)

    def test_create_w_bound_client_error(self):
        client = _Client(project=self.PROJECT)
        api = client.subscriber_api = _FauxSubscriberAPI()
        expected_response = api._snapshot_create_response = object()
        snapshot = self._make_one(self.SNAPSHOT_NAME, client=client)

        with self.assertRaises(RuntimeError):
            snapshot.create()

    def test_create_w_bound_subscription(self):
        client = _Client(project=self.PROJECT)
        api = client.subscriber_api = _FauxSubscriberAPI()
        expected_result = api._snapshot_create_response = object()
        subscription = _Subscription(name=self.SUB_NAME, client=client)
        snapshot = self._make_one(self.SNAPSHOT_NAME, subscription=subscription)

        snapshot.create()

        self.assertEqual(api._snapshot_created, (self.SNAPSHOT_PATH, self.SUB_PATH, ))

    def test_create_w_bound_subscription_w_alternate_client(self):
        client = _Client(project=self.PROJECT)
        client2 =  _Client(project=self.PROJECT)
        api = client2.subscriber_api = _FauxSubscriberAPI()
        expected_result = api._snapshot_create_response = object()
        subscription = _Subscription(name=self.SUB_NAME, client=client)
        snapshot = self._make_one(self.SNAPSHOT_NAME, subscription=subscription)

        snapshot.create(client=client2)

        self.assertEqual(api._snapshot_created, (self.SNAPSHOT_PATH, self.SUB_PATH, ))

    def test_delete_w_bound_client(self):
        client = _Client(project=self.PROJECT)
        api = client.subscriber_api = _FauxSubscriberAPI()
        expected_result = api._snapshot_create_response = object()
        snapshot = self._make_one(self.SNAPSHOT_NAME, client=client)

        snapshot.delete()

        self.assertEqual(api._snapshot_deleted, (self.SNAPSHOT_PATH, ))

    def test_delete_w_alternate_client(self):
        client = _Client(project=self.PROJECT)
        api = client.subscriber_api = _FauxSubscriberAPI()
        expected_result = api._snapshot_create_response = object()
        subscription = _Subscription(name=self.SUB_NAME, client=client)
        snapshot = self._make_one(self.SNAPSHOT_NAME, subscription=subscription)

        snapshot.delete()

        self.assertEqual(api._snapshot_deleted, (self.SNAPSHOT_PATH, ))


class _Client(object):

    connection = None

    def __init__(self, project):
        self.project = project

    def topic(self, name):
        from google.cloud.pubsub.topic import Topic

        return Topic(name, client=self)


class _Topic(object):

    def __init__(self, name, client):
        self._client = client


class _Subscription(object):

    def __init__(self, name, client=None):
        self._client = client
        self.full_name = 'projects/%s/subscriptions/%s' % (
            client.project, name, )


class _FauxSubscriberAPI(object):

    def snapshot_create(self, snapshot_path, subscription_path):
        self._snapshot_created = (snapshot_path, subscription_path, )

    def snapshot_delete(self, snapshot_path):
        self._snapshot_deleted = (snapshot_path, )


