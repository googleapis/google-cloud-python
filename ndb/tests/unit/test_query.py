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

import pickle
import unittest.mock

import pytest

from google.cloud.ndb import exceptions
from google.cloud.ndb import key as key_module
from google.cloud.ndb import model
from google.cloud.ndb import query
import tests.unit.utils


def test___all__():
    tests.unit.utils.verify___all__(query)


def test_Cursor():
    assert query.Cursor is NotImplemented


class TestQueryOptions:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            query.QueryOptions()


class TestRepeatedStructuredPropertyPredicate:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            query.RepeatedStructuredPropertyPredicate()


class TestParameterizedThing:
    @staticmethod
    def test___eq__():
        thing = query.ParameterizedThing()
        with pytest.raises(NotImplementedError):
            thing == None

    @staticmethod
    def test___ne__():
        thing = query.ParameterizedThing()
        with pytest.raises(NotImplementedError):
            thing != None


class TestParameter:
    @staticmethod
    def test_constructor():
        for key in (88, b"abc", "def"):
            parameter = query.Parameter(key)
            assert parameter._key == key

    @staticmethod
    def test_constructor_invalid():
        with pytest.raises(TypeError):
            query.Parameter(None)

    @staticmethod
    def test___repr__():
        parameter = query.Parameter("ghi")
        assert repr(parameter) == "Parameter('ghi')"

    @staticmethod
    def test___eq__():
        parameter1 = query.Parameter("yep")
        parameter2 = query.Parameter("nope")
        parameter3 = unittest.mock.sentinel.parameter
        assert parameter1 == parameter1
        assert not parameter1 == parameter2
        assert not parameter1 == parameter3

    @staticmethod
    def test___ne__():
        parameter1 = query.Parameter("yep")
        parameter2 = query.Parameter("nope")
        parameter3 = unittest.mock.sentinel.parameter
        assert not parameter1 != parameter1
        assert parameter1 != parameter2
        assert parameter1 != parameter3

    @staticmethod
    def test_key():
        parameter = query.Parameter(9000)
        assert parameter.key == 9000

    @staticmethod
    def test_resolve():
        key = 9000
        bound_value = "resoolt"
        parameter = query.Parameter(key)
        used = {}
        result = parameter.resolve({key: bound_value}, used)
        assert result == bound_value
        assert used == {key: True}

    @staticmethod
    def test_resolve_missing_key():
        parameter = query.Parameter(9000)
        used = {}
        with pytest.raises(exceptions.BadArgumentError):
            parameter.resolve({}, used)

        assert used == {}


class TestParameterizedFunction:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            query.ParameterizedFunction()


class TestNode:
    @staticmethod
    def test_constructor():
        with pytest.raises(TypeError):
            query.Node()

    @staticmethod
    def _make_one():
        # Bypass the intentionally broken constructor.
        node = object.__new__(query.Node)
        assert isinstance(node, query.Node)
        return node

    def test___eq__(self):
        node = self._make_one()
        with pytest.raises(NotImplementedError):
            node == None

    def test___ne__(self):
        node = self._make_one()
        with pytest.raises(NotImplementedError):
            node != None

    def test___le__(self):
        node = self._make_one()
        with pytest.raises(TypeError) as exc_info:
            node <= None

        assert exc_info.value.args == ("Nodes cannot be ordered",)

    def test___lt__(self):
        node = self._make_one()
        with pytest.raises(TypeError) as exc_info:
            node < None

        assert exc_info.value.args == ("Nodes cannot be ordered",)

    def test___ge__(self):
        node = self._make_one()
        with pytest.raises(TypeError) as exc_info:
            node >= None

        assert exc_info.value.args == ("Nodes cannot be ordered",)

    def test___gt__(self):
        node = self._make_one()
        with pytest.raises(TypeError) as exc_info:
            node > None

        assert exc_info.value.args == ("Nodes cannot be ordered",)

    def test__to_filter(self):
        node = self._make_one()
        with pytest.raises(NotImplementedError):
            node._to_filter()

    def test__post_filters(self):
        node = self._make_one()
        assert node._post_filters() is None

    def test_resolve(self):
        node = self._make_one()
        used = {}
        assert node.resolve({}, used) is node
        assert used == {}


