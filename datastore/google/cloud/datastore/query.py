# Copyright 2014 Google LLC
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

"""Create / interact with Google Cloud Datastore queries."""

import base64

from google.api_core import page_iterator
from google.cloud._helpers import _ensure_tuple_or_list

from google.cloud.datastore_v1.proto import entity_pb2
from google.cloud.datastore_v1.proto import query_pb2
from google.cloud.datastore import helpers
from google.cloud.datastore.key import Key


_NOT_FINISHED = query_pb2.QueryResultBatch.NOT_FINISHED
_NO_MORE_RESULTS = query_pb2.QueryResultBatch.NO_MORE_RESULTS

_FINISHED = (
    _NO_MORE_RESULTS,
    query_pb2.QueryResultBatch.MORE_RESULTS_AFTER_LIMIT,
    query_pb2.QueryResultBatch.MORE_RESULTS_AFTER_CURSOR,
)


class Query(object):
    """A Query against the Cloud Datastore.

    This class serves as an abstraction for creating a query over data
    stored in the Cloud Datastore.

    :type client: :class:`google.cloud.datastore.client.Client`
    :param client: The client used to connect to Datastore.

    :type kind: str
    :param kind: The kind to query.

    :type project: str
    :param project:
        (Optional) The project associated with the query.  If not passed, uses
        the client's value.

    :type namespace: str
    :param namespace:
        (Optional) The namespace to which to restrict results.  If not passed,
        uses the client's value.

    :type ancestor: :class:`~google.cloud.datastore.key.Key`
    :param ancestor:
        (Optional) key of the ancestor to which this query's results are
        restricted.

    :type filters: tuple[str, str, str]
    :param filters: Property filters applied by this query. The sequence
        is ``(property_name, operator, value)``.

    :type projection: sequence of string
    :param projection:  fields returned as part of query results.

    :type order: sequence of string
    :param order:  field names used to order query results. Prepend ``-``
                   to a field name to sort it in descending order.

    :type distinct_on: sequence of string
    :param distinct_on: field names used to group query results.

    :raises: ValueError if ``project`` is not passed and no implicit
             default is set.
    """

    OPERATORS = {
        '<=': query_pb2.PropertyFilter.LESS_THAN_OR_EQUAL,
        '>=': query_pb2.PropertyFilter.GREATER_THAN_OR_EQUAL,
        '<': query_pb2.PropertyFilter.LESS_THAN,
        '>': query_pb2.PropertyFilter.GREATER_THAN,
        '=': query_pb2.PropertyFilter.EQUAL,
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
        :returns: The project for the query.
        """
        return self._project or self._client.project

    @property
    def namespace(self):
        """This query's namespace

        :rtype: str or None
        :returns: the namespace assigned to this query
        """
        return self._namespace or self._client.namespace

    @namespace.setter
    def namespace(self, value):
        """Update the query's namespace.

        :type value: str
        """
        if not isinstance(value, str):
            raise ValueError("Namespace must be a string")
        self._namespace = value

    @property
    def kind(self):
        """Get the Kind of the Query.

        :rtype: str
        :returns: The kind for the query.
        """
        return self._kind

    @kind.setter
    def kind(self, value):
        """Update the Kind of the Query.

        :type value: str
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

        :rtype: :class:`~google.cloud.datastore.key.Key` or None
        :returns: The ancestor for the query.
        """
        return self._ancestor

    @ancestor.setter
    def ancestor(self, value):
        """Set the ancestor for the query

        :type value: :class:`~google.cloud.datastore.key.Key`
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

        :rtype: tuple[str, str, str]
        :returns: The filters set on the query. The sequence is
            ``(property_name, operator, value)``.
        """
        return self._filters[:]

    def add_filter(self, property_name, operator, value):
        """Filter the query based on a property name, operator and a value.

        Expressions take the form of::

          .add_filter('<property>', '<operator>', <value>)

        where property is a property stored on the entity in the datastore
        and operator is one of ``OPERATORS``
        (ie, ``=``, ``<``, ``<=``, ``>``, ``>=``)::

          >>> from google.cloud import datastore
          >>> client = datastore.Client()
          >>> query = client.query(kind='Person')
          >>> query.add_filter('name', '=', 'James')
          >>> query.add_filter('age', '>', 50)

        :type property_name: str
        :param property_name: A property name.

        :type operator: str
        :param operator: One of ``=``, ``<``, ``<=``, ``>``, ``>=``.

        :type value: :class:`int`, :class:`str`, :class:`bool`,
                     :class:`float`, :class:`NoneType`,
                     :class:`datetime.datetime`,
                     :class:`google.cloud.datastore.key.Key`
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

        :type projection: str or sequence of strings
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

        :type key: :class:`google.cloud.datastore.key.Key`
        :param key: The key to filter on.

        :type operator: str
        :param operator: (Optional) One of ``=``, ``<``, ``<=``, ``>``, ``>=``.
                         Defaults to ``=``.
        """
        self.add_filter('__key__', operator, key)

    @property
    def order(self):
        """Names of fields used to sort query results.

        :rtype: sequence of string
        :returns: The order(s) set on the query.
        """
        return self._order[:]

    @order.setter
    def order(self, value):
        """Set the fields used to sort query results.

        Sort fields will be applied in the order specified.

        :type value: str or sequence of strings
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
        :returns: The "distinct on" fields set on the query.
        """
        return self._distinct_on[:]

    @distinct_on.setter
    def distinct_on(self, value):
        """Set fields used to group query results.

        :type value: str or sequence of strings
        :param value: Each value is a string giving the name of a
                      property to use to group results together.
        """
        if isinstance(value, str):
            value = [value]
        self._distinct_on[:] = value

    def fetch(self, limit=None, offset=0, start_cursor=None, end_cursor=None,
              client=None, eventual=False):
        """Execute the Query; return an iterator for the matching entities.

        For example::

          >>> from google.cloud import datastore
          >>> client = datastore.Client()
          >>> query = client.query(kind='Person')
          >>> query.add_filter('name', '=', 'Sally')
          >>> list(query.fetch())
          [<Entity object>, <Entity object>, ...]
          >>> list(query.fetch(1))
          [<Entity object>]

        :type limit: int
        :param limit: (Optional) limit passed through to the iterator.

        :type offset: int
        :param offset: (Optional) offset passed through to the iterator.

        :type start_cursor: bytes
        :param start_cursor: (Optional) cursor passed through to the iterator.

        :type end_cursor: bytes
        :param end_cursor: (Optional) cursor passed through to the iterator.

        :type client: :class:`google.cloud.datastore.client.Client`
        :param client: (Optional) client used to connect to datastore.
                       If not supplied, uses the query's value.

        :type eventual: bool
        :param eventual: (Optional) Defaults to strongly consistent (False).
                                    Setting True will use eventual consistency,
                                    but cannot be used inside a transaction or
                                    will raise ValueError.

        :rtype: :class:`Iterator`
        :returns: The iterator for the query.
        """
        if client is None:
            client = self._client

        return Iterator(self,
                        client,
                        limit=limit,
                        offset=offset,
                        start_cursor=start_cursor,
                        end_cursor=end_cursor,
                        eventual=eventual)


class Iterator(page_iterator.Iterator):
    """Represent the state of a given execution of a Query.

    :type query: :class:`~google.cloud.datastore.query.Query`
    :param query: Query object holding permanent configuration (i.e.
                  things that don't change on with each page in
                  a results set).

    :type client: :class:`~google.cloud.datastore.client.Client`
    :param client: The client used to make a request.

    :type limit: int
    :param limit: (Optional) Limit the number of results returned.

    :type offset: int
    :param offset: (Optional) Offset used to begin a query.

    :type start_cursor: bytes
    :param start_cursor: (Optional) Cursor to begin paging through
                         query results.

    :type end_cursor: bytes
    :param end_cursor: (Optional) Cursor to end paging through
                       query results.

    :type eventual: bool
    :param eventual: (Optional) Defaults to strongly consistent (False).
                                Setting True will use eventual consistency,
                                but cannot be used inside a transaction or
                                will raise ValueError.
    """

    next_page_token = None

    def __init__(self, query, client, limit=None, offset=None,
                 start_cursor=None, end_cursor=None, eventual=False):
        super(Iterator, self).__init__(
            client=client, item_to_value=_item_to_entity,
            page_token=start_cursor, max_results=limit)
        self._query = query
        self._offset = offset
        self._end_cursor = end_cursor
        self._eventual = eventual
        # The attributes below will change over the life of the iterator.
        self._more_results = True
        self._skipped_results = 0

    def _build_protobuf(self):
        """Build a query protobuf.

        Relies on the current state of the iterator.

        :rtype:
            :class:`.query_pb2.Query`
        :returns: The query protobuf object for the current
                  state of the iterator.
        """
        pb = _pb_from_query(self._query)

        start_cursor = self.next_page_token
        if start_cursor is not None:
            pb.start_cursor = base64.urlsafe_b64decode(start_cursor)

        end_cursor = self._end_cursor
        if end_cursor is not None:
            pb.end_cursor = base64.urlsafe_b64decode(end_cursor)

        if self.max_results is not None:
            pb.limit.value = self.max_results - self.num_results

        if self._offset is not None:
            # NOTE: The offset goes down relative to the location
            #       because we are updating the cursor each time.
            pb.offset = self._offset - self._skipped_results

        return pb

    def _process_query_results(self, response_pb):
        """Process the response from a datastore query.

        :type response_pb: :class:`.datastore_pb2.RunQueryResponse`
        :param response_pb: The protobuf response from a ``runQuery`` request.

        :rtype: iterable
        :returns: The next page of entity results.
        :raises ValueError: If ``more_results`` is an unexpected value.
        """
        self._skipped_results = response_pb.batch.skipped_results

        if response_pb.batch.more_results == _NO_MORE_RESULTS:
            self.next_page_token = None
        else:
            self.next_page_token = base64.urlsafe_b64encode(
                response_pb.batch.end_cursor)
        self._end_cursor = None

        if response_pb.batch.more_results == _NOT_FINISHED:
            self._more_results = True
        elif response_pb.batch.more_results in _FINISHED:
            self._more_results = False
        else:
            raise ValueError('Unexpected value returned for `more_results`.')

        return [result.entity for result in response_pb.batch.entity_results]

    def _next_page(self):
        """Get the next page in the iterator.

        :rtype: :class:`~google.cloud.iterator.Page`
        :returns: The next page in the iterator (or :data:`None` if
                  there are no pages left).
        """
        if not self._more_results:
            return None

        query_pb = self._build_protobuf()
        transaction = self.client.current_transaction
        if transaction is None:
            transaction_id = None
        else:
            transaction_id = transaction.id
        read_options = helpers.get_read_options(self._eventual, transaction_id)

        partition_id = entity_pb2.PartitionId(
            project_id=self._query.project,
            namespace_id=self._query.namespace)
        response_pb = self.client._datastore_api.run_query(
            self._query.project,
            partition_id,
            read_options,
            query=query_pb,
        )
        entity_pbs = self._process_query_results(response_pb)
        return page_iterator.Page(self, entity_pbs, self._item_to_value)


def _pb_from_query(query):
    """Convert a Query instance to the corresponding protobuf.

    :type query: :class:`Query`
    :param query: The source query.

    :rtype: :class:`.query_pb2.Query`
    :returns: A protobuf that can be sent to the protobuf API.  N.b. that
              it does not contain "in-flight" fields for ongoing query
              executions (cursors, offset, limit).
    """
    pb = query_pb2.Query()

    for projection_name in query.projection:
        pb.projection.add().property.name = projection_name

    if query.kind:
        pb.kind.add().name = query.kind

    composite_filter = pb.filter.composite_filter
    composite_filter.op = query_pb2.CompositeFilter.AND

    if query.ancestor:
        ancestor_pb = query.ancestor.to_protobuf()

        # Filter on __key__ HAS_ANCESTOR == ancestor.
        ancestor_filter = composite_filter.filters.add().property_filter
        ancestor_filter.property.name = '__key__'
        ancestor_filter.op = query_pb2.PropertyFilter.HAS_ANCESTOR
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


# pylint: disable=unused-argument
def _item_to_entity(iterator, entity_pb):
    """Convert a raw protobuf entity to the native object.

    :type iterator: :class:`~google.api_core.page_iterator.Iterator`
    :param iterator: The iterator that is currently in use.

    :type entity_pb:
        :class:`.entity_pb2.Entity`
    :param entity_pb: An entity protobuf to convert to a native entity.

    :rtype: :class:`~google.cloud.datastore.entity.Entity`
    :returns: The next entity in the page.
    """
    return helpers.entity_from_protobuf(entity_pb)
# pylint: enable=unused-argument
