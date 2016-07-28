# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Transport classes for Python logging integration

Currently two options are provided, a synchronous transport that makes
an API call for each log statement, and an asynchronous handler that
sends the API using a :class:`gcloud.logging.Batch` object in the background.
"""

from gcloud.logging.handlers.transports.base import Transport
from gcloud.logging.handlers.transports.sync import SyncTransport
from gcloud.logging.handlers.transports.background_thread import (
    BackgroundThreadTransport)
