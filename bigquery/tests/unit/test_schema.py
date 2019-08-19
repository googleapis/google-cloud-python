# Copyright 2015 Google LLC
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

import mock


class TestSchemaField(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.schema import SchemaField

        return SchemaField

    @staticmethod
    def _get_standard_sql_data_type_class():
        from google.cloud.bigquery_v2 import types

        return types.StandardSqlDataType

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_constructor_defaults(self):
        field = self._make_one("test", "STRING")
        self.assertEqual(field._name, "test")
        self.assertEqual(field._field_type, "STRING")
        self.assertEqual(field._mode, "NULLABLE")
        self.assertIsNone(field._description)
        self.assertEqual(field._fields, ())

    def test_constructor_explicit(self):
        field = self._make_one("test", "STRING", mode="REQUIRED", description="Testing")
        self.assertEqual(field._name, "test")
        self.assertEqual(field._field_type, "STRING")
        self.assertEqual(field._mode, "REQUIRED")
        self.assertEqual(field._description, "Testing")
        self.assertEqual(field._fields, ())

    def test_constructor_subfields(self):
        sub_field1 = self._make_one("area_code", "STRING")
        sub_field2 = self._make_one("local_number", "STRING")
        field = self._make_one(
            "phone_number", "RECORD", fields=[sub_field1, sub_field2]
        )
        self.assertEqual(field._name, "phone_number")
        self.assertEqual(field._field_type, "RECORD")
        self.assertEqual(field._mode, "NULLABLE")
        self.assertIsNone(field._description)
        self.assertEqual(len(field._fields), 2)
        self.assertIs(field._fields[0], sub_field1)
        self.assertIs(field._fields[1], sub_field2)

    def test_to_api_repr(self):
        field = self._make_one("foo", "INTEGER", "NULLABLE")
        self.assertEqual(
            field.to_api_repr(),
            {"mode": "NULLABLE", "name": "foo", "type": "INTEGER", "description": None},
        )

    def test_to_api_repr_with_subfield(self):
        for record_type in ("RECORD", "STRUCT"):
            subfield = self._make_one("bar", "INTEGER", "NULLABLE")
            field = self._make_one("foo", record_type, "REQUIRED", fields=(subfield,))
            self.assertEqual(
                field.to_api_repr(),
                {
                    "fields": [
                        {
                            "mode": "NULLABLE",
                            "name": "bar",
                            "type": "INTEGER",
                            "description": None,
                        }
                    ],
                    "mode": "REQUIRED",
                    "name": "foo",
                    "type": record_type,
                    "description": None,
                },
            )

    def test_from_api_repr(self):
        field = self._get_target_class().from_api_repr(
            {
                "fields": [{"mode": "nullable", "name": "bar", "type": "integer"}],
                "mode": "required",
                "description": "test_description",
                "name": "foo",
                "type": "record",
            }
        )
        self.assertEqual(field.name, "foo")
        self.assertEqual(field.field_type, "RECORD")
        self.assertEqual(field.mode, "REQUIRED")
        self.assertEqual(field.description, "test_description")
        self.assertEqual(len(field.fields), 1)
        self.assertEqual(field.fields[0].name, "bar")
        self.assertEqual(field.fields[0].field_type, "INTEGER")
        self.assertEqual(field.fields[0].mode, "NULLABLE")

    def test_from_api_repr_defaults(self):
        field = self._get_target_class().from_api_repr(
            {"name": "foo", "type": "record"}
        )
        self.assertEqual(field.name, "foo")
        self.assertEqual(field.field_type, "RECORD")
        self.assertEqual(field.mode, "NULLABLE")
        self.assertEqual(field.description, None)
        self.assertEqual(len(field.fields), 0)

    def test_name_property(self):
        name = "lemon-ness"
        schema_field = self._make_one(name, "INTEGER")
        self.assertIs(schema_field.name, name)

    def test_field_type_property(self):
        field_type = "BOOLEAN"
        schema_field = self._make_one("whether", field_type)
        self.assertIs(schema_field.field_type, field_type)

    def test_mode_property(self):
        mode = "REPEATED"
        schema_field = self._make_one("again", "FLOAT", mode=mode)
        self.assertIs(schema_field.mode, mode)

    def test_is_nullable(self):
        mode = "NULLABLE"
        schema_field = self._make_one("test", "FLOAT", mode=mode)
        self.assertTrue(schema_field.is_nullable)

    def test_is_not_nullable(self):
        mode = "REPEATED"
        schema_field = self._make_one("test", "FLOAT", mode=mode)
        self.assertFalse(schema_field.is_nullable)

    def test_description_property(self):
        description = "It holds some data."
        schema_field = self._make_one("do", "TIMESTAMP", description=description)
        self.assertIs(schema_field.description, description)

    def test_fields_property(self):
        sub_field1 = self._make_one("one", "STRING")
        sub_field2 = self._make_one("fish", "INTEGER")
        fields = (sub_field1, sub_field2)
        schema_field = self._make_one("boat", "RECORD", fields=fields)
        self.assertIs(schema_field.fields, fields)

    def test_to_standard_sql_simple_type(self):
        sql_type = self._get_standard_sql_data_type_class()
        examples = (
            # a few legacy types
            ("INTEGER", sql_type.INT64),
            ("FLOAT", sql_type.FLOAT64),
            ("BOOLEAN", sql_type.BOOL),
            ("DATETIME", sql_type.DATETIME),
            # a few standard types
            ("INT64", sql_type.INT64),
            ("FLOAT64", sql_type.FLOAT64),
            ("BOOL", sql_type.BOOL),
            ("GEOGRAPHY", sql_type.GEOGRAPHY),
        )
        for legacy_type, standard_type in examples:
            field = self._make_one("some_field", legacy_type)
            standard_field = field.to_standard_sql()
            self.assertEqual(standard_field.name, "some_field")
            self.assertEqual(standard_field.type.type_kind, standard_type)
            self.assertFalse(standard_field.type.HasField("sub_type"))

    def test_to_standard_sql_struct_type(self):
        from google.cloud.bigquery_v2 import types

        # Expected result object:
        #
        # name: "image_usage"
        # type {
        #     type_kind: STRUCT
        #     struct_type {
        #         fields {
        #             name: "image_content"
        #             type {type_kind: BYTES}
        #         }
        #         fields {
        #             name: "last_used"
        #             type {
        #                 type_kind: STRUCT
        #                 struct_type {
        #                     fields {
        #                         name: "date_field"
        #                         type {type_kind: DATE}
        #                     }
        #                     fields {
        #                         name: "time_field"
        #                         type {type_kind: TIME}
        #                     }
        #                 }
        #             }
        #         }
        #     }
        # }

        sql_type = self._get_standard_sql_data_type_class()

        # level 2 fields
        sub_sub_field_date = types.StandardSqlField(
            name="date_field", type=sql_type(type_kind=sql_type.DATE)
        )
        sub_sub_field_time = types.StandardSqlField(
            name="time_field", type=sql_type(type_kind=sql_type.TIME)
        )

        # level 1 fields
        sub_field_struct = types.StandardSqlField(
            name="last_used", type=sql_type(type_kind=sql_type.STRUCT)
        )
        sub_field_struct.type.struct_type.fields.extend(
            [sub_sub_field_date, sub_sub_field_time]
        )
        sub_field_bytes = types.StandardSqlField(
            name="image_content", type=sql_type(type_kind=sql_type.BYTES)
        )

        # level 0 (top level)
        expected_result = types.StandardSqlField(
            name="image_usage", type=sql_type(type_kind=sql_type.STRUCT)
        )
        expected_result.type.struct_type.fields.extend(
            [sub_field_bytes, sub_field_struct]
        )

        # construct legacy SchemaField object
        sub_sub_field1 = self._make_one("date_field", "DATE")
        sub_sub_field2 = self._make_one("time_field", "TIME")
        sub_field_record = self._make_one(
            "last_used", "RECORD", fields=(sub_sub_field1, sub_sub_field2)
        )
        sub_field_bytes = self._make_one("image_content", "BYTES")

        for type_name in ("RECORD", "STRUCT"):
            schema_field = self._make_one(
                "image_usage", type_name, fields=(sub_field_bytes, sub_field_record)
            )
            standard_field = schema_field.to_standard_sql()
            self.assertEqual(standard_field, expected_result)

    def test_to_standard_sql_array_type_simple(self):
        from google.cloud.bigquery_v2 import types

        sql_type = self._get_standard_sql_data_type_class()

        # construct expected result object
        expected_sql_type = sql_type(type_kind=sql_type.ARRAY)
        expected_sql_type.array_element_type.type_kind = sql_type.INT64
        expected_result = types.StandardSqlField(
            name="valid_numbers", type=expected_sql_type
        )

        # construct "repeated" SchemaField object and convert to standard SQL
        schema_field = self._make_one("valid_numbers", "INT64", mode="REPEATED")
        standard_field = schema_field.to_standard_sql()

        self.assertEqual(standard_field, expected_result)

    def test_to_standard_sql_array_type_struct(self):
        from google.cloud.bigquery_v2 import types

        sql_type = self._get_standard_sql_data_type_class()

        # define person STRUCT
        name_field = types.StandardSqlField(
            name="name", type=sql_type(type_kind=sql_type.STRING)
        )
        age_field = types.StandardSqlField(
            name="age", type=sql_type(type_kind=sql_type.INT64)
        )
        person_struct = types.StandardSqlField(
            name="person_info", type=sql_type(type_kind=sql_type.STRUCT)
        )
        person_struct.type.struct_type.fields.extend([name_field, age_field])

        # define expected result - an ARRAY of person structs
        expected_sql_type = sql_type(
            type_kind=sql_type.ARRAY, array_element_type=person_struct.type
        )
        expected_result = types.StandardSqlField(
            name="known_people", type=expected_sql_type
        )

        # construct legacy repeated SchemaField object
        sub_field1 = self._make_one("name", "STRING")
        sub_field2 = self._make_one("age", "INTEGER")
        schema_field = self._make_one(
            "known_people", "RECORD", fields=(sub_field1, sub_field2), mode="REPEATED"
        )

        standard_field = schema_field.to_standard_sql()
        self.assertEqual(standard_field, expected_result)

    def test_to_standard_sql_unknown_type(self):
        sql_type = self._get_standard_sql_data_type_class()
        field = self._make_one("weird_field", "TROOLEAN")

        standard_field = field.to_standard_sql()

        self.assertEqual(standard_field.name, "weird_field")
        self.assertEqual(standard_field.type.type_kind, sql_type.TYPE_KIND_UNSPECIFIED)
        self.assertFalse(standard_field.type.HasField("sub_type"))

    def test___eq___wrong_type(self):
        field = self._make_one("test", "STRING")
        other = object()
        self.assertNotEqual(field, other)
        self.assertEqual(field, mock.ANY)

    def test___eq___name_mismatch(self):
        field = self._make_one("test", "STRING")
        other = self._make_one("other", "STRING")
        self.assertNotEqual(field, other)

    def test___eq___field_type_mismatch(self):
        field = self._make_one("test", "STRING")
        other = self._make_one("test", "INTEGER")
        self.assertNotEqual(field, other)

    def test___eq___mode_mismatch(self):
        field = self._make_one("test", "STRING", mode="REQUIRED")
        other = self._make_one("test", "STRING", mode="NULLABLE")
        self.assertNotEqual(field, other)

    def test___eq___description_mismatch(self):
        field = self._make_one("test", "STRING", description="Testing")
        other = self._make_one("test", "STRING", description="Other")
        self.assertNotEqual(field, other)

    def test___eq___fields_mismatch(self):
        sub1 = self._make_one("sub1", "STRING")
        sub2 = self._make_one("sub2", "STRING")
        field = self._make_one("test", "RECORD", fields=[sub1])
        other = self._make_one("test", "RECORD", fields=[sub2])
        self.assertNotEqual(field, other)

    def test___eq___hit(self):
        field = self._make_one("test", "STRING", mode="REQUIRED", description="Testing")
        other = self._make_one("test", "STRING", mode="REQUIRED", description="Testing")
        self.assertEqual(field, other)

    def test___eq___hit_case_diff_on_type(self):
        field = self._make_one("test", "STRING", mode="REQUIRED", description="Testing")
        other = self._make_one("test", "string", mode="REQUIRED", description="Testing")
        self.assertEqual(field, other)

    def test___eq___hit_w_fields(self):
        sub1 = self._make_one("sub1", "STRING")
        sub2 = self._make_one("sub2", "STRING")
        field = self._make_one("test", "RECORD", fields=[sub1, sub2])
        other = self._make_one("test", "RECORD", fields=[sub1, sub2])
        self.assertEqual(field, other)

    def test___ne___wrong_type(self):
        field = self._make_one("toast", "INTEGER")
        other = object()
        self.assertNotEqual(field, other)
        self.assertEqual(field, mock.ANY)

    def test___ne___same_value(self):
        field1 = self._make_one("test", "TIMESTAMP", mode="REPEATED")
        field2 = self._make_one("test", "TIMESTAMP", mode="REPEATED")
        # unittest ``assertEqual`` uses ``==`` not ``!=``.
        comparison_val = field1 != field2
        self.assertFalse(comparison_val)

    def test___ne___different_values(self):
        field1 = self._make_one(
            "test1", "FLOAT", mode="REPEATED", description="Not same"
        )
        field2 = self._make_one(
            "test2", "FLOAT", mode="NULLABLE", description="Knot saym"
        )
        self.assertNotEqual(field1, field2)

    def test___hash__set_equality(self):
        sub1 = self._make_one("sub1", "STRING")
        sub2 = self._make_one("sub2", "STRING")
        field1 = self._make_one("test", "RECORD", fields=[sub1])
        field2 = self._make_one("test", "RECORD", fields=[sub2])
        set_one = {field1, field2}
        set_two = {field1, field2}
        self.assertEqual(set_one, set_two)

    def test___hash__not_equals(self):
        sub1 = self._make_one("sub1", "STRING")
        sub2 = self._make_one("sub2", "STRING")
        field1 = self._make_one("test", "RECORD", fields=[sub1])
        field2 = self._make_one("test", "RECORD", fields=[sub2])
        set_one = {field1}
        set_two = {field2}
        self.assertNotEqual(set_one, set_two)

    def test___repr__(self):
        field1 = self._make_one("field1", "STRING")
        expected = "SchemaField('field1', 'STRING', 'NULLABLE', None, ())"
        self.assertEqual(repr(field1), expected)


# TODO: dedup with the same class in test_table.py.
class _SchemaBase(object):
    def _verify_field(self, field, r_field):
        self.assertEqual(field.name, r_field["name"])
        self.assertEqual(field.field_type, r_field["type"])
        self.assertEqual(field.mode, r_field.get("mode", "NULLABLE"))

    def _verifySchema(self, schema, resource):
        r_fields = resource["schema"]["fields"]
        self.assertEqual(len(schema), len(r_fields))

        for field, r_field in zip(schema, r_fields):
            self._verify_field(field, r_field)


class Test_parse_schema_resource(unittest.TestCase, _SchemaBase):
    def _call_fut(self, resource):
        from google.cloud.bigquery.schema import _parse_schema_resource

        return _parse_schema_resource(resource)

    def _make_resource(self):
        return {
            "schema": {
                "fields": [
                    {"name": "full_name", "type": "STRING", "mode": "REQUIRED"},
                    {"name": "age", "type": "INTEGER", "mode": "REQUIRED"},
                ]
            }
        }

    def test__parse_schema_resource_defaults(self):
        RESOURCE = self._make_resource()
        schema = self._call_fut(RESOURCE["schema"])
        self._verifySchema(schema, RESOURCE)

    def test__parse_schema_resource_subfields(self):
        RESOURCE = self._make_resource()
        RESOURCE["schema"]["fields"].append(
            {
                "name": "phone",
                "type": "RECORD",
                "mode": "REPEATED",
                "fields": [
                    {"name": "type", "type": "STRING", "mode": "REQUIRED"},
                    {"name": "number", "type": "STRING", "mode": "REQUIRED"},
                ],
            }
        )
        schema = self._call_fut(RESOURCE["schema"])
        self._verifySchema(schema, RESOURCE)

    def test__parse_schema_resource_fields_without_mode(self):
        RESOURCE = self._make_resource()
        RESOURCE["schema"]["fields"].append({"name": "phone", "type": "STRING"})

        schema = self._call_fut(RESOURCE["schema"])
        self._verifySchema(schema, RESOURCE)


class Test_build_schema_resource(unittest.TestCase, _SchemaBase):
    def _call_fut(self, resource):
        from google.cloud.bigquery.schema import _build_schema_resource

        return _build_schema_resource(resource)

    def test_defaults(self):
        from google.cloud.bigquery.schema import SchemaField

        full_name = SchemaField("full_name", "STRING", mode="REQUIRED")
        age = SchemaField("age", "INTEGER", mode="REQUIRED")
        resource = self._call_fut([full_name, age])
        self.assertEqual(len(resource), 2)
        self.assertEqual(
            resource[0],
            {
                "name": "full_name",
                "type": "STRING",
                "mode": "REQUIRED",
                "description": None,
            },
        )
        self.assertEqual(
            resource[1],
            {"name": "age", "type": "INTEGER", "mode": "REQUIRED", "description": None},
        )

    def test_w_description(self):
        from google.cloud.bigquery.schema import SchemaField

        DESCRIPTION = "DESCRIPTION"
        full_name = SchemaField(
            "full_name", "STRING", mode="REQUIRED", description=DESCRIPTION
        )
        age = SchemaField("age", "INTEGER", mode="REQUIRED")
        resource = self._call_fut([full_name, age])
        self.assertEqual(len(resource), 2)
        self.assertEqual(
            resource[0],
            {
                "name": "full_name",
                "type": "STRING",
                "mode": "REQUIRED",
                "description": DESCRIPTION,
            },
        )
        self.assertEqual(
            resource[1],
            {"name": "age", "type": "INTEGER", "mode": "REQUIRED", "description": None},
        )

    def test_w_subfields(self):
        from google.cloud.bigquery.schema import SchemaField

        full_name = SchemaField("full_name", "STRING", mode="REQUIRED")
        ph_type = SchemaField("type", "STRING", "REQUIRED")
        ph_num = SchemaField("number", "STRING", "REQUIRED")
        phone = SchemaField(
            "phone", "RECORD", mode="REPEATED", fields=[ph_type, ph_num]
        )
        resource = self._call_fut([full_name, phone])
        self.assertEqual(len(resource), 2)
        self.assertEqual(
            resource[0],
            {
                "name": "full_name",
                "type": "STRING",
                "mode": "REQUIRED",
                "description": None,
            },
        )
        self.assertEqual(
            resource[1],
            {
                "name": "phone",
                "type": "RECORD",
                "mode": "REPEATED",
                "description": None,
                "fields": [
                    {
                        "name": "type",
                        "type": "STRING",
                        "mode": "REQUIRED",
                        "description": None,
                    },
                    {
                        "name": "number",
                        "type": "STRING",
                        "mode": "REQUIRED",
                        "description": None,
                    },
                ],
            },
        )
