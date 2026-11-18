# Copyright 2023 Google LLC
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
"""
Import pytest fixtures for setting up table for data client system tests
"""

import os
import sys

script_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(script_path)


def pytest_configure(config) -> None:
    """Clean up leaked test instances in the controller before workers start."""
    from google.cloud.environment_vars import BIGTABLE_EMULATOR

    if (
        os.getenv(BIGTABLE_EMULATOR)
        or getattr(config.option, "help", False)
        or getattr(config.option, "collectonly", False)
        or hasattr(config, "workerinput")
    ):
        return

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        try:
            import google.auth

            _, project_id = google.auth.default()
        except Exception:
            return

    if project_id:
        from utils import clear_stale_instances

        # Purge leaked test instances older than 1 hour before allocating nodes.
        clear_stale_instances(project_id, older_than_days=1 / 24, max_deletions=100)
