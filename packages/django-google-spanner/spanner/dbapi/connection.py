# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

from .autocommit_off_connection import Connection as FutureConnection
# This Connection and Cursor combination worked alright before holding
# long-lived transactions. The purpose of this code is to ensure that
# we can develop in parallel with passing builds without blocking
# use of refreshing/single transactions, and that would be code
# before commit 14d52904e884e8557162d9a3f4648804a751473a.
from .autocommit_on_connection import Connection as PastConnection


def Connection(autocommit, *args, **kwargs):
    if autocommit:
        return PastConnection(*args, **kwargs)
    else:
        return FutureConnection(*args, **kwargs)
