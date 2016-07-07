# Copyright 2014 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Create / interact with gcloud datastore queries."""

import base64

from gcloud._helpers import _ensure_tuple_or_list
from gcloud.datastore._generated import query_pb2 as _query_pb2
from gcloud.datastore import helpers
from gcloud.datastore.key import Key


class Query(object):
    """A Query against the Cloud Datastore.

    This class serves as an abstraction for creating a query over data
    stored in the Cloud Datastore.

    :type client: :class:`gcloud.datastore.client.Client`
    :param client: The client used to connect to datastore.

    :type kind: string
    :param kind: The kind to query.

    :type project: string
    :param project: The project associated with the query.  If not passed,
                    uses the client's value.

    :type namespace: string or None
    :param namespace: The namespace to which to restrict results.  If not
                      passed, uses the client's value.

    :type ancestor: :class:`gcloud.datastore.key.Key` or None
    :param ancestor: key of the ancestor to which this query's results are
                     restricted.

    :type filters: sequence of (property_name, operator, value) tuples
    :param filters: property filters applied by this query.

    :type projection: sequence of string
    :param projection:  fields returned as part of query results.

    :type order: sequence of string
    :param order:  field names used to order query results. Prepend '-'
                   to a field name to sort it in descending order.

    :type distinct_on: sequence of string
    :param distinct_on: field names used to group query results.

    :raises: ValueError if ``project`` is not passed and no implicit
             default is set.
    """

    OPERATORS = {
        '<=': _query_pb2.PropertyFilter.LESS_THAN_OR_EQUAL,
        '>=': _query_pb2.PropertyFilter.GREATER_THAN_OR_EQUAL,
        '<': _query_pb2.PropertyFilter.LESS_THAN,
        '>': _query_pb2.PropertyFilter.GREATER_THAN,
        '=': _query_pb2.PropertyFilter.EQUAL,
    }
    """Mapping of operator strings and their protobuf equivalents."""

    def __init__(self,
                 client,
                 kind=None,
                 project=None,
                 namespace=None,
                 ancestor=None,
                 filters=(),
                 projection=(),
                 order=(),
                 distinct_on=()):

        self._client = client
        self._kind = kind
        self._project = project or client.project
        self._namespace = namespace or client.namespace
        self._ancestor = ancestor
        self._filters = []
        # Verify filters passed in.
        for property_name, operator, value in filters:
            self.add_filter(property_name, operator, value)
        self._projection = _ensure_tuple_or_list('projection', projection)
        self._order = _ensure_tuple_or_list('order', order)
        self._distinct_on = _ensure_tuple_or_list('distinct_on', distinct_on)

    @property
    def project(self):
        """Get the project for this Query.

        :rtype: str
        """
        return self._project or self._client.project

    @property
    def namespace(self):
        """This query's namespace

        :rtype: string or None
        :returns: the namespace assigned to this query
        """
        return self._namespace or self._client.namespace

    @namespace.setter
    def namespace(self, value):
        """Update the query's namespace.

        :type value: string
        """
        if not isinstance(value, str):
            raise ValueError("Namespace must be a string")
        self._namespace = value

    @property
    def kind(self):
        """Get the Kind of the Query.

        :rtype: string
        """
        return self._kind

    @kind.setter
    def kind(self, value):
        """Update the Kind of the Query.

        :type value: string
        :param value: updated kind for the query.

        .. note::

           The protobuf specification allows for ``kind`` to be repeated,
           but the current implementation returns an error if more than
           one value is passed.  If the back-end changes in the future to
           allow multiple values, this method will be updated to allow passing
           either a string or a sequence of strings.
        """
        if not isinstance(value, str):
            raise TypeError("Kind must be a string")
        self._kind = value

    @property
    def ancestor(self):
        """The ancestor key for the query.

        :rtype: Key or None
        """
        return self._ancestor

    @ancestor.setter
    def ancestor(self, value):
        """Set the ancestor for the query

        :type value: Key
        :param value: the new ancestor key
        """
        if not isinstance(value, Key):
            raise TypeError("Ancestor must be a Key")
        self._ancestor = value

    @ancestor.deleter
    def ancestor(self):
        """Remove the ancestor for the query."""
        self._ancestor = None

    @property
    def filters(self):
        """Filters set on the query.

        :rtype: sequence of (property_name, operator, value) tuples.
        """
        return self._filters[:]

    def add_filter(self, property_name, operator, value):
        """Filter the query based on a property name, operator and a value.

        Expressions take the form of::

          .add_filter('<property>', '<operator>', <value>)

        where property is a property stored on the entity in the datastore
        and operator is one of ``OPERATORS``
        (ie, ``=``, ``<``, ``<=``, ``>``, ``>=``)::

          >>> from gcloud import datastore
          >>> client = datastore.Client()
          >>> query = client.query(kind='Person')
          >>> query.add_filter('name', '=', 'James')
          >>> query.add_filter('age', '>', 50)

        :type property_name: string
        :param property_name: A property name.

        :type operator: string
        :param operator: One of ``=``, ``<``, ``<=``, ``>``, ``>=``.

        :type value: :class:`int`, :class:`str`, :class:`bool`,
                     :class:`float`, :class:`NoneType`,
                     :class:`datetime.datetime`,
                     :class:`gcloud.datastore.key.Key`
        :param value: The value to filter on.

        :raises: :class:`ValueError` if ``operation`` is not one of the
                 specified values, or if a filter names ``'__key__'`` but
                 passes an invalid value (a key is required).
        """
        if self.OPERATORS.get(operator) is None:
            error_message = 'Invalid expression: "%s"' % (operator,)
            choices_message = 'Please use one of: =, <, <=, >, >=.'
            raise ValueError(error_message, choices_message)

        if property_name == '__key__' and not isinstance(value, Key):
            raise ValueError('Invalid key: "%s"' % value)

        self._filters.append((property_name, operator, value))

    @property
    def projection(self):
        """Fields names returned by the query.

        :rtype: sequence of string
        :returns: Names of fields in query results.
        """
        return self._projection[:]

    @projection.setter
    def projection(self, projection):
        """Set the fields returned the query.

        :type projection: string or sequence of strings
        :param projection: Each value is a string giving the name of a
                           property to be included in the projection query.
        """
        if isinstance(projection, str):
            projection = [projection]
        self._projection[:] = projection

    def keys_only(self):
        """Set the projection to include only keys."""
        self._projection[:] = ['__key__']

    def key_filter(self, key, operator='='):
        """Filter on a key.

        :type key: :class:`gcloud.datastore.key.Key`
        :param key: The key to filter on.

        :type operator: string
        :param operator: (Optional) One of ``=``, ``<``, ``<=``, ``>``, ``>=``.
                         Defaults to ``=``.
        """
        self.add_filter('__key__', operator, key)

    @property
    def order(self):
        """Names of fields used to sort query results.

        :rtype: sequence of string
        """
        return self._order[:]

    @order.setter
    def order(self, value):
        """Set the fields used to sort query results.

        Sort fields will be applied in the order specified.

        :type value: string or sequence of strings
        :param value: Each value is a string giving the name of the
                      property on which to sort, optionally preceded by a
                      hyphen (-) to specify descending order.
                      Omitting the hyphen implies ascending order.
        """
        if isinstance(value, str):
            value = [value]
        self._order[:] = value

    @property
    def distinct_on(self):
        """Names of fields used to group query results.

        :rtype: sequence of string
        """
        return self._distinct_on[:]

    @distinct_on.setter
    def distinct_on(self, value):
        """Set fields used to group query results.

        :type value: string or sequence of strings
        :param value: Each value is a string giving the name of a
                      property to use to group results together.
        """
        if isinstance(value, str):
            value = [value]
        self._distinct_on[:] = value

    def fetch(self, limit=None, offset=0, start_cursor=None, end_cursor=None,
              client=None):
        """Execute the Query; return an iterator for the matching entities.

        For example::

          >>> from gcloud import datastore
          >>> client = datastore.Client()
          >>> query = client.query(kind='Person')
          >>> query.add_filter('name', '=', 'Sally')
          >>> list(query.fetch())
          [<Entity object>, <Entity object>, ...]
          >>> list(query.fetch(1))
          [<Entity object>]

        :type limit: integer or None
        :param limit: An optional limit passed through to the iterator.

        :type offset: integer
        :param offset: An optional offset passed through to the iterator.

        :type start_cursor: bytes
        :param start_cursor: An optional cursor passed through to the iterator.

        :type end_cursor: bytes
        :param end_cursor: An optional cursor passed through to the iterator.

        :type client: :class:`gcloud.datastore.client.Client`
        :param client: client used to connect to datastore.
                       If not supplied, uses the query's value.

        :rtype: :class:`Iterator`
        :raises: ValueError if ``connection`` is not passed and no implicit
                 default has been set.
        """
        if client is None:
            client = self._client

        return Iterator(
            self, client, limit, offset, start_cursor, end_cursor)


