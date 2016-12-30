# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""Google BigQuery implementation of the Database API Specification v2.0.

This module implements the `Python Database API Specification v2.0 (DB-API)`_
for Google BigQuery.

.. _Python Database API Specification v2.0 (DB-API):
   https://www.python.org/dev/peps/pep-0249/

.. warning::
   The ``dbapi`` module is **alpha**. The implementation is not complete. It
   might be changed in backward-incompatible ways and is not subject to any SLA
   or deprecation policy.
"""

from google.cloud.bigquery.dbapi.connection import connect  # noqa
from google.cloud.bigquery.dbapi.connection import Connection  # noqa
from google.cloud.bigquery.dbapi.cursor import Cursor  # noqa
from google.cloud.bigquery.dbapi.exceptions import Warning  # noqa
from google.cloud.bigquery.dbapi.exceptions import Error  # noqa
from google.cloud.bigquery.dbapi.exceptions import InterfaceError  # noqa
from google.cloud.bigquery.dbapi.exceptions import DatabaseError  # noqa
from google.cloud.bigquery.dbapi.exceptions import DataError  # noqa
from google.cloud.bigquery.dbapi.exceptions import OperationalError  # noqa
from google.cloud.bigquery.dbapi.exceptions import IntegrityError  # noqa
from google.cloud.bigquery.dbapi.exceptions import InternalError  # noqa
from google.cloud.bigquery.dbapi.exceptions import ProgrammingError  # noqa
from google.cloud.bigquery.dbapi.exceptions import NotSupportedError  # noqa
from google.cloud.bigquery.dbapi.types import Binary  # noqa
from google.cloud.bigquery.dbapi.types import Date  # noqa
from google.cloud.bigquery.dbapi.types import DateFromTicks  # noqa
from google.cloud.bigquery.dbapi.types import Time  # noqa
from google.cloud.bigquery.dbapi.types import TimeFromTicks  # noqa
from google.cloud.bigquery.dbapi.types import Timestamp  # noqa
from google.cloud.bigquery.dbapi.types import TimestampFromTicks  # noqa
from google.cloud.bigquery.dbapi.types import BINARY  # noqa
from google.cloud.bigquery.dbapi.types import DATETIME  # noqa
from google.cloud.bigquery.dbapi.types import NUMBER  # noqa
from google.cloud.bigquery.dbapi.types import ROWID  # noqa
from google.cloud.bigquery.dbapi.types import STRING  # noqa


apilevel = "2.0"

# Threads may share the module, but not connections.
threadsafety = 1

paramstyle = "pyformat"
