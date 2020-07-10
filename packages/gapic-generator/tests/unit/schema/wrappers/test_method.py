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
from typing import Sequence

from google.api import field_behavior_pb2
from google.api import http_pb2
from google.protobuf import descriptor_pb2

from gapic.schema import metadata
from gapic.schema import wrappers

from test_utils.test_utils import (
    make_enum,
    make_field,
    make_message,
    make_method,
)


def test_method_types():
    input_msg = make_message(name='Input', module='baz')
    output_msg = make_message(name='Output', module='baz')
    method = make_method('DoSomething', input_msg, output_msg,
                         package='foo.bar', module='bacon')
    assert method.name == 'DoSomething'
    assert method.input.name == 'Input'
    assert method.output.name == 'Output'


def test_method_void():
    empty = make_message(name='Empty', package='google.protobuf')
    method = make_method('Meh', output_message=empty)
    assert method.void


def test_method_not_void():
    not_empty = make_message(name='OutputMessage', package='foo.bar.v1')
    method = make_method('Meh', output_message=not_empty)
    assert not method.void


def test_method_client_output():
    output = make_message(name='Input', module='baz')
    method = make_method('DoStuff', output_message=output)
    assert method.client_output is method.output


def test_method_client_output_empty():
    empty = make_message(name='Empty', package='google.protobuf')
    method = make_method('Meh', output_message=empty)
    assert method.client_output == wrappers.PrimitiveType.build(None)


def test_method_client_output_paged():
    paged = make_field(name='foos', message=make_message('Foo'), repeated=True)
    input_msg = make_message(name='ListFoosRequest', fields=(
        make_field(name='parent', type=9),      # str
        make_field(name='page_size', type=5),   # int
        make_field(name='page_token', type=9),  # str
    ))
    output_msg = make_message(name='ListFoosResponse', fields=(
        paged,
        make_field(name='next_page_token', type=9),  # str
    ))
    method = make_method('ListFoos',
                         input_message=input_msg,
                         output_message=output_msg,
                         )
    assert method.paged_result_field == paged
    assert method.client_output.ident.name == 'ListFoosPager'


def test_method_client_output_async_empty():
    empty = make_message(name='Empty', package='google.protobuf')
    method = make_method('Meh', output_message=empty)
    assert method.client_output_async == wrappers.PrimitiveType.build(None)


def test_method_paged_result_field_not_first():
    paged = make_field(name='foos', message=make_message('Foo'), repeated=True)
    input_msg = make_message(name='ListFoosRequest', fields=(
        make_field(name='parent', type=9),      # str
        make_field(name='page_size', type=5),   # int
        make_field(name='page_token', type=9),  # str
    ))
    output_msg = make_message(name='ListFoosResponse', fields=(
        make_field(name='next_page_token', type=9),  # str
        paged,
    ))
    method = make_method('ListFoos',
                         input_message=input_msg,
                         output_message=output_msg,
                         )
    assert method.paged_result_field == paged


def test_method_paged_result_field_no_page_field():
    input_msg = make_message(name='ListFoosRequest', fields=(
        make_field(name='parent', type=9),      # str
        make_field(name='page_size', type=5),   # int
        make_field(name='page_token', type=9),  # str
    ))
    output_msg = make_message(name='ListFoosResponse', fields=(
        make_field(name='foos', message=make_message('Foo'), repeated=False),
        make_field(name='next_page_token', type=9),  # str
    ))
    method = make_method('ListFoos',
                         input_message=input_msg,
                         output_message=output_msg,
                         )
    assert method.paged_result_field is None


def test_method_paged_result_ref_types():
    input_msg = make_message(
        name='ListSquidsRequest',
        fields=(
            make_field(name='parent', type=9),      # str
            make_field(name='page_size', type=5),   # int
            make_field(name='page_token', type=9),  # str
        ),
        module='squid',
    )
    mollusc_msg = make_message('Mollusc', module='mollusc')
    output_msg = make_message(
        name='ListMolluscsResponse',
        fields=(
            make_field(name='molluscs', message=mollusc_msg, repeated=True),
            make_field(name='next_page_token', type=9)
        ),
        module='mollusc'
    )
    method = make_method(
        'ListSquids',
        input_message=input_msg,
        output_message=output_msg,
        module='squid'
    )

    ref_type_names = {t.name for t in method.ref_types}
    assert ref_type_names == {
        'ListSquidsRequest',
        'ListSquidsPager',
        'ListSquidsAsyncPager',
        'Mollusc',
    }


