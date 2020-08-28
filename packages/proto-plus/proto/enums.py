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

from google.protobuf import descriptor_pb2

from proto import _file_info
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

        # Determine the local path of this proto component within the file.
        local_path = tuple(attrs.get("__qualname__", name).split("."))

        # Sanity check: We get the wrong full name if a class is declared
        # inside a function local scope; correct this.
        if "<locals>" in local_path:
            ix = local_path.index("<locals>")
            local_path = local_path[: ix - 1] + local_path[ix + 1 :]

        # Determine the full name in protocol buffers.
        # The C++ proto implementation doesn't like dots in names, so use underscores.
        full_name = "_".join((package,) + local_path).lstrip("_")
        enum_desc = descriptor_pb2.EnumDescriptorProto(
            name=full_name,
            # Note: the superclass ctor removes the variants, so get them now.
            # Note: proto3 requires that the first variant value be zero.
            value=sorted(
                (
                    descriptor_pb2.EnumValueDescriptorProto(name=name, number=number)
                    # Minor hack to get all the enum variants out.
                    for name, number in attrs.items()
                    if isinstance(number, int)
                ),
                key=lambda v: v.number,
            ),
        )

        filename = _file_info._FileInfo.proto_file_name(
            attrs.get("__module__", name.lower())
        )

        file_info = _file_info._FileInfo.maybe_add_descriptor(filename, package)
        file_info.descriptor.enum_type.add().MergeFrom(enum_desc)

        # Run the superclass constructor.
        cls = super().__new__(mcls, name, bases, attrs)

        # We can't just add a "_meta" element to attrs because the Enum
        # machinery doesn't know what to do with a non-int value.
        cls._meta = _EnumInfo(full_name=full_name, pb=enum_desc)

        file_info.enums[full_name] = cls

        # Register the enum with the marshal.
        marshal.register(cls, EnumRule(cls))

        # Done; return the class.
        return cls


class Enum(enum.IntEnum, metaclass=ProtoEnumMeta):
    """A enum object that also builds a protobuf enum descriptor."""

    pass


class _EnumInfo:
    def __init__(self, *, full_name: str, pb):
        self.full_name = full_name
        self.pb = pb
