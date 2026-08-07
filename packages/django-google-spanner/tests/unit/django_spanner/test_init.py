# Copyright 2026 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

import datetime
from unittest import mock
from django.db import DEFAULT_DB_ALIAS
from django.db.models import JSONField, AutoField
from google.api_core.datetime_helpers import DatetimeWithNanoseconds
from google.cloud.spanner_v1 import JsonObject

from django_spanner import autofield_init
from tests.unit.django_spanner.simple_test import SpannerSimpleTestClass


class TestInit(SpannerSimpleTestClass):
    def test_jsonfield_get_prep_value(self):
        json_field = JSONField()

        # Dict value should be wrapped in JsonObject
        res_dict = json_field.get_prep_value({"a": 1})
        self.assertIsInstance(res_dict, JsonObject)
        self.assertEqual(res_dict, JsonObject({"a": 1}))

        # JsonObject value should be returned as-is
        jo = JsonObject({"b": 2})
        self.assertEqual(json_field.get_prep_value(jo), jo)

        # Other types should be returned as-is
        self.assertEqual(json_field.get_prep_value("string"), "string")
        self.assertIsNone(json_field.get_prep_value(None))

    def test_datetimewithnanoseconds_eq(self):
        UTC = datetime.timezone.utc
        dt = datetime.datetime(2020, 1, 10, 2, 44, 57, 999, UTC)
        dt_diff = datetime.datetime(2021, 1, 10, 2, 44, 57, 999, UTC)
        dtns1 = DatetimeWithNanoseconds(2020, 1, 10, 2, 44, 57, 999, UTC)
        dtns2 = DatetimeWithNanoseconds(2020, 1, 10, 2, 44, 57, 999, UTC)
        dtns3 = DatetimeWithNanoseconds(2020, 1, 10, 2, 44, 58, 000, UTC)

        # Equals another DatetimeWithNanoseconds (same instance or values)
        self.assertTrue(dtns1 == dtns2)
        self.assertFalse(dtns1 == dtns3)
        self.assertTrue(dtns1 != dtns3)
        self.assertFalse(dtns1 != dtns2)

        # Equals datetime.datetime with same ctime
        self.assertTrue(dtns1 == dt)
        self.assertFalse(dtns1 == dt_diff)

        # When old_datetimewithnanoseconds_eq is None
        with mock.patch("django_spanner.old_datetimewithnanoseconds_eq", None):
            self.assertTrue(dtns1 == dt)
            self.assertFalse(dtns1 == dt_diff)
            self.assertFalse(dtns1 == "not_a_dt")

        from django_spanner import datetimewithnanoseconds_eq
        self.assertFalse(datetimewithnanoseconds_eq(dtns1, dtns3))
        self.assertFalse(datetimewithnanoseconds_eq(dtns1, dt_diff))

    def test_gen_rand_int64(self):
        from django_spanner import gen_rand_int64
        val = gen_rand_int64()
        self.assertGreaterEqual(val, 0)
        self.assertLessEqual(val, 0x7FFFFFFFFFFFFFFF)

    def test_autofield_init_options(self):
        field = AutoField()
        autofield_init(field)
        self.assertTrue(field.blank)
