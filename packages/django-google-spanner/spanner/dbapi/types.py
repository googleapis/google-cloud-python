# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

# Implements the types requested by the Python Database API in:
#   https://www.python.org/dev/peps/pep-0249/#type-objects-and-constructors

import datetime
import time
from base64 import b64encode


def Date(year, month, day):
    return datetime.date(year, month, day)


def Time(hour, minute, second):
    return datetime.time(hour, minute, second)


def Timestamp(year, month, day, hour, minute, second):
    return datetime.datetime(year, month, day, hour, minute, second)


def DateFromTicks(ticks):
    return Date(*time.localtime(ticks)[:3])


def TimeFromTicks(ticks):
    return Time(*time.localtime(ticks)[3:6])


def TimestampFromTicks(ticks):
    return Timestamp(*time.localtime(ticks)[:6])


def Binary(string):
    """
    Creates an object capable of holding a binary (long) string value.
    """
    return b64encode(string)


class BINARY:
    """
    This object describes (long) binary columns in a database (e.g. LONG, RAW, BLOBS).
    """
    # TODO: Implement me.
    pass


class STRING:
    """
    This object describes columns in a database that are string-based (e.g. CHAR).
    """
    # TODO: Implement me.
    pass


class NUMBER:
    """
    This object describes numeric columns in a database.
    """
    # TODO: Implement me.
    pass


class DATETIME:
    """
    This object describes date/time columns in a database.
    """
    # TODO: Implement me.
    pass


class ROWID:
    """
    This object describes the "Row ID" column in a database.
    """
    # TODO: Implement me.
    pass


class TimestampStr(str):
    """
    TimestampStr exists so that we can purposefully format types as timestamps
    compatible with Cloud Spanner's TIMESTAMP type, but right before making
    queries, it'll help differentiate between normal strings and the case of
    types that should be TIMESTAMP.
    """
    pass


class DateStr(str):
    """
    DateStr is a sentinel type to help format Django dates as
    compatible with Cloud Spanner's DATE type, but right before making
    queries, it'll help differentiate between normal strings and the case of
    types that should be DATE.
    """
    pass
