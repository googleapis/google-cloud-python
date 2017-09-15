# Copyright 2017 Google Inc. All rights reserved.
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


import unittest


class Test_ArrayParamType(unittest.TestCase):

    def test_it(self):
        from google.cloud.proto.spanner.v1 import type_pb2
        from google.cloud.spanner.types import ArrayParamType
        from google.cloud.spanner.types import INT64_PARAM_TYPE

        expected = type_pb2.Type(
            code=type_pb2.ARRAY,
            array_element_type=type_pb2.Type(code=type_pb2.INT64))

        found = ArrayParamType(INT64_PARAM_TYPE)

        self.assertEqual(found, expected)


class Test_Struct(unittest.TestCase):

    def test_it(self):
        from google.cloud.proto.spanner.v1 import type_pb2
        from google.cloud.spanner.types import INT64_PARAM_TYPE
        from google.cloud.spanner.types import STRING_PARAM_TYPE
        from google.cloud.spanner.types import StructParamType
        from google.cloud.spanner.types import StructField

        struct_type = type_pb2.StructType(fields=[
            type_pb2.StructType.Field(
                name='name',
                type=type_pb2.Type(code=type_pb2.STRING)),
            type_pb2.StructType.Field(
                name='count',
                type=type_pb2.Type(code=type_pb2.INT64)),
        ])
        expected = type_pb2.Type(
            code=type_pb2.STRUCT,
            struct_type=struct_type)

        found = StructParamType([
            StructField('name', STRING_PARAM_TYPE),
            StructField('count', INT64_PARAM_TYPE),
        ])

        self.assertEqual(found, expected)
