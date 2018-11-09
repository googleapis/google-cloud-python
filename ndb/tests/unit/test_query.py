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
        with pytest.raises(exceptions.BadQueryError):
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
        with pytest.raises(exceptions.BadArgumentError):
            parameter_node._to_filter()

    @staticmethod
    def test_resolve_simple():
        prop = model.Property(name="val")
        param = query.Parameter("abc")
        parameter_node = query.ParameterNode(prop, "=", param)

        value = 67
        bindings = {"abc": value}
        used = {}
        resolved_node = parameter_node.resolve(bindings, used)

        assert resolved_node == query.FilterNode(b"val", "=", value)
        assert used == {"abc": True}

    @staticmethod
    def test_resolve_with_in():
        prop = model.Property(name="val")
        param = query.Parameter("replace")
        parameter_node = query.ParameterNode(prop, "in", param)

        value = (19, 20, 28)
        bindings = {"replace": value}
        used = {}
        resolved_node = parameter_node.resolve(bindings, used)

        assert resolved_node == query.DisjunctionNode(
            query.FilterNode(b"val", "=", 19),
            query.FilterNode(b"val", "=", 20),
            query.FilterNode(b"val", "=", 28),
        )
        assert used == {"replace": True}

    @staticmethod
    def test_resolve_in_empty_container():
        prop = model.Property(name="val")
        param = query.Parameter("replace")
        parameter_node = query.ParameterNode(prop, "in", param)

        value = ()
        bindings = {"replace": value}
        used = {}
        resolved_node = parameter_node.resolve(bindings, used)

        assert resolved_node == query.FalseNode()
        assert used == {"replace": True}


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
    def test_constructor_in():
        or_node = query.FilterNode("a", "in", ("x", "y", "z"))

        filter_node1 = query.FilterNode("a", "=", "x")
        filter_node2 = query.FilterNode("a", "=", "y")
        filter_node3 = query.FilterNode("a", "=", "z")
        assert or_node == query.DisjunctionNode(
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
    def test_constructor_ne():
        or_node = query.FilterNode("a", "!=", 2.5)

        filter_node1 = query.FilterNode("a", "<", 2.5)
        filter_node2 = query.FilterNode("a", ">", 2.5)
        assert or_node == query.DisjunctionNode(filter_node1, filter_node2)

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


class Test_BooleanClauses:
    @staticmethod
    def test_constructor_or():
        or_clauses = query._BooleanClauses("name", True)
        assert or_clauses.name == "name"
        assert or_clauses.combine_or
        assert or_clauses.or_parts == []

    @staticmethod
    def test_constructor_and():
        and_clauses = query._BooleanClauses("name", False)
        assert and_clauses.name == "name"
        assert not and_clauses.combine_or
        assert and_clauses.or_parts == [[]]

    @staticmethod
    def test_add_node_invalid():
        clauses = query._BooleanClauses("name", False)
        with pytest.raises(TypeError):
            clauses.add_node(None)

    @staticmethod
    def test_add_node_or_with_simple():
        clauses = query._BooleanClauses("name", True)
        node = query.FilterNode("a", "=", 7)
        clauses.add_node(node)
        assert clauses.or_parts == [node]

    @staticmethod
    def test_add_node_or_with_disjunction():
        clauses = query._BooleanClauses("name", True)
        node1 = query.FilterNode("a", "=", 7)
        node2 = query.FilterNode("b", ">", 7.5)
        node3 = query.DisjunctionNode(node1, node2)
        clauses.add_node(node3)
        assert clauses.or_parts == [node1, node2]

    @staticmethod
    def test_add_node_and_with_simple():
        clauses = query._BooleanClauses("name", False)
        node1 = query.FilterNode("a", "=", 7)
        node2 = query.FilterNode("b", ">", 7.5)
        node3 = query.FilterNode("c", "<", "now")
        # Modify to see the "broadcast"
        clauses.or_parts = [[node1], [node2], [node3]]

        node4 = query.FilterNode("d", ">=", 80)
        clauses.add_node(node4)
        assert clauses.or_parts == [
            [node1, node4],
            [node2, node4],
            [node3, node4],
        ]

    @staticmethod
    def test_add_node_and_with_conjunction():
        clauses = query._BooleanClauses("name", False)
        node1 = query.FilterNode("a", "=", 7)
        node2 = query.FilterNode("b", ">", 7.5)
        clauses.or_parts = [[node1], [node2]]  # Modify to see the "broadcast"

        node3 = query.FilterNode("c", "<", "now")
        node4 = query.FilterNode("d", ">=", 80)
        node5 = query.ConjunctionNode(node3, node4)
        clauses.add_node(node5)
        assert clauses.or_parts == [
            [node1, node3, node4],
            [node2, node3, node4],
        ]

    @staticmethod
    def test_add_node_and_with_disjunction():
        clauses = query._BooleanClauses("name", False)
        node1 = query.FilterNode("a", "=", 7)
        node2 = query.FilterNode("b", ">", 7.5)
        clauses.or_parts = [[node1], [node2]]  # Modify to see the "broadcast"

        node3 = query.FilterNode("c", "<", "now")
        node4 = query.FilterNode("d", ">=", 80)
        node5 = query.DisjunctionNode(node3, node4)
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
            query.ConjunctionNode()

    @staticmethod
    def test_constructor_one_node():
        node = query.FilterNode("a", "=", 7)
        result_node = query.ConjunctionNode(node)
        assert result_node is node

    @staticmethod
    def test_constructor_many_nodes():
        node1 = query.FilterNode("a", "=", 7)
        node2 = query.FilterNode("b", ">", 7.5)
        node3 = query.FilterNode("c", "<", "now")
        node4 = query.FilterNode("d", ">=", 80)

        result_node = query.ConjunctionNode(node1, node2, node3, node4)
        assert isinstance(result_node, query.ConjunctionNode)
        assert result_node._nodes == [node1, node2, node3, node4]

    @staticmethod
    def test_constructor_convert_or():
        node1 = query.FilterNode("a", "=", 7)
        node2 = query.FilterNode("b", ">", 7.5)
        node3 = query.DisjunctionNode(node1, node2)
        node4 = query.FilterNode("d", ">=", 80)

        result_node = query.ConjunctionNode(node3, node4)
        assert isinstance(result_node, query.DisjunctionNode)
        assert result_node._nodes == [
            query.ConjunctionNode(node1, node4),
            query.ConjunctionNode(node2, node4),
        ]

    @staticmethod
    @unittest.mock.patch("google.cloud.ndb.query._BooleanClauses")
    def test_constructor_unreachable(boolean_clauses):
        clauses = unittest.mock.Mock(
            or_parts=[], spec=("add_node", "or_parts")
        )
        boolean_clauses.return_value = clauses

        node1 = query.FilterNode("a", "=", 7)
        node2 = query.FilterNode("b", ">", 7.5)

        with pytest.raises(RuntimeError):
            query.ConjunctionNode(node1, node2)

        boolean_clauses.assert_called_once_with(
            "ConjunctionNode", combine_or=False
        )
        assert clauses.add_node.call_count == 2
        clauses.add_node.assert_has_calls(
            [unittest.mock.call(node1), unittest.mock.call(node2)]
        )

    @staticmethod
    def test_pickling():
        node1 = query.FilterNode("a", "=", 7)
        node2 = query.FilterNode("b", ">", 7.5)
        and_node = query.ConjunctionNode(node1, node2)

        pickled = pickle.dumps(and_node)
        unpickled = pickle.loads(pickled)
        assert and_node == unpickled

    @staticmethod
    def test___iter__():
        node1 = query.FilterNode("a", "=", 7)
        node2 = query.FilterNode("b", ">", 7.5)
        and_node = query.ConjunctionNode(node1, node2)

        assert list(and_node) == and_node._nodes

    @staticmethod
    def test___repr__():
        node1 = query.FilterNode("a", "=", 7)
        node2 = query.FilterNode("b", ">", 7.5)
        and_node = query.ConjunctionNode(node1, node2)
        expected = "AND(FilterNode('a', '=', 7), FilterNode('b', '>', 7.5))"
        assert repr(and_node) == expected

    @staticmethod
    def test___eq__():
        filter_node1 = query.FilterNode("a", "=", 7)
        filter_node2 = query.FilterNode("b", ">", 7.5)
        filter_node3 = query.FilterNode("c", "<", "now")

        and_node1 = query.ConjunctionNode(filter_node1, filter_node2)
        and_node2 = query.ConjunctionNode(filter_node2, filter_node1)
        and_node3 = query.ConjunctionNode(filter_node1, filter_node3)
        and_node4 = unittest.mock.sentinel.and_node

        assert and_node1 == and_node1
        assert not and_node1 == and_node2
        assert not and_node1 == and_node3
        assert not and_node1 == and_node4

    @staticmethod
    def test__to_filter_empty():
        node1 = query.FilterNode("a", "=", 7)
        node2 = query.FilterNode("b", "<", 6)
        and_node = query.ConjunctionNode(node1, node2)

        as_filter = and_node._to_filter(post=True)
        assert as_filter is None

    @staticmethod
    def test__to_filter_single():
        node1 = unittest.mock.Mock(spec=query.FilterNode)
        node2 = query.PostFilterNode("predicate")
        node3 = unittest.mock.Mock(spec=query.FilterNode)
        node3._to_filter.return_value = False
        and_node = query.ConjunctionNode(node1, node2, node3)

        as_filter = and_node._to_filter()
        assert as_filter is node1._to_filter.return_value

        node1._to_filter.assert_called_once_with(post=False)

    @staticmethod
    def test__to_filter_multiple():
        node1 = query.PostFilterNode("predicate1")
        node2 = query.PostFilterNode("predicate2")
        and_node = query.ConjunctionNode(node1, node2)

        with pytest.raises(NotImplementedError):
            and_node._to_filter(post=True)

    @staticmethod
    def test__post_filters_empty():
        node1 = query.FilterNode("a", "=", 7)
        node2 = query.FilterNode("b", ">", 77)
        and_node = query.ConjunctionNode(node1, node2)

        post_filters_node = and_node._post_filters()
        assert post_filters_node is None

    @staticmethod
    def test__post_filters_single():
        node1 = query.FilterNode("a", "=", 7)
        node2 = query.PostFilterNode("predicate2")
        and_node = query.ConjunctionNode(node1, node2)

        post_filters_node = and_node._post_filters()
        assert post_filters_node is node2

    @staticmethod
    def test__post_filters_multiple():
        node1 = query.FilterNode("a", "=", 7)
        node2 = query.PostFilterNode("predicate2")
        node3 = query.PostFilterNode("predicate3")
        and_node = query.ConjunctionNode(node1, node2, node3)

        post_filters_node = and_node._post_filters()
        assert post_filters_node == query.ConjunctionNode(node2, node3)

    @staticmethod
    def test__post_filters_same():
        node1 = query.PostFilterNode("predicate1")
        node2 = query.PostFilterNode("predicate2")
        and_node = query.ConjunctionNode(node1, node2)

        post_filters_node = and_node._post_filters()
        assert post_filters_node is and_node

    @staticmethod
    def test_resolve():
        node1 = query.FilterNode("a", "=", 7)
        node2 = query.FilterNode("b", ">", 77)
        and_node = query.ConjunctionNode(node1, node2)

        bindings = {}
        used = {}
        resolved_node = and_node.resolve(bindings, used)

        assert resolved_node is and_node
        assert bindings == {}
        assert used == {}

    @staticmethod
    def test_resolve_changed():
        node1 = unittest.mock.Mock(spec=query.FilterNode)
        node2 = query.FilterNode("b", ">", 77)
        node3 = query.FilterNode("c", "=", 7)
        node1.resolve.return_value = node3
        and_node = query.ConjunctionNode(node1, node2)

        bindings = {}
        used = {}
        resolved_node = and_node.resolve(bindings, used)

        assert isinstance(resolved_node, query.ConjunctionNode)
        assert resolved_node._nodes == [node3, node2]
        assert bindings == {}
        assert used == {}
        node1.resolve.assert_called_once_with(bindings, used)


class TestDisjunctionNode:
    @staticmethod
    def test_constructor_no_nodes():
        with pytest.raises(TypeError):
            query.DisjunctionNode()

    @staticmethod
    def test_constructor_one_node():
        node = query.FilterNode("a", "=", 7)
        result_node = query.DisjunctionNode(node)
        assert result_node is node

    @staticmethod
    def test_constructor_many_nodes():
        node1 = query.FilterNode("a", "=", 7)
        node2 = query.FilterNode("b", ">", 7.5)
        node3 = query.FilterNode("c", "<", "now")
        node4 = query.FilterNode("d", ">=", 80)

        result_node = query.DisjunctionNode(node1, node2, node3, node4)
        assert isinstance(result_node, query.DisjunctionNode)
        assert result_node._nodes == [node1, node2, node3, node4]

    @staticmethod
    def test_pickling():
        node1 = query.FilterNode("a", "=", 7)
        node2 = query.FilterNode("b", ">", 7.5)
        or_node = query.DisjunctionNode(node1, node2)

        pickled = pickle.dumps(or_node)
        unpickled = pickle.loads(pickled)
        assert or_node == unpickled

    @staticmethod
    def test___iter__():
        node1 = query.FilterNode("a", "=", 7)
        node2 = query.FilterNode("b", ">", 7.5)
        or_node = query.DisjunctionNode(node1, node2)

        assert list(or_node) == or_node._nodes

    @staticmethod
    def test___repr__():
        node1 = query.FilterNode("a", "=", 7)
        node2 = query.FilterNode("b", ">", 7.5)
        or_node = query.DisjunctionNode(node1, node2)
        expected = "OR(FilterNode('a', '=', 7), FilterNode('b', '>', 7.5))"
        assert repr(or_node) == expected

    @staticmethod
    def test___eq__():
        filter_node1 = query.FilterNode("a", "=", 7)
        filter_node2 = query.FilterNode("b", ">", 7.5)
        filter_node3 = query.FilterNode("c", "<", "now")

        or_node1 = query.DisjunctionNode(filter_node1, filter_node2)
        or_node2 = query.DisjunctionNode(filter_node2, filter_node1)
        or_node3 = query.DisjunctionNode(filter_node1, filter_node3)
        or_node4 = unittest.mock.sentinel.or_node

        assert or_node1 == or_node1
        assert not or_node1 == or_node2
        assert not or_node1 == or_node3
        assert not or_node1 == or_node4

    @staticmethod
    def test_resolve():
        node1 = query.FilterNode("a", "=", 7)
        node2 = query.FilterNode("b", ">", 77)
        or_node = query.DisjunctionNode(node1, node2)

        bindings = {}
        used = {}
        resolved_node = or_node.resolve(bindings, used)

        assert resolved_node is or_node
        assert bindings == {}
        assert used == {}

    @staticmethod
    def test_resolve_changed():
        node1 = unittest.mock.Mock(spec=query.FilterNode)
        node2 = query.FilterNode("b", ">", 77)
        node3 = query.FilterNode("c", "=", 7)
        node1.resolve.return_value = node3
        or_node = query.DisjunctionNode(node1, node2)

        bindings = {}
        used = {}
        resolved_node = or_node.resolve(bindings, used)

        assert isinstance(resolved_node, query.DisjunctionNode)
        assert resolved_node._nodes == [node3, node2]
        assert bindings == {}
        assert used == {}
        node1.resolve.assert_called_once_with(bindings, used)


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
