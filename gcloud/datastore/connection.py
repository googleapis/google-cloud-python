"""Connections to gcloud datastore API servers."""

from gcloud import connection
from gcloud.datastore import datastore_v1_pb2 as datastore_pb
from gcloud.datastore import helpers
from gcloud.datastore.dataset import Dataset


class Connection(connection.Connection):
    """A connection to the Google Cloud Datastore via the Protobuf API.

    This class should understand only the basic types (and protobufs)
    in method arguments, however should be capable of returning advanced types.

    :type credentials: :class:`oauth2client.client.OAuth2Credentials`
    :param credentials: The OAuth2 Credentials to use for this connection.
    """

    API_VERSION = 'v1beta2'
    """The version of the API, used in building the API call's URL."""

    API_URL_TEMPLATE = ('{api_base}/datastore/{api_version}'
                        '/datasets/{dataset_id}/{method}')
    """A template for the URL of a particular API call."""

    def __init__(self, credentials=None):
        super(Connection, self).__init__(credentials=credentials)
        self._current_transaction = None

    def _request(self, dataset_id, method, data):
        """Make a request over the Http transport to the Cloud Datastore API.

        :type dataset_id: string
        :param dataset_id: The ID of the dataset of which to make the request.

        :type method: string
        :param method: The API call method name (ie, ``runQuery``,
                       ``lookup``, etc)

        :type data: string
        :param data: The data to send with the API call.
                     Typically this is a serialized Protobuf string.

        :rtype: string
        :returns: The string response content from the API call.

        :raises: Exception if the response code is not 200 OK.
        """
        headers = {
            'Content-Type': 'application/x-protobuf',
            'Content-Length': str(len(data)),
            'User-Agent': self.USER_AGENT,
        }
        headers, content = self.http.request(
            uri=self.build_api_url(dataset_id=dataset_id, method=method),
            method='POST', headers=headers, body=data)

        if headers['status'] != '200':
            raise Exception('Request failed. Error was: %s' % content)

        return content

    def _rpc(self, dataset_id, method, request_pb, response_pb_cls):
        """ Make a protobuf RPC request.

        :type dataset_id: string
        :param dataset_id: The ID of the dataset to connect to. This is
                           usually your project name in the cloud console.

        :type method: string
        :param method: The name of the method to invoke.

        :type request_pb: :class:`google.protobuf.message.Message` instance
        :param method: the protobuf instance representing the request.

        :type response_pb_cls: a :class:`google.protobuf.message.Message'
                               subclass.
        :param method: The class used to unmarshall the response protobuf.
        """
        response = self._request(dataset_id=dataset_id, method=method,
                                 data=request_pb.SerializeToString())
        return response_pb_cls.FromString(response)

    @classmethod
    def build_api_url(cls, dataset_id, method, base_url=None,
                      api_version=None):
        """Construct the URL for a particular API call.

        This method is used internally
        to come up with the URL
        to use when making RPCs
        to the Cloud Datastore API.

        :type dataset_id: string
        :param dataset_id: The ID of the dataset to connect to. This is
                           usually your project name in the cloud console.

        :type method: string
        :param method: The API method to call (ie, runQuery, lookup, ...).

        :type base_url: string
        :param base_url: The base URL where the API lives.
                         You shouldn't have to provide this.

        :type api_version: string
        :param api_version: The version of the API to connect to.
                            You shouldn't have to provide this.
        """
        return cls.API_URL_TEMPLATE.format(
            api_base=(base_url or cls.API_BASE_URL),
            api_version=(api_version or cls.API_VERSION),
            dataset_id=dataset_id, method=method)

    def transaction(self, transaction=connection.Connection._EMPTY):
        """Getter/setter for the connection's transaction object.

        :type transaction: :class:`gcloud.datastore.transaction.Transaction`,
                           (setting), or omitted (getting).
        :param transaction: The new transaction (if passed).

        :rtype: :class:`gcloud.datastore.transaction.Transaction`, (getting)
                or :class:`gcloud.datastore.connection.Connection` (setting)
        :returns: the current transaction (getting) or self (setting).
        """
        if transaction is self._EMPTY:
            return self._current_transaction
        else:
            self._current_transaction = transaction
            return self

    def mutation(self):
        """Getter for mutation usable with current connection.

        :rtype: :class:`gcloud.datastore.datastore_v1_pb2.Mutation`.
        :returns: the mutation instance associated with the current transaction
                  (if one exists) or or a new mutation instance.
        """
        if self.transaction():
            return self.transaction().mutation()
        else:
            return datastore_pb.Mutation()

    def dataset(self, *args, **kwargs):
        """Factory method for Dataset objects.

        :param args: All args and kwargs will be passed along to the
                     :class:`gcloud.datastore.dataset.Dataset` initializer.

        :rtype: :class:`gcloud.datastore.dataset.Dataset`
        :returns: A dataset object that will use this connection as
                  its transport.
        """
        kwargs['connection'] = self
        return Dataset(*args, **kwargs)

    def begin_transaction(self, dataset_id, serializable=False):
        """Begin a transaction.

        :type dataset_id: string
        :param dataset_id: The dataset over which to execute the transaction.
        """

        if self.transaction():
            raise ValueError('Cannot start a transaction with another already '
                             'in progress.')

        request = datastore_pb.BeginTransactionRequest()

        if serializable:
            request.isolation_level = (
                datastore_pb.BeginTransactionRequest.SERIALIZABLE)
        else:
            request.isolation_level = (
                datastore_pb.BeginTransactionRequest.SNAPSHOT)

        response = self._rpc(dataset_id, 'beginTransaction', request,
                             datastore_pb.BeginTransactionResponse)

        return response.transaction

    def rollback_transaction(self, dataset_id):
        """Rollback the connection's existing transaction.

        Raises a ``ValueError``
        if the connection isn't currently in a transaction.

        :type dataset_id: string
        :param dataset_id: The dataset to which the transaction belongs.
        """
        if not self.transaction() or not self.transaction().id():
            raise ValueError('No transaction to rollback.')

        request = datastore_pb.RollbackRequest()
        request.transaction = self.transaction().id()
        # Nothing to do with this response, so just execute the method.
        self._rpc(dataset_id, 'rollback', request,
                  datastore_pb.RollbackResponse)

    def run_query(self, dataset_id, query_pb, namespace=None):
        """Run a query on the Cloud Datastore.

        Given a Query protobuf,
        sends a ``runQuery`` request to the Cloud Datastore API
        and returns a list of entity protobufs matching the query.

        You typically wouldn't use this method directly,
        in favor of the :func:`gcloud.datastore.query.Query.fetch` method.

        Under the hood, the :class:`gcloud.datastore.query.Query` class
        uses this method to fetch data:

        >>> from gcloud import datastore
        >>> connection = datastore.get_connection(email, key_path)
        >>> dataset = connection.dataset('dataset-id')
        >>> query = dataset.query().kind('MyKind').filter('property =', 'val')

        Using the `fetch`` method...

        >>> query.fetch()
        [<list of Entity unmarshalled from protobuf>]
        >>> query.cursor()
        <string containing cursor where fetch stopped>

        Under the hood this is doing...

        >>> connection.run_query('dataset-id', query.to_protobuf())
        [<list of Entity Protobufs>], cursor, more_results, skipped_results

        :type dataset_id: string
        :param dataset_id: The ID of the dataset over which to run the query.

        :type query_pb: :class:`gcloud.datastore.datastore_v1_pb2.Query`
        :param query_pb: The Protobuf representing the query to run.

        :type namespace: string
        :param namespace: The namespace over which to run the query.
        """
        request = datastore_pb.RunQueryRequest()

        if namespace:
            request.partition_id.namespace = namespace

        request.query.CopyFrom(query_pb)
        response = self._rpc(dataset_id, 'runQuery', request,
                             datastore_pb.RunQueryResponse)
        return (
            [e.entity for e in response.batch.entity_result],
            response.batch.end_cursor,
            response.batch.more_results,
            response.batch.skipped_results,
        )

    def lookup(self, dataset_id, key_pbs):
        """Lookup keys from a dataset in the Cloud Datastore.

        This method deals only with protobufs
        (:class:`gcloud.datastore.datastore_v1_pb2.Key`
        and
        :class:`gcloud.datastore.datastore_v1_pb2.Entity`)
        and is used under the hood for methods like
        :func:`gcloud.datastore.dataset.Dataset.get_entity`:

        >>> from gcloud import datastore
        >>> from gcloud.datastore.key import Key
        >>> connection = datastore.get_connection(email, key_path)
        >>> dataset = connection.dataset('dataset-id')
        >>> key = Key(dataset=dataset).kind('MyKind').id(1234)

        Using the :class:`gcloud.datastore.dataset.Dataset` helper:

        >>> dataset.get_entity(key)
        <Entity object>

        Using the ``connection`` class directly:

        >>> connection.lookup('dataset-id', key.to_protobuf())
        <Entity protobuf>

        :type dataset_id: string
        :param dataset_id: The dataset to look up the keys.

        :type key_pbs: list of :class:`gcloud.datastore.datastore_v1_pb2.Key`
                       (or a single Key)
        :param key_pbs: The key (or keys) to retrieve from the datastore.

        :rtype: list of :class:`gcloud.datastore.datastore_v1_pb2.Entity`
                (or a single Entity)
        :returns: The entities corresponding to the keys provided.
                  If a single key was provided and no results matched,
                  this will return None.
                  If multiple keys were provided and no results matched,
                  this will return an empty list.
        """
        lookup_request = datastore_pb.LookupRequest()

        single_key = isinstance(key_pbs, datastore_pb.Key)

        if single_key:
            key_pbs = [key_pbs]

        for key_pb in key_pbs:
            lookup_request.key.add().CopyFrom(key_pb)

        lookup_response = self._rpc(dataset_id, 'lookup', lookup_request,
                                    datastore_pb.LookupResponse)

        results = [result.entity for result in lookup_response.found]

        if single_key:
            if results:
                return results[0]
            else:
                return None

        return results

    def commit(self, dataset_id, mutation_pb):
        """Commit dataset mutations in context of current transation (if any).

        :type dataset_id: string
        :param dataset_id: The dataset in which to perform the changes.

        :type mutation_pb: :class:`gcloud.datastore.datastore_v1_pb2.Mutation`.
        :param mutation_pb: The protobuf for the mutations being saved.

        :rtype: :class:`gcloud.datastore.datastore_v1_pb2.MutationResult`.
        :returns': the result protobuf for the mutation.
        """
        request = datastore_pb.CommitRequest()

        if self.transaction():
            request.mode = datastore_pb.CommitRequest.TRANSACTIONAL
            request.transaction = self.transaction().id()
        else:
            request.mode = datastore_pb.CommitRequest.NON_TRANSACTIONAL

        request.mutation.CopyFrom(mutation_pb)
        response = self._rpc(dataset_id, 'commit', request,
                             datastore_pb.CommitResponse)
        return response.mutation_result

    def save_entity(self, dataset_id, key_pb, properties):
        """Save an entity to the Cloud Datastore with the provided properties.

        .. note::
           Any existing properties for the entity identified by 'key_pb'
           will be replaced by those passed in 'properties';  properties
           not passed in 'properties' no longer be set for the entity.

        :type dataset_id: string
        :param dataset_id: The dataset in which to save the entity.

        :type key_pb: :class:`gcloud.datastore.datastore_v1_pb2.Key`
        :param key_pb: The complete or partial key for the entity.

        :type properties: dict
        :param properties: The properties to store on the entity.
        """
        mutation = self.mutation()

        # If the Key is complete, we should upsert
        # instead of using insert_auto_id.
        path = key_pb.path_element[-1]
        auto_id = not (path.HasField('id') or path.HasField('name'))

        if auto_id:
            insert = mutation.insert_auto_id.add()
        else:
            insert = mutation.upsert.add()

        insert.key.CopyFrom(key_pb)

        for name, value in properties.iteritems():
            prop = insert.property.add()
            # Set the name of the property.
            prop.name = name

            # Set the appropriate value.
            helpers._set_protobuf_value(prop.value, value)

        # If this is in a transaction, we should just return True. The
        # transaction will handle assigning any keys as necessary.
        if self.transaction():
            return True

        result = self.commit(dataset_id, mutation)
        # If this was an auto-assigned ID, return the new Key.
        if auto_id:
            return result.insert_auto_id_key[0]

        return True

    def delete_entities(self, dataset_id, key_pbs):
        """Delete keys from a dataset in the Cloud Datastore.

        This method deals only with
        :class:`gcloud.datastore.datastore_v1_pb2.Key` protobufs
        and not with any of the other abstractions.
        For example, it's used under the hood in the
        :func:`gcloud.datastore.entity.Entity.delete` method.

        :type dataset_id: string
        :param dataset_id: The dataset from which to delete the keys.

        :type key_pbs: list of :class:`gcloud.datastore.datastore_v1_pb2.Key`
        :param key_pbs: The keys to delete from the datastore.

        :rtype: boolean (if in a transaction) or else
                :class:`gcloud.datastore.datastore_v1_pb2.MutationResult`.
        :returns: True
        """
        mutation = self.mutation()

        for key_pb in key_pbs:
            delete = mutation.delete.add()
            delete.CopyFrom(key_pb)

        if not self.transaction():
            self.commit(dataset_id, mutation)

        return True