class TestFalseNode:
    @staticmethod
    def test___eq__():
        false_node1 = query.FalseNode()
        false_node2 = query.FalseNode()
        false_node3 = unittest.mock.sentinel.false_node
        assert false_node1 == false_node1
        assert false_node1 == false_node2
        assert not false_node1 == false_node3

    @staticmethod
    def test__to_filter():
        false_node = query.FalseNode()
        with pytest.raises(_exceptions.BadQueryError):
            false_node._to_filter()

    @staticmethod
    def test__to_filter_post():
        false_node = query.FalseNode()
        assert false_node._to_filter(post=True) is None


class TestParameterNode:
    @staticmethod
    def test_constructor():
        prop = model.Property(name="val")
        param = query.Parameter("abc")
        parameter_node = query.ParameterNode(prop, "=", param)
        assert parameter_node._prop is prop
        assert parameter_node._op == "="
        assert parameter_node._param is param

    @staticmethod
    def test_constructor_bad_property():
        param = query.Parameter(11)
        with pytest.raises(TypeError):
            query.ParameterNode(None, "!=", param)

    @staticmethod
    def test_constructor_bad_op():
        prop = model.Property(name="guitar")
        param = query.Parameter("pick")
        with pytest.raises(TypeError):
            query.ParameterNode(prop, "less", param)

    @staticmethod
    def test_constructor_bad_param():
        prop = model.Property(name="california")
        with pytest.raises(TypeError):
            query.ParameterNode(prop, "<", None)

    @staticmethod
    def test_pickling():
        prop = model.Property(name="val")
        param = query.Parameter("abc")
        parameter_node = query.ParameterNode(prop, "=", param)

        pickled = pickle.dumps(parameter_node)
        unpickled = pickle.loads(pickled)
        assert parameter_node == unpickled

    @staticmethod
    def test___repr__():
        prop = model.Property(name="val")
        param = query.Parameter("abc")
        parameter_node = query.ParameterNode(prop, "=", param)

        expected = "ParameterNode({!r}, '=', Parameter('abc'))".format(prop)
        assert repr(parameter_node) == expected

    @staticmethod
    def test___eq__():
        prop1 = model.Property(name="val")
        param1 = query.Parameter("abc")
        parameter_node1 = query.ParameterNode(prop1, "=", param1)
        prop2 = model.Property(name="ue")
        parameter_node2 = query.ParameterNode(prop2, "=", param1)
        parameter_node3 = query.ParameterNode(prop1, "<", param1)
        param2 = query.Parameter(900)
        parameter_node4 = query.ParameterNode(prop1, "=", param2)
        parameter_node5 = unittest.mock.sentinel.parameter_node

        assert parameter_node1 == parameter_node1
        assert not parameter_node1 == parameter_node2
        assert not parameter_node1 == parameter_node3
        assert not parameter_node1 == parameter_node4
        assert not parameter_node1 == parameter_node5

    @staticmethod
    def test__to_filter():
        prop = model.Property(name="val")
        param = query.Parameter("abc")
        parameter_node = query.ParameterNode(prop, "=", param)
        with pytest.raises(_exceptions.BadArgumentError):
            parameter_node._to_filter()

    @staticmethod
    def test_resolve():
        prop = model.Property(name="val")
        param = query.Parameter("abc")
        parameter_node = query.ParameterNode(prop, "=", param)

        used = {}
        with pytest.raises(NotImplementedError):
            parameter_node.resolve({}, used)
        assert used == {}


