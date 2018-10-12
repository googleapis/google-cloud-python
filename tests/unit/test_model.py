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

import unittest.mock

import pytest

from google.cloud.ndb import key
from google.cloud.ndb import model
import tests.unit.utils


def test___all__():
    tests.unit.utils.verify___all__(model)


def test_Key():
    assert model.Key is key.Key


def test_BlobKey():
    assert model.BlobKey is NotImplemented


def test_GeoPt():
    assert model.GeoPt is NotImplemented


class TestIndexProperty:
    @staticmethod
    def test_constructor():
        index_prop = model.IndexProperty(name="a", direction="asc")
        assert index_prop._name == "a"
        assert index_prop._direction == "asc"

    @staticmethod
    def test_name():
        index_prop = model.IndexProperty(name="b", direction="asc")
        assert index_prop.name == "b"

    @staticmethod
    def test_direction():
        index_prop = model.IndexProperty(name="a", direction="desc")
        assert index_prop.direction == "desc"

    @staticmethod
    def test___repr__():
        index_prop = model.IndexProperty(name="c", direction="asc")
        assert repr(index_prop) == "IndexProperty(name='c', direction='asc')"

    @staticmethod
    def test___eq__():
        index_prop1 = model.IndexProperty(name="d", direction="asc")
        index_prop2 = model.IndexProperty(name="d", direction="desc")
        index_prop3 = unittest.mock.sentinel.index_prop
        assert index_prop1 == index_prop1
        assert not index_prop1 == index_prop2
        assert not index_prop1 == index_prop3

    @staticmethod
    def test___ne__():
        index_prop1 = model.IndexProperty(name="d", direction="asc")
        index_prop2 = model.IndexProperty(name="d", direction="desc")
        index_prop3 = unittest.mock.sentinel.index_prop
        assert not index_prop1 != index_prop1
        assert index_prop1 != index_prop2
        assert index_prop1 != index_prop3

    @staticmethod
    def test___hash__():
        index_prop1 = model.IndexProperty(name="zip", direction="asc")
        index_prop2 = model.IndexProperty(name="zip", direction="asc")
        assert index_prop1 is not index_prop2
        assert hash(index_prop1) == hash(index_prop2)
        assert hash(index_prop1) == hash(("zip", "asc"))


class TestIndex:
    @staticmethod
    def test_constructor():
        index_prop = model.IndexProperty(name="a", direction="asc")
        index = model.Index(
            kind="IndK", properties=(index_prop,), ancestor=False
        )
        assert index._kind == "IndK"
        assert index._properties == (index_prop,)
        assert not index._ancestor

    @staticmethod
    def test_kind():
        index = model.Index(kind="OK", properties=(), ancestor=False)
        assert index.kind == "OK"

    @staticmethod
    def test_properties():
        index_prop1 = model.IndexProperty(name="a", direction="asc")
        index_prop2 = model.IndexProperty(name="b", direction="desc")
        index = model.Index(
            kind="F", properties=(index_prop1, index_prop2), ancestor=False
        )
        assert index.properties == (index_prop1, index_prop2)

    @staticmethod
    def test_ancestor():
        index = model.Index(kind="LK", properties=(), ancestor=True)
        assert index.ancestor

    @staticmethod
    def test___repr__():
        index_prop = model.IndexProperty(name="a", direction="asc")
        index = model.Index(
            kind="IndK", properties=[index_prop], ancestor=False
        )
        expected = "Index(kind='IndK', properties=[{!r}], ancestor=False)"
        expected = expected.format(index_prop)
        assert repr(index) == expected

    @staticmethod
    def test___eq__():
        index_props = (model.IndexProperty(name="a", direction="asc"),)
        index1 = model.Index(kind="d", properties=index_props, ancestor=False)
        index2 = model.Index(kind="d", properties=(), ancestor=False)
        index3 = model.Index(kind="d", properties=index_props, ancestor=True)
        index4 = model.Index(kind="e", properties=index_props, ancestor=False)
        index5 = unittest.mock.sentinel.index
        assert index1 == index1
        assert not index1 == index2
        assert not index1 == index3
        assert not index1 == index4
        assert not index1 == index5

    @staticmethod
    def test___ne__():
        index_props = (model.IndexProperty(name="a", direction="asc"),)
        index1 = model.Index(kind="d", properties=index_props, ancestor=False)
        index2 = model.Index(kind="d", properties=(), ancestor=False)
        index3 = model.Index(kind="d", properties=index_props, ancestor=True)
        index4 = model.Index(kind="e", properties=index_props, ancestor=False)
        index5 = unittest.mock.sentinel.index
        assert not index1 != index1
        assert index1 != index2
        assert index1 != index3
        assert index1 != index4
        assert index1 != index5

    @staticmethod
    def test___hash__():
        index_props = (model.IndexProperty(name="a", direction="asc"),)
        index1 = model.Index(kind="d", properties=index_props, ancestor=False)
        index2 = model.Index(kind="d", properties=index_props, ancestor=False)
        assert index1 is not index2
        assert hash(index1) == hash(index2)
        assert hash(index1) == hash(("d", index_props, False))