class Iterator(object):
    """Represent the state of a given execution of a Query.

    :type query: :class:`gcloud.datastore.query.Query`
    :param query: Query object holding permanent configuration (i.e.
                  things that don't change on with each page in
                  a results set).

    :type client: :class:`gcloud.datastore.client.Client`
    :param client: The client used to make a request.

    :type limit: integer
    :param limit: (Optional) Limit the number of results returned.

    :type offset: integer
    :param offset: (Optional) Offset used to begin a query.

    :type start_cursor: bytes
    :param start_cursor: (Optional) Cursor to begin paging through
                         query results.

    :type end_cursor: bytes
    :param end_cursor: (Optional) Cursor to end paging through
                       query results.
    """

    _NOT_FINISHED = _query_pb2.QueryResultBatch.NOT_FINISHED

    _FINISHED = (
        _query_pb2.QueryResultBatch.NO_MORE_RESULTS,
        _query_pb2.QueryResultBatch.MORE_RESULTS_AFTER_LIMIT,
        _query_pb2.QueryResultBatch.MORE_RESULTS_AFTER_CURSOR,
    )

    def __init__(self, query, client, limit=None, offset=None,
                 start_cursor=None, end_cursor=None):
        self._query = query
        self._client = client
        self._limit = limit
        self._offset = offset
        self._start_cursor = start_cursor
        self._end_cursor = end_cursor
        self._page = self._more_results = None
        self._skipped_results = None

    def next_page(self):
        """Fetch a single "page" of query results.

        Low-level API for fine control:  the more convenient API is
        to iterate on the current Iterator.

        :rtype: tuple, (entities, more_results, cursor)
        """
        pb = _pb_from_query(self._query)

        start_cursor = self._start_cursor
        if start_cursor is not None:
            pb.start_cursor = base64.urlsafe_b64decode(start_cursor)

        end_cursor = self._end_cursor
        if end_cursor is not None:
            pb.end_cursor = base64.urlsafe_b64decode(end_cursor)

        if self._limit is not None:
            pb.limit.value = self._limit

        if self._offset is not None:
            pb.offset = self._offset

        transaction = self._client.current_transaction

        query_results = self._client.connection.run_query(
            query_pb=pb,
            project=self._query.project,
            namespace=self._query.namespace,
            transaction_id=transaction and transaction.id,
            )
        (entity_pbs, cursor_as_bytes,
         more_results_enum, self._skipped_results) = query_results

        if cursor_as_bytes == b'':
            self._start_cursor = None
        else:
            self._start_cursor = base64.urlsafe_b64encode(cursor_as_bytes)
        self._end_cursor = None

        if more_results_enum == self._NOT_FINISHED:
            self._more_results = True
        elif more_results_enum in self._FINISHED:
            self._more_results = False
        else:
            raise ValueError('Unexpected value returned for `more_results`.')

        self._page = [
            helpers.entity_from_protobuf(entity)
            for entity in entity_pbs]
        return self._page, self._more_results, self._start_cursor

    def __iter__(self):
        """Generator yielding all results matching our query.

        :rtype: sequence of :class:`gcloud.datastore.entity.Entity`
        """
        while True:
            self.next_page()
            for entity in self._page:
                yield entity
            if not self._more_results:
                break
            num_results = len(self._page)
            if self._limit is not None:
                self._limit -= num_results
            if self._offset is not None and self._skipped_results is not None:
                # NOTE: The offset goes down relative to the location
                #       because we are updating the cursor each time.
                self._offset -= self._skipped_results


