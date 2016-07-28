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

"""Transport for Python logging handler that logs directly to the the
Stackdriver Logging API with a synchronous call."""

from gcloud.logging.handlers.transports.base import Transport


class SyncTransport(Transport):
    """Basic sychronous transport that uses this library's Logging client to
    directly make the API call"""

    def __init__(self, client, name):
        super(SyncTransport, self).__init__(client, name)
        self.logger = client.logger(name)

    def send(self, record, message):
        """Overrides transport.send(). record is the LogRecord
        the handler was called with, message is the message from LogRecord
        after being formatted by associated log formatters.

        :type record: :class:`logging.LogRecord`
        :param record: Python log record

        :type message: str
        :param message: The formatted log message
        """
        self.logger.log_struct({"message": message,
                                "python_logger": record.name},
                               severity=record.levelname)
