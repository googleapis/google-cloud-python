# Copyright 2015 Google Inc.
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

"""The Operation resource in the Cloud Resource Manager API."""


from google.cloud.resource_manager._helpers import _PropertyMixin


class Operation(_PropertyMixin):
    """Operations are the result of network calls and can be long-running.

    See:
    https://cloud.google.com/resource-manager/reference/rest/v1/operations

    :type name: str
    :param name: The name of the operation.

    :type client: :class:`google.cloud.resource_manager.client.Client`
    :param client: The Client used with this operation.

    :type metadata: dict
    :param metadata: Metadata associated with this operation.

    :type done: boolean
    :param done: Whether or not the operation has finished.

    :type error: :class:`google.cloud.resource_manager.operation._Status`
    :param error: A message representing the error.

    :type response: dict
    :param response: The response data for the network call.
    """
    def __init__(self, name, client, metadata=None, done=False,
                 error=None, response=None):
        super(Operation, self).__init__(name=name)
        self._client = client
        self.name = name
        self.metadata = metadata
        self.done = done
        self.error = error
        self.response = response

    def __repr__(self):
        return '<Operation: %r (done=%r)>' % (self.name, self.done)

    @classmethod
    def from_api_repr(cls, resource, client):
        """Factory:  construct an Operation from its API representation.

        :type resource: dict
        :param resource: operation resource returned from the API

        :type client: :class:`google.cloud.resource_manager.client.Client`
        :param client: The Client used with this operation.

        :rtype: :class:`google.cloud.resource_manager.operation.Operation`
        :returns: The created operation.
        """
        operation = cls(client=client, name=resource.get('name'),
                        metadata=resource.get('metadata'),
                        done=resource.get('done'),
                        error=_Status.from_api_repr(resource.get('error')),
                        response=resource.get('response'))
        return operation

    def set_properties_from_api_repr(self, resource):
        """Update properties from its API representation."""
        self.name = resource.get('name')
        self.metadata = resource.get('metadata')
        self.done = resource.get('done')
        self.error = _Status.from_api_repr(resource.get('error'))
        self.response = resource.get('response')

    @property
    def full_name(self):
        """Fully-qualified name (ie, ``'operations/some/unique/name'``)."""
        if not self.name:
            raise ValueError('Missing operation name')
        return self.name

    @property
    def path(self):
        """URL for the operation (ie, ``'operations/some/unique/name'``)."""
        return '/%s' % (self.full_name)

    @property
    def client(self):
        """Returns the client."""
        return self._client

    def get(self, client=None):
        """API call:  reload the project via a ``GET`` request.

        This method will retrieve the current running operation. If you
        created a new :class:`Project` instance via
        :meth:`Client.new_project() \
        <google.cloud.resource_manager.client.Client.new_project>`,
        this method will retrieve operation metadata.

        See
        https://cloud.google.com/resource-manager/reference/rest/v1/operations/get

        :type client: :class:`google.cloud.resource_manager.client.Client` or
                      :data:`NoneType <types.NoneType>`
        :param client: the client to use. If not passed, falls back to
                       the client stored on the current operation.
        """
        client = self._require_client(client)

        resp = client._connection.api_request(method='GET', path=self.path)
        self.set_properties_from_api_repr(resource=resp)


class _Status(object):
    """
    Status defines a logical error model for different programming environments
    such as REST and RPC APIs.

    See:
    https://cloud.google.com/resource-manager/reference/rest/v1/operations#Status

    :type code: int
    :param code: The status code, which is the enum value of google.rpc.Code.

    :type message: str
    :param message: The error message in English, meant for the developer.

    :type details: list
    :param details: A list of messages with error details.
    """
    def __init__(self, code, message, details):
        self.code = code
        self.message = message
        self.details = details

    def __eq__(self, other):
        return (self.code == other.code
                and self.message == other.message
                and self.details == other.details)

    @classmethod
    def from_api_repr(cls, resource):
        """Factory:  construct a Status from its API representation.

        :type resource: dict
        :param resource: operation resource returned from the API

        :rtype: :class:`google.cloud.resource_manager.operation._Status`
        :returns: The status of the Operation.
        """
        if not resource:
            return None

        status = cls(code=resource.get('code'),
                     message=resource.get('message'),
                     details=resource.get('details'))
        return status
