# Copyright 2017, Google LLC All rights reserved.
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

from __future__ import absolute_import

import collections
import enum
import inspect
import sys

import proto

from google.api import http_pb2
from google.api_core import gapic_v1
from google.iam.v1 import iam_policy_pb2
from google.iam.v1 import policy_pb2
from google.iam.v1.logging import audit_data_pb2
from google.protobuf import descriptor_pb2
from google.protobuf import duration_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2
from google.protobuf import timestamp_pb2

from google.api_core.protobuf_helpers import get_messages

from google.pubsub_v1.types import pubsub as pubsub_gapic_types


# Define the default values for batching.
#
# This class is used when creating a publisher or subscriber client, and
# these settings can be altered to tweak Pub/Sub behavior.
# The defaults should be fine for most use cases.
BatchSettings = collections.namedtuple(
    "BatchSettings", ["max_bytes", "max_latency", "max_messages"]
)
BatchSettings.__new__.__defaults__ = (
    1 * 1000 * 1000,  # max_bytes: 1 MB
    0.01,  # max_latency: 10 ms
    100,  # max_messages: 100
)
BatchSettings.__doc__ = "The settings for batch publishing the messages."
BatchSettings.max_bytes.__doc__ = (
    "The maximum total size of the messages to collect before automatically "
    "publishing the batch, including any byte size overhead of the publish "
    "request itself. The maximum value is bound by the server-side limit of "
    "10_000_000 bytes."
)
BatchSettings.max_latency.__doc__ = (
    "The maximum number of seconds to wait for additional messages before "
    "automatically publishing the batch."
)
BatchSettings.max_messages.__doc__ = (
    "The maximum number of messages to collect before automatically "
    "publishing the batch."
)


class LimitExceededBehavior(str, enum.Enum):
    """The possible actions when exceeding the publish flow control limits."""

    IGNORE = "ignore"
    BLOCK = "block"
    ERROR = "error"


PublishFlowControl = collections.namedtuple(
    "PublishFlowControl", ["message_limit", "byte_limit", "limit_exceeded_behavior"]
)
PublishFlowControl.__new__.__defaults__ = (
    10 * BatchSettings.__new__.__defaults__[2],  # message limit
    10 * BatchSettings.__new__.__defaults__[0],  # byte limit
    LimitExceededBehavior.IGNORE,  # desired behavior
)
PublishFlowControl.__doc__ = "The client flow control settings for message publishing."
PublishFlowControl.message_limit.__doc__ = (
    "The maximum number of messages awaiting to be published."
)
PublishFlowControl.byte_limit.__doc__ = (
    "The maximum total size of messages awaiting to be published."
)
PublishFlowControl.limit_exceeded_behavior.__doc__ = (
    "The action to take when publish flow control limits are exceeded."
)

# Define the default publisher options.
#
# This class is used when creating a publisher client to pass in options
# to enable/disable features.
PublisherOptions = collections.namedtuple(
    "PublisherOptions", ["enable_message_ordering", "flow_control", "retry", "timeout"]
)
PublisherOptions.__new__.__defaults__ = (
    False,  # enable_message_ordering: False
    PublishFlowControl(),  # default flow control settings
    gapic_v1.method.DEFAULT,  # use default api_core value for retry
    gapic_v1.method.DEFAULT,  # use default api_core value for timeout
)
PublisherOptions.__doc__ = "The options for the publisher client."
PublisherOptions.enable_message_ordering.__doc__ = (
    "Whether to order messages in a batch by a supplied ordering key."
)
PublisherOptions.flow_control.__doc__ = (
    "Flow control settings for message publishing by the client. By default "
    "the publisher client does not do any throttling."
)
PublisherOptions.retry.__doc__ = (
    "Retry settings for message publishing by the client. This should be "
    "an instance of :class:`google.api_core.retry.Retry`."
)
PublisherOptions.timeout.__doc__ = (
    "Timeout settings for message publishing by the client. It should be compatible "
    "with :class:`~.pubsub_v1.types.TimeoutType`."
)

# Define the type class and default values for flow control settings.
#
# This class is used when creating a publisher or subscriber client, and
# these settings can be altered to tweak Pub/Sub behavior.
# The defaults should be fine for most use cases.
FlowControl = collections.namedtuple(
    "FlowControl",
    [
        "max_bytes",
        "max_messages",
        "max_lease_duration",
        "max_duration_per_lease_extension",
    ],
)
FlowControl.__new__.__defaults__ = (
    100 * 1024 * 1024,  # max_bytes: 100mb
    1000,  # max_messages: 1000
    1 * 60 * 60,  # max_lease_duration: 1 hour.
    0,  # max_duration_per_lease_extension: disabled
)
FlowControl.__doc__ = (
    "The settings for controlling the rate at which messages are pulled "
    "with an asynchronous subscription."
)
FlowControl.max_bytes.__doc__ = (
    "The maximum total size of received - but not yet processed - messages "
    "before pausing the message stream."
)
FlowControl.max_messages.__doc__ = (
    "The maximum number of received - but not yet processed - messages before "
    "pausing the message stream."
)
FlowControl.max_lease_duration.__doc__ = (
    "The maximum amount of time in seconds to hold a lease on a message "
    "before dropping it from the lease management."
)
FlowControl.max_duration_per_lease_extension.__doc__ = (
    "The max amount of time in seconds for a single lease extension attempt. "
    "Bounds the delay before a message redelivery if the subscriber "
    "fails to extend the deadline. Must be between 10 and 600 (inclusive). Ignored "
    "if set to 0."
)


# The current api core helper does not find new proto messages of type proto.Message,
# thus we need our own helper. Adjusted from
# https://github.com/googleapis/python-api-core/blob/8595f620e7d8295b6a379d6fd7979af3bef717e2/google/api_core/protobuf_helpers.py#L101-L118
def _get_protobuf_messages(module):
    """Discover all protobuf Message classes in a given import module.

    Args:
        module (module): A Python module; :func:`dir` will be run against this
            module to find Message subclasses.

    Returns:
        dict[str, proto.Message]: A dictionary with the
            Message class names as keys, and the Message subclasses themselves
            as values.
    """
    answer = collections.OrderedDict()
    for name in dir(module):
        candidate = getattr(module, name)
        if inspect.isclass(candidate) and issubclass(candidate, proto.Message):
            answer[name] = candidate
    return answer


_shared_modules = [
    http_pb2,
    iam_policy_pb2,
    policy_pb2,
    audit_data_pb2,
    descriptor_pb2,
    duration_pb2,
    empty_pb2,
    field_mask_pb2,
    timestamp_pb2,
]

_local_modules = [pubsub_gapic_types]

names = [
    "BatchSettings",
    "LimitExceededBehavior",
    "PublishFlowControl",
    "PublisherOptions",
    "FlowControl",
]

for module in _shared_modules:
    for name, message in get_messages(module).items():
        setattr(sys.modules[__name__], name, message)
        names.append(name)

for module in _local_modules:
    for name, message in _get_protobuf_messages(module).items():
        message.__module__ = "google.cloud.pubsub_v1.types"
        setattr(sys.modules[__name__], name, message)
        names.append(name)


__all__ = tuple(sorted(names))
