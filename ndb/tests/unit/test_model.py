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

import types
import unittest.mock
import zlib

import pytest

from google.cloud.ndb import exceptions
from google.cloud.ndb import key
from google.cloud.ndb import model
from google.cloud.ndb import query
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


class Test_BaseValue:
    @staticmethod
    def test_constructor():
        wrapped = model._BaseValue(17)
        assert wrapped.b_val == 17

    @staticmethod
    def test_constructor_invalid_input():
        with pytest.raises(TypeError):
            model._BaseValue(None)
        with pytest.raises(TypeError):
            model._BaseValue([1, 2])

    @staticmethod
    def test___repr__():
        wrapped = model._BaseValue(b"abc")
        assert repr(wrapped) == "_BaseValue(b'abc')"

    @staticmethod
    def test___eq__():
        wrapped1 = model._BaseValue("one val")
        wrapped2 = model._BaseValue(25.5)
        wrapped3 = unittest.mock.sentinel.base_value
        assert wrapped1 == wrapped1
        assert not wrapped1 == wrapped2
        assert not wrapped1 == wrapped3

    @staticmethod
    def test___ne__():
        wrapped1 = model._BaseValue("one val")
        wrapped2 = model._BaseValue(25.5)
        wrapped3 = unittest.mock.sentinel.base_value
        assert not wrapped1 != wrapped1
        assert wrapped1 != wrapped2
        assert wrapped1 != wrapped3

    @staticmethod
    def test___hash__():
        wrapped = model._BaseValue((11, 12, 88))
        with pytest.raises(TypeError):
            hash(wrapped)


