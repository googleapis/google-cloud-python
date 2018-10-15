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
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class Parameter(ParameterizedThing):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class ParameterizedFunction(ParameterizedThing):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class Node:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


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
