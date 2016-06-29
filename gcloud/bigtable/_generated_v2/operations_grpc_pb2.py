from google.longrunning.operations_pb2 import (
    CancelOperationRequest,
    DeleteOperationRequest,
    GetOperationRequest,
    ListOperationsRequest,
    ListOperationsResponse,
    Operation,
    google_dot_protobuf_dot_empty__pb2,
)
from grpc.beta import implementations as beta_implementations
from grpc.beta import interfaces as beta_interfaces
from grpc.framework.common import cardinality
from grpc.framework.interfaces.face import utilities as face_utilities


class OperationsStub(object):
  """Manages long-running operations with an API service.

  When an API method normally takes long time to complete, it can be designed
  to return [Operation][google.longrunning.Operation] to the client, and the client can use this
  interface to receive the real response asynchronously by polling the
  operation resource, or using `google.watcher.v1.Watcher` interface to watch
  the response, or pass the operation resource to another API (such as Google
  Cloud Pub/Sub API) to receive the response.  Any API service that returns
  long-running operations should implement the `Operations` interface so
  developers can have a consistent client experience.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GetOperation = channel.unary_unary(
        '/google.longrunning.Operations/GetOperation',
        request_serializer=GetOperationRequest.SerializeToString,
        response_deserializer=Operation.FromString,
        )
    self.ListOperations = channel.unary_unary(
        '/google.longrunning.Operations/ListOperations',
        request_serializer=ListOperationsRequest.SerializeToString,
        response_deserializer=ListOperationsResponse.FromString,
        )
    self.CancelOperation = channel.unary_unary(
        '/google.longrunning.Operations/CancelOperation',
        request_serializer=CancelOperationRequest.SerializeToString,
        response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )
    self.DeleteOperation = channel.unary_unary(
        '/google.longrunning.Operations/DeleteOperation',
        request_serializer=DeleteOperationRequest.SerializeToString,
        response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )


class OperationsServicer(object):
  """Manages long-running operations with an API service.

  When an API method normally takes long time to complete, it can be designed
  to return [Operation][google.longrunning.Operation] to the client, and the client can use this
  interface to receive the real response asynchronously by polling the
  operation resource, or using `google.watcher.v1.Watcher` interface to watch
  the response, or pass the operation resource to another API (such as Google
  Cloud Pub/Sub API) to receive the response.  Any API service that returns
  long-running operations should implement the `Operations` interface so
  developers can have a consistent client experience.
  """

  def GetOperation(self, request, context):
    """Gets the latest state of a long-running operation.  Clients may use this
    method to poll the operation result at intervals as recommended by the API
    service.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ListOperations(self, request, context):
    """Lists operations that match the specified filter in the request. If the
    server doesn't support this method, it returns
    `google.rpc.Code.UNIMPLEMENTED`.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def CancelOperation(self, request, context):
    """Starts asynchronous cancellation on a long-running operation.  The server
    makes a best effort to cancel the operation, but success is not
    guaranteed.  If the server doesn't support this method, it returns
    `google.rpc.Code.UNIMPLEMENTED`.  Clients may use
    [Operations.GetOperation] or other methods to check whether the
    cancellation succeeded or the operation completed despite cancellation.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def DeleteOperation(self, request, context):
    """Deletes a long-running operation.  It indicates the client is no longer
    interested in the operation result. It does not cancel the operation.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_OperationsServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GetOperation': grpc.unary_unary_rpc_method_handler(
          servicer.GetOperation,
          request_deserializer=GetOperationRequest.FromString,
          response_serializer=Operation.SerializeToString,
      ),
      'ListOperations': grpc.unary_unary_rpc_method_handler(
          servicer.ListOperations,
          request_deserializer=ListOperationsRequest.FromString,
          response_serializer=ListOperationsResponse.SerializeToString,
      ),
      'CancelOperation': grpc.unary_unary_rpc_method_handler(
          servicer.CancelOperation,
          request_deserializer=CancelOperationRequest.FromString,
          response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
      ),
      'DeleteOperation': grpc.unary_unary_rpc_method_handler(
          servicer.DeleteOperation,
          request_deserializer=DeleteOperationRequest.FromString,
          response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'google.longrunning.Operations', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))


class BetaOperationsServicer(object):
  """Manages long-running operations with an API service.

  When an API method normally takes long time to complete, it can be designed
  to return [Operation][google.longrunning.Operation] to the client, and the client can use this
  interface to receive the real response asynchronously by polling the
  operation resource, or using `google.watcher.v1.Watcher` interface to watch
  the response, or pass the operation resource to another API (such as Google
  Cloud Pub/Sub API) to receive the response.  Any API service that returns
  long-running operations should implement the `Operations` interface so
  developers can have a consistent client experience.
  """
  def GetOperation(self, request, context):
    """Gets the latest state of a long-running operation.  Clients may use this
    method to poll the operation result at intervals as recommended by the API
    service.
    """
    context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)
  def ListOperations(self, request, context):
    """Lists operations that match the specified filter in the request. If the
    server doesn't support this method, it returns
    `google.rpc.Code.UNIMPLEMENTED`.
    """
    context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)
  def CancelOperation(self, request, context):
    """Starts asynchronous cancellation on a long-running operation.  The server
    makes a best effort to cancel the operation, but success is not
    guaranteed.  If the server doesn't support this method, it returns
    `google.rpc.Code.UNIMPLEMENTED`.  Clients may use
    [Operations.GetOperation] or other methods to check whether the
    cancellation succeeded or the operation completed despite cancellation.
    """
    context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)
  def DeleteOperation(self, request, context):
    """Deletes a long-running operation.  It indicates the client is no longer
    interested in the operation result. It does not cancel the operation.
    """
    context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)


class BetaOperationsStub(object):
  """Manages long-running operations with an API service.

  When an API method normally takes long time to complete, it can be designed
  to return [Operation][google.longrunning.Operation] to the client, and the client can use this
  interface to receive the real response asynchronously by polling the
  operation resource, or using `google.watcher.v1.Watcher` interface to watch
  the response, or pass the operation resource to another API (such as Google
  Cloud Pub/Sub API) to receive the response.  Any API service that returns
  long-running operations should implement the `Operations` interface so
  developers can have a consistent client experience.
  """
  def GetOperation(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
    """Gets the latest state of a long-running operation.  Clients may use this
    method to poll the operation result at intervals as recommended by the API
    service.
    """
    raise NotImplementedError()
  GetOperation.future = None
  def ListOperations(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
    """Lists operations that match the specified filter in the request. If the
    server doesn't support this method, it returns
    `google.rpc.Code.UNIMPLEMENTED`.
    """
    raise NotImplementedError()
  ListOperations.future = None
  def CancelOperation(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
    """Starts asynchronous cancellation on a long-running operation.  The server
    makes a best effort to cancel the operation, but success is not
    guaranteed.  If the server doesn't support this method, it returns
    `google.rpc.Code.UNIMPLEMENTED`.  Clients may use
    [Operations.GetOperation] or other methods to check whether the
    cancellation succeeded or the operation completed despite cancellation.
    """
    raise NotImplementedError()
  CancelOperation.future = None
  def DeleteOperation(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
    """Deletes a long-running operation.  It indicates the client is no longer
    interested in the operation result. It does not cancel the operation.
    """
    raise NotImplementedError()
  DeleteOperation.future = None


def beta_create_Operations_server(servicer, pool=None, pool_size=None, default_timeout=None, maximum_timeout=None):
  request_deserializers = {
    ('google.longrunning.Operations', 'CancelOperation'): CancelOperationRequest.FromString,
    ('google.longrunning.Operations', 'DeleteOperation'): DeleteOperationRequest.FromString,
    ('google.longrunning.Operations', 'GetOperation'): GetOperationRequest.FromString,
    ('google.longrunning.Operations', 'ListOperations'): ListOperationsRequest.FromString,
  }
  response_serializers = {
    ('google.longrunning.Operations', 'CancelOperation'): google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
    ('google.longrunning.Operations', 'DeleteOperation'): google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
    ('google.longrunning.Operations', 'GetOperation'): Operation.SerializeToString,
    ('google.longrunning.Operations', 'ListOperations'): ListOperationsResponse.SerializeToString,
  }
  method_implementations = {
    ('google.longrunning.Operations', 'CancelOperation'): face_utilities.unary_unary_inline(servicer.CancelOperation),
    ('google.longrunning.Operations', 'DeleteOperation'): face_utilities.unary_unary_inline(servicer.DeleteOperation),
    ('google.longrunning.Operations', 'GetOperation'): face_utilities.unary_unary_inline(servicer.GetOperation),
    ('google.longrunning.Operations', 'ListOperations'): face_utilities.unary_unary_inline(servicer.ListOperations),
  }
  server_options = beta_implementations.server_options(request_deserializers=request_deserializers, response_serializers=response_serializers, thread_pool=pool, thread_pool_size=pool_size, default_timeout=default_timeout, maximum_timeout=maximum_timeout)
  return beta_implementations.server(method_implementations, options=server_options)


def beta_create_Operations_stub(channel, host=None, metadata_transformer=None, pool=None, pool_size=None):
  request_serializers = {
    ('google.longrunning.Operations', 'CancelOperation'): CancelOperationRequest.SerializeToString,
    ('google.longrunning.Operations', 'DeleteOperation'): DeleteOperationRequest.SerializeToString,
    ('google.longrunning.Operations', 'GetOperation'): GetOperationRequest.SerializeToString,
    ('google.longrunning.Operations', 'ListOperations'): ListOperationsRequest.SerializeToString,
  }
  response_deserializers = {
    ('google.longrunning.Operations', 'CancelOperation'): google_dot_protobuf_dot_empty__pb2.Empty.FromString,
    ('google.longrunning.Operations', 'DeleteOperation'): google_dot_protobuf_dot_empty__pb2.Empty.FromString,
    ('google.longrunning.Operations', 'GetOperation'): Operation.FromString,
    ('google.longrunning.Operations', 'ListOperations'): ListOperationsResponse.FromString,
  }
  cardinalities = {
    'CancelOperation': cardinality.Cardinality.UNARY_UNARY,
    'DeleteOperation': cardinality.Cardinality.UNARY_UNARY,
    'GetOperation': cardinality.Cardinality.UNARY_UNARY,
    'ListOperations': cardinality.Cardinality.UNARY_UNARY,
  }
  stub_options = beta_implementations.stub_options(host=host, metadata_transformer=metadata_transformer, request_serializers=request_serializers, response_deserializers=response_deserializers, thread_pool=pool, thread_pool_size=pool_size)
  return beta_implementations.dynamic_stub(channel, 'google.longrunning.Operations', cardinalities, options=stub_options)