class TestProperty:
    @staticmethod
    def test_constructor_defaults():
        prop = model.Property()
        # Check that none of the constructor defaults were used.
        assert prop.__dict__ == {}

    @staticmethod
    def _example_validator(prop, value):
        return value.lower()

    def test__example_validator(self):
        value = "AbCde"
        validated = self._example_validator(None, value)
        assert validated == "abcde"
        assert self._example_validator(None, validated) == "abcde"

    def test_constructor_explicit(self):
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

    @staticmethod
    def test_constructor_invalid_name():
        with pytest.raises(TypeError):
            model.Property(name=["not", "a", "string"])
        with pytest.raises(ValueError):
            model.Property(name="has.a.dot")

    @staticmethod
    def test_constructor_repeated_not_allowed():
        with pytest.raises(ValueError):
            model.Property(name="a", repeated=True, required=True)
        with pytest.raises(ValueError):
            model.Property(name="b", repeated=True, default="zim")

    @staticmethod
    def test_constructor_invalid_choices():
        with pytest.raises(TypeError):
            model.Property(name="a", choices={"wrong": "container"})

    @staticmethod
    def test_constructor_invalid_validator():
        with pytest.raises(TypeError):
            model.Property(
                name="a", validator=unittest.mock.sentinel.validator
            )

    def test_repr(self):
        prop = model.Property(
            "val",
            indexed=False,
            repeated=False,
            required=True,
            default="zorp",
            choices=("zorp", "zap", "zip"),
            validator=self._example_validator,
            verbose_name="VALUE FOR READING",
            write_empty_list=False,
        )
        expected = (
            "Property(b'val', indexed=False, required=True, "
            "default='zorp', choices={}, validator={}, "
            "verbose_name='VALUE FOR READING')".format(
                prop._choices, prop._validator
            )
        )
        assert repr(prop) == expected

    @staticmethod
    def test_repr_subclass():
        class SimpleProperty(model.Property):
            _foo_type = None
            _bar = "eleventy"

            def __init__(self, *, foo_type, bar):
                self._foo_type = foo_type
                self._bar = bar

        prop = SimpleProperty(foo_type=list, bar="nope")
        assert repr(prop) == "SimpleProperty(foo_type=list, bar='nope')"

    @staticmethod
    def test__datastore_type():
        prop = model.Property("foo")
        value = unittest.mock.sentinel.value
        assert prop._datastore_type(value) is value

    @staticmethod
    def test__comparison_indexed():
        prop = model.Property("color", indexed=False)
        with pytest.raises(exceptions.BadFilterError):
            prop._comparison("!=", "red")

    @staticmethod
    def test__comparison(property_clean_cache):
        prop = model.Property("sentiment", indexed=True)
        filter_node = prop._comparison(">=", 0.0)
        assert filter_node == query.FilterNode(b"sentiment", ">=", 0.0)

    @staticmethod
    def test__comparison_empty_value():
        prop = model.Property("height", indexed=True)
        filter_node = prop._comparison("=", None)
        assert filter_node == query.FilterNode(b"height", "=", None)
        # Cache is untouched.
        assert model.Property._FIND_METHODS_CACHE == {}

    @staticmethod
    def test___eq__(property_clean_cache):
        prop = model.Property("name", indexed=True)
        value = 1337
        expected = query.FilterNode(b"name", "=", value)

        filter_node_left = prop == value
        assert filter_node_left == expected
        filter_node_right = value == prop
        assert filter_node_right == expected

    @staticmethod
    def test___ne__(property_clean_cache):
        prop = model.Property("name", indexed=True)
        value = 7.0
        expected = query.DisjunctionNode(
            query.FilterNode(b"name", "<", value),
            query.FilterNode(b"name", ">", value),
        )

        or_node_left = prop != value
        assert or_node_left == expected
        or_node_right = value != prop
        assert or_node_right == expected

    @staticmethod
    def test___lt__(property_clean_cache):
        prop = model.Property("name", indexed=True)
        value = 2.0
        expected = query.FilterNode(b"name", "<", value)

        filter_node_left = prop < value
        assert filter_node_left == expected
        filter_node_right = value > prop
        assert filter_node_right == expected

    @staticmethod
    def test___le__(property_clean_cache):
        prop = model.Property("name", indexed=True)
        value = 20.0
        expected = query.FilterNode(b"name", "<=", value)

        filter_node_left = prop <= value
        assert filter_node_left == expected
        filter_node_right = value >= prop
        assert filter_node_right == expected

    @staticmethod
    def test___gt__(property_clean_cache):
        prop = model.Property("name", indexed=True)
        value = "new"
        expected = query.FilterNode(b"name", ">", value)

        filter_node_left = prop > value
        assert filter_node_left == expected
        filter_node_right = value < prop
        assert filter_node_right == expected

    @staticmethod
    def test___ge__(property_clean_cache):
        prop = model.Property("name", indexed=True)
        value = "old"
        expected = query.FilterNode(b"name", ">=", value)

        filter_node_left = prop >= value
        assert filter_node_left == expected
        filter_node_right = value <= prop
        assert filter_node_right == expected

    @staticmethod
    def test__IN_not_indexed():
        prop = model.Property("name", indexed=False)
        with pytest.raises(exceptions.BadFilterError):
            prop._IN([10, 20, 81])

        # Cache is untouched.
        assert model.Property._FIND_METHODS_CACHE == {}

    @staticmethod
    def test__IN_wrong_container():
        prop = model.Property("name", indexed=True)
        with pytest.raises(exceptions.BadArgumentError):
            prop._IN({1: "a", 11: "b"})

        # Cache is untouched.
        assert model.Property._FIND_METHODS_CACHE == {}

    @staticmethod
    def test__IN(property_clean_cache):
        prop = model.Property("name", indexed=True)
        or_node = prop._IN(["a", None, "xy"])
        expected = query.DisjunctionNode(
            query.FilterNode(b"name", "=", "a"),
            query.FilterNode(b"name", "=", None),
            query.FilterNode(b"name", "=", "xy"),
        )
        assert or_node == expected
        # Also verify the alias
        assert or_node == prop.IN(["a", None, "xy"])

    @staticmethod
    def test___neg__():
        prop = model.Property("name")
        with pytest.raises(NotImplementedError):
            -prop

    @staticmethod
    def test___pos__():
        prop = model.Property("name")
        with pytest.raises(NotImplementedError):
            +prop

    @staticmethod
    def test__do_validate(property_clean_cache):
        validator = unittest.mock.Mock(spec=())
        value = 18
        choices = (1, 2, validator.return_value)

        prop = model.Property(name="foo", validator=validator, choices=choices)
        result = prop._do_validate(value)
        assert result is validator.return_value
        # Check validator call.
        validator.assert_called_once_with(prop, value)

    @staticmethod
    def test__do_validate_base_value():
        value = model._BaseValue(b"\x00\x01")

        prop = model.Property(name="foo")
        result = prop._do_validate(value)
        assert result is value
        # Cache is untouched.
        assert model.Property._FIND_METHODS_CACHE == {}

    @staticmethod
    def test__do_validate_validator_none(property_clean_cache):
        validator = unittest.mock.Mock(spec=(), return_value=None)
        value = 18

        prop = model.Property(name="foo", validator=validator)
        result = prop._do_validate(value)
        assert result == value
        # Check validator call.
        validator.assert_called_once_with(prop, value)

    @staticmethod
    def test__do_validate_not_in_choices(property_clean_cache):
        value = 18
        prop = model.Property(name="foo", choices=(1, 2))

        with pytest.raises(exceptions.BadValueError):
            prop._do_validate(value)

    @staticmethod
    def test__do_validate_call_validation(property_clean_cache):
        class SimpleProperty(model.Property):
            def _validate(self, value):
                value.append("SimpleProperty._validate")
                return value

        value = []
        prop = SimpleProperty(name="foo")
        result = prop._do_validate(value)
        assert result is value
        assert value == ["SimpleProperty._validate"]

    @staticmethod
    def test__fix_up():
        prop = model.Property(name="foo")
        assert prop._code_name is None
        prop._fix_up(None, "bar")
        assert prop._code_name == "bar"

    @staticmethod
    def test__fix_up_no_name():
        prop = model.Property()
        assert prop._name is None
        assert prop._code_name is None

        prop._fix_up(None, "both")
        assert prop._code_name == "both"
        assert prop._name == "both"

    @staticmethod
    def test__store_value():
        entity = unittest.mock.Mock(_values={}, spec=("_values",))
        prop = model.Property(name="foo")
        prop._store_value(entity, unittest.mock.sentinel.value)
        assert entity._values == {prop._name: unittest.mock.sentinel.value}

    @staticmethod
    def test__set_value(property_clean_cache):
        entity = unittest.mock.Mock(
            _projection=None, _values={}, spec=("_projection", "_values")
        )
        prop = model.Property(name="foo", repeated=False)
        prop._set_value(entity, 19)
        assert entity._values == {prop._name: 19}

    @staticmethod
    def test__set_value_none():
        entity = unittest.mock.Mock(
            _projection=None, _values={}, spec=("_projection", "_values")
        )
        prop = model.Property(name="foo", repeated=False)
        prop._set_value(entity, None)
        assert entity._values == {prop._name: None}
        # Cache is untouched.
        assert model.Property._FIND_METHODS_CACHE == {}

    @staticmethod
    def test__set_value_repeated(property_clean_cache):
        entity = unittest.mock.Mock(
            _projection=None, _values={}, spec=("_projection", "_values")
        )
        prop = model.Property(name="foo", repeated=True)
        prop._set_value(entity, (11, 12, 13))
        assert entity._values == {prop._name: [11, 12, 13]}

    @staticmethod
    def test__set_value_repeated_bad_container():
        entity = unittest.mock.Mock(
            _projection=None, _values={}, spec=("_projection", "_values")
        )
        prop = model.Property(name="foo", repeated=True)
        with pytest.raises(exceptions.BadValueError):
            prop._set_value(entity, None)
        # Cache is untouched.
        assert model.Property._FIND_METHODS_CACHE == {}

    @staticmethod
    def test__set_value_projection():
        entity = unittest.mock.Mock(
            _projection=("a", "b"), spec=("_projection",)
        )
        prop = model.Property(name="foo", repeated=True)
        with pytest.raises(model.ReadonlyPropertyError):
            prop._set_value(entity, None)
        # Cache is untouched.
        assert model.Property._FIND_METHODS_CACHE == {}

    @staticmethod
    def test__has_value():
        prop = model.Property(name="foo")
        values = {prop._name: 88}
        entity1 = unittest.mock.Mock(_values=values, spec=("_values",))
        entity2 = unittest.mock.Mock(_values={}, spec=("_values",))

        assert prop._has_value(entity1)
        assert not prop._has_value(entity2)

    @staticmethod
    def test__retrieve_value():
        prop = model.Property(name="foo")
        values = {prop._name: b"\x00\x01"}
        entity1 = unittest.mock.Mock(_values=values, spec=("_values",))
        entity2 = unittest.mock.Mock(_values={}, spec=("_values",))

        assert prop._retrieve_value(entity1) == b"\x00\x01"
        assert prop._retrieve_value(entity2) is None
        assert prop._retrieve_value(entity2, default=b"zip") == b"zip"

    @staticmethod
    def test__get_user_value():
        prop = model.Property(name="prop")
        value = b"\x00\x01"
        values = {prop._name: value}
        entity = unittest.mock.Mock(_values=values, spec=("_values",))
        assert value is prop._get_user_value(entity)
        # Cache is untouched.
        assert model.Property._FIND_METHODS_CACHE == {}

    @staticmethod
    def test__get_user_value_wrapped(property_clean_cache):
        class SimpleProperty(model.Property):
            def _from_base_type(self, value):
                return value * 2.0

        prop = SimpleProperty(name="prop")
        values = {prop._name: model._BaseValue(9.5)}
        entity = unittest.mock.Mock(_values=values, spec=("_values",))
        assert prop._get_user_value(entity) == 19.0

    @staticmethod
    def test__get_base_value(property_clean_cache):
        class SimpleProperty(model.Property):
            def _validate(self, value):
                return value + 1

        prop = SimpleProperty(name="prop")
        values = {prop._name: 20}
        entity = unittest.mock.Mock(_values=values, spec=("_values",))
        assert prop._get_base_value(entity) == model._BaseValue(21)

    @staticmethod
    def test__get_base_value_wrapped():
        prop = model.Property(name="prop")
        value = model._BaseValue(b"\x00\x01")
        values = {prop._name: value}
        entity = unittest.mock.Mock(_values=values, spec=("_values",))
        assert value is prop._get_base_value(entity)
        # Cache is untouched.
        assert model.Property._FIND_METHODS_CACHE == {}

    @staticmethod
    def test__get_base_value_unwrapped_as_list(property_clean_cache):
        class SimpleProperty(model.Property):
            def _validate(self, value):
                return value + 11

        prop = SimpleProperty(name="prop", repeated=False)
        values = {prop._name: 20}
        entity = unittest.mock.Mock(_values=values, spec=("_values",))
        assert prop._get_base_value_unwrapped_as_list(entity) == [31]

    @staticmethod
    def test__get_base_value_unwrapped_as_list_empty():
        prop = model.Property(name="prop", repeated=False)
        entity = unittest.mock.Mock(_values={}, spec=("_values",))
        assert prop._get_base_value_unwrapped_as_list(entity) == [None]
        # Cache is untouched.
        assert model.Property._FIND_METHODS_CACHE == {}

    @staticmethod
    def test__get_base_value_unwrapped_as_list_repeated(property_clean_cache):
        class SimpleProperty(model.Property):
            def _validate(self, value):
                return value / 10.0

        prop = SimpleProperty(name="prop", repeated=True)
        values = {prop._name: [20, 30, 40]}
        entity = unittest.mock.Mock(_values=values, spec=("_values",))
        expected = [2.0, 3.0, 4.0]
        assert prop._get_base_value_unwrapped_as_list(entity) == expected

    @staticmethod
    def test__opt_call_from_base_type():
        prop = model.Property(name="prop")
        value = b"\x00\x01"
        assert value is prop._opt_call_from_base_type(value)
        # Cache is untouched.
        assert model.Property._FIND_METHODS_CACHE == {}

    @staticmethod
    def test__opt_call_from_base_type_wrapped(property_clean_cache):
        class SimpleProperty(model.Property):
            def _from_base_type(self, value):
                return value * 2.0

        prop = SimpleProperty(name="prop")
        value = model._BaseValue(8.5)
        assert prop._opt_call_from_base_type(value) == 17.0

    @staticmethod
    def test__value_to_repr(property_clean_cache):
        class SimpleProperty(model.Property):
            def _from_base_type(self, value):
                return value * 3.0

        prop = SimpleProperty(name="prop")
        value = model._BaseValue(9.25)
        assert prop._value_to_repr(value) == "27.75"

    @staticmethod
    def test__opt_call_to_base_type(property_clean_cache):
        class SimpleProperty(model.Property):
            def _validate(self, value):
                return value + 1

        prop = SimpleProperty(name="prop")
        value = 17
        result = prop._opt_call_to_base_type(value)
        assert result == model._BaseValue(value + 1)

    @staticmethod
    def test__opt_call_to_base_type_wrapped():
        prop = model.Property(name="prop")
        value = model._BaseValue(b"\x00\x01")
        assert value is prop._opt_call_to_base_type(value)
        # Cache is untouched.
        assert model.Property._FIND_METHODS_CACHE == {}

    @staticmethod
    def test__call_from_base_type(property_clean_cache):
        class SimpleProperty(model.Property):
            def _from_base_type(self, value):
                value.append("SimpleProperty._from_base_type")
                return value

        prop = SimpleProperty(name="prop")
        value = []
        assert value is prop._call_from_base_type(value)
        assert value == ["SimpleProperty._from_base_type"]

    @staticmethod
    def _property_subtype_chain():
        class A(model.Property):
            def _validate(self, value):
                value.append("A._validate")
                return value

            def _to_base_type(self, value):
                value.append("A._to_base_type")
                return value

        class B(A):
            def _validate(self, value):
                value.append("B._validate")
                return value

            def _to_base_type(self, value):
                value.append("B._to_base_type")
                return value

        class C(B):
            def _validate(self, value):
                value.append("C._validate")
                return value

        value = []

        prop_a = A(name="name-a")
        assert value is prop_a._validate(value)
        assert value == ["A._validate"]
        assert value is prop_a._to_base_type(value)
        assert value == ["A._validate", "A._to_base_type"]
        prop_b = B(name="name-b")
        assert value is prop_b._validate(value)
        assert value == ["A._validate", "A._to_base_type", "B._validate"]
        assert value is prop_b._to_base_type(value)
        assert value == [
            "A._validate",
            "A._to_base_type",
            "B._validate",
            "B._to_base_type",
        ]
        prop_c = C(name="name-c")
        assert value is prop_c._validate(value)
        assert value == [
            "A._validate",
            "A._to_base_type",
            "B._validate",
            "B._to_base_type",
            "C._validate",
        ]

        return A, B, C

    def test__call_to_base_type(self, property_clean_cache):
        _, _, PropertySubclass = self._property_subtype_chain()
        prop = PropertySubclass(name="prop")
        value = []
        assert value is prop._call_to_base_type(value)
        assert value == [
            "C._validate",
            "B._validate",
            "B._to_base_type",
            "A._validate",
            "A._to_base_type",
        ]

    def test__call_shallow_validation(self, property_clean_cache):
        _, _, PropertySubclass = self._property_subtype_chain()
        prop = PropertySubclass(name="prop")
        value = []
        assert value is prop._call_shallow_validation(value)
        assert value == ["C._validate", "B._validate"]

    @staticmethod
    def test__call_shallow_validation_no_break(property_clean_cache):
        class SimpleProperty(model.Property):
            def _validate(self, value):
                value.append("SimpleProperty._validate")
                return value

        prop = SimpleProperty(name="simple")
        value = []
        assert value is prop._call_shallow_validation(value)
        assert value == ["SimpleProperty._validate"]

    @staticmethod
    def _property_subtype():
        class SomeProperty(model.Property):
            def find_me(self):
                return self._name

            def IN(self):
                return len(self._name) < 20

        prop = SomeProperty(name="hi")
        assert prop.find_me() == b"hi"
        assert prop.IN()

        return SomeProperty

    def test__find_methods(self, property_clean_cache):
        SomeProperty = self._property_subtype()
        # Make sure cache is empty.
        assert model.Property._FIND_METHODS_CACHE == {}

        methods = SomeProperty._find_methods("IN", "find_me")
        assert methods == [
            SomeProperty.IN,
            SomeProperty.find_me,
            model.Property.IN,
        ]
        # Check cache
        key = "{}.{}".format(
            SomeProperty.__module__, SomeProperty.__qualname__
        )
        assert model.Property._FIND_METHODS_CACHE == {
            key: {("IN", "find_me"): methods}
        }

    def test__find_methods_reverse(self, property_clean_cache):
        SomeProperty = self._property_subtype()
        # Make sure cache is empty.
        assert model.Property._FIND_METHODS_CACHE == {}

        methods = SomeProperty._find_methods("IN", "find_me", reverse=True)
        assert methods == [
            model.Property.IN,
            SomeProperty.find_me,
            SomeProperty.IN,
        ]
        # Check cache
        key = "{}.{}".format(
            SomeProperty.__module__, SomeProperty.__qualname__
        )
        assert model.Property._FIND_METHODS_CACHE == {
            key: {("IN", "find_me"): list(reversed(methods))}
        }

    def test__find_methods_cached(self, property_clean_cache):
        SomeProperty = self._property_subtype()
        # Set cache
        methods = unittest.mock.sentinel.methods
        key = "{}.{}".format(
            SomeProperty.__module__, SomeProperty.__qualname__
        )
        model.Property._FIND_METHODS_CACHE = {
            key: {("IN", "find_me"): methods}
        }
        assert SomeProperty._find_methods("IN", "find_me") is methods

    def test__find_methods_cached_reverse(self, property_clean_cache):
        SomeProperty = self._property_subtype()
        # Set cache
        methods = ["a", "b"]
        key = "{}.{}".format(
            SomeProperty.__module__, SomeProperty.__qualname__
        )
        model.Property._FIND_METHODS_CACHE = {
            key: {("IN", "find_me"): methods}
        }
        assert SomeProperty._find_methods("IN", "find_me", reverse=True) == [
            "b",
            "a",
        ]

    @staticmethod
    def test__apply_list():
        method1 = unittest.mock.Mock(spec=())
        method2 = unittest.mock.Mock(spec=(), return_value=None)
        method3 = unittest.mock.Mock(spec=())

        prop = model.Property(name="benji")
        to_call = prop._apply_list([method1, method2, method3])
        assert isinstance(to_call, types.FunctionType)

        value = unittest.mock.sentinel.value
        result = to_call(value)
        assert result is method3.return_value

        # Check mocks.
        method1.assert_called_once_with(prop, value)
        method2.assert_called_once_with(prop, method1.return_value)
        method3.assert_called_once_with(prop, method1.return_value)

    @staticmethod
    def test__apply_to_values():
        value = "foo"
        prop = model.Property(name="bar", repeated=False)
        entity = unittest.mock.Mock(
            _values={prop._name: value}, spec=("_values",)
        )
        function = unittest.mock.Mock(spec=(), return_value="foo2")

        result = prop._apply_to_values(entity, function)
        assert result == function.return_value
        assert entity._values == {prop._name: result}
        # Check mocks.
        function.assert_called_once_with(value)

    @staticmethod
    def test__apply_to_values_when_none():
        prop = model.Property(name="bar", repeated=False, default=None)
        entity = unittest.mock.Mock(_values={}, spec=("_values",))
        function = unittest.mock.Mock(spec=())

        result = prop._apply_to_values(entity, function)
        assert result is None
        assert entity._values == {}
        # Check mocks.
        function.assert_not_called()

    @staticmethod
    def test__apply_to_values_transformed_none():
        value = 7.5
        prop = model.Property(name="bar", repeated=False)
        entity = unittest.mock.Mock(
            _values={prop._name: value}, spec=("_values",)
        )
        function = unittest.mock.Mock(spec=(), return_value=None)

        result = prop._apply_to_values(entity, function)
        assert result == value
        assert entity._values == {prop._name: result}
        # Check mocks.
        function.assert_called_once_with(value)

    @staticmethod
    def test__apply_to_values_transformed_unchanged():
        value = unittest.mock.sentinel.value
        prop = model.Property(name="bar", repeated=False)
        entity = unittest.mock.Mock(
            _values={prop._name: value}, spec=("_values",)
        )
        function = unittest.mock.Mock(spec=(), return_value=value)

        result = prop._apply_to_values(entity, function)
        assert result == value
        assert entity._values == {prop._name: result}
        # Check mocks.
        function.assert_called_once_with(value)

    @staticmethod
    def test__apply_to_values_repeated():
        value = [1, 2, 3]
        prop = model.Property(name="bar", repeated=True)
        entity = unittest.mock.Mock(
            _values={prop._name: value}, spec=("_values",)
        )
        function = unittest.mock.Mock(spec=(), return_value=42)

        result = prop._apply_to_values(entity, function)
        assert result == [
            function.return_value,
            function.return_value,
            function.return_value,
        ]
        assert result is value  # Check modify in-place.
        assert entity._values == {prop._name: result}
        # Check mocks.
        assert function.call_count == 3
        calls = [
            unittest.mock.call(1),
            unittest.mock.call(2),
            unittest.mock.call(3),
        ]
        function.assert_has_calls(calls)

    @staticmethod
    def test__apply_to_values_repeated_when_none():
        prop = model.Property(name="bar", repeated=True, default=None)
        entity = unittest.mock.Mock(_values={}, spec=("_values",))
        function = unittest.mock.Mock(spec=())

        result = prop._apply_to_values(entity, function)
        assert result == []
        assert entity._values == {prop._name: result}
        # Check mocks.
        function.assert_not_called()

    @staticmethod
    def test__get_value():
        prop = model.Property(name="prop")
        value = b"\x00\x01"
        values = {prop._name: value}
        entity = unittest.mock.Mock(
            _projection=None, _values=values, spec=("_projection", "_values")
        )
        assert value is prop._get_value(entity)
        # Cache is untouched.
        assert model.Property._FIND_METHODS_CACHE == {}

    @staticmethod
    def test__get_value_projected_present():
        prop = model.Property(name="prop")
        value = 92.5
        values = {prop._name: value}
        entity = unittest.mock.Mock(
            _projection=(prop._name,),
            _values=values,
            spec=("_projection", "_values"),
        )
        assert value is prop._get_value(entity)
        # Cache is untouched.
        assert model.Property._FIND_METHODS_CACHE == {}

    @staticmethod
    def test__get_value_projected_absent():
        prop = model.Property(name="prop")
        entity = unittest.mock.Mock(
            _projection=("nope",), spec=("_projection",)
        )
        with pytest.raises(model.UnprojectedPropertyError):
            prop._get_value(entity)
        # Cache is untouched.
        assert model.Property._FIND_METHODS_CACHE == {}

    @staticmethod
    def test__delete_value():
        prop = model.Property(name="prop")
        value = b"\x00\x01"
        values = {prop._name: value}
        entity = unittest.mock.Mock(_values=values, spec=("_values",))
        prop._delete_value(entity)
        assert values == {}

    @staticmethod
    def test__delete_value_no_op():
        prop = model.Property(name="prop")
        values = {}
        entity = unittest.mock.Mock(_values=values, spec=("_values",))
        prop._delete_value(entity)
        assert values == {}

    @staticmethod
    def test__is_initialized_not_required():
        prop = model.Property(name="prop", required=False)
        entity = unittest.mock.sentinel.entity
        assert prop._is_initialized(entity)
        # Cache is untouched.
        assert model.Property._FIND_METHODS_CACHE == {}

    @staticmethod
    def test__is_initialized_default_fallback():
        prop = model.Property(name="prop", required=True, default=11111)
        values = {}
        entity = unittest.mock.Mock(
            _projection=None, _values=values, spec=("_projection", "_values")
        )
        assert prop._is_initialized(entity)
        # Cache is untouched.
        assert model.Property._FIND_METHODS_CACHE == {}

    @staticmethod
    def test__is_initialized_set_to_none():
        prop = model.Property(name="prop", required=True)
        values = {prop._name: None}
        entity = unittest.mock.Mock(
            _projection=None, _values=values, spec=("_projection", "_values")
        )
        assert not prop._is_initialized(entity)
        # Cache is untouched.
        assert model.Property._FIND_METHODS_CACHE == {}

    @staticmethod
    def test_instance_descriptors(property_clean_cache):
        class Model:
            prop = model.Property(name="prop", required=True)

            def __init__(self):
                self._projection = None
                self._values = {}

        m = Model()
        value = 1234.5
        # __set__
        m.prop = value
        assert m._values == {b"prop": value}
        # __get__
        assert m.prop == value
        # __delete__
        del m.prop
        assert m._values == {}

    @staticmethod
    def test_class_descriptors():
        prop = model.Property(name="prop", required=True)

        class Model:
            prop2 = prop

        assert Model.prop2 is prop

    @staticmethod
    def test__serialize():
        prop = model.Property(name="prop")
        with pytest.raises(NotImplementedError):
            prop._serialize(None, None)

    @staticmethod
    def test__deserialize():
        prop = model.Property(name="prop")
        with pytest.raises(NotImplementedError):
            prop._deserialize(None, None)

    @staticmethod
    def test__prepare_for_put():
        prop = model.Property(name="prop")
        assert prop._prepare_for_put(None) is None

    @staticmethod
    def test__check_property():
        prop = model.Property(name="prop")
        assert prop._check_property() is None

    @staticmethod
    def test__check_property_not_indexed():
        prop = model.Property(name="prop", indexed=False)
        with pytest.raises(model.InvalidPropertyError):
            prop._check_property(require_indexed=True)

    @staticmethod
    def test__check_property_with_subproperty():
        prop = model.Property(name="prop", indexed=True)
        with pytest.raises(model.InvalidPropertyError):
            prop._check_property(rest="a.b.c")

    @staticmethod
    def test__get_for_dict():
        prop = model.Property(name="prop")
        value = b"\x00\x01"
        values = {prop._name: value}
        entity = unittest.mock.Mock(
            _projection=None, _values=values, spec=("_projection", "_values")
        )
        assert value is prop._get_for_dict(entity)
        # Cache is untouched.
        assert model.Property._FIND_METHODS_CACHE == {}


