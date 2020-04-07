# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

from django.db import NotSupportedError
from django.db.backends.base.schema import BaseDatabaseSchemaEditor


class DatabaseSchemaEditor(BaseDatabaseSchemaEditor):
    sql_create_table = "CREATE TABLE %(table)s (%(definition)s) PRIMARY KEY(%(primary_key)s)"
    sql_delete_table = "DROP TABLE %(table)s"
    sql_create_fk = None
    # Spanner doesn't support partial indexes. This string omits the
    # %(condition)s placeholder so that partial indexes are ignored.
    sql_create_index = "CREATE INDEX %(name)s ON %(table)s%(using)s (%(columns)s)%(extra)s"
    sql_create_unique = "CREATE UNIQUE NULL_FILTERED INDEX %(name)s ON %(table)s (%(columns)s)"
    sql_delete_unique = "DROP INDEX %(name)s"

    # Cloud Spanner requires when changing if a column is NULLABLE,
    # that it should get redefined with its type and size.
    # See https://cloud.google.com/spanner/docs/schema-updates#updates-that-require-validation
    sql_alter_column_null = "ALTER COLUMN %(column)s %(type)s"
    sql_alter_column_not_null = "ALTER COLUMN %(column)s %(type)s NOT NULL"
    sql_alter_column_type = "ALTER COLUMN %(column)s %(type)s"

    sql_delete_column = "ALTER TABLE %(table)s DROP COLUMN %(column)s"

    def create_model(self, model):
        """
        Create a table and any accompanying indexes or unique constraints for
        the given `model`.
        """
        # Create column SQL, add FK deferreds if needed
        column_sqls = []
        params = []
        for field in model._meta.local_fields:
            # SQL
            definition, extra_params = self.column_sql(model, field)
            if definition is None:
                continue
            # Check constraints can go on the column SQL here
            db_params = field.db_parameters(connection=self.connection)
            if db_params['check']:
                definition += " " + self.sql_check_constraint % db_params
            # Autoincrement SQL (for backends with inline variant)
            col_type_suffix = field.db_type_suffix(connection=self.connection)
            if col_type_suffix:
                definition += " %s" % col_type_suffix
            params.extend(extra_params)
            # FK
            if field.remote_field and field.db_constraint:
                to_table = field.remote_field.model._meta.db_table
                to_column = field.remote_field.model._meta.get_field(field.remote_field.field_name).column
                if self.sql_create_inline_fk:
                    definition += " " + self.sql_create_inline_fk % {
                        "to_table": self.quote_name(to_table),
                        "to_column": self.quote_name(to_column),
                    }
                elif self.connection.features.supports_foreign_keys:
                    self.deferred_sql.append(self._create_fk_sql(model, field, "_fk_%(to_table)s_%(to_column)s"))
            # Add the SQL to our big list
            column_sqls.append("%s %s" % (
                self.quote_name(field.column),
                definition,
            ))
            # Create a unique constraint separately because Spanner doesn't
            # allow them inline on a column.
            if field.unique and not field.primary_key:
                self.deferred_sql.append(self._create_unique_sql(model, [field.column]))

        # Add any unique_togethers (always deferred, as some fields might be
        # created afterwards, like geometry fields with some backends)
        for fields in model._meta.unique_together:
            columns = [model._meta.get_field(field).column for field in fields]
            self.deferred_sql.append(self._create_unique_sql(model, columns))
        constraints = [constraint.constraint_sql(model, self) for constraint in model._meta.constraints]
        # Make the table
        sql = self.sql_create_table % {
            "table": self.quote_name(model._meta.db_table),
            "definition": ", ".join(constraint for constraint in (*column_sqls, *constraints) if constraint),
            "primary_key": self.quote_name(model._meta.pk.column),
        }
        if model._meta.db_tablespace:
            tablespace_sql = self.connection.ops.tablespace_sql(model._meta.db_tablespace)
            if tablespace_sql:
                sql += ' ' + tablespace_sql
        # Prevent using [] as params, in the case a literal '%' is used in the definition
        self.execute(sql, params or None)

        # Add any field index and index_together's (deferred as SQLite _remake_table needs it)
        self.deferred_sql.extend(self._model_indexes_sql(model))

        # Make M2M tables
        for field in model._meta.local_many_to_many:
            if field.remote_field.through._meta.auto_created:
                self.create_model(field.remote_field.through)

    def delete_model(self, model):
        # Spanner requires dropping all of a table's indexes before dropping
        # the table.
        index_names = self._constraint_names(model, index=True, primary_key=False)
        for index_name in index_names:
            self.execute(self._delete_index_sql(model, index_name))
        super().delete_model(model)

    def add_field(self, model, field):
        # Special-case implicit M2M tables
        if field.many_to_many and field.remote_field.through._meta.auto_created:
            return self.create_model(field.remote_field.through)
        # Get the column's definition
        definition, params = self.column_sql(model, field, exclude_not_null=True)
        # It might not actually have a column behind it
        if definition is None:
            return
        # Check constraints can go on the column SQL here
        db_params = field.db_parameters(connection=self.connection)
        if db_params['check']:
            definition += " " + self.sql_check_constraint % db_params
        # Build the SQL and run it
        sql = self.sql_create_column % {
            "table": self.quote_name(model._meta.db_table),
            "column": self.quote_name(field.column),
            "definition": definition,
        }
        self.execute(sql, params)
        # Set defaults values on existing rows. (Django usually uses-database
        # defaults for this but Spanner doesn't support them.)
        effective_default = self.effective_default(field)
        if effective_default is not None:
            self.execute('UPDATE %(table)s SET %(column)s=%%s' % {
                "table": self.quote_name(model._meta.db_table),
                "column": self.quote_name(field.column),
            }, (effective_default,))
        # Spanner doesn't support adding NOT NULL columns to existing tables.
        if not field.null:
            self.execute(self.sql_alter_column % {
                "table": self.quote_name(model._meta.db_table),
                "changes": self.sql_alter_column_not_null % {
                    'column': self.quote_name(field.column),
                    'type':  db_params['type'],
                },
            })
        # Add an index, if required
        self.deferred_sql.extend(self._field_indexes_sql(model, field))
        # Create a unique constraint separately because Spanner doesn't allow
        # them inline on a column.
        if field.unique and not field.primary_key:
            self.deferred_sql.append(self._create_unique_sql(model, [field.column]))
        # Add any FK constraints later
        if field.remote_field and self.connection.features.supports_foreign_keys and field.db_constraint:
            self.deferred_sql.append(self._create_fk_sql(model, field, "_fk_%(to_table)s_%(to_column)s"))

    def remove_field(self, model, field):
        # Spanner requires dropping a column's indexes before dropping the
        # column.
        index_names = self._constraint_names(model, [field.column], index=True)
        for index_name in index_names:
            self.execute(self._delete_index_sql(model, index_name))
        super().remove_field(model, field)

    def column_sql(self, model, field, include_default=False, exclude_not_null=False):
        """
        Take a field and return its column definition.
        The field must already have had set_attributes_from_name() called.
        """
        # Get the column's type and use that as the basis of the SQL
        db_params = field.db_parameters(connection=self.connection)
        sql = db_params['type']
        params = []
        # Check for fields that aren't actually columns (e.g. M2M)
        if sql is None:
            return None, None
        # Work out nullability
        null = field.null
        # Oracle treats the empty string ('') as null, so coerce the null
        # option whenever '' is a possible value.
        if (field.empty_strings_allowed and not field.primary_key and
                self.connection.features.interprets_empty_strings_as_nulls):
            null = True
        if not null and not exclude_not_null:
            sql += " NOT NULL"
        # Optionally add the tablespace if it's an implicitly indexed column
        tablespace = field.db_tablespace or model._meta.db_tablespace
        if tablespace and self.connection.features.supports_tablespaces and field.unique:
            sql += " %s" % self.connection.ops.tablespace_sql(tablespace, inline=True)
        # Return the sql
        return sql, params

    def add_index(self, model, index):
        # Work around a bug in Django where a space isn't inserting before
        # DESC: https://code.djangoproject.com/ticket/30961
        # This method can be removed in Django 3.1.
        index.fields_orders = [
            (field_name, ' DESC' if order == 'DESC' else '')
            for field_name, order in index.fields_orders
        ]
        super().add_index(model, index)

    def quote_value(self, value):
        # TODO: a real implementation:
        # https://github.com/orijtech/django-spanner/issues/227
        return str(value)

    def _alter_field(self, model, old_field, new_field, old_type, new_type,
                     old_db_params, new_db_params, strict=False):
        # Spanner requires dropping indexes before changing the nullability
        # of a column.
        nullability_changed = old_field.null != new_field.null
        if nullability_changed:
            index_names = self._constraint_names(
                model, [old_field.column], index=True,
            )
            if index_names and not old_field.db_index:
                raise NotSupportedError(
                    "Changing nullability of a field with an index other than "
                    "Field(db_index=True) isn't yet supported."
                )
            if len(index_names) > 1:
                raise NotSupportedError(
                    "Changing nullability of a field with more than one "
                    "index isn't yet supported."
                )
            for index_name in index_names:
                self.execute(self._delete_index_sql(model, index_name))
        super()._alter_field(
            model, old_field, new_field, old_type, new_type,
            old_db_params, new_db_params, strict=False,
        )
        # Recreate the index that was dropped earlier.
        if nullability_changed and new_field.db_index:
            self.execute(self._create_index_sql(model, [new_field]))

    def _alter_column_type_sql(self, model, old_field, new_field, new_type):
        # Spanner needs to use sql_alter_column_not_null if the field is
        # NOT NULL, otherwise the constraint is dropped.
        sql = self.sql_alter_column_type if new_field.null else self.sql_alter_column_not_null
        return (
            (
                sql % {
                    "column": self.quote_name(new_field.column),
                    "type": new_type,
                },
                [],
            ),
            [],
        )

    def _check_sql(self, name, check):
        # Spanner doesn't support CHECK constraints.
        return None

    def _unique_sql(self, model, fields, name, condition=None):
        # Inline constraints aren't supported, so create the index separately.
        sql = self._create_unique_sql(model, fields, name=name, condition=condition)
        if sql:
            self.deferred_sql.append(sql)
        return None

    def skip_default(self, field):
        """Cloud Spanner doesn't support column defaults."""
        return True
