import abc
from grpc.beta import implementations as beta_implementations
from grpc.early_adopter import implementations as early_adopter_implementations
from grpc.framework.alpha import utilities as alpha_utilities
from grpc.framework.common import cardinality
from grpc.framework.interfaces.face import utilities as face_utilities
class EarlyAdopterDatastoreServicer(object):
  """<fill me in later!>"""
  __metaclass__ = abc.ABCMeta
  @abc.abstractmethod
  def Lookup(self, request, context):
    raise NotImplementedError()
  @abc.abstractmethod
  def RunQuery(self, request, context):
    raise NotImplementedError()
  @abc.abstractmethod
  def BeginTransaction(self, request, context):
    raise NotImplementedError()
  @abc.abstractmethod
  def Commit(self, request, context):
    raise NotImplementedError()
  @abc.abstractmethod
  def Rollback(self, request, context):
    raise NotImplementedError()
  @abc.abstractmethod
  def AllocateIds(self, request, context):
    raise NotImplementedError()
class EarlyAdopterDatastoreServer(object):
  """<fill me in later!>"""
  __metaclass__ = abc.ABCMeta
  @abc.abstractmethod
  def start(self):
    raise NotImplementedError()
  @abc.abstractmethod
  def stop(self):
    raise NotImplementedError()
class EarlyAdopterDatastoreStub(object):
  """<fill me in later!>"""
  __metaclass__ = abc.ABCMeta
  @abc.abstractmethod
  def Lookup(self, request):
    raise NotImplementedError()
  Lookup.async = None
  @abc.abstractmethod
  def RunQuery(self, request):
    raise NotImplementedError()
  RunQuery.async = None
  @abc.abstractmethod
  def BeginTransaction(self, request):
    raise NotImplementedError()
  BeginTransaction.async = None
  @abc.abstractmethod
  def Commit(self, request):
    raise NotImplementedError()
  Commit.async = None
  @abc.abstractmethod
  def Rollback(self, request):
    raise NotImplementedError()
  Rollback.async = None
  @abc.abstractmethod
  def AllocateIds(self, request):
    raise NotImplementedError()
  AllocateIds.async = None
def early_adopter_create_Datastore_server(servicer, port, private_key=None, certificate_chain=None):
  import gcloud.datastore._generated.datastore_pb2
  import gcloud.datastore._generated.datastore_pb2
  import gcloud.datastore._generated.datastore_pb2
  import gcloud.datastore._generated.datastore_pb2
  import gcloud.datastore._generated.datastore_pb2
  import gcloud.datastore._generated.datastore_pb2
  import gcloud.datastore._generated.datastore_pb2
  import gcloud.datastore._generated.datastore_pb2
  import gcloud.datastore._generated.datastore_pb2
  import gcloud.datastore._generated.datastore_pb2
  import gcloud.datastore._generated.datastore_pb2
  import gcloud.datastore._generated.datastore_pb2
  method_service_descriptions = {
    "AllocateIds": alpha_utilities.unary_unary_service_description(
      servicer.AllocateIds,
      gcloud.datastore._generated.datastore_pb2.AllocateIdsRequest.FromString,
      gcloud.datastore._generated.datastore_pb2.AllocateIdsResponse.SerializeToString,
    ),
    "BeginTransaction": alpha_utilities.unary_unary_service_description(
      servicer.BeginTransaction,
      gcloud.datastore._generated.datastore_pb2.BeginTransactionRequest.FromString,
      gcloud.datastore._generated.datastore_pb2.BeginTransactionResponse.SerializeToString,
    ),
    "Commit": alpha_utilities.unary_unary_service_description(
      servicer.Commit,
      gcloud.datastore._generated.datastore_pb2.CommitRequest.FromString,
      gcloud.datastore._generated.datastore_pb2.CommitResponse.SerializeToString,
    ),
    "Lookup": alpha_utilities.unary_unary_service_description(
      servicer.Lookup,
      gcloud.datastore._generated.datastore_pb2.LookupRequest.FromString,
      gcloud.datastore._generated.datastore_pb2.LookupResponse.SerializeToString,
    ),
    "Rollback": alpha_utilities.unary_unary_service_description(
      servicer.Rollback,
      gcloud.datastore._generated.datastore_pb2.RollbackRequest.FromString,
      gcloud.datastore._generated.datastore_pb2.RollbackResponse.SerializeToString,
    ),
    "RunQuery": alpha_utilities.unary_unary_service_description(
      servicer.RunQuery,
      gcloud.datastore._generated.datastore_pb2.RunQueryRequest.FromString,
      gcloud.datastore._generated.datastore_pb2.RunQueryResponse.SerializeToString,
    ),
  }
  return early_adopter_implementations.server("google.datastore.v1beta3.Datastore", method_service_descriptions, port, private_key=private_key, certificate_chain=certificate_chain)
