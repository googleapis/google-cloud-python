# Copyright 2021 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd


from unittest import mock

from django.db import NotSupportedError, connection, connections
from django.db.models import Index
from django.db.models.fields import AutoField, IntegerField

from django_spanner import gen_rand_int64
from django_spanner.schema import DatabaseSchemaEditor
from tests._helpers import HAS_OPENTELEMETRY_INSTALLED
from tests.unit.django_spanner.simple_test import SpannerSimpleTestClass
from tests.unit.django_spanner.test__opentelemetry_tracing import (
    DATABASE_ID,
    INSTANCE_ID,
    PROJECT,
)

from .models import Author

BASE_ATTRIBUTES = {
    "db.type": "spanner",
    "db.engine": "django_spanner",
    "db.project": PROJECT,
    "db.instance": INSTANCE_ID,
    "db.name": DATABASE_ID,
}


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

    def test_create_model_foreign_key_and_check_constraint(self):
        from django.db.models import Model, ForeignKey, IntegerField, CASCADE
        class Book(Model):
            author = ForeignKey(Author, on_delete=CASCADE)
            pages = IntegerField()
            class Meta:
                app_label = "tests"

        with DatabaseSchemaEditor(self.connection) as schema_editor:
            schema_editor.execute = mock.MagicMock()

            # Test sql_create_inline_fk
            schema_editor.sql_create_inline_fk = "CONSTRAINT FK FOREIGN KEY (%(from_column_norm)s) REFERENCES %(to_table_norm)s (%(to_column_norm)s)"
            schema_editor.create_model(Book)

            # Test supports_foreign_keys with no inline_fk (False and True)
            schema_editor.sql_create_inline_fk = None
            with mock.patch.object(schema_editor.connection.features, "supports_foreign_keys", False):
                schema_editor.create_model(Book)
            with mock.patch.object(schema_editor.connection.features, "supports_foreign_keys", True):
                schema_editor.create_model(Book)

            # Test check constraint on column
            f_pages = Book._meta.get_field("pages")
            with mock.patch.object(f_pages, "db_parameters", return_value={"type": "INT64", "check": "pages > 0"}):
                schema_editor.create_model(Book)

    def test_create_model_unique_together_and_constraints(self):
        from django.db.models import Model, OneToOneField, IntegerField, UniqueConstraint, CheckConstraint, Q, CASCADE
        class Profile(Model):
            author = OneToOneField(Author, on_delete=CASCADE, primary_key=True)
            code = IntegerField()
            class Meta:
                app_label = "tests"
                unique_together = [("code",)]
                constraints = [
                    UniqueConstraint(fields=["code"], name="unique_code_idx"),
                    CheckConstraint(check=Q(code__gt=0), name="code_gt_zero"),
                ]

        with DatabaseSchemaEditor(self.connection) as schema_editor:
            schema_editor.execute = mock.MagicMock()
            schema_editor.create_model(Profile)

    def test_m2m_field_schema_operations(self):
        from django.db.models import Model, ManyToManyField, IntegerField
        class Article(Model):
            authors = ManyToManyField(Author)
            num = IntegerField()
            class Meta:
                app_label = "tests"

        with DatabaseSchemaEditor(self.connection) as schema_editor:
            schema_editor.execute = mock.MagicMock()
            schema_editor._constraint_names = mock.MagicMock(return_value=[])

            # Test col_type_suffix and empty tablespace_sql
            with mock.patch.object(Article._meta.get_field("num"), "db_type_suffix", return_value="SUFFIX"):
                with mock.patch.object(Article._meta, "db_tablespace", "tbl"):
                    with mock.patch.object(schema_editor.connection.ops, "tablespace_sql", return_value=""):
                        schema_editor.create_model(Article)

            m2m_field = Article._meta.get_field("authors")
            schema_editor.add_field(Article, m2m_field)
            schema_editor.remove_field(Article, m2m_field)
            schema_editor.alter_field(Article, m2m_field, m2m_field)

            # Test add_field with FK, unique, and check constraint
            from django.db.models import ForeignKey, CASCADE, IntegerField, CharField
            fk_field = ForeignKey(Author, on_delete=CASCADE)
            fk_field.set_attributes_from_name("author_fk")
            fk_field.model = Author
            fk_field.unique = True
            with mock.patch.object(fk_field, "db_parameters", return_value={"type": "INT64", "check": "num > 0"}):
                with mock.patch.object(schema_editor.connection.features, "supports_foreign_keys", True):
                    schema_editor.add_field(Author, fk_field)

            # Test M2M, None column SQL, and db_default edge cases
            for m in [Article, Author]:
                schema_editor.create_model(m)
            self.assertIsNone(schema_editor.column_sql(Article, m2m_field)[0])

            def_field = IntegerField(db_default=10)
            def_field.set_attributes_from_name("def_num")
            def_field.model = Author
            self.assertIn("DEFAULT", schema_editor.column_sql(Author, def_field)[0])

            with mock.patch.object(schema_editor, "db_default_sql", return_value=(None, [])):
                self.assertNotIn("DEFAULT", schema_editor.column_sql(Author, def_field)[0])

            with mock.patch.object(schema_editor, "column_sql", return_value=(None, None)):
                schema_editor.create_model(Article)

            # Test _alter_column_type_sql with same type, empty_strings_allowed, tablespace
            char_field1 = CharField(max_length=50, db_tablespace="tbl", unique=True)
            char_field1.set_attributes_from_name("title")
            char_field1.model = Author
            char_field2 = CharField(max_length=100, db_tablespace="tbl", unique=True)
            char_field2.set_attributes_from_name("title")
            char_field2.model = Author
            with mock.patch.object(schema_editor.connection.features, "interprets_empty_strings_as_nulls", True):
                with mock.patch.object(schema_editor.connection.features, "supports_tablespaces", True):
                    schema_editor._alter_column_type_sql(Author, char_field1, char_field2, "STRING(100)")
                    # Test column_sql with tablespace & empty string null (lines 371, 381)
                    schema_editor.column_sql(Author, char_field1)
            # Same type returns sql statement
            sql_same, _ = schema_editor._alter_column_type_sql(Author, char_field1, char_field1, "STRING(50)")
            self.assertIsNotNone(sql_same)

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
        if HAS_OPENTELEMETRY_INSTALLED:
            span_list = self.ot_exporter.get_finished_spans()
            self.assertEqual(len(span_list), 1)
            self.assertSpanAttributes(
                "CloudSpannerDjango.create_model",
                attributes=dict(BASE_ATTRIBUTES, model_name="tests_author"),
                span=span_list[0],
            )

    def test_delete_model(self):
        """
        Tests deleting a model
        """
        with DatabaseSchemaEditor(self.connection) as schema_editor:
            schema_editor.execute = mock.MagicMock()
            schema_editor._constraint_names = mock.MagicMock(return_value=[])
            with mock.patch.object(schema_editor.connection.features, "supports_foreign_keys", True):
                schema_editor.delete_model(Author)

            schema_editor.execute.assert_called_with(
                "DROP TABLE tests_author",
            )

        if HAS_OPENTELEMETRY_INSTALLED:
            span_list = self.ot_exporter.get_finished_spans()
            self.assertEqual(len(span_list), 1)
            self.assertSpanAttributes(
                "CloudSpannerDjango.delete_model",
                attributes=dict(BASE_ATTRIBUTES, model_name="tests_author"),
                span=span_list[0],
            )

    def test_delete_model_with_index(self):
        """
        Tests deleting a model with index
        """
        with DatabaseSchemaEditor(self.connection) as schema_editor:
            schema_editor.execute = mock.MagicMock()

            def delete_index_sql(*args, **kwargs):
                # Overriding Statement creation with sql string.
                return "DROP INDEX num_unique"

            def constraint_names(*args, **kwargs):
                return ["num_unique"]

            schema_editor._delete_index_sql = delete_index_sql
            schema_editor._constraint_names = constraint_names
            schema_editor.delete_model(Author)

            calls = [
                mock.call("DROP INDEX num_unique"),
                mock.call("DROP TABLE tests_author"),
            ]

            schema_editor.execute.assert_has_calls(calls)

        if HAS_OPENTELEMETRY_INSTALLED:
            span_list = self.ot_exporter.get_finished_spans()
            self.assertEqual(len(span_list), 2)
            self.assertSpanAttributes(
                "CloudSpannerDjango.delete_model.delete_index",
                attributes=dict(
                    BASE_ATTRIBUTES,
                    model_name="tests_author",
                    index_name="num_unique",
                ),
                span=span_list[0],
            )
            self.assertSpanAttributes(
                "CloudSpannerDjango.delete_model",
                attributes=dict(
                    BASE_ATTRIBUTES,
                    model_name="tests_author",
                ),
                span=span_list[1],
            )

    def test_add_field(self):
        """
        Tests adding fields to models
        """
        with DatabaseSchemaEditor(self.connection) as schema_editor:
            schema_editor.execute = mock.MagicMock()
            new_field = IntegerField(null=True)
            new_field.set_attributes_from_name("age")
            new_field.model = Author
            schema_editor.add_field(Author, new_field)

            schema_editor.execute.assert_called_once_with(
                "ALTER TABLE tests_author ADD COLUMN age INT64", []
            )

    def test_remove_field(self):
        """
        Tests remove fields from models
        """
        with DatabaseSchemaEditor(self.connection) as schema_editor:
            schema_editor.execute = mock.MagicMock()
            schema_editor._constraint_names = mock.MagicMock()
            remove_field = IntegerField(unique=True)
            remove_field.set_attributes_from_name("num")
            remove_field.model = Author
            schema_editor.remove_field(Author, remove_field)

            schema_editor.execute.assert_called_once_with(
                "ALTER TABLE tests_author DROP COLUMN num"
            )

        if HAS_OPENTELEMETRY_INSTALLED:
            span_list = self.ot_exporter.get_finished_spans()
            self.assertEqual(len(span_list), 1)
            self.assertSpanAttributes(
                "CloudSpannerDjango.remove_field",
                attributes=dict(
                    BASE_ATTRIBUTES,
                    model_name="tests_author",
                    field="num",
                ),
                span=span_list[0],
            )

    def test_remove_field_with_index(self):
        """
        Tests remove fields from models
        """
        with DatabaseSchemaEditor(self.connection) as schema_editor:
            schema_editor.execute = mock.MagicMock()

            def delete_index_sql(*args, **kwargs):
                # Overriding Statement creation with sql string.
                return "DROP INDEX num_unique"

            def constraint_names(*args, **kwargs):
                return ["num_unique"]

            schema_editor._delete_index_sql = delete_index_sql
            schema_editor._constraint_names = constraint_names

            remove_field = IntegerField(unique=True)
            remove_field.set_attributes_from_name("num")
            remove_field.model = Author
            schema_editor.remove_field(Author, remove_field)

            calls = [
                mock.call("DROP INDEX num_unique"),
                mock.call("ALTER TABLE tests_author DROP COLUMN num"),
            ]
            schema_editor.execute.assert_has_calls(calls)

        if HAS_OPENTELEMETRY_INSTALLED:
            span_list = self.ot_exporter.get_finished_spans()
            self.assertEqual(len(span_list), 2)
            self.assertSpanAttributes(
                "CloudSpannerDjango.remove_field.delete_index",
                attributes=dict(
                    BASE_ATTRIBUTES,
                    model_name="tests_author",
                    field="num",
                    index_name="num_unique",
                ),
                span=span_list[0],
            )
            self.assertSpanAttributes(
                "CloudSpannerDjango.remove_field",
                attributes=dict(
                    BASE_ATTRIBUTES,
                    model_name="tests_author",
                    field="num",
                ),
                span=span_list[1],
            )

    def test_column_sql_not_null_field(self):
        """
        Tests column sql for not null field
        """
        with DatabaseSchemaEditor(self.connection) as schema_editor:
            schema_editor.execute = mock.MagicMock()
            new_field = IntegerField()
            new_field.set_attributes_from_name("num")
            new_field.model = Author
            sql, params = schema_editor.column_sql(Author, new_field)
            self.assertEqual(sql, "INT64 NOT NULL")
            self.assertEqual(params, [])

    def test_column_sql_nullable_field(self):
        """
        Tests column sql for nullable field
        """
        with DatabaseSchemaEditor(self.connection) as schema_editor:
            schema_editor.execute = mock.MagicMock()
            new_field = IntegerField(null=True)
            new_field.set_attributes_from_name("num")
            new_field.model = Author
            sql, params = schema_editor.column_sql(Author, new_field)
            self.assertEqual(sql, "INT64")
            self.assertEqual(params, [])

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
            self.assertEqual(name, "")
        if HAS_OPENTELEMETRY_INSTALLED:
            span_list = self.ot_exporter.get_finished_spans()
            self.assertEqual(len(span_list), 1)
            self.assertSpanAttributes(
                "CloudSpannerDjango.add_index",
                attributes=dict(
                    BASE_ATTRIBUTES,
                    model_name="tests_author",
                    index="num",
                ),
                span=span_list[0],
            )

    def test_alter_field(self):
        """
        Tests altering existing field in table
        """
        with DatabaseSchemaEditor(self.connection) as schema_editor:
            schema_editor.execute = mock.MagicMock()
            old_field = IntegerField()
            old_field.set_attributes_from_name("num")
            old_field.model = Author
            new_field = IntegerField()
            new_field.set_attributes_from_name("author_num")
            new_field.model = Author
            schema_editor.alter_field(Author, old_field, new_field)

            schema_editor.execute.assert_called_once_with(
                "ALTER TABLE tests_author RENAME COLUMN num TO author_num"
            )

    def test_alter_field_change_null_with_single_index(self):
        """
        Tests altering nullability of field with single index
        """
        with DatabaseSchemaEditor(self.connection) as schema_editor:
            schema_editor.execute = mock.MagicMock()

            def delete_index_sql(*args, **kwargs):
                # Overriding Statement creation with sql string.
                return "DROP INDEX num_unique"

            def create_index_sql(*args, **kwargs):
                # Overriding Statement creation with sql string.
                return "CREATE INDEX tests_author ON tests_author (author_num)"

            def constraint_names(*args, **kwargs):
                return ["num_unique"]

            schema_editor._delete_index_sql = delete_index_sql
            schema_editor._create_index_sql = create_index_sql
            schema_editor._constraint_names = constraint_names
            old_field = IntegerField(null=True, db_index=True)
            old_field.set_attributes_from_name("num")
            old_field.model = Author
            new_field = IntegerField(db_index=True)
            new_field.set_attributes_from_name("author_num")
            new_field.model = Author
            schema_editor.alter_field(Author, old_field, new_field)

            calls = [
                mock.call("DROP INDEX num_unique"),
                mock.call("ALTER TABLE tests_author RENAME COLUMN num TO author_num"),
                mock.call(
                    "ALTER TABLE tests_author ALTER COLUMN author_num INT64 NOT NULL",
                    [],
                ),
                mock.call("CREATE INDEX tests_author ON tests_author (author_num)"),
            ]
            schema_editor.execute.assert_has_calls(calls)
        if HAS_OPENTELEMETRY_INSTALLED:
            span_list = self.ot_exporter.get_finished_spans()
            self.assertEqual(len(span_list), 3)
            self.assertSpanAttributes(
                "CloudSpannerDjango.alter_field.delete_index",
                attributes=dict(
                    BASE_ATTRIBUTES,
                    model_name="tests_author",
                    index_name="num_unique",
                    alter_field="num",
                ),
                span=span_list[0],
            )
            self.assertSpanAttributes(
                "CloudSpannerDjango.alter_field",
                attributes=dict(
                    BASE_ATTRIBUTES,
                    model_name="tests_author",
                    alter_field="num",
                ),
                span=span_list[1],
            )
            self.assertSpanAttributes(
                "CloudSpannerDjango.alter_field.recreate_index",
                attributes=dict(
                    BASE_ATTRIBUTES,
                    model_name="tests_author",
                    alter_field="author_num",
                ),
                span=span_list[2],
            )

    def test_alter_field_nullability_change_raise_not_support_error(self):
        """
        Tests altering nullability of existing field in table
        """
        with DatabaseSchemaEditor(self.connection) as schema_editor:
            schema_editor.execute = mock.MagicMock()

            def constraint_names(*args, **kwargs):
                return ["num_unique"]

            schema_editor._constraint_names = constraint_names
            old_field = IntegerField(null=True)
            old_field.set_attributes_from_name("num")
            old_field.model = Author
            new_field = IntegerField()
            new_field.set_attributes_from_name("author_num")
            new_field.model = Author
            with self.assertRaises(NotSupportedError):
                schema_editor.alter_field(Author, old_field, new_field)

    def test_alter_field_change_null_with_multiple_index_error(self):
        """
        Tests altering nullability of field with multiple index not supported
        """
        with DatabaseSchemaEditor(self.connection) as schema_editor:
            schema_editor.execute = mock.MagicMock()

            def constraint_names(*args, **kwargs):
                return ["num_unique", "dummy_index"]

            schema_editor._constraint_names = constraint_names
            old_field = IntegerField(null=True, db_index=True)
            old_field.set_attributes_from_name("num")
            old_field.model = Author
            new_field = IntegerField()
            new_field.set_attributes_from_name("author_num")
            new_field.model = Author
            with self.assertRaises(NotSupportedError):
                schema_editor.alter_field(Author, old_field, new_field)

    def test_autofield_no_default(self):
        """Spanner, default is not provided."""
        field = AutoField(name="field_name")
        assert gen_rand_int64 == field.default

    def test_autofield_default(self):
        """Spanner, default provided."""
        mock_func = mock.Mock()
        field = AutoField(name="field_name", default=mock_func)
        assert gen_rand_int64 != field.default
        assert mock_func == field.default

    def test_autofield_not_spanner(self):
        """Not Spanner, default not provided."""
        connection.settings_dict["ENGINE"] = "another_db"
        field = AutoField(name="field_name")
        assert gen_rand_int64 != field.default
        connection.settings_dict["ENGINE"] = "django_spanner"

    def test_autofield_not_spanner_w_default(self):
        """Not Spanner, default provided."""
        connection.settings_dict["ENGINE"] = "another_db"
        mock_func = mock.Mock()
        field = AutoField(name="field_name", default=mock_func)
        assert gen_rand_int64 != field.default
        assert mock_func == field.default
        connection.settings_dict["ENGINE"] = "django_spanner"

    def test_autofield_spanner_as_non_default_db_random_generation_enabled(
        self,
    ):
        """Not Spanner as the default db, default for field not provided."""
        connections.settings["default"]["ENGINE"] = "another_db"
        connections.settings["secondary"]["ENGINE"] = "django_spanner"
        connections.settings["secondary"]["RANDOM_ID_GENERATION_ENABLED"] = "true"
        field = AutoField(name="field_name")
        assert gen_rand_int64 == field.default
        connections.settings["default"]["ENGINE"] = "django_spanner"
        connections.settings["secondary"]["ENGINE"] = "django_spanner"
        del connections.settings["secondary"]["RANDOM_ID_GENERATION_ENABLED"]

    def test_schema_editor_utils_and_sql_formatting(self):
        with DatabaseSchemaEditor(self.connection) as se:
            se.execute = mock.MagicMock()

            # Quote values and prepare default
            self.assertEqual(se.quote_value("it's"), "'it''s'")
            self.assertEqual(se.quote_value(True), "TRUE")
            self.assertEqual(se.prepare_default(123), "123")

            # Unique & check SQL
            self.assertIsNone(se._unique_sql(Author, [Author._meta.get_field("name")], "idx"))
            with mock.patch("django_spanner.schema.USE_EMULATOR", False):
                self.assertIsNotNone(se._check_sql("chk", "num > 0"))
                se.deferred_sql.clear()
                se._unique_sql(Author, [Author._meta.get_field("name")], "idx")

            with mock.patch.object(se, "_create_unique_sql", return_value=None):
                se._unique_sql(Author, [Author._meta.get_field("name")], "idx")

            # Column SQL generated & db_default
            gen_f = IntegerField()
            gen_f.generated = True
            gen_f.set_attributes_from_name("g")
            gen_f.model = Author
            gen_f.generated_sql = lambda c: ("num * %s + %s + %s + %s", ["2", True, None, 5])
            self.assertIn("STORED", se.column_sql(Author, gen_f)[0])

            def_f = IntegerField(db_default=10)
            def_f.set_attributes_from_name("d")
            def_f.model = Author
            se.db_default_sql = lambda f: ("%s + %s + %s + %s", ["10", False, None, 3])
            self.assertIn("DEFAULT", se.column_sql(Author, def_f)[0])

            # Skip default & column type alter
            self.assertFalse(se.skip_default(gen_f))
            self.assertFalse(se.skip_default(def_f))

            f_null = IntegerField(null=True)
            f_null.set_attributes_from_name("v")
            self.assertTrue(len(se._alter_column_type_sql(Author, f_null, f_null, "INT64")[0]) > 0)

            # None definition add_field & tablespace
            with mock.patch.object(se, "column_sql", return_value=(None, None)):
                self.assertIsNone(se.add_field(Author, gen_f))

            with mock.patch.object(Author._meta, "db_tablespace", "tbl"):
                with mock.patch.object(se.connection.ops, "tablespace_sql", return_value="IN tbl"):
                    se.create_model(Author)
