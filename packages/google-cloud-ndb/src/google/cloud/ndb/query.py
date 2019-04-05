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

import logging

from google.cloud.ndb import _datastore_query
from google.cloud.ndb import exceptions
from google.cloud.ndb import model


__all__ = [
    "Cursor",
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
    "QueryIterator",
]


Cursor = NotImplemented  # From `google.appengine.datastore.datastore_query`
_EQ_OP = "="
_NE_OP = "!="
_IN_OP = "in"
_LT_OP = "<"
_GT_OP = ">"
_OPS = frozenset([_EQ_OP, _NE_OP, _LT_OP, "<=", _GT_OP, ">=", _IN_OP])

_log = logging.getLogger(__name__)


class QueryOptions:
    __slots__ = (
        # Query options
        "kind",
        "project",
        "namespace",
        "ancestor",
        "filters",
        "order_by",
        "orders",
        "distinct_on",
        "group_by",
        # Fetch options
        "keys_only",
        "limit",
        "offset",
        "start_cursor",
        "end_cursor",
        "eventual",
        "batch_size",
        "prefetch_size",
        "produce_cursors",
        "start_cursor",
        "end_cursor",
        "deadline",
        "read_policy",
        # Both (!?!)
        "projection",
    )

    def __init__(self, config=None, **kwargs):
        if config is not None and not isinstance(config, QueryOptions):
            raise TypeError("Config must be a QueryOptions instance.")

        for key in self.__slots__:
            default = getattr(config, key, None) if config else None
            setattr(self, key, kwargs.get(key, default))

    def __eq__(self, other):
        if not isinstance(other, QueryOptions):
            return NotImplemented

        for key in self.__slots__:
            if getattr(self, key, None) != getattr(other, key, None):
                return False

        return True

    def __repr__(self):
        options = ", ".join(
            [
                "{}={}".format(key, repr(getattr(self, key, None)))
                for key in self.__slots__
                if getattr(self, key, None) is not None
            ]
        )
        return "QueryOptions({})".format(options)


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

    def _to_filter(self, post=False):
        """Helper to convert to low-level filters.

        Args:
            post (bool): Indicates if this is a post-filter node.

        Returns:
            Optional[List[Node]]: List of filter protocol buffers that should
                be combined using OR. The code in `_datastore_query` will
                recognize that a list has been returned and run multiple
                queries.
        """
        if post:
            raise NotImplementedError("No idea what I should do here, yet.")

        return [node._to_filter(post=post) for node in self._nodes]


# AND and OR are preferred aliases for these.
AND = ConjunctionNode
OR = DisjunctionNode


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

        if app:
            if project:
                raise TypeError(
                    "Cannot use both app and project, they are synonyms. app "
                    "is deprecated."
                )
            project = app

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
        for arg in positional:
            if arg not in used:
                unused.append(i)
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

    def fetch(
        self,
        keys_only=None,
        projection=None,
        offset=0,
        limit=None,
        batch_size=None,  # 20?   # placeholder
        prefetch_size=None,
        produce_cursors=False,
        start_cursor=None,
        end_cursor=None,
        deadline=None,
        read_policy=None,  #  _datastore_api.EVENTUAL,  # placeholder
        options=None,
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
            deadline (Optional[int]): Override the RPC deadline, in seconds.
            read_policy: Defaults to `ndb.EVENTUAL` for potentially faster
                query results without having to wait for Datastore to apply
                pending changes to all returned records.
            options (QueryOptions): DEPRECATED: An object containing options
                values for some of these arguments.

        Returns:
            List([model.Model]): The query results.
        """
        return self.fetch_async(
            keys_only=keys_only,
            projection=projection,
            offset=offset,
            limit=limit,
            batch_size=batch_size,
            prefetch_size=prefetch_size,
            produce_cursors=produce_cursors,
            start_cursor=start_cursor,
            end_cursor=end_cursor,
            deadline=deadline,
            read_policy=read_policy,
            options=options,
        ).result()

    def fetch_async(
        self,
        keys_only=None,
        projection=None,
        offset=0,
        limit=None,
        batch_size=None,  # 20?   # placeholder
        prefetch_size=None,
        produce_cursors=False,
        start_cursor=None,
        end_cursor=None,
        deadline=None,
        read_policy=None,  #  _datastore_api.EVENTUAL,  # placeholder
        options=None,
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
            deadline (Optional[int]): Override the RPC deadline, in seconds.
            read_policy: Defaults to `ndb.EVENTUAL` for potentially faster
                query results without having to wait for Datastore to apply
                pending changes to all returned records.
            options (QueryOptions): DEPRECATED: An object containing options
                values for some of these arguments.

        Returns:
            tasklets.Future: Eventual result will be a List[model.Model] of the
                results.
        """
        if options is not None:
            _log.warning(
                "Deprecation warning: passing options to Query.fetch or "
                "Query.fetch_async is deprecated. Please pass arguments "
                "directly."
            )

        offset = self._option("offset", offset, options)
        if offset:
            raise NotImplementedError(
                "'offset' is not implemented yet for queries"
            )

        limit = self._option("limit", limit, options)
        if limit:
            raise NotImplementedError(
                "'limit' is not implemented yet for queries"
            )

        batch_size = self._option("batch_size", batch_size, options)
        if batch_size:
            raise NotImplementedError(
                "'batch_size' is not implemented yet for queries"
            )

        prefetch_size = self._option("prefetch_size", prefetch_size, options)
        if prefetch_size:
            raise NotImplementedError(
                "'prefetch_size' is not implemented yet for queries"
            )

        produce_cursors = self._option(
            "produce_cursors", produce_cursors, options
        )
        if produce_cursors:
            raise NotImplementedError(
                "'produce_cursors' is not implemented yet for queries"
            )

        start_cursor = self._option("start_cursor", start_cursor, options)
        if start_cursor:
            raise NotImplementedError(
                "'start_cursor' is not implemented yet for queries"
            )

        end_cursor = self._option("end_cursor", end_cursor, options)
        if end_cursor:
            raise NotImplementedError(
                "'end_cursor' is not implemented yet for queries"
            )

        deadline = self._option("deadline", deadline, options)
        if deadline:
            raise NotImplementedError(
                "'deadline' is not implemented yet for queries"
            )

        read_policy = self._option("read_policy", read_policy, options)
        if read_policy:
            raise NotImplementedError(
                "'read_policy' is not implemented yet for queries"
            )

        projection = self._option("projection", projection, options)
        keys_only = self._option("keys_only", keys_only, options)
        if keys_only:
            if projection:
                raise TypeError(
                    "Cannot specify 'projection' with 'keys_only=True'"
                )
            projection = ["__key__"]

        query_arguments = (
            ("kind", self._option("kind", None, options)),
            ("project", self._option("project", None, options)),
            ("namespace", self._option("namespace", None, options)),
            ("ancestor", self._option("ancestor", None, options)),
            ("filters", self._option("filters", None, options)),
            ("order_by", self._option("order_by", None, options)),
            ("distinct_on", self._option("distinct_on", None, options)),
            ("projection", projection),
        )
        query_arguments = {
            name: value for name, value in query_arguments if value is not None
        }
        query_options = QueryOptions(**query_arguments)

        return _datastore_query.fetch(query_options)

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


def gql(*args, **kwargs):
    raise NotImplementedError


class QueryIterator:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError
