# Copyright 2016 Google Inc.
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

"""Transport for Python logging handler.

Logs directly to the the Stackdriver Logging API with a synchronous call.
"""

from google.cloud.logging.handlers.transports.base import Transport
from google.cloud.logging.resource import Resource


_GLOBAL_RESOURCE = Resource(type='global', labels={})


class SyncTransport(Transport):
    """Basic sychronous transport.

    Uses this library's Logging client to directly make the API call.
    """

    def __init__(self, client, name):
        self.logger = client.logger(name)

    def send(self, record, message, resource=_GLOBAL_RESOURCE):
        """Overrides transport.send().

        :type record: :class:`logging.LogRecord`
        :param record: Python log record that the handler was called with.

        :type message: str
        :param message: The message from the ``LogRecord`` after being
                        formatted by the associated log formatters.
        """
        info = {'message': message, 'python_logger': record.name}
        self.logger.log_struct(info, severity=record.levelname, resource=resource)
