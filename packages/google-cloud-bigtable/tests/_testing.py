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

from google.cloud.bigtable_v2.types.data import ProtoRows, Value as PBValue


TYPE_INT = {
    "int64_type": {
        "encoding": {"big_endian_bytes": {"bytes_type": {"encoding": {"raw": {}}}}}
    }
}


def proto_rows_bytes(*args):
    return ProtoRows.serialize(ProtoRows(values=[PBValue(**arg) for arg in args]))


def split_bytes_into_chunks(bytes_to_split, num_chunks):
    from google.cloud.bigtable.helpers import batched

    assert num_chunks <= len(bytes_to_split)
    bytes_per_part = (len(bytes_to_split) - 1) // num_chunks + 1
    result = list(map(bytes, batched(bytes_to_split, bytes_per_part)))
    assert len(result) == num_chunks
    return result
