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

import functools
import inspect
import logging

from google.cloud.ndb import context as context_module
from google.cloud.ndb import _datastore_api
from google.cloud.ndb import _datastore_query
from google.cloud.ndb import _gql
from google.cloud.ndb import exceptions
from google.cloud.ndb import model
from google.cloud.ndb import _options


__all__ = [
    "QueryOptions",
    "PropertyOrder",
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
]


_EQ_OP = "="
_NE_OP = "!="
_IN_OP = "in"
_LT_OP = "<"
_GT_OP = ">"
_OPS = frozenset([_EQ_OP, _NE_OP, _LT_OP, "<=", _GT_OP, ">=", _IN_OP])

_log = logging.getLogger(__name__)


class PropertyOrder(object):
    """The sort order for a property name, to be used when ordering the
       results of a query.

       Args:
           name (str): The name of the model property to use for ordering.
           reverse (bool): Whether to reverse the sort order (descending)
               or not (ascending). Default is False.
    """

    __slots__ = ["name", "reverse"]

    def __init__(self, name, reverse=False):
        self.name = name
        self.reverse = reverse

    def __repr__(self):
        return "PropertyOrder(name='{}', reverse={})".format(
            self.name, self.reverse
        )

    def __neg__(self):
        reverse = not self.reverse
        return self.__class__(name=self.name, reverse=reverse)


class RepeatedStructuredPropertyPredicate:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class ParameterizedThing:
    """Base class for :class:`Parameter` and :class:`ParameterizedFunction`.

    This exists purely for :func:`isinstance` checks.
    """

    def __eq__(self, other):
        raise NotImplementedError

    def __ne__(self, other):
        eq = self.__eq__(other)
        if eq is not NotImplemented:
            eq = not eq
        return eq


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

    __slots__ = ("_key",)

    def __init__(self, key):
        if not isinstance(key, (int, str)):
            raise TypeError(
                "Parameter key must be an integer or string, not {}".format(
                    key
                )
            )
        self._key = key

    def __repr__(self):
        return "{}({!r})".format(type(self).__name__, self._key)

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
    """Represents a GQL function with parameterized arguments.

    For example, ParameterizedFunction('key', [Parameter(1)]) stands for
    the GQL syntax KEY(:1).
    """

    def __init__(self, func, values):
        self.__func = func
        self.__values = values

    def __repr__(self):
        return "ParameterizedFunction(%r, %r)" % (self.__func, self.__values)

    def __eq__(self, other):
        if not isinstance(other, ParameterizedFunction):
            return NotImplemented
        return self.__func == other.__func and self.__values == other.__values

    @property
    def func(self):
        return self.__func

    @property
    def values(self):
        return self.__values


