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
from google.cloud.ndb import query as query_module
from google.cloud.ndb import tasklets
import tests.unit.utils


def test___all__():
    tests.unit.utils.verify___all__(query_module)


def test_Cursor():
    assert query_module.Cursor is NotImplemented


class TestQueryOptions:
    @staticmethod
    def test_constructor():
        options = query_module.QueryOptions(kind="test", project="app")
        assert options.kind == "test"
        assert options.project == "app"

    @staticmethod
    def test_constructor_with_config():
        config = query_module.QueryOptions(
            kind="other", namespace="config_test"
        )
        options = query_module.QueryOptions(
            config=config, kind="test", project="app"
        )
        assert options.kind == "test"
        assert options.project == "app"
        assert options.namespace == "config_test"

    @staticmethod
    def test_constructor_with_bad_config():
        with pytest.raises(TypeError):
            query_module.QueryOptions(config="bad")

    @staticmethod
    def test___repr__():
        representation = "QueryOptions(kind='test', project='app')"
        options = query_module.QueryOptions(kind="test", project="app")
        assert options.__repr__() == representation

    @staticmethod
    def test__eq__():
        options = query_module.QueryOptions(kind="test", project="app")
        other = query_module.QueryOptions(kind="test", project="app")
        otherother = query_module.QueryOptions(kind="nope", project="noway")

        assert options == other
        assert options != otherother
        assert options != "foo"


class TestPropertyOrder:
    @staticmethod
    def test_constructor():
        order = query_module.PropertyOrder(name="property", reverse=False)
        assert order.name == "property"
        assert order.reverse is False

    @staticmethod
    def test___repr__():
        representation = "PropertyOrder(name='property', reverse=False)"
        order = query_module.PropertyOrder(name="property", reverse=False)
        assert order.__repr__() == representation

    @staticmethod
    def test___neg__ascending():
        order = query_module.PropertyOrder(name="property", reverse=False)
        assert order.reverse is False
        new_order = -order
        assert new_order.reverse is True

    @staticmethod
    def test___neg__descending():
        order = query_module.PropertyOrder(name="property", reverse=True)
        assert order.reverse is True
        new_order = -order
        assert new_order.reverse is False


class TestRepeatedStructuredPropertyPredicate:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            query_module.RepeatedStructuredPropertyPredicate()


class TestParameterizedThing:
    @staticmethod
    def test___eq__():
        thing = query_module.ParameterizedThing()
        with pytest.raises(NotImplementedError):
            thing == unittest.mock.sentinel.other

    @staticmethod
    def test___ne__():
        thing = query_module.ParameterizedThing()
        with pytest.raises(NotImplementedError):
            thing != unittest.mock.sentinel.other


class TestParameter:
    @staticmethod
    def test_constructor():
        for key in (88, "def"):
            parameter = query_module.Parameter(key)
            assert parameter._key == key

    @staticmethod
    def test_constructor_invalid():
        with pytest.raises(TypeError):
            query_module.Parameter(None)

    @staticmethod
    def test___repr__():
        parameter = query_module.Parameter("ghi")
        assert repr(parameter) == "Parameter('ghi')"

    @staticmethod
    def test___eq__():
        parameter1 = query_module.Parameter("yep")
        parameter2 = query_module.Parameter("nope")
        parameter3 = unittest.mock.sentinel.parameter
        assert parameter1 == parameter1
        assert not parameter1 == parameter2
        assert not parameter1 == parameter3

    @staticmethod
    def test___ne__():
        parameter1 = query_module.Parameter("yep")
        parameter2 = query_module.Parameter("nope")
        parameter3 = unittest.mock.sentinel.parameter
        assert not parameter1 != parameter1
        assert parameter1 != parameter2
        assert parameter1 != parameter3

    @staticmethod
    def test_key():
        parameter = query_module.Parameter(9000)
        assert parameter.key == 9000

    @staticmethod
    def test_resolve():
        key = 9000
        bound_value = "resoolt"
        parameter = query_module.Parameter(key)
        used = {}
        result = parameter.resolve({key: bound_value}, used)
        assert result == bound_value
        assert used == {key: True}

    @staticmethod
    def test_resolve_missing_key():
        parameter = query_module.Parameter(9000)
        used = {}
        with pytest.raises(exceptions.BadArgumentError):
            parameter.resolve({}, used)

        assert used == {}


class TestParameterizedFunction:
    @staticmethod
    def test_constructor():
        query = query_module.ParameterizedFunction(
            "user", query_module.Parameter(1)
        )
        assert query.func == "user"
        assert query.values == query_module.Parameter(1)

    @staticmethod
    def test___repr__():
        query = query_module.ParameterizedFunction(
            "user", query_module.Parameter(1)
        )
        assert (
            query.__repr__() == "ParameterizedFunction('user', Parameter(1))"
        )

    @staticmethod
    def test___eq__parameter():
        query = query_module.ParameterizedFunction(
            "user", query_module.Parameter(1)
        )
        assert (
            query.__eq__(
                query_module.ParameterizedFunction(
                    "user", query_module.Parameter(1)
                )
            )
            is True
        )

    @staticmethod
    def test___eq__no_parameter():
        query = query_module.ParameterizedFunction(
            "user", query_module.Parameter(1)
        )
        assert query.__eq__(42) is NotImplemented


class TestNode:
    @staticmethod
    def test_constructor():
        with pytest.raises(TypeError):
            query_module.Node()

    @staticmethod
    def _make_one():
        # Bypass the intentionally broken constructor.
        node = object.__new__(query_module.Node)
        assert isinstance(node, query_module.Node)
        return node

    def test___eq__(self):
        node = self._make_one()
        with pytest.raises(NotImplementedError):
            node == unittest.mock.sentinel.other

    def test___ne__(self):
        node = self._make_one()
        with pytest.raises(NotImplementedError):
            node != unittest.mock.sentinel.other

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
        false_node1 = query_module.FalseNode()
        false_node2 = query_module.FalseNode()
        false_node3 = unittest.mock.sentinel.false_node
        assert false_node1 == false_node1
        assert false_node1 == false_node2
        assert not false_node1 == false_node3

    @staticmethod
    def test__to_filter():
        false_node = query_module.FalseNode()
        with pytest.raises(exceptions.BadQueryError):
            false_node._to_filter()

    @staticmethod
    def test__to_filter_post():
        false_node = query_module.FalseNode()
        assert false_node._to_filter(post=True) is None


