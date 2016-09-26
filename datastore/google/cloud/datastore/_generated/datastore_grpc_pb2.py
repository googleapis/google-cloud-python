# BEGIN: Imports from datastore_pb2
from google.cloud.datastore._generated.datastore_pb2 import AllocateIdsRequest
from google.cloud.datastore._generated.datastore_pb2 import AllocateIdsResponse
from google.cloud.datastore._generated.datastore_pb2 import BeginTransactionRequest
from google.cloud.datastore._generated.datastore_pb2 import BeginTransactionResponse
from google.cloud.datastore._generated.datastore_pb2 import CommitRequest
from google.cloud.datastore._generated.datastore_pb2 import CommitResponse
from google.cloud.datastore._generated.datastore_pb2 import LookupRequest
from google.cloud.datastore._generated.datastore_pb2 import LookupResponse
from google.cloud.datastore._generated.datastore_pb2 import Mutation
from google.cloud.datastore._generated.datastore_pb2 import MutationResult
from google.cloud.datastore._generated.datastore_pb2 import ReadOptions
from google.cloud.datastore._generated.datastore_pb2 import RollbackRequest
from google.cloud.datastore._generated.datastore_pb2 import RollbackResponse
from google.cloud.datastore._generated.datastore_pb2 import RunQueryRequest
from google.cloud.datastore._generated.datastore_pb2 import RunQueryResponse
#   END: Imports from datastore_pb2
import grpc
from grpc.beta import implementations as beta_implementations
from grpc.beta import interfaces as beta_interfaces
from grpc.framework.common import cardinality
from grpc.framework.interfaces.face import utilities as face_utilities


