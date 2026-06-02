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

import os
from datetime import datetime, timedelta, timezone

from google.api_core.exceptions import NotFound
from google.cloud import bigtable_admin_v2 as admin_v2


def clear_stale_instances(project_id: str, prefix: str, older_than_days: int = 1):
    """
    Synchronously deletes any instances in the given project that are older
    than older_than_days and whose name or display name matches the given prefix.
    """
    client = admin_v2.BigtableInstanceAdminClient(
        client_options={"quota_project_id": project_id}
    )
    parent = client.common_project_path(project_id)
    next_page_token = ""

    while True:
        try:
            response = client.list_instances(
                request={"parent": parent, "page_token": next_page_token}
            )
        except Exception:
            # Cannot list instances, skip cleanup
            break

        for instance in response.instances:
            # Check if instance matches the prefix
            display_name_matches = instance.display_name.startswith(prefix)
            name_matches = instance.name.split("/")[-1].startswith(prefix)

            if display_name_matches or name_matches:
                if instance.create_time:
                    now = datetime.now(timezone.utc)
                    if now - instance.create_time > timedelta(days=older_than_days):
                        try:
                            client.delete_instance(name=instance.name)
                        except NotFound:
                            pass

        next_page_token = response.next_page_token
        if not next_page_token:
            break
