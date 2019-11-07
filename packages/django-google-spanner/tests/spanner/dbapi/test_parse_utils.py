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
    extract_connection_params, parse_spanner_url,
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
