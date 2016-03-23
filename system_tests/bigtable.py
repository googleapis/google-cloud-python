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

import datetime
import operator
import time

import unittest2

from gcloud import _helpers
from gcloud._helpers import _datetime_from_microseconds
from gcloud._helpers import _microseconds_from_datetime
from gcloud._helpers import UTC
from gcloud.bigtable.client import Client
from gcloud.bigtable.column_family import MaxVersionsGCRule
from gcloud.bigtable.row_filters import ApplyLabelFilter
from gcloud.bigtable.row_filters import ColumnQualifierRegexFilter
from gcloud.bigtable.row_filters import RowFilterChain
from gcloud.bigtable.row_filters import RowFilterUnion
from gcloud.bigtable.row_data import Cell
from gcloud.bigtable.row_data import PartialRowData
from gcloud.environment_vars import TESTS_PROJECT


_helpers.PROJECT = TESTS_PROJECT
CENTRAL_1C_ZONE = 'us-central1-c'
NOW_MILLIS = int(1000 * time.time())
CLUSTER_ID = 'gcloud-python-%d' % (NOW_MILLIS,)
TABLE_ID = 'gcloud-python-test-table'
COLUMN_FAMILY_ID1 = u'col-fam-id1'
COLUMN_FAMILY_ID2 = u'col-fam-id2'
COL_NAME1 = b'col-name1'
COL_NAME2 = b'col-name2'
COL_NAME3 = b'col-name3-but-other-fam'
CELL_VAL1 = b'cell-val'
CELL_VAL2 = b'cell-val-newer'
CELL_VAL3 = b'altcol-cell-val'
CELL_VAL4 = b'foo'
ROW_KEY = b'row-key'
ROW_KEY_ALT = b'row-key-alt'
EXISTING_CLUSTERS = []
EXPECTED_ZONES = (
    'asia-east1-b',
    'europe-west1-c',
    'us-central1-b',
    CENTRAL_1C_ZONE,
)


class Config(object):
    """Run-time configuration to be modified at set-up.

    This is a mutable stand-in to allow test set-up to modify
    global state.
    """
    CLIENT = None
    CLUSTER = None


def _operation_wait(operation, max_attempts=5):
    """Wait until an operation has completed.

    :type operation: :class:`gcloud.bigtable.cluster.Operation`
    :param operation: Operation that has not finished.

    :type max_attempts: int
    :param max_attempts: (Optional) The maximum number of times to check if
                         the operation has finished. Defaults to 5.
    """
    total_sleep = 0
    while not operation.finished():
        if total_sleep > max_attempts:
            return False
        time.sleep(1)
        total_sleep += 1

    return True


def setUpModule():
    Config.CLIENT = Client(admin=True)
    Config.CLUSTER = Config.CLIENT.cluster(CENTRAL_1C_ZONE, CLUSTER_ID,
                                           display_name=CLUSTER_ID)
    Config.CLIENT.start()
    clusters, failed_zones = Config.CLIENT.list_clusters()

    if len(failed_zones) != 0:
        raise ValueError('List clusters failed in module set up.')

    EXISTING_CLUSTERS[:] = clusters

    # After listing, create the test cluster.
    created_op = Config.CLUSTER.create()
    if not _operation_wait(created_op):
        raise RuntimeError('Cluster creation exceed 5 seconds.')


def tearDownModule():
    Config.CLUSTER.delete()
    Config.CLIENT.stop()


