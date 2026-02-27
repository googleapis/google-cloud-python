#  Copyright 2026 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
"""Spanner Python Driver."""
import logging
from typing import Final

from .connection import Connection, connect
from .cursor import Cursor
from .dbapi import apilevel, paramstyle, threadsafety
from .errors import (
    DatabaseError,
    DataError,
    Error,
    IntegrityError,
    InterfaceError,
    InternalError,
    NotSupportedError,
    OperationalError,
    ProgrammingError,
    Warning,
)
from .types import (
    BINARY,
    DATETIME,
    NUMBER,
    ROWID,
    STRING,
    Binary,
    Date,
    DateFromTicks,
    Time,
    TimeFromTicks,
    Timestamp,
    TimestampFromTicks,
)

__version__: Final[str] = "0.0.1"

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

__all__: list[str] = [
    "apilevel",
    "threadsafety",
    "paramstyle",
    "Connection",
    "connect",
    "Cursor",
    "Date",
    "Time",
    "Timestamp",
    "DateFromTicks",
    "TimeFromTicks",
    "TimestampFromTicks",
    "Binary",
    "STRING",
    "BINARY",
    "NUMBER",
    "DATETIME",
    "ROWID",
    "InterfaceError",
    "ProgrammingError",
    "OperationalError",
    "DatabaseError",
    "DataError",
    "NotSupportedError",
    "IntegrityError",
    "InternalError",
    "Warning",
    "Error",
]
