# Copyright 2023 Google LLC
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

from ibis.backends.bigquery import datatypes as bq_types
from ibis.expr import datatypes as ibis_types

from bigframes import remote_function as rf


def test_supported_types_correspond():
    # The same types should be representable by the supported Python and BigQuery types.
    ibis_types_from_python = {ibis_types.dtype(t) for t in rf.SUPPORTED_IO_PYTHON_TYPES}
    ibis_types_from_bigquery = {
        bq_types.BigQueryType.to_ibis(tk) for tk in rf.SUPPORTED_IO_BIGQUERY_TYPEKINDS
    }

    assert ibis_types_from_python == ibis_types_from_bigquery
