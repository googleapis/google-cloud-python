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

from google.cloud.bigquery.schema import PolicyTagList
import unittest

import mock
import pytest


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
        self.assertEqual(field.name, "test")
        self.assertEqual(field.field_type, "STRING")
        self.assertEqual(field.mode, "NULLABLE")
        self.assertIsNone(field.description)
        self.assertEqual(field.fields, ())
        self.assertEqual(field.policy_tags, PolicyTagList())

    def test_constructor_explicit(self):
        field = self._make_one("test", "STRING", mode="REQUIRED", description="Testing")
        self.assertEqual(field.name, "test")
        self.assertEqual(field.field_type, "STRING")
        self.assertEqual(field.mode, "REQUIRED")
        self.assertEqual(field.description, "Testing")
        self.assertEqual(field.fields, ())

    def test_constructor_subfields(self):
        sub_field1 = self._make_one("area_code", "STRING")
        sub_field2 = self._make_one("local_number", "STRING")
        field = self._make_one(
            "phone_number", "RECORD", fields=[sub_field1, sub_field2]
        )
        self.assertEqual(field.name, "phone_number")
        self.assertEqual(field.field_type, "RECORD")
        self.assertEqual(field.mode, "NULLABLE")
        self.assertIsNone(field.description)
        self.assertEqual(len(field.fields), 2)
        self.assertEqual(field.fields[0], sub_field1)
        self.assertEqual(field.fields[1], sub_field2)

    def test_constructor_with_policy_tags(self):
        from google.cloud.bigquery.schema import PolicyTagList

        policy = PolicyTagList(names=("foo", "bar"))
        field = self._make_one(
            "test", "STRING", mode="REQUIRED", description="Testing", policy_tags=policy
        )
        self.assertEqual(field.name, "test")
        self.assertEqual(field.field_type, "STRING")
        self.assertEqual(field.mode, "REQUIRED")
        self.assertEqual(field.description, "Testing")
        self.assertEqual(field.fields, ())
        self.assertEqual(field.policy_tags, policy)

    def test_to_api_repr(self):
        from google.cloud.bigquery.schema import PolicyTagList

        policy = PolicyTagList(names=("foo", "bar"))
        self.assertEqual(
            policy.to_api_repr(), {"names": ["foo", "bar"]},
        )

        field = self._make_one("foo", "INTEGER", "NULLABLE", policy_tags=policy)
        self.assertEqual(
            field.to_api_repr(),
            {
                "mode": "NULLABLE",
                "name": "foo",
                "type": "INTEGER",
                "policyTags": {"names": ["foo", "bar"]},
            },
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
                            "policyTags": {"names": []},
                        }
                    ],
                    "mode": "REQUIRED",
                    "name": "foo",
                    "type": record_type,
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

    def test_from_api_repr_policy(self):
        field = self._get_target_class().from_api_repr(
            {
                "fields": [{"mode": "nullable", "name": "bar", "type": "integer"}],
                "name": "foo",
                "type": "record",
                "policyTags": {"names": ["one", "two"]},
            }
        )
        self.assertEqual(field.name, "foo")
        self.assertEqual(field.field_type, "RECORD")
        self.assertEqual(field.policy_tags.names, ("one", "two"))
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
        self.assertEqual(schema_field.name, name)

    def test_field_type_property(self):
        field_type = "BOOLEAN"
        schema_field = self._make_one("whether", field_type)
        self.assertEqual(schema_field.field_type, field_type)

    def test_mode_property(self):
        mode = "REPEATED"
        schema_field = self._make_one("again", "FLOAT", mode=mode)
        self.assertEqual(schema_field.mode, mode)

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
        self.assertEqual(schema_field.description, description)

    def test_fields_property(self):
        sub_field1 = self._make_one("one", "STRING")
        sub_field2 = self._make_one("fish", "INTEGER")
        fields = (sub_field1, sub_field2)
        schema_field = self._make_one("boat", "RECORD", fields=fields)
        self.assertEqual(schema_field.fields, fields)

    def test_to_standard_sql_simple_type(self):
        sql_type = self._get_standard_sql_data_type_class()
        examples = (
            # a few legacy types
            ("INTEGER", sql_type.TypeKind.INT64),
            ("FLOAT", sql_type.TypeKind.FLOAT64),
            ("BOOLEAN", sql_type.TypeKind.BOOL),
            ("DATETIME", sql_type.TypeKind.DATETIME),
            # a few standard types
            ("INT64", sql_type.TypeKind.INT64),
            ("FLOAT64", sql_type.TypeKind.FLOAT64),
            ("BOOL", sql_type.TypeKind.BOOL),
            ("GEOGRAPHY", sql_type.TypeKind.GEOGRAPHY),
        )
        for legacy_type, standard_type in examples:
            field = self._make_one("some_field", legacy_type)
            standard_field = field.to_standard_sql()
            self.assertEqual(standard_field.name, "some_field")
            self.assertEqual(standard_field.type.type_kind, standard_type)

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
            name="date_field", type=sql_type(type_kind=sql_type.TypeKind.DATE)
        )
        sub_sub_field_time = types.StandardSqlField(
            name="time_field", type=sql_type(type_kind=sql_type.TypeKind.TIME)
        )

        # level 1 fields
        sub_field_struct = types.StandardSqlField(
            name="last_used", type=sql_type(type_kind=sql_type.TypeKind.STRUCT)
        )
        sub_field_struct.type.struct_type.fields.extend(
            [sub_sub_field_date, sub_sub_field_time]
        )
        sub_field_bytes = types.StandardSqlField(
            name="image_content", type=sql_type(type_kind=sql_type.TypeKind.BYTES)
        )

        # level 0 (top level)
        expected_result = types.StandardSqlField(
            name="image_usage", type=sql_type(type_kind=sql_type.TypeKind.STRUCT)
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
        expected_sql_type = sql_type(type_kind=sql_type.TypeKind.ARRAY)
        expected_sql_type.array_element_type.type_kind = sql_type.TypeKind.INT64
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
            name="name", type=sql_type(type_kind=sql_type.TypeKind.STRING)
        )
        age_field = types.StandardSqlField(
            name="age", type=sql_type(type_kind=sql_type.TypeKind.INT64)
        )
        person_struct = types.StandardSqlField(
            name="person_info", type=sql_type(type_kind=sql_type.TypeKind.STRUCT)
        )
        person_struct.type.struct_type.fields.extend([name_field, age_field])

        # define expected result - an ARRAY of person structs
        expected_sql_type = sql_type(
            type_kind=sql_type.TypeKind.ARRAY, array_element_type=person_struct.type
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
        self.assertEqual(
            standard_field.type.type_kind, sql_type.TypeKind.TYPE_KIND_UNSPECIFIED
        )

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

    def test___eq___hit_w_policy_tags(self):
        field = self._make_one(
            "test",
            "STRING",
            mode="REQUIRED",
            description="Testing",
            policy_tags=PolicyTagList(names=["foo", "bar"]),
        )
        other = self._make_one(
            "test",
            "STRING",
            mode="REQUIRED",
            description="Testing",
            policy_tags=PolicyTagList(names=["bar", "foo"]),
        )
        self.assertEqual(field, other)  # Policy tags order does not matter.

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

    def test___ne___different_policy_tags(self):
        field = self._make_one(
            "test",
            "STRING",
            mode="REQUIRED",
            description="Testing",
            policy_tags=PolicyTagList(names=["foo", "bar"]),
        )
        other = self._make_one(
            "test",
            "STRING",
            mode="REQUIRED",
            description="Testing",
            policy_tags=PolicyTagList(names=["foo", "baz"]),
        )
        self.assertNotEqual(field, other)

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
        expected = "SchemaField('field1', 'STRING', 'NULLABLE', None, (), ())"
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
                "policyTags": {"names": []},
            },
        )
        self.assertEqual(
            resource[1],
            {
                "name": "age",
                "type": "INTEGER",
                "mode": "REQUIRED",
                "policyTags": {"names": []},
            },
        )

    def test_w_description(self):
        from google.cloud.bigquery.schema import SchemaField

        DESCRIPTION = "DESCRIPTION"
        full_name = SchemaField(
            "full_name", "STRING", mode="REQUIRED", description=DESCRIPTION
        )
        age = SchemaField(
            "age",
            "INTEGER",
            mode="REQUIRED",
            # Explicitly unset description.
            description=None,
        )
        resource = self._call_fut([full_name, age])
        self.assertEqual(len(resource), 2)
        self.assertEqual(
            resource[0],
            {
                "name": "full_name",
                "type": "STRING",
                "mode": "REQUIRED",
                "description": DESCRIPTION,
                "policyTags": {"names": []},
            },
        )
        self.assertEqual(
            resource[1],
            {
                "name": "age",
                "type": "INTEGER",
                "mode": "REQUIRED",
                "description": None,
                "policyTags": {"names": []},
            },
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
                "policyTags": {"names": []},
            },
        )
        self.assertEqual(
            resource[1],
            {
                "name": "phone",
                "type": "RECORD",
                "mode": "REPEATED",
                "fields": [
                    {
                        "name": "type",
                        "type": "STRING",
                        "mode": "REQUIRED",
                        "policyTags": {"names": []},
                    },
                    {
                        "name": "number",
                        "type": "STRING",
                        "mode": "REQUIRED",
                        "policyTags": {"names": []},
                    },
                ],
            },
        )


