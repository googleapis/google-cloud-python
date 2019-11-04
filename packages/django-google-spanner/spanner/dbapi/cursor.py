# Copyright 2019 Google LLC
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .exceptions import (
        ProgrammingError
)

class Cursor(object):
    def __init__(self, session):
        self.__session = session
        self.__itr = None
        self.__res = None


    @property
    def description(self):
        if not self.__res.metadata:
            return None

        row_type = self.__res.metadata.row_type
        columns = []
        for field in row_type.fields:
            columns.append(Column(name=field.name, type_code=field.type.code))
        return tuple(columns)


    @property
    def rowcount(self):
        raise ProgrammingError('Unimplemented')


    def close(self):
        if not self.__session:
            raise ProgrammingError('Cursor is not connected to the database')

        self.__session.delete()
        self.__session = None


    def execute(self, sql, *args, **kwargs):
        """
        Performs the Spanner.execute_sql call as per
            https://googleapis.dev/python/spanner/latest/session-api.html#google.cloud.spanner_v1.session.Session.execute_sql

        Args:
            sql: A SQL statement
            *args: variadic argument list
            **kwargs: key worded arguments

        Returns:
            None
        """
        # Reference
        #  https://googleapis.dev/python/spanner/latest/session-api.html#google.cloud.spanner_v1.session.Session.execute_sql
        if not self.__session:
            raise ProgrammingError('Cursor is not connected to the database')

        # Immediately using:
        #   iter(response)
        # here, because this Spanner API doesn't provide
        # easy mechanisms to detect when only a single item
        # is returned or many, yet mixing results that
        # are for .fetchone() with those that would result in
        # many items returns a RuntimeError if .fetchone() is
        # invoked and vice versa.
        self.__res = self.__session.execute_sql(sql, *args, **kwargs)
        self.__itr = iter(self.__res)


    def __enter__(self):
        return self


    def __exit__(self, etype, value, traceback):
        self.close()


    def executemany(self, operation, seq_of_params):
        if not self.__session:
            raise ProgrammingError('Cursor is not connected to the database')

        raise ProgrammingError('Unimplemented')


    def __next__(self):
        return next(self.__itr)


    def __iter__(self):
        return self.__itr


    def fetchone(self):
        return next(self)


    def fetchall(self):
        return list(self.__itr)


    @property
    def arraysize(self):
        raise ProgrammingError('Unimplemented')


    def setinputsizes(sizes):
        raise ProgrammingError('Unimplemented')


    def setoutputsize(size, column=None):
        raise ProgrammingError('Unimplemented')


    def close(self):
        self.__session.delete()


class Column:
    def __init__(self, name, type_code, display_size=None, internal_size=None, precision=None, scale=None, null_ok=False):
        self.name = name
        self.type_code = type_code
        self.display_size = display_size
        self.internal_size = internal_size
        self.precision = precision
        self.scale = scale
        self.null_ok = null_ok


    def __repr__(self):
        return self.__str__()


    def __str__(self):
        rstr = ', '.join([field for field in [
            "name='%s'" %(self.name),
            "type_code=%d" %(self.type_code),
            None if not self.display_size else "display_size='%s'"%(self.display_size),
            None if not self.internal_size else "internal_size='%s'"%(self.internal_size),
            None if not self.precision else "precision='%s'" % (self.precision),
            None if not self.scale else "scale='%s'" % (self.scale),
            None if not self.null_ok else "null_ok='%s'" % (self.null_ok),
        ] if field])

        return 'Column(%s)' % rstr
