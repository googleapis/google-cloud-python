# Copyright 2021 Google LLC
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

from google.cloud import datastore
from google.cloud.datastore.client import DATASTORE_DATASET
from test_utils.system import unique_resource_id

EMULATOR_DATASET = os.getenv(DATASTORE_DATASET)


def unique_id(prefix, separator="-"):
    return f"{prefix}{unique_resource_id(separator)}"


_SENTINEL = object()


def clone_client(base_client, namespace=_SENTINEL):
    if namespace is _SENTINEL:
        namespace = base_client.namespace

    kwargs = {}
    if EMULATOR_DATASET is None:
        kwargs["credentials"] = base_client._credentials

    return datastore.Client(
        project=base_client.project,
        namespace=namespace,
        _http=base_client._http,
        **kwargs,
    )