class TestParameterNode:
    @staticmethod
    def test_constructor():
        prop = model.Property(name="val")
        param = query_module.Parameter("abc")
        parameter_node = query_module.ParameterNode(prop, "=", param)
        assert parameter_node._prop is prop
        assert parameter_node._op == "="
        assert parameter_node._param is param

    @staticmethod
    def test_constructor_bad_property():
        param = query_module.Parameter(11)
        with pytest.raises(TypeError):
            query_module.ParameterNode(None, "!=", param)

    @staticmethod
    def test_constructor_bad_op():
        prop = model.Property(name="guitar")
        param = query_module.Parameter("pick")
        with pytest.raises(TypeError):
            query_module.ParameterNode(prop, "less", param)

    @staticmethod
    def test_constructor_bad_param():
        prop = model.Property(name="california")
        with pytest.raises(TypeError):
            query_module.ParameterNode(prop, "<", None)

    @staticmethod
    def test_pickling():
        prop = model.Property(name="val")
        param = query_module.Parameter("abc")
        parameter_node = query_module.ParameterNode(prop, "=", param)

        pickled = pickle.dumps(parameter_node)
        unpickled = pickle.loads(pickled)
        assert parameter_node == unpickled

    @staticmethod
    def test___repr__():
        prop = model.Property(name="val")
        param = query_module.Parameter("abc")
        parameter_node = query_module.ParameterNode(prop, "=", param)

        expected = "ParameterNode({!r}, '=', Parameter('abc'))".format(prop)
        assert repr(parameter_node) == expected

    @staticmethod
    def test___eq__():
        prop1 = model.Property(name="val")
        param1 = query_module.Parameter("abc")
        parameter_node1 = query_module.ParameterNode(prop1, "=", param1)
        prop2 = model.Property(name="ue")
        parameter_node2 = query_module.ParameterNode(prop2, "=", param1)
        parameter_node3 = query_module.ParameterNode(prop1, "<", param1)
        param2 = query_module.Parameter(900)
        parameter_node4 = query_module.ParameterNode(prop1, "=", param2)
        parameter_node5 = unittest.mock.sentinel.parameter_node

        assert parameter_node1 == parameter_node1
        assert not parameter_node1 == parameter_node2
        assert not parameter_node1 == parameter_node3
        assert not parameter_node1 == parameter_node4
        assert not parameter_node1 == parameter_node5

    @staticmethod
    def test__to_filter():
        prop = model.Property(name="val")
        param = query_module.Parameter("abc")
        parameter_node = query_module.ParameterNode(prop, "=", param)
        with pytest.raises(exceptions.BadArgumentError):
            parameter_node._to_filter()

    @staticmethod
    def test_resolve_simple():
        prop = model.Property(name="val")
        param = query_module.Parameter("abc")
        parameter_node = query_module.ParameterNode(prop, "=", param)

        value = 67
        bindings = {"abc": value}
        used = {}
        resolved_node = parameter_node.resolve(bindings, used)

        assert resolved_node == query_module.FilterNode("val", "=", value)
        assert used == {"abc": True}

    @staticmethod
    def test_resolve_with_in():
        prop = model.Property(name="val")
        param = query_module.Parameter("replace")
        parameter_node = query_module.ParameterNode(prop, "in", param)

        value = (19, 20, 28)
        bindings = {"replace": value}
        used = {}
        resolved_node = parameter_node.resolve(bindings, used)

        assert resolved_node == query_module.DisjunctionNode(
            query_module.FilterNode("val", "=", 19),
            query_module.FilterNode("val", "=", 20),
            query_module.FilterNode("val", "=", 28),
        )
        assert used == {"replace": True}

    @staticmethod
    def test_resolve_in_empty_container():
        prop = model.Property(name="val")
        param = query_module.Parameter("replace")
        parameter_node = query_module.ParameterNode(prop, "in", param)

        value = ()
        bindings = {"replace": value}
        used = {}
        resolved_node = parameter_node.resolve(bindings, used)

        assert resolved_node == query_module.FalseNode()
        assert used == {"replace": True}


