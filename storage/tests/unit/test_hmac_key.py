# Copyright 2019 Google LLC
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


class TestHMACKeyMetadata(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.storage.hmac_key import HMACKeyMetadata

        return HMACKeyMetadata

    def _make_one(self, client=None, *args, **kw):
        if client is None:
            client = object()
        return self._get_target_class()(client, *args, **kw)

    def test_ctor_defaults(self):
        client = object()
        metadata = self._make_one(client)
        self.assertIs(metadata._client, client)
        self.assertEqual(metadata._properties, {})
        self.assertIsNone(metadata.access_id)
        self.assertIsNone(metadata.etag)
        self.assertIsNone(metadata.project)
        self.assertIsNone(metadata.service_account_email)
        self.assertIsNone(metadata.state)
        self.assertIsNone(metadata.time_created)
        self.assertIsNone(metadata.updated)

    def test_access_id_getter(self):
        metadata = self._make_one()
        expected = "ACCESS-ID"
        metadata._properties["accessId"] = expected
        self.assertEqual(metadata.access_id, expected)

    def test_etag_getter(self):
        metadata = self._make_one()
        expected = "ETAG"
        metadata._properties["etag"] = expected
        self.assertEqual(metadata.etag, expected)

    def test_project_getter(self):
        metadata = self._make_one()
        expected = "PROJECT-ID"
        metadata._properties["projectId"] = expected
        self.assertEqual(metadata.project, expected)

    def test_service_account_email_getter(self):
        metadata = self._make_one()
        expected = "service_account@example.com"
        metadata._properties["serviceAccountEmail"] = expected
        self.assertEqual(metadata.service_account_email, expected)

    def test_state_getter(self):
        metadata = self._make_one()
        expected = "STATE"
        metadata._properties["state"] = expected
        self.assertEqual(metadata.state, expected)

    def test_state_setter_invalid_state(self):
        metadata = self._make_one()
        expected = "INVALID"

        with self.assertRaises(ValueError):
            metadata.state = expected

        self.assertIsNone(metadata.state)

    def test_state_setter_inactive(self):
        metadata = self._make_one()
        metadata._properties["state"] = "ACTIVE"
        expected = "INACTIVE"
        metadata.state = expected
        self.assertEqual(metadata.state, expected)
        self.assertEqual(metadata._properties["state"], expected)

    def test_state_setter_active(self):
        metadata = self._make_one()
        metadata._properties["state"] = "INACTIVE"
        expected = "ACTIVE"
        metadata.state = expected
        self.assertEqual(metadata.state, expected)
        self.assertEqual(metadata._properties["state"], expected)

    def test_time_created_getter(self):
        import datetime
        from pytz import UTC

        metadata = self._make_one()
        now = datetime.datetime.utcnow()
        now_stamp = "{}Z".format(now.isoformat())
        metadata._properties["timeCreated"] = now_stamp
        self.assertEqual(metadata.time_created, now.replace(tzinfo=UTC))

    def test_updated_getter(self):
        import datetime
        from pytz import UTC

        metadata = self._make_one()
        now = datetime.datetime.utcnow()
        now_stamp = "{}Z".format(now.isoformat())
        metadata._properties["updated"] = now_stamp
        self.assertEqual(metadata.updated, now.replace(tzinfo=UTC))
