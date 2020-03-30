# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

import datetime
import decimal
from unittest import TestCase

from google.cloud.spanner_v1 import param_types
from spanner_dbapi.exceptions import Error, ProgrammingError
from spanner_dbapi.parse_utils import (
    STMT_DDL, STMT_NON_UPDATING, DateStr, TimestampStr, classify_stmt,
    ensure_where_clause, escape_name, get_param_types, parse_insert,
    rows_for_insert_or_update, sql_pyformat_args_to_spanner, strip_backticks,
)
from spanner_dbapi.utils import backtick_unicode


class ParseUtilsTests(TestCase):
    def test_classify_stmt(self):
        cases = [
                ('SELECT 1', STMT_NON_UPDATING,),
                ('SELECT s.SongName FROM Songs AS s', STMT_NON_UPDATING,),
                ('WITH sq AS (SELECT SchoolID FROM Roster) SELECT * from sq', STMT_NON_UPDATING,),
                (
                    'CREATE TABLE django_content_type (id STRING(64) NOT NULL, name STRING(100) '
                    'NOT NULL, app_label STRING(100) NOT NULL, model STRING(100) NOT NULL) PRIMARY KEY(id)',
                    STMT_DDL,
                ),
                (
                    'CREATE INDEX SongsBySingerAlbumSongNameDesc ON '
                    'Songs(SingerId, AlbumId, SongName DESC), INTERLEAVE IN Albums',
                    STMT_DDL,
                ),
                ('CREATE INDEX SongsBySongName ON Songs(SongName)', STMT_DDL,),
                ('CREATE INDEX AlbumsByAlbumTitle2 ON Albums(AlbumTitle) STORING (MarketingBudget)', STMT_DDL,),
        ]

        for tt in cases:
            sql, want_classification = tt
            got_classification = classify_stmt(sql)
            self.assertEqual(got_classification, want_classification, 'Classification mismatch')

    def test_parse_insert(self):
        cases = [
            (
                'INSERT INTO django_migrations (app, name, applied) VALUES (%s, %s, %s)',
                [1, 2, 3, 4, 5, 6],
                {
                    'sql_params_list': [
                        (
                            'INSERT INTO django_migrations (app, name, applied) VALUES (%s, %s, %s)',
                            (1, 2, 3,),
                        ),
                        (
                            'INSERT INTO django_migrations (app, name, applied) VALUES (%s, %s, %s)',
                            (4, 5, 6,),
                        ),
                    ],
                },
            ),
            (
                'INSERT INTO django_migrations(app, name, applied) VALUES (%s, %s, %s)',
                [1, 2, 3, 4, 5, 6],
                {
                    'sql_params_list': [
                        (
                            'INSERT INTO django_migrations (app, name, applied) VALUES (%s, %s, %s)',
                            (1, 2, 3,),
                        ),
                        (
                            'INSERT INTO django_migrations (app, name, applied) VALUES (%s, %s, %s)',
                            (4, 5, 6,),
                        ),
                    ],
                },
            ),
            (
                'INSERT INTO sales.addresses (street, city, state, zip_code) '
                'SELECT street, city, state, zip_code FROM sales.customers'
                'ORDER BY first_name, last_name',
                None,
                {
                    'sql_params_list': [(
                        'INSERT INTO sales.addresses (street, city, state, zip_code) '
                        'SELECT street, city, state, zip_code FROM sales.customers'
                        'ORDER BY first_name, last_name',
                        None,
                    )],
                }
            ),
            (

                'INSERT INTO ap (n, ct, cn) '
                'VALUES (%s, %s, %s), (%s, %s, %s), (%s, %s, %s),(%s,      %s, %s)',
                (1, 2, 3, 4, 5, 6, 7, 8, 9),
                {
                    'sql_params_list': [
                        (
                            'INSERT INTO ap (n, ct, cn) VALUES (%s, %s, %s)',
                            (1, 2, 3,),
                        ),
                        (
                            'INSERT INTO ap (n, ct, cn) VALUES (%s, %s, %s)',
                            (4, 5, 6,),
                        ),
                        (
                            'INSERT INTO ap (n, ct, cn) VALUES (%s, %s, %s)',
                            (7, 8, 9,),
                        ),
                    ],
                },
            ),
            (
                'INSERT INTO `no` (`yes`) VALUES (%s)',
                (1, 4, 5),
                {
                    'sql_params_list': [
                        (
                            'INSERT INTO `no` (`yes`) VALUES (%s)',
                            (1,),
                        ),
                        (
                            'INSERT INTO `no` (`yes`) VALUES (%s)',
                            (4,),
                        ),
                        (
                            'INSERT INTO `no` (`yes`) VALUES (%s)',
                            (5,),
                        ),
                    ],
                },
            ),
            (
                'INSERT INTO T (f1, f2) VALUES (1, 2)',
                None,
                {
                    'sql_params_list': [
                        (
                            'INSERT INTO T (f1, f2) VALUES (1, 2)',
                            None,
                        ),
                    ],
                },
            ),
            (
                'INSERT INTO `no` (`yes`, tiff) VALUES (%s, LOWER(%s)), (%s, %s), (%s, %s)',
                (1, 'FOO', 5, 10, 11, 29),
                {
                    'sql_params_list': [
                        ('INSERT INTO `no` (`yes`, tiff)  VALUES(%s, LOWER(%s))', (1, 'FOO',)),
                        ('INSERT INTO `no` (`yes`, tiff)  VALUES(%s, %s)', (5, 10)),
                        ('INSERT INTO `no` (`yes`, tiff)  VALUES(%s, %s)', (11, 29)),
                    ],
                },
            ),
        ]

        for sql, params, want in cases:
            with self.subTest(sql=sql):
                got = parse_insert(sql, params)
                self.assertEqual(got, want, 'Mismatch with parse_insert of `%s`' % sql)

    def test_parse_insert_invalid(self):
        cases = [
            (
                'INSERT INTO django_migrations (app, name, applied) VALUES (%s, %s, %s), (%s, %s, %s)',
                [1, 2, 3, 4, 5, 6, 7],
                'len\\(params\\)=7 MUST be a multiple of len\\(pyformat_args\\)=3',
            ),
            (
                'INSERT INTO django_migrations (app, name, applied) VALUES (%s, %s, %s), (%s, %s, LOWER(%s))',
                [1, 2, 3, 4, 5, 6, 7],
                'Invalid length: VALUES\\(...\\) len: 6 != len\\(params\\): 7',
            ),
            (
                'INSERT INTO django_migrations (app, name, applied) VALUES (%s, %s, %s), (%s, %s, LOWER(%s)))',
                [1, 2, 3, 4, 5, 6],
                'VALUES: expected `,` got \\) in \\)',
            ),
        ]

        for sql, params, wantException in cases:
            with self.subTest(sql=sql):
                self.assertRaisesRegex(
                    ProgrammingError,
                    wantException,
                    lambda: parse_insert(sql, params),
                )

    def test_rows_for_insert_or_update(self):
        cases = [
            (
                ['id', 'app', 'name'],
                [(5, 'ap', 'n',), (6, 'bp', 'm',)],
                None,
                [(5, 'ap', 'n',), (6, 'bp', 'm',)],
            ),
            (
                ['app', 'name'],
                [('ap', 'n',), ('bp', 'm',)],
                None,
                [('ap', 'n'), ('bp', 'm',)]
            ),
            (
                ['app', 'name', 'fn'],
                ['ap', 'n', 'f1', 'bp', 'm', 'f2', 'cp', 'o', 'f3'],
                ['(%s, %s, %s)', '(%s, %s, %s)', '(%s, %s, %s)'],
                [('ap', 'n', 'f1',), ('bp', 'm', 'f2',), ('cp', 'o', 'f3',)]
            ),
            (
                ['app', 'name', 'fn', 'ln'],
                [('ap', 'n', (45, 'nested',), 'll',), ('bp', 'm', 'f2', 'mt',), ('fp', 'cp', 'o', 'f3',)],
                None,
                [
                    ('ap', 'n', (45, 'nested',), 'll',),
                    ('bp', 'm', 'f2', 'mt',),
                    ('fp', 'cp', 'o', 'f3',),
                ],
            ),
            (
                ['app', 'name', 'fn'],
                ['ap', 'n', 'f1'],
                None,
                [('ap', 'n', 'f1',)]
            ),
        ]

        for i, (columns, params, pyformat_args, want) in enumerate(cases):
            with self.subTest(i=i):
                got = rows_for_insert_or_update(columns, params, pyformat_args)
                self.assertEqual(got, want)

    def test_sql_pyformat_args_to_spanner(self):
        cases = [
            (
                ('SELECT * from t WHERE f1=%s, f2 = %s, f3=%s', (10, 'abc', 'y**$22l3f',)),
                ('SELECT * from t WHERE f1=@a0, f2 = @a1, f3=@a2', {'a0': 10, 'a1': 'abc', 'a2': 'y**$22l3f'}),
            ),
            (
                ('INSERT INTO t (f1, f2, f2) VALUES (%s, %s, %s)', ('app', 'name', 'applied',)),
                ('INSERT INTO t (f1, f2, f2) VALUES (@a0, @a1, @a2)', {'a0': 'app', 'a1': 'name', 'a2': 'applied'}),
            ),
            (
                (
                    'INSERT INTO t (f1, f2, f2) VALUES (%(f1)s, %(f2)s, %(f3)s)',
                    {'f1': 'app', 'f2': 'name', 'f3': 'applied'},
                ),
                (
                    'INSERT INTO t (f1, f2, f2) VALUES (@a0, @a1, @a2)',
                    {'a0': 'app', 'a1': 'name', 'a2': 'applied'},
                ),
            ),
            (
                # Intentionally using a dict with more keys than will be resolved.
                ('SELECT * from t WHERE f1=%(f1)s', {'f1': 'app', 'f2': 'name'}),
                ('SELECT * from t WHERE f1=@a0', {'a0': 'app'}),
            ),
            (
                # No args to replace, we MUST return the original params dict
                # since it might be useful to pass to the next user.
                ('SELECT * from t WHERE id=10', {'f1': 'app', 'f2': 'name'}),
                ('SELECT * from t WHERE id=10', {'f1': 'app', 'f2': 'name'}),
            ),
            (
                ('SELECT (an.p + %s) AS np FROM an WHERE (an.p + %s) = %s', (1, 1.0, decimal.Decimal('31'),)),
                ('SELECT (an.p + @a0) AS np FROM an WHERE (an.p + @a1) = @a2', {'a0': 1, 'a1': 1.0, 'a2': 31.0}),
            ),
        ]
        for ((sql_in, params), sql_want) in cases:
            with self.subTest(sql=sql_in):
                got_sql, got_named_args = sql_pyformat_args_to_spanner(sql_in, params)
                want_sql, want_named_args = sql_want
                self.assertEqual(got_sql, want_sql, 'SQL does not match')
                self.assertEqual(got_named_args, want_named_args, 'Named args do not match')

    def test_sql_pyformat_args_to_spanner_invalid(self):
        cases = [
            ('SELECT * from t WHERE f1=%s, f2 = %s, f3=%s, extra=%s', (10, 'abc', 'y**$22l3f',)),
        ]
        for sql, params in cases:
            with self.subTest(sql=sql):
                self.assertRaisesRegex(Error, 'pyformat_args mismatch',
                                       lambda: sql_pyformat_args_to_spanner(sql, params),
                                       )

    def test_get_param_types(self):
        cases = [
            (
                {'a1': 10, 'b1': '2005-08-30T01:01:01.000001Z', 'c1': '2019-12-05', 'd1': 10.39},
                {
                    'a1': param_types.INT64,
                    'b1': param_types.STRING,
                    'c1': param_types.STRING,
                    'd1': param_types.FLOAT64,
                },
            ),
            (
                {'a1': 10, 'b1': TimestampStr('2005-08-30T01:01:01.000001Z'), 'c1': '2019-12-05'},
                {'a1': param_types.INT64, 'b1': param_types.TIMESTAMP, 'c1': param_types.STRING},
            ),
            (
                {'a1': 10, 'b1': '2005-08-30T01:01:01.000001Z', 'c1': DateStr('2019-12-05')},
                {'a1': param_types.INT64, 'b1': param_types.STRING, 'c1': param_types.DATE},
            ),
            (
                {'a1': 10, 'b1': '2005-08-30T01:01:01.000001Z'},
                {'a1': param_types.INT64, 'b1': param_types.STRING},
            ),
            (
                {'a1': 10, 'b1': TimestampStr('2005-08-30T01:01:01.000001Z'), 'c1': DateStr('2005-08-30')},
                {'a1': param_types.INT64, 'b1': param_types.TIMESTAMP, 'c1': param_types.DATE},
            ),
            (
                {'a1': 10, 'b1': 'aaaaa08-30T01:01:01.000001Z'},
                {'a1': param_types.INT64, 'b1': param_types.STRING},
            ),
            (
                {'a1': 10, 'b1': '2005-08-30T01:01:01.000001', 't1': True, 't2': False, 'f1': 99e9},
                {
                    'a1': param_types.INT64,
                    'b1': param_types.STRING,
                    't1': param_types.BOOL,
                    't2': param_types.BOOL,
                    'f1': param_types.FLOAT64,
                },
            ),
            (
                {'a1': 10, 'b1': '2019-11-26T02:55:41.000000Z'},
                {'a1': param_types.INT64, 'b1': param_types.STRING},
            ),
            (
                {
                    'a1': 10, 'b1': TimestampStr('2019-11-26T02:55:41.000000Z'),
                    'dt1': datetime.datetime(2011, 9, 1, 13, 20, 30),
                    'd1': datetime.date(2011, 9, 1),
                },
                {
                    'a1': param_types.INT64, 'b1': param_types.TIMESTAMP,
                    'dt1': param_types.TIMESTAMP, 'd1': param_types.DATE,
                },
            ),
            (
                {'a1': 10, 'b1': TimestampStr('2019-11-26T02:55:41.000000Z')},
                {'a1': param_types.INT64, 'b1': param_types.TIMESTAMP},
            ),
            ({'a1': b'bytes'}, {'a1': param_types.BYTES}),
            ({'a1': 10, 'b1': None}, {'a1': param_types.INT64}),
            (None, None),
        ]

        for i, (params, want_param_types) in enumerate(cases):
            with self.subTest(i=i):
                got_param_types = get_param_types(params)
                self.assertEqual(got_param_types, want_param_types)

    def test_ensure_where_clause(self):
        cases = [
                (
                    'UPDATE a SET a.b=10 FROM articles a JOIN d c ON a.ai = c.ai WHERE c.ci = 1',
                    'UPDATE a SET a.b=10 FROM articles a JOIN d c ON a.ai = c.ai WHERE c.ci = 1',
                ),
                (
                    'UPDATE (SELECT * FROM A JOIN c ON ai.id = c.id WHERE cl.ci = 1) SET d=5',
                    'UPDATE (SELECT * FROM A JOIN c ON ai.id = c.id WHERE cl.ci = 1) SET d=5 WHERE 1=1',
                ),
                (
                    'UPDATE T SET A = 1 WHERE C1 = 1 AND C2 = 2',
                    'UPDATE T SET A = 1 WHERE C1 = 1 AND C2 = 2',
                ),
                (
                    'UPDATE T SET r=r*0.9 WHERE id IN (SELECT id FROM items WHERE r / w >= 1.3 AND q > 100)',
                    'UPDATE T SET r=r*0.9 WHERE id IN (SELECT id FROM items WHERE r / w >= 1.3 AND q > 100)',
                ),
                (
                    'UPDATE T SET r=r*0.9 WHERE id IN (SELECT id FROM items WHERE r / w >= 1.3 AND q > 100)',
                    'UPDATE T SET r=r*0.9 WHERE id IN (SELECT id FROM items WHERE r / w >= 1.3 AND q > 100)',
                ),
                (
                    'DELETE * FROM TABLE',
                    'DELETE * FROM TABLE WHERE 1=1',
                ),
        ]

        for sql, want in cases:
            with self.subTest(sql=sql):
                got = ensure_where_clause(sql)
                self.assertEqual(got, want)

    def test_escape_name(self):
        cases = [
                ('SELECT', '`SELECT`'),
                ('id', 'id'),
                ('', ''),
                ('dashed-value', '`dashed-value`'),
                ('with space', '`with space`'),
        ]

        for name, want in cases:
            with self.subTest(name=name):
                got = escape_name(name)
                self.assertEqual(got, want)

    def test_strip_backticks(self):
        cases = [
            ('foo', 'foo'),
            ('`foo`', 'foo'),
        ]
        for name, want in cases:
            with self.subTest(name=name):
                got = strip_backticks(name)
                self.assertEqual(got, want)

    def test_backtick_unicode(self):
        cases = [
            ('SELECT (1) as foo WHERE 1=1', 'SELECT (1) as foo WHERE 1=1'),
            ('SELECT (1) as föö', 'SELECT (1) as `föö`'),
            ('SELECT (1) as `föö`', 'SELECT (1) as `föö`'),
            ('SELECT (1) as `föö` `umläut', 'SELECT (1) as `föö` `umläut'),
            ('SELECT (1) as `föö', 'SELECT (1) as `föö'),
        ]
        for sql, want in cases:
            with self.subTest(sql=sql):
                got = backtick_unicode(sql)
                self.assertEqual(got, want)
