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

"""High-level wrapper for datastore queries."""

from google.cloud.ndb import exceptions
from google.cloud.ndb import model


__all__ = [
    "Cursor",
    "QueryOptions",
    "RepeatedStructuredPropertyPredicate",
    "ParameterizedThing",
    "Parameter",
    "ParameterizedFunction",
    "Node",
    "FalseNode",
    "ParameterNode",
    "FilterNode",
    "PostFilterNode",
    "ConjunctionNode",
    "DisjunctionNode",
    "AND",
    "OR",
    "Query",
    "gql",
    "QueryIterator",
]


Cursor = NotImplemented  # From `google.appengine.datastore.datastore_query`
_IN_OP = "in"
_OPS = frozenset(["=", "!=", "<", "<=", ">", ">=", _IN_OP])


class QueryOptions:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class RepeatedStructuredPropertyPredicate:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class ParameterizedThing:
    """Base class for :class:`Parameter` and :class:`ParameterizedFunction`.

    This exists purely for :func:`isinstance` checks.
    """

    def __eq__(self, other):
        raise NotImplementedError

    def __ne__(self, other):
        return not self == other


class Parameter(ParameterizedThing):
    """Represents a bound variable in a GQL query.

    ``Parameter(1)`` corresponds to a slot labeled ``:1`` in a GQL query.
    ``Parameter('xyz')`` corresponds to a slot labeled ``:xyz``.

    The value must be set (bound) separately.

    Args:
        key (Union[str, int]): The parameter key.

    Raises:
        TypeError: If the ``key`` is not a string or integer.
    """

    def __init__(self, key):
        if not isinstance(key, (int, str, bytes)):
            raise TypeError(
                "Parameter key must be an integer or string, not {}".format(
                    key
                )
            )
        self._key = key

    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, self._key)

    def __eq__(self, other):
        if not isinstance(other, Parameter):
            return NotImplemented

        return self._key == other._key

    @property
    def key(self):
        """Retrieve the key."""
        return self._key

    def resolve(self, bindings, used):
        """Resolve the current parameter from the parameter bindings.

        Args:
            bindings (dict): A mapping of parameter bindings.
            used (Dict[Union[str, int], bool]): A mapping of already used
                parameters. This will be modified if the current parameter
                is in ``bindings``.

        Returns:
            Any: The bound value for the current parameter.

        Raises:
            .BadArgumentError: If the current parameter is not in ``bindings``.
        """
        key = self._key
        if key not in bindings:
            raise exceptions.BadArgumentError(
                "Parameter :{} is not bound.".format(key)
            )
        value = bindings[key]
        used[key] = True
        return value


class ParameterizedFunction(ParameterizedThing):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class Node:
    """Base class for filter expression tree nodes.

    Tree nodes are considered immutable, even though they can contain
    Parameter instances, which are not.  In particular, two identical
    trees may be represented by the same Node object in different
    contexts.

    Raises:
        TypeError: Always, only subclasses are allowed.
    """

    def __new__(cls):
        if cls is Node:
            raise TypeError("Cannot instantiate Node, only a subclass.")
        return super(Node, cls).__new__(cls)

    def __eq__(self, other):
        raise NotImplementedError

    def __ne__(self, other):
        return not self == other

    def __le__(self, unused_other):
        raise TypeError("Nodes cannot be ordered")

    def __lt__(self, unused_other):
        raise TypeError("Nodes cannot be ordered")

    def __ge__(self, unused_other):
        raise TypeError("Nodes cannot be ordered")

    def __gt__(self, unused_other):
        raise TypeError("Nodes cannot be ordered")

    def _to_filter(self, post=False):
        """Helper to convert to low-level filter, or :data:`None`.

        Raises:
            NotImplementedError: Always. This method is virtual.
        """
        raise NotImplementedError

    def _post_filters(self):
        """Helper to extract post-filter nodes, if any.

        Returns:
            None: Always. Because this is the base implementation.
        """
        return None

    def resolve(self, bindings, used):
        """Return a node with parameters replaced by the selected values.

        .. note::

            Both ``bindings`` and ``used`` are unused by this base class
            implementation.

        Args:
            bindings (dict): A mapping of parameter bindings.
            used (Dict[Union[str, int], bool]): A mapping of already used
                parameters. This will be modified if the current parameter
                is in ``bindings``.

        Returns:
            Node: The current node.
        """
        return self


