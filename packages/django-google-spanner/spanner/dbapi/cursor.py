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


    @property
    def description(self):
        raise ProgrammingError('Unimplemented')


    @property
    def rowcount(self):
        raise ProgrammingError('Unimplemented')


    def close(self):
        if not self.__session:
            raise ProgrammingError('Cursor is not connected to the database')

        raise ProgrammingError('Unimplemented')


    def execute(self, operation, *args, **kwargs):
        if not self.__session:
            raise ProgrammingError('Cursor is not connected to the database')

        raise ProgrammingError('Unimplemented')


    def executemany(self, operation, seq_of_params):
        if not self.__session:
            raise ProgrammingError('Cursor is not connected to the database')

        raise ProgrammingError('Unimplemented')


    def fetchone(self):
        raise ProgrammingError('Unimplemented')


    def fetchall(self):
        raise ProgrammingError('Unimplemented')


    @property
    def arraysize(self):
        raise ProgrammingError('Unimplemented')


    def setinputsizes(sizes):
        raise ProgrammingError('Unimplemented')


    def setoutputsize(size, column=None):
        raise ProgrammingError('Unimplemented')


    def close(self):
        raise ProgrammingError('Unimplemented')