class TestModelKey:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            model.ModelKey()


class TestBooleanProperty:
    @staticmethod
    def test__validate():
        prop = model.BooleanProperty(name="certify")
        value = True
        assert prop._validate(value) is value

    @staticmethod
    def test__validate_bad_value():
        prop = model.BooleanProperty(name="certify")
        with pytest.raises(exceptions.BadValueError):
            prop._validate(None)

    @staticmethod
    def test__db_set_value():
        prop = model.BooleanProperty(name="certify")
        with pytest.raises(NotImplementedError):
            prop._db_set_value(None, None, None)

    @staticmethod
    def test__db_get_value():
        prop = model.BooleanProperty(name="certify")
        with pytest.raises(NotImplementedError):
            prop._db_get_value(None, None)


class TestIntegerProperty:
    @staticmethod
    def test__validate():
        prop = model.IntegerProperty(name="count")
        value = 829038402384
        assert prop._validate(value) is value

    @staticmethod
    def test__validate_bool():
        prop = model.IntegerProperty(name="count")
        value = True
        assert prop._validate(value) == 1

    @staticmethod
    def test__validate_bad_value():
        prop = model.IntegerProperty(name="count")
        with pytest.raises(exceptions.BadValueError):
            prop._validate(None)

    @staticmethod
    def test__db_set_value():
        prop = model.IntegerProperty(name="count")
        with pytest.raises(NotImplementedError):
            prop._db_set_value(None, None, None)

    @staticmethod
    def test__db_get_value():
        prop = model.IntegerProperty(name="count")
        with pytest.raises(NotImplementedError):
            prop._db_get_value(None, None)


