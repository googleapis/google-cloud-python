# Copyright (C) 2019  Google LLC
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

import itertools

from collections import namedtuple
from typing import(Iterable, Optional)

from google.protobuf import descriptor_pb2

from gapic.schema import wrappers

# Injected dummy test types

DummyMethod = namedtuple(
    "DummyMethod",
    [
        "input",
        "output",
        "lro",
        "paged_result_field",
        "client_streaming",
        "server_streaming",
    ],
)

DummyMethod.__new__.__defaults__ = (False,) * len(DummyMethod._fields)

DummyMessage = namedtuple("DummyMessage", ["fields", "type", "options"])
DummyMessage.__new__.__defaults__ = (False,) * len(DummyMessage._fields)

DummyField = namedtuple("DummyField",
                        ["message", "enum", "repeated", "field_pb", "meta"])
DummyField.__new__.__defaults__ = (False,) * len(DummyField._fields)

DummyService = namedtuple("DummyService", ["methods"])

DummyApiSchema = namedtuple("DummyApiSchema", ["services", "naming"])
DummyApiSchema.__new__.__defaults__ = (False,) * len(DummyApiSchema._fields)

DummyNaming = namedtuple(
    "DummyNaming", ["warehouse_package_name", "name", "version"])
DummyNaming.__new__.__defaults__ = (False,) * len(DummyNaming._fields)


def message_factory(exp: str,
                    repeated_iter=itertools.repeat(False),
                    enum: Optional[wrappers.EnumType] = None) -> DummyMessage:
    # This mimics the structure of MessageType in the wrappers module:
    # A MessageType has a map from field names to Fields,
    # and a Field has an (optional) MessageType.
    # The 'exp' parameter is a dotted attribute expression
    # used to describe the field and type hierarchy,
    # e.g. "mollusc.cephalopod.coleoid"
    toks = exp.split(".")
    messages = [DummyMessage({}, tok.upper() + "_TYPE") for tok in toks]
    if enum:
        messages[-1] = enum

    for base, field, attr_name, repeated_field in zip(
        messages, messages[1:], toks[1:], repeated_iter
    ):
        base.fields[attr_name] = (DummyField(message=field, repeated=repeated_field)
                                  if isinstance(field, DummyMessage)
                                  else DummyField(enum=field))

    return messages[0]


def enum_factory(name: str, variants: Iterable[str]) -> wrappers.EnumType:
    enum_pb = descriptor_pb2.EnumDescriptorProto(
        name=name,
        value=tuple(
            descriptor_pb2.EnumValueDescriptorProto(name=v, number=i)
            for i, v in enumerate(variants)
        )
    )

    enum = wrappers.EnumType(
        enum_pb=enum_pb,
        values=[wrappers.EnumValueType(enum_value_pb=v) for v in enum_pb.value]
    )

    return enum
