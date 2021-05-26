# Copyright 2021 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

from base64 import b64encode
from datetime import timedelta
from decimal import Decimal
from django.conf import settings
from django.core.management.color import no_style
from django.db.utils import DatabaseError
from google.cloud.spanner_dbapi.types import DateStr
from tests.unit.django_spanner.simple_test import SpannerSimpleTestClass
import uuid


class TestOperations(SpannerSimpleTestClass):
    def test_max_name_length(self):
        self.assertEqual(self.db_operations.max_name_length(), 128)

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
            self.db_operations.sql_flush(
                style=no_style(), tables=["Table1", "Table2"]
            ),
            ["DELETE FROM Table1", "DELETE FROM Table2"],
        )

    def test_sql_flush_empty_table_list(self):
        self.assertEqual(
            self.db_operations.sql_flush(style=no_style(), tables=[]), [],
        )

    def test_adapt_datefield_value(self):
        self.assertIsInstance(
            self.db_operations.adapt_datefield_value("dummy_date"), DateStr,
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

    def test_date_extract_sql(self):
        self.assertEqual(
            self.db_operations.date_extract_sql("week", "dummy_field"),
            "EXTRACT(isoweek FROM dummy_field)",
        )

    def test_date_extract_sql_lookup_type_dayofweek(self):
        self.assertEqual(
            self.db_operations.date_extract_sql("dayofweek", "dummy_field"),
            "EXTRACT(dayofweek FROM dummy_field)",
        )

    def test_datetime_extract_sql(self):
        settings.USE_TZ = True
        self.assertEqual(
            self.db_operations.datetime_extract_sql(
                "dayofweek", "dummy_field", "IST"
            ),
            'EXTRACT(dayofweek FROM dummy_field AT TIME ZONE "IST")',
        )

    def test_datetime_extract_sql_use_tz_false(self):
        settings.USE_TZ = False
        self.assertEqual(
            self.db_operations.datetime_extract_sql(
                "dayofweek", "dummy_field", "IST"
            ),
            'EXTRACT(dayofweek FROM dummy_field AT TIME ZONE "UTC")',
        )
        settings.USE_TZ = True  # reset changes.

    def test_time_extract_sql(self):
        self.assertEqual(
            self.db_operations.time_extract_sql("dayofweek", "dummy_field"),
            'EXTRACT(dayofweek FROM dummy_field AT TIME ZONE "UTC")',
        )

    def test_time_trunc_sql(self):
        self.assertEqual(
            self.db_operations.time_trunc_sql("dayofweek", "dummy_field"),
            'TIMESTAMP_TRUNC(dummy_field, dayofweek, "UTC")',
        )

    def test_datetime_cast_date_sql(self):
        self.assertEqual(
            self.db_operations.datetime_cast_date_sql("dummy_field", "IST"),
            'DATE(dummy_field, "IST")',
        )

    def test_datetime_cast_time_sql(self):
        settings.USE_TZ = True
        self.assertEqual(
            self.db_operations.datetime_cast_time_sql("dummy_field", "IST"),
            "TIMESTAMP(FORMAT_TIMESTAMP('%Y-%m-%d %R:%E9S %Z', dummy_field, 'IST'))",
        )

    def test_datetime_cast_time_sql_use_tz_false(self):
        settings.USE_TZ = False
        self.assertEqual(
            self.db_operations.datetime_cast_time_sql("dummy_field", "IST"),
            "TIMESTAMP(FORMAT_TIMESTAMP('%Y-%m-%d %R:%E9S %Z', dummy_field, 'UTC'))",
        )
        settings.USE_TZ = True  # reset changes.

    def test_date_interval_sql(self):
        self.assertEqual(
            self.db_operations.date_interval_sql(timedelta(days=1)),
            "INTERVAL 86400000000 MICROSECOND",
        )

    def test_format_for_duration_arithmetic(self):
        self.assertEqual(
            self.db_operations.format_for_duration_arithmetic(1200),
            "INTERVAL 1200 MICROSECOND",
        )

    def test_combine_expression_mod(self):
        self.assertEqual(
            self.db_operations.combine_expression("%%", ["10", "2"]),
            "MOD(10, 2)",
        )

    def test_combine_expression_power(self):
        self.assertEqual(
            self.db_operations.combine_expression("^", ["10", "2"]),
            "POWER(10, 2)",
        )

    def test_combine_expression_bit_extention(self):
        self.assertEqual(
            self.db_operations.combine_expression(">>", ["10", "2"]),
            "CAST(FLOOR(10 / POW(2, 2)) AS INT64)",
        )

    def test_combine_expression_multiply(self):
        self.assertEqual(
            self.db_operations.combine_expression("*", ["10", "2"]), "10 * 2",
        )

    def test_combine_duration_expression_add(self):
        self.assertEqual(
            self.db_operations.combine_duration_expression(
                "+",
                ['TIMESTAMP "2008-12-25 15:30:00+00', "INTERVAL 10 MINUTE"],
            ),
            'TIMESTAMP_ADD(TIMESTAMP "2008-12-25 15:30:00+00, INTERVAL 10 MINUTE)',
        )

    def test_combine_duration_expression_subtract(self):
        self.assertEqual(
            self.db_operations.combine_duration_expression(
                "-",
                ['TIMESTAMP "2008-12-25 15:30:00+00', "INTERVAL 10 MINUTE"],
            ),
            'TIMESTAMP_SUB(TIMESTAMP "2008-12-25 15:30:00+00, INTERVAL 10 MINUTE)',
        )

    def test_combine_duration_expression_database_error(self):
        msg = "Invalid connector for timedelta:"
        with self.assertRaisesRegex(DatabaseError, msg):
            self.db_operations.combine_duration_expression(
                "*",
                ['TIMESTAMP "2008-12-25 15:30:00+00', "INTERVAL 10 MINUTE"],
            )

    def test_lookup_cast_match_lookup_type(self):
        self.assertEqual(
            self.db_operations.lookup_cast("contains",), "CAST(%s AS STRING)",
        )

    def test_lookup_cast_unmatched_lookup_type(self):
        self.assertEqual(
            self.db_operations.lookup_cast("dummy",), "%s",
        )
