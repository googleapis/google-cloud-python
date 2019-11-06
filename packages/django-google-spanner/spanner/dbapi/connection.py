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

from .cursor import Cursor
from .exceptions import Error

class Connection(object):
    def __init__(self, db_handle):
        self.__dbhandle = db_handle
        self.__closed = False


    def __raise_if_already_closed(self):
        """
        Raises an exception if attempting to use an already closed connection.
        """
        if self.__closed:
            raise Error('attempting to use an already closed connection')


    def close(self):
        self.__raise_if_already_closed()
        self.__dbhandle = None
        self.__closed = True


    def __enter__(self):
        return self


    def __exit__(self, etype, value, traceback):
        return self.close()


    def commit(self):
        raise Error('unimplemented')


    def rollback(self):
        raise Error('unimplemented')


    def cursor(self):
        session = self.__dbhandle.session()
        if not session.exists():
            session.create()

        return Cursor(session)


    def update_ddl(self, ddl_statements):
        """
        Runs the list of Data Definition Language (DDL) statements on the specified
        database. Note that each DDL statement MUST NOT contain a semicolon.

        Args:
            ddl_statements: a list of DDL statements, each without a semicolon.

        Returns:
            google.api_core.operation.Operation
        """

        return self.__dbhandle.update_ddl(ddl_statements)
