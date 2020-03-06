# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

from django.db.backends.base.introspection import (
    BaseDatabaseIntrospection, FieldInfo, TableInfo,
)
from google.cloud.spanner_v1.proto import type_pb2


class DatabaseIntrospection(BaseDatabaseIntrospection):
    data_types_reverse = {
        type_pb2.BOOL: 'BooleanField',
        type_pb2.BYTES: 'BinaryField',
        type_pb2.DATE: 'DateField',
        type_pb2.FLOAT64: 'FloatField',
        type_pb2.INT64: 'IntegerField',
        type_pb2.STRING: 'CharField',
        type_pb2.TIMESTAMP: 'DateTimeField',
    }

    def get_table_list(self, cursor):
        """Return a list of table and view names in the current database."""
        # The second TableInfo field is 't' for table or 'v' for view.
        return [TableInfo(row[0], 't') for row in cursor.list_tables()]

    def get_table_description(self, cursor, table_name):
        """
        Return a description of the table with the DB-API cursor.description
        interface.
        """
        cursor.execute("SELECT * FROM %s LIMIT 1" % self.connection.ops.quote_name(table_name))
        return [
            FieldInfo(
                line.name,
                line.type_code,
                # TODO: Fill these in as they're implemented.
                None,  # display_size
                None,  # internal_size
                None,  # precision
                None,  # scale
                None,  # null_ok
                None,  # default
            )
            for line in cursor.description
        ]