class TestClusterAdminAPI(unittest2.TestCase):

    def setUp(self):
        self.clusters_to_delete = []

    def tearDown(self):
        for cluster in self.clusters_to_delete:
            cluster.delete()

    def test_list_zones(self):
        zones = Config.CLIENT.list_zones()
        self.assertEqual(sorted(zones), sorted(EXPECTED_ZONES))

    def test_list_clusters(self):
        clusters, failed_zones = Config.CLIENT.list_clusters()
        self.assertEqual(failed_zones, [])
        # We have added one new cluster in `setUpModule`.
        self.assertEqual(len(clusters), len(EXISTING_CLUSTERS) + 1)
        for cluster in clusters:
            cluster_existence = (cluster in EXISTING_CLUSTERS or
                                 cluster == Config.CLUSTER)
            self.assertTrue(cluster_existence)

    def test_reload(self):
        # Use same arguments as Config.CLUSTER (created in `setUpModule`)
        # so we can use reload() on a fresh instance.
        cluster = Config.CLIENT.cluster(CENTRAL_1C_ZONE, CLUSTER_ID)
        # Make sure metadata unset before reloading.
        cluster.display_name = None
        cluster.serve_nodes = None

        cluster.reload()
        self.assertEqual(cluster.display_name, Config.CLUSTER.display_name)
        self.assertEqual(cluster.serve_nodes, Config.CLUSTER.serve_nodes)

    def test_create_cluster(self):
        cluster_id = '%s-a' % (CLUSTER_ID,)
        cluster = Config.CLIENT.cluster(CENTRAL_1C_ZONE, cluster_id)
        operation = cluster.create()
        # Make sure this cluster gets deleted after the test case.
        self.clusters_to_delete.append(cluster)

        # We want to make sure the operation completes.
        self.assertTrue(_operation_wait(operation))

        # Create a new cluster instance and make sure it is the same.
        cluster_alt = Config.CLIENT.cluster(CENTRAL_1C_ZONE, cluster_id)
        cluster_alt.reload()

        self.assertEqual(cluster, cluster_alt)
        self.assertEqual(cluster.display_name, cluster_alt.display_name)
        self.assertEqual(cluster.serve_nodes, cluster_alt.serve_nodes)

    def test_update(self):
        curr_display_name = Config.CLUSTER.display_name
        Config.CLUSTER.display_name = 'Foo Bar Baz'
        operation = Config.CLUSTER.update()

        # We want to make sure the operation completes.
        self.assertTrue(_operation_wait(operation))

        # Create a new cluster instance and make sure it is the same.
        cluster_alt = Config.CLIENT.cluster(CENTRAL_1C_ZONE, CLUSTER_ID)
        self.assertNotEqual(cluster_alt.display_name,
                            Config.CLUSTER.display_name)
        cluster_alt.reload()
        self.assertEqual(cluster_alt.display_name,
                         Config.CLUSTER.display_name)

        # Make sure to put the cluster back the way it was for the
        # other test cases.
        Config.CLUSTER.display_name = curr_display_name
        operation = Config.CLUSTER.update()

        # We want to make sure the operation completes.
        self.assertTrue(_operation_wait(operation))


