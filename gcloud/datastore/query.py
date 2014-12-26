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

from gcloud.datastore import datastore_v1_pb2 as datastore_pb
from gcloud.datastore import helpers
from gcloud.datastore.key import Key


class Query(object):
    """A Query against the Cloud Datastore.

    This class serves as an abstraction for creating a query over data
    stored in the Cloud Datastore.

    Each :class:`Query` object is immutable, and a clone is returned
    whenever any part of the query is modified::

      >>> query = Query('MyKind')
      >>> limited_query = query.limit(10)
      >>> query.limit() == 10
      False
      >>> limited_query.limit() == 10
      True

    You typically won't construct a :class:`Query` by initializing it
    like ``Query('MyKind', dataset=...)`` but instead use the helper
    :func:`gcloud.datastore.dataset.Dataset.query` method which
    generates a query that can be executed without any additional work::

      >>> from gcloud import datastore
      >>> dataset = datastore.get_dataset('dataset-id')
      >>> query = dataset.query('MyKind')

    :type kind: string
    :param kind: The kind to query.

    :type dataset: :class:`gcloud.datastore.dataset.Dataset`
    :param dataset: The dataset to query.

    :type namespace: string or None
    :param dataset: The namespace to which to restrict results.
    """

    _NOT_FINISHED = datastore_pb.QueryResultBatch.NOT_FINISHED
    _FINISHED = (
        datastore_pb.QueryResultBatch.NO_MORE_RESULTS,
        datastore_pb.QueryResultBatch.MORE_RESULTS_AFTER_LIMIT,
    )
    OPERATORS = {
        '<=': datastore_pb.PropertyFilter.LESS_THAN_OR_EQUAL,
        '>=': datastore_pb.PropertyFilter.GREATER_THAN_OR_EQUAL,
        '<': datastore_pb.PropertyFilter.LESS_THAN,
        '>': datastore_pb.PropertyFilter.GREATER_THAN,
        '=': datastore_pb.PropertyFilter.EQUAL,
    }
    """Mapping of operator strings and their protobuf equivalents."""

    def __init__(self, kind=None, dataset=None, namespace=None):
        self._dataset = dataset
        self._namespace = namespace
        self._pb = datastore_pb.Query()
        self._offset = 0

        if kind:
            self._pb.kind.add().name = kind

    def _clone(self):
        """Create a new Query, copying self.

        :rtype: :class:`gcloud.datastore.query.Query`
        :returns: a copy of 'self'.
        """
        clone = self.__class__(dataset=self._dataset,
                               namespace=self._namespace)
        clone._pb.CopyFrom(self._pb)
        return clone

    def namespace(self):
        """This query's namespace

        :rtype: string or None
        :returns: the namespace assigned to this query
        """
        return self._namespace

    def to_protobuf(self):
        """Convert :class:`Query` instance to :class:`.datastore_v1_pb2.Query`.

        :rtype: :class:`gcloud.datastore.datastore_v1_pb2.Query`
        :returns: A Query protobuf that can be sent to the protobuf API.
        """
        return self._pb

    def filter(self, property_name, operator, value):
        """Filter the query based on a property name, operator and a value.

        This will return a clone of the current :class:`Query`
        filtered by the expression and value provided.

        Expressions take the form of::

          .filter('<property>', '<operator>', <value>)

        where property is a property stored on the entity in the datastore
        and operator is one of ``OPERATORS``
        (ie, ``=``, ``<``, ``<=``, ``>``, ``>=``)::

          >>> query = Query('Person')
          >>> filtered_query = query.filter('name', '=', 'James')
          >>> filtered_query = query.filter('age', '>', 50)

        Because each call to ``.filter()`` returns a cloned ``Query`` object
        we are able to string these together::

          >>> query = Query('Person').filter(
          ...     'name', '=', 'James').filter('age', '>', 50)

        :type property_name: string
        :param property_name: A property name.

        :type operator: string
        :param operator: One of ``=``, ``<``, ``<=``, ``>``, ``>=``.

        :type value: integer, string, boolean, float, None, datetime
        :param value: The value to filter on.

        :rtype: :class:`Query`
        :returns: A Query filtered by the expression and value provided.
        :raises: `ValueError` if `operation` is not one of the specified
                 values.
        """
        clone = self._clone()

        pb_op_enum = self.OPERATORS.get(operator)
        if pb_op_enum is None:
            error_message = 'Invalid expression: "%s"' % (operator,)
            choices_message = 'Please use one of: =, <, <=, >, >=.'
            raise ValueError(error_message, choices_message)

        # Build a composite filter AND'd together.
        composite_filter = clone._pb.filter.composite_filter
        composite_filter.operator = datastore_pb.CompositeFilter.AND

        # Add the specific filter
        property_filter = composite_filter.filter.add().property_filter
        property_filter.property.name = property_name
        property_filter.operator = pb_op_enum

        # Set the value to filter on based on the type.
        helpers._set_protobuf_value(property_filter.value, value)
        return clone

    def ancestor(self, ancestor):
        """Filter the query based on an ancestor.

        This will return a clone of the current :class:`Query` filtered
        by the ancestor provided.  For example::

          >>> parent_key = Key.from_path('Person', '1')
          >>> query = dataset.query('Person')
          >>> filtered_query = query.ancestor(parent_key)

        If you don't have a :class:`gcloud.datastore.key.Key` but just
        know the path, you can provide that as well::

          >>> query = dataset.query('Person')
          >>> filtered_query = query.ancestor(['Person', '1'])

        Each call to ``.ancestor()`` returns a cloned :class:`Query`,
        however a query may only have one ancestor at a time.

        :type ancestor: :class:`gcloud.datastore.key.Key` or list
        :param ancestor: Either a Key or a path of the form
                         ``['Kind', 'id or name', 'Kind', 'id or name', ...]``.

        :rtype: :class:`Query`
        :returns: A Query filtered by the ancestor provided.
        """

        clone = self._clone()

        # If an ancestor filter already exists, remove it.
        for i, filter in enumerate(clone._pb.filter.composite_filter.filter):
            property_filter = filter.property_filter
            if (property_filter.operator ==
                    datastore_pb.PropertyFilter.HAS_ANCESTOR):
                del clone._pb.filter.composite_filter.filter[i]

                # If we just deleted the last item, make sure to clear out the
                # filter property all together.
                if not clone._pb.filter.composite_filter.filter:
                    clone._pb.ClearField('filter')

        # If the ancestor is None, just return (we already removed the filter).
        if not ancestor:
            return clone

        # If a list was provided, turn it into a Key.
        if isinstance(ancestor, list):
            ancestor = Key.from_path(*ancestor)

        # If we don't have a Key value by now, something is wrong.
        if not isinstance(ancestor, Key):
            raise TypeError('Expected list or Key, got %s.' % type(ancestor))

        # Get the composite filter and add a new property filter.
        composite_filter = clone._pb.filter.composite_filter
        composite_filter.operator = datastore_pb.CompositeFilter.AND

        # Filter on __key__ HAS_ANCESTOR == ancestor.
        ancestor_filter = composite_filter.filter.add().property_filter
        ancestor_filter.property.name = '__key__'
        ancestor_filter.operator = datastore_pb.PropertyFilter.HAS_ANCESTOR
        ancestor_filter.value.key_value.CopyFrom(ancestor.to_protobuf())

        return clone

    def kind(self, kind=None):
        """Get or set the Kind of the Query.

        :type kind: string
        :param kind: Optional. The entity kinds for which to query.

        :rtype: string or :class:`Query`
        :returns: If `kind` is None, returns the kind. If a kind is provided,
                  returns a clone of the :class:`Query` with that kind set.
        :raises: `ValueError` from the getter if multiple kinds are set on
                 the query.
        """
        if kind is not None:
            kinds = [kind]
            clone = self._clone()
            clone._pb.ClearField('kind')
            for new_kind in kinds:
                clone._pb.kind.add().name = new_kind
            return clone
        else:
            # In the proto definition for Query, `kind` is repeated.
            kind_names = [kind_expr.name for kind_expr in self._pb.kind]
            num_kinds = len(kind_names)
            if num_kinds == 1:
                return kind_names[0]
            elif num_kinds > 1:
                raise ValueError('Only a single kind can be set.')

    def limit(self, limit=None):
        """Get or set the limit of the Query.

        This is the maximum number of rows (Entities) to return for this
        Query.

        This is a hybrid getter / setter, used as::

          >>> query = Query('Person')
          >>> query = query.limit(100)  # Set the limit to 100 rows.
          >>> query.limit()  # Get the limit for this query.
          100

        :rtype: integer, None, or :class:`Query`
        :returns: If no arguments, returns the current limit.
                  If a limit is provided, returns a clone of the :class:`Query`
                  with that limit set.
        """
        if limit:
            clone = self._clone()
            clone._pb.limit = limit
            return clone
        else:
            return self._pb.limit

    def dataset(self, dataset=None):
        """Get or set the :class:`.datastore.dataset.Dataset` for this Query.

        This is the dataset against which the Query will be run.

        This is a hybrid getter / setter, used as::

          >>> query = Query('Person')
          >>> query = query.dataset(my_dataset)  # Set the dataset.
          >>> query.dataset()  # Get the current dataset.
          <Dataset object>

        :rtype: :class:`gcloud.datastore.dataset.Dataset`, None,
                or :class:`Query`
        :returns: If no arguments, returns the current dataset.
                  If a dataset is provided, returns a clone of the
                  :class:`Query` with that dataset set.
        """
        if dataset:
            clone = self._clone()
            clone._dataset = dataset
            return clone
        else:
            return self._dataset

    def fetch_page(self, limit=None):
        """Executes the Query and returns matching entities, and paging info.

        In addition to the fetched entities, it also returns a cursor to allow
        paging through a results set and a boolean `more_results` indicating
        if there are any more.

        This makes an API call to the Cloud Datastore, sends the Query
        as a protobuf, parses the responses to Entity protobufs, and
        then converts them to :class:`gcloud.datastore.entity.Entity`
        objects.

        For example::

          >>> from gcloud import datastore
          >>> dataset = datastore.get_dataset('dataset-id')
          >>> query = dataset.query('Person').filter('name', '=', 'Sally')
          >>> query.fetch_page()
          [<Entity object>, <Entity object>, ...], 'cursorbase64', True
          >>> query.fetch_page(1)
          [<Entity object>], 'cursorbase64', True
          >>> query.limit()
          None

        :type limit: integer
        :param limit: An optional limit to apply temporarily to this query.
                      That is, the Query itself won't be altered,
                      but the limit will be applied to the query
                      before it is executed.

        :rtype: tuple of mixed types
        :returns: The first entry is a :class:`gcloud.datastore.entity.Entity`
                  list matching this query's criteria. The second is a base64
                  encoded cursor for paging and the third is a boolean
                  indicating if there are more results.
        :raises: `ValueError` if more_results is not one of the enums
                 NOT_FINISHED, MORE_RESULTS_AFTER_LIMIT, NO_MORE_RESULTS.
        """
        clone = self

        if limit:
            clone = self.limit(limit)

        query_results = self.dataset().connection().run_query(
            query_pb=clone.to_protobuf(),
            dataset_id=self.dataset().id(),
            namespace=self._namespace,
            )
        # NOTE: `query_results` contains an extra value that we don't use,
        #       namely `skipped_results`.
        #
        # NOTE: The value of `more_results` is not currently useful because
        #       the back-end always returns an enum
        #       value of MORE_RESULTS_AFTER_LIMIT even if there are no more
        #       results. See
        #       https://github.com/GoogleCloudPlatform/gcloud-python/issues/280
        #       for discussion.
        entity_pbs, cursor_as_bytes, more_results_enum = query_results[:3]

        entities = [helpers.entity_from_protobuf(entity,
                                                 dataset=self.dataset())
                    for entity in entity_pbs]

        cursor = base64.b64encode(cursor_as_bytes)

        if more_results_enum == self._NOT_FINISHED:
            more_results = True
        elif more_results_enum in self._FINISHED:
            more_results = False
        else:
            raise ValueError('Unexpected value returned for `more_results`.')

        return entities, cursor, more_results

    def fetch(self, limit=None):
        """Executes the Query and returns matching entities

        This calls `fetch_page()` but does not use the paging information.

        For example::

          >>> from gcloud import datastore
          >>> dataset = datastore.get_dataset('dataset-id')
          >>> query = dataset.query('Person').filter('name', '=', 'Sally')
          >>> query.fetch()
          [<Entity object>, <Entity object>, ...]
          >>> query.fetch(1)
          [<Entity object>]
          >>> query.limit()
          None

        :type limit: integer
        :param limit: An optional limit to apply temporarily to this query.
                      That is, the Query itself won't be altered,
                      but the limit will be applied to the query
                      before it is executed.

        :rtype: list of :class:`gcloud.datastore.entity.Entity`'s
        :returns: The list of entities matching this query's criteria.
        """
        entities, _, _ = self.fetch_page(limit=limit)
        return entities

    @property
    def start_cursor(self):
        """Property to encode start cursor bytes as base64."""
        if not self._pb.HasField('start_cursor'):
            return None

        start_as_bytes = self._pb.start_cursor
        return base64.b64encode(start_as_bytes)

    @property
    def end_cursor(self):
        """Property to encode end cursor bytes as base64."""
        if not self._pb.HasField('end_cursor'):
            return None

        end_as_bytes = self._pb.end_cursor
        return base64.b64encode(end_as_bytes)

    def with_cursor(self, start_cursor, end_cursor=None):
        """Specifies the starting / ending positions in a query's result set.

        :type start_cursor: bytes
        :param start_cursor: Base64-encoded cursor string specifying where to
                             start reading query results.

        :type end_cursor: bytes
        :param end_cursor: Base64-encoded cursor string specifying where to
                           stop reading query results.

        :rtype: :class:`Query`
        :returns: If neither cursor is passed, returns self;  else, returns a
                  clone of the :class:`Query`, with cursors updated.
        """
        clone = self
        if start_cursor or end_cursor:
            clone = self._clone()
        if start_cursor:
            clone._pb.start_cursor = base64.b64decode(start_cursor)
        if end_cursor:
            clone._pb.end_cursor = base64.b64decode(end_cursor)
        return clone

    def order(self, *properties):
        """Adds a sort order to the query.

        Sort fields will be applied in the order specified.

        :type properties: sequence of strings
        :param properties: Each value is a string giving the name of the
                           property on which to sort, optionally preceded by a
                           hyphen (-) to specify descending order.
                           Omitting the hyphen implies ascending order.

        :rtype: :class:`Query`
        :returns: A new Query instance, ordered as specified.
        """
        clone = self._clone()

        for prop in properties:
            property_order = clone._pb.order.add()

            if prop.startswith('-'):
                property_order.property.name = prop[1:]
                property_order.direction = property_order.DESCENDING
            else:
                property_order.property.name = prop
                property_order.direction = property_order.ASCENDING

        return clone

    def projection(self, projection=None):
        """Adds a projection to the query.

        This is a hybrid getter / setter, used as::

          >>> query = Query('Person')
          >>> query.projection()  # Get the projection for this query.
          []
          >>> query = query.projection(['name'])
          >>> query.projection()  # Get the projection for this query.
          ['name']

        :type projection: sequence of strings
        :param projection: Each value is a string giving the name of a
                           property to be included in the projection query.

        :rtype: :class:`Query` or `list` of strings.
        :returns: If no arguments, returns the current projection.
                  If a projection is provided, returns a clone of the
                  :class:`Query` with that projection set.
        """
        if projection is None:
            return [prop_expr.property.name
                    for prop_expr in self._pb.projection]

        clone = self._clone()

        # Reset projection values to empty.
        clone._pb.ClearField('projection')

        # Add each name to list of projections.
        for projection_name in projection:
            clone._pb.projection.add().property.name = projection_name
        return clone

    def keys(self):
        """Adds a projection to get keys only

        :rtype: :class:`Query`
        :returns: A new Query instance only returns entity keys
        """
        return self.projection(['__key__'])

    def offset(self, offset=None):
        """Adds offset to the query to allow pagination.

        NOTE: Paging with cursors should be preferred to using an offset.

        This is a hybrid getter / setter, used as::

          >>> query = Query('Person')
          >>> query.offset()  # Get the offset for this query.
          0
          >>> query = query.offset(10)
          >>> query.offset()  # Get the offset for this query.
          10

        :type offset: non-negative integer.
        :param offset: Value representing where to start a query for
                       a given kind.

        :rtype: :class:`Query` or `int`.
        :returns: If no arguments, returns the current offset.
                  If an offset is provided, returns a clone of the
                  :class:`Query` with that offset set.
        """
        if offset is None:
            return self._offset

        clone = self._clone()
        clone._offset = offset
        clone._pb.offset = offset
        return clone

    def group_by(self, group_by=None):
        """Adds a group_by to the query.

        This is a hybrid getter / setter, used as::

          >>> query = Query('Person')
          >>> query.group_by()  # Get the group_by for this query.
          []
          >>> query = query.group_by(['name'])
          >>> query.group_by()  # Get the group_by for this query.
          ['name']

        :type group_by: sequence of strings
        :param group_by: Each value is a string giving the name of a
                         property to use to group results together.

        :rtype: :class:`Query` or `list` of strings.
        :returns: If no arguments, returns the current group_by.
                  If a list of group by properties is provided, returns a clone
                  of the :class:`Query` with that list of values set.
        """
        if group_by is None:
            return [prop_ref.name for prop_ref in self._pb.group_by]

        clone = self._clone()

        # Reset group_by values to empty.
        clone._pb.ClearField('group_by')

        # Add each name to list of group_bys.
        for group_by_name in group_by:
            clone._pb.group_by.add().name = group_by_name
        return clone
