# Copyright 2021 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd


from django.db.models import Index
from django.db.models.fields import IntegerField
from django_spanner.schema import DatabaseSchemaEditor
from tests.unit.django_spanner.simple_test import SpannerSimpleTestClass
from unittest import mock
from .models import Author


class TestUtils(SpannerSimpleTestClass):
    def test_quote_value(self):
        """
        Tries quoting input value.
        """
        schema_editor = DatabaseSchemaEditor(self.connection)
        self.assertEqual(schema_editor.quote_value(value=1.1), "1.1")

    def test_skip_default(self):
        """
        Tries skipping default as Cloud spanner doesn't support it.
        """
        schema_editor = DatabaseSchemaEditor(self.connection)
        self.assertTrue(schema_editor.skip_default(field=None))

    def test_create_model(self):
        """
        Tries creating a model's table.
        """
        with DatabaseSchemaEditor(self.connection) as schema_editor:
            schema_editor.execute = mock.MagicMock()
            schema_editor.create_model(Author)

            schema_editor.execute.assert_called_once_with(
                "CREATE TABLE tests_author (id INT64 NOT NULL, name STRING(40) "
                + "NOT NULL, last_name STRING(40) NOT NULL, num INT64 NOT "
                + "NULL, created TIMESTAMP NOT NULL, modified TIMESTAMP) "
                + "PRIMARY KEY(id)",
                None,
            )

    def test_delete_model(self):
        """
        Tests deleting a model
        """
        with DatabaseSchemaEditor(self.connection) as schema_editor:
            schema_editor.execute = mock.MagicMock()
            schema_editor._constraint_names = mock.MagicMock()
            schema_editor.delete_model(Author)

            schema_editor.execute.assert_called_once_with(
                "DROP TABLE tests_author",
            )

    def test_add_field(self):
        """
        Tests adding fields to models
        """
        with DatabaseSchemaEditor(self.connection) as schema_editor:
            schema_editor.execute = mock.MagicMock()
            new_field = IntegerField(null=True)
            new_field.set_attributes_from_name("age")
            schema_editor.add_field(Author, new_field)

            schema_editor.execute.assert_called_once_with(
                "ALTER TABLE tests_author ADD COLUMN age INT64", []
            )

    def test_column_sql_not_null_field(self):
        """
        Tests column sql for not null field
        """
        with DatabaseSchemaEditor(self.connection) as schema_editor:
            schema_editor.execute = mock.MagicMock()
            new_field = IntegerField()
            new_field.set_attributes_from_name("num")
            sql, params = schema_editor.column_sql(Author, new_field)
            self.assertEqual(sql, "INT64 NOT NULL")

    def test_column_sql_nullable_field(self):
        """
        Tests column sql for nullable field
        """
        with DatabaseSchemaEditor(self.connection) as schema_editor:
            schema_editor.execute = mock.MagicMock()
            new_field = IntegerField(null=True)
            new_field.set_attributes_from_name("num")
            sql, params = schema_editor.column_sql(Author, new_field)
            self.assertEqual(sql, "INT64")

    def test_column_add_index(self):
        """
        Tests column add index
        """
        with DatabaseSchemaEditor(self.connection) as schema_editor:
            schema_editor.execute = mock.MagicMock()
            index = Index(name="test_author_index_num", fields=["num"])
            schema_editor.add_index(Author, index)
            name, args, kwargs = schema_editor.execute.mock_calls[0]

            self.assertEqual(
                str(args[0]),
                "CREATE INDEX test_author_index_num ON tests_author (num)",
            )
            self.assertEqual(kwargs["params"], None)

    def test_alter_field(self):
        """
        Tests altering existing field in table
        """
        with DatabaseSchemaEditor(self.connection) as schema_editor:
            schema_editor.execute = mock.MagicMock()
            old_field = IntegerField()
            old_field.set_attributes_from_name("num")
            new_field = IntegerField()
            new_field.set_attributes_from_name("author_num")
            schema_editor.alter_field(Author, old_field, new_field)

            schema_editor.execute.assert_called_once_with(
                "ALTER TABLE tests_author RENAME COLUMN num TO author_num"
            )
