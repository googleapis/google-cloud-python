# Copyright 2017 Google LLC
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

    BUCKET_NAME = "test-bucket"
    BUCKET_PROJECT = "bucket-project-123"
    TOPIC_NAME = "test-topic"
    TOPIC_ALT_PROJECT = "topic-project-456"
    TOPIC_REF_FMT = "//pubsub.googleapis.com/projects/{}/topics/{}"
    TOPIC_REF = TOPIC_REF_FMT.format(BUCKET_PROJECT, TOPIC_NAME)
    TOPIC_ALT_REF = TOPIC_REF_FMT.format(TOPIC_ALT_PROJECT, TOPIC_NAME)
    CUSTOM_ATTRIBUTES = {"attr1": "value1", "attr2": "value2"}
    BLOB_NAME_PREFIX = "blob-name-prefix/"
    NOTIFICATION_ID = "123"
    SELF_LINK = "https://example.com/notification/123"
    ETAG = "DEADBEEF"
    CREATE_PATH = "/b/{}/notificationConfigs".format(BUCKET_NAME)
    NOTIFICATION_PATH = "/b/{}/notificationConfigs/{}".format(
        BUCKET_NAME, NOTIFICATION_ID
    )

    @staticmethod
    def event_types():
        from google.cloud.storage.notification import (
            OBJECT_FINALIZE_EVENT_TYPE,
            OBJECT_DELETE_EVENT_TYPE,
        )

        return [OBJECT_FINALIZE_EVENT_TYPE, OBJECT_DELETE_EVENT_TYPE]

    @staticmethod
    def payload_format():
        from google.cloud.storage.notification import JSON_API_V1_PAYLOAD_FORMAT

        return JSON_API_V1_PAYLOAD_FORMAT

    @staticmethod
    def _get_default_timeout():
        from google.cloud.storage.constants import _DEFAULT_TIMEOUT

        return _DEFAULT_TIMEOUT

    @staticmethod
    def _get_target_class():
        from google.cloud.storage.notification import BucketNotification

        return BucketNotification

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def _make_client(self, project=BUCKET_PROJECT):
        from google.cloud.storage.client import Client

        return mock.Mock(project=project, spec=Client)

    def _make_bucket(self, client, name=BUCKET_NAME, user_project=None):
        bucket = mock.Mock(spec=["client", "name", "user_project"])
        bucket.client = client
        bucket.name = name
        bucket.user_project = user_project
        return bucket

    def test_ctor_w_missing_project(self):
        client = self._make_client(project=None)
        bucket = self._make_bucket(client)

        with self.assertRaises(ValueError):
            self._make_one(bucket, self.TOPIC_NAME)

    def test_ctor_defaults(self):
        from google.cloud.storage.notification import NONE_PAYLOAD_FORMAT

        client = self._make_client()
        bucket = self._make_bucket(client)

        notification = self._make_one(bucket, self.TOPIC_NAME)

        self.assertIs(notification.bucket, bucket)
        self.assertEqual(notification.topic_name, self.TOPIC_NAME)
        self.assertEqual(notification.topic_project, self.BUCKET_PROJECT)
        self.assertIsNone(notification.custom_attributes)
        self.assertIsNone(notification.event_types)
        self.assertIsNone(notification.blob_name_prefix)
        self.assertEqual(notification.payload_format, NONE_PAYLOAD_FORMAT)

    def test_ctor_explicit(self):
        client = self._make_client()
        bucket = self._make_bucket(client)

        notification = self._make_one(
            bucket,
            self.TOPIC_NAME,
            topic_project=self.TOPIC_ALT_PROJECT,
            custom_attributes=self.CUSTOM_ATTRIBUTES,
            event_types=self.event_types(),
            blob_name_prefix=self.BLOB_NAME_PREFIX,
            payload_format=self.payload_format(),
        )

        self.assertIs(notification.bucket, bucket)
        self.assertEqual(notification.topic_name, self.TOPIC_NAME)
        self.assertEqual(notification.topic_project, self.TOPIC_ALT_PROJECT)
        self.assertEqual(notification.custom_attributes, self.CUSTOM_ATTRIBUTES)
        self.assertEqual(notification.event_types, self.event_types())
        self.assertEqual(notification.blob_name_prefix, self.BLOB_NAME_PREFIX)
        self.assertEqual(notification.payload_format, self.payload_format())

    def test_from_api_repr_no_topic(self):
        klass = self._get_target_class()
        client = self._make_client()
        bucket = self._make_bucket(client)
        resource = {}

        with self.assertRaises(ValueError):
            klass.from_api_repr(resource, bucket=bucket)

    def test_from_api_repr_invalid_topic(self):
        klass = self._get_target_class()
        client = self._make_client()
        bucket = self._make_bucket(client)
        resource = {"topic": "@#$%"}

        with self.assertRaises(ValueError):
            klass.from_api_repr(resource, bucket=bucket)

    def test_from_api_repr_minimal(self):
        from google.cloud.storage.notification import NONE_PAYLOAD_FORMAT

        klass = self._get_target_class()
        client = self._make_client()
        bucket = self._make_bucket(client)
        resource = {
            "topic": self.TOPIC_REF,
            "id": self.NOTIFICATION_ID,
            "etag": self.ETAG,
            "selfLink": self.SELF_LINK,
            "payload_format": NONE_PAYLOAD_FORMAT,
        }

        notification = klass.from_api_repr(resource, bucket=bucket)

        self.assertIs(notification.bucket, bucket)
        self.assertEqual(notification.topic_name, self.TOPIC_NAME)
        self.assertEqual(notification.topic_project, self.BUCKET_PROJECT)
        self.assertIsNone(notification.custom_attributes)
        self.assertIsNone(notification.event_types)
        self.assertIsNone(notification.blob_name_prefix)
        self.assertEqual(notification.payload_format, NONE_PAYLOAD_FORMAT)
        self.assertEqual(notification.etag, self.ETAG)
        self.assertEqual(notification.self_link, self.SELF_LINK)

    def test_from_api_repr_explicit(self):
        klass = self._get_target_class()
        client = self._make_client()
        bucket = self._make_bucket(client)
        resource = {
            "topic": self.TOPIC_ALT_REF,
            "custom_attributes": self.CUSTOM_ATTRIBUTES,
            "event_types": self.event_types(),
            "object_name_prefix": self.BLOB_NAME_PREFIX,
            "payload_format": self.payload_format(),
            "id": self.NOTIFICATION_ID,
            "etag": self.ETAG,
            "selfLink": self.SELF_LINK,
        }

        notification = klass.from_api_repr(resource, bucket=bucket)

        self.assertIs(notification.bucket, bucket)
        self.assertEqual(notification.topic_name, self.TOPIC_NAME)
        self.assertEqual(notification.topic_project, self.TOPIC_ALT_PROJECT)
        self.assertEqual(notification.custom_attributes, self.CUSTOM_ATTRIBUTES)
        self.assertEqual(notification.event_types, self.event_types())
        self.assertEqual(notification.blob_name_prefix, self.BLOB_NAME_PREFIX)
        self.assertEqual(notification.payload_format, self.payload_format())
        self.assertEqual(notification.notification_id, self.NOTIFICATION_ID)
        self.assertEqual(notification.etag, self.ETAG)
        self.assertEqual(notification.self_link, self.SELF_LINK)

    def test_notification_id(self):
        client = self._make_client()
        bucket = self._make_bucket(client)

        notification = self._make_one(bucket, self.TOPIC_NAME)

        self.assertIsNone(notification.notification_id)

        notification._properties["id"] = self.NOTIFICATION_ID
        self.assertEqual(notification.notification_id, self.NOTIFICATION_ID)

    def test_etag(self):
        client = self._make_client()
        bucket = self._make_bucket(client)

        notification = self._make_one(bucket, self.TOPIC_NAME)

        self.assertIsNone(notification.etag)

        notification._properties["etag"] = self.ETAG
        self.assertEqual(notification.etag, self.ETAG)

    def test_self_link(self):
        client = self._make_client()
        bucket = self._make_bucket(client)

        notification = self._make_one(bucket, self.TOPIC_NAME)

        self.assertIsNone(notification.self_link)

        notification._properties["selfLink"] = self.SELF_LINK
        self.assertEqual(notification.self_link, self.SELF_LINK)

    def test_create_w_existing_notification_id(self):
        client = self._make_client()
        bucket = self._make_bucket(client)
        notification = self._make_one(bucket, self.TOPIC_NAME)
        notification._properties["id"] = self.NOTIFICATION_ID

        with self.assertRaises(ValueError):
            notification.create()

    def test_create_w_defaults(self):
        from google.cloud.storage.notification import NONE_PAYLOAD_FORMAT

        client = self._make_client()
        bucket = self._make_bucket(client)
        notification = self._make_one(bucket, self.TOPIC_NAME)
        api_request = client._connection.api_request
        api_request.return_value = {
            "topic": self.TOPIC_REF,
            "id": self.NOTIFICATION_ID,
            "etag": self.ETAG,
            "selfLink": self.SELF_LINK,
            "payload_format": NONE_PAYLOAD_FORMAT,
        }

        notification.create()

        self.assertEqual(notification.notification_id, self.NOTIFICATION_ID)
        self.assertEqual(notification.etag, self.ETAG)
        self.assertEqual(notification.self_link, self.SELF_LINK)
        self.assertIsNone(notification.custom_attributes)
        self.assertIsNone(notification.event_types)
        self.assertIsNone(notification.blob_name_prefix)
        self.assertEqual(notification.payload_format, NONE_PAYLOAD_FORMAT)

        data = {"topic": self.TOPIC_REF, "payload_format": NONE_PAYLOAD_FORMAT}
        api_request.assert_called_once_with(
            method="POST",
            path=self.CREATE_PATH,
            query_params={},
            data=data,
            timeout=self._get_default_timeout(),
        )

    def test_create_w_explicit_client(self):
        USER_PROJECT = "user-project-123"
        client = self._make_client()
        alt_client = self._make_client()
        bucket = self._make_bucket(client, user_project=USER_PROJECT)
        notification = self._make_one(
            bucket,
            self.TOPIC_NAME,
            topic_project=self.TOPIC_ALT_PROJECT,
            custom_attributes=self.CUSTOM_ATTRIBUTES,
            event_types=self.event_types(),
            blob_name_prefix=self.BLOB_NAME_PREFIX,
            payload_format=self.payload_format(),
        )
        api_request = alt_client._connection.api_request
        api_request.return_value = {
            "topic": self.TOPIC_ALT_REF,
            "custom_attributes": self.CUSTOM_ATTRIBUTES,
            "event_types": self.event_types(),
            "object_name_prefix": self.BLOB_NAME_PREFIX,
            "payload_format": self.payload_format(),
            "id": self.NOTIFICATION_ID,
            "etag": self.ETAG,
            "selfLink": self.SELF_LINK,
        }

        notification.create(client=alt_client, timeout=42)

        self.assertEqual(notification.custom_attributes, self.CUSTOM_ATTRIBUTES)
        self.assertEqual(notification.event_types, self.event_types())
        self.assertEqual(notification.blob_name_prefix, self.BLOB_NAME_PREFIX)
        self.assertEqual(notification.payload_format, self.payload_format())
        self.assertEqual(notification.notification_id, self.NOTIFICATION_ID)
        self.assertEqual(notification.etag, self.ETAG)
        self.assertEqual(notification.self_link, self.SELF_LINK)

        data = {
            "topic": self.TOPIC_ALT_REF,
            "custom_attributes": self.CUSTOM_ATTRIBUTES,
            "event_types": self.event_types(),
            "object_name_prefix": self.BLOB_NAME_PREFIX,
            "payload_format": self.payload_format(),
        }
        api_request.assert_called_once_with(
            method="POST",
            path=self.CREATE_PATH,
            query_params={"userProject": USER_PROJECT},
            data=data,
            timeout=42,
        )

    def test_exists_wo_notification_id(self):
        client = self._make_client()
        bucket = self._make_bucket(client)
        notification = self._make_one(bucket, self.TOPIC_NAME)

        with self.assertRaises(ValueError):
            notification.exists()

    def test_exists_miss(self):
        from google.cloud.exceptions import NotFound

        client = self._make_client()
        bucket = self._make_bucket(client)
        notification = self._make_one(bucket, self.TOPIC_NAME)
        notification._properties["id"] = self.NOTIFICATION_ID
        api_request = client._connection.api_request
        api_request.side_effect = NotFound("testing")

        self.assertFalse(notification.exists(timeout=42))

        api_request.assert_called_once_with(
            method="GET", path=self.NOTIFICATION_PATH, query_params={}, timeout=42
        )

    def test_exists_hit(self):
        USER_PROJECT = "user-project-123"
        client = self._make_client()
        bucket = self._make_bucket(client, user_project=USER_PROJECT)
        notification = self._make_one(bucket, self.TOPIC_NAME)
        notification._properties["id"] = self.NOTIFICATION_ID
        api_request = client._connection.api_request
        api_request.return_value = {
            "topic": self.TOPIC_REF,
            "id": self.NOTIFICATION_ID,
            "etag": self.ETAG,
            "selfLink": self.SELF_LINK,
        }

        self.assertTrue(notification.exists(client=client))

        api_request.assert_called_once_with(
            method="GET",
            path=self.NOTIFICATION_PATH,
            query_params={"userProject": USER_PROJECT},
            timeout=self._get_default_timeout(),
        )

    def test_reload_wo_notification_id(self):
        client = self._make_client()
        bucket = self._make_bucket(client)
        notification = self._make_one(bucket, self.TOPIC_NAME)

        with self.assertRaises(ValueError):
            notification.reload()

    def test_reload_miss(self):
        from google.cloud.exceptions import NotFound

        client = self._make_client()
        bucket = self._make_bucket(client)
        notification = self._make_one(bucket, self.TOPIC_NAME)
        notification._properties["id"] = self.NOTIFICATION_ID
        api_request = client._connection.api_request
        api_request.side_effect = NotFound("testing")

        with self.assertRaises(NotFound):
            notification.reload(timeout=42)

        api_request.assert_called_once_with(
            method="GET", path=self.NOTIFICATION_PATH, query_params={}, timeout=42
        )

    def test_reload_hit(self):
        from google.cloud.storage.notification import NONE_PAYLOAD_FORMAT

        USER_PROJECT = "user-project-123"
        client = self._make_client()
        bucket = self._make_bucket(client, user_project=USER_PROJECT)
        notification = self._make_one(bucket, self.TOPIC_NAME)
        notification._properties["id"] = self.NOTIFICATION_ID
        api_request = client._connection.api_request
        api_request.return_value = {
            "topic": self.TOPIC_REF,
            "id": self.NOTIFICATION_ID,
            "etag": self.ETAG,
            "selfLink": self.SELF_LINK,
            "payload_format": NONE_PAYLOAD_FORMAT,
        }

        notification.reload(client=client)

        self.assertEqual(notification.etag, self.ETAG)
        self.assertEqual(notification.self_link, self.SELF_LINK)
        self.assertIsNone(notification.custom_attributes)
        self.assertIsNone(notification.event_types)
        self.assertIsNone(notification.blob_name_prefix)
        self.assertEqual(notification.payload_format, NONE_PAYLOAD_FORMAT)

        api_request.assert_called_once_with(
            method="GET",
            path=self.NOTIFICATION_PATH,
            query_params={"userProject": USER_PROJECT},
            timeout=self._get_default_timeout(),
        )

    def test_delete_wo_notification_id(self):
        client = self._make_client()
        bucket = self._make_bucket(client)
        notification = self._make_one(bucket, self.TOPIC_NAME)

        with self.assertRaises(ValueError):
            notification.delete()

    def test_delete_miss(self):
        from google.cloud.exceptions import NotFound

        client = self._make_client()
        bucket = self._make_bucket(client)
        notification = self._make_one(bucket, self.TOPIC_NAME)
        notification._properties["id"] = self.NOTIFICATION_ID
        api_request = client._connection.api_request
        api_request.side_effect = NotFound("testing")

        with self.assertRaises(NotFound):
            notification.delete(timeout=42)

        api_request.assert_called_once_with(
            method="DELETE", path=self.NOTIFICATION_PATH, query_params={}, timeout=42
        )

    def test_delete_hit(self):
        USER_PROJECT = "user-project-123"
        client = self._make_client()
        bucket = self._make_bucket(client, user_project=USER_PROJECT)
        notification = self._make_one(bucket, self.TOPIC_NAME)
        notification._properties["id"] = self.NOTIFICATION_ID
        api_request = client._connection.api_request
        api_request.return_value = None

        notification.delete(client=client)

        api_request.assert_called_once_with(
            method="DELETE",
            path=self.NOTIFICATION_PATH,
            query_params={"userProject": USER_PROJECT},
            timeout=self._get_default_timeout(),
        )


