if __name__ != 'google.api':
  import sys
  # Set `api.__path__` equal to `api.protobuf4.__path__` so that
  # subpackages under google/api/protobuf4 can be imported as if
  # they were located directly beneath google/api.
  sys.modules['google.api'].__path__ = __path__