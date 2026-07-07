# Copyright 2026 Google LLC
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

from unittest.mock import MagicMock
from gapic.codegen.components.package_init import PackageInitGenerator


def test_generate_gapic_version():
    mock_api = MagicMock()
    mock_api.gapic_version = "0.1.0"
    content = PackageInitGenerator.generate_gapic_version(mock_api)
    
    assert "# Copyright 2026 Google LLC" in content
    assert '__version__ = "0.1.0"  # {x-release-please-version}' in content


def test_generate_py_typed():
    mock_api = MagicMock()
    mock_api.naming.warehouse_package_name = "google-iam-credentials"
    content = PackageInitGenerator.generate_py_typed(mock_api)
    assert "# Marker file for PEP 561." in content
    assert "google-iam-credentials" in content


def test_pure_python_engine_render():
    from gapic.codegen.engine import PurePythonEngine

    assert PurePythonEngine.render("gapic_version.py.j2", {}) is None

    mock_api = MagicMock()
    mock_api.gapic_version = "0.1.0"
    mock_api.naming.warehouse_package_name = "google-iam-credentials"

    v_out = PurePythonEngine.render("gapic_version.py.j2", {"api": mock_api})
    assert '__version__ = "0.1.0"' in v_out

    t_out = PurePythonEngine.render("py.typed.j2", {"api": mock_api})
    assert "google-iam-credentials" in t_out

    assert PurePythonEngine.render("other_file.py.j2", {"api": mock_api}) is None