class TestFilterNode:
    @staticmethod
    def test_constructor():
        filter_node = query_module.FilterNode("a", ">", 9)
        assert filter_node._name == "a"
        assert filter_node._opsymbol == ">"
        assert filter_node._value == 9

    @staticmethod
    def test_constructor_with_key():
        key = key_module.Key("a", "b", app="c", namespace="d")
        filter_node = query_module.FilterNode("name", "=", key)
        assert filter_node._name == "name"
        assert filter_node._opsymbol == "="
        assert filter_node._value is key._key

    @staticmethod
    def test_constructor_in():
        or_node = query_module.FilterNode("a", "in", ("x", "y", "z"))

        filter_node1 = query_module.FilterNode("a", "=", "x")
        filter_node2 = query_module.FilterNode("a", "=", "y")
        filter_node3 = query_module.FilterNode("a", "=", "z")
        assert or_node == query_module.DisjunctionNode(
            filter_node1, filter_node2, filter_node3
        )

    @staticmethod
    def test_constructor_in_single():
        filter_node = query_module.FilterNode("a", "in", [9000])
        assert isinstance(filter_node, query_module.FilterNode)
        assert filter_node._name == "a"
        assert filter_node._opsymbol == "="
        assert filter_node._value == 9000

    @staticmethod
    def test_constructor_in_empty():
        filter_node = query_module.FilterNode("a", "in", set())
        assert isinstance(filter_node, query_module.FalseNode)

    @staticmethod
    def test_constructor_in_invalid_container():
        with pytest.raises(TypeError):
            query_module.FilterNode("a", "in", {})

    @staticmethod
    def test_constructor_ne():
        or_node = query_module.FilterNode("a", "!=", 2.5)

        filter_node1 = query_module.FilterNode("a", "<", 2.5)
        filter_node2 = query_module.FilterNode("a", ">", 2.5)
        assert or_node == query_module.DisjunctionNode(
            filter_node1, filter_node2
        )

    @staticmethod
    def test_pickling():
        filter_node = query_module.FilterNode("speed", ">=", 88)

        pickled = pickle.dumps(filter_node)
        unpickled = pickle.loads(pickled)
        assert filter_node == unpickled

    @staticmethod
    def test___repr__():
        filter_node = query_module.FilterNode("speed", ">=", 88)
        assert repr(filter_node) == "FilterNode('speed', '>=', 88)"

    @staticmethod
    def test___eq__():
        filter_node1 = query_module.FilterNode("speed", ">=", 88)
        filter_node2 = query_module.FilterNode("slow", ">=", 88)
        filter_node3 = query_module.FilterNode("speed", "<=", 88)
        filter_node4 = query_module.FilterNode("speed", ">=", 188)
        filter_node5 = unittest.mock.sentinel.filter_node
        assert filter_node1 == filter_node1
        assert not filter_node1 == filter_node2
        assert not filter_node1 == filter_node3
        assert not filter_node1 == filter_node4
        assert not filter_node1 == filter_node5

    @staticmethod
    def test__to_filter_post():
        filter_node = query_module.FilterNode("speed", ">=", 88)
        assert filter_node._to_filter(post=True) is None

    @staticmethod
    def test__to_filter_bad_op():
        filter_node = query_module.FilterNode("speed", ">=", 88)
        filter_node._opsymbol = "!="
        with pytest.raises(NotImplementedError):
            filter_node._to_filter()

    @staticmethod
    @unittest.mock.patch("google.cloud.ndb.query._datastore_query")
    def test__to_filter(_datastore_query):
        as_filter = _datastore_query.make_filter.return_value
        filter_node = query_module.FilterNode("speed", ">=", 88)
        assert filter_node._to_filter() is as_filter
        _datastore_query.make_filter.assert_called_once_with("speed", ">=", 88)


class TestPostFilterNode:
    @staticmethod
    def test_constructor():
        predicate = unittest.mock.sentinel.predicate
        post_filter_node = query_module.PostFilterNode(predicate)
        assert post_filter_node.predicate is predicate

    @staticmethod
    def test_pickling():
        predicate = "must-be-pickle-able"
        post_filter_node = query_module.PostFilterNode(predicate)

        pickled = pickle.dumps(post_filter_node)
        unpickled = pickle.loads(pickled)
        assert post_filter_node == unpickled

    @staticmethod
    def test___repr__():
        predicate = "predicate-not-repr"
        post_filter_node = query_module.PostFilterNode(predicate)
        assert repr(post_filter_node) == "PostFilterNode(predicate-not-repr)"

    @staticmethod
    def test___eq__():
        predicate1 = unittest.mock.sentinel.predicate1
        post_filter_node1 = query_module.PostFilterNode(predicate1)
        predicate2 = unittest.mock.sentinel.predicate2
        post_filter_node2 = query_module.PostFilterNode(predicate2)
        post_filter_node3 = unittest.mock.sentinel.post_filter_node
        assert post_filter_node1 == post_filter_node1
        assert not post_filter_node1 == post_filter_node2
        assert not post_filter_node1 == post_filter_node3

    @staticmethod
    def test__to_filter_post():
        predicate = unittest.mock.sentinel.predicate
        post_filter_node = query_module.PostFilterNode(predicate)
        assert post_filter_node._to_filter(post=True) is predicate

    @staticmethod
    def test__to_filter():
        predicate = unittest.mock.sentinel.predicate
        post_filter_node = query_module.PostFilterNode(predicate)
        assert post_filter_node._to_filter() is None


class Test_BooleanClauses:
    @staticmethod
    def test_constructor_or():
        or_clauses = query_module._BooleanClauses("name", True)
        assert or_clauses.name == "name"
        assert or_clauses.combine_or
        assert or_clauses.or_parts == []

    @staticmethod
    def test_constructor_and():
        and_clauses = query_module._BooleanClauses("name", False)
        assert and_clauses.name == "name"
        assert not and_clauses.combine_or
        assert and_clauses.or_parts == [[]]

    @staticmethod
    def test_add_node_invalid():
        clauses = query_module._BooleanClauses("name", False)
        with pytest.raises(TypeError):
            clauses.add_node(None)

    @staticmethod
    def test_add_node_or_with_simple():
        clauses = query_module._BooleanClauses("name", True)
        node = query_module.FilterNode("a", "=", 7)
        clauses.add_node(node)
        assert clauses.or_parts == [node]

    @staticmethod
    def test_add_node_or_with_disjunction():
        clauses = query_module._BooleanClauses("name", True)
        node1 = query_module.FilterNode("a", "=", 7)
        node2 = query_module.FilterNode("b", ">", 7.5)
        node3 = query_module.DisjunctionNode(node1, node2)
        clauses.add_node(node3)
        assert clauses.or_parts == [node1, node2]

    @staticmethod
    def test_add_node_and_with_simple():
        clauses = query_module._BooleanClauses("name", False)
        node1 = query_module.FilterNode("a", "=", 7)
        node2 = query_module.FilterNode("b", ">", 7.5)
        node3 = query_module.FilterNode("c", "<", "now")
        # Modify to see the "broadcast"
        clauses.or_parts = [[node1], [node2], [node3]]

        node4 = query_module.FilterNode("d", ">=", 80)
        clauses.add_node(node4)
        assert clauses.or_parts == [
            [node1, node4],
            [node2, node4],
            [node3, node4],
        ]

    @staticmethod
    def test_add_node_and_with_conjunction():
        clauses = query_module._BooleanClauses("name", False)
        node1 = query_module.FilterNode("a", "=", 7)
        node2 = query_module.FilterNode("b", ">", 7.5)
        clauses.or_parts = [[node1], [node2]]  # Modify to see the "broadcast"

        node3 = query_module.FilterNode("c", "<", "now")
        node4 = query_module.FilterNode("d", ">=", 80)
        node5 = query_module.ConjunctionNode(node3, node4)
        clauses.add_node(node5)
        assert clauses.or_parts == [
            [node1, node3, node4],
            [node2, node3, node4],
        ]

    @staticmethod
    def test_add_node_and_with_disjunction():
        clauses = query_module._BooleanClauses("name", False)
        node1 = query_module.FilterNode("a", "=", 7)
        node2 = query_module.FilterNode("b", ">", 7.5)
        clauses.or_parts = [[node1], [node2]]  # Modify to see the "broadcast"

        node3 = query_module.FilterNode("c", "<", "now")
        node4 = query_module.FilterNode("d", ">=", 80)
        node5 = query_module.DisjunctionNode(node3, node4)
        clauses.add_node(node5)
        assert clauses.or_parts == [
            [node1, node3],
            [node1, node4],
            [node2, node3],
            [node2, node4],
        ]


