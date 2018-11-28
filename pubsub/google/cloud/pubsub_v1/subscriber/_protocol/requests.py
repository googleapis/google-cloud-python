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

"""Base class for concurrency policy."""

from __future__ import absolute_import, division

import collections

# Namedtuples for management requests. Used by the Message class to communicate
# items of work back to the policy.
AckRequest = collections.namedtuple(
    "AckRequest", ["ack_id", "byte_size", "time_to_ack"]
)

DropRequest = collections.namedtuple("DropRequest", ["ack_id", "byte_size"])

LeaseRequest = collections.namedtuple("LeaseRequest", ["ack_id", "byte_size"])

ModAckRequest = collections.namedtuple("ModAckRequest", ["ack_id", "seconds"])

NackRequest = collections.namedtuple("NackRequest", ["ack_id", "byte_size"])
