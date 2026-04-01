# Copyright 2026 Google LLC
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

import pytest

import bigframes.bigquery as bbq


@pytest.fixture()
def objectrefs(bq_connection):
    return bbq.obj.make_ref(
        [
            "gs://cloud-samples-data/bigquery/tutorials/cymbal-pets/images/tick-terminator-for-dogs.png"
        ],
        bq_connection,
    )


def test_obj_fetch_metadata(objectrefs):
    metadata = bbq.obj.fetch_metadata(objectrefs)

    result = metadata.to_pandas()
    assert len(result) == len(objectrefs)


def test_obj_get_access_url(objectrefs):
    access = bbq.obj.get_access_url(objectrefs, "r")

    result = access.to_pandas()
    assert len(result) == len(objectrefs)
