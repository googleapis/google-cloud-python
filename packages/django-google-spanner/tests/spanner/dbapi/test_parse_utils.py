# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from unittest import TestCase

from spanner.dbapi.exceptions import Error
from spanner.dbapi.parse_utils import (
    STMT_DDL, STMT_NON_UPDATING, add_missing_id, classify_stmt,
    extract_connection_params, parse_insert, parse_spanner_url,
    reINSTANCE_CONFIG, sql_pyformat_args_to_spanner, validate_instance_config,
)


class ParseUtilsTests(TestCase):
    def test_no_args(self):
        with self.assertRaises(Error) as exc:
            url = None
            got = parse_spanner_url(url)
            self.assertEqual(got, None)
        self.assertEqual(exc.exception.args, ('expecting a non-blank spanner_url',))

    def test_no_host(self):
        # No host present in the URL.
        with self.assertRaises(Error) as exc:
            url = '://spanner.googleapis.com/projects/test-project-012345/instances/test-instance/databases/dev-db'
            got = parse_spanner_url(url)
            self.assertEqual(got, None)
        self.assertEqual(exc.exception.args, ('expecting cloudspanner as the scheme',))

    def test_invalid_scheme(self):
        # Doesn't contain "cloudspanner" as the scheme.
        with self.assertRaises(Error) as exc:
            url = 'foo://spanner.googleapis.com/projects/test-project-012345/instances/test-instance/databases/dev-db'
            got = parse_spanner_url(url)
            self.assertEqual(got, None)
        self.assertEqual(exc.exception.args, ('invalid scheme foo, expected cloudspanner',))

    def test_with_host(self):
        url = (
            'cloudspanner://spanner.googleapis.com/projects/test-project-012345/'
            'instances/test-instance/databases/dev-db'
        )
        got = parse_spanner_url(url)
        want = dict(
            host='spanner.googleapis.com',
            project_id='test-project-012345',
            instance='test-instance',
            database='dev-db',
        )
        self.assertEqual(got, want)

    def test_with_host_and_port(self):
        url = (
            'cloudspanner://spanner.googleapis.com:443/projects/test-project-012345/'
            'instances/test-instance/databases/dev-db'
        )
        got = parse_spanner_url(url)
        want = dict(
            host='spanner.googleapis.com:443',
            project_id='test-project-012345',
            instance='test-instance',
            database='dev-db',
        )
        self.assertEqual(got, want)

    def test_with_host_with_properties(self):
        url = (
            'cloudspanner://spanner.googleapis.com/projects/test-project-012345/'
            'instances/test-instance/databases/dev-db?autocommit=true;readonly=true'
        )
        got = parse_spanner_url(url)
        want = dict(
            host='spanner.googleapis.com',
            project_id='test-project-012345',
            instance='test-instance',
            database='dev-db',
            autocommit=True,
            readonly=True,
        )
        self.assertEqual(got, want)

    def test_extract_connection_params(self):
        cases = [
                (
                    dict(
                        INSTANCE='instance',
                        INSTANCE_CONFIG='projects/proj/instanceConfigs/regional-us-west2',
                        NAME='db',
                        PROJECT_ID='project',
                        AUTOCOMMIT=True,
                        READONLY=True,
                    ),
                    dict(
                        database='db',
                        instance='instance',
                        instance_config='projects/proj/instanceConfigs/regional-us-west2',
                        project_id='project',
                        autocommit=True,
                        readonly=True,
                    ),
                ),
        ]

        for case in cases:
            din, want = case
            got = extract_connection_params(din)
            self.assertEqual(got, want, 'unequal dicts')

    def test_SPANNER_URL_vs_dictParity(self):
        by_spanner_url = dict(
                SPANNER_URL='cloudspanner:/projects/proj/instances/django-dev1/databases/db1?'
                            'instance_config=projects/proj/instanceConfigs/regional-us-west2;'
                            'autocommit=true;readonly=true'
        )
        by_dict = dict(
                INSTANCE='django-dev1',
                NAME='db1',
                INSTANCE_CONFIG='projects/proj/instanceConfigs/regional-us-west2',
                PROJECT_ID='proj',
                AUTOCOMMIT=True,
                READONLY=True,
        )

        got_by_spanner_url = extract_connection_params(by_spanner_url)
        got_by_dict = extract_connection_params(by_dict)

        self.assertEqual(got_by_spanner_url, got_by_dict, 'No parity between equivalent configs')

    def test_validate_instance_config(self):
        configs = [
                'projects/appdev-soda-spanner-staging/instanceConfigs/regional-us-west2',
                'projects/odeke-sandbox/instanceConfigs/regional-us-west2',
        ]

        for config in configs:
            got = validate_instance_config(config)
            self.assertEqual(got, None, "expected '%s' to pass" % config)

    def test_validate_instance_config_bad(self):
        cases = [
                ('', "'' does not match pattern " + reINSTANCE_CONFIG.pattern,),
                (
                    '    projects/appdev-soda-spanner-staging/instanceConfigs/regional-us-west2',
                    "'    projects/appdev-soda-spanner-staging/instanceConfigs/regional-us-west2'"
                    " does not match pattern " + reINSTANCE_CONFIG.pattern,),
                ('projects/odeke-sandbox/instanceConfigs/regional-us-west2', None,),
        ]

        for tt in cases:
            config, want_err = tt
            got = validate_instance_config(config)
            self.assertEqual(got, want_err, "expected '%s' to error" % config)

    def test_classify_stmt(self):
        cases = [
                ('SELECT 1', STMT_NON_UPDATING,),
                ('SELECT s.SongName FROM Songs AS s', STMT_NON_UPDATING,),
                ('EXPLAIN app', STMT_NON_UPDATING,),
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
                {
                    'table': 'django_migrations',
                    'columns': ['app', 'name', 'applied'],
                },
            ),
            (
                'INSERT INTO sales.addresses (street, city, state, zip_code)'
                'SELECT street, city, state, zip_code FROM sales.customers'
                'ORDER BY first_name, last_name',
                {
                    'table': 'sales.addresses',
                    'columns': ['street', 'city', 'state', 'zip_code'],
                },
            ),
        ]
        for sql, want in cases:
            with self.subTest(sql=sql):
                got = parse_insert(sql)
                self.assertEqual(got, want, 'Mismatch with parse_insert of `%s`' % sql)

    def test_add_missing_id(self):
        def gen_id():
            cur_id = 0
            while 1:
                cur_id += 1
                yield cur_id

        gen_gen_id = gen_id()

        def next_id():
            return next(gen_gen_id)

        cases = [
            (
                ['id', 'app', 'name'],
                [(5, 'ap', 'n',), (6, 'bp', 'm',)],
                (
                    ['id', 'app', 'name'],
                    [(5, 'ap', 'n',), (6, 'bp', 'm',)],
                ),
            ),
            (
                ['app', 'name'],
                [('ap', 'n',), ('bp', 'm',)],
                (
                    ['app', 'name', 'id'],
                    [('ap', 'n', 1,), ('bp', 'm', 2,)]
                ),
            ),
        ]
        for i, case in enumerate(cases):
            columns, params, want = case
            with self.subTest(i=i):
                got = add_missing_id(columns, params, next_id)
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