class FalseNode(Node):
    """Tree node for an always-failing filter."""

    def __eq__(self, other):
        """Equality check.

        An instance will always equal another :class:`FalseNode` instance. This
        is because they hold no state.
        """
        if not isinstance(other, FalseNode):
            return NotImplemented
        return True

    def _to_filter(self, post=False):
        """(Attempt to) convert to a low-level filter instance.

        Args:
            post (bool): Indicates if this is a post-filter node.

        Raises:
            .BadQueryError: If ``post`` is :data:`False`, because there's no
                point submitting a query that will never return anything.
        """
        if post:
            return None
        raise _exceptions.BadQueryError(
            "Cannot convert FalseNode to predicate"
        )


class ParameterNode(Node):
    """Tree node for a parameterized filter.

    Args:
        prop (.Property): A property describing a value type.
        op (str): The comparison operator. One of ``=``, ``!=``, ``<``, ``<=``,
            ``>``, ``>=`` or ``in``.
        param (ParameterizedThing): The parameter corresponding to the node.

    Raises:
        TypeError: If ``prop`` is not a :class:`.Property`.
        TypeError: If ``op`` is not one of the accepted operators.
        TypeError: If ``param`` is not a :class:`.Parameter` or
            :class:`.ParameterizedFunction`.
    """

    def __new__(cls, prop, op, param):
        if not isinstance(prop, model.Property):
            raise TypeError("Expected a Property, got {!r}".format(prop))
        if op not in _OPS:
            raise TypeError("Expected a valid operator, got {!r}".format(op))
        if not isinstance(param, ParameterizedThing):
            raise TypeError(
                "Expected a ParameterizedThing, got {!r}".format(param)
            )
        obj = super(ParameterNode, cls).__new__(cls)
        obj._prop = prop
        obj._op = op
        obj._param = param
        return obj

    def __getnewargs__(self):
        """Private API used to specify ``__new__`` arguments when unpickling.

        .. note::

            This method only applies if the ``pickle`` protocol is 2 or
            greater.

        Returns:
            Tuple[.Property, str, .ParameterizedThing]: A tuple containing the
            internal state: the property, operation and parameter.
        """
        return self._prop, self._op, self._param

    def __repr__(self):
        return "ParameterNode({!r}, {!r}, {!r})".format(
            self._prop, self._op, self._param
        )

    def __eq__(self, other):
        if not isinstance(other, ParameterNode):
            return NotImplemented
        return (
            self._prop._name == other._prop._name
            and self._op == other._op
            and self._param == other._param
        )

    def _to_filter(self, post=False):
        """Helper to convert to low-level filter, or :data:`None`.

        Args:
            post (bool): Indicates if this is a post-filter node.

        Raises:
            .BadArgumentError: Always. This is because this node represents
            a parameter, i.e. no value exists to be filtered on.
        """
        raise _exceptions.BadArgumentError(
            "Parameter :{} is not bound.".format(self._param.key)
        )

    def resolve(self, bindings, used):
        """Return a node with parameters replaced by the selected values.

        Args:
            bindings (dict): A mapping of parameter bindings.
            used (Dict[Union[str, int], bool]): A mapping of already used
                parameters.

        Raises:
            NotImplementedError: Always. This is because the implementation
                will rely on as-yet-unimplemented features in
                :class:`Property`.
        """
        raise NotImplementedError(
            "Some features of Property need to be implemented first"
        )


class FilterNode(Node):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class PostFilterNode(Node):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class ConjunctionNode(Node):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class DisjunctionNode(Node):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


# AND and OR are preferred aliases for these.
AND = ConjunctionNode
OR = DisjunctionNode


class Query:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


def gql(*args, **kwargs):
    raise NotImplementedError


class QueryIterator:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError
