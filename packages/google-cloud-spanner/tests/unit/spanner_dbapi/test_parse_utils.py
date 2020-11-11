# Copyright 2020 Google LLC All rights reserved.
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

import sys
import unittest

from google.cloud.spanner_v1 import param_types


class TestParseUtils(unittest.TestCase):

    skip_condition = sys.version_info[0] < 3
    skip_message = "Subtests are not supported in Python 2"

    def test_classify_stmt(self):
        from google.cloud.spanner_dbapi.parse_utils import STMT_DDL
        from google.cloud.spanner_dbapi.parse_utils import STMT_INSERT
        from google.cloud.spanner_dbapi.parse_utils import STMT_NON_UPDATING
        from google.cloud.spanner_dbapi.parse_utils import STMT_UPDATING
        from google.cloud.spanner_dbapi.parse_utils import classify_stmt

        cases = (
            ("SELECT 1", STMT_NON_UPDATING),
            ("SELECT s.SongName FROM Songs AS s", STMT_NON_UPDATING),
            (
                "WITH sq AS (SELECT SchoolID FROM Roster) SELECT * from sq",
                STMT_NON_UPDATING,
            ),
            (
                "CREATE TABLE django_content_type (id STRING(64) NOT NULL, name STRING(100) "
                "NOT NULL, app_label STRING(100) NOT NULL, model STRING(100) NOT NULL) PRIMARY KEY(id)",
                STMT_DDL,
            ),
            (
                "CREATE INDEX SongsBySingerAlbumSongNameDesc ON "
                "Songs(SingerId, AlbumId, SongName DESC), INTERLEAVE IN Albums",
                STMT_DDL,
            ),
            ("CREATE INDEX SongsBySongName ON Songs(SongName)", STMT_DDL),
            (
                "CREATE INDEX AlbumsByAlbumTitle2 ON Albums(AlbumTitle) STORING (MarketingBudget)",
                STMT_DDL,
            ),
            ("INSERT INTO table (col1) VALUES (1)", STMT_INSERT),
            ("UPDATE table SET col1 = 1 WHERE col1 = NULL", STMT_UPDATING),
        )

        for query, want_class in cases:
            self.assertEqual(classify_stmt(query), want_class)

    @unittest.skipIf(skip_condition, skip_message)
    def test_parse_insert(self):
        from google.cloud.spanner_dbapi.parse_utils import parse_insert
        from google.cloud.spanner_dbapi.exceptions import ProgrammingError

        with self.assertRaises(ProgrammingError):
            parse_insert("bad-sql", None)

        cases = [
            (
                "INSERT INTO django_migrations (app, name, applied) VALUES (%s, %s, %s)",
                [1, 2, 3, 4, 5, 6],
                {
                    "sql_params_list": [
                        (
                            "INSERT INTO django_migrations (app, name, applied) VALUES (%s, %s, %s)",
                            (1, 2, 3),
                        ),
                        (
                            "INSERT INTO django_migrations (app, name, applied) VALUES (%s, %s, %s)",
                            (4, 5, 6),
                        ),
                    ]
                },
            ),
            (
                "INSERT INTO django_migrations(app, name, applied) VALUES (%s, %s, %s)",
                [1, 2, 3, 4, 5, 6],
                {
                    "sql_params_list": [
                        (
                            "INSERT INTO django_migrations (app, name, applied) VALUES (%s, %s, %s)",
                            (1, 2, 3),
                        ),
                        (
                            "INSERT INTO django_migrations (app, name, applied) VALUES (%s, %s, %s)",
                            (4, 5, 6),
                        ),
                    ]
                },
            ),
            (
                "INSERT INTO sales.addresses (street, city, state, zip_code) "
                "SELECT street, city, state, zip_code FROM sales.customers"
                "ORDER BY first_name, last_name",
                None,
                {
                    "sql_params_list": [
                        (
                            "INSERT INTO sales.addresses (street, city, state, zip_code) "
                            "SELECT street, city, state, zip_code FROM sales.customers"
                            "ORDER BY first_name, last_name",
                            None,
                        )
                    ]
                },
            ),
            (
                "INSERT INTO ap (n, ct, cn) "
                "VALUES (%s, %s, %s), (%s, %s, %s), (%s, %s, %s),(%s,      %s, %s)",
                (1, 2, 3, 4, 5, 6, 7, 8, 9),
                {
                    "sql_params_list": [
                        ("INSERT INTO ap (n, ct, cn) VALUES (%s, %s, %s)", (1, 2, 3)),
                        ("INSERT INTO ap (n, ct, cn) VALUES (%s, %s, %s)", (4, 5, 6)),
                        ("INSERT INTO ap (n, ct, cn) VALUES (%s, %s, %s)", (7, 8, 9)),
                    ]
                },
            ),
            (
                "INSERT INTO `no` (`yes`) VALUES (%s)",
                (1, 4, 5),
                {
                    "sql_params_list": [
                        ("INSERT INTO `no` (`yes`) VALUES (%s)", (1,)),
                        ("INSERT INTO `no` (`yes`) VALUES (%s)", (4,)),
                        ("INSERT INTO `no` (`yes`) VALUES (%s)", (5,)),
                    ]
                },
            ),
            (
                "INSERT INTO T (f1, f2) VALUES (1, 2)",
                None,
                {"sql_params_list": [("INSERT INTO T (f1, f2) VALUES (1, 2)", None)]},
            ),
            (
                "INSERT INTO `no` (`yes`, tiff) VALUES (%s, LOWER(%s)), (%s, %s), (%s, %s)",
                (1, "FOO", 5, 10, 11, 29),
                {
                    "sql_params_list": [
                        (
                            "INSERT INTO `no` (`yes`, tiff)  VALUES(%s, LOWER(%s))",
                            (1, "FOO"),
                        ),
                        ("INSERT INTO `no` (`yes`, tiff)  VALUES(%s, %s)", (5, 10)),
                        ("INSERT INTO `no` (`yes`, tiff)  VALUES(%s, %s)", (11, 29)),
                    ]
                },
            ),
        ]

        sql = "INSERT INTO django_migrations (app, name, applied) VALUES (%s, %s, %s)"
        with self.assertRaises(ProgrammingError):
            parse_insert(sql, None)

        for sql, params, want in cases:
            with self.subTest(sql=sql):
                got = parse_insert(sql, params)
                self.assertEqual(got, want, "Mismatch with parse_insert of `%s`" % sql)

    @unittest.skipIf(skip_condition, skip_message)
    def test_parse_insert_invalid(self):
        from google.cloud.spanner_dbapi import exceptions
        from google.cloud.spanner_dbapi.parse_utils import parse_insert

        cases = [
            (
                "INSERT INTO django_migrations (app, name, applied) VALUES (%s, %s, %s), (%s, %s, %s)",
                [1, 2, 3, 4, 5, 6, 7],
                "len\\(params\\)=7 MUST be a multiple of len\\(pyformat_args\\)=3",
            ),
            (
                "INSERT INTO django_migrations (app, name, applied) VALUES (%s, %s, %s), (%s, %s, LOWER(%s))",
                [1, 2, 3, 4, 5, 6, 7],
                "Invalid length: VALUES\\(...\\) len: 6 != len\\(params\\): 7",
            ),
            (
                "INSERT INTO django_migrations (app, name, applied) VALUES (%s, %s, %s), (%s, %s, LOWER(%s)))",
                [1, 2, 3, 4, 5, 6],
                "VALUES: expected `,` got \\) in \\)",
            ),
        ]

        for sql, params, wantException in cases:
            with self.subTest(sql=sql):
                self.assertRaisesRegex(
                    exceptions.ProgrammingError,
                    wantException,
                    lambda: parse_insert(sql, params),
                )

    @unittest.skipIf(skip_condition, skip_message)
    def test_rows_for_insert_or_update(self):
        from google.cloud.spanner_dbapi.parse_utils import rows_for_insert_or_update
        from google.cloud.spanner_dbapi.exceptions import Error

        with self.assertRaises(Error):
            rows_for_insert_or_update([0], [[]])

        with self.assertRaises(Error):
            rows_for_insert_or_update([0], None, ["0", "%s"])

        cases = [
            (
                ["id", "app", "name"],
                [(5, "ap", "n"), (6, "bp", "m")],
                None,
                [(5, "ap", "n"), (6, "bp", "m")],
            ),
            (
                ["app", "name"],
                [("ap", "n"), ("bp", "m")],
                None,
                [("ap", "n"), ("bp", "m")],
            ),
            (
                ["app", "name", "fn"],
                ["ap", "n", "f1", "bp", "m", "f2", "cp", "o", "f3"],
                ["(%s, %s, %s)", "(%s, %s, %s)", "(%s, %s, %s)"],
                [("ap", "n", "f1"), ("bp", "m", "f2"), ("cp", "o", "f3")],
            ),
            (
                ["app", "name", "fn", "ln"],
                [
                    ("ap", "n", (45, "nested"), "ll"),
                    ("bp", "m", "f2", "mt"),
                    ("fp", "cp", "o", "f3"),
                ],
                None,
                [
                    ("ap", "n", (45, "nested"), "ll"),
                    ("bp", "m", "f2", "mt"),
                    ("fp", "cp", "o", "f3"),
                ],
            ),
            (["app", "name", "fn"], ["ap", "n", "f1"], None, [("ap", "n", "f1")]),
        ]

        for i, (columns, params, pyformat_args, want) in enumerate(cases):
            with self.subTest(i=i):
                got = rows_for_insert_or_update(columns, params, pyformat_args)
                self.assertEqual(got, want)

    @unittest.skipIf(skip_condition, skip_message)
    def test_sql_pyformat_args_to_spanner(self):
        import decimal

        from google.cloud.spanner_dbapi.parse_utils import sql_pyformat_args_to_spanner

        cases = [
            (
                (
                    "SELECT * from t WHERE f1=%s, f2 = %s, f3=%s",
                    (10, "abc", "y**$22l3f"),
                ),
                (
                    "SELECT * from t WHERE f1=@a0, f2 = @a1, f3=@a2",
                    {"a0": 10, "a1": "abc", "a2": "y**$22l3f"},
                ),
            ),
            (
                (
                    "INSERT INTO t (f1, f2, f2) VALUES (%s, %s, %s)",
                    ("app", "name", "applied"),
                ),
                (
                    "INSERT INTO t (f1, f2, f2) VALUES (@a0, @a1, @a2)",
                    {"a0": "app", "a1": "name", "a2": "applied"},
                ),
            ),
            (
                (
                    "INSERT INTO t (f1, f2, f2) VALUES (%(f1)s, %(f2)s, %(f3)s)",
                    {"f1": "app", "f2": "name", "f3": "applied"},
                ),
                (
                    "INSERT INTO t (f1, f2, f2) VALUES (@a0, @a1, @a2)",
                    {"a0": "app", "a1": "name", "a2": "applied"},
                ),
            ),
            (
                # Intentionally using a dict with more keys than will be resolved.
                ("SELECT * from t WHERE f1=%(f1)s", {"f1": "app", "f2": "name"}),
                ("SELECT * from t WHERE f1=@a0", {"a0": "app"}),
            ),
            (
                # No args to replace, we MUST return the original params dict
                # since it might be useful to pass to the next user.
                ("SELECT * from t WHERE id=10", {"f1": "app", "f2": "name"}),
                ("SELECT * from t WHERE id=10", {"f1": "app", "f2": "name"}),
            ),
            (
                (
                    "SELECT (an.p + %s) AS np FROM an WHERE (an.p + %s) = %s",
                    (1, 1.0, decimal.Decimal("31")),
                ),
                (
                    "SELECT (an.p + @a0) AS np FROM an WHERE (an.p + @a1) = @a2",
                    {"a0": 1, "a1": 1.0, "a2": str(31)},
                ),
            ),
        ]
        for ((sql_in, params), sql_want) in cases:
            with self.subTest(sql=sql_in):
                got_sql, got_named_args = sql_pyformat_args_to_spanner(sql_in, params)
                want_sql, want_named_args = sql_want
                self.assertEqual(got_sql, want_sql, "SQL does not match")
                self.assertEqual(
                    got_named_args, want_named_args, "Named args do not match"
                )

    @unittest.skipIf(skip_condition, skip_message)
    def test_sql_pyformat_args_to_spanner_invalid(self):
        from google.cloud.spanner_dbapi import exceptions
        from google.cloud.spanner_dbapi.parse_utils import sql_pyformat_args_to_spanner

        cases = [
            (
                "SELECT * from t WHERE f1=%s, f2 = %s, f3=%s, extra=%s",
                (10, "abc", "y**$22l3f"),
            )
        ]
        for sql, params in cases:
            with self.subTest(sql=sql):
                self.assertRaisesRegex(
                    exceptions.Error,
                    "pyformat_args mismatch",
                    lambda: sql_pyformat_args_to_spanner(sql, params),
                )

    def test_cast_for_spanner(self):
        import decimal

        from google.cloud.spanner_dbapi.parse_utils import cast_for_spanner

        dec = 3
        value = decimal.Decimal(dec)
        self.assertEqual(cast_for_spanner(value), str(dec))
        self.assertEqual(cast_for_spanner(5), 5)
        self.assertEqual(cast_for_spanner("string"), "string")

    @unittest.skipIf(skip_condition, skip_message)
    def test_get_param_types(self):
        import datetime

        from google.cloud.spanner_dbapi.parse_utils import DateStr
        from google.cloud.spanner_dbapi.parse_utils import TimestampStr
        from google.cloud.spanner_dbapi.parse_utils import get_param_types

        params = {
            "a1": 10,
            "b1": "string",
            "c1": 10.39,
            "d1": TimestampStr("2005-08-30T01:01:01.000001Z"),
            "e1": DateStr("2019-12-05"),
            "f1": True,
            "g1": datetime.datetime(2011, 9, 1, 13, 20, 30),
            "h1": datetime.date(2011, 9, 1),
            "i1": b"bytes",
            "j1": None,
        }
        want_types = {
            "a1": param_types.INT64,
            "b1": param_types.STRING,
            "c1": param_types.FLOAT64,
            "d1": param_types.TIMESTAMP,
            "e1": param_types.DATE,
            "f1": param_types.BOOL,
            "g1": param_types.TIMESTAMP,
            "h1": param_types.DATE,
            "i1": param_types.BYTES,
        }
        got_types = get_param_types(params)
        self.assertEqual(got_types, want_types)

    def test_get_param_types_none(self):
        from google.cloud.spanner_dbapi.parse_utils import get_param_types

        self.assertEqual(get_param_types(None), None)

    @unittest.skipIf(skip_condition, skip_message)
    def test_ensure_where_clause(self):
        from google.cloud.spanner_dbapi.parse_utils import ensure_where_clause

        cases = [
            (
                "UPDATE a SET a.b=10 FROM articles a JOIN d c ON a.ai = c.ai WHERE c.ci = 1",
                "UPDATE a SET a.b=10 FROM articles a JOIN d c ON a.ai = c.ai WHERE c.ci = 1",
            ),
            (
                "UPDATE (SELECT * FROM A JOIN c ON ai.id = c.id WHERE cl.ci = 1) SET d=5",
                "UPDATE (SELECT * FROM A JOIN c ON ai.id = c.id WHERE cl.ci = 1) SET d=5 WHERE 1=1",
            ),
            (
                "UPDATE T SET A = 1 WHERE C1 = 1 AND C2 = 2",
                "UPDATE T SET A = 1 WHERE C1 = 1 AND C2 = 2",
            ),
            (
                "UPDATE T SET r=r*0.9 WHERE id IN (SELECT id FROM items WHERE r / w >= 1.3 AND q > 100)",
                "UPDATE T SET r=r*0.9 WHERE id IN (SELECT id FROM items WHERE r / w >= 1.3 AND q > 100)",
            ),
            (
                "UPDATE T SET r=r*0.9 WHERE id IN (SELECT id FROM items WHERE r / w >= 1.3 AND q > 100)",
                "UPDATE T SET r=r*0.9 WHERE id IN (SELECT id FROM items WHERE r / w >= 1.3 AND q > 100)",
            ),
            ("DELETE * FROM TABLE", "DELETE * FROM TABLE WHERE 1=1"),
        ]

        for sql, want in cases:
            with self.subTest(sql=sql):
                got = ensure_where_clause(sql)
                self.assertEqual(got, want)

    @unittest.skipIf(skip_condition, skip_message)
    def test_escape_name(self):
        from google.cloud.spanner_dbapi.parse_utils import escape_name

        cases = (
            ("SELECT", "`SELECT`"),
            ("dashed-value", "`dashed-value`"),
            ("with space", "`with space`"),
            ("name", "name"),
            ("", ""),
        )
        for name, want in cases:
            with self.subTest(name=name):
                got = escape_name(name)
                self.assertEqual(got, want)
