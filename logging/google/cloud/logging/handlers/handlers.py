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

"""Python :mod:`logging` handlers for Stackdriver Logging."""

import logging

from google.cloud.logging.handlers.transports import BackgroundThreadTransport

DEFAULT_LOGGER_NAME = 'python'

EXCLUDED_LOGGER_DEFAULTS = ('google.cloud', 'oauth2client')


class CloudLoggingHandler(logging.StreamHandler):
    """Handler that directly makes Stackdriver logging API calls.

    This is a Python standard ``logging`` handler using that can be used to
    route Python standard logging messages directly to the Stackdriver
    Logging API.

    This handler supports both an asynchronous and synchronous transport.

    :type client: :class:`google.cloud.logging.client`
    :param client: the authenticated Google Cloud Logging client for this
                   handler to use

    :type name: str
    :param name: the name of the custom log in Stackdriver Logging. Defaults
                 to 'python'. The name of the Python logger will be represented
                 in the ``python_logger`` field.

    :type transport: type
    :param transport: Class for creating new transport objects. It should
                      extend from the base :class:`.Transport` type and
                      implement :meth`.Transport.send`. Defaults to
                      :class:`.BackgroundThreadTransport`. The other
                      option is :class:`.SyncTransport`.

    Example:

    .. code-block:: python

        import google.cloud.logging
        from google.cloud.logging.handlers import CloudLoggingHandler

        client = google.cloud.logging.Client()
        handler = CloudLoggingHandler(client)

        cloud_logger = logging.getLogger('cloudLogger')
        cloud_logger.setLevel(logging.INFO)
        cloud_logger.addHandler(handler)

        cloud.logger.error('bad news')  # API call

    """

    def __init__(self, client,
                 name=DEFAULT_LOGGER_NAME,
                 transport=BackgroundThreadTransport):
        super(CloudLoggingHandler, self).__init__()
        self.name = name
        self.client = client
        self.transport = transport(client, name)

    def emit(self, record):
        """Actually log the specified logging record.

        Overrides the default emit behavior of ``StreamHandler``.

        See: https://docs.python.org/2/library/logging.html#handler-objects

        :type record: :class:`logging.LogRecord`
        :param record: The record to be logged.
        """
        message = super(CloudLoggingHandler, self).format(record)
        self.transport.send(record, message)


def setup_logging(handler, excluded_loggers=EXCLUDED_LOGGER_DEFAULTS,
                  log_level=logging.INFO):
    """Attach a logging handler to the Python root logger

    Excludes loggers that this library itself uses to avoid
    infinite recursion.

    :type handler: :class:`logging.handler`
    :param handler: the handler to attach to the global handler

    :type excluded_loggers: tuple
    :param excluded_loggers: (Optional) The loggers to not attach the handler
                             to. This will always include the loggers in the
                             path of the logging client itself.

    :type log_level: int
    :param log_level: (Optional) Python logging log level. Defaults to
                      :const:`logging.INFO`.

    Example:

    .. code-block:: python

        import logging
        import google.cloud.logging
        from google.cloud.logging.handlers import CloudLoggingHandler

        client = google.cloud.logging.Client()
        handler = CloudLoggingHandler(client)
        google.cloud.logging.setup_logging(handler)
        logging.getLogger().setLevel(logging.DEBUG)

        logging.error('bad news')  # API call

    """
    all_excluded_loggers = set(excluded_loggers + EXCLUDED_LOGGER_DEFAULTS)
    logger = logging.getLogger()
    logger.setLevel(log_level)
    logger.addHandler(handler)
    logger.addHandler(logging.StreamHandler())
    for logger_name in all_excluded_loggers:
        logger = logging.getLogger(logger_name)
        logger.propagate = False
        logger.addHandler(logging.StreamHandler())
