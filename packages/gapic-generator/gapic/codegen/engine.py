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

from typing import Any, Optional
from gapic.codegen.components.package_init import PackageInitGenerator


class PurePythonEngine:
    """Pure-Python template-free code generation engine."""

    @staticmethod
    def render(template_name: str, context: dict[str, Any]) -> Optional[str]:
        """Dispatches template rendering to pure-Python component generators.

        Returns None to fall back to Jinja rendering if the template is not yet migrated.
        """
        api_schema = context.get("api")
        if not api_schema:
            return None

        # Package Init & Versioning Component
        if template_name.endswith("gapic_version.py.j2"):
            return PackageInitGenerator.generate_gapic_version(api_schema)
        if template_name.endswith("py.typed.j2"):
            return PackageInitGenerator.generate_py_typed(api_schema)

        # Fallback to Jinja for un-migrated templates
        return None