class Test_to_schema_fields(unittest.TestCase):
    @staticmethod
    def _call_fut(schema):
        from google.cloud.bigquery.schema import _to_schema_fields

        return _to_schema_fields(schema)

    def test_invalid_type(self):
        schema = [
            ("full_name", "STRING", "REQUIRED"),
            ("address", "STRING", "REQUIRED"),
        ]
        with self.assertRaises(ValueError):
            self._call_fut(schema)

    def test_schema_fields_sequence(self):
        from google.cloud.bigquery.schema import SchemaField

        schema = [
            SchemaField("full_name", "STRING", mode="REQUIRED"),
            SchemaField("age", "INT64", mode="NULLABLE"),
        ]
        result = self._call_fut(schema)
        self.assertEqual(result, schema)

    def test_invalid_mapping_representation(self):
        schema = [
            {"name": "full_name", "type": "STRING", "mode": "REQUIRED"},
            {"name": "address", "typeooo": "STRING", "mode": "REQUIRED"},
        ]
        with self.assertRaises(Exception):
            self._call_fut(schema)

    def test_valid_mapping_representation(self):
        from google.cloud.bigquery.schema import SchemaField

        schema = [
            {"name": "full_name", "type": "STRING", "mode": "REQUIRED"},
            {
                "name": "residence",
                "type": "STRUCT",
                "mode": "NULLABLE",
                "fields": [
                    {"name": "foo", "type": "DATE", "mode": "NULLABLE"},
                    {"name": "bar", "type": "BYTES", "mode": "REQUIRED"},
                ],
            },
        ]

        expected_schema = [
            SchemaField("full_name", "STRING", mode="REQUIRED"),
            SchemaField(
                "residence",
                "STRUCT",
                mode="NULLABLE",
                fields=[
                    SchemaField("foo", "DATE", mode="NULLABLE"),
                    SchemaField("bar", "BYTES", mode="REQUIRED"),
                ],
            ),
        ]

        result = self._call_fut(schema)
        self.assertEqual(result, expected_schema)


