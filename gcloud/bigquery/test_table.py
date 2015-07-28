# Copyright 2015 Google Inc. All rights reserved.
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

import unittest2


class TestTable(unittest2.TestCase):
    PROJECT = 'project'
    DS_NAME = 'dataset-name'
    TABLE_NAME = 'table-name'

    def _getTargetClass(self):
        from gcloud.bigquery.table import Table
        return Table

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor(self):
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        table = self._makeOne(self.TABLE_NAME, dataset)
        self.assertEqual(table.name, self.TABLE_NAME)
        self.assertTrue(table._dataset is dataset)
        self.assertEqual(
            table.path,
            '/projects/%s/datasets/%s/tables/%s' % (
                self.PROJECT, self.DS_NAME, self.TABLE_NAME))

        self.assertEqual(table.created, None)
        self.assertEqual(table.dataset_id, None)
        self.assertEqual(table.etag, None)
        self.assertEqual(table.modified, None)
        self.assertEqual(table.num_bytes, None)
        self.assertEqual(table.num_rows, None)
        self.assertEqual(table.self_link, None)
        self.assertEqual(table.table_type, None)

        self.assertEqual(table.description, None)
        self.assertEqual(table.expires, None)
        self.assertEqual(table.friendly_name, None)
        self.assertEqual(table.location, None)
        self.assertEqual(table.view_query, None)

    def test_description_setter_bad_value(self):
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        table = self._makeOne(self.TABLE_NAME, dataset)
        with self.assertRaises(ValueError):
            table.description = 12345

    def test_description_setter(self):
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        table = self._makeOne(self.TABLE_NAME, dataset)
        table.description = 'DESCRIPTION'
        self.assertEqual(table.description, 'DESCRIPTION')

    def test_expires_setter_bad_value(self):
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        table = self._makeOne(self.TABLE_NAME, dataset)
        with self.assertRaises(ValueError):
            table.expires = object()

    def test_expires_setter(self):
        import datetime
        import pytz
        WHEN = datetime.datetime(2015, 7, 28, 16, 39, tzinfo=pytz.utc)
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        table = self._makeOne(self.TABLE_NAME, dataset)
        table.expires = WHEN
        self.assertEqual(table.expires, WHEN)

    def test_friendly_name_setter_bad_value(self):
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        table = self._makeOne(self.TABLE_NAME, dataset)
        with self.assertRaises(ValueError):
            table.friendly_name = 12345

    def test_friendly_name_setter(self):
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        table = self._makeOne(self.TABLE_NAME, dataset)
        table.friendly_name = 'FRIENDLY'
        self.assertEqual(table.friendly_name, 'FRIENDLY')

    def test_location_setter_bad_value(self):
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        table = self._makeOne(self.TABLE_NAME, dataset)
        with self.assertRaises(ValueError):
            table.location = 12345

    def test_location_setter(self):
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        table = self._makeOne(self.TABLE_NAME, dataset)
        table.location = 'LOCATION'
        self.assertEqual(table.location, 'LOCATION')

    def test_view_query_setter_bad_value(self):
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        table = self._makeOne(self.TABLE_NAME, dataset)
        with self.assertRaises(ValueError):
            table.view_query = 12345

    def test_view_query_setter(self):
        client = _Client(self.PROJECT)
        dataset = _Dataset(client)
        table = self._makeOne(self.TABLE_NAME, dataset)
        table.view_query = 'select * from foo'
        self.assertEqual(table.view_query, 'select * from foo')
        table.view_query = None
        self.assertEqual(table.view_query, None)


class _Client(object):

    def __init__(self, project='project', connection=None):
        self.project = project
        self.connection = connection


class _Dataset(object):

    def __init__(self, client, name=TestTable.DS_NAME):
        self._client = client
        self._name = name

    @property
    def path(self):
        return '/projects/%s/datasets/%s' % (
            self._client.project, self._name)
