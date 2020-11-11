# Copyright 2017 Google LLC All rights reserved.
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
        from google.cloud.spanner_v1 import Type
        from google.cloud.spanner_v1 import TypeCode
        from google.cloud.spanner_v1 import param_types

        expected = Type(
            code=TypeCode.ARRAY, array_element_type=Type(code=TypeCode.INT64)
        )

        found = param_types.Array(param_types.INT64)

        self.assertEqual(found, expected)


class Test_Struct(unittest.TestCase):
    def test_it(self):
        from google.cloud.spanner_v1 import Type
        from google.cloud.spanner_v1 import TypeCode
        from google.cloud.spanner_v1 import StructType
        from google.cloud.spanner_v1 import param_types

        struct_type = StructType(
            fields=[
                StructType.Field(name="name", type_=Type(code=TypeCode.STRING)),
                StructType.Field(name="count", type_=Type(code=TypeCode.INT64)),
            ]
        )
        expected = Type(code=TypeCode.STRUCT, struct_type=struct_type)

        found = param_types.Struct(
            [
                param_types.StructField("name", param_types.STRING),
                param_types.StructField("count", param_types.INT64),
            ]
        )

        self.assertEqual(found, expected)
