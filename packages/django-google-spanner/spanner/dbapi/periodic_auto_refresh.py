# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

"""
The code in this file provides a drop-in replacement for spanner_v1.Transaction,
but one that auto-refreshes every 8.5 seconds, to deal with Cloud Spanner's server's
max idle time of 10 seconds, per:
    https://cloud.google.com/spanner/docs/reference/rest/v1/TransactionOptions#idle-transactions

It handles concurrency concerns by using an event loop, a queue and callbacks. If the queue
is empty for 8.5 seconds, it'll ping Cloud Spanner by sending the recommended:
    execute_sql('SELECT 1')
and then reading the result back.
"""

import queue
import threading
import time


class PeriodicAutoRefresher:
    TICK = 'tick'

    def __init__(self, period_secs=10, ping_fn=None):
        self.__period_secs = period_secs
        self.__done = threading.Event()
        self.__Q = queue.Queue()
        self.__ping_fn = ping_fn
        self.__start_time = time.time()

        pth = threading.Thread(target=self.__event_loop, name='period-auto-refresh')
        pth.start()
        self.__pth = pth

    def __still_running(self):
        return not self.__done.is_set()

    def stop(self):
        self.__done.set()
        self.__pth.join()

    def record_tick(self):
        self.__Q.put_nowait(self.TICK)


class PeriodicAutoRefreshingTransaction:
    """
    PeriodicAutoRefreshingTransaction is the drop-in replacement for spanner_v1.Transaction
    but with a max-idle duration of 8.5 seconds, since the last use time of the underlying
    Transaction, else we'll perform a ping to Cloud Spanner with 'SELECT 1'.

    It becomes active after .begin() has been invoked.
    """

    def __init__(self, txn):
        self.__txn = txn
        self.__running = False
        self.__lock = threading.Lock()
        self.__period_secs = 8.5

    def begin(self):
        res = self.__txn.begin()
        self.__running = True
        self.__start_time = time.time()
        self.__last_active_time = 0

        pth = threading.Thread(target=self.__event_loop, name='periodic-auto-refresh')
        pth.start()
        self.__pth = pth

        return res

    def __event_loop(self):
        while True:
            time.sleep(self.__period_secs)

            self.__lock.acquire()
            running = self.__running
            diff_secs = time.time() - self.__last_active_time
            if not running:
                self.__lock.release()
                return

            if diff_secs >= self.__period_secs:
                self.__ping_locked()
            self.__lock.release()

    def __ping_locked(self):
        print('Pinging Cloud Spanner at %s' % time.time() - self.__start_time)
        res = self.__txn.execute_sql('SELECT 1')
        if res:
            for it in res:
                _ = it

    def execute_sql(self, *args, **kwargs):
        self.__record_last_active_time()
        return self.__txn.execute_sql(*args, **kwargs)

    def execute_update(self, *args, **kwargs):
        self.__record_last_active_time()
        return self.__txn.execute_update(*args, **kwargs)

    def commit(self):
        self.__stop()
        return self.__txn.commit()

    def rollback(self):
        self.__stop()
        return self.__txn.rollback()

    def __stop(self):
        self.__lock.acquire()
        self.__running = False
        self.__lock.release()
        self.__pth.join()

    def __record_last_active_time(self):
        self.__lock.acquire()
        self.__last_active_time = time.time()
        self.__lock.release()

    def was_committed_or_rolledback(self):
        # For now it is alright to access Transaction._rolled_back
        # even though it is unexported. We've filed a follow-up issue:
        #   https://github.com/googleapis/python-spanner/issues/13
        self.__lock.acquire()
        ok = self.__txn.committed or self.__txn._rolled_back
        self.__lock.release()
        return ok
