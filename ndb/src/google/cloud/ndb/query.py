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
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class ParameterNode(Node):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


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
