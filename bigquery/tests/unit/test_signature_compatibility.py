# Copyright 2019 Google LLC
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

import inspect

import pytest


@pytest.fixture
def query_job_class():
    from google.cloud.bigquery.job import QueryJob

    return QueryJob


@pytest.fixture
def row_iterator_class():
    from google.cloud.bigquery.table import RowIterator

    return RowIterator


@pytest.mark.skipif(
    not hasattr(inspect, "signature"),
    reason="inspect.signature() is not availalbe in older Python versions",
)
def test_to_arrow_method_signatures_match(query_job_class, row_iterator_class):
    sig = inspect.signature(query_job_class.to_arrow)
    sig2 = inspect.signature(row_iterator_class.to_arrow)
    assert sig == sig2


@pytest.mark.skipif(
    not hasattr(inspect, "signature"),
    reason="inspect.signature() is not availalbe in older Python versions",
)
def test_to_dataframe_method_signatures_match(query_job_class, row_iterator_class):
    sig = inspect.signature(query_job_class.to_dataframe)
    sig2 = inspect.signature(row_iterator_class.to_dataframe)
    assert sig == sig2
