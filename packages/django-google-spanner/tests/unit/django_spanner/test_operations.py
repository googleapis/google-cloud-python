# Copyright 2021 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

import os
import uuid
from base64 import b64encode
from datetime import timedelta
from decimal import Decimal

from django.conf import settings
from django.core.management.color import no_style
from django.db.utils import DatabaseError
from google.cloud.spanner_dbapi.types import DateStr

from unittest import mock

from tests.unit.django_spanner.simple_test import SpannerSimpleTestClass


class TestOperations(SpannerSimpleTestClass):
    def test_execute_sql_flush(self):
        cursor = mock.MagicMock()
        cursor_cm = mock.MagicMock()
        cursor_cm.__enter__.return_value = cursor
        with mock.patch.object(self.db_operations.connection, "get_autocommit", return_value=True):
            with mock.patch.object(self.db_operations.connection, "cursor", return_value=cursor_cm):
                self.db_operations.execute_sql_flush(["DELETE FROM T1 WHERE 1=1"])
                cursor.execute.assert_called_once_with("DELETE FROM T1 WHERE 1=1")

    def test_execute_sql_flush_empty_and_autocommit_false_and_error(self):
        # Empty list
        self.assertIsNone(self.db_operations.execute_sql_flush([]))

        cursor = mock.MagicMock()
        cursor_cm = mock.MagicMock()
        cursor_cm.__enter__.return_value = cursor
        with mock.patch.object(self.db_operations.connection, "get_autocommit", return_value=False):
            with mock.patch.object(self.db_operations.connection, "set_autocommit") as mock_set_auto:
                with mock.patch.object(self.db_operations.connection, "cursor", return_value=cursor_cm):
                    self.db_operations.execute_sql_flush(["DELETE FROM T1 WHERE 1=1"])
                    mock_set_auto.assert_has_calls([mock.call(True), mock.call(False)])

        # Exception during execution causes no-progress error
        cursor_err = mock.MagicMock()
        cursor_err.execute.side_effect = DatabaseError("db error")
        cursor_err_cm = mock.MagicMock()
        cursor_err_cm.__enter__.return_value = cursor_err
        with mock.patch.object(self.db_operations.connection, "get_autocommit", return_value=True):
            with mock.patch.object(self.db_operations.connection, "cursor", return_value=cursor_err_cm):
                with self.assertRaises(DatabaseError):
                    self.db_operations.execute_sql_flush(["DELETE FROM T1"])

    def test_execute_sql_flush_max_passes(self):
        cursor = mock.MagicMock()
        # 11 queries: 1 succeeds per pass for 10 passes, pass 11 triggers max_passes
        side_effects = []
        for i in range(10):
            side_effects.append(None) # first statement succeeds
            side_effects.extend([DatabaseError("err")] * (10 - i)) # remaining fail
        cursor.execute.side_effect = side_effects
        cursor_cm = mock.MagicMock()
        cursor_cm.__enter__.return_value = cursor
        queries = ["DELETE FROM T%d" % i for i in range(11)]
        with mock.patch.object(self.db_operations.connection, "get_autocommit", return_value=True):
            with mock.patch.object(self.db_operations.connection, "cursor", return_value=cursor_cm):
                with self.assertRaises(DatabaseError):
                    self.db_operations.execute_sql_flush(queries)

    def test_date_and_datetime_trunc_week(self):
        sql_date, _ = self.db_operations.date_trunc_sql("week", "col", [])
        self.assertIn("DATE_SUB", sql_date)
        self.assertIn("DATE_ADD", sql_date)

        sql_date_day, _ = self.db_operations.date_trunc_sql("day", "col", [])
        self.assertNotIn("DATE_SUB", sql_date_day)

        sql_dt, _ = self.db_operations.datetime_trunc_sql("week", "col", [])
        self.assertIn("TIMESTAMP_SUB", sql_dt)
        self.assertIn("TIMESTAMP_ADD", sql_dt)

        sql_dt_day, _ = self.db_operations.datetime_trunc_sql("day", "col", [])
        self.assertNotIn("TIMESTAMP_SUB", sql_dt_day)

    def test_limit_offset_params_and_savepoints(self):
        self.assertEqual(self.db_operations.integer_field_range("IntegerField"), (-9223372036854775808, 9223372036854775807))
        lim, off = self.db_operations._get_limit_offset_params(5, None)
        self.assertEqual(off, 5)
        self.assertEqual(lim, 9223372036854775807 - 5)

        lim0, off0 = self.db_operations._get_limit_offset_params(0, 10)
        self.assertEqual(off0, 0)
        self.assertEqual(lim0, 10)

        self.assertEqual(self.db_operations.savepoint_create_sql("s1"), "SELECT 1")
        self.assertEqual(self.db_operations.savepoint_commit_sql("s1"), "SELECT 1")
        self.assertEqual(self.db_operations.savepoint_rollback_sql("s1"), "SELECT 1")

    def test_adapt_and_convert_datetime_time_fields(self):
        from django.db.models import F, DateTimeField, TimeField, BinaryField, UUIDField
        from google.api_core.datetime_helpers import DatetimeWithNanoseconds
        import datetime

        # adapt_datetimefield_value with resolve_expression
        expr = F("created")
        self.assertEqual(self.db_operations.adapt_datetimefield_value(expr), expr)
        self.assertIsNone(self.db_operations.adapt_datetimefield_value(None))

        # adapt_timefield_value
        self.assertEqual(self.db_operations.adapt_timefield_value(expr), expr)
        self.assertIsNone(self.db_operations.adapt_timefield_value(None))
        t_val = datetime.time(12, 30, 45)
        res_t = self.db_operations.adapt_timefield_value(t_val)
        self.assertEqual(res_t, "0001-01-01T12:30:45.000000Z")

        # get_db_converters
        for f_cls in [DateTimeField, TimeField, BinaryField, UUIDField]:
            mock_expr = mock.MagicMock()
            mock_expr.output_field.get_internal_type.return_value = f_cls().__class__.__name__
            convs = self.db_operations.get_db_converters(mock_expr)
            self.assertTrue(len(convs) > 0)

        # convert_datetimefield_value & convert_timefield_value
        dtns = DatetimeWithNanoseconds(2020, 1, 1, 12, 0, 0)
        self.assertIsNone(self.db_operations.convert_datetimefield_value(None, None, None))
        with mock.patch("django.conf.settings.USE_TZ", False):
            conv_dt = self.db_operations.convert_datetimefield_value(dtns, None, None)
            self.assertEqual(conv_dt.year, 2020)

        self.assertIsNone(self.db_operations.convert_timefield_value(None, None, None))
        conv_t = self.db_operations.convert_timefield_value(dtns, None, None)
        self.assertEqual(conv_t.hour, 12)

    def test_quote_name_env_and_bulk_batch_size(self):
        with mock.patch.dict(os.environ, {"RUNNING_SPANNER_BACKEND_TESTS": "1"}):
            self.assertEqual(self.db_operations.quote_name("my name"), "my_name")
        self.assertEqual(self.db_operations.bulk_batch_size(["f1", "f2"], []), 900 // 2)

    def test_adapt_datetimefield_value_value_error(self):
        import datetime
        from django.utils import timezone
        dt_aware = timezone.make_aware(datetime.datetime(2020, 1, 1, 12, 0, 0), datetime.timezone.utc)
        with mock.patch("django.conf.settings.USE_TZ", False):
            with self.assertRaises(ValueError):
                self.db_operations.adapt_datetimefield_value(dt_aware)

        # Aware datetime when USE_TZ is True executes line 254 (make_naive)
        self.db_operations.connection.settings_dict["TIME_ZONE"] = "UTC"
        with mock.patch("django.conf.settings.USE_TZ", True):
            res = self.db_operations.adapt_datetimefield_value(dt_aware)
            self.assertIsNotNone(res)

        # Naive datetime takes 252->260 branch directly
        dt_naive = datetime.datetime(2020, 1, 1, 12, 0, 0)
        res_naive = self.db_operations.adapt_datetimefield_value(dt_naive)
        self.assertIsNotNone(res_naive)

    def test_combine_expression_xor(self):
        res = self.db_operations.combine_expression("#", ["a", "b"])
        self.assertIn("^", res)

    def test_quote_name(self):
        quoted_name = self.db_operations.quote_name("abc")
        self.assertEqual(quoted_name, "abc")

    def test_quote_name_spanner_reserved_keyword_escaped(self):
        quoted_name = self.db_operations.quote_name("ALL")
        self.assertEqual(quoted_name, "`ALL`")

    def test_bulk_batch_size(self):
        self.assertEqual(
            self.db_operations.bulk_batch_size(fields=None, objs=None),
            self.db_operations.connection.features.max_query_params,
        )

    def test_sql_flush(self):
        self.assertEqual(
            self.db_operations.sql_flush(style=no_style(), tables=["Table1", "Table2"]),
            ["DELETE FROM Table1 WHERE 1=1", "DELETE FROM Table2 WHERE 1=1"],
        )

    def test_sql_flush_empty_table_list(self):
        self.assertEqual(
            self.db_operations.sql_flush(style=no_style(), tables=[]),
            [],
        )

    def test_adapt_datefield_value(self):
        self.assertIsInstance(
            self.db_operations.adapt_datefield_value("dummy_date"),
            DateStr,
        )

    def test_adapt_datefield_value_none(self):
        self.assertIsNone(
            self.db_operations.adapt_datefield_value(value=None),
        )

    def test_adapt_decimalfield_value(self):
        self.assertIsInstance(
            self.db_operations.adapt_decimalfield_value(value=Decimal("1")),
            Decimal,
        )

    def test_adapt_decimalfield_value_none(self):
        self.assertIsNone(
            self.db_operations.adapt_decimalfield_value(value=None),
        )

    def test_convert_binaryfield_value(self):
        self.assertEqual(
            self.db_operations.convert_binaryfield_value(
                value=b64encode(b"abc"), expression=None, connection=None
            ),
            b"abc",
        )

    def test_convert_binaryfield_value_none(self):
        self.assertIsNone(
            self.db_operations.convert_binaryfield_value(
                value=None, expression=None, connection=None
            ),
        )

    def test_adapt_datetimefield_value_none(self):
        self.assertIsNone(
            self.db_operations.adapt_datetimefield_value(value=None),
        )

    def test_adapt_timefield_value_none(self):
        self.assertIsNone(
            self.db_operations.adapt_timefield_value(value=None),
        )

    def test_convert_uuidfield_value(self):
        uuid_obj = uuid.uuid4()
        self.assertEqual(
            self.db_operations.convert_uuidfield_value(
                str(uuid_obj), expression=None, connection=None
            ),
            uuid_obj,
        )

    def test_convert_uuidfield_value_none(self):
        self.assertIsNone(
            self.db_operations.convert_uuidfield_value(
                value=None, expression=None, connection=None
            ),
        )

    def test_sql_expressions_and_conversions(self):
        ops = self.db_operations
        self.assertEqual(ops.date_extract_sql("week", "f"), ("EXTRACT(isoweek FROM f)", None))
        self.assertEqual(ops.date_extract_sql("dayofweek", "f"), ("EXTRACT(dayofweek FROM f)", None))
        self.assertEqual(ops.time_extract_sql("dayofweek", "f"), ('EXTRACT(dayofweek FROM f AT TIME ZONE "UTC")', None))
        self.assertEqual(ops.time_trunc_sql("dayofweek", "f", None), ('TIMESTAMP_TRUNC(f, dayofweek, "UTC")', None))
        self.assertEqual(ops.datetime_cast_date_sql("f", None, "IST"), ('DATE(f, "IST")', None))
        self.assertEqual(ops.date_interval_sql(timedelta(days=1)), "INTERVAL 86400000000 MICROSECOND")
        self.assertEqual(ops.format_for_duration_arithmetic(1200), "INTERVAL 1200 MICROSECOND")
        self.assertEqual(ops.combine_expression("%%", ["10", "2"]), "MOD(10, 2)")
        self.assertEqual(ops.combine_expression("^", ["10", "2"]), "POWER(10, 2)")
        self.assertEqual(ops.combine_expression(">>", ["10", "2"]), "CAST(FLOOR(10 / POW(2, 2)) AS INT64)")
        self.assertEqual(ops.combine_expression("*", ["10", "2"]), "10 * 2")
        self.assertEqual(ops.combine_duration_expression("+", ["t", "i"]), "TIMESTAMP_ADD(t, i)")
        self.assertEqual(ops.combine_duration_expression("-", ["t", "i"]), "TIMESTAMP_SUB(t, i)")
        self.assertEqual(ops.lookup_cast("contains"), "CAST(%s AS STRING)")
        self.assertEqual(ops.lookup_cast("dummy"), "%s")

        with self.assertRaises(DatabaseError):
            ops.combine_duration_expression("*", ["t", "i"])

        for use_tz in [True, False]:
            settings.USE_TZ = use_tz
            tz = "IST" if use_tz else "UTC"
            self.assertIn(tz, ops.datetime_extract_sql("dayofweek", "f", None, "IST")[0])
            self.assertIn(tz, ops.datetime_cast_time_sql("f", None, "IST")[0])
        settings.USE_TZ = True
