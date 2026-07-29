# Copyright 2025 Google LLC
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

"""Helpers for working across versions of different depenencies."""

from typing import List

import pyarrow


def pyarrow_struct_type_fields(struct_type: pyarrow.StructType) -> List[pyarrow.Field]:
    """StructType.fields was added in pyarrow 18.

    See: https://arrow.apache.org/docs/18.0/python/generated/pyarrow.StructType.html
    """

    if hasattr(struct_type, "fields"):
        return struct_type.fields

    return [
        struct_type.field(field_index) for field_index in range(struct_type.num_fields)
    ]