def early_adopter_create_Datastore_stub(host, port, metadata_transformer=None, secure=False, root_certificates=None, private_key=None, certificate_chain=None, server_host_override=None):
  import gcloud.datastore._generated.datastore_pb2
  import gcloud.datastore._generated.datastore_pb2
  import gcloud.datastore._generated.datastore_pb2
  import gcloud.datastore._generated.datastore_pb2
  import gcloud.datastore._generated.datastore_pb2
  import gcloud.datastore._generated.datastore_pb2
  import gcloud.datastore._generated.datastore_pb2
  import gcloud.datastore._generated.datastore_pb2
  import gcloud.datastore._generated.datastore_pb2
  import gcloud.datastore._generated.datastore_pb2
  import gcloud.datastore._generated.datastore_pb2
  import gcloud.datastore._generated.datastore_pb2
  method_invocation_descriptions = {
    "AllocateIds": alpha_utilities.unary_unary_invocation_description(
      gcloud.datastore._generated.datastore_pb2.AllocateIdsRequest.SerializeToString,
      gcloud.datastore._generated.datastore_pb2.AllocateIdsResponse.FromString,
    ),
    "BeginTransaction": alpha_utilities.unary_unary_invocation_description(
      gcloud.datastore._generated.datastore_pb2.BeginTransactionRequest.SerializeToString,
      gcloud.datastore._generated.datastore_pb2.BeginTransactionResponse.FromString,
    ),
    "Commit": alpha_utilities.unary_unary_invocation_description(
      gcloud.datastore._generated.datastore_pb2.CommitRequest.SerializeToString,
      gcloud.datastore._generated.datastore_pb2.CommitResponse.FromString,
    ),
    "Lookup": alpha_utilities.unary_unary_invocation_description(
      gcloud.datastore._generated.datastore_pb2.LookupRequest.SerializeToString,
      gcloud.datastore._generated.datastore_pb2.LookupResponse.FromString,
    ),
    "Rollback": alpha_utilities.unary_unary_invocation_description(
      gcloud.datastore._generated.datastore_pb2.RollbackRequest.SerializeToString,
      gcloud.datastore._generated.datastore_pb2.RollbackResponse.FromString,
    ),
    "RunQuery": alpha_utilities.unary_unary_invocation_description(
      gcloud.datastore._generated.datastore_pb2.RunQueryRequest.SerializeToString,
      gcloud.datastore._generated.datastore_pb2.RunQueryResponse.FromString,
    ),
  }
  return early_adopter_implementations.stub("google.datastore.v1beta3.Datastore", method_invocation_descriptions, host, port, metadata_transformer=metadata_transformer, secure=secure, root_certificates=root_certificates, private_key=private_key, certificate_chain=certificate_chain, server_host_override=server_host_override)

class BetaDatastoreServicer(object):
  """<fill me in later!>"""
  __metaclass__ = abc.ABCMeta
  @abc.abstractmethod
  def Lookup(self, request, context):
    raise NotImplementedError()
  @abc.abstractmethod
  def RunQuery(self, request, context):
    raise NotImplementedError()
  @abc.abstractmethod
  def BeginTransaction(self, request, context):
    raise NotImplementedError()
  @abc.abstractmethod
  def Commit(self, request, context):
    raise NotImplementedError()
  @abc.abstractmethod
  def Rollback(self, request, context):
    raise NotImplementedError()
  @abc.abstractmethod
  def AllocateIds(self, request, context):
    raise NotImplementedError()

