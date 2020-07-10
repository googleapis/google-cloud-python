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
import re
from typing import Sequence, Tuple

import pytest

from google.api import resource_pb2
from google.protobuf import descriptor_pb2

from gapic.schema import metadata
from gapic.schema import wrappers

from test_utils.test_utils import (
    make_enum,
    make_field,
    make_message,
)


def test_message_properties():
    message = make_message('MyMessage')
    assert message.name == 'MyMessage'


def test_message_docstring():
    L = descriptor_pb2.SourceCodeInfo.Location

    meta = metadata.Metadata(documentation=L(
        leading_comments='Lorem ipsum',
        trailing_comments='dolor set amet',
    ))
    message = make_message('Name', meta=meta)
    assert message.meta.doc == 'Lorem ipsum'


def test_message_ident():
    message = make_message('Baz', package='foo.v1', module='bar')
    assert str(message.ident) == 'bar.Baz'
    assert message.ident.sphinx == '~.bar.Baz'


def test_message_ident_collisions():
    message = make_message('Baz', package='foo.v1', module='bar').with_context(
        collisions={'bar'},
    )
    assert str(message.ident) == 'fv_bar.Baz'
    assert message.ident.sphinx == '~.fv_bar.Baz'


def test_get_field():
    fields = (make_field('field_one'), make_field('field_two'))
    message = make_message('Message', fields=fields)
    field_one = message.get_field('field_one')
    assert isinstance(field_one, wrappers.Field)
    assert field_one.name == 'field_one'


def test_field_types():
    # Create the inner message.
    inner_msg = make_message(
        'InnerMessage',
        fields=(
            make_field(
                'hidden_message',
                message=make_message('HiddenMessage'),
            ),
        )
    )
    inner_enum = make_enum('InnerEnum')

    # Create the outer message, which contains an Inner as a field.
    fields = (
        make_field('inner_message', message=inner_msg),
        make_field('inner_enum', enum=inner_enum),
        make_field('not_interesting'),
    )
    outer = make_message('Outer', fields=fields)

    # Assert that composite field types are recognized but primitives are not.
    assert len(outer.field_types) == 2
    assert inner_msg in outer.field_types
    assert inner_enum in outer.field_types


def test_field_types_recursive():
    enumeration = make_enum('Enumeration')
    innest_msg = make_message(
        'InnestMessage',
        fields=(
            make_field('enumeration', enum=enumeration),
        )
    )
    inner_msg = make_message(
        'InnerMessage',
        fields=(
            make_field('innest_message', message=innest_msg),
        )
    )
    topmost_msg = make_message(
        'TopmostMessage',
        fields=(
            make_field('inner_message', message=inner_msg),
            make_field('uninteresting')
        )
    )

    actual = {t.name for t in topmost_msg.recursive_field_types}
    expected = {t.name for t in (enumeration, innest_msg, inner_msg)}
    assert actual == expected


def test_get_field_recursive():
    # Create the inner message.
    inner_fields = (make_field('zero'), make_field('one'))
    inner = make_message('Inner', fields=inner_fields, package='foo.v1')

    # Create the outer message, which contains an Inner as a field.
    outer_field = make_field('inner', message=inner)
    outer = make_message('Outer', fields=(outer_field,))

    # Assert that a recusive retrieval works.
    assert outer.get_field('inner', 'zero') == inner_fields[0]
    assert outer.get_field('inner', 'one') == inner_fields[1]


def test_get_field_nested_not_found_error():
    # Create the inner message.
    inner_field = make_field('zero')
    inner = make_message('Inner', fields=(inner_field,), package='foo.v1')

    # Create the outer message, which contains an Inner as a field.
    outer_field = make_field('inner', message=inner)
    outer = make_message('Outer', fields=(outer_field,))

    # Assert that a recusive retrieval fails.
    with pytest.raises(KeyError):
        assert outer.get_field('inner', 'zero', 'beyond')