class TestFloatProperty:
    @staticmethod
    def test__validate():
        prop = model.FloatProperty(name="continuous")
        value = 7.25
        assert prop._validate(value) is value

    @staticmethod
    def test__validate_int():
        prop = model.FloatProperty(name="continuous")
        value = 1015
        assert prop._validate(value) == 1015.0

    @staticmethod
    def test__validate_bool():
        prop = model.FloatProperty(name="continuous")
        value = True
        assert prop._validate(value) == 1.0

    @staticmethod
    def test__validate_bad_value():
        prop = model.FloatProperty(name="continuous")
        with pytest.raises(exceptions.BadValueError):
            prop._validate(None)

    @staticmethod
    def test__db_set_value():
        prop = model.FloatProperty(name="continuous")
        with pytest.raises(NotImplementedError):
            prop._db_set_value(None, None, None)

    @staticmethod
    def test__db_get_value():
        prop = model.FloatProperty(name="continuous")
        with pytest.raises(NotImplementedError):
            prop._db_get_value(None, None)


class Test_CompressedValue:
    @staticmethod
    def test_constructor():
        value = b"abc" * 1000
        z_val = zlib.compress(value)
        compressed_value = model._CompressedValue(z_val)

        assert compressed_value.z_val == z_val

    @staticmethod
    def test___repr__():
        z_val = zlib.compress(b"12345678901234567890")
        compressed_value = model._CompressedValue(z_val)
        expected = "_CompressedValue(" + repr(z_val) + ")"
        assert repr(compressed_value) == expected

    @staticmethod
    def test___eq__():
        z_val1 = zlib.compress(b"12345678901234567890")
        compressed_value1 = model._CompressedValue(z_val1)
        z_val2 = zlib.compress(b"12345678901234567890abcde\x00")
        compressed_value2 = model._CompressedValue(z_val2)
        compressed_value3 = unittest.mock.sentinel.compressed_value
        assert compressed_value1 == compressed_value1
        assert not compressed_value1 == compressed_value2
        assert not compressed_value1 == compressed_value3

    @staticmethod
    def test___ne__():
        z_val1 = zlib.compress(b"12345678901234567890")
        compressed_value1 = model._CompressedValue(z_val1)
        z_val2 = zlib.compress(b"12345678901234567890abcde\x00")
        compressed_value2 = model._CompressedValue(z_val2)
        compressed_value3 = unittest.mock.sentinel.compressed_value
        assert not compressed_value1 != compressed_value1
        assert compressed_value1 != compressed_value2
        assert compressed_value1 != compressed_value3

    @staticmethod
    def test___hash__():
        z_val = zlib.compress(b"12345678901234567890")
        compressed_value = model._CompressedValue(z_val)
        with pytest.raises(TypeError):
            hash(compressed_value)