class TestPolicyTags(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.schema import PolicyTagList

        return PolicyTagList

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_constructor(self):
        empty_policy_tags = self._make_one()
        self.assertIsNotNone(empty_policy_tags.names)
        self.assertEqual(len(empty_policy_tags.names), 0)
        policy_tags = self._make_one(["foo", "bar"])
        self.assertEqual(policy_tags.names, ("foo", "bar"))

    def test_from_api_repr(self):
        klass = self._get_target_class()
        api_repr = {"names": ["foo"]}
        policy_tags = klass.from_api_repr(api_repr)
        self.assertEqual(policy_tags.to_api_repr(), api_repr)

        # Ensure the None case correctly returns None, rather
        # than an empty instance.
        policy_tags2 = klass.from_api_repr(None)
        self.assertIsNone(policy_tags2)

    def test_to_api_repr(self):
        taglist = self._make_one(names=["foo", "bar"])
        self.assertEqual(
            taglist.to_api_repr(), {"names": ["foo", "bar"]},
        )
        taglist2 = self._make_one(names=("foo", "bar"))
        self.assertEqual(
            taglist2.to_api_repr(), {"names": ["foo", "bar"]},
        )

    def test___eq___wrong_type(self):
        policy = self._make_one(names=["foo"])
        other = object()
        self.assertNotEqual(policy, other)
        self.assertEqual(policy, mock.ANY)

    def test___eq___names_mismatch(self):
        policy = self._make_one(names=["foo", "bar"])
        other = self._make_one(names=["bar", "baz"])
        self.assertNotEqual(policy, other)

    def test___hash__set_equality(self):
        policy1 = self._make_one(["foo", "bar"])
        policy2 = self._make_one(["bar", "baz"])
        set_one = {policy1, policy2}
        set_two = {policy1, policy2}
        self.assertEqual(set_one, set_two)

    def test___hash__not_equals(self):
        policy1 = self._make_one(["foo", "bar"])
        policy2 = self._make_one(["bar", "baz"])
        set_one = {policy1}
        set_two = {policy2}
        self.assertNotEqual(set_one, set_two)


@pytest.mark.parametrize(
    "api,expect,key2",
    [
        (
            dict(name="n", type="NUMERIC"),
            ("n", "NUMERIC", None, None, None),
            ("n", "NUMERIC"),
        ),
        (
            dict(name="n", type="NUMERIC", precision=9),
            ("n", "NUMERIC", 9, None, None),
            ("n", "NUMERIC(9)"),
        ),
        (
            dict(name="n", type="NUMERIC", precision=9, scale=2),
            ("n", "NUMERIC", 9, 2, None),
            ("n", "NUMERIC(9, 2)"),
        ),
        (
            dict(name="n", type="BIGNUMERIC"),
            ("n", "BIGNUMERIC", None, None, None),
            ("n", "BIGNUMERIC"),
        ),
        (
            dict(name="n", type="BIGNUMERIC", precision=40),
            ("n", "BIGNUMERIC", 40, None, None),
            ("n", "BIGNUMERIC(40)"),
        ),
        (
            dict(name="n", type="BIGNUMERIC", precision=40, scale=2),
            ("n", "BIGNUMERIC", 40, 2, None),
            ("n", "BIGNUMERIC(40, 2)"),
        ),
        (
            dict(name="n", type="STRING"),
            ("n", "STRING", None, None, None),
            ("n", "STRING"),
        ),
        (
            dict(name="n", type="STRING", maxLength=9),
            ("n", "STRING", None, None, 9),
            ("n", "STRING(9)"),
        ),
        (
            dict(name="n", type="BYTES"),
            ("n", "BYTES", None, None, None),
            ("n", "BYTES"),
        ),
        (
            dict(name="n", type="BYTES", maxLength=9),
            ("n", "BYTES", None, None, 9),
            ("n", "BYTES(9)"),
        ),
    ],
)
def test_from_api_repr_parameterized(api, expect, key2):
    from google.cloud.bigquery.schema import SchemaField

    field = SchemaField.from_api_repr(api)

    assert (
        field.name,
        field.field_type,
        field.precision,
        field.scale,
        field.max_length,
    ) == expect

    assert field._key()[:2] == key2


@pytest.mark.parametrize(
    "field,api",
    [
        (
            dict(name="n", field_type="NUMERIC"),
            dict(name="n", type="NUMERIC", mode="NULLABLE", policyTags={"names": []}),
        ),
        (
            dict(name="n", field_type="NUMERIC", precision=9),
            dict(
                name="n",
                type="NUMERIC",
                mode="NULLABLE",
                precision=9,
                policyTags={"names": []},
            ),
        ),
        (
            dict(name="n", field_type="NUMERIC", precision=9, scale=2),
            dict(
                name="n",
                type="NUMERIC",
                mode="NULLABLE",
                precision=9,
                scale=2,
                policyTags={"names": []},
            ),
        ),
        (
            dict(name="n", field_type="BIGNUMERIC"),
            dict(
                name="n", type="BIGNUMERIC", mode="NULLABLE", policyTags={"names": []}
            ),
        ),
        (
            dict(name="n", field_type="BIGNUMERIC", precision=40),
            dict(
                name="n",
                type="BIGNUMERIC",
                mode="NULLABLE",
                precision=40,
                policyTags={"names": []},
            ),
        ),
        (
            dict(name="n", field_type="BIGNUMERIC", precision=40, scale=2),
            dict(
                name="n",
                type="BIGNUMERIC",
                mode="NULLABLE",
                precision=40,
                scale=2,
                policyTags={"names": []},
            ),
        ),
        (
            dict(name="n", field_type="STRING"),
            dict(name="n", type="STRING", mode="NULLABLE", policyTags={"names": []}),
        ),
        (
            dict(name="n", field_type="STRING", max_length=9),
            dict(
                name="n",
                type="STRING",
                mode="NULLABLE",
                maxLength=9,
                policyTags={"names": []},
            ),
        ),
        (
            dict(name="n", field_type="BYTES"),
            dict(name="n", type="BYTES", mode="NULLABLE", policyTags={"names": []}),
        ),
        (
            dict(name="n", field_type="BYTES", max_length=9),
            dict(
                name="n",
                type="BYTES",
                mode="NULLABLE",
                maxLength=9,
                policyTags={"names": []},
            ),
        ),
    ],
)
def test_to_api_repr_parameterized(field, api):
    from google.cloud.bigquery.schema import SchemaField

    assert SchemaField(**field).to_api_repr() == api
