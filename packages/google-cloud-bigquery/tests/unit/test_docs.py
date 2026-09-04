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

import pathlib
import runpy


def test_docs_conf_executes_successfully():
    docs_dir = pathlib.Path(__file__).parent.parent.parent / "docs"
    conf_path = docs_dir / "conf.py"

    if not conf_path.exists():
        import pytest
        pytest.skip("docs/conf.py not found")

    res = runpy.run_path(str(conf_path))

    assert "project" in res
    assert res["project"] == "google-cloud-bigquery"