def _pb_from_query(query):
    """Convert a Query instance to the corresponding protobuf.

    :type query: :class:`Query`
    :param query: The source query.

    :rtype: :class:`gcloud.datastore._generated.query_pb2.Query`
    :returns: A protobuf that can be sent to the protobuf API.  N.b. that
              it does not contain "in-flight" fields for ongoing query
              executions (cursors, offset, limit).
    """
    pb = _query_pb2.Query()

    for projection_name in query.projection:
        pb.projection.add().property.name = projection_name

    if query.kind:
        pb.kind.add().name = query.kind

    composite_filter = pb.filter.composite_filter
    composite_filter.op = _query_pb2.CompositeFilter.AND

    if query.ancestor:
        ancestor_pb = query.ancestor.to_protobuf()

        # Filter on __key__ HAS_ANCESTOR == ancestor.
        ancestor_filter = composite_filter.filters.add().property_filter
        ancestor_filter.property.name = '__key__'
        ancestor_filter.op = _query_pb2.PropertyFilter.HAS_ANCESTOR
        ancestor_filter.value.key_value.CopyFrom(ancestor_pb)

    for property_name, operator, value in query.filters:
        pb_op_enum = query.OPERATORS.get(operator)

        # Add the specific filter
        property_filter = composite_filter.filters.add().property_filter
        property_filter.property.name = property_name
        property_filter.op = pb_op_enum

        # Set the value to filter on based on the type.
        if property_name == '__key__':
            key_pb = value.to_protobuf()
            property_filter.value.key_value.CopyFrom(key_pb)
        else:
            helpers._set_protobuf_value(property_filter.value, value)

    if not composite_filter.filters:
        pb.ClearField('filter')

    for prop in query.order:
        property_order = pb.order.add()

        if prop.startswith('-'):
            property_order.property.name = prop[1:]
            property_order.direction = property_order.DESCENDING
        else:
            property_order.property.name = prop
            property_order.direction = property_order.ASCENDING

    for distinct_on_name in query.distinct_on:
        pb.distinct_on.add().name = distinct_on_name

    return pb