def test_get_field_nonterminal_repeated_error():
    # Create the inner message.
    inner_fields = (make_field('zero'), make_field('one'))
    inner = make_message('Inner', fields=inner_fields, package='foo.v1')

    # Create the outer message, which contains an Inner as a field.
    outer_field = make_field('inner', message=inner, repeated=True)
    outer = make_message('Outer', fields=(outer_field,))

    # Assert that a recusive retrieval fails.
    with pytest.raises(KeyError):
        assert outer.get_field('inner', 'zero') == inner_fields[0]
    with pytest.raises(KeyError):
        assert outer.get_field('inner', 'one') == inner_fields[1]


def test_resource_path():
    options = descriptor_pb2.MessageOptions()
    resource = options.Extensions[resource_pb2.resource]
    resource.pattern.append(
        "kingdoms/{kingdom}/phyla/{phylum}/classes/{klass}")
    resource.pattern.append(
        "kingdoms/{kingdom}/divisions/{division}/classes/{klass}")
    resource.type = "taxonomy.biology.com/Class"
    message = make_message('Squid', options=options)

    assert message.resource_path == "kingdoms/{kingdom}/phyla/{phylum}/classes/{klass}"
    assert message.resource_path_args == ["kingdom", "phylum", "klass"]
    assert message.resource_type == "Class"


def test_parse_resource_path():
    options = descriptor_pb2.MessageOptions()
    resource = options.Extensions[resource_pb2.resource]
    resource.pattern.append(
        "kingdoms/{kingdom}/phyla/{phylum}/classes/{klass}"
    )
    resource.type = "taxonomy.biology.com/Klass"
    message = make_message('Klass', options=options)

    # Plausible resource ID path
    path = "kingdoms/animalia/phyla/mollusca/classes/cephalopoda"
    expected = {
        'kingdom': 'animalia',
        'phylum': 'mollusca',
        'klass': 'cephalopoda',
    }
    actual = re.match(message.path_regex_str, path).groupdict()

    assert expected == actual

    options2 = descriptor_pb2.MessageOptions()
    resource2 = options2.Extensions[resource_pb2.resource]
    resource2.pattern.append(
        "kingdoms-{kingdom}_{phylum}#classes%{klass}"
    )
    resource2.type = "taxonomy.biology.com/Klass"
    message2 = make_message('Klass', options=options2)

    # Plausible resource ID path from a non-standard schema
    path2 = "kingdoms-Animalia/_Mollusca~#classes%Cephalopoda"
    expected2 = {
        'kingdom': 'Animalia/',
        'phylum': 'Mollusca~',
        'klass': 'Cephalopoda',
    }
    actual2 = re.match(message2.path_regex_str, path2).groupdict()

    assert expected2 == actual2


def test_field_map():
    # Create an Entry message.
    entry_msg = make_message(
        name='FooEntry',
        fields=(
            make_field(name='key', type=9),
            make_field(name='value', type=9),
        ),
        options=descriptor_pb2.MessageOptions(map_entry=True),
    )
    entry_field = make_field('foos', message=entry_msg, repeated=True)
    assert entry_msg.map
    assert entry_field.map


def test_oneof_fields():
    mass_kg = make_field(name="mass_kg", oneof="mass", type=5)
    mass_lbs = make_field(name="mass_lbs", oneof="mass", type=5)
    length_m = make_field(name="length_m", oneof="length", type=5)
    length_f = make_field(name="length_f", oneof="length", type=5)
    color = make_field(name="color", type=5)
    request = make_message(
        name="CreateMolluscReuqest",
        fields=(
            mass_kg,
            mass_lbs,
            length_m,
            length_f,
            color,
        ),
    )
    actual_oneofs = request.oneof_fields()
    expected_oneofs = {
        "mass": [mass_kg, mass_lbs],
        "length": [length_m, length_f],
    }
