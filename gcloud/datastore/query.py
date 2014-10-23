"""Create / interact with gcloud datastore queries."""

import base64

from gcloud.datastore import datastore_v1_pb2 as datastore_pb
from gcloud.datastore import helpers
from gcloud.datastore.key import Key


class Query(object):
    """A Query against the Cloud Datastore.

    This class serves as an abstraction for creating
    a query over data stored in the Cloud Datastore.

    Each :class:`Query` object is immutable,
    and a clone is returned whenever
    any part of the query is modified::

      >>> query = Query('MyKind')
      >>> limited_query = query.limit(10)
      >>> query.limit() == 10
      False
      >>> limited_query.limit() == 10
      True

    You typically won't construct a :class:`Query`
    by initializing it like ``Query('MyKind', dataset=...)``
    but instead use the helper
    :func:`gcloud.datastore.dataset.Dataset.query` method
    which generates a query that can be executed
    without any additional work::

      >>> from gcloud import datastore
      >>> dataset = datastore.get_dataset('dataset-id', email, key_path)
      >>> query = dataset.query('MyKind')

    :type kind: string
    :param kind: The kind to query.

    :type dataset: :class:`gcloud.datastore.dataset.Dataset`
    :param dataset: The dataset to query.

    :type namespace: string or None
    :param dataset: The namespace to which to restrict results.
    """

    OPERATORS = {
        '<': datastore_pb.PropertyFilter.LESS_THAN,
        '<=': datastore_pb.PropertyFilter.LESS_THAN_OR_EQUAL,
        '>': datastore_pb.PropertyFilter.GREATER_THAN,
        '>=': datastore_pb.PropertyFilter.GREATER_THAN_OR_EQUAL,
        '=': datastore_pb.PropertyFilter.EQUAL,
    }
    """Mapping of operator strings and their protobuf equivalents."""

    def __init__(self, kind=None, dataset=None, namespace=None):
        self._dataset = dataset
        self._namespace = namespace
        self._pb = datastore_pb.Query()
        self._cursor = None

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
        clone._cursor = self._cursor
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

    def filter(self, expression, value):
        """Filter the query based on an expression and a value.

        This will return a clone of the current :class:`Query`
        filtered by the expression and value provided.

        Expressions take the form of::

          .filter('<property> <operator>', <value>)

        where property is a property stored on the entity in the datastore
        and operator is one of ``OPERATORS``
        (ie, ``=``, ``<``, ``<=``, ``>``, ``>=``)::

          >>> query = Query('Person')
          >>> filtered_query = query.filter('name =', 'James')
          >>> filtered_query = query.filter('age >', 50)

        Because each call to ``.filter()`` returns a cloned ``Query`` object
        we are able to string these together::

          >>> query = Query('Person').filter(
          ...     'name =', 'James').filter('age >', 50)

        :type expression: string
        :param expression: An expression of a property and an
                           operator (ie, ``=``).

        :type value: integer, string, boolean, float, None, datetime
        :param value: The value to filter on.

        :rtype: :class:`Query`
        :returns: A Query filtered by the expression and value provided.
        """
        clone = self._clone()

        # Take an expression like 'property >=', and parse it into
        # useful pieces.
        property_name, operator = None, None
        expression = expression.strip()

        for operator_string in self.OPERATORS:
            if expression.endswith(operator_string):
                operator = self.OPERATORS[operator_string]
                property_name = expression[0:-len(operator_string)].strip()

        if not operator or not property_name:
            raise ValueError('Invalid expression: "%s"' % expression)

        # Build a composite filter AND'd together.
        composite_filter = clone._pb.filter.composite_filter
        composite_filter.operator = datastore_pb.CompositeFilter.AND

        # Add the specific filter
        property_filter = composite_filter.filter.add().property_filter
        property_filter.property.name = property_name
        property_filter.operator = operator

        # Set the value to filter on based on the type.
        helpers._set_protobuf_value(property_filter.value, value)
        return clone

    def ancestor(self, ancestor):
        """Filter the query based on an ancestor.

        This will return a clone of the current :class:`Query`
        filtered by the ancestor provided.

        For example::

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

    def kind(self, *kinds):
        """Get or set the Kind of the Query.

        .. note::
          This is an **additive** operation.
          That is, if the Query is set for kinds A and B,
          and you call ``.kind('C')``,
          it will query for kinds A, B, *and*, C.

        :type kinds: string
        :param kinds: The entity kinds for which to query.

        :rtype: string or :class:`Query`
        :returns: If no arguments, returns the kind.
                  If a kind is provided, returns a clone of the :class:`Query`
                  with those kinds set.
        """
        if kinds:
            clone = self._clone()
            for kind in kinds:
                clone._pb.kind.add().name = kind
            return clone
        else:
            return self._pb.kind

    def limit(self, limit=None):
        """Get or set the limit of the Query.

        This is the maximum number of rows (Entities) to return for this Query.

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

    def fetch(self, limit=None):
        """Executes the Query and returns all matching entities.

        This makes an API call to the Cloud Datastore, sends the Query as a
        protobuf, parses the responses to Entity protobufs, and then converts
        them to :class:`gcloud.datastore.entity.Entity` objects.

        For example::

          >>> from gcloud import datastore
          >>> dataset = datastore.get_dataset('dataset-id', email, key_path)
          >>> query = dataset.query('Person').filter('name =', 'Sally')
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
        clone = self

        if limit:
            clone = self.limit(limit)

        query_results = self.dataset().connection().run_query(
            query_pb=clone.to_protobuf(),
            dataset_id=self.dataset().id(),
            namespace=self._namespace,
            )
        # NOTE: `query_results` contains two extra values that we don't use,
        #       namely `more_results` and `skipped_results`. The value of
        #       `more_results` is unusable because it always returns an enum
        #       value of MORE_RESULTS_AFTER_LIMIT even if there are no more
        #       results. See
        #       https://github.com/GoogleCloudPlatform/gcloud-python/issues/280
        #       for discussion.
        entity_pbs, end_cursor = query_results[:2]

        self._cursor = end_cursor
        return [helpers.entity_from_protobuf(entity, dataset=self.dataset())
                for entity in entity_pbs]

    def cursor(self):
        """Returns cursor ID

        .. Caution:: Invoking this method on a query that has not yet been
          executed will raise a RuntimeError.

        :rtype: string
        :returns: base64-encoded cursor ID string denoting the last position
                  consumed in the query's result set.
        """
        if not self._cursor:
            raise RuntimeError('No cursor')
        return base64.b64encode(self._cursor)

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
