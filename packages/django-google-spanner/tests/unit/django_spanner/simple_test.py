# Copyright 2021 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

from django_spanner.client import DatabaseClient
from django_spanner.base import DatabaseWrapper
from django_spanner.operations import DatabaseOperations

# from unittest import TestCase
from tests._helpers import OpenTelemetryBase
import os


class SpannerSimpleTestClass(OpenTelemetryBase):
    @classmethod
    def setUpClass(cls):
        super(SpannerSimpleTestClass, cls).setUpClass()
        cls.PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]

        cls.INSTANCE_ID = "instance_id"
        cls.DATABASE_ID = "database_id"
        cls.USER_AGENT = "django_spanner/2.2.0a1"
        cls.OPTIONS = {"option": "dummy"}

        cls.settings_dict = {
            "PROJECT": cls.PROJECT,
            "INSTANCE": cls.INSTANCE_ID,
            "NAME": cls.DATABASE_ID,
            "user_agent": cls.USER_AGENT,
            "OPTIONS": cls.OPTIONS,
        }
        cls.db_client = DatabaseClient(cls.settings_dict)
        cls.db_wrapper = cls.connection = DatabaseWrapper(cls.settings_dict)
        cls.db_operations = DatabaseOperations(cls.connection)
