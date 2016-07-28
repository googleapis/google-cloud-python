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

"""Base class for Python logging handler Transport objects"""


class Transport(object):
    """Base class for gcloud logging handler Transports.
    Subclasses of Transports must have constructors that accept a client and
    name object, and must override the send method.
    """

    def __init__(self, client, name):
        pass  # pragma: NO COVER

    def send(self, record, message):
        """Must be overriden by transport options. record is the LogRecord
        the handler was called with, message is the message from LogRecord
        after being formatted by associated log formatters.

        :type record: :class:`logging.LogRecord`
        :param record: Python log record

        :type message: str
        :param message: The formatted log message
        """
        raise NotImplementedError()
