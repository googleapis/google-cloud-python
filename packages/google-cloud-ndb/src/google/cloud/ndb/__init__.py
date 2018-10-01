# Copyright 2018 Google LLC
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

"""``ndb`` is a library for Google Cloud Datastore.

It was originally included in the Google App Engine runtime as a "new"
version of the ``db`` API (hence ``ndb``).
"""

__version__ = "0.0.1.dev1"
__all__ = [
    "AutoBatcher",
    "Context",
    "ContextOptions",
    "EVENTUAL_CONSISTENCY",
    "TransactionOptions",
    "add_flow_exception",
    "Future",
    "get_context",
    "get_return_value",
    "make_context",
    "make_default_context",
    "MultiFuture",
    "QueueFuture",
    "ReducingFuture",
    "Return",
    "SerialQueueFuture",
    "set_context",
    "sleep",
    "synctasklet",
    "tasklet",
    "toplevel",
]

from google.cloud.ndb.context import AutoBatcher
from google.cloud.ndb.context import Context
from google.cloud.ndb.context import ContextOptions
from google.cloud.ndb.context import EVENTUAL_CONSISTENCY
from google.cloud.ndb.context import TransactionOptions
from google.cloud.ndb.tasklets import add_flow_exception
from google.cloud.ndb.tasklets import Future
from google.cloud.ndb.tasklets import get_context
from google.cloud.ndb.tasklets import get_return_value
from google.cloud.ndb.tasklets import make_context
from google.cloud.ndb.tasklets import make_default_context
from google.cloud.ndb.tasklets import MultiFuture
from google.cloud.ndb.tasklets import QueueFuture
from google.cloud.ndb.tasklets import ReducingFuture
from google.cloud.ndb.tasklets import Return
from google.cloud.ndb.tasklets import SerialQueueFuture
from google.cloud.ndb.tasklets import set_context
from google.cloud.ndb.tasklets import sleep
from google.cloud.ndb.tasklets import synctasklet
from google.cloud.ndb.tasklets import tasklet
from google.cloud.ndb.tasklets import toplevel
