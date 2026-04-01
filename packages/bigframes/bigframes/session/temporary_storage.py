# Copyright 2024 Google LLC
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

from typing import Protocol, Sequence

from google.cloud import bigquery


class TemporaryStorageManager(Protocol):
    @property
    def location(self) -> str:
        ...

    def create_temp_table(
        self, schema: Sequence[bigquery.SchemaField], cluster_cols: Sequence[str] = []
    ) -> bigquery.TableReference:
        ...

    # implementations should be robust to repeatedly closing
    def close(self) -> None:
        ...
