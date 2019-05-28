# Copyright 2019 Google LLC
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

import enum

from proto import _package_info
from proto.marshal.rules.enums import EnumRule


class ProtoEnumMeta(enum.EnumMeta):
    """A metaclass for building and registering protobuf enums."""
    def __new__(mcls, name, bases, attrs):
        # Do not do any special behavior for `proto.Enum` itself.
        if bases[0] == enum.IntEnum:
            return super().__new__(mcls, name, bases, attrs)

        # Get the essential information about the proto package, and where
        # this component belongs within the file.
        package, marshal = _package_info.compile(name, attrs)

        # Run the superclass constructor.
        cls = super().__new__(mcls, name, bases, attrs)

        # Register the enum with the marshal.
        marshal.register(cls, EnumRule(cls))

        # Done; return the class.
        return cls


class Enum(enum.IntEnum, metaclass=ProtoEnumMeta):
    """A enum object that also builds a protobuf enum descriptor."""
    pass