def test_flattened_ref_types():
    method = make_method(
        'IdentifyMollusc',
        input_message=make_message(
            'IdentifyMolluscRequest',
            fields=(
                make_field(
                    'cephalopod',
                    message=make_message(
                        'Cephalopod',
                        fields=(
                            make_field('mass_kg', type='TYPE_INT32'),
                            make_field(
                                'squid',
                                number=2,
                                message=make_message('Squid'),
                            ),
                            make_field(
                                'clam',
                                number=3,
                                message=make_message('Clam'),
                            ),
                        ),
                    ),
                ),
                make_field(
                    'stratum',
                    enum=make_enum(
                        'Stratum',
                    )
                ),
            ),
        ),
        signatures=('cephalopod.squid,stratum',),
        output_message=make_message('Mollusc'),
    )

    expected_flat_ref_type_names = {
        'IdentifyMolluscRequest',
        'Squid',
        'Stratum',
        'Mollusc',
    }
    actual_flat_ref_type_names = {t.name for t in method.flat_ref_types}
    assert expected_flat_ref_type_names == actual_flat_ref_type_names


def test_method_paged_result_primitive():
    paged = make_field(name='squids', type=9, repeated=True)
    input_msg = make_message(
        name='ListSquidsRequest',
        fields=(
            make_field(name='parent', type=9),      # str
            make_field(name='page_size', type=5),   # int
            make_field(name='page_token', type=9),  # str
        ),
    )
    output_msg = make_message(name='ListFoosResponse', fields=(
        paged,
        make_field(name='next_page_token', type=9),  # str
    ))
    method = make_method(
        'ListSquids',
        input_message=input_msg,
        output_message=output_msg,
    )
    assert method.paged_result_field == paged
    assert method.client_output.ident.name == 'ListSquidsPager'


def test_method_field_headers_none():
    method = make_method('DoSomething')
    assert isinstance(method.field_headers, collections.abc.Sequence)


def test_method_field_headers_present():
    verbs = [
        'get',
        'put',
        'post',
        'delete',
        'patch',
    ]

    for v in verbs:
        rule = http_pb2.HttpRule(**{v: '/v1/{parent=projects/*}/topics'})
        method = make_method('DoSomething', http_rule=rule)
        assert method.field_headers == ('parent',)


def test_method_idempotent_yes():
    http_rule = http_pb2.HttpRule(get='/v1/{parent=projects/*}/topics')
    method = make_method('DoSomething', http_rule=http_rule)
    assert method.idempotent is True


def test_method_idempotent_no():
    http_rule = http_pb2.HttpRule(post='/v1/{parent=projects/*}/topics')
    method = make_method('DoSomething', http_rule=http_rule)
    assert method.idempotent is False


def test_method_idempotent_no_http_rule():
    method = make_method('DoSomething')
    assert method.idempotent is False


def test_method_unary_unary():
    method = make_method('F', client_streaming=False, server_streaming=False)
    assert method.grpc_stub_type == 'unary_unary'


def test_method_unary_stream():
    method = make_method('F', client_streaming=False, server_streaming=True)
    assert method.grpc_stub_type == 'unary_stream'


def test_method_stream_unary():
    method = make_method('F', client_streaming=True, server_streaming=False)
    assert method.grpc_stub_type == 'stream_unary'


def test_method_stream_stream():
    method = make_method('F', client_streaming=True, server_streaming=True)
    assert method.grpc_stub_type == 'stream_stream'


def test_method_flattened_fields():
    a = make_field('a', type=5)  # int
    b = make_field('b', type=5)
    input_msg = make_message('Z', fields=(a, b))
    method = make_method('F', input_message=input_msg, signatures=('a,b',))
    assert len(method.flattened_fields) == 2
    assert 'a' in method.flattened_fields
    assert 'b' in method.flattened_fields


def test_method_flattened_fields_empty_sig():
    a = make_field('a', type=5)  # int
    b = make_field('b', type=5)
    input_msg = make_message('Z', fields=(a, b))
    method = make_method('F', input_message=input_msg, signatures=('',))
    assert len(method.flattened_fields) == 0


