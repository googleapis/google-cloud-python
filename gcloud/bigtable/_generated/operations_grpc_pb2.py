import abc
from grpc.beta import implementations as beta_implementations
from grpc.framework.common import cardinality
from grpc.framework.interfaces.face import utilities as face_utilities

class BetaOperationsServicer(object):
  """<fill me in later!>"""
  __metaclass__ = abc.ABCMeta
  @abc.abstractmethod
  def GetOperation(self, request, context):
    raise NotImplementedError()
  @abc.abstractmethod
  def ListOperations(self, request, context):
    raise NotImplementedError()
  @abc.abstractmethod
  def CancelOperation(self, request, context):
    raise NotImplementedError()
  @abc.abstractmethod
  def DeleteOperation(self, request, context):
    raise NotImplementedError()

class BetaOperationsStub(object):
  """The interface to which stubs will conform."""
  __metaclass__ = abc.ABCMeta
  @abc.abstractmethod
  def GetOperation(self, request, timeout):
    raise NotImplementedError()
  GetOperation.future = None
  @abc.abstractmethod
  def ListOperations(self, request, timeout):
    raise NotImplementedError()
  ListOperations.future = None
  @abc.abstractmethod
  def CancelOperation(self, request, timeout):
    raise NotImplementedError()
  CancelOperation.future = None
  @abc.abstractmethod
  def DeleteOperation(self, request, timeout):
    raise NotImplementedError()
  DeleteOperation.future = None

def beta_create_Operations_server(servicer, pool=None, pool_size=None, default_timeout=None, maximum_timeout=None):
  import google.longrunning.operations_pb2
  import google.longrunning.operations_pb2
  import google.longrunning.operations_pb2
  import google.longrunning.operations_pb2
  import google.longrunning.operations_pb2
  import google.protobuf.empty_pb2
  import google.longrunning.operations_pb2
  import google.protobuf.empty_pb2
  request_deserializers = {
    ('google.longrunning.Operations', 'CancelOperation'): google.longrunning.operations_pb2.CancelOperationRequest.FromString,
    ('google.longrunning.Operations', 'DeleteOperation'): google.longrunning.operations_pb2.DeleteOperationRequest.FromString,
    ('google.longrunning.Operations', 'GetOperation'): google.longrunning.operations_pb2.GetOperationRequest.FromString,
    ('google.longrunning.Operations', 'ListOperations'): google.longrunning.operations_pb2.ListOperationsRequest.FromString,
  }
  response_serializers = {
    ('google.longrunning.Operations', 'CancelOperation'): google.protobuf.empty_pb2.Empty.SerializeToString,
    ('google.longrunning.Operations', 'DeleteOperation'): google.protobuf.empty_pb2.Empty.SerializeToString,
    ('google.longrunning.Operations', 'GetOperation'): google.longrunning.operations_pb2.Operation.SerializeToString,
    ('google.longrunning.Operations', 'ListOperations'): google.longrunning.operations_pb2.ListOperationsResponse.SerializeToString,
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
  import google.longrunning.operations_pb2
  import google.longrunning.operations_pb2
  import google.longrunning.operations_pb2
  import google.longrunning.operations_pb2
  import google.longrunning.operations_pb2
  import google.protobuf.empty_pb2
  import google.longrunning.operations_pb2
  import google.protobuf.empty_pb2
  request_serializers = {
    ('google.longrunning.Operations', 'CancelOperation'): google.longrunning.operations_pb2.CancelOperationRequest.SerializeToString,
    ('google.longrunning.Operations', 'DeleteOperation'): google.longrunning.operations_pb2.DeleteOperationRequest.SerializeToString,
    ('google.longrunning.Operations', 'GetOperation'): google.longrunning.operations_pb2.GetOperationRequest.SerializeToString,
    ('google.longrunning.Operations', 'ListOperations'): google.longrunning.operations_pb2.ListOperationsRequest.SerializeToString,
  }
  response_deserializers = {
    ('google.longrunning.Operations', 'CancelOperation'): google.protobuf.empty_pb2.Empty.FromString,
    ('google.longrunning.Operations', 'DeleteOperation'): google.protobuf.empty_pb2.Empty.FromString,
    ('google.longrunning.Operations', 'GetOperation'): google.longrunning.operations_pb2.Operation.FromString,
    ('google.longrunning.Operations', 'ListOperations'): google.longrunning.operations_pb2.ListOperationsResponse.FromString,
  }
  cardinalities = {
    'CancelOperation': cardinality.Cardinality.UNARY_UNARY,
    'DeleteOperation': cardinality.Cardinality.UNARY_UNARY,
    'GetOperation': cardinality.Cardinality.UNARY_UNARY,
    'ListOperations': cardinality.Cardinality.UNARY_UNARY,
  }
  stub_options = beta_implementations.stub_options(host=host, metadata_transformer=metadata_transformer, request_serializers=request_serializers, response_deserializers=response_deserializers, thread_pool=pool, thread_pool_size=pool_size)
  return beta_implementations.dynamic_stub(channel, 'google.longrunning.Operations', cardinalities, options=stub_options)
