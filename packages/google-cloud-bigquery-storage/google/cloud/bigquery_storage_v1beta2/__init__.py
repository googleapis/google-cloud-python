# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
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

from __future__ import absolute_import

from google.cloud.bigquery_storage_v1beta2 import gapic_version as package_version

__version__ = package_version.__version__

from google.cloud.bigquery_storage_v1beta2 import client, types


class BigQueryReadClient(client.BigQueryReadClient):
    __doc__ = client.BigQueryReadClient.__doc__


class BigQueryWriteClient(client.BigQueryWriteClient):
    __doc__ = client.BigQueryWriteClient.__doc__


__all__ = (
    # google.cloud.bigquery_storage_v1beta2
    "__version__",
    "types",
    # google.cloud.bigquery_storage_v1beta2.client
    "BigQueryReadClient",
    "BigQueryWriteClient",
)