class Test__parse_topic_path(unittest.TestCase):
    @staticmethod
    def _call_fut(*args, **kwargs):
        from google.cloud.storage import notification

        return notification._parse_topic_path(*args, **kwargs)

    @staticmethod
    def _make_topic_path(project, topic_name):
        from google.cloud.storage import notification

        return notification._TOPIC_REF_FMT.format(project, topic_name)

    def test_project_name_too_long(self):
        project = "a" * 31
        topic_path = self._make_topic_path(project, "topic-name")
        with self.assertRaises(ValueError):
            self._call_fut(topic_path)

    def test_project_name_uppercase(self):
        project = "aaaAaa"
        topic_path = self._make_topic_path(project, "topic-name")
        with self.assertRaises(ValueError):
            self._call_fut(topic_path)

    def test_leading_digit(self):
        project = "1aaaaa"
        topic_path = self._make_topic_path(project, "topic-name")
        with self.assertRaises(ValueError):
            self._call_fut(topic_path)

    def test_leading_hyphen(self):
        project = "-aaaaa"
        topic_path = self._make_topic_path(project, "topic-name")
        with self.assertRaises(ValueError):
            self._call_fut(topic_path)

    def test_trailing_hyphen(self):
        project = "aaaaa-"
        topic_path = self._make_topic_path(project, "topic-name")
        with self.assertRaises(ValueError):
            self._call_fut(topic_path)

    def test_invalid_format(self):
        topic_path = "@#$%"
        with self.assertRaises(ValueError):
            self._call_fut(topic_path)

    def test_success(self):
        topic_name = "tah-pic-nehm"
        project_choices = (
            "a" * 30,  # Max length.
            "a-b--c---d",  # Valid hyphen usage.
            "abcdefghijklmnopqrstuvwxyz",  # Valid letters.
            "z0123456789",  # Valid digits (non-leading).
            "a-bcdefghijklmn12opqrstuv0wxyz",
        )
        for project in project_choices:
            topic_path = self._make_topic_path(project, topic_name)
            result = self._call_fut(topic_path)
            self.assertEqual(result, (topic_name, project))
