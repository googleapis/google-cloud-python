# Copyright 2024, Google LLC
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import uuid

from .instanceadmin import (
    add_cluster,
    delete_cluster,
    delete_instance,
    run_instance_operations,
)

PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
INSTANCE_ID = f"instance-admin-{str(uuid.uuid4())[:16]}"
CLUSTER_ID = f"cluster-admin-{str(uuid.uuid4())[:16]}"
NEW_CLUSTER_ID = f"cluster-add-{str(uuid.uuid4())[:16]}"


def test_instance_operations(capsys):
    run_instance_operations(PROJECT, INSTANCE_ID, CLUSTER_ID)
    out, _ = capsys.readouterr()
    assert f"Created instance: {INSTANCE_ID}" in out
    assert "Listing instances:" in out
    assert "Listing clusters..." in out

    add_cluster(PROJECT, INSTANCE_ID, NEW_CLUSTER_ID)
    out, _ = capsys.readouterr()
    assert f"Cluster created: {NEW_CLUSTER_ID}" in out

    delete_cluster(PROJECT, INSTANCE_ID, NEW_CLUSTER_ID)
    out, _ = capsys.readouterr()
    assert f"Cluster deleted: {NEW_CLUSTER_ID}" in out

    delete_instance(PROJECT, INSTANCE_ID)
    out, _ = capsys.readouterr()
    assert f"Deleted instance: {INSTANCE_ID}" in out
