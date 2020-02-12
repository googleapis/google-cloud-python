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
    def __init__(self, period_secs=10, ping_fn=None):
        self.__period_secs = period_secs
        self.__Q = queue.Queue()
        self.__ping_fn = ping_fn
        self.__start_time = time.time()

        pth = threading.Thread(target=self.__event_loop, name='period-auto-refresh')
        pth.start()
        self.__pth = pth

    def __event_loop(self):
        while True:
            try:
                head = self.__Q.get(block=True, timeout=self.__period_secs)
                if not head:
                    return

                callback, fn, args, kwargs = head
                res, exc = None, None

                try:
                    res = fn(*args, **kwargs)
                except Exception as e:
                    exc = e
                finally:
                    callback(res, exc)
            except queue.Empty:
                self.__ping_fn()

    def stop(self):
        self.__Q.put_nowait(None)
        self.__pth.join()

    def run_op(self, callback, fn, *args, **kwargs):
        self.__Q.put_nowait((callback, fn, args, kwargs))


class PeriodicAutoRefreshingTransaction:
    """
    PeriodicAutoRefreshingTransaction is the drop-in replacement for spanner_v1.Transaction
    but with a max-idle duration of 8.5 seconds, since the last use time of the underlying
    Transaction, else we'll perform a ping to Cloud Spanner with 'SELECT 1'.
    It becomes active after .begin() has been invoked.
    """

    def __init__(self, txn):
        self.__txn = txn

    def begin(self):
        res = self.__txn.begin()
        self.__par = PeriodicAutoRefresher(period_secs=8.5, ping_fn=self.__ping)
        return res

    def __ping(self):
        if self.__txn.committed or self.__txn._rolled_back:
            print('Already committed or rolledback so cannot ping Cloud Spanner')
            return

        print('Pinging Cloud Spanner at %s' % time.time())
        res = self.__txn.execute_sql('SELECT 1')
        if res:
            for it in res:
                _ = it

    def execute_sql(self, *args, **kwargs):
        return self.__on_event_queue(self.__txn.execute_sql, *args, **kwargs)

    def execute_update(self, *args, **kwargs):
        return self.__on_event_queue(self.__txn.execute_update, *args, **kwargs)

    def commit(self):
        res = self.__on_event_queue(self.__txn.commit)
        self.__par.stop()
        return res

    def rollback(self):
        res = self.__on_event_queue(self.__txn.rollback)
        self.__par.stop()
        return res

    @property
    def committed(self):
        # For now it is alright to access Transaction._rolled_back
        # even though it is unexported. We've filed a follow-up issue:
        #   https://github.com/googleapis/python-spanner/issues/13
        return self.__txn and self.__txn.committed

    @property
    def _rolled_back(self):
        # For now it is alright to access Transaction._rolled_back
        # even though it is unexported. We've filed a follow-up issue:
        #   https://github.com/googleapis/python-spanner/issues/13
        return self.__txn and self.__txn._rolled_back

    def __on_event_queue(self, fn, *args, **kwargs):
        ready = threading.Event()
        res_exc = {}

        # Using a lambda here because a defined closure would have scope/visibility
        # problems trying to set res_exc, even if we used 'global res_exc'. A lambda solves
        # the issue due to different scoping.
        # We have to propagate the underlying results and exceptions from
        # the asynchronously running callback, converting it to a synchronous call.
        callback = lambda in_res, in_exc: (res_exc.setdefault('res', in_res), res_exc.setdefault('exc', in_exc), ready.set())  # noqa

        self.__par.run_op(callback, fn, *args, **kwargs)
        ready.wait()

        res, exc = res_exc['res'], res_exc['exc']

        if exc:
            raise exc

        return res
