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

"""Unit tests for versionless import."""


def test_shim():
    from google.cloud import bigquery_datatransfer, bigquery_datatransfer_v1

    assert sorted(bigquery_datatransfer.__all__) == sorted(
        bigquery_datatransfer_v1.__all__
    )

    for name in bigquery_datatransfer.__all__:
        found = getattr(bigquery_datatransfer, name)
        expected = getattr(bigquery_datatransfer_v1, name)
        assert found is expected
