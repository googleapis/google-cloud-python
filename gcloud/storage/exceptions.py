# TODO: Make these super useful.
from gcloud import exceptions

class StorageError(exceptions.Error):
  pass


class ConnectionError(exceptions.ConnectionError):
  """
  Storage error handler for HTTP response errors for gcloud storage.
  """
  pass


class NotFoundError(ConnectionError):
  pass


class UnauthorizedError(ConnectionError):
  pass


class InvalidBucketNameError(ConnectionError):
  pass


class TooManyBucketsError(ConnectionError):
  pass


class BucketAlreadyExistsError(ConnectionError):
  pass


class DomainVerificationRequiredError(ConnectionError):
  pass


class BucketAlreadyOwnedByYouError(ConnectionError):
  pass


class BucketNameUnavailableError(ConnectionError):
  pass


class KeyTooLongError(ConnectionError):
  pass