class BetaDatastoreStub(object):
  """The interface to which stubs will conform."""
  __metaclass__ = abc.ABCMeta
  @abc.abstractmethod
  def Lookup(self, request, timeout):
    raise NotImplementedError()
  Lookup.future = None
  @abc.abstractmethod
  def RunQuery(self, request, timeout):
    raise NotImplementedError()
  RunQuery.future = None
  @abc.abstractmethod
  def BeginTransaction(self, request, timeout):
    raise NotImplementedError()
  BeginTransaction.future = None
  @abc.abstractmethod
  def Commit(self, request, timeout):
    raise NotImplementedError()
  Commit.future = None
  @abc.abstractmethod
  def Rollback(self, request, timeout):
    raise NotImplementedError()
  Rollback.future = None
  @abc.abstractmethod
  def AllocateIds(self, request, timeout):
    raise NotImplementedError()
  AllocateIds.future = None

def beta_create_Datastore_server(servicer, pool=None, pool_size=None, default_timeout=None, maximum_timeout=None):
  import gcloud.datastore._generated.datastore_pb2
  import gcloud.datastore._generated.datastore_pb2
  import gcloud.datastore._generated.datastore_pb2
  import gcloud.datastore._generated.datastore_pb2
  import gcloud.datastore._generated.datastore_pb2
  import gcloud.datastore._generated.datastore_pb2
  import gcloud.datastore._generated.datastore_pb2
  import gcloud.datastore._generated.datastore_pb2
  import gcloud.datastore._generated.datastore_pb2
  import gcloud.datastore._generated.datastore_pb2
  import gcloud.datastore._generated.datastore_pb2
  import gcloud.datastore._generated.datastore_pb2
  request_deserializers = {
    ('google.datastore.v1beta3.Datastore', 'AllocateIds'): gcloud.datastore._generated.datastore_pb2.AllocateIdsRequest.FromString,
    ('google.datastore.v1beta3.Datastore', 'BeginTransaction'): gcloud.datastore._generated.datastore_pb2.BeginTransactionRequest.FromString,
    ('google.datastore.v1beta3.Datastore', 'Commit'): gcloud.datastore._generated.datastore_pb2.CommitRequest.FromString,
    ('google.datastore.v1beta3.Datastore', 'Lookup'): gcloud.datastore._generated.datastore_pb2.LookupRequest.FromString,
    ('google.datastore.v1beta3.Datastore', 'Rollback'): gcloud.datastore._generated.datastore_pb2.RollbackRequest.FromString,
    ('google.datastore.v1beta3.Datastore', 'RunQuery'): gcloud.datastore._generated.datastore_pb2.RunQueryRequest.FromString,
  }
  response_serializers = {
    ('google.datastore.v1beta3.Datastore', 'AllocateIds'): gcloud.datastore._generated.datastore_pb2.AllocateIdsResponse.SerializeToString,
    ('google.datastore.v1beta3.Datastore', 'BeginTransaction'): gcloud.datastore._generated.datastore_pb2.BeginTransactionResponse.SerializeToString,
    ('google.datastore.v1beta3.Datastore', 'Commit'): gcloud.datastore._generated.datastore_pb2.CommitResponse.SerializeToString,
    ('google.datastore.v1beta3.Datastore', 'Lookup'): gcloud.datastore._generated.datastore_pb2.LookupResponse.SerializeToString,
    ('google.datastore.v1beta3.Datastore', 'Rollback'): gcloud.datastore._generated.datastore_pb2.RollbackResponse.SerializeToString,
    ('google.datastore.v1beta3.Datastore', 'RunQuery'): gcloud.datastore._generated.datastore_pb2.RunQueryResponse.SerializeToString,
  }
  method_implementations = {
    ('google.datastore.v1beta3.Datastore', 'AllocateIds'): face_utilities.unary_unary_inline(servicer.AllocateIds),
    ('google.datastore.v1beta3.Datastore', 'BeginTransaction'): face_utilities.unary_unary_inline(servicer.BeginTransaction),
    ('google.datastore.v1beta3.Datastore', 'Commit'): face_utilities.unary_unary_inline(servicer.Commit),
    ('google.datastore.v1beta3.Datastore', 'Lookup'): face_utilities.unary_unary_inline(servicer.Lookup),
    ('google.datastore.v1beta3.Datastore', 'Rollback'): face_utilities.unary_unary_inline(servicer.Rollback),
    ('google.datastore.v1beta3.Datastore', 'RunQuery'): face_utilities.unary_unary_inline(servicer.RunQuery),
  }
  server_options = beta_implementations.server_options(request_deserializers=request_deserializers, response_serializers=response_serializers, thread_pool=pool, thread_pool_size=pool_size, default_timeout=default_timeout, maximum_timeout=maximum_timeout)
  return beta_implementations.server(method_implementations, options=server_options)

