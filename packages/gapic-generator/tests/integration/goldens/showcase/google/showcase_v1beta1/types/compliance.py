# -*- coding: utf-8 -*-
# Copyright 2026 Google LLC
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
#
from __future__ import annotations

from typing import MutableMapping, MutableSequence

import proto  # type: ignore


__protobuf__ = proto.module(
    package='google.showcase.v1beta1',
    manifest={
        'Continent',
        'RepeatRequest',
        'RepeatResponse',
        'ComplianceSuite',
        'ComplianceGroup',
        'ComplianceData',
        'ComplianceDataChild',
        'ComplianceDataGrandchild',
        'EnumRequest',
        'EnumResponse',
    },
)


class Continent(proto.Enum):
    r"""

    Values:
        CONTINENT_UNSPECIFIED (0):
            No description available.
        AFRICA (1):
            No description available.
        AMERICA (2):
            No description available.
        ANTARTICA (3):
            No description available.
        AUSTRALIA (4):
            No description available.
        EUROPE (5):
            No description available.
    """
    CONTINENT_UNSPECIFIED = 0
    AFRICA = 1
    AMERICA = 2
    ANTARTICA = 3
    AUSTRALIA = 4
    EUROPE = 5


class RepeatRequest(proto.Message):
    r"""

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):

        info (google.showcase_v1beta1.types.ComplianceData):

        server_verify (bool):
            If true, the server will verify that the
            received request matches the request with the
            same name in the compliance test suite.
        intended_binding_uri (str):
            The URI template this request is expected to
            be bound to server-side.

            This field is a member of `oneof`_ ``_intended_binding_uri``.
        f_int32 (int):
            Some top level fields, to test that these are
            encoded correctly in query params.
        f_int64 (int):

        f_double (float):

        p_int32 (int):

            This field is a member of `oneof`_ ``_p_int32``.
        p_int64 (int):

            This field is a member of `oneof`_ ``_p_int64``.
        p_double (float):

            This field is a member of `oneof`_ ``_p_double``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    info: 'ComplianceData' = proto.Field(
        proto.MESSAGE,
        number=2,
        message='ComplianceData',
    )
    server_verify: bool = proto.Field(
        proto.BOOL,
        number=3,
    )
    intended_binding_uri: str = proto.Field(
        proto.STRING,
        number=10,
        optional=True,
    )
    f_int32: int = proto.Field(
        proto.INT32,
        number=4,
    )
    f_int64: int = proto.Field(
        proto.INT64,
        number=5,
    )
    f_double: float = proto.Field(
        proto.DOUBLE,
        number=6,
    )
    p_int32: int = proto.Field(
        proto.INT32,
        number=7,
        optional=True,
    )
    p_int64: int = proto.Field(
        proto.INT64,
        number=8,
        optional=True,
    )
    p_double: float = proto.Field(
        proto.DOUBLE,
        number=9,
        optional=True,
    )


class RepeatResponse(proto.Message):
    r"""

    Attributes:
        request (google.showcase_v1beta1.types.RepeatRequest):

        binding_uri (str):
            The URI template the request was bound to
            server-side.
    """

    request: 'RepeatRequest' = proto.Field(
        proto.MESSAGE,
        number=1,
        message='RepeatRequest',
    )
    binding_uri: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ComplianceSuite(proto.Message):
    r"""ComplianceSuite contains a set of requests that
    microgenerators should issue over REST to the Compliance service
    to test their gRPC-to-REST transcoding implementation.

    Attributes:
        group (MutableSequence[google.showcase_v1beta1.types.ComplianceGroup]):

    """

    group: MutableSequence['ComplianceGroup'] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message='ComplianceGroup',
    )


class ComplianceGroup(proto.Message):
    r"""ComplianceGroups encapsulates a group of RPC requests to the
    Compliance server: one request for each combination of elements of
    ``rpcs`` and of ``requests``.

    Attributes:
        name (str):

        rpcs (MutableSequence[str]):

        requests (MutableSequence[google.showcase_v1beta1.types.RepeatRequest]):

    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    rpcs: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )
    requests: MutableSequence['RepeatRequest'] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message='RepeatRequest',
    )


