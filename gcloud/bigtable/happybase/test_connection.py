# Copyright 2016 Google Inc. All rights reserved.
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


class Test__get_cluster(unittest2.TestCase):

    def _callFUT(self, timeout=None):
        from gcloud.bigtable.happybase.connection import _get_cluster
        return _get_cluster(timeout=timeout)

    def _helper(self, timeout=None, clusters=(), failed_zones=()):
        from functools import partial
        from gcloud._testing import _Monkey
        from gcloud.bigtable.happybase import connection as MUT

        client_with_clusters = partial(_Client, clusters=clusters,
                                       failed_zones=failed_zones)
        with _Monkey(MUT, Client=client_with_clusters):
            result = self._callFUT(timeout=timeout)

        # If we've reached this point, then _callFUT didn't fail, so we know
        # there is exactly one cluster.
        cluster, = clusters
        self.assertEqual(result, cluster)
        client = cluster.client
        self.assertEqual(client.args, ())
        expected_kwargs = {'admin': True}
        if timeout is not None:
            expected_kwargs['timeout_seconds'] = timeout / 1000.0
        self.assertEqual(client.kwargs, expected_kwargs)
        self.assertEqual(client.start_calls, 1)
        self.assertEqual(client.stop_calls, 1)

    def test_default(self):
        cluster = _Cluster()
        self._helper(clusters=[cluster])

    def test_with_timeout(self):
        cluster = _Cluster()
        self._helper(timeout=2103, clusters=[cluster])

    def test_with_no_clusters(self):
        with self.assertRaises(ValueError):
            self._helper()

    def test_with_too_many_clusters(self):
        clusters = [_Cluster(), _Cluster()]
        with self.assertRaises(ValueError):
            self._helper(clusters=clusters)

    def test_with_failed_zones(self):
        cluster = _Cluster()
        failed_zone = 'us-central1-c'
        with self.assertRaises(ValueError):
            self._helper(clusters=[cluster],
                         failed_zones=[failed_zone])