class TestIndexState:

    INDEX = unittest.mock.sentinel.index

    def test_constructor(self):
        index_state = model.IndexState(
            definition=self.INDEX, state="error", id=42
        )
        assert index_state._definition is self.INDEX
        assert index_state._state == "error"
        assert index_state._id == 42

    def test_definition(self):
        index_state = model.IndexState(
            definition=self.INDEX, state="serving", id=1
        )
        assert index_state.definition is self.INDEX

    @staticmethod
    def test_state():
        index_state = model.IndexState(definition=None, state="deleting", id=1)
        assert index_state.state == "deleting"

    @staticmethod
    def test_id():
        index_state = model.IndexState(definition=None, state="error", id=1001)
        assert index_state.id == 1001

    @staticmethod
    def test___repr__():
        index_prop = model.IndexProperty(name="a", direction="asc")
        index = model.Index(
            kind="IndK", properties=[index_prop], ancestor=False
        )
        index_state = model.IndexState(
            definition=index, state="building", id=1337
        )
        expected = (
            "IndexState(definition=Index(kind='IndK', properties=["
            "IndexProperty(name='a', direction='asc')], ancestor=False), "
            "state='building', id=1337)"
        )
        assert repr(index_state) == expected

    def test___eq__(self):
        index_state1 = model.IndexState(
            definition=self.INDEX, state="error", id=20
        )
        index_state2 = model.IndexState(
            definition=unittest.mock.sentinel.not_index, state="error", id=20
        )
        index_state3 = model.IndexState(
            definition=self.INDEX, state="serving", id=20
        )
        index_state4 = model.IndexState(
            definition=self.INDEX, state="error", id=80
        )
        index_state5 = unittest.mock.sentinel.index_state
        assert index_state1 == index_state1
        assert not index_state1 == index_state2
        assert not index_state1 == index_state3
        assert not index_state1 == index_state4
        assert not index_state1 == index_state5

    def test___ne__(self):
        index_state1 = model.IndexState(
            definition=self.INDEX, state="error", id=20
        )
        index_state2 = model.IndexState(
            definition=unittest.mock.sentinel.not_index, state="error", id=20
        )
        index_state3 = model.IndexState(
            definition=self.INDEX, state="serving", id=20
        )
        index_state4 = model.IndexState(
            definition=self.INDEX, state="error", id=80
        )
        index_state5 = unittest.mock.sentinel.index_state
        assert not index_state1 != index_state1
        assert index_state1 != index_state2
        assert index_state1 != index_state3
        assert index_state1 != index_state4
        assert index_state1 != index_state5

    def test___hash__(self):
        index_state1 = model.IndexState(
            definition=self.INDEX, state="error", id=88
        )
        index_state2 = model.IndexState(
            definition=self.INDEX, state="error", id=88
        )
        assert index_state1 is not index_state2
        assert hash(index_state1) == hash(index_state2)
        assert hash(index_state1) == hash((self.INDEX, "error", 88))


class TestModelAdapter:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.ModelAdapter()


def test_make_connection():
    with pytest.raises(NotImplementedError):
        model.make_connection()


class TestModelAttribute:
    @staticmethod
    def test_constructor():
        attr = model.ModelAttribute()
        assert isinstance(attr, model.ModelAttribute)

    @staticmethod
    def test__fix_up():
        attr = model.ModelAttribute()
        assert attr._fix_up(model.Model, "birthdate") is None


@pytest.fixture
def zero_prop_counter():
    counter_val = model.Property._CREATION_COUNTER
    model.Property._CREATION_COUNTER = 0
    try:
        yield
    finally:
        model.Property._CREATION_COUNTER = counter_val


