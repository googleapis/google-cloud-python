# Copyright 2024 Google LLC
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

# This script create the bigtable resources required for
# bigframes.streaming testing if they don't already exist

import os
import sys

from google.cloud.bigtable import column_family
import google.cloud.bigtable as bigtable

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")

if not PROJECT_ID:
    print(
        "Please set GOOGLE_CLOUD_PROJECT environment variable before running.",
        file=sys.stderr,
    )
    sys.exit(1)


def create_instance(client):
    instance_name = "streaming-testing-instance"
    instance = bigtable.instance.Instance(
        instance_name,
        client,
    )
    cluster_id = "streaming-testing-instance-c1"
    cluster = instance.cluster(
        cluster_id,
        location_id="us-west1-a",
        serve_nodes=1,
    )
    if not instance.exists():
        operation = instance.create(
            clusters=[cluster],
        )
        operation.result(timeout=480)
        print(f"Created instance {instance_name}")
    return instance


def create_table(instance):
    table_id = "table-testing"
    table = bigtable.table.Table(
        table_id,
        instance,
    )
    max_versions_rule = column_family.MaxVersionsGCRule(1)
    column_family_id = "body_mass_g"
    column_families = {column_family_id: max_versions_rule}
    if not table.exists():
        table.create(column_families=column_families)
        print(f"Created table {table_id}")


def main():
    client = bigtable.Client(project=PROJECT_ID, admin=True)

    instance = create_instance(client)
    create_table(instance)


if __name__ == "__main__":
    main()
