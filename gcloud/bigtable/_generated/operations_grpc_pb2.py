import abc
from grpc.beta import implementations as beta_implementations
from grpc.early_adopter import implementations as early_adopter_implementations
from grpc.framework.alpha import utilities as alpha_utilities
from grpc.framework.common import cardinality
from grpc.framework.interfaces.face import utilities as face_utilities
class EarlyAdopterOperationsServicer(object):
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
class EarlyAdopterOperationsServer(object):
  """<fill me in later!>"""
  __metaclass__ = abc.ABCMeta
  @abc.abstractmethod
  def start(self):
    raise NotImplementedError()
  @abc.abstractmethod
  def stop(self):
    raise NotImplementedError()
class EarlyAdopterOperationsStub(object):
  """<fill me in later!>"""
  __metaclass__ = abc.ABCMeta
  @abc.abstractmethod
  def GetOperation(self, request):
    raise NotImplementedError()
  GetOperation.async = None
  @abc.abstractmethod
  def ListOperations(self, request):
    raise NotImplementedError()
  ListOperations.async = None
  @abc.abstractmethod
  def CancelOperation(self, request):
    raise NotImplementedError()
  CancelOperation.async = None
  @abc.abstractmethod
  def DeleteOperation(self, request):
    raise NotImplementedError()
  DeleteOperation.async = None
def early_adopter_create_Operations_server(servicer, port, private_key=None, certificate_chain=None):
  import google.longrunning.operations_pb2
  import google.longrunning.operations_pb2
  import google.longrunning.operations_pb2
  import google.longrunning.operations_pb2
  import google.longrunning.operations_pb2
  import google.protobuf.empty_pb2
  import google.longrunning.operations_pb2
  import google.protobuf.empty_pb2
  method_service_descriptions = {
    "CancelOperation": alpha_utilities.unary_unary_service_description(
      servicer.CancelOperation,
      google.longrunning.operations_pb2.CancelOperationRequest.FromString,
      google.protobuf.empty_pb2.Empty.SerializeToString,
    ),
    "DeleteOperation": alpha_utilities.unary_unary_service_description(
      servicer.DeleteOperation,
      google.longrunning.operations_pb2.DeleteOperationRequest.FromString,
      google.protobuf.empty_pb2.Empty.SerializeToString,
    ),
    "GetOperation": alpha_utilities.unary_unary_service_description(
      servicer.GetOperation,
      google.longrunning.operations_pb2.GetOperationRequest.FromString,
      google.longrunning.operations_pb2.Operation.SerializeToString,
    ),
    "ListOperations": alpha_utilities.unary_unary_service_description(
      servicer.ListOperations,
      google.longrunning.operations_pb2.ListOperationsRequest.FromString,
      google.longrunning.operations_pb2.ListOperationsResponse.SerializeToString,
    ),
  }
  return early_adopter_implementations.server("google.longrunning.Operations", method_service_descriptions, port, private_key=private_key, certificate_chain=certificate_chain)
def early_adopter_create_Operations_stub(host, port, metadata_transformer=None, secure=False, root_certificates=None, private_key=None, certificate_chain=None, server_host_override=None):
  import google.longrunning.operations_pb2
  import google.longrunning.operations_pb2
  import google.longrunning.operations_pb2
  import google.longrunning.operations_pb2
  import google.longrunning.operations_pb2
  import google.protobuf.empty_pb2
  import google.longrunning.operations_pb2
  import google.protobuf.empty_pb2
  method_invocation_descriptions = {
    "CancelOperation": alpha_utilities.unary_unary_invocation_description(
      google.longrunning.operations_pb2.CancelOperationRequest.SerializeToString,
      google.protobuf.empty_pb2.Empty.FromString,
    ),
    "DeleteOperation": alpha_utilities.unary_unary_invocation_description(
      google.longrunning.operations_pb2.DeleteOperationRequest.SerializeToString,
      google.protobuf.empty_pb2.Empty.FromString,
    ),
    "GetOperation": alpha_utilities.unary_unary_invocation_description(
      google.longrunning.operations_pb2.GetOperationRequest.SerializeToString,
      google.longrunning.operations_pb2.Operation.FromString,
    ),
    "ListOperations": alpha_utilities.unary_unary_invocation_description(
      google.longrunning.operations_pb2.ListOperationsRequest.SerializeToString,
      google.longrunning.operations_pb2.ListOperationsResponse.FromString,
    ),
  }
  return early_adopter_implementations.stub("google.longrunning.Operations", method_invocation_descriptions, host, port, metadata_transformer=metadata_transformer, secure=secure, root_certificates=root_certificates, private_key=private_key, certificate_chain=certificate_chain, server_host_override=server_host_override)

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