class Node:
    """Base class for filter expression tree nodes.

    Tree nodes are considered immutable, even though they can contain
    Parameter instances, which are not. In particular, two identical
    trees may be represented by the same Node object in different
    contexts.

    Raises:
        TypeError: Always, only subclasses are allowed.
    """

    _multiquery = False

    __slots__ = ()

    def __new__(cls):
        if cls is Node:
            raise TypeError("Cannot instantiate Node, only a subclass.")
        return super(Node, cls).__new__(cls)

    def __eq__(self, other):
        raise NotImplementedError

    def __le__(self, unused_other):
        raise TypeError("Nodes cannot be ordered")

    def __lt__(self, unused_other):
        raise TypeError("Nodes cannot be ordered")

    def __ge__(self, unused_other):
        raise TypeError("Nodes cannot be ordered")

    def __gt__(self, unused_other):
        raise TypeError("Nodes cannot be ordered")

    def _to_filter(self, post=False):
        """Helper to convert to low-level filter.

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

    __slots__ = ()

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
        raise exceptions.BadQueryError("Cannot convert FalseNode to predicate")


class ParameterNode(Node):
    """Tree node for a parameterized filter.

    Args:
        prop (~google.cloud.ndb.model.Property): A property describing a value
            type.
        op (str): The comparison operator. One of ``=``, ``!=``, ``<``, ``<=``,
            ``>``, ``>=`` or ``in``.
        param (ParameterizedThing): The parameter corresponding to the node.

    Raises:
        TypeError: If ``prop`` is not a
            :class:`~google.cloud.ndb.model.Property`.
        TypeError: If ``op`` is not one of the accepted operators.
        TypeError: If ``param`` is not a :class:`.Parameter` or
            :class:`.ParameterizedFunction`.
    """

    __slots__ = ("_prop", "_op", "_param")

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
            Tuple[~google.cloud.ndb.model.Property, str, ParameterizedThing]:
            A tuple containing the internal state: the property, operation and
            parameter.
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
        """Helper to convert to low-level filter.

        Args:
            post (bool): Indicates if this is a post-filter node.

        Raises:
            .BadArgumentError: Always. This is because this node represents
            a parameter, i.e. no value exists to be filtered on.
        """
        raise exceptions.BadArgumentError(
            "Parameter :{} is not bound.".format(self._param.key)
        )

    def resolve(self, bindings, used):
        """Return a node with parameters replaced by the selected values.

        Args:
            bindings (dict): A mapping of parameter bindings.
            used (Dict[Union[str, int], bool]): A mapping of already used
                parameters.

        Returns:
            Union[~google.cloud.ndb.query.DisjunctionNode, \
                ~google.cloud.ndb.query.FilterNode, \
                ~google.cloud.ndb.query.FalseNode]: A node corresponding to
            the value substituted.
        """
        value = self._param.resolve(bindings, used)
        if self._op == _IN_OP:
            return self._prop._IN(value)
        else:
            return self._prop._comparison(self._op, value)


class FilterNode(Node):
    """Tree node for a single filter expression.

    For example ``FilterNode("a", ">", 3)`` filters for entities where the
    value ``a`` is greater than ``3``.

    .. warning::

        The constructor for this type may not always return a
        :class:`FilterNode`. For example:

        * The filter ``name != value`` is converted into
          ``(name > value) OR (name < value)`` (a :class:`DisjunctionNode`)
        * The filter ``name in (value1, ..., valueN)`` is converted into
          ``(name = value1) OR ... OR (name = valueN)`` (also a
          :class:`DisjunctionNode`)
        * The filter ``name in ()`` (i.e. a property is among an empty list
          of values) is converted into a :class:`FalseNode`
        * The filter ``name in (value1,)`` (i.e. a list with one element) is
          converted into ``name = value1``, a related :class:`FilterNode`
          with a different ``opsymbol`` and ``value`` than what was passed
          to the constructor

    Args:
        name (str): The name of the property being filtered.
        opsymbol (str): The comparison operator. One of ``=``, ``!=``, ``<``,
            ``<=``, ``>``, ``>=`` or ``in``.
        value (Any): The value to filter on / relative to.

    Raises:
        TypeError: If ``opsymbol`` is ``"in"`` but ``value`` is not a
            basic container (:class:`list`, :class:`tuple`, :class:`set` or
            :class:`frozenset`)
    """

    __slots__ = ("_name", "_opsymbol", "_value")

    def __new__(cls, name, opsymbol, value):
        if isinstance(value, model.Key):
            value = value._key

        if opsymbol == _NE_OP:
            node1 = FilterNode(name, _LT_OP, value)
            node2 = FilterNode(name, _GT_OP, value)
            return DisjunctionNode(node1, node2)

        if opsymbol == _IN_OP:
            if not isinstance(value, (list, tuple, set, frozenset)):
                raise TypeError(
                    "in expected a list, tuple or set of values; "
                    "received {!r}".format(value)
                )
            nodes = [
                FilterNode(name, _EQ_OP, sub_value) for sub_value in value
            ]
            if not nodes:
                return FalseNode()
            if len(nodes) == 1:
                return nodes[0]
            return DisjunctionNode(*nodes)

        instance = super(FilterNode, cls).__new__(cls)
        instance._name = name
        instance._opsymbol = opsymbol
        instance._value = value
        return instance

    def __getnewargs__(self):
        """Private API used to specify ``__new__`` arguments when unpickling.

        .. note::

            This method only applies if the ``pickle`` protocol is 2 or
            greater.

        Returns:
            Tuple[str, str, Any]: A tuple containing the
            internal state: the name, ``opsymbol`` and value.
        """
        return self._name, self._opsymbol, self._value

    def __repr__(self):
        return "{}({!r}, {!r}, {!r})".format(
            type(self).__name__, self._name, self._opsymbol, self._value
        )

    def __eq__(self, other):
        if not isinstance(other, FilterNode):
            return NotImplemented

        return (
            self._name == other._name
            and self._opsymbol == other._opsymbol
            and self._value == other._value
        )

    def _to_filter(self, post=False):
        """Helper to convert to low-level filter.

        Args:
            post (bool): Indicates if this is a post-filter node.

        Returns:
            Optional[query_pb2.PropertyFilter]: Returns :data:`None`, if
                this is a post-filter, otherwise returns the protocol buffer
                representation of the filter.

        Raises:
            NotImplementedError: If the ``opsymbol`` is ``!=`` or ``in``, since
                they should correspond to a composite filter. This should
                never occur since the constructor will create ``OR`` nodes for
                ``!=`` and ``in``
        """
        if post:
            return None
        if self._opsymbol in (_NE_OP, _IN_OP):
            raise NotImplementedError(
                "Inequality filters are not single filter "
                "expressions and therefore cannot be converted "
                "to a single filter ({!r})".format(self._opsymbol)
            )

        return _datastore_query.make_filter(
            self._name, self._opsymbol, self._value
        )


class PostFilterNode(Node):
    """Tree node representing an in-memory filtering operation.

    This is used to represent filters that cannot be executed by the
    datastore, for example a query for a structured value.

    Args:
        predicate (Callable[[Any], bool]): A filter predicate that
            takes a datastore entity (typically as a protobuf) and
            returns :data:`True` or :data:`False` if the entity matches
            the given filter.
    """

    __slots__ = ("predicate",)

    def __new__(cls, predicate):
        instance = super(PostFilterNode, cls).__new__(cls)
        instance.predicate = predicate
        return instance

    def __getnewargs__(self):
        """Private API used to specify ``__new__`` arguments when unpickling.

        .. note::

            This method only applies if the ``pickle`` protocol is 2 or
            greater.

        Returns:
            Tuple[Callable[[Any], bool],]: A tuple containing a single value,
            the ``predicate`` attached to this node.
        """
        return (self.predicate,)

    def __repr__(self):
        return "{}({})".format(type(self).__name__, self.predicate)

    def __eq__(self, other):
        if not isinstance(other, PostFilterNode):
            return NotImplemented
        return self is other or self.predicate == other.predicate

    def _to_filter(self, post=False):
        """Helper to convert to low-level filter.

        Args:
            post (bool): Indicates if this is a post-filter node.

        Returns:
            Tuple[Callable[[Any], bool], None]: If this is a post-filter, this
            returns the stored ``predicate``, otherwise it returns
            :data:`None`.
        """
        if post:
            return self.predicate
        else:
            return None


class _BooleanClauses:
    """This type will be used for symbolically performing boolean operations.

    Internally, the state will track a symbolic expression like::

        A or (B and C) or (A and D)

    as a list of the ``OR`` components::

        [A, B and C, A and D]

    When ``combine_or=False``, it will track ``AND`` statements as a list,
    making the final simplified form of our example::

        [[A], [B, C], [A, D]]

    Via :meth:`add_node`, we will ensure that new nodes will be correctly
    combined (via ``AND`` or ``OR``) with the current expression.

    Args:
        name (str): The name of the class that is tracking a
            boolean expression.
        combine_or (bool): Indicates if new nodes will be combined
            with the current boolean expression via ``AND`` or ``OR``.
    """

    __slots__ = ("name", "combine_or", "or_parts")

    def __init__(self, name, combine_or):
        self.name = name
        self.combine_or = combine_or
        if combine_or:
            # For ``OR()`` the parts are just nodes.
            self.or_parts = []
        else:
            # For ``AND()`` the parts are "segments", i.e. node lists.
            self.or_parts = [[]]

    def add_node(self, node):
        """Update the current boolean expression.

        This uses the distributive law for sets to combine as follows:

        - ``(A or B or C or ...) or  D`` -> ``A or B or C or ... or D``
        - ``(A or B or C or ...) and D`` ->
          ``(A and D) or (B and D) or (C and D) or ...``

        Args:
            node (Node): A node to add to the list of clauses.

        Raises:
            TypeError: If ``node`` is not a :class:`.Node`.
        """
        if not isinstance(node, Node):
            raise TypeError(
                "{}() expects Node instances as arguments; "
                "received a non-Node instance {!r}".format(self.name, node)
            )

        if self.combine_or:
            if isinstance(node, DisjunctionNode):
                #    [S1 or ... or Sn] or [A1 or ... or Am]
                # -> S1 or ... Sn or A1 or ... or Am
                self.or_parts.extend(node._nodes)
            else:
                #    [S1 or ... or Sn] or [A1]
                # -> S1 or ... or Sn or A1
                self.or_parts.append(node)
        else:
            if isinstance(node, DisjunctionNode):
                #    [S1 or ... or Sn] and [A1 or ... or Am]
                # -> [S1 and A1] or ... or [Sn and A1] or
                #        ... or [Sn and Am] or ... or [Sn and Am]
                new_segments = []
                for segment in self.or_parts:
                    # ``segment`` represents ``Si``
                    for sub_node in node:
                        # ``sub_node`` represents ``Aj``
                        new_segment = segment + [sub_node]
                        new_segments.append(new_segment)
                # Replace wholesale.
                self.or_parts[:] = new_segments
            elif isinstance(node, ConjunctionNode):
                #    [S1 or ... or Sn] and [A1 and ... and Am]
                # -> [S1 and A1 and ... and Am] or ... or
                #        [Sn and A1 and ... and Am]
                for segment in self.or_parts:
                    # ``segment`` represents ``Si``
                    segment.extend(node._nodes)
            else:
                #    [S1 or ... or Sn] and [A1]
                # -> [S1 and A1] or ... or [Sn and A1]
                for segment in self.or_parts:
                    segment.append(node)


class ConjunctionNode(Node):
    """Tree node representing a boolean ``AND`` operator on multiple nodes.

    .. warning::

        The constructor for this type may not always return a
        :class:`ConjunctionNode`. For example:

        * If the passed in ``nodes`` has only one entry, that single node
          will be returned by the constructor
        * If the resulting boolean expression has an ``OR`` in it, then a
          :class:`DisjunctionNode` will be returned; e.g.
          ``AND(OR(A, B), C)`` becomes ``OR(AND(A, C), AND(B, C))``

    Args:
        nodes (Tuple[Node, ...]): A list of nodes to be joined.

    Raises:
        TypeError: If ``nodes`` is empty.
        RuntimeError: If the ``nodes`` combine to an "empty" boolean
            expression.
    """

    __slots__ = ("_nodes",)

    def __new__(cls, *nodes):
        if not nodes:
            raise TypeError("ConjunctionNode() requires at least one node.")
        elif len(nodes) == 1:
            return nodes[0]

        clauses = _BooleanClauses("ConjunctionNode", combine_or=False)
        for node in nodes:
            clauses.add_node(node)

        if not clauses.or_parts:
            # NOTE: The original implementation returned a ``FalseNode``
            #       here but as far as I can tell this code is unreachable.
            raise RuntimeError("Invalid boolean expression")

        if len(clauses.or_parts) > 1:
            return DisjunctionNode(
                *[ConjunctionNode(*segment) for segment in clauses.or_parts]
            )

        instance = super(ConjunctionNode, cls).__new__(cls)
        instance._nodes = clauses.or_parts[0]
        return instance

    def __getnewargs__(self):
        """Private API used to specify ``__new__`` arguments when unpickling.

        .. note::

            This method only applies if the ``pickle`` protocol is 2 or
            greater.

        Returns:
            Tuple[Node, ...]: The list of stored nodes, converted to a
            :class:`tuple`.
        """
        return tuple(self._nodes)

    def __iter__(self):
        return iter(self._nodes)

    def __repr__(self):
        all_nodes = ", ".join(map(str, self._nodes))
        return "AND({})".format(all_nodes)

    def __eq__(self, other):
        if not isinstance(other, ConjunctionNode):
            return NotImplemented

        return self._nodes == other._nodes

    def _to_filter(self, post=False):
        """Helper to convert to low-level filter.

        Args:
            post (bool): Indicates if this is a post-filter node.

        Returns:
            Optional[Node]: The single or composite filter corresponding to
                the pre- or post-filter nodes stored. May return :data:`None`.
        """
        filters = []
        for node in self._nodes:
            if isinstance(node, PostFilterNode) == post:
                as_filter = node._to_filter(post=post)
                if as_filter:
                    filters.append(as_filter)

        if not filters:
            return None
        if len(filters) == 1:
            return filters[0]

        return _datastore_query.make_composite_and_filter(filters)

    def _post_filters(self):
        """Helper to extract post-filter nodes, if any.

        Filters all of the stored nodes that are :class:`PostFilterNode`.

        Returns:
            Optional[Node]: One of the following:

            * :data:`None` if there are no post-filter nodes in this ``AND()``
              clause
            * The single node if there is exactly one post-filter node, e.g.
              if the only node in ``AND(A, B, ...)`` that is a post-filter
              node is ``B``
            * The current node if every stored node a post-filter node, e.g.
              if all nodes ``A, B, ...`` in ``AND(A, B, ...)`` are
              post-filter nodes
            * A **new** :class:`ConjunctionNode` containing the post-filter
              nodes, e.g. if only ``A, C`` are post-filter nodes in
              ``AND(A, B, C)``, then the returned node is ``AND(A, C)``
        """
        post_filters = [
            node for node in self._nodes if isinstance(node, PostFilterNode)
        ]
        if not post_filters:
            return None
        if len(post_filters) == 1:
            return post_filters[0]
        if post_filters == self._nodes:
            return self
        return ConjunctionNode(*post_filters)

    def resolve(self, bindings, used):
        """Return a node with parameters replaced by the selected values.

        Args:
            bindings (dict): A mapping of parameter bindings.
            used (Dict[Union[str, int], bool]): A mapping of already used
                parameters. This will be modified for each parameter found
                in ``bindings``.

        Returns:
            Node: The current node, if all nodes are already resolved.
            Otherwise returns a modifed :class:`ConjunctionNode` with
            each individual node resolved.
        """
        resolved_nodes = [node.resolve(bindings, used) for node in self._nodes]
        if resolved_nodes == self._nodes:
            return self

        return ConjunctionNode(*resolved_nodes)


class DisjunctionNode(Node):
    """Tree node representing a boolean ``OR`` operator on multiple nodes.

    .. warning::

        This constructor may not always return a :class:`DisjunctionNode`.
        If the passed in ``nodes`` has only one entry, that single node
        will be returned by the constructor.

    Args:
        nodes (Tuple[Node, ...]): A list of nodes to be joined.

    Raises:
        TypeError: If ``nodes`` is empty.
    """

    _multiquery = True
    __slots__ = ("_nodes",)

    def __new__(cls, *nodes):
        if not nodes:
            raise TypeError("DisjunctionNode() requires at least one node")
        elif len(nodes) == 1:
            return nodes[0]

        instance = super(DisjunctionNode, cls).__new__(cls)
        instance._nodes = []

        clauses = _BooleanClauses("DisjunctionNode", combine_or=True)
        for node in nodes:
            clauses.add_node(node)

        instance._nodes[:] = clauses.or_parts
        return instance

    def __getnewargs__(self):
        """Private API used to specify ``__new__`` arguments when unpickling.

        .. note::

            This method only applies if the ``pickle`` protocol is 2 or
            greater.

        Returns:
            Tuple[Node, ...]: The list of stored nodes, converted to a
            :class:`tuple`.
        """
        return tuple(self._nodes)

    def __iter__(self):
        return iter(self._nodes)

    def __repr__(self):
        all_nodes = ", ".join(map(str, self._nodes))
        return "OR({})".format(all_nodes)

    def __eq__(self, other):
        if not isinstance(other, DisjunctionNode):
            return NotImplemented

        return self._nodes == other._nodes

    def resolve(self, bindings, used):
        """Return a node with parameters replaced by the selected values.

        Args:
            bindings (dict): A mapping of parameter bindings.
            used (Dict[Union[str, int], bool]): A mapping of already used
                parameters. This will be modified for each parameter found
                in ``bindings``.

        Returns:
            Node: The current node, if all nodes are already resolved.
            Otherwise returns a modifed :class:`DisjunctionNode` with
            each individual node resolved.
        """
        resolved_nodes = [node.resolve(bindings, used) for node in self._nodes]
        if resolved_nodes == self._nodes:
            return self

        return DisjunctionNode(*resolved_nodes)


# AND and OR are preferred aliases for these.
AND = ConjunctionNode
OR = DisjunctionNode


def _query_options(wrapped):
    """A decorator for functions with query arguments for arguments.

    Many methods of :class:`Query` all take more or less the same arguments
    from which they need to create a :class:`QueryOptions` instance following
    the same somewhat complicated rules.

    This decorator wraps these methods with a function that does this
    processing for them and passes in a :class:`QueryOptions` instance using
    the ``_options`` argument to those functions, bypassing all of the
    other arguments.
    """
    # If there are any positional arguments, get their names
    signature = inspect.signature(wrapped)
    positional = [
        name
        for name, parameter in signature.parameters.items()
        if parameter.kind
        in (parameter.POSITIONAL_ONLY, parameter.POSITIONAL_OR_KEYWORD)
        and name != "self"
    ]
    assert not (positional and positional[0] == "self")

    @functools.wraps(wrapped)
    def wrapper(self, *args, **kwargs):
        # Maybe we already did this (in the case of X calling X_async)
        if "_options" in kwargs:
            return wrapped(self, _options=kwargs["_options"])

        # Transfer any positional args to keyword args, so they're all in the
        # same structure.
        for name, value in zip(positional, args):
            if name in kwargs:
                raise TypeError(
                    "{}() got multiple values for argument '{}'".format(
                        wrapped.__name__, name
                    )
                )
            kwargs[name] = value

        options = kwargs.pop("options", None)
        if options is not None:
            _log.warning(
                "Deprecation warning: passing 'options' to 'Query' methods is "
                "deprecated. Please pass arguments directly."
            )

        if kwargs.get("keys_only"):
            if kwargs.get("projection"):
                raise TypeError(
                    "Cannot specify 'projection' with 'keys_only=True'"
                )
            kwargs["projection"] = ["__key__"]
            del kwargs["keys_only"]

        if kwargs.get("transaction"):
            read_consistency = kwargs.pop(
                "read_consistency", kwargs.pop("read_policy", None)
            )
            if read_consistency == _datastore_api.EVENTUAL:
                raise TypeError(
                    "Can't use 'transaction' with 'read_policy=ndb.EVENTUAL'"
                )

        # Get arguments for QueryOptions attributes
        query_arguments = {
            name: self._option(name, kwargs.pop(name, None), options)
            for name in QueryOptions.slots()
        }

        # Any left over kwargs don't actually correspond to slots in
        # QueryOptions, but should be left to the QueryOptions constructor to
        # sort out. Some might be synonyms or shorthand for other options.
        query_arguments.update(kwargs)

        client = context_module.get_context().client
        query_options = QueryOptions(client=client, **query_arguments)

        return wrapped(self, _options=query_options)

    return wrapper


class QueryOptions(_options.ReadOptions):
    __slots__ = (
        # Query options
        "kind",
        "ancestor",
        "filters",
        "order_by",
        "orders",
        "distinct_on",
        "group_by",
        "namespace",
        "project",
        # Fetch options
        "keys_only",
        "limit",
        "offset",
        "start_cursor",
        "end_cursor",
        # Both (!?!)
        "projection",
    )

    def __init__(self, config=None, client=None, **kwargs):
        if kwargs.get("batch_size"):
            raise exceptions.NoLongerImplementedError()

        if kwargs.get("prefetch_size"):
            raise exceptions.NoLongerImplementedError()

        if kwargs.pop("produce_cursors", None):
            _log.warning(
                "Deprecation warning: 'produce_cursors' is deprecated. "
                "Cursors are always produced when available. This option is "
                "ignored."
            )

        super(QueryOptions, self).__init__(config=config, **kwargs)

        if client:
            if not self.project:
                self.project = client.project

            if not self.namespace:
                self.namespace = client.namespace


class Query:
    """Query object.

    Args:
        kind (str): The kind of entities to be queried.
        filters (FilterNode): Node representing a filter expression tree.
        ancestor (key.Key): Entities returned will be descendants of
            `ancestor`.
        order_by (list[Union[str, google.cloud.ndb.model.Property]]): The
            model properties used to order query results.
        orders (list[Union[str, google.cloud.ndb.model.Property]]):
            Deprecated. Synonym for `order_by`.
        project (str): The project to perform the query in. Also known as the
            app, in Google App Engine. If not passed, uses the client's value.
        app (str): Deprecated. Synonym for `project`.
        namespace (str): The namespace to which to restrict results.
            If not passed, uses the client's value.
        projection (list[str]): The fields to return as part of the query
            results.
        distinct_on (list[str]): The field names used to group query
            results.
        group_by (list[str]): Deprecated. Synonym for distinct_on.
        default_options (QueryOptions): QueryOptions object.

    Raises:
        TypeError: If any of the arguments are invalid.
    """

    def __init__(
        self,
        kind=None,
        filters=None,
        ancestor=None,
        order_by=None,
        orders=None,
        project=None,
        app=None,
        namespace=None,
        projection=None,
        distinct_on=None,
        group_by=None,
        default_options=None,
    ):
        self.default_options = None

        if app:
            if project:
                raise TypeError(
                    "Cannot use both app and project, they are synonyms. app "
                    "is deprecated."
                )
            project = app

        if default_options is not None:
            _log.warning(
                "Deprecation warning: passing default_options to the Query"
                "constructor is deprecated. Please directly pass any "
                "arguments you want to use to the Query constructor or its "
                "methods."
            )

            if not isinstance(default_options, QueryOptions):
                raise TypeError(
                    "default_options must be QueryOptions or None; "
                    "received {}".format(default_options)
                )

            # Not sure why we're doing all this checking just for this one
            # option.
            if projection is not None:
                if getattr(default_options, "projection", None) is not None:
                    raise TypeError(
                        "cannot use projection keyword argument and "
                        "default_options.projection at the same time"
                    )

            self.default_options = default_options
            kind = self._option("kind", kind)
            filters = self._option("filters", filters)
            ancestor = self._option("ancestor", ancestor)
            order_by = self._option("order_by", order_by)
            orders = self._option("orders", orders)
            project = self._option("project", project)
            app = self._option("app", app)
            namespace = self._option("namespace", namespace)
            projection = self._option("projection", projection)
            distinct_on = self._option("distinct_on", distinct_on)
            group_by = self._option("group_by", group_by)

        if ancestor is not None:
            if isinstance(ancestor, ParameterizedThing):
                if isinstance(ancestor, ParameterizedFunction):
                    if ancestor.func != "key":
                        raise TypeError(
                            "ancestor cannot be a GQL function"
                            "other than Key"
                        )
            else:
                if not isinstance(ancestor, model.Key):
                    raise TypeError(
                        "ancestor must be a Key; "
                        "received {}".format(ancestor)
                    )
                if not ancestor.id():
                    raise ValueError("ancestor cannot be an incomplete key")
                if project is not None:
                    if project != ancestor.app():
                        raise TypeError("ancestor/project id mismatch")
                else:
                    project = ancestor.app()
                if namespace is not None:
                    if namespace != ancestor.namespace():
                        raise TypeError("ancestor/namespace mismatch")
                else:
                    namespace = ancestor.namespace()
        if filters is not None:
            if not isinstance(filters, Node):
                raise TypeError(
                    "filters must be a query Node or None; "
                    "received {}".format(filters)
                )
        if order_by is not None and orders is not None:
            raise TypeError(
                "Cannot use both orders and order_by, they are synonyms"
                "(orders is deprecated now)"
            )
        if order_by is None:
            order_by = orders
        if order_by is not None:
            if not isinstance(order_by, (list, tuple)):
                raise TypeError(
                    "order must be a list, a tuple or None; "
                    "received {}".format(order_by)
                )
            order_by = self._to_property_orders(order_by)

        self.kind = kind
        self.ancestor = ancestor
        self.filters = filters
        self.order_by = order_by
        self.project = project
        self.namespace = namespace

        self.projection = None
        if projection is not None:
            if not projection:
                raise TypeError("projection argument cannot be empty")
            if not isinstance(projection, (tuple, list)):
                raise TypeError(
                    "projection must be a tuple, list or None; "
                    "received {}".format(projection)
                )
            self._check_properties(self._to_property_names(projection))
            self.projection = tuple(projection)

        if distinct_on is not None and group_by is not None:
            raise TypeError(
                "Cannot use both group_by and distinct_on, they are synonyms. "
                "group_by is deprecated."
            )
        if distinct_on is None:
            distinct_on = group_by

        self.distinct_on = None
        if distinct_on is not None:
            if not distinct_on:
                raise TypeError("distinct_on argument cannot be empty")
            if not isinstance(distinct_on, (tuple, list)):
                raise TypeError(
                    "distinct_on must be a tuple, list or None; "
                    "received {}".format(distinct_on)
                )
            self._check_properties(self._to_property_names(distinct_on))
            self.distinct_on = tuple(distinct_on)

    def __repr__(self):
        args = []
        if self.project is not None:
            args.append("project=%r" % self.project)
        if self.namespace is not None:
            args.append("namespace=%r" % self.namespace)
        if self.kind is not None:
            args.append("kind=%r" % self.kind)
        if self.ancestor is not None:
            args.append("ancestor=%r" % self.ancestor)
        if self.filters is not None:
            args.append("filters=%r" % self.filters)
        if self.order_by is not None:
            args.append("order_by=%r" % self.order_by)
        if self.projection:
            args.append(
                "projection=%r" % (self._to_property_names(self.projection))
            )
        if self.distinct_on:
            args.append(
                "distinct_on=%r" % (self._to_property_names(self.distinct_on))
            )
        if self.default_options is not None:
            args.append("default_options=%r" % self.default_options)
        return "%s(%s)" % (self.__class__.__name__, ", ".join(args))

    @property
    def is_distinct(self):
        """True if results are guaranteed to contain a unique set of property
        values.

        This happens when every property in distinct_on is also in projection.
        """
        return bool(
            self.distinct_on
            and set(self._to_property_names(self.distinct_on))
            <= set(self._to_property_names(self.projection))
        )

    def filter(self, *filters):
        """Return a new Query with additional filter(s) applied.

        Args:
            filters (list[Node]): One or more instances of Node.

        Returns:
            Query: A new query with the new filters applied.

        Raises:
            TypeError: If one of the filters is not a Node.
        """
        if not filters:
            return self
        new_filters = []
        if self.filters:
            new_filters.append(self.filters)
        for filter in filters:
            if not isinstance(filter, Node):
                raise TypeError(
                    "Cannot filter a non-Node argument; received %r" % filter
                )
            new_filters.append(filter)
        if len(new_filters) == 1:
            new_filters = new_filters[0]
        else:
            new_filters = ConjunctionNode(*new_filters)
        return self.__class__(
            kind=self.kind,
            ancestor=self.ancestor,
            filters=new_filters,
            order_by=self.order_by,
            project=self.project,
            namespace=self.namespace,
            default_options=self.default_options,
            projection=self.projection,
            distinct_on=self.distinct_on,
        )

    def order(self, *props):
        """Return a new Query with additional sort order(s) applied.

        Args:
            props (list[Union[str, google.cloud.ndb.model.Property]]): One or
                more model properties to sort by.

        Returns:
            Query: A new query with the new order applied.
        """
        if not props:
            return self
        property_orders = self._to_property_orders(props)
        order_by = self.order_by
        if order_by is None:
            order_by = property_orders
        else:
            order_by.extend(property_orders)
        return self.__class__(
            kind=self.kind,
            ancestor=self.ancestor,
            filters=self.filters,
            order_by=order_by,
            project=self.project,
            namespace=self.namespace,
            default_options=self.default_options,
            projection=self.projection,
            distinct_on=self.distinct_on,
        )

    def analyze(self):
        """Return a list giving the parameters required by a query.

        When a query is created using gql, any bound parameters
        are created as ParameterNode instances. This method returns
        the names of any such parameters.

        Returns:
            list[str]: required parameter names.
        """

        class MockBindings(dict):
            def __contains__(self, key):
                self[key] = None
                return True

        bindings = MockBindings()
        used = {}
        ancestor = self.ancestor
        if isinstance(ancestor, ParameterizedThing):
            ancestor = ancestor.resolve(bindings, used)
        filters = self.filters
        if filters is not None:
            filters = filters.resolve(bindings, used)
        return sorted(used)  # Returns only the keys.

    def bind(self, *positional, **keyword):
        """Bind parameter values.  Returns a new Query object.

        When a query is created using gql, any bound parameters
        are created as ParameterNode instances. This method
        receives values for both positional (:1, :2, etc.) or
        keyword (:xyz, :abc, etc.) bound parameters, then sets the
        values accordingly. This mechanism allows easy reuse of a
        parameterized query, by passing the values to bind here.

        Args:
            positional (list[Any]): One or more positional values to bind.
            keyword (dict[Any]): One or more keyword values to bind.

        Returns:
            Query: A new query with the new bound parameter values.

        Raises:
            google.cloud.ndb.exceptions.BadArgumentError: If one of
                the positional parameters is not used in the query.
        """
        bindings = dict(keyword)
        for i, arg in enumerate(positional):
            bindings[i + 1] = arg
        used = {}
        ancestor = self.ancestor
        if isinstance(ancestor, ParameterizedThing):
            ancestor = ancestor.resolve(bindings, used)
        filters = self.filters
        if filters is not None:
            filters = filters.resolve(bindings, used)
        unused = []
        for i, arg in enumerate(positional):
            if i + 1 not in used:
                unused.append(i + 1)
        if unused:
            raise exceptions.BadArgumentError(
                "Positional arguments %s were given but not used."
                % ", ".join(str(i) for i in unused)
            )
        return self.__class__(
            kind=self.kind,
            ancestor=ancestor,
            filters=filters,
            order_by=self.order_by,
            project=self.project,
            namespace=self.namespace,
            default_options=self.default_options,
            projection=self.projection,
            distinct_on=self.distinct_on,
        )

    def _to_property_names(self, properties):
        fixed = []
        for prop in properties:
            if isinstance(prop, str):
                fixed.append(prop)
            elif isinstance(prop, model.Property):
                fixed.append(prop._name)
            else:
                raise TypeError(
                    "Unexpected property {}; "
                    "should be string or Property".format(prop)
                )
        return fixed

    def _to_property_orders(self, order_by):
        orders = []
        for order in order_by:
            if isinstance(order, PropertyOrder):
                # if a negated property, will already be a PropertyOrder
                orders.append(order)
            elif isinstance(order, model.Property):
                # use the sign to turn it into a PropertyOrder
                orders.append(+order)
            elif isinstance(order, str):
                name = order
                reverse = False
                if order.startswith("-"):
                    name = order[1:]
                    reverse = True
                property_order = PropertyOrder(name, reverse=reverse)
                orders.append(property_order)
            else:
                raise TypeError("Order values must be properties or strings")
        return orders

    def _check_properties(self, fixed, **kwargs):
        modelclass = model.Model._kind_map.get(self.kind)
        if modelclass is not None:
            modelclass._check_properties(fixed, **kwargs)

    @_query_options
    def fetch(
        self,
        limit=None,
        *,
        keys_only=None,
        projection=None,
        offset=None,
        batch_size=None,
        prefetch_size=None,
        produce_cursors=False,
        start_cursor=None,
        end_cursor=None,
        timeout=None,
        deadline=None,
        read_consistency=None,
        read_policy=None,
        transaction=None,
        options=None,
        _options=None,
    ):
        """Run a query, fetching results.

        Args:
            limit (Optional[int]): Maximum number of results to fetch.
                data:`None` or data:`0` indicates no limit.
            keys_only (bool): Return keys instead of entities.
            projection (list[str]): The fields to return as part of the query
                results.
            offset (int): Number of query results to skip.
            limit (Optional[int]): Maximum number of query results to return.
                If not specified, there is no limit.
            batch_size (Optional[int]): Number of results to fetch in a single
                RPC call. Affects efficiency of queries only. Larger batch
                sizes use more memory but make fewer RPC calls.
            prefetch_size (Optional[int]): Overrides batch size for first batch
                returned.
            produce_cursors (bool): Whether to generate cursors from query.
            start_cursor: Starting point for search.
            end_cursor: Endpoint point for search.
            timeout (Optional[int]): Override the gRPC timeout, in seconds.
            deadline (Optional[int]): DEPRECATED: Synonym for ``timeout``.
            read_consistency: If not in a transaction, defaults to
                ``ndb.EVENTUAL`` for potentially faster query results without
                having to wait for Datastore to apply pending changes to all
                returned records. Otherwise consistency with current
                transaction is maintained.
            read_policy: DEPRECATED: Synonym for ``read_consistency``.
            transaction (bytes): Transaction ID to use for query. Results will
                be consistent with Datastore state for that transaction.
                Implies ``read_policy=ndb.STRONG``.
            options (QueryOptions): DEPRECATED: An object containing options
                values for some of these arguments.

        Returns:
            List([model.Model]): The query results.
        """
        return self.fetch_async(_options=_options).result()

    @_query_options
    def fetch_async(
        self,
        limit=None,
        *,
        keys_only=None,
        projection=None,
        offset=None,
        batch_size=None,
        prefetch_size=None,
        produce_cursors=False,
        start_cursor=None,
        end_cursor=None,
        timeout=None,
        deadline=None,
        read_consistency=None,
        read_policy=None,
        transaction=None,
        options=None,
        _options=None,
    ):
        """Run a query, asynchronously fetching the results.

        Args:
            keys_only (bool): Return keys instead of entities.
            projection (list[str]): The fields to return as part of the query
                results.
            offset (int): Number of query results to skip.
            limit (Optional[int]): Maximum number of query results to return.
                If not specified, there is no limit.
            batch_size (Optional[int]): Number of results to fetch in a single
                RPC call. Affects efficiency of queries only. Larger batch
                sizes use more memory but make fewer RPC calls.
            prefetch_size (Optional[int]): Overrides batch size for first batch
                returned.
            produce_cursors (bool): Whether to generate cursors from query.
            start_cursor: Starting point for search.
            end_cursor: Endpoint point for search.
            timeout (Optional[int]): Override the gRPC timeout, in seconds.
            deadline (Optional[int]): DEPRECATED: Synonym for ``timeout``.
            read_consistency: If not in a transaction, defaults to
                ``ndb.EVENTUAL`` for potentially faster query results without
                having to wait for Datastore to apply pending changes to all
                returned records. Otherwise consistency with current
                transaction is maintained.
            read_policy: DEPRECATED: Synonym for ``read_consistency``.
            transaction (bytes): Transaction ID to use for query. Results will
                be consistent with Datastore state for that transaction.
                Implies ``read_policy=ndb.STRONG``.
            options (QueryOptions): DEPRECATED: An object containing options
                values for some of these arguments.

        Returns:
            tasklets.Future: Eventual result will be a List[model.Model] of the
                results.
        """
        return _datastore_query.fetch(_options)

    def _option(self, name, given, options=None):
        """Get given value or a provided default for an option.

        Precedence is given first to the `given` value, then any value passed
        in with `options`, then any value that is already set on this query,
        and, lastly, any default value in `default_options` if provided to the
        :class:`Query` constructor.

        This attempts to reconcile, in as rational a way possible, all the
        different ways of passing the same option to a query established by
        legacy NDB. Because of the absurd amount of complexity involved,
        `QueryOptions` is deprecated in favor of just passing arguments
        directly to the `Query` constructor or its methods.

        Args:
            name (str): Name of the option.
            given (Any): The given value for the option.
            options (Optional[QueryOptions]): An object containing option
                values.

        Returns:
            Any: Either the given value or a provided default.
        """
        if given is not None:
            return given

        if options is not None:
            value = getattr(options, name, None)
            if value is not None:
                return value

        value = getattr(self, name, None)
        if value is not None:
            return value

        if self.default_options is not None:
            return getattr(self.default_options, name, None)

        return None

    def run_to_queue(self, queue, conn, options=None, dsquery=None):
        """Run this query, putting entities into the given queue."""
        raise exceptions.NoLongerImplementedError()

    @_query_options
    def iter(
        self,
        keys_only=None,
        limit=None,
        projection=None,
        offset=None,
        batch_size=None,
        prefetch_size=None,
        produce_cursors=False,
        start_cursor=None,
        end_cursor=None,
        timeout=None,
        deadline=None,
        read_consistency=None,
        read_policy=None,
        transaction=None,
        options=None,
        _options=None,
    ):
        """Get an iterator over query results.

        Args:
            keys_only (bool): Return keys instead of entities.
            limit (Optional[int]): Maximum number of query results to return.
                If not specified, there is no limit.
            projection (list[str]): The fields to return as part of the query
                results.
            offset (int): Number of query results to skip.
            batch_size (Optional[int]): Number of results to fetch in a single
                RPC call. Affects efficiency of queries only. Larger batch
                sizes use more memory but make fewer RPC calls.
            prefetch_size (Optional[int]): Overrides batch size for first batch
                returned.
            produce_cursors (bool): Whether to generate cursors from query.
            start_cursor: Starting point for search.
            end_cursor: Endpoint point for search.
            timeout (Optional[int]): Override the gRPC timeout, in seconds.
            deadline (Optional[int]): DEPRECATED: Synonym for ``timeout``.
            read_consistency: If not in a transaction, defaults to
                ``ndb.EVENTUAL`` for potentially faster query results without
                having to wait for Datastore to apply pending changes to all
                returned records. Otherwise consistency with current
                transaction is maintained.
            read_policy: DEPRECATED: Synonym for ``read_consistency``.
            transaction (bytes): Transaction ID to use for query. Results will
                be consistent with Datastore state for that transaction.
                Implies ``read_policy=ndb.STRONG``.
            options (QueryOptions): DEPRECATED: An object containing options
                values for some of these arguments.

        Returns:
            QueryIterator: An iterator.
        """
        return _datastore_query.iterate(_options)

    __iter__ = iter

    def map(
        self,
        callback,
        *,
        pass_batch_into_callback=None,
        merge_future=None,
        keys_only=None,
        limit=None,
        projection=None,
        offset=None,
        batch_size=None,
        prefetch_size=None,
        produce_cursors=False,
        start_cursor=None,
        end_cursor=None,
        timeout=None,
        deadline=None,
        read_consistency=None,
        read_policy=None,
        transaction=None,
        options=None,
    ):
        """Map a callback function or tasklet over the query results.

        Args:
            callback (Callable): A function or tasklet to be applied to each
                result; see below.
            merge_future: Optional ``Future`` subclass; see below.
            keys_only (bool): Return keys instead of entities.
            projection (list[str]): The fields to return as part of the query
                results.
            offset (int): Number of query results to skip.
            limit (Optional[int]): Maximum number of query results to return.
                If not specified, there is no limit.
            batch_size (Optional[int]): Number of results to fetch in a single
                RPC call. Affects efficiency of queries only. Larger batch
                sizes use more memory but make fewer RPC calls.
            prefetch_size (Optional[int]): Overrides batch size for first batch
                returned.
            produce_cursors (bool): Whether to generate cursors from query.
            start_cursor: Starting point for search.
            end_cursor: Endpoint point for search.
            timeout (Optional[int]): Override the gRPC timeout, in seconds.
            deadline (Optional[int]): DEPRECATED: Synonym for ``timeout``.
            read_consistency: If not in a transaction, defaults to
                ``ndb.EVENTUAL`` for potentially faster query results without
                having to wait for Datastore to apply pending changes to all
                returned records. Otherwise consistency with current
                transaction is maintained.
            read_policy: DEPRECATED: Synonym for ``read_consistency``.
            transaction (bytes): Transaction ID to use for query. Results will
                be consistent with Datastore state for that transaction.
                Implies ``read_policy=ndb.STRONG``.
            options (QueryOptions): DEPRECATED: An object containing options
                values for some of these arguments.

        Callback signature: The callback is normally called with an entity
        as argument.  However if keys_only=True is given, it is called
        with a Key.  Also, when pass_batch_into_callback is True, it is
        called with three arguments: the current batch, the index within
        the batch, and the entity or Key at that index.  The callback can
        return whatever it wants.  If the callback is None, a trivial
        callback is assumed that just returns the entity or key passed in
        (ignoring produce_cursors).

        Optional merge future: The merge_future is an advanced argument
        that can be used to override how the callback results are combined
        into the overall map() return value.  By default a list of
        callback return values is produced.  By substituting one of a
        small number of specialized alternatives you can arrange
        otherwise.  See tasklets.MultiFuture for the default
        implementation and a description of the protocol the merge_future
        object must implement the default.  Alternatives from the same
        module include QueueFuture, SerialQueueFuture and ReducingFuture.

        Returns:
            Any: When the query has run to completion and all callbacks have
                returned, map() returns a list of the results of all callbacks.
                (But see 'optional merge future' above.)
        """
        raise NotImplementedError

    def map_async(
        self,
        callback,
        *,
        pass_batch_into_callback=None,
        merge_future=None,
        keys_only=None,
        limit=None,
        projection=None,
        offset=None,
        batch_size=None,
        prefetch_size=None,
        produce_cursors=False,
        start_cursor=None,
        end_cursor=None,
        timeout=None,
        deadline=None,
        read_consistency=None,
        read_policy=None,
        transaction=None,
        options=None,
    ):
        """Map a callback function or tasklet over the query results.

        This is the asynchronous version of :meth:`Query.map`.

        Returns:
            tasklets.Future: See :meth:`Query.map` for eventual result.
        """
        raise NotImplementedError

    def get(
        self,
        keys_only=None,
        limit=None,
        projection=None,
        offset=None,
        batch_size=None,
        prefetch_size=None,
        produce_cursors=False,
        start_cursor=None,
        end_cursor=None,
        timeout=None,
        deadline=None,
        read_consistency=None,
        read_policy=None,
        transaction=None,
        options=None,
    ):
        """Get the first query result, if any.

        This is equivalent to calling ``q.fetch(1)`` and returning the first
        result, if any.

        Args:
            keys_only (bool): Return keys instead of entities.
            projection (list[str]): The fields to return as part of the query
                results.
            offset (int): Number of query results to skip.
            limit (Optional[int]): Maximum number of query results to return.
                If not specified, there is no limit.
            batch_size (Optional[int]): Number of results to fetch in a single
                RPC call. Affects efficiency of queries only. Larger batch
                sizes use more memory but make fewer RPC calls.
            prefetch_size (Optional[int]): Overrides batch size for first batch
                returned.
            produce_cursors (bool): Whether to generate cursors from query.
            start_cursor: Starting point for search.
            end_cursor: Endpoint point for search.
            timeout (Optional[int]): Override the gRPC timeout, in seconds.
            deadline (Optional[int]): DEPRECATED: Synonym for ``timeout``.
            read_consistency: If not in a transaction, defaults to
                ``ndb.EVENTUAL`` for potentially faster query results without
                having to wait for Datastore to apply pending changes to all
                returned records. Otherwise consistency with current
                transaction is maintained.
            read_policy: DEPRECATED: Synonym for ``read_consistency``.
            transaction (bytes): Transaction ID to use for query. Results will
                be consistent with Datastore state for that transaction.
                Implies ``read_policy=ndb.STRONG``.
            options (QueryOptions): DEPRECATED: An object containing options
                values for some of these arguments.

            Returns:
                Optional[Union[entity.Entity, key.Key]]: A single result, or
                    :data:`None` if there are no results.
        """
        raise NotImplementedError

    def get_async(
        self,
        keys_only=None,
        limit=None,
        projection=None,
        offset=None,
        batch_size=None,
        prefetch_size=None,
        produce_cursors=False,
        start_cursor=None,
        end_cursor=None,
        timeout=None,
        deadline=None,
        read_consistency=None,
        read_policy=None,
        transaction=None,
        options=None,
    ):
        """Get the first query result, if any.

        This is the asynchronous version of :meth:`Query.get`.

        Returns:
            tasklets.Future: See :meth:`Query.get` for eventual result.
        """
        raise NotImplementedError

    def count(
        self,
        keys_only=None,
        limit=None,
        projection=None,
        offset=None,
        batch_size=None,
        prefetch_size=None,
        produce_cursors=False,
        start_cursor=None,
        end_cursor=None,
        timeout=None,
        deadline=None,
        read_consistency=None,
        read_policy=None,
        transaction=None,
        options=None,
    ):
        """Count the number of query results, up to a limit.

        This returns the same result as ``len(q.fetch(limit))`` but more
        efficiently.

        Note that you should pass a maximum value to limit the amount of
        work done by the query.

        Args:
            keys_only (bool): Return keys instead of entities.
            projection (list[str]): The fields to return as part of the query
                results.
            offset (int): Number of query results to skip.
            limit (Optional[int]): Maximum number of query results to return.
                If not specified, there is no limit.
            batch_size (Optional[int]): Number of results to fetch in a single
                RPC call. Affects efficiency of queries only. Larger batch
                sizes use more memory but make fewer RPC calls.
            prefetch_size (Optional[int]): Overrides batch size for first batch
                returned.
            produce_cursors (bool): Whether to generate cursors from query.
            start_cursor: Starting point for search.
            end_cursor: Endpoint point for search.
            timeout (Optional[int]): Override the gRPC timeout, in seconds.
            deadline (Optional[int]): DEPRECATED: Synonym for ``timeout``.
            read_consistency: If not in a transaction, defaults to
                ``ndb.EVENTUAL`` for potentially faster query results without
                having to wait for Datastore to apply pending changes to all
                returned records. Otherwise consistency with current
                transaction is maintained.
            read_policy: DEPRECATED: Synonym for ``read_consistency``.
            transaction (bytes): Transaction ID to use for query. Results will
                be consistent with Datastore state for that transaction.
                Implies ``read_policy=ndb.STRONG``.
            options (QueryOptions): DEPRECATED: An object containing options
                values for some of these arguments.

            Returns:
                Optional[Union[entity.Entity, key.Key]]: A single result, or
                    :data:`None` if there are no results.
        """
        raise NotImplementedError

    def count_async(
        self,
        keys_only=None,
        limit=None,
        projection=None,
        offset=None,
        batch_size=None,
        prefetch_size=None,
        produce_cursors=False,
        start_cursor=None,
        end_cursor=None,
        timeout=None,
        deadline=None,
        read_consistency=None,
        read_policy=None,
        transaction=None,
        options=None,
    ):
        """Count the number of query results, up to a limit.

        This is the asynchronous version of :meth:`Query.count`.

        Returns:
            tasklets.Future: See :meth:`Query.count` for eventual result.
        """
        raise NotImplementedError

    def fetch_page(
        self,
        page_size,
        *,
        keys_only=None,
        limit=None,
        projection=None,
        offset=None,
        batch_size=None,
        prefetch_size=None,
        produce_cursors=False,
        start_cursor=None,
        end_cursor=None,
        timeout=None,
        deadline=None,
        read_consistency=None,
        read_policy=None,
        transaction=None,
        options=None,
    ):
        """Fetch a page of results.

        This is a specialized method for use by paging user interfaces.

        To fetch the next page, you pass the cursor returned by one call to the
        next call using the `start_cursor` argument.  A common idiom is to pass
        the cursor to the client using :meth:`_datastore_query.Cursor.urlsafe`
        and to reconstruct that cursor on a subsequent request using the
        `urlsafe` argument to :class:`Cursor`.

        Args:
            page_size (int): The number of results per page. At most, this many
                results will be returned.

        Returns:
            Tuple[list, bytes, bool]: A tuple `(results, cursor, more)` where
                `results` is a list of query results, `cursor` is a cursor
                pointing just after the last result returned, and `more`
                indicates whether there are (likely) more results after that.
        """
        raise NotImplementedError

    def fetch_page_async(
        self,
        page_size,
        *,
        keys_only=None,
        limit=None,
        projection=None,
        offset=None,
        batch_size=None,
        prefetch_size=None,
        produce_cursors=False,
        start_cursor=None,
        end_cursor=None,
        timeout=None,
        deadline=None,
        read_consistency=None,
        read_policy=None,
        transaction=None,
        options=None,
    ):
        """Fetch a page of results.

        This is the asynchronous version of :meth:`Query.fetch_page`.

        Returns:
            tasklets.Future: See :meth:`Query.fetch_page` for eventual result.
        """
        raise NotImplementedError


def gql(query_string, *args, **kwds):
    """Parse a GQL query string.

    Args:
        query_string (str): Full GQL query, e.g. 'SELECT * FROM Kind WHERE
            prop = 1 ORDER BY prop2'.
        args: If present, used to call bind().
        kwds: If present, used to call bind().

    Returns:
        Query: a query instance.

    Raises:
        google.cloud.ndb.exceptions.BadQueryError: When bad gql is passed in.
    """
    query = _gql.GQL(query_string).get_query()
    if args or kwds:
        query = query.bind(*args, **kwds)
    return query
