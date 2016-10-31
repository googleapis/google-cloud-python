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

"""Common logging helpers."""


from google.cloud.logging.entries import ProtobufEntry
from google.cloud.logging.entries import StructEntry
from google.cloud.logging.entries import TextEntry


def entry_from_resource(resource, client, loggers):
    """Detect correct entry type from resource and instantiate.

    :type resource: dict
    :param resource: One entry resource from API response.

    :type client: :class:`~google.cloud.logging.client.Client`
    :param client: Client that owns the log entry.

    :type loggers: dict
    :param loggers:
        A mapping of logger fullnames -> loggers.  If the logger
        that owns the entry is not in ``loggers``, the entry
        will have a newly-created logger.

    :rtype: :class:`~google.cloud.logging.entries._BaseEntry`
    :returns: The entry instance, constructed via the resource
    """
    if 'textPayload' in resource:
        return TextEntry.from_api_repr(resource, client, loggers)
    elif 'jsonPayload' in resource:
        return StructEntry.from_api_repr(resource, client, loggers)
    elif 'protoPayload' in resource:
        return ProtobufEntry.from_api_repr(resource, client, loggers)

    raise ValueError('Cannot parse log entry resource.')
