# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

from .autocommit_off_cursor import Cursor
from .base_connection import BaseConnection
from .periodic_auto_refresh import PeriodicAutoRefreshingTransaction


class Connection(BaseConnection):
    def __init__(self, db_handle, session, discard_session):
        super().__init__(db_handle)
        self.__sess = session
        self.__discard_session = discard_session
        self.__txn = None
        self.__on_transaction_clean_up = None
        self._ddl_statements = []

    def close(self):
        self.rollback()
        self.__clear()
        self._closed = True

    def __enter__(self):
        return self

    def __clear(self):
        self._dbhandle = None
        self.__discard_session()
        self.__sess = None

    def __exit__(self, etype, value, traceback):
        self._raise_if_already_closed()

        self.run_prior_DDL_statements()

        if not etype:  # Not an exception thus we should commit.
            self.commit()
        else:  # An exception occured within the context so rollback.
            self.rollback()

        self.__clear()

    def __can_commit_or_rollback(self):
        # For now it is alright to access Transaction._rolled_back
        # even though it is unexported. We've filed a follow-up issue:
        #   https://github.com/googleapis/python-spanner/issues/13
        return self.__txn and not (self.__txn.committed or self.__txn._rolled_back)

    def __clean_up_transaction_state(self):
        if self.__on_transaction_clean_up:
            self.__on_transaction_clean_up()

    def commit(self):
        self.__clean_up_transaction_state()

        if self.__can_commit_or_rollback():
            res = self.__txn.commit()
            self.__txn = None
            return res
        elif hasattr(self.__txn, 'stop'):
            self.__txn.stop()

    def rollback(self):
        self.__clean_up_transaction_state()

        if self.__can_commit_or_rollback():
            res = self.__txn.rollback()
            self.__txn = None
            return res
        elif hasattr(self.__txn, 'stop'):
            self.__txn.stop()

    def cursor(self):
        self._raise_if_already_closed()

        cur = Cursor(self)
        self.__on_transaction_clean_up = cur._clear_transaction_state
        return cur

    def discard_aborted_txn(self):
        # Discard the prior, now bad transaction.
        if hasattr(self.__txn, 'stop'):
            self.__txn.stop()
        self.__txn = None

    def get_txn(self):
        self.run_prior_DDL_statements()

        if not self.__txn:
            if True:  # An easy toggle for if we need to switch to plain Transactions.
                self.__txn = self.__sess.transaction()
            else:
                self.__txn = PeriodicAutoRefreshingTransaction(self.__sess.transaction())

            self.__txn.begin()

        # For now it is alright to access Transaction._rolled_back
        # even though it is unexported. We've filed a follow-up issue:
        #   https://github.com/googleapis/python-spanner/issues/13
        if self.__txn.committed or self.__txn._rolled_back:
            self.discard_aborted_txn()
            # Retry getting that transaction afresh.
            self.__txn = self.get_txn()

        return self.__txn
