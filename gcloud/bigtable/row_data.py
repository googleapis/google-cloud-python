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

"""Container for Google Cloud Bigtable Cells and Streaming Row Contents."""


from gcloud._helpers import _datetime_from_microseconds


class Cell(object):
    """Representation of a Google Cloud Bigtable Cell.

    :type value: bytes
    :param value: The value stored in the cell.

    :type timestamp: :class:`datetime.datetime`
    :param timestamp: The timestamp when the cell was stored.

    :type labels: list
    :param labels: (Optional) List of strings. Labels applied to the cell.
    """

    def __init__(self, value, timestamp, labels=()):
        self.value = value
        self.timestamp = timestamp
        self.labels = list(labels)

    @classmethod
    def from_pb(cls, cell_pb):
        """Create a new cell from a Cell protobuf.

        :type cell_pb: :class:`._generated.bigtable_data_pb2.Cell`
        :param cell_pb: The protobuf to convert.

        :rtype: :class:`Cell`
        :returns: The cell corresponding to the protobuf.
        """
        timestamp = _datetime_from_microseconds(cell_pb.timestamp_micros)
        if cell_pb.labels:
            return cls(cell_pb.value, timestamp, labels=cell_pb.labels)
        else:
            return cls(cell_pb.value, timestamp)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (other.value == self.value and
                other.timestamp == self.timestamp and
                other.labels == self.labels)

    def __ne__(self, other):
        return not self.__eq__(other)
