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

from gapic.codegen.writer import CodeWriter
from gapic.schema.api import API


class PackageInitGenerator:
    """Pure Python generator for package initialization files (__init__.py, gapic_version.py, py.typed)."""

    @staticmethod
    def generate_gapic_version(api_schema: API) -> str:
        """Generates gapic_version.py content."""
        writer = CodeWriter()
        writer.write_license_header()
        writer.write_line(f'__version__ = "{api_schema.gapic_version}"  # {{x-release-please-version}}')
        return writer.dump()

    @staticmethod
    def generate_py_typed(api_schema: API) -> str:
        """Generates py.typed file (PEP 561 marker)."""
        pkg_name = api_schema.naming.warehouse_package_name
        return f"# Marker file for PEP 561.\n# The {pkg_name} package uses inline types.\n"
