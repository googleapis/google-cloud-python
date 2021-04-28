# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

import sys
import unittest
import os


@unittest.skipIf(
    sys.version_info < (3, 6), reason="Skipping Python versions <= 3.5"
)
class TestClient(unittest.TestCase):
    PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
    INSTANCE_ID = "instance_id"
    DATABASE_ID = "database_id"
    USER_AGENT = "django_spanner/2.2.0a1"
    OPTIONS = {"option": "dummy"}

    settings_dict = {
        "PROJECT": PROJECT,
        "INSTANCE": INSTANCE_ID,
        "NAME": DATABASE_ID,
        "user_agent": USER_AGENT,
        "OPTIONS": OPTIONS,
    }

    def _get_target_class(self):
        from django_spanner.client import DatabaseClient

        return DatabaseClient

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_runshell(self):
        from google.cloud.spanner_dbapi.exceptions import NotSupportedError

        db_wrapper = self._make_one(self.settings_dict)

        with self.assertRaises(NotSupportedError):
            db_wrapper.runshell(parameters=self.settings_dict)