class TestConjunctionNode:
    @staticmethod
    def test_constructor_no_nodes():
        with pytest.raises(TypeError):
            query_module.ConjunctionNode()

    @staticmethod
    def test_constructor_one_node():
        node = query_module.FilterNode("a", "=", 7)
        result_node = query_module.ConjunctionNode(node)
        assert result_node is node

    @staticmethod
    def test_constructor_many_nodes():
        node1 = query_module.FilterNode("a", "=", 7)
        node2 = query_module.FilterNode("b", ">", 7.5)
        node3 = query_module.FilterNode("c", "<", "now")
        node4 = query_module.FilterNode("d", ">=", 80)

        result_node = query_module.ConjunctionNode(node1, node2, node3, node4)
        assert isinstance(result_node, query_module.ConjunctionNode)
        assert result_node._nodes == [node1, node2, node3, node4]

    @staticmethod
    def test_constructor_convert_or():
        node1 = query_module.FilterNode("a", "=", 7)
        node2 = query_module.FilterNode("b", ">", 7.5)
        node3 = query_module.DisjunctionNode(node1, node2)
        node4 = query_module.FilterNode("d", ">=", 80)

        result_node = query_module.ConjunctionNode(node3, node4)
        assert isinstance(result_node, query_module.DisjunctionNode)
        assert result_node._nodes == [
            query_module.ConjunctionNode(node1, node4),
            query_module.ConjunctionNode(node2, node4),
        ]

    @staticmethod
    @unittest.mock.patch("google.cloud.ndb.query._BooleanClauses")
    def test_constructor_unreachable(boolean_clauses):
        clauses = unittest.mock.Mock(
            or_parts=[], spec=("add_node", "or_parts")
        )
        boolean_clauses.return_value = clauses

        node1 = query_module.FilterNode("a", "=", 7)
        node2 = query_module.FilterNode("b", ">", 7.5)

        with pytest.raises(RuntimeError):
            query_module.ConjunctionNode(node1, node2)

        boolean_clauses.assert_called_once_with(
            "ConjunctionNode", combine_or=False
        )
        assert clauses.add_node.call_count == 2
        clauses.add_node.assert_has_calls(
            [unittest.mock.call(node1), unittest.mock.call(node2)]
        )

    @staticmethod
    def test_pickling():
        node1 = query_module.FilterNode("a", "=", 7)
        node2 = query_module.FilterNode("b", ">", 7.5)
        and_node = query_module.ConjunctionNode(node1, node2)

        pickled = pickle.dumps(and_node)
        unpickled = pickle.loads(pickled)
        assert and_node == unpickled

    @staticmethod
    def test___iter__():
        node1 = query_module.FilterNode("a", "=", 7)
        node2 = query_module.FilterNode("b", ">", 7.5)
        and_node = query_module.ConjunctionNode(node1, node2)

        assert list(and_node) == and_node._nodes

    @staticmethod
    def test___repr__():
        node1 = query_module.FilterNode("a", "=", 7)
        node2 = query_module.FilterNode("b", ">", 7.5)
        and_node = query_module.ConjunctionNode(node1, node2)
        expected = "AND(FilterNode('a', '=', 7), FilterNode('b', '>', 7.5))"
        assert repr(and_node) == expected

    @staticmethod
    def test___eq__():
        filter_node1 = query_module.FilterNode("a", "=", 7)
        filter_node2 = query_module.FilterNode("b", ">", 7.5)
        filter_node3 = query_module.FilterNode("c", "<", "now")

        and_node1 = query_module.ConjunctionNode(filter_node1, filter_node2)
        and_node2 = query_module.ConjunctionNode(filter_node2, filter_node1)
        and_node3 = query_module.ConjunctionNode(filter_node1, filter_node3)
        and_node4 = unittest.mock.sentinel.and_node

        assert and_node1 == and_node1
        assert not and_node1 == and_node2
        assert not and_node1 == and_node3
        assert not and_node1 == and_node4

    @staticmethod
    def test__to_filter_empty():
        node1 = query_module.FilterNode("a", "=", 7)
        node2 = query_module.FilterNode("b", "<", 6)
        and_node = query_module.ConjunctionNode(node1, node2)

        as_filter = and_node._to_filter(post=True)
        assert as_filter is None

    @staticmethod
    def test__to_filter_single():
        node1 = unittest.mock.Mock(spec=query_module.FilterNode)
        node2 = query_module.PostFilterNode("predicate")
        node3 = unittest.mock.Mock(spec=query_module.FilterNode)
        node3._to_filter.return_value = False
        and_node = query_module.ConjunctionNode(node1, node2, node3)

        as_filter = and_node._to_filter()
        assert as_filter is node1._to_filter.return_value

        node1._to_filter.assert_called_once_with(post=False)

    @staticmethod
    @unittest.mock.patch("google.cloud.ndb.query._datastore_query")
    def test__to_filter_multiple(_datastore_query):
        node1 = query_module.PostFilterNode("predicate1")
        node2 = query_module.PostFilterNode("predicate2")
        and_node = query_module.ConjunctionNode(node1, node2)

        as_filter = _datastore_query.make_composite_and_filter.return_value
        assert and_node._to_filter(post=True) is as_filter
        _datastore_query.make_composite_and_filter.assert_called_once_with(
            ["predicate1", "predicate2"]
        )

    @staticmethod
    def test__post_filters_empty():
        node1 = query_module.FilterNode("a", "=", 7)
        node2 = query_module.FilterNode("b", ">", 77)
        and_node = query_module.ConjunctionNode(node1, node2)

        post_filters_node = and_node._post_filters()
        assert post_filters_node is None

    @staticmethod
    def test__post_filters_single():
        node1 = query_module.FilterNode("a", "=", 7)
        node2 = query_module.PostFilterNode("predicate2")
        and_node = query_module.ConjunctionNode(node1, node2)

        post_filters_node = and_node._post_filters()
        assert post_filters_node is node2

    @staticmethod
    def test__post_filters_multiple():
        node1 = query_module.FilterNode("a", "=", 7)
        node2 = query_module.PostFilterNode("predicate2")
        node3 = query_module.PostFilterNode("predicate3")
        and_node = query_module.ConjunctionNode(node1, node2, node3)

        post_filters_node = and_node._post_filters()
        assert post_filters_node == query_module.ConjunctionNode(node2, node3)

    @staticmethod
    def test__post_filters_same():
        node1 = query_module.PostFilterNode("predicate1")
        node2 = query_module.PostFilterNode("predicate2")
        and_node = query_module.ConjunctionNode(node1, node2)

        post_filters_node = and_node._post_filters()
        assert post_filters_node is and_node

    @staticmethod
    def test_resolve():
        node1 = query_module.FilterNode("a", "=", 7)
        node2 = query_module.FilterNode("b", ">", 77)
        and_node = query_module.ConjunctionNode(node1, node2)

        bindings = {}
        used = {}
        resolved_node = and_node.resolve(bindings, used)

        assert resolved_node is and_node
        assert bindings == {}
        assert used == {}

    @staticmethod
    def test_resolve_changed():
        node1 = unittest.mock.Mock(spec=query_module.FilterNode)
        node2 = query_module.FilterNode("b", ">", 77)
        node3 = query_module.FilterNode("c", "=", 7)
        node1.resolve.return_value = node3
        and_node = query_module.ConjunctionNode(node1, node2)

        bindings = {}
        used = {}
        resolved_node = and_node.resolve(bindings, used)

        assert isinstance(resolved_node, query_module.ConjunctionNode)
        assert resolved_node._nodes == [node3, node2]
        assert bindings == {}
        assert used == {}
        node1.resolve.assert_called_once_with(bindings, used)


