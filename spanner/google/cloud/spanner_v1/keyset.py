# Copyright 2016 Google LLC All rights reserved.
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

"""Wrap representation of Spanner keys / ranges."""

from google.cloud.spanner_v1.proto.keys_pb2 import KeyRange as KeyRangePB
from google.cloud.spanner_v1.proto.keys_pb2 import KeySet as KeySetPB

from google.cloud.spanner_v1._helpers import _make_list_value_pb
from google.cloud.spanner_v1._helpers import _make_list_value_pbs


class KeyRange(object):
    """Identify range of table rows via start / end points.

    :type start_open: list of scalars
    :param start_open: keys identifying start of range (this key excluded)

    :type start_closed: list of scalars
    :param start_closed: keys identifying start of range (this key included)

    :type end_open: list of scalars
    :param end_open: keys identifying end of range (this key excluded)

    :type end_closed: list of scalars
    :param end_closed: keys identifying end of range (this key included)
    """
    def __init__(self, start_open=None, start_closed=None,
                 end_open=None, end_closed=None):
        if not any([start_open, start_closed, end_open, end_closed]):
            raise ValueError("Must specify at least a start or end row.")

        if start_open and start_closed:
            raise ValueError("Specify one of 'start_open' / 'start_closed'.")

        if end_open and end_closed:
            raise ValueError("Specify one of 'end_open' / 'end_closed'.")

        self.start_open = start_open
        self.start_closed = start_closed
        self.end_open = end_open
        self.end_closed = end_closed

    def to_pb(self):
        """Construct a KeyRange protobuf.

        :rtype: :class:`~google.cloud.spanner_v1.proto.keys_pb2.KeyRange`
        :returns: protobuf corresponding to this instance.
        """
        kwargs = {}

        if self.start_open:
            kwargs['start_open'] = _make_list_value_pb(self.start_open)

        if self.start_closed:
            kwargs['start_closed'] = _make_list_value_pb(self.start_closed)

        if self.end_open:
            kwargs['end_open'] = _make_list_value_pb(self.end_open)

        if self.end_closed:
            kwargs['end_closed'] = _make_list_value_pb(self.end_closed)

        return KeyRangePB(**kwargs)


class KeySet(object):
    """Identify table rows via keys / ranges.

    :type keys: list of list of scalars
    :param keys: keys identifying individual rows within a table.

    :type ranges: list of :class:`KeyRange`
    :param ranges: ranges identifying rows within a table.

    :type all_: boolean
    :param all_: if True, identify all rows within a table
    """
    def __init__(self, keys=(), ranges=(), all_=False):
        if all_ and (keys or ranges):
            raise ValueError("'all_' is exclusive of 'keys' / 'ranges'.")
        self.keys = list(keys)
        self.ranges = list(ranges)
        self.all_ = all_

    def to_pb(self):
        """Construct a KeySet protobuf.

        :rtype: :class:`~google.cloud.spanner_v1.proto.keys_pb2.KeySet`
        :returns: protobuf corresponding to this instance.
        """
        if self.all_:
            return KeySetPB(all=True)
        kwargs = {}

        if self.keys:
            kwargs['keys'] = _make_list_value_pbs(self.keys)

        if self.ranges:
            kwargs['ranges'] = [krange.to_pb() for krange in self.ranges]

        return KeySetPB(**kwargs)
