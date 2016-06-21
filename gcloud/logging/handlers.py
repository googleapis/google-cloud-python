# Copyright 2016 Google Inc. All rights reserved.
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

"""Python :mod:`logging` handlers for Google Cloud Logging."""

import logging

EXCLUDE_LOGGER_DEFAULTS = (
    'gcloud',
    'oauth2client.client'
)


class CloudLoggingHandler(logging.StreamHandler, object):
    """Python standard logging handler to log messages to the Google Cloud
    Logging API.

    This handler can be used to route Python standard logging messages to
    Google Cloud logging.

    Note that this handler currently only supports a synchronous API call,
    which means each logging statement that uses this handler will require
    an API call.

    :type client: :class:`gcloud.logging.client`
    :param client: the authenticated gcloud logging client for this handler
                   to use

    Example:

    .. doctest::

        import gcloud.logging
        from gcloud.logging.handlers import CloudLoggingHandler

        client = gcloud.logging.Client()
        handler = CloudLoggingHandler(client)

        cloud_logger = logging.getLogger('cloudLogger')
        cloud_logger.setLevel(logging.INFO)
        cloud_logger.addHandler(handler)

        cloud.logger.error("bad news") # API call

    """

    def __init__(self, client):
        super(CloudLoggingHandler, self).__init__()
        self.client = client

    def emit(self, record):
        """
        Overrides the default emit behavior of StreamHandler.

        See: https://docs.python.org/2/library/logging.html#handler-objects
        """
        message = super(CloudLoggingHandler, self).format(record)
        logger = self.client.logger(record.name)
        logger.log_struct({"message": message},
                          severity=record.levelname)


def setup_logging(handler, excluded_loggers=EXCLUDE_LOGGER_DEFAULTS):
    """Helper function to attach the CloudLoggingAPI handler to the Python
    root logger, while excluding loggers this library itself uses to avoid
    infinite recursion

    :type handler: :class:`logging.handler`
    :param handler: the handler to attach to the global handler

    :type excluded_loggers: tuple
    :param excluded_loggers: The loggers to not attach the handler to. This
                             will always include the loggers in the path of
                             the logging client itself.

    Example:

    .. doctest::

        import logging
        import gcloud.logging
        from gcloud.logging.handlers import CloudLoggingAPIHandler

        client = gcloud.logging.Client()
        handler = CloudLoggingHandler(client)
        setup_logging(handler)
        logging.getLogger().setLevel(logging.DEBUG)

        logging.error("bad news") # API call

    """
    all_excluded_loggers = set(excluded_loggers + EXCLUDE_LOGGER_DEFAULTS)
    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.addHandler(logging.StreamHandler())
    for logger_name in all_excluded_loggers:
        logger = logging.getLogger(logger_name)
        logger.propagate = False
        logger.addHandler(logging.StreamHandler())
