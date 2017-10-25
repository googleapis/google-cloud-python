# Copyright 2017 Google Inc.
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

"""Helpers for :mod:`protobuf`."""

import collections
import inspect

from google.protobuf.message import Message


def from_any_pb(pb_type, any_pb):
    """Converts an ``Any`` protobuf to the specified message type.

    Args:
        pb_type (type): the type of the message that any_pb stores an instance
            of.
        any_pb (google.protobuf.any_pb2.Any): the object to be converted.

    Returns:
        pb_type: An instance of the pb_type message.

    Raises:
        TypeError: if the message could not be converted.
    """
    msg = pb_type()
    if not any_pb.Unpack(msg):
        raise TypeError(
            'Could not convert {} to {}'.format(
                any_pb.__class__.__name__, pb_type.__name__))

    return msg


def check_oneof(**kwargs):
    """Raise ValueError if more than one keyword argument is not none.
    Args:
        kwargs (dict): The keyword arguments sent to the function.
    Raises:
        ValueError: If more than one entry in kwargs is not none.
    """
    # Sanity check: If no keyword arguments were sent, this is fine.
    if not kwargs:
        return

    not_nones = [val for val in kwargs.values() if val is not None]
    if len(not_nones) > 1:
        raise ValueError('Only one of {fields} should be set.'.format(
            fields=', '.join(sorted(kwargs.keys())),
        ))


def get_messages(module):
    """Return a dictionary of message names and objects.
    Args:
        module (module): A Python module; dir() will be run against this
            module to find Message subclasses.
    Returns:
        dict[str, Message]: A dictionary with the Message class names as
            keys, and the Message subclasses themselves as values.
    """
    answer = collections.OrderedDict()
    for name in dir(module):
        candidate = getattr(module, name)
        if inspect.isclass(candidate) and issubclass(candidate, Message):
            answer[name] = candidate
    return answer