class TestDisjunctionNode:
    @staticmethod
    def test_constructor_no_nodes():
        with pytest.raises(TypeError):
            query_module.DisjunctionNode()

    @staticmethod
    def test_constructor_one_node():
        node = query_module.FilterNode("a", "=", 7)
        result_node = query_module.DisjunctionNode(node)
        assert result_node is node

    @staticmethod
    def test_constructor_many_nodes():
        node1 = query_module.FilterNode("a", "=", 7)
        node2 = query_module.FilterNode("b", ">", 7.5)
        node3 = query_module.FilterNode("c", "<", "now")
        node4 = query_module.FilterNode("d", ">=", 80)

        result_node = query_module.DisjunctionNode(node1, node2, node3, node4)
        assert isinstance(result_node, query_module.DisjunctionNode)
        assert result_node._nodes == [node1, node2, node3, node4]

    @staticmethod
    def test_pickling():
        node1 = query_module.FilterNode("a", "=", 7)
        node2 = query_module.FilterNode("b", ">", 7.5)
        or_node = query_module.DisjunctionNode(node1, node2)

        pickled = pickle.dumps(or_node)
        unpickled = pickle.loads(pickled)
        assert or_node == unpickled

    @staticmethod
    def test___iter__():
        node1 = query_module.FilterNode("a", "=", 7)
        node2 = query_module.FilterNode("b", ">", 7.5)
        or_node = query_module.DisjunctionNode(node1, node2)

        assert list(or_node) == or_node._nodes

    @staticmethod
    def test___repr__():
        node1 = query_module.FilterNode("a", "=", 7)
        node2 = query_module.FilterNode("b", ">", 7.5)
        or_node = query_module.DisjunctionNode(node1, node2)
        expected = "OR(FilterNode('a', '=', 7), FilterNode('b', '>', 7.5))"
        assert repr(or_node) == expected

    @staticmethod
    def test___eq__():
        filter_node1 = query_module.FilterNode("a", "=", 7)
        filter_node2 = query_module.FilterNode("b", ">", 7.5)
        filter_node3 = query_module.FilterNode("c", "<", "now")

        or_node1 = query_module.DisjunctionNode(filter_node1, filter_node2)
        or_node2 = query_module.DisjunctionNode(filter_node2, filter_node1)
        or_node3 = query_module.DisjunctionNode(filter_node1, filter_node3)
        or_node4 = unittest.mock.sentinel.or_node

        assert or_node1 == or_node1
        assert not or_node1 == or_node2
        assert not or_node1 == or_node3
        assert not or_node1 == or_node4

    @staticmethod
    def test_resolve():
        node1 = query_module.FilterNode("a", "=", 7)
        node2 = query_module.FilterNode("b", ">", 77)
        or_node = query_module.DisjunctionNode(node1, node2)

        bindings = {}
        used = {}
        resolved_node = or_node.resolve(bindings, used)

        assert resolved_node is or_node
        assert bindings == {}
        assert used == {}

    @staticmethod
    def test_resolve_changed():
        node1 = unittest.mock.Mock(spec=query_module.FilterNode)
        node2 = query_module.FilterNode("b", ">", 77)
        node3 = query_module.FilterNode("c", "=", 7)
        node1.resolve.return_value = node3
        or_node = query_module.DisjunctionNode(node1, node2)

        bindings = {}
        used = {}
        resolved_node = or_node.resolve(bindings, used)

        assert isinstance(resolved_node, query_module.DisjunctionNode)
        assert resolved_node._nodes == [node3, node2]
        assert bindings == {}
        assert used == {}
        node1.resolve.assert_called_once_with(bindings, used)

    @staticmethod
    def test__to_filter():
        node1 = unittest.mock.Mock(spec=query_module.FilterNode)
        node2 = unittest.mock.Mock(spec=query_module.FilterNode)
        or_node = query_module.DisjunctionNode(node1, node2)

        assert or_node._to_filter() == [
            node1._to_filter.return_value,
            node2._to_filter.return_value,
        ]

    @staticmethod
    def test__to_filter_post():
        node1 = unittest.mock.Mock(spec=query_module.FilterNode)
        node2 = unittest.mock.Mock(spec=query_module.FilterNode)
        or_node = query_module.DisjunctionNode(node1, node2)

        with pytest.raises(NotImplementedError):
            or_node._to_filter(post=True)


