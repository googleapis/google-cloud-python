# Copyright 2016 Google Inc. All rights reserved.
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

"""Wrap long-running operations returned from Google Cloud APIs."""

from google.longrunning import operations_pb2


_GOOGLE_APIS_PREFIX = 'types.googleapis.com'

_TYPE_URL_MAP = {
}


def _compute_type_url(klass, prefix=_GOOGLE_APIS_PREFIX):
    """Compute a type URL for a klass.

    :type klass: type
    :param klass: class to be used as a factory for the given type

    :type prefix: str
    :param prefix: URL prefix for the type

    :rtype: str
    :returns: the URL, prefixed as appropriate
    """
    name = klass.DESCRIPTOR.full_name
    return '%s/%s' % (prefix, name)


def _register_type_url(type_url, klass):
    """Register a klass as the factory for a given type URL.

    :type type_url: str
    :param type_url: URL naming the type

    :type klass: type
    :param klass: class to be used as a factory for the given type

    :raises: ValueError if a registration already exists for the URL.
    """
    if type_url in _TYPE_URL_MAP:
        if _TYPE_URL_MAP[type_url] is not klass:
            raise ValueError("Conflict: %s" % (_TYPE_URL_MAP[type_url],))

    _TYPE_URL_MAP[type_url] = klass


class Operation(object):
    """Representation of a Google API Long-Running Operation.

    :type name: str
    :param name: The fully-qualified path naming the operation.

    :type client: object: must provide ``_operations_stub`` accessor.
    :param client: The client used to poll for the status of the operation.

    :type pb_metadata: object
    :param pb_metadata: Instance of protobuf metadata class

    :type kw: dict
    :param kw: caller-assigned metadata about the operation
    """

    target = None
    """Instance assocated with the operations:  callers may set."""

    def __init__(self, name, client, pb_metadata=None, **kw):
        self.name = name
        self.client = client
        self.pb_metadata = pb_metadata
        self.metadata = kw.copy()
        self._complete = False

    @classmethod
    def from_pb(cls, op_pb, client, **kw):
        """Factory:  construct an instance from a protobuf.

        :type op_pb: :class:`google.longrunning.operations_pb2.Operation`
        :param op_pb: Protobuf to be parsed.

        :type client: object: must provide ``_operations_stub`` accessor.
        :param client: The client used to poll for the status of the operation.

        :type kw: dict
        :param kw: caller-assigned metadata about the operation

        :rtype: :class:`Operation`
        :returns: new instance, with attributes based on the protobuf.
        """
        pb_metadata = None
        if op_pb.metadata.type_url:
            type_url = op_pb.metadata.type_url
            md_klass = _TYPE_URL_MAP.get(type_url)
            if md_klass:
                pb_metadata = md_klass.FromString(op_pb.metadata.value)
        return cls(op_pb.name, client, pb_metadata, **kw)

    @property
    def complete(self):
        """Has the operation already completed?

        :rtype: bool
        :returns: True if already completed, else false.
        """
        return self._complete

    def poll(self):
        """Check if the operation has finished.

        :rtype: bool
        :returns: A boolean indicating if the current operation has completed.
        :raises: :class:`ValueError <exceptions.ValueError>` if the operation
                 has already completed.
        """
        if self.complete:
            raise ValueError('The operation has completed.')

        request_pb = operations_pb2.GetOperationRequest(name=self.name)
        # We expect a `google.longrunning.operations_pb2.Operation`.
        operation_pb = self.client._operations_stub.GetOperation(request_pb)

        if operation_pb.done:
            self._complete = True

        return self.complete