class TestBlobProperty:
    @staticmethod
    def test_constructor_defaults():
        prop = model.BlobProperty()
        # Check that none of the constructor defaults were used.
        assert prop.__dict__ == {}

    @staticmethod
    def test_constructor_explicit():
        prop = model.BlobProperty(
            name="blob_val",
            compressed=True,
            indexed=False,
            repeated=False,
            required=True,
            default=b"eleven\x11",
            choices=(b"a", b"b", b"c", b"eleven\x11"),
            validator=TestProperty._example_validator,
            verbose_name="VALUE FOR READING",
            write_empty_list=False,
        )
        assert prop._name == b"blob_val" and prop._name != "blob_val"
        assert not prop._indexed
        assert not prop._repeated
        assert prop._required
        assert prop._default == b"eleven\x11"
        assert prop._choices == frozenset((b"a", b"b", b"c", b"eleven\x11"))
        assert prop._validator is TestProperty._example_validator
        assert prop._verbose_name == "VALUE FOR READING"
        assert not prop._write_empty_list

    @staticmethod
    def test_constructor_compressed_and_indexed():
        with pytest.raises(NotImplementedError):
            model.BlobProperty(name="foo", compressed=True, indexed=True)

    @staticmethod
    def test__value_to_repr():
        prop = model.BlobProperty(name="blob")
        as_repr = prop._value_to_repr(b"abc")
        assert as_repr == "b'abc'"

    @staticmethod
    def test__value_to_repr_truncated():
        prop = model.BlobProperty(name="blob")
        value = bytes(range(256)) * 5
        as_repr = prop._value_to_repr(value)
        expected = repr(value)[: model._MAX_STRING_LENGTH] + "...'"
        assert as_repr == expected

    @staticmethod
    def test__validate():
        prop = model.BlobProperty(name="blob")
        assert prop._validate(b"abc") is None

    @staticmethod
    def test__validate_wrong_type():
        prop = model.BlobProperty(name="blob")
        values = ("non-bytes", 48, {"a": "c"})
        for value in values:
            with pytest.raises(exceptions.BadValueError):
                prop._validate(value)

    @staticmethod
    def test__validate_indexed_too_long():
        prop = model.BlobProperty(name="blob", indexed=True)
        value = b"\x00" * 2000
        with pytest.raises(exceptions.BadValueError):
            prop._validate(value)

    @staticmethod
    def test__to_base_type():
        prop = model.BlobProperty(name="blob", compressed=True)
        value = b"abc" * 10
        converted = prop._to_base_type(value)

        assert isinstance(converted, model._CompressedValue)
        assert converted.z_val == zlib.compress(value)

    @staticmethod
    def test__to_base_type_no_convert():
        prop = model.BlobProperty(name="blob", compressed=False)
        value = b"abc" * 10
        converted = prop._to_base_type(value)
        assert converted is None

    @staticmethod
    def test__from_base_type():
        prop = model.BlobProperty(name="blob")
        original = b"abc" * 10
        z_val = zlib.compress(original)
        value = model._CompressedValue(z_val)
        converted = prop._from_base_type(value)

        assert converted == original

    @staticmethod
    def test__from_base_type_no_convert():
        prop = model.BlobProperty(name="blob")
        converted = prop._from_base_type(b"abc")
        assert converted is None

    @staticmethod
    def test__db_set_value():
        prop = model.BlobProperty(name="blob")
        with pytest.raises(NotImplementedError):
            prop._db_set_value(None, None, None)

    @staticmethod
    def test__db_set_compressed_meaning():
        prop = model.BlobProperty(name="blob")
        with pytest.raises(NotImplementedError):
            prop._db_set_compressed_meaning(None)

    @staticmethod
    def test__db_set_uncompressed_meaning():
        prop = model.BlobProperty(name="blob")
        with pytest.raises(NotImplementedError):
            prop._db_set_uncompressed_meaning(None)

    @staticmethod
    def test__db_get_value():
        prop = model.BlobProperty(name="blob")
        with pytest.raises(NotImplementedError):
            prop._db_get_value(None, None)


