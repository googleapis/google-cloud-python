# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import collections
import copy

from proto.utils import cached_property


class Repeated(collections.MutableSequence):
    """A view around a mutable sequence in protocol buffers.

    This implements the full Python MutableSequence interface, but all methods
    modify the underlying field container directly.
    """
    def __init__(self, sequence, *, marshal):
        """Initialize a wrapper around a protobuf repeated field.

        Args:
            sequence: A protocol buffers repeated field.
            marshal (~.MarshalRegistry): An instantiated marshal, used to
                convert values going to and from this map.
        """
        self._pb = sequence
        self._marshal = marshal

    def __copy__(self):
        """Copy this object and return the copy."""
        return type(self)(self.pb[:], marshal=self._marshal)

    def __delitem__(self, key):
        """Delete the given item."""
        del self.pb[key]

    def __eq__(self, other):
        if hasattr(other, 'pb'):
            return tuple(self.pb) == tuple(other.pb)
        return tuple(self.pb) == tuple(other)

    def __getitem__(self, key):
        """Return the given item."""
        return self.pb[key]

    def __len__(self):
        """Return the length of the sequence."""
        return len(self.pb)

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return repr(self.pb)

    def __setitem__(self, key, value):
        self.pb[key] = value

    def insert(self, index: int, value):
        """Insert ``value`` in the sequence before ``index``."""
        self.pb.insert(index, value)

    def sort(self, *, key: str = None, reverse: bool = False):
        """Stable sort *IN PLACE*."""
        self.pb.sort(key=key, reverse=reverse)

    @property
    def pb(self):
        return self._pb


class RepeatedComposite(Repeated):
    """A view around a mutable sequence of messages in protocol buffers.

    This implements the full Python MutableSequence interface, but all methods
    modify the underlying field container directly.
    """
    @cached_property
    def _pb_type(self):
        """Return the protocol buffer type for this sequence."""
        # There is no public-interface mechanism to determine the type
        # of what should go in the list (and the C implementation seems to
        # have no exposed mechanism at all).
        #
        # If the list has members, use the existing list members to
        # determine the type.
        if len(self.pb) > 0:
            return type(self.pb[0])

        # We have no members in the list.
        # In order to get the type, we create a throw-away copy and add a
        # blank member to it.
        canary = copy.deepcopy(self.pb).add()
        return type(canary)

    def __eq__(self, other):
        if super().__eq__(other):
            return True
        return tuple([i for i in self]) == tuple(other)

    def __getitem__(self, key):
        return self._marshal.to_python(self._pb_type, self.pb[key])

    def __setitem__(self, key, value):
        pb_value = self._marshal.to_proto(self._pb_type, value, strict=True)

        # Protocol buffers does not define a useful __setitem__, so we
        # have to pop everything after this point off the list and reload it.
        after = [pb_value]
        while self.pb[key:]:
            after.append(self.pb.pop(key))
        self.pb.extend(after)

    def insert(self, index: int, value):
        """Insert ``value`` in the sequence before ``index``."""
        pb_value = self._marshal.to_proto(self._pb_type, value, strict=True)

        # Protocol buffers does not define a useful insert, so we have
        # to pop everything after this point off the list and reload it.
        after = [pb_value]
        while self.pb[index:]:
            after.append(self.pb.pop(index))
        self.pb.extend(after)