class ComplianceData(proto.Message):
    r"""ComplianceData is a message used for testing REST transcoding
    of different data types.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        f_string (str):

        f_int32 (int):

        f_sint32 (int):

        f_sfixed32 (int):

        f_uint32 (int):

        f_fixed32 (int):

        f_int64 (int):

        f_sint64 (int):

        f_sfixed64 (int):

        f_uint64 (int):

        f_fixed64 (int):

        f_double (float):

        f_float (float):

        f_bool (bool):

        f_bytes (bytes):

        f_kingdom (google.showcase_v1beta1.types.ComplianceData.LifeKingdom):

        f_child (google.showcase_v1beta1.types.ComplianceDataChild):

        p_string (str):
            optional fields

            This field is a member of `oneof`_ ``_p_string``.
        p_int32 (int):

            This field is a member of `oneof`_ ``_p_int32``.
        p_sint32 (int):

            This field is a member of `oneof`_ ``_p_sint32``.
        p_sfixed32 (int):

            This field is a member of `oneof`_ ``_p_sfixed32``.
        p_uint32 (int):

            This field is a member of `oneof`_ ``_p_uint32``.
        p_fixed32 (int):

            This field is a member of `oneof`_ ``_p_fixed32``.
        p_int64 (int):

            This field is a member of `oneof`_ ``_p_int64``.
        p_sint64 (int):

            This field is a member of `oneof`_ ``_p_sint64``.
        p_sfixed64 (int):

            This field is a member of `oneof`_ ``_p_sfixed64``.
        p_uint64 (int):

            This field is a member of `oneof`_ ``_p_uint64``.
        p_fixed64 (int):

            This field is a member of `oneof`_ ``_p_fixed64``.
        p_float (float):

            This field is a member of `oneof`_ ``_p_float``.
        p_double (float):

            This field is a member of `oneof`_ ``_p_double``.
        p_bool (bool):

            This field is a member of `oneof`_ ``_p_bool``.
        p_kingdom (google.showcase_v1beta1.types.ComplianceData.LifeKingdom):
            The proto compiler seems to misgenerate optional bytes
            fields. The generated code looks like:

            ::

               if cmd.Flags().Changed("info.p_bytes") {
                  RepeatDataBodyInfoInput.Info.PBytes = &repeatDataBodyInfoInputInfoPBytes
               }

            The dereference of ``&repeatDataBodyInfoInputInfoPBytes`` is
            incorrect since ``repeatDataBodyInfoInputInfoPBytes`` is
            already a ``byte[]`` optional bytes p_bytes = 49;

            This field is a member of `oneof`_ ``_p_kingdom``.
        p_child (google.showcase_v1beta1.types.ComplianceDataChild):

            This field is a member of `oneof`_ ``_p_child``.
    """
    class LifeKingdom(proto.Enum):
        r"""

        Values:
            LIFE_KINGDOM_UNSPECIFIED (0):
                No description available.
            ARCHAEBACTERIA (1):
                No description available.
            EUBACTERIA (2):
                No description available.
            PROTISTA (3):
                No description available.
            FUNGI (4):
                No description available.
            PLANTAE (5):
                No description available.
            ANIMALIA (6):
                No description available.
        """
        LIFE_KINGDOM_UNSPECIFIED = 0
        ARCHAEBACTERIA = 1
        EUBACTERIA = 2
        PROTISTA = 3
        FUNGI = 4
        PLANTAE = 5
        ANIMALIA = 6

    f_string: str = proto.Field(
        proto.STRING,
        number=1,
    )
    f_int32: int = proto.Field(
        proto.INT32,
        number=2,
    )
    f_sint32: int = proto.Field(
        proto.SINT32,
        number=3,
    )
    f_sfixed32: int = proto.Field(
        proto.SFIXED32,
        number=4,
    )
    f_uint32: int = proto.Field(
        proto.UINT32,
        number=5,
    )
    f_fixed32: int = proto.Field(
        proto.FIXED32,
        number=6,
    )
    f_int64: int = proto.Field(
        proto.INT64,
        number=7,
    )
    f_sint64: int = proto.Field(
        proto.SINT64,
        number=8,
    )
    f_sfixed64: int = proto.Field(
        proto.SFIXED64,
        number=9,
    )
    f_uint64: int = proto.Field(
        proto.UINT64,
        number=10,
    )
    f_fixed64: int = proto.Field(
        proto.FIXED64,
        number=11,
    )
    f_double: float = proto.Field(
        proto.DOUBLE,
        number=12,
    )
    f_float: float = proto.Field(
        proto.FLOAT,
        number=13,
    )
    f_bool: bool = proto.Field(
        proto.BOOL,
        number=14,
    )
    f_bytes: bytes = proto.Field(
        proto.BYTES,
        number=15,
    )
    f_kingdom: LifeKingdom = proto.Field(
        proto.ENUM,
        number=22,
        enum=LifeKingdom,
    )
    f_child: 'ComplianceDataChild' = proto.Field(
        proto.MESSAGE,
        number=16,
        message='ComplianceDataChild',
    )
    p_string: str = proto.Field(
        proto.STRING,
        number=17,
        optional=True,
    )
    p_int32: int = proto.Field(
        proto.INT32,
        number=18,
        optional=True,
    )
    p_sint32: int = proto.Field(
        proto.SINT32,
        number=39,
        optional=True,
    )
    p_sfixed32: int = proto.Field(
        proto.SFIXED32,
        number=40,
        optional=True,
    )
    p_uint32: int = proto.Field(
        proto.UINT32,
        number=41,
        optional=True,
    )
    p_fixed32: int = proto.Field(
        proto.FIXED32,
        number=42,
        optional=True,
    )
    p_int64: int = proto.Field(
        proto.INT64,
        number=43,
        optional=True,
    )
    p_sint64: int = proto.Field(
        proto.SINT64,
        number=44,
        optional=True,
    )
    p_sfixed64: int = proto.Field(
        proto.SFIXED64,
        number=45,
        optional=True,
    )
    p_uint64: int = proto.Field(
        proto.UINT64,
        number=46,
        optional=True,
    )
    p_fixed64: int = proto.Field(
        proto.FIXED64,
        number=47,
        optional=True,
    )
    p_float: float = proto.Field(
        proto.FLOAT,
        number=48,
        optional=True,
    )
    p_double: float = proto.Field(
        proto.DOUBLE,
        number=19,
        optional=True,
    )
    p_bool: bool = proto.Field(
        proto.BOOL,
        number=20,
        optional=True,
    )
    p_kingdom: LifeKingdom = proto.Field(
        proto.ENUM,
        number=23,
        optional=True,
        enum=LifeKingdom,
    )
    p_child: 'ComplianceDataChild' = proto.Field(
        proto.MESSAGE,
        number=21,
        optional=True,
        message='ComplianceDataChild',
    )


