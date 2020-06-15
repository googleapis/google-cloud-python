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
import sys
import warnings

from google.cloud.bigtable_admin_v2 import types
from google.cloud.bigtable_admin_v2.gapic import bigtable_instance_admin_client
from google.cloud.bigtable_admin_v2.gapic import bigtable_table_admin_client
from google.cloud.bigtable_admin_v2.gapic import enums


if sys.version_info[:2] == (2, 7):
    message = (
        "A future version of this library will drop support for Python 2.7. "
        "More details about Python 2 support for Google Cloud Client Libraries "
        "can be found at https://cloud.google.com/python/docs/python2-sunset/"
    )
    warnings.warn(message, DeprecationWarning)


class BigtableInstanceAdminClient(
    bigtable_instance_admin_client.BigtableInstanceAdminClient
):
    __doc__ = bigtable_instance_admin_client.BigtableInstanceAdminClient.__doc__
    enums = enums


class BigtableTableAdminClient(bigtable_table_admin_client.BigtableTableAdminClient):
    __doc__ = bigtable_table_admin_client.BigtableTableAdminClient.__doc__
    enums = enums


__all__ = (
    "enums",
    "types",
    "BigtableInstanceAdminClient",
    "BigtableTableAdminClient",
)