def test_AND():
    assert query_module.AND is query_module.ConjunctionNode


def test_OR():
    assert query_module.OR is query_module.DisjunctionNode


class TestQuery:
    @staticmethod
    def test_constructor():
        query = query_module.Query(kind="Foo")
        assert query.kind == "Foo"
        assert query.ancestor is None
        assert query.filters is None
        assert query.order_by is None

    @staticmethod
    def test_constructor_app_and_project():
        with pytest.raises(TypeError):
            query_module.Query(app="foo", project="bar")

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_constructor_with_ancestor_parameterized_function():
        query = query_module.Query(
            ancestor=query_module.ParameterizedFunction(
                "key", query_module.Parameter(1)
            )
        )
        assert query.ancestor == query_module.ParameterizedFunction(
            "key", query_module.Parameter(1)
        )

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_constructor_with_ancestor_and_project():
        key = key_module.Key("a", "b", app="app")
        query = query_module.Query(ancestor=key, project="app")
        assert query.project == "app"

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_constructor_with_ancestor_and_namespace():
        key = key_module.Key("a", "b", namespace="space")
        query = query_module.Query(ancestor=key, namespace="space")
        assert query.namespace == "space"

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_constructor_with_ancestor_parameterized_thing():
        query = query_module.Query(ancestor=query_module.ParameterizedThing())
        assert isinstance(query.ancestor, query_module.ParameterizedThing)

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_constructor_with_projection():
        query = query_module.Query(kind="Foo", projection=["X"])
        assert query.projection == ("X",)

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    @unittest.mock.patch("google.cloud.ndb.model.Model._check_properties")
    def test_constructor_with_projection_as_property(_check_props):
        query = query_module.Query(
            kind="Foo", projection=[model.Property(name="X")]
        )
        assert query.projection == ("X",)
        _check_props.assert_not_called()

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    @unittest.mock.patch("google.cloud.ndb.model.Model._check_properties")
    def test_constructor_with_projection_as_property_modelclass(_check_props):
        class Foo(model.Model):
            x = model.IntegerProperty()

        query = query_module.Query(
            kind="Foo", projection=[model.Property(name="x")]
        )
        assert query.projection == ("x",)
        _check_props.assert_called_once_with(["x"])

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_constructor_with_distinct_on():
        query = query_module.Query(kind="Foo", distinct_on=["X"])
        assert query.distinct_on == ("X",)

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_constructor_with_group_by():
        query = query_module.Query(kind="Foo", group_by=["X"])
        assert query.distinct_on == ("X",)

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_constructor_with_distinct_on_and_group_by():
        with pytest.raises(TypeError):
            query_module.Query(distinct_on=[], group_by=[])

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_constructor_with_filters():
        query = query_module.Query(
            filters=query_module.FilterNode("f", None, None)
        )
        assert isinstance(query.filters, query_module.Node)

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_constructor_with_order_by():
        query = query_module.Query(order_by=[])
        assert query.order_by == []

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_constructor_with_orders():
        query = query_module.Query(orders=[])
        assert query.order_by == []

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_constructor_with_orders_and_order_by():
        with pytest.raises(TypeError):
            query_module.Query(orders=[], order_by=[])

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_constructor_with_default_options():
        options = query_module.QueryOptions()
        query = query_module.Query(default_options=options)
        assert query.default_options == options

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_constructor_with_bad_default_options():
        with pytest.raises(TypeError):
            query_module.Query(default_options="bad")

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_constructor_with_default_options_and_projection():
        options = query_module.QueryOptions(projection=["X"])
        with pytest.raises(TypeError):
            query_module.Query(projection=["Y"], default_options=options)

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_query_errors():
        with pytest.raises(TypeError):
            query_module.Query(
                ancestor=query_module.ParameterizedFunction(
                    "user", query_module.Parameter(1)
                )
            )
        with pytest.raises(TypeError):
            query_module.Query(ancestor=42)
        with pytest.raises(ValueError):
            query_module.Query(ancestor=model.Key("Kind", None))
        with pytest.raises(TypeError):
            query_module.Query(ancestor=model.Key("Kind", 1), app="another")
        with pytest.raises(TypeError):
            query_module.Query(ancestor=model.Key("X", 1), namespace="another")
        with pytest.raises(TypeError):
            query_module.Query(filters=42)
        with pytest.raises(TypeError):
            query_module.Query(order_by=42)
        with pytest.raises(TypeError):
            query_module.Query(projection="")
        with pytest.raises(TypeError):
            query_module.Query(projection=42)
        with pytest.raises(TypeError):
            query_module.Query(projection=[42])
        with pytest.raises(TypeError):
            query_module.Query(group_by="")
        with pytest.raises(TypeError):
            query_module.Query(group_by=42)
        with pytest.raises(TypeError):
            query_module.Query(group_by=[])

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test___repr__():
        options = query_module.QueryOptions(kind="Bar")
        query = query_module.Query(
            kind="Foo",
            ancestor=key_module.Key("a", "b", app="app", namespace="space"),
            namespace="space",
            app="app",
            group_by=["X"],
            projection=[model.Property(name="x")],
            filters=query_module.FilterNode("f", None, None),
            default_options=options,
            order_by=[],
        )
        rep = (
            "Query(project='app', namespace='space', kind='Foo', ancestor="
            "Key('a', 'b', app='app', namespace='space'), filters="
            "FilterNode('f', None, None), order_by=[], projection=['x'], "
            "distinct_on=['X'], default_options=QueryOptions(kind='Bar'))"
        )
        assert query.__repr__() == rep

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test___repr__no_params():
        query = query_module.Query()
        rep = "Query()"
        assert query.__repr__() == rep

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_bind():
        options = query_module.QueryOptions(kind="Bar")
        query = query_module.Query(
            kind="Foo",
            ancestor=key_module.Key("a", "b", app="app", namespace="space"),
            namespace="space",
            app="app",
            group_by=["X"],
            projection=[model.Property(name="x")],
            filters=query_module.FilterNode("f", None, None),
            default_options=options,
            order_by=[],
        )
        query2 = query.bind()
        assert query2.kind == "Foo"

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_bind_with_parameter_ancestor():
        options = query_module.QueryOptions(kind="Bar")
        query = query_module.Query(
            kind="Foo",
            ancestor=query_module.Parameter("xyz"),
            namespace="space",
            app="app",
            group_by=["X"],
            projection=[model.Property(name="x")],
            filters=query_module.FilterNode("f", None, None),
            default_options=options,
            order_by=[],
        )
        key = key_module.Key("a", "b", app="app", namespace="space")
        query2 = query.bind(xyz=key)
        assert query2.kind == "Foo"

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_bind_with_bound_and_unbound():
        options = query_module.QueryOptions(kind="Bar")
        query = query_module.Query(
            kind="Foo",
            ancestor=query_module.Parameter("xyz"),
            namespace="space",
            app="app",
            group_by=["X"],
            projection=[model.Property(name="x")],
            filters=query_module.FilterNode("f", None, None),
            default_options=options,
            order_by=[],
        )
        with pytest.raises(exceptions.BadArgumentError):
            query.bind(42, "xyz", xyz="1")

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_bind_error():
        query = query_module.Query()
        with pytest.raises(exceptions.BadArgumentError):
            query.bind(42)

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_is_distinct_true(context):
        query = query_module.Query(
            group_by=["X"], projection=[model.Property(name="X")]
        )
        assert query.is_distinct is True

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_is_distinct_false(context):
        query = query_module.Query(
            group_by=["X"], projection=[model.Property(name="y")]
        )
        assert query.is_distinct is False

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_filter(context):
        query = query_module.Query(
            kind="Foo", filters=query_module.FilterNode("x", "=", 1)
        )
        filters = [
            query_module.FilterNode("y", ">", 0),
            query_module.FilterNode("y", "<", 1000),
        ]
        query = query.filter(*filters)
        filters.insert(0, query_module.FilterNode("x", "=", 1))
        assert query.filters == query_module.ConjunctionNode(*filters)

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_filter_one_arg(context):
        query = query_module.Query(kind="Foo")
        filters = (query_module.FilterNode("y", ">", 0),)
        query = query.filter(*filters)
        assert query.filters == filters[0]

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_filter_no_args(context):
        query = query_module.Query(
            kind="Foo", filters=query_module.FilterNode("x", "=", 1)
        )
        filters = []
        query = query.filter(*filters)
        assert query.filters == query_module.FilterNode("x", "=", 1)

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_filter_bad_args(context):
        query = query_module.Query(
            kind="Foo", filters=query_module.FilterNode("x", "=", 1)
        )
        filters = ["f"]
        with pytest.raises(TypeError):
            query.filter(*filters)

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_analyze(context):
        query = query_module.Query(
            kind="Foo",
            filters=query_module.FilterNode("x", "=", 1),
            ancestor=query_module.Parameter("xyz"),
        )
        analysis = query.analyze()
        assert analysis == ["xyz"]

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_analyze_no_args(context):
        query = query_module.Query(kind="Foo")
        analysis = query.analyze()
        assert analysis == []

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_order(context):
        prop1 = model.Property(name="prop1")
        prop2 = model.Property(name="prop2")
        prop3 = model.Property(name="prop3")
        prop4 = model.Property(name="prop4")
        query = query_module.Query(kind="Foo", order_by=[prop1, -prop2])
        query = query.order(prop3, prop4)
        assert len(query.order_by) == 4
        assert query.order_by[0].name == "prop1"
        assert query.order_by[0].reverse is False
        assert query.order_by[1].name == "prop2"
        assert query.order_by[1].reverse is True
        assert query.order_by[2].name == "prop3"
        assert query.order_by[2].reverse is False
        assert query.order_by[3].name == "prop4"
        assert query.order_by[3].reverse is False

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_order_mixed(context):
        class Foo(model.Model):
            prop1 = model.Property(name="prop1")
            prop2 = model.Property(name="prop2")
            prop3 = model.Property(name="prop3")
            prop4 = model.Property(name="prop4")

        query = query_module.Query(kind="Foo", order_by=["prop1", -Foo.prop2])
        query = query.order("-prop3", Foo.prop4)
        assert len(query.order_by) == 4
        assert query.order_by[0].name == "prop1"
        assert query.order_by[0].reverse is False
        assert query.order_by[1].name == "prop2"
        assert query.order_by[1].reverse is True
        assert query.order_by[2].name == "prop3"
        assert query.order_by[2].reverse is True
        assert query.order_by[3].name == "prop4"
        assert query.order_by[3].reverse is False

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_order_no_initial_order(context):
        prop1 = model.Property(name="prop1")
        prop2 = model.Property(name="prop2")
        query = query_module.Query(kind="Foo")
        query = query.order(prop1, -prop2)
        assert len(query.order_by) == 2
        assert query.order_by[0].name == "prop1"
        assert query.order_by[0].reverse is False
        assert query.order_by[1].name == "prop2"
        assert query.order_by[1].reverse is True

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_order_no_args(context):
        prop1 = model.Property(name="prop1")
        prop2 = model.Property(name="prop2")
        query = query_module.Query(kind="Foo", order_by=[prop1, -prop2])
        query = query.order()
        assert len(query.order_by) == 2
        assert query.order_by[0].name == "prop1"
        assert query.order_by[0].reverse is False
        assert query.order_by[1].name == "prop2"
        assert query.order_by[1].reverse is True

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_order_bad_args(context):
        query = query_module.Query(kind="Foo")
        with pytest.raises(TypeError):
            query.order([5, 10])

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    @unittest.mock.patch("google.cloud.ndb.query._datastore_query")
    def test_fetch_async(_datastore_query):
        future = tasklets.Future("fetch")
        _datastore_query.fetch.return_value = future
        query = query_module.Query()
        assert query.fetch_async() is future

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    @unittest.mock.patch("google.cloud.ndb.query._datastore_query")
    def test_fetch_async_with_keys_only(_datastore_query):
        query = query_module.Query()
        response = _datastore_query.fetch.return_value
        assert query.fetch_async(keys_only=True) is response
        _datastore_query.fetch.assert_called_once_with(
            query_module.QueryOptions(projection=["__key__"])
        )

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    @unittest.mock.patch("google.cloud.ndb.query._datastore_query")
    def test_fetch_async_with_keys_only_as_option(_datastore_query):
        query = query_module.Query()
        options = query_module.QueryOptions(keys_only=True)
        response = _datastore_query.fetch.return_value
        assert query.fetch_async(options=options) is response
        _datastore_query.fetch.assert_called_once_with(
            query_module.QueryOptions(projection=["__key__"])
        )

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_fetch_async_with_keys_only_and_projection():
        query = query_module.Query(projection=["foo", "bar"])
        with pytest.raises(TypeError):
            query.fetch_async(keys_only=True)

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    @unittest.mock.patch("google.cloud.ndb.query._datastore_query")
    def test_fetch_async_with_projection(_datastore_query):
        query = query_module.Query()
        response = _datastore_query.fetch.return_value
        assert query.fetch_async(projection=("foo", "bar")) is response
        _datastore_query.fetch.assert_called_once_with(
            query_module.QueryOptions(projection=("foo", "bar"))
        )

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    @unittest.mock.patch("google.cloud.ndb.query._datastore_query")
    def test_fetch_async_with_projection_from_query(_datastore_query):
        query = query_module.Query(projection=("foo", "bar"))
        options = query_module.QueryOptions()
        response = _datastore_query.fetch.return_value
        assert query.fetch_async(options=options) is response
        _datastore_query.fetch.assert_called_once_with(
            query_module.QueryOptions(projection=("foo", "bar"))
        )

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_fetch_async_with_offset():
        query = query_module.Query()
        with pytest.raises(NotImplementedError):
            query.fetch_async(offset=20)

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_fetch_async_with_limit():
        query = query_module.Query()
        with pytest.raises(NotImplementedError):
            query.fetch_async(limit=20)

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_fetch_async_with_batch_size():
        query = query_module.Query()
        with pytest.raises(NotImplementedError):
            query.fetch_async(batch_size=20)

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_fetch_async_with_prefetch_size():
        query = query_module.Query()
        with pytest.raises(NotImplementedError):
            query.fetch_async(prefetch_size=20)

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_fetch_async_with_produce_cursors():
        query = query_module.Query()
        with pytest.raises(NotImplementedError):
            query.fetch_async(produce_cursors=True)

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_fetch_async_with_start_cursor():
        query = query_module.Query()
        with pytest.raises(NotImplementedError):
            query.fetch_async(start_cursor=20)

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_fetch_async_with_end_cursor():
        query = query_module.Query()
        with pytest.raises(NotImplementedError):
            query.fetch_async(end_cursor=20)

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_fetch_async_with_deadline():
        query = query_module.Query()
        with pytest.raises(NotImplementedError):
            query.fetch_async(deadline=20)

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    def test_fetch_async_with_read_policy():
        query = query_module.Query()
        with pytest.raises(NotImplementedError):
            query.fetch_async(read_policy=20)

    @staticmethod
    @pytest.mark.usefixtures("in_context")
    @unittest.mock.patch("google.cloud.ndb.query._datastore_query")
    def test_fetch(_datastore_query):
        future = tasklets.Future("fetch")
        future.set_result("foo")
        _datastore_query.fetch.return_value = future
        query = query_module.Query()
        assert query.fetch() == "foo"


def test_gql():
    with pytest.raises(NotImplementedError):
        query_module.gql()


class TestQueryIterator:
    @staticmethod
    def test_constructor():
        with pytest.raises(NotImplementedError):
            query_module.QueryIterator()