def beta_create_Datastore_stub(channel, host=None, metadata_transformer=None, pool=None, pool_size=None):
  import gcloud.datastore._generated.datastore_pb2
  import gcloud.datastore._generated.datastore_pb2
  import gcloud.datastore._generated.datastore_pb2
  import gcloud.datastore._generated.datastore_pb2
  import gcloud.datastore._generated.datastore_pb2
  import gcloud.datastore._generated.datastore_pb2
  import gcloud.datastore._generated.datastore_pb2
  import gcloud.datastore._generated.datastore_pb2
  import gcloud.datastore._generated.datastore_pb2
  import gcloud.datastore._generated.datastore_pb2
  import gcloud.datastore._generated.datastore_pb2
  import gcloud.datastore._generated.datastore_pb2
  request_serializers = {
    ('google.datastore.v1beta3.Datastore', 'AllocateIds'): gcloud.datastore._generated.datastore_pb2.AllocateIdsRequest.SerializeToString,
    ('google.datastore.v1beta3.Datastore', 'BeginTransaction'): gcloud.datastore._generated.datastore_pb2.BeginTransactionRequest.SerializeToString,
    ('google.datastore.v1beta3.Datastore', 'Commit'): gcloud.datastore._generated.datastore_pb2.CommitRequest.SerializeToString,
    ('google.datastore.v1beta3.Datastore', 'Lookup'): gcloud.datastore._generated.datastore_pb2.LookupRequest.SerializeToString,
    ('google.datastore.v1beta3.Datastore', 'Rollback'): gcloud.datastore._generated.datastore_pb2.RollbackRequest.SerializeToString,
    ('google.datastore.v1beta3.Datastore', 'RunQuery'): gcloud.datastore._generated.datastore_pb2.RunQueryRequest.SerializeToString,
  }
  response_deserializers = {
    ('google.datastore.v1beta3.Datastore', 'AllocateIds'): gcloud.datastore._generated.datastore_pb2.AllocateIdsResponse.FromString,
    ('google.datastore.v1beta3.Datastore', 'BeginTransaction'): gcloud.datastore._generated.datastore_pb2.BeginTransactionResponse.FromString,
    ('google.datastore.v1beta3.Datastore', 'Commit'): gcloud.datastore._generated.datastore_pb2.CommitResponse.FromString,
    ('google.datastore.v1beta3.Datastore', 'Lookup'): gcloud.datastore._generated.datastore_pb2.LookupResponse.FromString,
    ('google.datastore.v1beta3.Datastore', 'Rollback'): gcloud.datastore._generated.datastore_pb2.RollbackResponse.FromString,
    ('google.datastore.v1beta3.Datastore', 'RunQuery'): gcloud.datastore._generated.datastore_pb2.RunQueryResponse.FromString,
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
  return beta_implementations.dynamic_stub(channel, 'google.datastore.v1beta3.Datastore', cardinalities, options=stub_options)
