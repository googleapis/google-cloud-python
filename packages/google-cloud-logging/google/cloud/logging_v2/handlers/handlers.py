# Copyright 2016 Google LLC
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

"""Python :mod:`logging` handlers for Cloud Logging."""

import logging

from google.cloud.logging_v2.handlers.transports import BackgroundThreadTransport
from google.cloud.logging_v2.logger import _GLOBAL_RESOURCE

DEFAULT_LOGGER_NAME = "python"

EXCLUDED_LOGGER_DEFAULTS = ("google.cloud", "google.auth", "google_auth_httplib2")


class CloudLoggingHandler(logging.StreamHandler):
    """Handler that directly makes Cloud Logging API calls.

    This is a Python standard ``logging`` handler using that can be used to
    route Python standard logging messages directly to the Stackdriver
    Logging API.

    This handler is used when not in GAE or GKE environment.

    This handler supports both an asynchronous and synchronous transport.

    Example:

    .. code-block:: python

        import logging
        import google.cloud.logging
        from google.cloud.logging_v2.handlers import CloudLoggingHandler

        client = google.cloud.logging.Client()
        handler = CloudLoggingHandler(client)

        cloud_logger = logging.getLogger('cloudLogger')
        cloud_logger.setLevel(logging.INFO)
        cloud_logger.addHandler(handler)

        cloud_logger.error('bad news')  # API call
    """

    def __init__(
        self,
        client,
        *,
        name=DEFAULT_LOGGER_NAME,
        transport=BackgroundThreadTransport,
        resource=_GLOBAL_RESOURCE,
        labels=None,
        stream=None,
    ):
        """
        Args:
            client (~logging_v2.client.Client):
                The authenticated Google Cloud Logging client for this
                handler to use.
            name (str): the name of the custom log in Cloud Logging.
                Defaults to 'python'. The name of the Python logger will be represented
                in the ``python_logger`` field.
            transport (~logging_v2.transports.Transport):
                Class for creating new transport objects. It should
                extend from the base :class:`.Transport` type and
                implement :meth`.Transport.send`. Defaults to
                :class:`.BackgroundThreadTransport`. The other
                option is :class:`.SyncTransport`.
            resource (~logging_v2.resource.Resource):
                Resource for this Handler. Defaults to ``GLOBAL_RESOURCE``.
            labels (Optional[dict]): Monitored resource of the entry, defaults
                to the global resource type.
            stream (Optional[IO]): Stream to be used by the handler.
        """
        super(CloudLoggingHandler, self).__init__(stream)
        self.name = name
        self.client = client
        self.transport = transport(client, name)
        self.project_id = client.project
        self.resource = resource
        self.labels = labels

    def emit(self, record):
        """Actually log the specified logging record.

        Overrides the default emit behavior of ``StreamHandler``.

        See https://docs.python.org/2/library/logging.html#handler-objects

        Args:
            record (logging.LogRecord): The record to be logged.
        """
        message = super(CloudLoggingHandler, self).format(record)
        trace_id = getattr(record, "trace", None)
        span_id = getattr(record, "span_id", None)
        http_request = getattr(record, "http_request", None)
        resource = getattr(record, "resource", self.resource)
        user_labels = getattr(record, "labels", {})
        # merge labels
        total_labels = self.labels if self.labels is not None else {}
        total_labels.update(user_labels)
        if len(total_labels) == 0:
            total_labels = None
        # send off request
        self.transport.send(
            record,
            message,
            resource=resource,
            labels=(total_labels if total_labels else None),
            trace=trace_id,
            span_id=span_id,
            http_request=http_request,
        )


def setup_logging(
    handler, *, excluded_loggers=EXCLUDED_LOGGER_DEFAULTS, log_level=logging.INFO
):
    """Attach a logging handler to the Python root logger

    Excludes loggers that this library itself uses to avoid
    infinite recursion.

    Example:

    .. code-block:: python

        import logging
        import google.cloud.logging
        from google.cloud.logging_v2.handlers import CloudLoggingHandler

        client = google.cloud.logging.Client()
        handler = CloudLoggingHandler(client)
        google.cloud.logging.handlers.setup_logging(handler)
        logging.getLogger().setLevel(logging.DEBUG)

        logging.error('bad news')  # API call

    Args:
        handler (logging.handler): the handler to attach to the global handler
        excluded_loggers (Optional[Tuple[str]]): The loggers to not attach the handler
            to. This will always include the loggers in the
            path of the logging client itself.
        log_level (Optional[int]): Python logging log level. Defaults to
            :const:`logging.INFO`.
    """
    all_excluded_loggers = set(excluded_loggers + EXCLUDED_LOGGER_DEFAULTS)
    logger = logging.getLogger()
    logger.setLevel(log_level)
    logger.addHandler(handler)
    for logger_name in all_excluded_loggers:
        logger = logging.getLogger(logger_name)
        logger.propagate = False
        logger.addHandler(logging.StreamHandler())
