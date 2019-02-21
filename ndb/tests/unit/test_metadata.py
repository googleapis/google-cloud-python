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
from google.cloud.ndb import key as key_module
import tests.unit.utils


def test___all__():
    tests.unit.utils.verify___all__(metadata)


class Test_BaseMetadata:
    @staticmethod
    def test_get_kind():
        kind = metadata._BaseMetadata.KIND_NAME
        assert metadata._BaseMetadata._get_kind() == kind

    @staticmethod
    def test_cannot_instantiate():
        with pytest.raises(TypeError):
            metadata._BaseMetadata()


class TestEntityGroup:
    @staticmethod
    def test_get_kind():
        kind = metadata.EntityGroup.KIND_NAME
        assert metadata.EntityGroup._get_kind() == kind

    @staticmethod
    def test_constructor():
        entity_group = metadata.EntityGroup()
        assert entity_group.__dict__ == {"_values": {}}

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_key_for_entity_group():
        key = key_module.Key(
            metadata.EntityGroup.KIND_NAME,
            "test",
            metadata.EntityGroup.KIND_NAME,
            1,
        )
        assert key == metadata.EntityGroup.key_for_entity_group(key)


class TestKind:
    @staticmethod
    def test_get_kind():
        kind = metadata.Kind.KIND_NAME
        assert metadata.Kind._get_kind() == kind

    @staticmethod
    def test_constructor():
        kind = metadata.Kind()
        assert kind.__dict__ == {"_values": {}}

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_key_for_kind():
        key = key_module.Key(metadata.Kind.KIND_NAME, "test")
        assert key == metadata.Kind.key_for_kind("test")

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_key_to_kind():
        key = key_module.Key(metadata.Kind.KIND_NAME, "test")
        assert metadata.Kind.key_to_kind(key) == "test"

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_kind_name():
        key = key_module.Key(metadata.Kind.KIND_NAME, "test")
        kind = metadata.Kind(key=key)
        assert kind.kind_name == "test"


class TestNamespace:
    @staticmethod
    def test_get_kind():
        kind = metadata.Namespace.KIND_NAME
        assert metadata.Namespace._get_kind() == kind

    @staticmethod
    def test_constructor():
        namespace = metadata.Namespace()
        assert namespace.__dict__ == {"_values": {}}

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_key_for_namespace():
        key = key_module.Key(metadata.Namespace.KIND_NAME, "test")
        assert key == metadata.Namespace.key_for_namespace("test")

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_key_for_namespace_empty():
        key = key_module.Key(
            metadata.Namespace.KIND_NAME, metadata.Namespace.EMPTY_NAMESPACE_ID
        )
        assert key == metadata.Namespace.key_for_namespace("")

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_key_to_namespace():
        key = key_module.Key(metadata.Namespace.KIND_NAME, "test")
        assert metadata.Namespace.key_to_namespace(key) == "test"

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_namespace_name():
        key = key_module.Key(metadata.Namespace.KIND_NAME, "test")
        namespace = metadata.Namespace(key=key)
        assert namespace.namespace_name == "test"


class TestProperty:
    @staticmethod
    def test_get_kind():
        kind = metadata.Property.KIND_NAME
        assert metadata.Property._get_kind() == kind

    @staticmethod
    def test_constructor():
        property = metadata.Property()
        assert property.__dict__ == {"_values": {}}

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_key_for_kind():
        key = key_module.Key(metadata.Kind.KIND_NAME, "test")
        assert key == metadata.Property.key_for_kind("test")

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_key_to_kind():
        kind = key_module.Key(metadata.Kind.KIND_NAME, "test")
        assert metadata.Property.key_to_kind(kind) == "test"

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_kind_name():
        key = key_module.Key(
            metadata.Kind.KIND_NAME,
            "test",
            metadata.Property.KIND_NAME,
            "test2",
        )
        property = metadata.Property(key=key)
        assert property.kind_name == "test"

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_key_for_property():
        key = key_module.Key(
            metadata.Kind.KIND_NAME,
            "test",
            metadata.Property.KIND_NAME,
            "test2",
        )
        assert key == metadata.Property.key_for_property("test", "test2")

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_key_to_property():
        kind = key_module.Key(metadata.Property.KIND_NAME, "test")
        assert metadata.Property.key_to_property(kind) == "test"

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_key_to_property_only_kind():
        kind = key_module.Key(metadata.Kind.KIND_NAME, "test")
        assert metadata.Property.key_to_property(kind) is None

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_property_name():
        key = key_module.Key(
            metadata.Kind.KIND_NAME,
            "test",
            metadata.Property.KIND_NAME,
            "test2",
        )
        property = metadata.Property(key=key)
        assert property.property_name == "test2"


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
