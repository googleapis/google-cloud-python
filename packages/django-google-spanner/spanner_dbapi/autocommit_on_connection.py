# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

from .autocommit_on_cursor import Cursor
from .base_connection import BaseConnection


class Connection(BaseConnection):
    def close(self):
        self.rollback()
        self.__dbhandle = None
        self._closed = True

    def __enter__(self):
        return self

    def __exit__(self, etype, value, traceback):
        self.commit()
        self.close()

    def commit(self):
        self._raise_if_already_closed()

        self.run_prior_DDL_statements()

    def rollback(self):
        self._raise_if_already_closed()

        # TODO: to be added.

    def cursor(self):
        self._raise_if_already_closed()

        return Cursor(self)
