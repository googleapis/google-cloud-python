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

import dataclasses
import typing

from bigframes import dtypes
from bigframes.operations import base_ops
import bigframes.operations.type as op_typing

ObjFetchMetadataOp = base_ops.create_unary_op(
    name="obj_fetch_metadata", type_signature=op_typing.BLOB_TRANSFORM
)
obj_fetch_metadata_op = ObjFetchMetadataOp()


@dataclasses.dataclass(frozen=True)
class ObjGetAccessUrl(base_ops.UnaryOp):
    name: typing.ClassVar[str] = "obj_get_access_url"
    mode: str  # access mode, e.g. R read, W write, RW read & write

    def output_type(self, *input_types):
        return dtypes.JSON_DTYPE


@dataclasses.dataclass(frozen=True)
class ObjMakeRef(base_ops.BinaryOp):
    name: typing.ClassVar[str] = "obj.make_ref"

    def output_type(self, *input_types):
        if not all(map(dtypes.is_string_like, input_types)):
            raise TypeError("obj.make_ref requires string-like arguments")

        return dtypes.OBJ_REF_DTYPE


obj_make_ref_op = ObjMakeRef()
