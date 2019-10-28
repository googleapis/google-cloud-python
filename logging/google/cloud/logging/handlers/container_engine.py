# Copyright 2016 Google LLC All Rights Reserved.
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

"""Logging handler for Google Container Engine (GKE).

Formats log messages in a JSON format, so that Kubernetes clusters with the
fluentd Google Cloud plugin installed can format their log messages so that
metadata such as log level is properly captured.
"""

import logging.handlers

from google.cloud.logging.handlers._helpers import format_stackdriver_json


class ContainerEngineHandler(logging.StreamHandler):
    """Handler to format log messages the format expected by GKE fluent.

    This handler is written to format messages for the Google Container Engine
    (GKE) fluentd plugin, so that metadata such as log level are properly set.

    :type name: str
    :param name: (optional) the name of the custom log in Stackdriver Logging.

    :type stream: file-like object
    :param stream: (optional) stream to be used by the handler.
    """

    def __init__(self, name=None, stream=None):
        super(ContainerEngineHandler, self).__init__(stream=stream)
        self.name = name

    def format(self, record):
        """Format the message into JSON expected by fluentd.

        :type record: :class:`~logging.LogRecord`
        :param record: the log record

        :rtype: str
        :returns: A JSON string formatted for GKE fluentd.
        """
        message = super(ContainerEngineHandler, self).format(record)
        return format_stackdriver_json(record, message)