class TestTextProperty:
    @staticmethod
    def test_constructor_defaults():
        prop = model.TextProperty()
        assert not prop._indexed

    @staticmethod
    def test_constructor_explicit():
        prop = model.TextProperty(name="text", indexed=False)
        assert prop._name == b"text"
        assert not prop._indexed

    @staticmethod
    def test_constructor_not_allowed():
        with pytest.raises(NotImplementedError):
            model.TextProperty(indexed=True)

    @staticmethod
    def test__validate():
        prop = model.TextProperty(name="text")
        assert prop._validate("abc") is None

    @staticmethod
    def test__validate_bad_bytes():
        prop = model.TextProperty(name="text")
        value = b"\x80abc"
        with pytest.raises(exceptions.BadValueError):
            prop._validate(value)

    @staticmethod
    def test__validate_bad_type():
        prop = model.TextProperty(name="text")
        with pytest.raises(exceptions.BadValueError):
            prop._validate(None)

    @staticmethod
    def test__to_base_type():
        prop = model.TextProperty(name="text")
        assert prop._to_base_type(b"abc") is None

    @staticmethod
    def test__to_base_type_converted():
        prop = model.TextProperty(name="text")
        value = "\N{snowman}"
        assert prop._to_base_type(value) == b"\xe2\x98\x83"

    @staticmethod
    def test__from_base_type():
        prop = model.TextProperty(name="text")
        assert prop._from_base_type("abc") is None

    @staticmethod
    def test__from_base_type_converted():
        prop = model.TextProperty(name="text")
        value = b"\xe2\x98\x83"
        assert prop._from_base_type(value) == "\N{snowman}"

    @staticmethod
    def test__from_base_type_cannot_convert():
        prop = model.TextProperty(name="text")
        value = b"\x80abc"
        assert prop._from_base_type(value) is None

    @staticmethod
    def test__db_set_uncompressed_meaning():
        prop = model.TextProperty(name="text")
        with pytest.raises(NotImplementedError):
            prop._db_set_uncompressed_meaning(None)


class TestStringProperty:
    @staticmethod
    def test_constructor_defaults():
        prop = model.StringProperty()
        assert prop._indexed

    @staticmethod
    def test_constructor_explicit():
        prop = model.StringProperty(name="limited-text", indexed=True)
        assert prop._name == b"limited-text"
        assert prop._indexed

    @staticmethod
    def test_constructor_not_allowed():
        with pytest.raises(NotImplementedError):
            model.StringProperty(indexed=False)

    @staticmethod
    def test__validate_bad_length():
        prop = model.StringProperty(name="limited-text")
        value = b"1" * 2000
        with pytest.raises(exceptions.BadValueError):
            prop._validate(value)


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
