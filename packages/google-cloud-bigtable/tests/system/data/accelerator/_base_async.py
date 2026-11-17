# Copyright 2026 Google LLC
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

import pytest

from google.cloud.bigtable.data._accelerator import _daemon
from google.cloud.bigtable.data._cross_sync import CrossSync
from google.cloud.bigtable.data.mutations import DeleteAllFromRow, RowMutationEntry

from .. import SystemTestRunner
from . import _harness

__CROSS_SYNC_OUTPUT__ = "tests.system.data.accelerator._base_autogen"


@CrossSync.convert_class(sync_name="AcceleratorTestBase")
class AcceleratorTestBaseAsync(SystemTestRunner):
    @pytest.fixture(scope="session", autouse=True)
    def _require_accel_env(self):
        _harness.require_real_bigtable_or_skip()
        path = _harness.require_binary_or_skip()
        orig_resolve = _daemon._resolve_binary_path
        if _harness.SETTINGS.accelerator_bin:
            _daemon._resolve_binary_path = lambda: path
        try:
            yield
        finally:
            _daemon._resolve_binary_path = orig_resolve

    @pytest.fixture(scope="session")
    @classmethod
    def column_family_config(cls):
        from google.cloud.bigtable_admin_v2 import types

        gc_rule = types.GcRule(max_age=datetime.timedelta(days=1))
        int_aggregate_type = types.Type.Aggregate(
            input_type=types.Type(int64_type={"encoding": {"big_endian_bytes": {}}}),
            sum={},
        )
        return {
            _harness.TEST_FAMILY: types.ColumnFamily(gc_rule=gc_rule),
            _harness.TEST_FAMILY_2: types.ColumnFamily(gc_rule=gc_rule),
            _harness.TEST_AGGREGATE_FAMILY: types.ColumnFamily(
                gc_rule=gc_rule,
                value_type=types.Type(aggregate_type=int_aggregate_type),
            ),
        }

    @classmethod
    def _ensure_table(
        cls,
        admin_client,
        project_id,
        instance_id,
        table_id,
        column_family_config,
        column_split_config,
    ):
        from google.api_core import exceptions
        from google.cloud.bigtable.data import BigtableDataClient, ReadRowsQuery

        assert len(table_id) <= 50
        with BigtableDataClient(
            project=project_id, use_accelerator=False
        ) as probe_client:
            with probe_client.get_table(instance_id, table_id) as probe_table:
                try:
                    probe_table.read_rows(ReadRowsQuery(limit=1))
                    return table_id
                except exceptions.NotFound:
                    pass
        parent_path = f"projects/{project_id}/instances/{instance_id}"
        try:
            admin_client.table_admin_client.create_table(
                request={
                    "parent": parent_path,
                    "table_id": table_id,
                    "table": {"column_families": column_family_config},
                    "initial_splits": [{"key": key} for key in column_split_config],
                },
            )
        except exceptions.AlreadyExists:
            pass
        return table_id

    @pytest.fixture(scope="session")
    @classmethod
    def table_id(
        cls,
        admin_client,
        project_id,
        instance_id,
        column_family_config,
        column_split_config,
    ):
        yield cls._ensure_table(
            admin_client,
            project_id,
            instance_id,
            _harness.SETTINGS.table_id,
            column_family_config,
            column_split_config,
        )

    @pytest.fixture(scope="session")
    @classmethod
    def second_table_id(
        cls,
        admin_client,
        project_id,
        instance_id,
        column_family_config,
        column_split_config,
    ):
        yield cls._ensure_table(
            admin_client,
            project_id,
            instance_id,
            _harness.SETTINGS.second_table_id,
            column_family_config,
            column_split_config,
        )

    def _project_id(self):
        return _harness.SETTINGS.project_id

    def _make_client(self, use_accelerator=None, **kwargs):
        return CrossSync.DataClient(
            project=self._project_id(), use_accelerator=use_accelerator, **kwargs
        )

    def assert_accelerator_active(self, table):
        assert table._accelerator_client is not None, (
            "expected the accelerator to be active (use_accelerator=True) but the "
            "target fell back to native. Check ADC principal / identity "
            "verification and that the bundled daemon binary can start."
        )

    def assert_native(self, table):
        assert table._accelerator_client is None, (
            "expected a native target (use_accelerator=False) but an accelerator "
            "client was attached."
        )

    @CrossSync.convert
    @CrossSync.pytest_fixture(scope="session")
    async def client(self):
        async with self._make_client() as client:
            yield client

    @CrossSync.convert
    @CrossSync.pytest_fixture(scope="session")
    async def accel_client(self):
        async with self._make_client(use_accelerator=True) as client:
            yield client

    @CrossSync.convert
    @CrossSync.pytest_fixture(scope="session")
    async def native_client(self):
        async with self._make_client(use_accelerator=False) as client:
            yield client

    @CrossSync.convert
    @CrossSync.pytest_fixture(scope="session")
    async def accel_table(self, accel_client, instance_id, table_id):
        async with accel_client.get_table(instance_id, table_id) as table:
            self.assert_accelerator_active(table)
            yield table

    @CrossSync.convert
    @CrossSync.pytest_fixture(scope="session")
    async def native_table(self, native_client, instance_id, table_id):
        async with native_client.get_table(instance_id, table_id) as table:
            self.assert_native(table)
            yield table

    @CrossSync.convert
    @CrossSync.pytest_fixture(scope="session")
    async def default_table(self, client, instance_id, table_id):
        async with client.get_table(instance_id, table_id) as table:
            yield table

    @CrossSync.convert
    @CrossSync.pytest_fixture(scope="function")
    async def janitor(self, native_table):
        class _Janitor:
            def __init__(self):
                self.keys = set()

            def track(self, key):
                self.keys.add(key)
                return key

        j = _Janitor()
        yield j
        if j.keys:
            entries = [RowMutationEntry(key, [DeleteAllFromRow()]) for key in j.keys]
            await native_table.bulk_mutate_rows(entries)
