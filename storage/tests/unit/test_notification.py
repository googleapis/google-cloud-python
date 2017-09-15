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
    TOPIC_REF_FMT = '//pubsub.googleapis.com/projects/{}/topics/{}'
    TOPIC_REF = TOPIC_REF_FMT.format(BUCKET_PROJECT, TOPIC_NAME)
    TOPIC_ALT_REF = TOPIC_REF_FMT.format(TOPIC_ALT_PROJECT, TOPIC_NAME)
    CUSTOM_ATTRIBUTES = {
        'attr1': 'value1',
        'attr2': 'value2',
    }
    BLOB_NAME_PREFIX = 'blob-name-prefix/'

    @staticmethod
    def event_types():
        from google.cloud.storage.notification import (
            OBJECT_FINALIZE_EVENT_TYPE,
            OBJECT_DELETE_EVENT_TYPE)

        return [OBJECT_FINALIZE_EVENT_TYPE, OBJECT_DELETE_EVENT_TYPE]

    @staticmethod
    def payload_format():
        from google.cloud.storage.notification import (
            JSON_API_V1_PAYLOAD_FORMAT)

        return JSON_API_V1_PAYLOAD_FORMAT

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
         bucket = mock.Mock(spec=['client', 'name'])
         bucket.client= client
         bucket.name = name
         return bucket

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
        client = self._make_client()
        bucket = self._make_bucket(client)

        notification = self._make_one(
            bucket, self.TOPIC_NAME,
            topic_project=self.TOPIC_ALT_PROJECT,
            custom_attributes=self.CUSTOM_ATTRIBUTES,
            event_types=self.event_types(),
            blob_name_prefix=self.BLOB_NAME_PREFIX,
            payload_format=self.payload_format(),
        )

        self.assertIs(notification.bucket, bucket)
        self.assertEqual(notification.topic_name, self.TOPIC_NAME)
        self.assertEqual(notification.topic_project, self.TOPIC_ALT_PROJECT)
        self.assertEqual(
            notification.custom_attributes, self.CUSTOM_ATTRIBUTES)
        self.assertEqual(notification.event_types, self.event_types())
        self.assertEqual(notification.blob_name_prefix, self.BLOB_NAME_PREFIX)
        self.assertEqual(
            notification.payload_format, self.payload_format())

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

    def test_create_w_existing_notification_id(self):
        NOTIFICATION_ID = '123'
        client = self._make_client()
        bucket = self._make_bucket(client)
        notification = self._make_one(
            bucket, self.TOPIC_NAME)
        notification._properties['id'] = NOTIFICATION_ID

        with self.assertRaises(ValueError):
            notification.create()

    def test_create_w_defaults(self):
        NOTIFICATION_ID = '123'
        ETAG = 'DEADBEEF'
        SELF_LINK = 'https://example.com/notification/123'
        client = self._make_client()
        bucket = self._make_bucket(client)
        notification = self._make_one(
            bucket, self.TOPIC_NAME)
        api_request = client._connection.api_request
        api_request.return_value = {
            'topic': self.TOPIC_REF,
            'id': NOTIFICATION_ID,
            'etag': ETAG,
            'selfLink': SELF_LINK,
        }

        notification.create()

        self.assertEqual(notification.notification_id, NOTIFICATION_ID)
        self.assertEqual(notification.etag, ETAG)
        self.assertEqual(notification.self_link, SELF_LINK)
        self.assertIsNone(notification.custom_attributes)
        self.assertIsNone(notification.event_types)
        self.assertIsNone(notification.blob_name_prefix)
        self.assertIsNone(notification.payload_format)

        path = '/b/{}/notificationConfigs'.format(self.BUCKET_NAME)
        data = {
            'topic': self.TOPIC_REF,
        }
        api_request.assert_called_once_with(
            method='POST',
            path=path,
            data=data,
        )

    def test_create_w_explicit_client(self):
        NOTIFICATION_ID = '123'
        ETAG = 'DEADBEEF'
        SELF_LINK = 'https://example.com/notification/123'
        client = self._make_client()
        alt_client = self._make_client()
        bucket = self._make_bucket(client)
        notification = self._make_one(
            bucket, self.TOPIC_NAME,
            topic_project=self.TOPIC_ALT_PROJECT,
            custom_attributes=self.CUSTOM_ATTRIBUTES,
            event_types=self.event_types(),
            blob_name_prefix=self.BLOB_NAME_PREFIX,
            payload_format=self.payload_format(),
        )
        api_request = alt_client._connection.api_request
        api_request.return_value = {
            'topic': self.TOPIC_ALT_REF,
            'custom_attributes': self.CUSTOM_ATTRIBUTES,
            'event_types': self.event_types(),
            'blob_name_prefix': self.BLOB_NAME_PREFIX,
            'payload_format': self.payload_format(),
            'id': NOTIFICATION_ID,
            'etag': ETAG,
            'selfLink': SELF_LINK,
        }

        notification.create(client=alt_client)

        self.assertEqual(
            notification.custom_attributes, self.CUSTOM_ATTRIBUTES)
        self.assertEqual(notification.event_types, self.event_types())
        self.assertEqual(notification.blob_name_prefix, self.BLOB_NAME_PREFIX)
        self.assertEqual(
            notification.payload_format, self.payload_format())
        self.assertEqual(notification.notification_id, NOTIFICATION_ID)
        self.assertEqual(notification.etag, ETAG)
        self.assertEqual(notification.self_link, SELF_LINK)

        path = '/b/{}/notificationConfigs'.format(self.BUCKET_NAME)
        data = {
            'topic': self.TOPIC_ALT_REF,
            'custom_attributes': self.CUSTOM_ATTRIBUTES,
            'event_types': self.event_types(),
            'blob_name_prefix': self.BLOB_NAME_PREFIX,
            'payload_format': self.payload_format(),
        }
        api_request.assert_called_once_with(
            method='POST',
            path=path,
            data=data,
        )