class ComplianceDataChild(proto.Message):
    r"""

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        f_string (str):

        f_float (float):

        f_double (float):

        f_bool (bool):

        f_continent (google.showcase_v1beta1.types.Continent):

        f_child (google.showcase_v1beta1.types.ComplianceDataGrandchild):

        p_string (str):

            This field is a member of `oneof`_ ``_p_string``.
        p_float (float):

            This field is a member of `oneof`_ ``_p_float``.
        p_double (float):

            This field is a member of `oneof`_ ``_p_double``.
        p_bool (bool):

            This field is a member of `oneof`_ ``_p_bool``.
        p_continent (google.showcase_v1beta1.types.Continent):

        p_child (google.showcase_v1beta1.types.ComplianceDataGrandchild):

            This field is a member of `oneof`_ ``_p_child``.
    """

    f_string: str = proto.Field(
        proto.STRING,
        number=1,
    )
    f_float: float = proto.Field(
        proto.FLOAT,
        number=2,
    )
    f_double: float = proto.Field(
        proto.DOUBLE,
        number=3,
    )
    f_bool: bool = proto.Field(
        proto.BOOL,
        number=4,
    )
    f_continent: 'Continent' = proto.Field(
        proto.ENUM,
        number=11,
        enum='Continent',
    )
    f_child: 'ComplianceDataGrandchild' = proto.Field(
        proto.MESSAGE,
        number=5,
        message='ComplianceDataGrandchild',
    )
    p_string: str = proto.Field(
        proto.STRING,
        number=6,
        optional=True,
    )
    p_float: float = proto.Field(
        proto.FLOAT,
        number=7,
        optional=True,
    )
    p_double: float = proto.Field(
        proto.DOUBLE,
        number=8,
        optional=True,
    )
    p_bool: bool = proto.Field(
        proto.BOOL,
        number=9,
        optional=True,
    )
    p_continent: 'Continent' = proto.Field(
        proto.ENUM,
        number=12,
        enum='Continent',
    )
    p_child: 'ComplianceDataGrandchild' = proto.Field(
        proto.MESSAGE,
        number=10,
        optional=True,
        message='ComplianceDataGrandchild',
    )


class ComplianceDataGrandchild(proto.Message):
    r"""

    Attributes:
        f_string (str):

        f_double (float):

        f_bool (bool):

    """

    f_string: str = proto.Field(
        proto.STRING,
        number=1,
    )
    f_double: float = proto.Field(
        proto.DOUBLE,
        number=2,
    )
    f_bool: bool = proto.Field(
        proto.BOOL,
        number=3,
    )


class EnumRequest(proto.Message):
    r"""

    Attributes:
        unknown_enum (bool):
            Whether the client is requesting a new,
            unknown enum value or a known enum value already
            declared in this proto file.
    """

    unknown_enum: bool = proto.Field(
        proto.BOOL,
        number=1,
    )


class EnumResponse(proto.Message):
    r"""

    Attributes:
        request (google.showcase_v1beta1.types.EnumRequest):
            The original request for a known or unknown
            enum from the server.
        continent (google.showcase_v1beta1.types.Continent):
            The actual enum the server provided.
    """

    request: 'EnumRequest' = proto.Field(
        proto.MESSAGE,
        number=1,
        message='EnumRequest',
    )
    continent: 'Continent' = proto.Field(
        proto.ENUM,
        number=2,
        enum='Continent',
    )


__all__ = tuple(sorted(__protobuf__.manifest))
