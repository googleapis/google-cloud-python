# Copyright 2021 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

import uuid
from decimal import Decimal

from django.db import models
from django.db.models import F, Subquery, Value
from django.db.models.functions import Concat
from django.test.utils import isolate_apps

from django_spanner.compiler import SQLCompiler
from tests.unit.django_spanner.simple_test import SpannerSimpleTestClass

from .models import Author, Number


class TestLookups(SpannerSimpleTestClass):
    def test_cast_param_to_float_lte_sql_query(self):
        qs1 = Number.objects.filter(decimal_num__lte=Decimal("1.1")).values(
            "decimal_num"
        )
        compiler = SQLCompiler(qs1.query, self.connection, "default")
        sql_compiled, params = compiler.as_sql()
        self.assertEqual(
            sql_compiled,
            "SELECT tests_number.decimal_num AS decimal_num FROM tests_number WHERE "
            + "tests_number.decimal_num <= %s",
        )
        self.assertEqual(params, (Decimal("1.1"),))

    def test_cast_param_to_float_for_int_field_query(self):
        qs1 = Number.objects.filter(num__lte=1.1).values("num")

        compiler = SQLCompiler(qs1.query, self.connection, "default")
        sql_compiled, params = compiler.as_sql()
        self.assertEqual(
            sql_compiled,
            "SELECT tests_number.num AS num FROM tests_number WHERE "
            + "tests_number.num <= %s",
        )
        self.assertEqual(params, (1,))

    def test_cast_param_to_float_for_foreign_key_field_query(self):
        qs1 = Number.objects.filter(item_id__exact="10").values("num")
        compiler = SQLCompiler(qs1.query, self.connection, "default")
        sql_compiled, params = compiler.as_sql()
        self.assertEqual(
            sql_compiled,
            "SELECT tests_number.num AS num FROM tests_number WHERE "
            + "tests_number.item_id = %s",
        )
        self.assertEqual(params, (10,))

    def test_cast_param_to_float_with_no_params_query(self):
        qs1 = Number.objects.filter(item_id__exact=F("num")).values("num")
        compiler = SQLCompiler(qs1.query, self.connection, "default")
        sql_compiled, params = compiler.as_sql()
        expected_sql = (
            "SELECT tests_number.num AS num FROM tests_number WHERE "
            + "tests_number.item_id = (tests_number.num)"
        )
        self.assertEqual(sql_compiled, expected_sql)
        self.assertEqual(params, ())

    def test_startswith_endswith_sql_query_with_startswith(self):
        qs1 = Author.objects.filter(name__startswith="abc").values("num")
        compiler = SQLCompiler(qs1.query, self.connection, "default")
        sql_compiled, params = compiler.as_sql()
        self.assertEqual(
            sql_compiled,
            "SELECT tests_author.num AS num FROM tests_author WHERE "
            "STARTS_WITH(CAST(tests_author.name AS STRING), CAST(%s AS STRING))",
        )
        self.assertEqual(params, ("abc",))

    def test_startswith_endswith_sql_query_with_endswith(self):
        qs1 = Author.objects.filter(name__endswith="abc").values("num")
        compiler = SQLCompiler(qs1.query, self.connection, "default")
        sql_compiled, params = compiler.as_sql()
        self.assertEqual(
            sql_compiled,
            "SELECT tests_author.num AS num FROM tests_author WHERE "
            "ENDS_WITH(CAST(tests_author.name AS STRING), CAST(%s AS STRING))",
        )
        self.assertEqual(params, ("abc",))

    def test_startswith_endswith_sql_query_case_insensitive(self):
        qs1 = Author.objects.filter(name__istartswith="abc").values("num")
        compiler = SQLCompiler(qs1.query, self.connection, "default")
        sql_compiled, params = compiler.as_sql()
        self.assertEqual(
            sql_compiled,
            "SELECT tests_author.num AS num FROM tests_author WHERE "
            "STARTS_WITH(UPPER(CAST(tests_author.name AS STRING)), "
            "UPPER(CAST(%s AS STRING)))",
        )
        self.assertEqual(params, ("abc",))

    def test_startswith_endswith_sql_query_with_bileteral_transform(self):
        qs1 = Author.objects.filter(name__upper__startswith="abc").values("name")

        compiler = SQLCompiler(qs1.query, self.connection, "default")
        sql_compiled, params = compiler.as_sql()
        expected_sql = (
            "SELECT tests_author.name AS name FROM tests_author WHERE "
            "STARTS_WITH(CAST(UPPER(tests_author.name) AS STRING), "
            "CAST((UPPER(%s)) AS STRING))"
        )
        self.assertEqual(sql_compiled, expected_sql)
        self.assertEqual(params, ("abc",))

    def test_startswith_endswith_case_insensitive_transform_sql_query(self):
        qs1 = Author.objects.filter(name__upper__istartswith="abc").values("name")

        compiler = SQLCompiler(qs1.query, self.connection, "default")
        sql_compiled, params = compiler.as_sql()
        expected_sql = (
            "SELECT tests_author.name AS name FROM tests_author WHERE "
            "STARTS_WITH(UPPER(CAST(UPPER(tests_author.name) AS STRING)), "
            "UPPER(CAST((UPPER(%s)) AS STRING)))"
        )
        self.assertEqual(sql_compiled, expected_sql)
        self.assertEqual(params, ("abc",))

    def test_startswith_endswith_endswith_sql_query_with_transform(self):
        qs1 = Author.objects.filter(name__upper__endswith="abc").values("name")

        compiler = SQLCompiler(qs1.query, self.connection, "default")
        sql_compiled, params = compiler.as_sql()

        expected_sql = (
            "SELECT tests_author.name AS name FROM tests_author WHERE "
            "ENDS_WITH(CAST(UPPER(tests_author.name) AS STRING), "
            "CAST((UPPER(%s)) AS STRING))"
        )
        self.assertEqual(sql_compiled, expected_sql)
        self.assertEqual(params, ("abc",))

    def test_regex_sql_query_case_sensitive(self):
        qs1 = Author.objects.filter(name__regex="abc").values("num")
        compiler = SQLCompiler(qs1.query, self.connection, "default")
        sql_compiled, params = compiler.as_sql()
        self.assertEqual(
            sql_compiled,
            "SELECT tests_author.num AS num FROM tests_author WHERE "
            "REGEXP_CONTAINS(CAST(tests_author.name AS STRING), %s)",
        )
        self.assertEqual(params, ("abc",))

    def test_regex_sql_query_case_insensitive(self):
        qs1 = Author.objects.filter(name__iregex="abc").values("num")
        compiler = SQLCompiler(qs1.query, self.connection, "default")
        sql_compiled, params = compiler.as_sql()
        self.assertEqual(
            sql_compiled,
            "SELECT tests_author.num AS num FROM tests_author WHERE "
            "REGEXP_CONTAINS(CAST(tests_author.name AS STRING), %s)",
        )
        self.assertEqual(params, ("(?i)abc",))

    def test_regex_sql_query_case_sensitive_with_transform(self):
        qs1 = Author.objects.filter(name__upper__regex="abc").values("num")
        compiler = SQLCompiler(qs1.query, self.connection, "default")
        sql_compiled, params = compiler.as_sql()

        expected_sql = (
            "SELECT tests_author.num AS num FROM tests_author WHERE "
            + "REGEXP_CONTAINS(CAST(UPPER(tests_author.name) AS STRING), "
            + "(UPPER(%s)))"
        )
        self.assertEqual(sql_compiled, expected_sql)
        self.assertEqual(params, ("abc",))

    def test_regex_sql_query_case_insensitive_with_transform(self):
        qs1 = Author.objects.filter(name__upper__iregex="abc").values("num")
        compiler = SQLCompiler(qs1.query, self.connection, "default")
        sql_compiled, params = compiler.as_sql()

        expected_sql = (
            "SELECT tests_author.num AS num FROM tests_author WHERE "
            + "REGEXP_CONTAINS(CAST(UPPER(tests_author.name) AS STRING), "
            + "CONCAT('(?i)', (UPPER(%s))))"
        )
        self.assertEqual(sql_compiled, expected_sql)
        self.assertEqual(params, ("abc",))

    def test_contains_sql_query_case_insensitive(self):
        qs1 = Author.objects.filter(name__icontains="abc").values("num")
        compiler = SQLCompiler(qs1.query, self.connection, "default")
        sql_compiled, params = compiler.as_sql()
        self.assertEqual(
            sql_compiled,
            "SELECT tests_author.num AS num FROM tests_author WHERE "
            "STRPOS(UPPER(CAST(tests_author.name AS STRING)), "
            "UPPER(CAST(%s AS STRING))) > 0",
        )
        self.assertEqual(params, ("abc",))

    def test_contains_sql_query_case_sensitive(self):
        qs1 = Author.objects.filter(name__contains="abc").values("num")
        compiler = SQLCompiler(qs1.query, self.connection, "default")
        sql_compiled, params = compiler.as_sql()
        self.assertEqual(
            sql_compiled,
            "SELECT tests_author.num AS num FROM tests_author WHERE "
            "STRPOS(CAST(tests_author.name AS STRING), CAST(%s AS STRING)) > 0",
        )
        self.assertEqual(params, ("abc",))

    def test_contains_sql_query_case_insensitive_transform(self):
        qs1 = Author.objects.filter(name__upper__icontains="abc").values("name")
        compiler = SQLCompiler(qs1.query, self.connection, "default")
        sql_compiled, params = compiler.as_sql()
        expected_sql = (
            "SELECT tests_author.name AS name FROM tests_author WHERE "
            "STRPOS(UPPER(CAST(UPPER(tests_author.name) AS STRING)), "
            "UPPER(CAST((UPPER(%s)) AS STRING))) > 0"
        )
        self.assertEqual(sql_compiled, expected_sql)
        self.assertEqual(params, ("abc",))

    def test_contains_sql_query_case_sensitive_transform(self):
        qs1 = Author.objects.filter(name__upper__contains="abc").values("name")
        compiler = SQLCompiler(qs1.query, self.connection, "default")
        sql_compiled, params = compiler.as_sql()
        expected_sql = (
            "SELECT tests_author.name AS name FROM tests_author WHERE "
            "STRPOS(CAST(UPPER(tests_author.name) AS STRING), "
            "CAST((UPPER(%s)) AS STRING)) > 0"
        )
        self.assertEqual(sql_compiled, expected_sql)
        self.assertEqual(params, ("abc",))

    def test_iexact_sql_query_case_insensitive(self):
        qs1 = Author.objects.filter(name__iexact="abc").values("num")
        compiler = SQLCompiler(qs1.query, self.connection, "default")
        sql_compiled, params = compiler.as_sql()

        self.assertEqual(
            sql_compiled,
            "SELECT tests_author.num AS num FROM tests_author WHERE "
            "UPPER(CAST(tests_author.name AS STRING)) = UPPER(CAST(%s AS STRING))",
        )
        self.assertEqual(params, ("abc",))

    def test_iexact_sql_query_case_insensitive_function_transform(self):
        qs1 = Author.objects.filter(name__upper__iexact=F("last_name")).values("name")
        compiler = SQLCompiler(qs1.query, self.connection, "default")
        sql_compiled, params = compiler.as_sql()

        expected_sql = (
            "SELECT tests_author.name AS name FROM tests_author WHERE "
            "UPPER(CAST(UPPER(tests_author.name) AS STRING)) = "
            "UPPER(CAST((UPPER(tests_author.last_name)) AS STRING))"
        )
        self.assertEqual(sql_compiled, expected_sql)
        self.assertEqual(params, ())

    def test_iexact_sql_query_case_insensitive_value_match(self):
        qs1 = Author.objects.filter(name__upper__iexact="abc").values("name")
        compiler = SQLCompiler(qs1.query, self.connection, "default")
        sql_compiled, params = compiler.as_sql()

        expected_sql = (
            "SELECT tests_author.name AS name FROM tests_author WHERE "
            "UPPER(CAST(UPPER(tests_author.name) AS STRING)) = "
            "UPPER(CAST((UPPER(%s)) AS STRING))"
        )
        self.assertEqual(sql_compiled, expected_sql)
        self.assertEqual(params, ("abc",))

    def test_icontains_with_lhs_params(self):
        qs = (
            Author.objects.annotate(greeting=Concat(Value("User: "), "name"))
            .filter(greeting__icontains="john")
            .values("name")
        )
        compiler = SQLCompiler(qs.query, self.connection, "default")
        sql, params = compiler.as_sql()
        self.assertIn("STRPOS(", sql)
        self.assertEqual(params, ("User: ", "", "", "john"))

    def test_iexact_with_lhs_params(self):
        qs = (
            Author.objects.annotate(greeting=Concat(Value("User: "), "name"))
            .filter(greeting__iexact="john")
            .values("name")
        )
        compiler = SQLCompiler(qs.query, self.connection, "default")
        sql, params = compiler.as_sql()
        self.assertIn(" = UPPER(", sql)
        self.assertEqual(params, ("User: ", "", "", "john"))

    def test_istartswith_with_lhs_params(self):
        qs = (
            Author.objects.annotate(greeting=Concat(Value("User: "), "name"))
            .filter(greeting__istartswith="john")
            .values("name")
        )
        compiler = SQLCompiler(qs.query, self.connection, "default")
        sql, params = compiler.as_sql()
        self.assertIn("STARTS_WITH(", sql)
        self.assertEqual(params, ("User: ", "", "", "john"))

    def test_iendswith_with_lhs_params(self):
        qs = (
            Author.objects.annotate(greeting=Concat(Value("User: "), "name"))
            .filter(greeting__iendswith="john")
            .values("name")
        )
        compiler = SQLCompiler(qs.query, self.connection, "default")
        sql, params = compiler.as_sql()
        self.assertIn("ENDS_WITH(", sql)
        self.assertEqual(params, ("User: ", "", "", "john"))

    def test_iregex_with_lhs_params(self):
        qs = (
            Author.objects.annotate(greeting=Concat(Value("User: "), "name"))
            .filter(greeting__iregex="^john")
            .values("name")
        )
        compiler = SQLCompiler(qs.query, self.connection, "default")
        sql, params = compiler.as_sql()
        self.assertEqual(params, ("User: ", "", "", "(?i)^john"))

    def _assert_where_clauses(self, cases, table="tests_author", column="num"):
        for queryset, expected_where, expected_params in cases:
            with self.subTest(expected_where=expected_where, params=expected_params):
                compiler = SQLCompiler(
                    queryset.values(column).query, self.connection, "default"
                )
                sql_compiled, params = compiler.as_sql()
                self.assertEqual(
                    sql_compiled,
                    f"SELECT {table}.{column} AS {column} FROM {table} "
                    f"WHERE {expected_where}",
                )
                self.assertEqual(params, expected_params)

    def test_pattern_lookups_with_expression_rhs_and_metacharacters(self):
        metacharacters = r".*+?()[]{}\|^$%_"
        self._assert_where_clauses(
            [
                (
                    Author.objects.filter(name__contains=Value(metacharacters)),
                    "STRPOS(CAST(tests_author.name AS STRING), CAST(%s AS STRING)) > 0",
                    (metacharacters,),
                ),
                (
                    Author.objects.filter(name__icontains=Value(metacharacters)),
                    "STRPOS(UPPER(CAST(tests_author.name AS STRING)), "
                    "UPPER(CAST(%s AS STRING))) > 0",
                    (metacharacters,),
                ),
                (
                    Author.objects.filter(name__startswith=Value(metacharacters)),
                    "STARTS_WITH(CAST(tests_author.name AS STRING), "
                    "CAST(%s AS STRING))",
                    (metacharacters,),
                ),
                (
                    Author.objects.filter(name__istartswith=Value(metacharacters)),
                    "STARTS_WITH(UPPER(CAST(tests_author.name AS STRING)), "
                    "UPPER(CAST(%s AS STRING)))",
                    (metacharacters,),
                ),
                (
                    Author.objects.filter(name__endswith=Value(metacharacters)),
                    "ENDS_WITH(CAST(tests_author.name AS STRING), CAST(%s AS STRING))",
                    (metacharacters,),
                ),
                (
                    Author.objects.filter(name__iendswith=Value(metacharacters)),
                    "ENDS_WITH(UPPER(CAST(tests_author.name AS STRING)), "
                    "UPPER(CAST(%s AS STRING)))",
                    (metacharacters,),
                ),
                (
                    Author.objects.filter(name__contains=F("last_name")),
                    "STRPOS(CAST(tests_author.name AS STRING), "
                    "CAST((tests_author.last_name) AS STRING)) > 0",
                    (),
                ),
                (
                    Author.objects.filter(name__startswith=F("num")),
                    "STARTS_WITH(CAST(tests_author.name AS STRING), "
                    "CAST((tests_author.num) AS STRING))",
                    (),
                ),
                (
                    Author.objects.filter(name__upper__contains=metacharacters),
                    "STRPOS(CAST(UPPER(tests_author.name) AS STRING), "
                    "CAST((UPPER(%s)) AS STRING)) > 0",
                    (metacharacters,),
                ),
                (
                    Author.objects.filter(name__upper__iendswith=metacharacters),
                    "ENDS_WITH(UPPER(CAST(UPPER(tests_author.name) AS STRING)), "
                    "UPPER(CAST((UPPER(%s)) AS STRING)))",
                    (metacharacters,),
                ),
                (
                    Author.objects.filter(name__contains=""),
                    "STRPOS(CAST(tests_author.name AS STRING), CAST(%s AS STRING)) > 0",
                    ("",),
                ),
                (
                    Author.objects.filter(name__startswith="%"),
                    "STARTS_WITH(CAST(tests_author.name AS STRING), "
                    "CAST(%s AS STRING))",
                    ("%",),
                ),
                (
                    Author.objects.filter(name__endswith="%"),
                    "ENDS_WITH(CAST(tests_author.name AS STRING), CAST(%s AS STRING))",
                    ("%",),
                ),
                (
                    Author.objects.filter(name__contains=Value(None)),
                    "STRPOS(CAST(tests_author.name AS STRING), "
                    "CAST(NULL AS STRING)) > 0",
                    (),
                ),
                (
                    Author.objects.filter(name__contains=4),
                    "STRPOS(CAST(tests_author.name AS STRING), CAST(%s AS STRING)) > 0",
                    ("4",),
                ),
            ]
        )

    def test_iexact_with_expression_rhs_and_metacharacters(self):
        metacharacters = r".*+?()[]{}\|^$%_"
        self._assert_where_clauses(
            [
                (
                    Author.objects.filter(name__iexact=metacharacters),
                    "UPPER(CAST(tests_author.name AS STRING)) = "
                    "UPPER(CAST(%s AS STRING))",
                    (metacharacters,),
                ),
                (
                    Author.objects.filter(name__iexact=Value(metacharacters)),
                    "UPPER(CAST(tests_author.name AS STRING)) = "
                    "UPPER(CAST(%s AS STRING))",
                    (metacharacters,),
                ),
                (
                    Author.objects.filter(name__iexact=F("last_name")),
                    "UPPER(CAST(tests_author.name AS STRING)) = "
                    "UPPER(CAST((tests_author.last_name) AS STRING))",
                    (),
                ),
                (
                    Author.objects.filter(name__upper__iexact=metacharacters),
                    "UPPER(CAST(UPPER(tests_author.name) AS STRING)) = "
                    "UPPER(CAST((UPPER(%s)) AS STRING))",
                    (metacharacters,),
                ),
                (
                    Author.objects.filter(name__iexact=Value(None)),
                    "UPPER(CAST(tests_author.name AS STRING)) = "
                    "UPPER(CAST(NULL AS STRING))",
                    (),
                ),
                (
                    Author.objects.filter(name__iexact=4),
                    "UPPER(CAST(tests_author.name AS STRING)) = "
                    "UPPER(CAST(%s AS STRING))",
                    ("4",),
                ),
                (
                    Author.objects.filter(name__iexact=1.5),
                    "UPPER(CAST(tests_author.name AS STRING)) = "
                    "UPPER(CAST(%s AS STRING))",
                    ("1.5",),
                ),
                (
                    Author.objects.filter(name__iexact=Decimal("1.50")),
                    "UPPER(CAST(tests_author.name AS STRING)) = "
                    "UPPER(CAST(%s AS STRING))",
                    ("1.50",),
                ),
                (
                    Author.objects.filter(name__iexact=Value(1.5)),
                    "UPPER(CAST(tests_author.name AS STRING)) = "
                    "UPPER(CAST(CAST(%s AS FLOAT64) AS STRING))",
                    (1.5,),
                ),
                (
                    Author.objects.filter(
                        name__iexact=Subquery(
                            Author.objects.filter(last_name=".*").values("last_name")[
                                :1
                            ]
                        )
                    ),
                    "UPPER(CAST(tests_author.name AS STRING)) = "
                    "UPPER(CAST((SELECT U0.last_name AS last_name "
                    "FROM tests_author U0 WHERE U0.last_name = %s LIMIT 1) AS STRING))",
                    (".*",),
                ),
            ]
        )

    @isolate_apps("tests")
    def test_uuid_field_pattern_and_iexact_lookups(self):
        class UuidLookupModel(models.Model):
            token = models.UUIDField()

            class Meta:
                app_label = "tests"

        uuid_string = "12345678-1234-5678-1234-567812345678"
        uuid_value = uuid.UUID(uuid_string)
        self._assert_where_clauses(
            [
                (
                    UuidLookupModel.objects.filter(token__iexact=uuid_value),
                    "UPPER(CAST(tests_uuidlookupmodel.token AS STRING)) = "
                    "UPPER(CAST((REPLACE(%s, %s, %s)) AS STRING))",
                    ("12345678123456781234567812345678", "-", ""),
                ),
                (
                    UuidLookupModel.objects.filter(token__iexact=uuid_string),
                    "UPPER(CAST(tests_uuidlookupmodel.token AS STRING)) = "
                    "UPPER(CAST((REPLACE(%s, %s, %s)) AS STRING))",
                    (uuid_string, "-", ""),
                ),
                (
                    UuidLookupModel.objects.filter(token__iexact=Value(None)),
                    "UPPER(CAST(tests_uuidlookupmodel.token AS STRING)) = "
                    "UPPER(CAST((REPLACE(NULL, %s, %s)) AS STRING))",
                    ("-", ""),
                ),
                (
                    UuidLookupModel.objects.filter(token__contains=".*"),
                    "STRPOS(CAST(tests_uuidlookupmodel.token AS STRING), "
                    "CAST((REPLACE(%s, %s, %s)) AS STRING)) > 0",
                    (".*", "-", ""),
                ),
                (
                    UuidLookupModel.objects.filter(token__istartswith="1234-56"),
                    "STARTS_WITH(UPPER(CAST(tests_uuidlookupmodel.token AS STRING)), "
                    "UPPER(CAST((REPLACE(%s, %s, %s)) AS STRING)))",
                    ("1234-56", "-", ""),
                ),
            ],
            table="tests_uuidlookupmodel",
            column="token",
        )

    @isolate_apps("tests")
    def test_json_key_transform_pattern_and_iexact_lookups(self):
        class JsonLookupModel(models.Model):
            data = models.JSONField()

            class Meta:
                app_label = "tests"

        self._assert_where_clauses(
            [
                (
                    JsonLookupModel.objects.filter(data__foo__iexact="Bar.*"),
                    "UPPER(CAST(JSON_VALUE(tests_jsonlookupmodel.data, '$.\"foo\"') AS STRING)) = "
                    "UPPER(CAST(%s AS STRING))",
                    ("Bar.*",),
                ),
                (
                    JsonLookupModel.objects.filter(data__foo__icontains="Bar.*"),
                    "STRPOS(UPPER(CAST(JSON_VALUE(tests_jsonlookupmodel.data, '$.\"foo\"') AS STRING)), "
                    "UPPER(CAST(%s AS STRING))) > 0",
                    ("Bar.*",),
                ),
                (
                    JsonLookupModel.objects.filter(data__foo__startswith="Bar.*"),
                    "STARTS_WITH(CAST(JSON_VALUE(tests_jsonlookupmodel.data, '$.\"foo\"') AS STRING), "
                    "CAST(%s AS STRING))",
                    ("Bar.*",),
                ),
                (
                    JsonLookupModel.objects.filter(data__foo__endswith="Bar.*"),
                    "ENDS_WITH(CAST(JSON_VALUE(tests_jsonlookupmodel.data, '$.\"foo\"') AS STRING), "
                    "CAST(%s AS STRING))",
                    ("Bar.*",),
                ),
            ],
            table="tests_jsonlookupmodel",
            column="data",
        )

    def test_json_key_transforms_and_has_key(self):
        from unittest.mock import MagicMock

        from django.db.models import JSONField
        from django.db.models.expressions import Col
        from django.db.models.fields.json import (
            HasKey,
            KeyTextTransform,
            KeyTransform,
        )

        field = JSONField()
        field.set_attributes_from_name("value")
        col = Col("tests_detail", field)
        compiler = MagicMock()
        compiler.compile.return_value = ("tests_detail.value", [])

        kt = KeyTransform("name", col)
        sql, params = kt.as_spanner(compiler, self.connection)
        self.assertEqual(
            sql,
            "JSON_QUERY(tests_detail.value, '$.\"name\"')",
        )
        self.assertEqual(params, ())

        ktt = KeyTextTransform("name", col)
        sql, params = ktt.as_spanner(compiler, self.connection)
        self.assertEqual(
            sql,
            "JSON_VALUE(tests_detail.value, '$.\"name\"')",
        )
        self.assertEqual(params, ())

        kt_nested = KeyTransform("b", KeyTransform("0", KeyTransform("a", col)))
        sql, params = kt_nested.as_spanner(compiler, self.connection)
        self.assertEqual(
            sql,
            'JSON_QUERY(tests_detail.value, \'$."a"[0]."b"\')',
        )
        self.assertEqual(params, ())

        kt_escaped = KeyTransform("a'b%s", col)
        sql, params = kt_escaped.as_spanner(compiler, self.connection)
        self.assertEqual(
            sql,
            "JSON_QUERY(tests_detail.value, '$.\"a\\'b%%s\"')",
        )
        self.assertEqual(params, ())

        hk = HasKey(col, "name")
        sql, params = hk.as_spanner(compiler, self.connection)
        self.assertEqual(
            sql,
            "JSON_QUERY(tests_detail.value, '$.\"name\"') IS NOT NULL",
        )
        self.assertEqual(params, ())

        hk_nested_int = HasKey(KeyTransform("nested", col), "0")
        sql, params = hk_nested_int.as_spanner(compiler, self.connection)
        self.assertEqual(
            sql,
            'JSON_QUERY(tests_detail.value, \'$."nested"."0"\') IS NOT NULL',
        )
        self.assertEqual(params, ())

    def test_json_field_get_prep_value(self):
        from django.db.models import JSONField

        field = JSONField()
        val = {"key": "value"}
        res = field.get_prep_value(val)
        self.assertEqual(res, val)