class TestFilterNode:
    @staticmethod
    def test_constructor():
        filter_node = query.FilterNode("a", ">", 9)
        assert filter_node._name == "a"
        assert filter_node._opsymbol == ">"
        assert filter_node._value == 9

    @staticmethod
    def test_constructor_with_key():
        key = key_module.Key("a", "b", app="c", namespace="d")
        with pytest.raises(NotImplementedError):
            query.FilterNode("name", "=", key)

    @staticmethod
    @unittest.mock.patch("google.cloud.ndb.query.DisjunctionNode")
    def test_constructor_in(disjunction_node):
        or_node = query.FilterNode("a", "in", ("x", "y", "z"))
        assert or_node is disjunction_node.return_value

        filter_node1 = query.FilterNode("a", "=", "x")
        filter_node2 = query.FilterNode("a", "=", "y")
        filter_node3 = query.FilterNode("a", "=", "z")
        disjunction_node.assert_called_once_with(
            filter_node1, filter_node2, filter_node3
        )

    @staticmethod
    def test_constructor_in_single():
        filter_node = query.FilterNode("a", "in", [9000])
        assert isinstance(filter_node, query.FilterNode)
        assert filter_node._name == "a"
        assert filter_node._opsymbol == "="
        assert filter_node._value == 9000

    @staticmethod
    def test_constructor_in_empty():
        filter_node = query.FilterNode("a", "in", set())
        assert isinstance(filter_node, query.FalseNode)

    @staticmethod
    def test_constructor_in_invalid_container():
        with pytest.raises(TypeError):
            query.FilterNode("a", "in", {})

    @staticmethod
    @unittest.mock.patch("google.cloud.ndb.query.DisjunctionNode")
    def test_constructor_ne(disjunction_node):
        or_node = query.FilterNode("a", "!=", 2.5)
        assert or_node is disjunction_node.return_value

        filter_node1 = query.FilterNode("a", "<", 2.5)
        filter_node2 = query.FilterNode("a", ">", 2.5)
        disjunction_node.assert_called_once_with(filter_node1, filter_node2)

    @staticmethod
    def test_pickling():
        filter_node = query.FilterNode("speed", ">=", 88)

        pickled = pickle.dumps(filter_node)
        unpickled = pickle.loads(pickled)
        assert filter_node == unpickled

    @staticmethod
    def test___repr__():
        filter_node = query.FilterNode("speed", ">=", 88)
        assert repr(filter_node) == "FilterNode('speed', '>=', 88)"

    @staticmethod
    def test___eq__():
        filter_node1 = query.FilterNode("speed", ">=", 88)
        filter_node2 = query.FilterNode("slow", ">=", 88)
        filter_node3 = query.FilterNode("speed", "<=", 88)
        filter_node4 = query.FilterNode("speed", ">=", 188)
        filter_node5 = unittest.mock.sentinel.filter_node
        assert filter_node1 == filter_node1
        assert not filter_node1 == filter_node2
        assert not filter_node1 == filter_node3
        assert not filter_node1 == filter_node4
        assert not filter_node1 == filter_node5

    @staticmethod
    def test__to_filter_post():
        filter_node = query.FilterNode("speed", ">=", 88)
        assert filter_node._to_filter(post=True) is None

    @staticmethod
    def test__to_filter_bad_op():
        filter_node = query.FilterNode("speed", ">=", 88)
        filter_node._opsymbol = "!="
        with pytest.raises(NotImplementedError):
            filter_node._to_filter()

    @staticmethod
    def test__to_filter():
        filter_node = query.FilterNode("speed", ">=", 88)
        with pytest.raises(NotImplementedError):
            filter_node._to_filter()


class TestPostFilterNode:
    @staticmethod
    def test_constructor():
        predicate = unittest.mock.sentinel.predicate
        post_filter_node = query.PostFilterNode(predicate)
        assert post_filter_node.predicate is predicate

    @staticmethod
    def test_pickling():
        predicate = "must-be-pickle-able"
        post_filter_node = query.PostFilterNode(predicate)

        pickled = pickle.dumps(post_filter_node)
        unpickled = pickle.loads(pickled)
        assert post_filter_node == unpickled

    @staticmethod
    def test___repr__():
        predicate = "predicate-not-repr"
        post_filter_node = query.PostFilterNode(predicate)
        assert repr(post_filter_node) == "PostFilterNode(predicate-not-repr)"

    @staticmethod
    def test___eq__():
        predicate1 = unittest.mock.sentinel.predicate1
        post_filter_node1 = query.PostFilterNode(predicate1)
        predicate2 = unittest.mock.sentinel.predicate2
        post_filter_node2 = query.PostFilterNode(predicate2)
        post_filter_node3 = unittest.mock.sentinel.post_filter_node
        assert post_filter_node1 == post_filter_node1
        assert not post_filter_node1 == post_filter_node2
        assert not post_filter_node1 == post_filter_node3

    @staticmethod
    def test__to_filter_post():
        predicate = unittest.mock.sentinel.predicate
        post_filter_node = query.PostFilterNode(predicate)
        assert post_filter_node._to_filter(post=True) is predicate

    @staticmethod
    def test__to_filter():
        predicate = unittest.mock.sentinel.predicate
        post_filter_node = query.PostFilterNode(predicate)
        assert post_filter_node._to_filter() is None


class TestConjunctionNode:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            query.ConjunctionNode()


class TestDisjunctionNode:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            query.DisjunctionNode()


def test_AND():
    assert query.AND is query.ConjunctionNode


def test_OR():
    assert query.OR is query.DisjunctionNode


class TestQuery:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            query.Query()


def test_gql():
    with pytest.raises(NotImplementedError):
        query.gql()


class TestQueryIterator:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            query.QueryIterator()