class TestTableAdminAPI(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._table = Config.CLUSTER.table(TABLE_ID)
        cls._table.create()

    @classmethod
    def tearDownClass(cls):
        cls._table.delete()

    def setUp(self):
        self.tables_to_delete = []

    def tearDown(self):
        for table in self.tables_to_delete:
            table.delete()

    def test_list_tables(self):
        # Since `Config.CLUSTER` is newly created in `setUpModule`, the table
        # created in `setUpClass` here will be the only one.
        tables = Config.CLUSTER.list_tables()
        self.assertEqual(tables, [self._table])

    def test_create_table(self):
        temp_table_id = 'foo-bar-baz-table'
        temp_table = Config.CLUSTER.table(temp_table_id)
        temp_table.create()
        self.tables_to_delete.append(temp_table)

        # First, create a sorted version of our expected result.
        name_attr = operator.attrgetter('name')
        expected_tables = sorted([temp_table, self._table], key=name_attr)

        # Then query for the tables in the cluster and sort them by
        # name as well.
        tables = Config.CLUSTER.list_tables()
        sorted_tables = sorted(tables, key=name_attr)
        self.assertEqual(sorted_tables, expected_tables)

    def test_rename_table(self):
        # pylint: disable=no-name-in-module
        from grpc.beta import interfaces
        from grpc.framework.interfaces.face import face
        # pylint: enable=no-name-in-module

        temp_table_id = 'foo-bar-baz-table'
        temp_table = Config.CLUSTER.table(temp_table_id)
        temp_table.create()
        self.tables_to_delete.append(temp_table)

        with self.assertRaises(face.LocalError) as exc_manager:
            temp_table.rename(temp_table_id + '-alt')
        exc_caught = exc_manager.exception
        self.assertNotEqual(exc_caught, None)
        self.assertEqual(exc_caught.code,
                         interfaces.StatusCode.UNIMPLEMENTED)
        self.assertEqual(
            exc_caught.details,
            'BigtableTableService.RenameTable is not yet implemented')

    def test_create_column_family(self):
        temp_table_id = 'foo-bar-baz-table'
        temp_table = Config.CLUSTER.table(temp_table_id)
        temp_table.create()
        self.tables_to_delete.append(temp_table)

        self.assertEqual(temp_table.list_column_families(), {})
        gc_rule = MaxVersionsGCRule(1)
        column_family = temp_table.column_family(COLUMN_FAMILY_ID1,
                                                 gc_rule=gc_rule)
        column_family.create()

        col_fams = temp_table.list_column_families()

        self.assertEqual(len(col_fams), 1)
        retrieved_col_fam = col_fams[COLUMN_FAMILY_ID1]
        self.assertTrue(retrieved_col_fam._table is column_family._table)
        self.assertEqual(retrieved_col_fam.column_family_id,
                         column_family.column_family_id)
        self.assertEqual(retrieved_col_fam.gc_rule, gc_rule)

    def test_update_column_family(self):
        temp_table_id = 'foo-bar-baz-table'
        temp_table = Config.CLUSTER.table(temp_table_id)
        temp_table.create()
        self.tables_to_delete.append(temp_table)

        gc_rule = MaxVersionsGCRule(1)
        column_family = temp_table.column_family(COLUMN_FAMILY_ID1,
                                                 gc_rule=gc_rule)
        column_family.create()

        # Check that our created table is as expected.
        col_fams = temp_table.list_column_families()
        self.assertEqual(col_fams, {COLUMN_FAMILY_ID1: column_family})

        # Update the column family's GC rule and then try to update.
        column_family.gc_rule = None
        column_family.update()

        # Check that the update has propagated.
        col_fams = temp_table.list_column_families()
        self.assertEqual(col_fams[COLUMN_FAMILY_ID1].gc_rule, None)

    def test_delete_column_family(self):
        temp_table_id = 'foo-bar-baz-table'
        temp_table = Config.CLUSTER.table(temp_table_id)
        temp_table.create()
        self.tables_to_delete.append(temp_table)

        self.assertEqual(temp_table.list_column_families(), {})
        column_family = temp_table.column_family(COLUMN_FAMILY_ID1)
        column_family.create()

        # Make sure the family is there before deleting it.
        col_fams = temp_table.list_column_families()
        self.assertEqual(list(col_fams.keys()), [COLUMN_FAMILY_ID1])

        column_family.delete()
        # Make sure we have successfully deleted it.
        self.assertEqual(temp_table.list_column_families(), {})


class TestDataAPI(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._table = table = Config.CLUSTER.table(TABLE_ID)
        table.create()
        table.column_family(COLUMN_FAMILY_ID1).create()
        table.column_family(COLUMN_FAMILY_ID2).create()

    @classmethod
    def tearDownClass(cls):
        # Will also delete any data contained in the table.
        cls._table.delete()

    def setUp(self):
        self.rows_to_delete = []

    def tearDown(self):
        for row in self.rows_to_delete:
            row.clear()
            row.delete()
            row.commit()

    def _write_to_row(self, row1=None, row2=None, row3=None, row4=None):
        timestamp1 = datetime.datetime.utcnow().replace(tzinfo=UTC)
        timestamp1_micros = _microseconds_from_datetime(timestamp1)
        # Truncate to millisecond granularity.
        timestamp1_micros -= (timestamp1_micros % 1000)
        timestamp1 = _datetime_from_microseconds(timestamp1_micros)
        # 1000 microseconds is a millisecond
        timestamp2 = timestamp1 + datetime.timedelta(microseconds=1000)
        timestamp3 = timestamp1 + datetime.timedelta(microseconds=2000)
        timestamp4 = timestamp1 + datetime.timedelta(microseconds=3000)
        if row1 is not None:
            row1.set_cell(COLUMN_FAMILY_ID1, COL_NAME1, CELL_VAL1,
                          timestamp=timestamp1)
        if row2 is not None:
            row2.set_cell(COLUMN_FAMILY_ID1, COL_NAME1, CELL_VAL2,
                          timestamp=timestamp2)
        if row3 is not None:
            row3.set_cell(COLUMN_FAMILY_ID1, COL_NAME2, CELL_VAL3,
                          timestamp=timestamp3)
        if row4 is not None:
            row4.set_cell(COLUMN_FAMILY_ID2, COL_NAME3, CELL_VAL4,
                          timestamp=timestamp4)

        # Create the cells we will check.
        cell1 = Cell(CELL_VAL1, timestamp1)
        cell2 = Cell(CELL_VAL2, timestamp2)
        cell3 = Cell(CELL_VAL3, timestamp3)
        cell4 = Cell(CELL_VAL4, timestamp4)
        return cell1, cell2, cell3, cell4

    def test_read_row(self):
        row = self._table.row(ROW_KEY)
        self.rows_to_delete.append(row)

        cell1, cell2, cell3, cell4 = self._write_to_row(row, row, row, row)
        row.commit()

        # Read back the contents of the row.
        partial_row_data = self._table.read_row(ROW_KEY)
        self.assertTrue(partial_row_data.committed)
        self.assertEqual(partial_row_data.row_key, ROW_KEY)

        # Check the cells match.
        ts_attr = operator.attrgetter('timestamp')
        expected_row_contents = {
            COLUMN_FAMILY_ID1: {
                COL_NAME1: sorted([cell1, cell2], key=ts_attr, reverse=True),
                COL_NAME2: [cell3],
            },
            COLUMN_FAMILY_ID2: {
                COL_NAME3: [cell4],
            },
        }
        self.assertEqual(partial_row_data.cells, expected_row_contents)

    def test_read_rows(self):
        row = self._table.row(ROW_KEY)
        row_alt = self._table.row(ROW_KEY_ALT)
        self.rows_to_delete.extend([row, row_alt])

        cell1, cell2, cell3, cell4 = self._write_to_row(row, row_alt,
                                                        row, row_alt)
        row.commit()
        row_alt.commit()

        rows_data = self._table.read_rows()
        self.assertEqual(rows_data.rows, {})
        rows_data.consume_all()

        # NOTE: We should refrain from editing protected data on instances.
        #       Instead we should make the values public or provide factories
        #       for constructing objects with them.
        row_data = PartialRowData(ROW_KEY)
        row_data._chunks_encountered = True
        row_data._committed = True
        row_data._cells = {
            COLUMN_FAMILY_ID1: {
                COL_NAME1: [cell1],
                COL_NAME2: [cell3],
            },
        }

        row_alt_data = PartialRowData(ROW_KEY_ALT)
        row_alt_data._chunks_encountered = True
        row_alt_data._committed = True
        row_alt_data._cells = {
            COLUMN_FAMILY_ID1: {
                COL_NAME1: [cell2],
            },
            COLUMN_FAMILY_ID2: {
                COL_NAME3: [cell4],
            },
        }

        expected_rows = {
            ROW_KEY: row_data,
            ROW_KEY_ALT: row_alt_data,
        }
        self.assertEqual(rows_data.rows, expected_rows)

    def test_read_with_label_applied(self):
        row = self._table.row(ROW_KEY)
        self.rows_to_delete.append(row)

        cell1, _, cell3, _ = self._write_to_row(row, None, row)
        row.commit()

        # Combine a label with column 1.
        label1 = u'label-red'
        label1_filter = ApplyLabelFilter(label1)
        col1_filter = ColumnQualifierRegexFilter(COL_NAME1)
        chain1 = RowFilterChain(filters=[col1_filter, label1_filter])

        # Combine a label with column 2.
        label2 = u'label-blue'
        label2_filter = ApplyLabelFilter(label2)
        col2_filter = ColumnQualifierRegexFilter(COL_NAME2)
        chain2 = RowFilterChain(filters=[col2_filter, label2_filter])

        # Bring our two labeled columns together.
        row_filter = RowFilterUnion(filters=[chain1, chain2])
        partial_row_data = self._table.read_row(ROW_KEY, filter_=row_filter)
        self.assertTrue(partial_row_data.committed)
        self.assertEqual(partial_row_data.row_key, ROW_KEY)

        cells_returned = partial_row_data.cells
        col_fam1 = cells_returned.pop(COLUMN_FAMILY_ID1)
        # Make sure COLUMN_FAMILY_ID1 was the only key.
        self.assertEqual(len(cells_returned), 0)

        cell1_new, = col_fam1.pop(COL_NAME1)
        cell3_new, = col_fam1.pop(COL_NAME2)
        # Make sure COL_NAME1 and COL_NAME2 were the only keys.
        self.assertEqual(len(col_fam1), 0)

        # Check that cell1 has matching values and gained a label.
        self.assertEqual(cell1_new.value, cell1.value)
        self.assertEqual(cell1_new.timestamp, cell1.timestamp)
        self.assertEqual(cell1.labels, [])
        self.assertEqual(cell1_new.labels, [label1])

        # Check that cell3 has matching values and gained a label.
        self.assertEqual(cell3_new.value, cell3.value)
        self.assertEqual(cell3_new.timestamp, cell3.timestamp)
        self.assertEqual(cell3.labels, [])
        self.assertEqual(cell3_new.labels, [label2])
