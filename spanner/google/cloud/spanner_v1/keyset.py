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

    .. note::

        Exactly one of ``start_open`` and ``start_closed`` must be
        passed and exactly one of ``end_open`` and ``end_closed`` must be.
        To "start at the beginning" (i.e. specify no start for the range)
        pass ``start_closed=[]``. To "go to the end" (i.e. specify no end
        for the range) pass ``end_closed=[]``.

    Args:
        start_open (List): Keys identifying start of range (this key
            excluded).
        start_closed (List): Keys identifying start of range (this key
            included).
        end_open (List): Keys identifying end of range (this key
            excluded).
        end_closed (List): Keys identifying end of range (this key
            included).

    Raises:
        ValueError: If **neither** ``start_open`` or ``start_closed`` is
            passed.
        ValueError: If **both** ``start_open`` and ``start_closed`` are passed.
        ValueError: If **neither** ``end_open`` or ``end_closed`` is passed.
        ValueError: If **both** ``end_open`` and ``end_closed`` are passed.
    """
    def __init__(self, start_open=None, start_closed=None,
                 end_open=None, end_closed=None):
        if ((start_open is None and start_closed is None)
                or (start_open is not None and start_closed is not None)):
            raise ValueError('Specify exactly one of start_closed or start_open')

        if ((end_open is None and end_closed is None)
                or (end_open is not None and end_closed is not None)):
            raise ValueError('Specify exactly one of end_closed or end_open')

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
