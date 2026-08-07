# Copyright 2021 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

from unittest import mock
from django.core.exceptions import EmptyResultSet
from django.db.models.query import QuerySet
from django.db.utils import DatabaseError

from django_spanner.compiler import SQLCompiler
from tests.unit.django_spanner.simple_test import SpannerSimpleTestClass

from .models import Number


class TestCompiler(SpannerSimpleTestClass):
    def test_unsupported_ordering_slicing_raises_db_error(self):
        """
        Tries limit/offset and order by in subqueries which are not supported
        by spanner.
        """
        qs1 = Number.objects.all()
        qs2 = Number.objects.all()
        msg = "LIMIT/OFFSET not allowed in subqueries of compound statements"
        with self.assertRaisesRegex(DatabaseError, msg):
            list(qs1.union(qs2[:10]))
        msg = "ORDER BY not allowed in subqueries of compound statements"
        with self.assertRaisesRegex(DatabaseError, msg):
            list(qs1.order_by("id").union(qs2))

    def test_get_combinator_sql_all_union_sql_generated(self):
        """
        Tries union sql generator.
        """

        qs1 = Number.objects.filter(num__lte=1).values("num")
        qs2 = Number.objects.filter(num__gte=8).values("num")
        qs4 = qs1.union(qs2)

        compiler = SQLCompiler(qs4.query, self.connection, "default")
        sql_compiled, params = compiler.get_combinator_sql("union", True)
        self.assertEqual(
            sql_compiled,
            [
                "SELECT tests_number.num AS num FROM tests_number WHERE "
                + "tests_number.num <= %s UNION ALL SELECT tests_number.num "
                + "AS num FROM tests_number WHERE tests_number.num >= %s"
            ],
        )
        self.assertEqual(params, [1, 8])

    def test_get_combinator_sql_distinct_union_sql_generated(self):
        """
        Tries union sql generator with distinct.
        """

        qs1 = Number.objects.filter(num__lte=1).values("num")
        qs2 = Number.objects.filter(num__gte=8).values("num")
        qs4 = qs1.union(qs2)

        compiler = SQLCompiler(qs4.query, self.connection, "default")
        sql_compiled, params = compiler.get_combinator_sql("union", False)
        self.assertEqual(
            sql_compiled,
            [
                "SELECT tests_number.num AS num FROM tests_number WHERE "
                + "tests_number.num <= %s UNION DISTINCT SELECT "
                + "tests_number.num AS num FROM tests_number WHERE "
                + "tests_number.num >= %s"
            ],
        )
        self.assertEqual(params, [1, 8])

    def test_get_combinator_sql_difference_all_sql_generated(self):
        """
        Tries difference sql generator.
        """
        qs1 = Number.objects.filter(num__lte=1).values("num")
        qs2 = Number.objects.filter(num__gte=8).values("num")
        qs4 = qs1.difference(qs2)

        compiler = SQLCompiler(qs4.query, self.connection, "default")
        sql_compiled, params = compiler.get_combinator_sql("difference", True)

        self.assertEqual(
            sql_compiled,
            [
                "SELECT tests_number.num AS num FROM tests_number WHERE "
                + "tests_number.num <= %s EXCEPT ALL SELECT tests_number.num "
                + "AS num FROM tests_number WHERE tests_number.num >= %s"
            ],
        )
        self.assertEqual(params, [1, 8])

    def test_get_combinator_sql_difference_distinct_sql_generated(self):
        """
        Tries difference sql generator with distinct.
        """
        qs1 = Number.objects.filter(num__lte=1).values("num")
        qs2 = Number.objects.filter(num__gte=8).values("num")
        qs4 = qs1.difference(qs2)

        compiler = SQLCompiler(qs4.query, self.connection, "default")
        sql_compiled, params = compiler.get_combinator_sql("difference", False)

        self.assertEqual(
            sql_compiled,
            [
                "SELECT tests_number.num AS num FROM tests_number WHERE "
                + "tests_number.num <= %s EXCEPT DISTINCT SELECT "
                + "tests_number.num AS num FROM tests_number WHERE "
                + "tests_number.num >= %s"
            ],
        )
        self.assertEqual(params, [1, 8])

    def test_get_combinator_sql_union_and_difference_query_together(self):
        """
        Tries sql generator with union of queryset with queryset of difference.
        """
        qs1 = Number.objects.filter(num__lte=1).values("num")
        qs2 = Number.objects.filter(num__gte=8).values("num")
        qs3 = Number.objects.filter(num__exact=10).values("num")
        qs4 = qs1.union(qs2.difference(qs3))

        compiler = SQLCompiler(qs4.query, self.connection, "default")
        sql_compiled, params = compiler.get_combinator_sql("union", False)
        self.assertEqual(
            sql_compiled,
            [
                "(SELECT tests_number.num AS num FROM tests_number WHERE "
                + "tests_number.num <= %s) UNION DISTINCT (SELECT * FROM ("
                + "SELECT tests_number.num AS num FROM tests_number WHERE "
                + "tests_number.num >= %s EXCEPT DISTINCT "
                + "SELECT tests_number.num AS num FROM tests_number "
                + "WHERE tests_number.num = %s))"
            ],
        )
        self.assertEqual(params, [1, 8, 10])

    def test_get_combinator_sql_parentheses_in_compound_not_supported(self):
        """
        Tries sql generator with union of queryset with queryset of difference,
        adding support for parentheses in compound sql statement.
        """

        qs1 = Number.objects.filter(num__lte=1).values("num")
        qs2 = Number.objects.filter(num__gte=8).values("num")
        qs3 = Number.objects.filter(num__exact=10).values("num")
        qs4 = qs1.union(qs2.difference(qs3))

        compiler = SQLCompiler(qs4.query, self.connection, "default")
        compiler.connection.features.supports_parentheses_in_compound = False
        sql_compiled, params = compiler.get_combinator_sql("union", False)
        self.assertEqual(
            sql_compiled,
            [
                "SELECT tests_number.num AS num FROM tests_number WHERE "
                + "tests_number.num <= %s UNION DISTINCT SELECT * FROM ("
                + "SELECT tests_number.num AS num FROM tests_number WHERE "
                + "tests_number.num >= %s EXCEPT DISTINCT "
                + "SELECT tests_number.num AS num FROM tests_number "
                + "WHERE tests_number.num = %s)"
            ],
        )
        self.assertEqual(params, [1, 8, 10])

    def test_get_combinator_sql_empty_queryset_raises_exception(self):
        """
        Tries sql generator with empty queryset.
        """
        compiler = SQLCompiler(QuerySet().query, self.connection, "default")
        with self.assertRaises(EmptyResultSet):
            compiler.get_combinator_sql("union", False)

    def test_get_combinator_sql_sliced_and_features(self):
        qs1 = Number.objects.filter(num__lte=1)
        qs2 = Number.objects.none()  # Empty result set
        qs3 = Number.objects.filter(num__gte=8)
        qs4 = qs1.union(qs3)

        compiler = SQLCompiler(qs4.query, self.connection, "default")
        compiler.connection.features.supports_slicing_ordering_in_compound = True
        compiler.query.high_mark = 10
        sql, params = compiler.get_combinator_sql("union", False)
        self.assertTrue(len(sql) > 0)

        # Test values_select set_values
        qs_val = Number.objects.values("num")
        qs_comb = qs_val.union(Number.objects.all())
        comp_val = SQLCompiler(qs_comb.query, self.connection, "default")
        sql2, params2 = comp_val.get_combinator_sql("union", True)
        self.assertTrue(len(sql2) > 0)

    def test_get_combinator_sql_edge_cases(self):
        qs1, qs_empty = Number.objects.filter(num=1), Number.objects.none()

        # Test valid combinators (union, difference, subquery)
        for comp in [
            SQLCompiler(qs1.union(qs_empty).query, self.connection, "default"),
            SQLCompiler(qs1.difference(qs_empty).query, self.connection, "default"),
        ]:
            comp.query.subquery = True
            self.assertTrue(len(comp.get_combinator_sql("union", False)[0]) > 0)

        # Test EmptyResultSet exceptions (intersection on empty, union on empty parts)
        qs_none1, qs_none2 = Number.objects.none(), Number.objects.none()
        for comp in [
            SQLCompiler(qs_empty.intersection(qs1).query, self.connection, "default"),
            SQLCompiler(qs_none1.union(qs_none2).query, self.connection, "default"),
        ]:
            with self.assertRaises(EmptyResultSet):
                comp.get_combinator_sql("union", False)

        # supports_parentheses_in_compound False with subquery combinator
        comp_sub = SQLCompiler(qs1.union(Number.objects.filter(num=2)).query, self.connection, "default")
        mock_sub = mock.MagicMock(as_sql=mock.MagicMock(return_value=("SELECT 1", [])))
        mock_sub.query.combinator = "union"
        mock_sub.query.is_sliced = False
        mock_sub.get_order_by.return_value = []
        with mock.patch.object(self.connection.features, "supports_parentheses_in_compound", False):
            with mock.patch.object(comp_sub.query.combined_queries[0], "get_compiler", return_value=mock_sub):
                with mock.patch.object(comp_sub.query.combined_queries[1], "get_compiler", return_value=mock_sub):
                    self.assertIn("SELECT * FROM", comp_sub.get_combinator_sql("union", False)[0][0])