class DatastoreStub(object):
  """Each RPC normalizes the partition IDs of the keys in its input entities,
  and always returns entities with keys with normalized partition IDs.
  This applies to all keys and entities, including those in values, except keys
  with both an empty path and an empty or unset partition ID. Normalization of
  input keys sets the project ID (if not already set) to the project ID from
  the request.

  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Lookup = channel.unary_unary(
        '/google.datastore.v1.Datastore/Lookup',
        request_serializer=LookupRequest.SerializeToString,
        response_deserializer=LookupResponse.FromString,
        )
    self.RunQuery = channel.unary_unary(
        '/google.datastore.v1.Datastore/RunQuery',
        request_serializer=RunQueryRequest.SerializeToString,
        response_deserializer=RunQueryResponse.FromString,
        )
    self.BeginTransaction = channel.unary_unary(
        '/google.datastore.v1.Datastore/BeginTransaction',
        request_serializer=BeginTransactionRequest.SerializeToString,
        response_deserializer=BeginTransactionResponse.FromString,
        )
    self.Commit = channel.unary_unary(
        '/google.datastore.v1.Datastore/Commit',
        request_serializer=CommitRequest.SerializeToString,
        response_deserializer=CommitResponse.FromString,
        )
    self.Rollback = channel.unary_unary(
        '/google.datastore.v1.Datastore/Rollback',
        request_serializer=RollbackRequest.SerializeToString,
        response_deserializer=RollbackResponse.FromString,
        )
    self.AllocateIds = channel.unary_unary(
        '/google.datastore.v1.Datastore/AllocateIds',
        request_serializer=AllocateIdsRequest.SerializeToString,
        response_deserializer=AllocateIdsResponse.FromString,
        )


class DatastoreServicer(object):
  """Each RPC normalizes the partition IDs of the keys in its input entities,
  and always returns entities with keys with normalized partition IDs.
  This applies to all keys and entities, including those in values, except keys
  with both an empty path and an empty or unset partition ID. Normalization of
  input keys sets the project ID (if not already set) to the project ID from
  the request.

  """

  def Lookup(self, request, context):
    """Looks up entities by key.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def RunQuery(self, request, context):
    """Queries for entities.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def BeginTransaction(self, request, context):
    """Begins a new transaction.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Commit(self, request, context):
    """Commits a transaction, optionally creating, deleting or modifying some
    entities.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Rollback(self, request, context):
    """Rolls back a transaction.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def AllocateIds(self, request, context):
    """Allocates IDs for the given keys, which is useful for referencing an entity
    before it is inserted.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_DatastoreServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Lookup': grpc.unary_unary_rpc_method_handler(
          servicer.Lookup,
          request_deserializer=LookupRequest.FromString,
          response_serializer=LookupResponse.SerializeToString,
      ),
      'RunQuery': grpc.unary_unary_rpc_method_handler(
          servicer.RunQuery,
          request_deserializer=RunQueryRequest.FromString,
          response_serializer=RunQueryResponse.SerializeToString,
      ),
      'BeginTransaction': grpc.unary_unary_rpc_method_handler(
          servicer.BeginTransaction,
          request_deserializer=BeginTransactionRequest.FromString,
          response_serializer=BeginTransactionResponse.SerializeToString,
      ),
      'Commit': grpc.unary_unary_rpc_method_handler(
          servicer.Commit,
          request_deserializer=CommitRequest.FromString,
          response_serializer=CommitResponse.SerializeToString,
      ),
      'Rollback': grpc.unary_unary_rpc_method_handler(
          servicer.Rollback,
          request_deserializer=RollbackRequest.FromString,
          response_serializer=RollbackResponse.SerializeToString,
      ),
      'AllocateIds': grpc.unary_unary_rpc_method_handler(
          servicer.AllocateIds,
          request_deserializer=AllocateIdsRequest.FromString,
          response_serializer=AllocateIdsResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'google.datastore.v1.Datastore', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))


class BetaDatastoreServicer(object):
  """Each RPC normalizes the partition IDs of the keys in its input entities,
  and always returns entities with keys with normalized partition IDs.
  This applies to all keys and entities, including those in values, except keys
  with both an empty path and an empty or unset partition ID. Normalization of
  input keys sets the project ID (if not already set) to the project ID from
  the request.

  """
  def Lookup(self, request, context):
    """Looks up entities by key.
    """
    context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)
  def RunQuery(self, request, context):
    """Queries for entities.
    """
    context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)
  def BeginTransaction(self, request, context):
    """Begins a new transaction.
    """
    context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)
  def Commit(self, request, context):
    """Commits a transaction, optionally creating, deleting or modifying some
    entities.
    """
    context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)
  def Rollback(self, request, context):
    """Rolls back a transaction.
    """
    context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)
  def AllocateIds(self, request, context):
    """Allocates IDs for the given keys, which is useful for referencing an entity
    before it is inserted.
    """
    context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)


class BetaDatastoreStub(object):
  """Each RPC normalizes the partition IDs of the keys in its input entities,
  and always returns entities with keys with normalized partition IDs.
  This applies to all keys and entities, including those in values, except keys
  with both an empty path and an empty or unset partition ID. Normalization of
  input keys sets the project ID (if not already set) to the project ID from
  the request.

  """
  def Lookup(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
    """Looks up entities by key.
    """
    raise NotImplementedError()
  Lookup.future = None
  def RunQuery(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
    """Queries for entities.
    """
    raise NotImplementedError()
  RunQuery.future = None
  def BeginTransaction(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
    """Begins a new transaction.
    """
    raise NotImplementedError()
  BeginTransaction.future = None
  def Commit(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
    """Commits a transaction, optionally creating, deleting or modifying some
    entities.
    """
    raise NotImplementedError()
  Commit.future = None
  def Rollback(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
    """Rolls back a transaction.
    """
    raise NotImplementedError()
  Rollback.future = None
  def AllocateIds(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
    """Allocates IDs for the given keys, which is useful for referencing an entity
    before it is inserted.
    """
    raise NotImplementedError()
  AllocateIds.future = None


def beta_create_Datastore_server(servicer, pool=None, pool_size=None, default_timeout=None, maximum_timeout=None):
  request_deserializers = {
    ('google.datastore.v1.Datastore', 'AllocateIds'): AllocateIdsRequest.FromString,
    ('google.datastore.v1.Datastore', 'BeginTransaction'): BeginTransactionRequest.FromString,
    ('google.datastore.v1.Datastore', 'Commit'): CommitRequest.FromString,
    ('google.datastore.v1.Datastore', 'Lookup'): LookupRequest.FromString,
    ('google.datastore.v1.Datastore', 'Rollback'): RollbackRequest.FromString,
    ('google.datastore.v1.Datastore', 'RunQuery'): RunQueryRequest.FromString,
  }
  response_serializers = {
    ('google.datastore.v1.Datastore', 'AllocateIds'): AllocateIdsResponse.SerializeToString,
    ('google.datastore.v1.Datastore', 'BeginTransaction'): BeginTransactionResponse.SerializeToString,
    ('google.datastore.v1.Datastore', 'Commit'): CommitResponse.SerializeToString,
    ('google.datastore.v1.Datastore', 'Lookup'): LookupResponse.SerializeToString,
    ('google.datastore.v1.Datastore', 'Rollback'): RollbackResponse.SerializeToString,
    ('google.datastore.v1.Datastore', 'RunQuery'): RunQueryResponse.SerializeToString,
  }
  method_implementations = {
    ('google.datastore.v1.Datastore', 'AllocateIds'): face_utilities.unary_unary_inline(servicer.AllocateIds),
    ('google.datastore.v1.Datastore', 'BeginTransaction'): face_utilities.unary_unary_inline(servicer.BeginTransaction),
    ('google.datastore.v1.Datastore', 'Commit'): face_utilities.unary_unary_inline(servicer.Commit),
    ('google.datastore.v1.Datastore', 'Lookup'): face_utilities.unary_unary_inline(servicer.Lookup),
    ('google.datastore.v1.Datastore', 'Rollback'): face_utilities.unary_unary_inline(servicer.Rollback),
    ('google.datastore.v1.Datastore', 'RunQuery'): face_utilities.unary_unary_inline(servicer.RunQuery),
  }
  server_options = beta_implementations.server_options(request_deserializers=request_deserializers, response_serializers=response_serializers, thread_pool=pool, thread_pool_size=pool_size, default_timeout=default_timeout, maximum_timeout=maximum_timeout)
  return beta_implementations.server(method_implementations, options=server_options)


def beta_create_Datastore_stub(channel, host=None, metadata_transformer=None, pool=None, pool_size=None):
  request_serializers = {
    ('google.datastore.v1.Datastore', 'AllocateIds'): AllocateIdsRequest.SerializeToString,
    ('google.datastore.v1.Datastore', 'BeginTransaction'): BeginTransactionRequest.SerializeToString,
    ('google.datastore.v1.Datastore', 'Commit'): CommitRequest.SerializeToString,
    ('google.datastore.v1.Datastore', 'Lookup'): LookupRequest.SerializeToString,
    ('google.datastore.v1.Datastore', 'Rollback'): RollbackRequest.SerializeToString,
    ('google.datastore.v1.Datastore', 'RunQuery'): RunQueryRequest.SerializeToString,
  }
  response_deserializers = {
    ('google.datastore.v1.Datastore', 'AllocateIds'): AllocateIdsResponse.FromString,
    ('google.datastore.v1.Datastore', 'BeginTransaction'): BeginTransactionResponse.FromString,
    ('google.datastore.v1.Datastore', 'Commit'): CommitResponse.FromString,
    ('google.datastore.v1.Datastore', 'Lookup'): LookupResponse.FromString,
    ('google.datastore.v1.Datastore', 'Rollback'): RollbackResponse.FromString,
    ('google.datastore.v1.Datastore', 'RunQuery'): RunQueryResponse.FromString,
  }
  cardinalities = {
    'AllocateIds': cardinality.Cardinality.UNARY_UNARY,
    'BeginTransaction': cardinality.Cardinality.UNARY_UNARY,
    'Commit': cardinality.Cardinality.UNARY_UNARY,
    'Lookup': cardinality.Cardinality.UNARY_UNARY,
    'Rollback': cardinality.Cardinality.UNARY_UNARY,
    'RunQuery': cardinality.Cardinality.UNARY_UNARY,
  }
  stub_options = beta_implementations.stub_options(host=host, metadata_transformer=metadata_transformer, request_serializers=request_serializers, response_deserializers=response_deserializers, thread_pool=pool, thread_pool_size=pool_size)
  return beta_implementations.dynamic_stub(channel, 'google.datastore.v1.Datastore', cardinalities, options=stub_options)
