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


class TestBucketNotification(unittest.TestCase):

    BUCKET_NAME = 'test-bucket'
    BUCKET_PROJECT = 'bucket-project-123'
    TOPIC_NAME = 'test-topic'
    TOPIC_ALT_PROJECT = 'topic-project-456'

    @staticmethod
    def _get_target_class():
        from google.cloud.storage.notification import BucketNotification

        return BucketNotification

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def _make_client(self, project=BUCKET_PROJECT):
        from google.cloud.storage.client import Client

        return mock.Mock(project=project, spec=Client)

    def _make_bucket(self, client, name=BUCKET_NAME):
        from google.cloud.storage.bucket import Bucket

        return mock.Mock(client=client, name=name, spec=Bucket)

    def test_ctor_defaults(self):
        client = self._make_client()
        bucket = self._make_bucket(client)

        notification = self._make_one(
            bucket, self.TOPIC_NAME)

        self.assertIs(notification.bucket, bucket)
        self.assertEqual(notification.topic_name, self.TOPIC_NAME)
        self.assertEqual(notification.topic_project, self.BUCKET_PROJECT)
        self.assertIsNone(notification.custom_attributes)
        self.assertIsNone(notification.event_types)
        self.assertIsNone(notification.blob_name_prefix)
        self.assertIsNone(notification.payload_format)

    def test_ctor_explicit(self):
        from google.cloud.storage.notification import (
            OBJECT_FINALIZE_EVENT_TYPE,
            OBJECT_DELETE_EVENT_TYPE,
            JSON_API_V1_PAYLOAD_FORMAT)

        client = self._make_client()
        bucket = self._make_bucket(client)
        CUSTOM_ATTRIBUTES = {
            'attr1': 'value1',
            'attr2': 'value2',
        }
        EVENT_TYPES = [OBJECT_FINALIZE_EVENT_TYPE, OBJECT_DELETE_EVENT_TYPE]
        BLOB_NAME_PREFIX = 'blob-name-prefix/'

        notification = self._make_one(
            bucket, self.TOPIC_NAME,
            topic_project=self.TOPIC_ALT_PROJECT,
            custom_attributes=CUSTOM_ATTRIBUTES,
            event_types=EVENT_TYPES,
            blob_name_prefix=BLOB_NAME_PREFIX,
            payload_format=JSON_API_V1_PAYLOAD_FORMAT,
        )

        self.assertIs(notification.bucket, bucket)
        self.assertEqual(notification.topic_name, self.TOPIC_NAME)
        self.assertEqual(notification.topic_project, self.TOPIC_ALT_PROJECT)
        self.assertEqual(notification.custom_attributes, CUSTOM_ATTRIBUTES)
        self.assertEqual(notification.event_types, EVENT_TYPES)
        self.assertEqual(notification.blob_name_prefix, BLOB_NAME_PREFIX)
        self.assertEqual(
            notification.payload_format, JSON_API_V1_PAYLOAD_FORMAT)

    def test_notification_id(self):
        client = self._make_client()
        bucket = self._make_bucket(client)
        NOTIFICATION_ID = '123'

        notification = self._make_one(
            bucket, self.TOPIC_NAME)

        self.assertIsNone(notification.notification_id)

        notification._properties['id'] = NOTIFICATION_ID
        self.assertEqual(notification.notification_id, NOTIFICATION_ID)

    def test_etag(self):
        client = self._make_client()
        bucket = self._make_bucket(client)
        ETAG = 'DEADBEEF'

        notification = self._make_one(
            bucket, self.TOPIC_NAME)

        self.assertIsNone(notification.etag)

        notification._properties['etag'] = ETAG
        self.assertEqual(notification.etag, ETAG)

    def test_self_link(self):
        client = self._make_client()
        bucket = self._make_bucket(client)
        SELF_LINK = 'https://example.com/notification/123'

        notification = self._make_one(
            bucket, self.TOPIC_NAME)

        self.assertIsNone(notification.self_link)

        notification._properties['selfLink'] = SELF_LINK
        self.assertEqual(notification.self_link, SELF_LINK)