class TestProperty:
    @staticmethod
    def test_constructor_defaults(zero_prop_counter):
        prop = model.Property()
        # Check that the creation counter was updated.
        assert model.Property._CREATION_COUNTER == 1
        assert prop._creation_counter == 1
        # Check that none of the constructor defaults were used.
        assert prop.__dict__ == {"_creation_counter": 1}

    @staticmethod
    def _example_validator(prop, value):
        return value.lower()

    def test__example_validator(self):
        value = "AbCde"
        validated = self._example_validator(None, value)
        assert validated == "abcde"
        assert self._example_validator(None, validated) == "abcde"

    def test_constructor_explicit(self, zero_prop_counter):
        prop = model.Property(
            name="val",
            indexed=False,
            repeated=False,
            required=True,
            default="zorp",
            choices=("zorp", "zap", "zip"),
            validator=self._example_validator,
            verbose_name="VALUE FOR READING",
            write_empty_list=False,
        )
        assert prop._name == b"val" and prop._name != "val"
        assert not prop._indexed
        assert not prop._repeated
        assert prop._required
        assert prop._default == "zorp"
        assert prop._choices == frozenset(("zorp", "zap", "zip"))
        assert prop._validator is self._example_validator
        assert prop._verbose_name == "VALUE FOR READING"
        assert not prop._write_empty_list
        # Check that the creation counter was updated.
        assert model.Property._CREATION_COUNTER == 1
        assert prop._creation_counter == 1

    @staticmethod
    def test_constructor_invalid_name(zero_prop_counter):
        with pytest.raises(TypeError):
            model.Property(name=["not", "a", "string"])
        with pytest.raises(ValueError):
            model.Property(name="has.a.dot")
        # Check that the creation counter was not updated.
        assert model.Property._CREATION_COUNTER == 0

    @staticmethod
    def test_constructor_repeated_not_allowed(zero_prop_counter):
        with pytest.raises(ValueError):
            model.Property(name="a", repeated=True, required=True)
        with pytest.raises(ValueError):
            model.Property(name="b", repeated=True, default="zim")
        # Check that the creation counter was not updated.
        assert model.Property._CREATION_COUNTER == 0

    @staticmethod
    def test_constructor_invalid_choices(zero_prop_counter):
        with pytest.raises(TypeError):
            model.Property(name="a", choices={"wrong": "container"})
        # Check that the creation counter was not updated.
        assert model.Property._CREATION_COUNTER == 0

    @staticmethod
    def test_constructor_invalid_validator(zero_prop_counter):
        with pytest.raises(TypeError):
            model.Property(
                name="a", validator=unittest.mock.sentinel.validator
            )
        # Check that the creation counter was not updated.
        assert model.Property._CREATION_COUNTER == 0


class TestModelKey:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.ModelKey()


class TestBooleanProperty:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.BooleanProperty()


class TestIntegerProperty:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.IntegerProperty()


class TestFloatProperty:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.FloatProperty()


class TestBlobProperty:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.BlobProperty()


class TestTextProperty:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.TextProperty()


class TestStringProperty:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.StringProperty()


class TestGeoPtProperty:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.GeoPtProperty()


class TestPickleProperty:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.PickleProperty()


class TestJsonProperty:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.JsonProperty()


class TestUserProperty:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.UserProperty()


class TestKeyProperty:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.KeyProperty()


class TestBlobKeyProperty:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.BlobKeyProperty()


class TestDateTimeProperty:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.DateTimeProperty()


class TestDateProperty:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.DateProperty()


class TestTimeProperty:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.TimeProperty()


class TestStructuredProperty:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.StructuredProperty()


class TestLocalStructuredProperty:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.LocalStructuredProperty()


class TestGenericProperty:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.GenericProperty()


class TestComputedProperty:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.ComputedProperty()


class TestMetaModel:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.MetaModel()


class TestModel:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.Model()

    @staticmethod
    def test__get_kind():
        assert model.Model._get_kind() == "Model"

        class Simple(model.Model):
            pass

        assert Simple._get_kind() == "Simple"


class TestExpando:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.Expando()


def test_transaction():
    with pytest.raises(NotImplementedError):
        model.transaction()


def test_transaction_async():
    with pytest.raises(NotImplementedError):
        model.transaction_async()


def test_in_transaction():
    with pytest.raises(NotImplementedError):
        model.in_transaction()


def test_transactional():
    with pytest.raises(NotImplementedError):
        model.transactional()


def test_transactional_async():
    with pytest.raises(NotImplementedError):
        model.transactional_async()


def test_transactional_tasklet():
    with pytest.raises(NotImplementedError):
        model.transactional_tasklet()


def test_non_transactional():
    with pytest.raises(NotImplementedError):
        model.non_transactional()


def test_get_multi_async():
    with pytest.raises(NotImplementedError):
        model.get_multi_async()


def test_get_multi():
    with pytest.raises(NotImplementedError):
        model.get_multi()


def test_put_multi_async():
    with pytest.raises(NotImplementedError):
        model.put_multi_async()


def test_put_multi():
    with pytest.raises(NotImplementedError):
        model.put_multi()


def test_delete_multi_async():
    with pytest.raises(NotImplementedError):
        model.delete_multi_async()


def test_delete_multi():
    with pytest.raises(NotImplementedError):
        model.delete_multi()


def test_get_indexes_async():
    with pytest.raises(NotImplementedError):
        model.get_indexes_async()


def test_get_indexes():
    with pytest.raises(NotImplementedError):
        model.get_indexes()