class TestConnection(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.bigtable.happybase.connection import Connection
        return Connection

    def _makeOne(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_constructor_defaults(self):
        cluster = _Cluster()  # Avoid implicit environ check.
        self.assertEqual(cluster._client.start_calls, 0)
        connection = self._makeOne(cluster=cluster)
        self.assertEqual(cluster._client.start_calls, 1)
        self.assertEqual(cluster._client.stop_calls, 0)

        self.assertEqual(connection._cluster, cluster)
        self.assertEqual(connection.table_prefix, None)
        self.assertEqual(connection.table_prefix_separator, '_')

    def test_constructor_no_autoconnect(self):
        cluster = _Cluster()  # Avoid implicit environ check.
        connection = self._makeOne(autoconnect=False, cluster=cluster)
        self.assertEqual(cluster._client.start_calls, 0)
        self.assertEqual(cluster._client.stop_calls, 0)
        self.assertEqual(connection.table_prefix, None)
        self.assertEqual(connection.table_prefix_separator, '_')

    def test_constructor_missing_cluster(self):
        from gcloud._testing import _Monkey
        from gcloud.bigtable.happybase import connection as MUT

        cluster = _Cluster()
        timeout = object()
        get_cluster_called = []

        def mock_get_cluster(timeout):
            get_cluster_called.append(timeout)
            return cluster

        with _Monkey(MUT, _get_cluster=mock_get_cluster):
            connection = self._makeOne(autoconnect=False, cluster=None,
                                       timeout=timeout)
            self.assertEqual(connection.table_prefix, None)
            self.assertEqual(connection.table_prefix_separator, '_')
            self.assertEqual(connection._cluster, cluster)

        self.assertEqual(get_cluster_called, [timeout])

    def test_constructor_explicit(self):
        autoconnect = False
        table_prefix = 'table-prefix'
        table_prefix_separator = 'sep'
        cluster_copy = _Cluster()
        cluster = _Cluster(copies=[cluster_copy])

        connection = self._makeOne(
            autoconnect=autoconnect,
            table_prefix=table_prefix,
            table_prefix_separator=table_prefix_separator,
            cluster=cluster)
        self.assertEqual(connection.table_prefix, table_prefix)
        self.assertEqual(connection.table_prefix_separator,
                         table_prefix_separator)

    def test_constructor_with_unknown_argument(self):
        cluster = _Cluster()
        with self.assertRaises(TypeError):
            self._makeOne(cluster=cluster, unknown='foo')

    def test_constructor_with_legacy_args(self):
        from gcloud._testing import _Monkey
        from gcloud.bigtable.happybase import connection as MUT

        warned = []

        def mock_warn(msg):
            warned.append(msg)

        cluster = _Cluster()
        with _Monkey(MUT, _WARN=mock_warn):
            self._makeOne(cluster=cluster, host=object(),
                          port=object(), compat=object(),
                          transport=object(), protocol=object())

        self.assertEqual(len(warned), 1)
        self.assertIn('host', warned[0])
        self.assertIn('port', warned[0])
        self.assertIn('compat', warned[0])
        self.assertIn('transport', warned[0])
        self.assertIn('protocol', warned[0])

    def test_constructor_with_timeout_and_cluster(self):
        cluster = _Cluster()
        with self.assertRaises(ValueError):
            self._makeOne(cluster=cluster, timeout=object())

    def test_constructor_non_string_prefix(self):
        table_prefix = object()

        with self.assertRaises(TypeError):
            self._makeOne(autoconnect=False,
                          table_prefix=table_prefix)

    def test_constructor_non_string_prefix_separator(self):
        table_prefix_separator = object()

        with self.assertRaises(TypeError):
            self._makeOne(autoconnect=False,
                          table_prefix_separator=table_prefix_separator)

    def test_open(self):
        cluster = _Cluster()  # Avoid implicit environ check.
        connection = self._makeOne(autoconnect=False, cluster=cluster)
        self.assertEqual(cluster._client.start_calls, 0)
        connection.open()
        self.assertEqual(cluster._client.start_calls, 1)
        self.assertEqual(cluster._client.stop_calls, 0)

    def test_close(self):
        cluster = _Cluster()  # Avoid implicit environ check.
        connection = self._makeOne(autoconnect=False, cluster=cluster)
        self.assertEqual(cluster._client.stop_calls, 0)
        connection.close()
        self.assertEqual(cluster._client.stop_calls, 1)
        self.assertEqual(cluster._client.start_calls, 0)

    def test___del__with_cluster(self):
        cluster = _Cluster()  # Avoid implicit environ check.
        connection = self._makeOne(autoconnect=False, cluster=cluster)
        self.assertEqual(cluster._client.stop_calls, 0)
        connection.__del__()
        self.assertEqual(cluster._client.stop_calls, 1)

    def test___del__no_cluster(self):
        cluster = _Cluster()  # Avoid implicit environ check.
        connection = self._makeOne(autoconnect=False, cluster=cluster)
        self.assertEqual(cluster._client.stop_calls, 0)
        del connection._cluster
        connection.__del__()
        self.assertEqual(cluster._client.stop_calls, 0)

    def test__table_name_with_prefix_set(self):
        table_prefix = 'table-prefix'
        table_prefix_separator = '<>'
        cluster = _Cluster()

        connection = self._makeOne(
            autoconnect=False,
            table_prefix=table_prefix,
            table_prefix_separator=table_prefix_separator,
            cluster=cluster)

        name = 'some-name'
        prefixed = connection._table_name(name)
        self.assertEqual(prefixed,
                         table_prefix + table_prefix_separator + name)

    def test__table_name_with_no_prefix_set(self):
        cluster = _Cluster()
        connection = self._makeOne(autoconnect=False,
                                   cluster=cluster)

        name = 'some-name'
        prefixed = connection._table_name(name)
        self.assertEqual(prefixed, name)

    def test_table_factory(self):
        from gcloud.bigtable.happybase.table import Table

        cluster = _Cluster()  # Avoid implicit environ check.
        connection = self._makeOne(autoconnect=False, cluster=cluster)

        name = 'table-name'
        table = connection.table(name)

        self.assertTrue(isinstance(table, Table))
        self.assertEqual(table.name, name)
        self.assertEqual(table.connection, connection)

    def _table_factory_prefix_helper(self, use_prefix=True):
        from gcloud.bigtable.happybase.table import Table

        cluster = _Cluster()  # Avoid implicit environ check.
        table_prefix = 'table-prefix'
        table_prefix_separator = '<>'
        connection = self._makeOne(
            autoconnect=False, table_prefix=table_prefix,
            table_prefix_separator=table_prefix_separator,
            cluster=cluster)

        name = 'table-name'
        table = connection.table(name, use_prefix=use_prefix)

        self.assertTrue(isinstance(table, Table))
        prefixed_name = table_prefix + table_prefix_separator + name
        if use_prefix:
            self.assertEqual(table.name, prefixed_name)
        else:
            self.assertEqual(table.name, name)
        self.assertEqual(table.connection, connection)

    def test_table_factory_with_prefix(self):
        self._table_factory_prefix_helper(use_prefix=True)

    def test_table_factory_with_ignored_prefix(self):
        self._table_factory_prefix_helper(use_prefix=False)

    def test_tables(self):
        from gcloud.bigtable.table import Table

        table_name1 = 'table-name1'
        table_name2 = 'table-name2'
        cluster = _Cluster(list_tables_result=[
            Table(table_name1, None),
            Table(table_name2, None),
        ])
        connection = self._makeOne(autoconnect=False, cluster=cluster)
        result = connection.tables()
        self.assertEqual(result, [table_name1, table_name2])

    def test_tables_with_prefix(self):
        from gcloud.bigtable.table import Table

        table_prefix = 'prefix'
        table_prefix_separator = '<>'
        unprefixed_table_name1 = 'table-name1'

        table_name1 = (table_prefix + table_prefix_separator +
                       unprefixed_table_name1)
        table_name2 = 'table-name2'
        cluster = _Cluster(list_tables_result=[
            Table(table_name1, None),
            Table(table_name2, None),
        ])
        connection = self._makeOne(
            autoconnect=False, cluster=cluster, table_prefix=table_prefix,
            table_prefix_separator=table_prefix_separator)
        result = connection.tables()
        self.assertEqual(result, [unprefixed_table_name1])

    def test_create_table(self):
        import operator
        from gcloud._testing import _Monkey
        from gcloud.bigtable.happybase import connection as MUT

        cluster = _Cluster()  # Avoid implicit environ check.
        connection = self._makeOne(autoconnect=False, cluster=cluster)
        mock_gc_rule = object()
        called_options = []

        def mock_parse_family_option(option):
            called_options.append(option)
            return mock_gc_rule

        name = 'table-name'
        col_fam1 = 'cf1'
        col_fam_option1 = object()
        col_fam2 = u'cf2'
        col_fam_option2 = object()
        col_fam3 = b'cf3'
        col_fam_option3 = object()
        families = {
            col_fam1: col_fam_option1,
            # A trailing colon is also allowed.
            col_fam2 + ':': col_fam_option2,
            col_fam3 + b':': col_fam_option3,
        }

        tables_created = []

        def make_table(*args, **kwargs):
            result = _MockLowLevelTable(*args, **kwargs)
            tables_created.append(result)
            return result

        with _Monkey(MUT, _LowLevelTable=make_table,
                     _parse_family_option=mock_parse_family_option):
            connection.create_table(name, families)

        # Just one table would have been created.
        table_instance, = tables_created
        self.assertEqual(table_instance.args, (name, cluster))
        self.assertEqual(table_instance.kwargs, {})
        self.assertEqual(table_instance.create_calls, 1)

        # Check if our mock was called twice, but we don't know the order.
        self.assertEqual(
            set(called_options),
            set([col_fam_option1, col_fam_option2, col_fam_option3]))

        # We expect three column family instances created, but don't know the
        # order due to non-deterministic dict.items().
        col_fam_created = table_instance.col_fam_created
        self.assertEqual(len(col_fam_created), 3)
        col_fam_created.sort(key=operator.attrgetter('column_family_id'))
        self.assertEqual(col_fam_created[0].column_family_id, col_fam1)
        self.assertEqual(col_fam_created[0].gc_rule, mock_gc_rule)
        self.assertEqual(col_fam_created[0].create_calls, 1)
        self.assertEqual(col_fam_created[1].column_family_id, col_fam2)
        self.assertEqual(col_fam_created[1].gc_rule, mock_gc_rule)
        self.assertEqual(col_fam_created[1].create_calls, 1)
        self.assertEqual(col_fam_created[2].column_family_id,
                         col_fam3.decode('utf-8'))
        self.assertEqual(col_fam_created[2].gc_rule, mock_gc_rule)
        self.assertEqual(col_fam_created[2].create_calls, 1)

    def test_create_table_bad_type(self):
        cluster = _Cluster()  # Avoid implicit environ check.
        connection = self._makeOne(autoconnect=False, cluster=cluster)

        name = 'table-name'
        families = None
        with self.assertRaises(TypeError):
            connection.create_table(name, families)

    def test_create_table_bad_value(self):
        cluster = _Cluster()  # Avoid implicit environ check.
        connection = self._makeOne(autoconnect=False, cluster=cluster)

        name = 'table-name'
        families = {}
        with self.assertRaises(ValueError):
            connection.create_table(name, families)

    def _delete_table_helper(self, disable=False):
        from gcloud._testing import _Monkey
        from gcloud.bigtable.happybase import connection as MUT

        cluster = _Cluster()  # Avoid implicit environ check.
        connection = self._makeOne(autoconnect=False, cluster=cluster)

        tables_created = []

        def make_table(*args, **kwargs):
            result = _MockLowLevelTable(*args, **kwargs)
            tables_created.append(result)
            return result

        name = 'table-name'
        with _Monkey(MUT, _LowLevelTable=make_table):
            connection.delete_table(name, disable=disable)

        # Just one table would have been created.
        table_instance, = tables_created
        self.assertEqual(table_instance.args, (name, cluster))
        self.assertEqual(table_instance.kwargs, {})
        self.assertEqual(table_instance.delete_calls, 1)

    def test_delete_table(self):
        self._delete_table_helper()

    def test_delete_table_disable(self):
        from gcloud._testing import _Monkey
        from gcloud.bigtable.happybase import connection as MUT

        warned = []

        def mock_warn(msg):
            warned.append(msg)

        with _Monkey(MUT, _WARN=mock_warn):
            self._delete_table_helper(disable=True)

        self.assertEqual(warned, [MUT._DISABLE_DELETE_MSG])

    def test_enable_table(self):
        cluster = _Cluster()  # Avoid implicit environ check.
        connection = self._makeOne(autoconnect=False, cluster=cluster)

        name = 'table-name'
        with self.assertRaises(NotImplementedError):
            connection.enable_table(name)

    def test_disable_table(self):
        cluster = _Cluster()  # Avoid implicit environ check.
        connection = self._makeOne(autoconnect=False, cluster=cluster)

        name = 'table-name'
        with self.assertRaises(NotImplementedError):
            connection.disable_table(name)

    def test_is_table_enabled(self):
        cluster = _Cluster()  # Avoid implicit environ check.
        connection = self._makeOne(autoconnect=False, cluster=cluster)

        name = 'table-name'
        with self.assertRaises(NotImplementedError):
            connection.is_table_enabled(name)

    def test_compact_table(self):
        cluster = _Cluster()  # Avoid implicit environ check.
        connection = self._makeOne(autoconnect=False, cluster=cluster)

        name = 'table-name'
        major = True
        with self.assertRaises(NotImplementedError):
            connection.compact_table(name, major=major)


class Test__parse_family_option(unittest2.TestCase):

    def _callFUT(self, option):
        from gcloud.bigtable.happybase.connection import _parse_family_option
        return _parse_family_option(option)

    def test_dictionary_no_keys(self):
        option = {}
        result = self._callFUT(option)
        self.assertEqual(result, None)

    def test_null(self):
        option = None
        result = self._callFUT(option)
        self.assertEqual(result, None)

    def test_dictionary_bad_key(self):
        from gcloud._testing import _Monkey
        from gcloud.bigtable.happybase import connection as MUT

        warned = []

        def mock_warn(msg):
            warned.append(msg)

        option = {'badkey': None}
        with _Monkey(MUT, _WARN=mock_warn):
            result = self._callFUT(option)

        self.assertEqual(result, None)
        self.assertEqual(len(warned), 1)
        self.assertIn('badkey', warned[0])

    def test_dictionary_versions_key(self):
        from gcloud.bigtable.column_family import MaxVersionsGCRule

        versions = 42
        option = {'max_versions': versions}
        result = self._callFUT(option)

        gc_rule = MaxVersionsGCRule(versions)
        self.assertEqual(result, gc_rule)

    def test_dictionary_ttl_key(self):
        import datetime
        from gcloud.bigtable.column_family import MaxAgeGCRule

        time_to_live = 24 * 60 * 60
        max_age = datetime.timedelta(days=1)
        option = {'time_to_live': time_to_live}
        result = self._callFUT(option)

        gc_rule = MaxAgeGCRule(max_age)
        self.assertEqual(result, gc_rule)

    def test_dictionary_both_keys(self):
        import datetime
        from gcloud.bigtable.column_family import GCRuleIntersection
        from gcloud.bigtable.column_family import MaxAgeGCRule
        from gcloud.bigtable.column_family import MaxVersionsGCRule

        versions = 42
        time_to_live = 24 * 60 * 60
        option = {
            'max_versions': versions,
            'time_to_live': time_to_live,
        }
        result = self._callFUT(option)

        max_age = datetime.timedelta(days=1)
        # NOTE: This relies on the order of the rules in the method we are
        #       calling matching this order here.
        gc_rule1 = MaxAgeGCRule(max_age)
        gc_rule2 = MaxVersionsGCRule(versions)
        gc_rule = GCRuleIntersection(rules=[gc_rule1, gc_rule2])
        self.assertEqual(result, gc_rule)

    def test_non_dictionary(self):
        option = object()
        self.assertFalse(isinstance(option, dict))
        result = self._callFUT(option)
        self.assertEqual(result, option)


class _Client(object):

    def __init__(self, *args, **kwargs):
        self.clusters = kwargs.pop('clusters', [])
        for cluster in self.clusters:
            cluster.client = self
        self.failed_zones = kwargs.pop('failed_zones', [])
        self.args = args
        self.kwargs = kwargs
        self.start_calls = 0
        self.stop_calls = 0

    def start(self):
        self.start_calls += 1

    def stop(self):
        self.stop_calls += 1

    def list_clusters(self):
        return self.clusters, self.failed_zones


class _Cluster(object):

    def __init__(self, copies=(), list_tables_result=()):
        self.copies = list(copies)
        # Included to support Connection.__del__
        self._client = _Client()
        self.list_tables_result = list_tables_result

    def copy(self):
        if self.copies:
            result = self.copies[0]
            self.copies[:] = self.copies[1:]
            return result
        else:
            return self

    def list_tables(self):
        return self.list_tables_result


class _MockLowLevelColumnFamily(object):

    def __init__(self, column_family_id, gc_rule=None):
        self.column_family_id = column_family_id
        self.gc_rule = gc_rule
        self.create_calls = 0

    def create(self):
        self.create_calls += 1


class _MockLowLevelTable(object):

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.delete_calls = 0
        self.create_calls = 0
        self.col_fam_created = []

    def delete(self):
        self.delete_calls += 1

    def create(self):
        self.create_calls += 1

    def column_family(self, column_family_id, gc_rule=None):
        result = _MockLowLevelColumnFamily(column_family_id, gc_rule=gc_rule)
        self.col_fam_created.append(result)
        return result
