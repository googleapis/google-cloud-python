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

import pytest

from google.cloud.ndb import metadata
import tests.unit.utils


def test___all__():
    tests.unit.utils.verify___all__(metadata)


class Test_BaseMetadata:
    @staticmethod
    def test_cannot_instantiate():
        with pytest.raises(TypeError):
            metadata._BaseMetadata()


class TestEntityGroup:
    @staticmethod
    def test_constructor():
        entity_group = metadata.EntityGroup()


class TestKind:
    @staticmethod
    def test_constructor():
        kind = metadata.Kind()


class TestNamespace:

    @staticmethod
    def test_constructor():
        namespace = metadata.Namespace()


class TestProperty:
    @staticmethod
    def test_constructor():
        property = metadata.Property()


def test_get_entity_group_version():
    with pytest.raises(NotImplementedError):
        metadata.get_entity_group_version()


def test_get_kinds():
    with pytest.raises(NotImplementedError):
        metadata.get_kinds()


def test_get_namespaces():
    with pytest.raises(NotImplementedError):
        metadata.get_namespaces()


def test_get_properties_of_kind():
    with pytest.raises(NotImplementedError):
        metadata.get_properties_of_kind()


def test_get_representations_of_kind():
    with pytest.raises(NotImplementedError):
        metadata.get_representations_of_kind()