def test_method_flattened_fields_different_package_non_primitive():
    # This test verifies that method flattening handles a special case where:
    # * the method's request message type lives in a different package and
    # * a field in the method_signature is a non-primitive.
    #
    # If the message is defined in a different package it is not guaranteed to
    # be a proto-plus wrapped type, which puts restrictions on assigning
    # directly to its fields, which complicates request construction.
    # The easiest solution in this case is to just prohibit these fields
    # in the method flattening.
    message = make_message('Mantle',
                           package="mollusc.cephalopod.v1", module="squid")
    mantle = make_field('mantle', type=11, type_name='Mantle',
                        message=message, meta=message.meta)
    arms_count = make_field('arms_count', type=5, meta=message.meta)
    input_message = make_message(
        'Squid', fields=(mantle, arms_count),
        package=".".join(message.meta.address.package),
        module=message.meta.address.module
    )
    method = make_method('PutSquid', input_message=input_message,
                         package="remote.package.v1", module="module", signatures=("mantle,arms_count",))
    assert set(method.flattened_fields) == {'arms_count'}


def test_method_include_flattened_message_fields():
    a = make_field('a', type=5)
    b = make_field('b', type=11, type_name='Eggs',
                   message=make_message('Eggs'))
    input_msg = make_message('Z', fields=(a, b))
    method = make_method('F', input_message=input_msg, signatures=('a,b',))
    assert len(method.flattened_fields) == 2


def test_method_legacy_flattened_fields():
    required_options = descriptor_pb2.FieldOptions()
    required_options.Extensions[field_behavior_pb2.field_behavior].append(
        field_behavior_pb2.FieldBehavior.Value("REQUIRED"))

    # Cephalopods are required.
    squid = make_field(name="squid", options=required_options)
    octopus = make_field(
        name="octopus",
        message=make_message(
            name="Octopus",
            fields=[make_field(name="mass", options=required_options)]
        ),
        options=required_options)

    # Bivalves are optional.
    clam = make_field(name="clam")
    oyster = make_field(
        name="oyster",
        message=make_message(
            name="Oyster",
            fields=[make_field(name="has_pearl")]
        )
    )

    # Interleave required and optional fields to make sure
    # that, in the legacy flattening, required fields are always first.
    request = make_message("request", fields=[squid, clam, octopus, oyster])

    method = make_method(
        name="CreateMolluscs",
        input_message=request,
        # Signatures should be ignored.
        signatures=[
            "squid,octopus.mass",
            "squid,octopus,oyster.has_pearl"
        ]
    )

    # Use an ordered dict because ordering is important:
    # required fields should come first.
    expected = collections.OrderedDict([
        ("squid", squid),
        ("octopus", octopus),
        ("clam", clam),
        ("oyster", oyster)
    ])

    assert method.legacy_flattened_fields == expected


def test_flattened_oneof_fields():
    mass_kg = make_field(name="mass_kg", oneof="mass", type=5)
    mass_lbs = make_field(name="mass_lbs", oneof="mass", type=5)

    length_m = make_field(name="length_m", oneof="length", type=5)
    length_f = make_field(name="length_f", oneof="length", type=5)

    color = make_field(name="color", type=5)
    mantle = make_field(
        name="mantle",
        message=make_message(
            name="Mantle",
            fields=(
                make_field(name="color", type=5),
                mass_kg,
                mass_lbs,
            ),
        ),
    )
    request = make_message(
        name="CreateMolluscReuqest",
        fields=(
            length_m,
            length_f,
            color,
            mantle,
        ),
    )
    method = make_method(
        name="CreateMollusc",
        input_message=request,
        signatures=[
            "length_m,",
            "length_f,",
            "mantle.mass_kg,",
            "mantle.mass_lbs,",
            "color",
        ]
    )

    expected = {"mass": [mass_kg, mass_lbs], "length": [length_m, length_f]}
    actual = method.flattened_oneof_fields()
    assert expected == actual

    # Check this method too becasue the setup is a lot of work.
    expected = {
        "color": "color",
        "length_m": "length_m",
        "length_f": "length_f",
        "mass_kg": "mantle.mass_kg",
        "mass_lbs": "mantle.mass_lbs",
    }
    actual = method.flattened_field_to_key
    assert expected == actual
