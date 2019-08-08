# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
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
"""System tests for reading rows from tables."""

import os

import pytest

from google.cloud import bigquery_storage_v1beta1


@pytest.fixture()
def project_id():
    return os.environ["PROJECT_ID"]


@pytest.fixture()
def client():
    return bigquery_storage_v1beta1.BigQueryStorageClient()


@pytest.fixture()
def table_reference():
    table_ref = bigquery_storage_v1beta1.types.TableReference()
    table_ref.project_id = "bigquery-public-data"
    table_ref.dataset_id = "usa_names"
    table_ref.table_id = "usa_1910_2013"
    return table_ref


@pytest.fixture()
def small_table_reference():
    table_ref = bigquery_storage_v1beta1.types.TableReference()
    table_ref.project_id = "bigquery-public-data"
    table_ref.dataset_id = "utility_us"
    table_ref.table_id = "country_code_iso"
    return table_ref
