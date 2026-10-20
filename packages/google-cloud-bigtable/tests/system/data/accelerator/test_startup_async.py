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
import time
import pytest
from google.cloud.bigtable.data._cross_sync import CrossSync
from . import _harness
if CrossSync.is_async:
    from ._base_async import AcceleratorTestBaseAsync as AcceleratorTestBase
else:
    from ._base_autogen import AcceleratorTestBase
__CROSS_SYNC_OUTPUT__ = "tests.system.data.accelerator.test_startup_autogen"


@CrossSync.convert_class(sync_name="TestStartup")
class TestStartupAsync(AcceleratorTestBase):
    @CrossSync.pytest
    async def test_slow_bind_waits_then_falls_back(self, tmp_bin_dir, instance_id, table_id, monkeypatch):
        _harness.slow_bind_binary(tmp_bin_dir, 1.5, monkeypatch=monkeypatch)
        t0 = time.monotonic()
        async with self._make_client() as client:
            with pytest.warns(RuntimeWarning):
                table = client.get_table(instance_id, table_id)
            async with table:
                assert time.monotonic() - t0 >= 0.75 and table._accelerator_client is None
