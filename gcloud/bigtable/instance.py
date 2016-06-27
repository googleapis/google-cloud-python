# Copyright 2015 Google Inc. All rights reserved.
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

"""User friendly container for Google Cloud Bigtable Instance."""


import re

from google.longrunning import operations_pb2

from gcloud._helpers import _pb_timestamp_to_datetime
from gcloud.bigtable._generated_v2 import (
    instance_pb2 as data_v2_pb2)
from gcloud.bigtable._generated_v2 import (
    bigtable_instance_admin_pb2 as messages_v1_pb2)
from gcloud.bigtable._generated_v2 import (
    bigtable_table_admin_pb2 as table_messages_v1_pb2)
from gcloud.bigtable.table import Table


_INSTANCE_NAME_RE = re.compile(r'^projects/(?P<project>[^/]+)/'
                              r'instances/(?P<instance_id>[a-z][-a-z0-9]*)$')
_OPERATION_NAME_RE = re.compile(r'^operations/projects/([^/]+)/'
                                r'instances/([a-z][-a-z0-9]*)/operations/'
                                r'(?P<operation_id>\d+)$')
_TYPE_URL_BASE = 'type.googleapis.com/google.bigtable.'
_ADMIN_TYPE_URL_BASE = _TYPE_URL_BASE + 'admin.v2.'
_INSTANCE_CREATE_METADATA = _ADMIN_TYPE_URL_BASE + 'CreateInstanceMetadata'
_TYPE_URL_MAP = {
    _INSTANCE_CREATE_METADATA: messages_v1_pb2.CreateInstanceMetadata,
}


def _prepare_create_request(instance):
    """Creates a protobuf request for a CreateInstance request.

    :type instance: :class:`Instance`
    :param instance: The instance to be created.

    :rtype: :class:`.messages_v1_pb2.CreateInstanceRequest`
    :returns: The CreateInstance request object containing the instance info.
    """
    parent_name = ('projects/' + instance._client.project)
    return messages_v1_pb2.CreateInstanceRequest(
        name=parent_name,
        instance_id=instance.instance_id,
        instance=data_v2_pb2.Instance(
            display_name=instance.display_name,
        ),
    )


def _parse_pb_any_to_native(any_val, expected_type=None):
    """Convert a serialized "google.protobuf.Any" value to actual type.

    :type any_val: :class:`google.protobuf.any_pb2.Any`
    :param any_val: A serialized protobuf value container.

    :type expected_type: str
    :param expected_type: (Optional) The type URL we expect ``any_val``
                          to have.

    :rtype: object
    :returns: The de-serialized object.
    :raises: :class:`ValueError <exceptions.ValueError>` if the
             ``expected_type`` does not match the ``type_url`` on the input.
    """
    if expected_type is not None and expected_type != any_val.type_url:
        raise ValueError('Expected type: %s, Received: %s' % (
            expected_type, any_val.type_url))
    container_class = _TYPE_URL_MAP[any_val.type_url]
    return container_class.FromString(any_val.value)


def _process_operation(operation_pb):
    """Processes a create protobuf response.

    :type operation_pb: :class:`google.longrunning.operations_pb2.Operation`
    :param operation_pb: The long-running operation response from a
                         Create/Update/Undelete instance request.

    :rtype: tuple
    :returns: A pair of an integer and datetime stamp. The integer is the ID
              of the operation (``operation_id``) and the timestamp when
              the create operation began (``operation_begin``).
    :raises: :class:`ValueError <exceptions.ValueError>` if the operation name
             doesn't match the :data:`_OPERATION_NAME_RE` regex.
    """
    match = _OPERATION_NAME_RE.match(operation_pb.name)
    if match is None:
        raise ValueError('Operation name was not in the expected '
                         'format after a instance modification.',
                         operation_pb.name)
    operation_id = int(match.group('operation_id'))

    request_metadata = _parse_pb_any_to_native(operation_pb.metadata)
    operation_begin = _pb_timestamp_to_datetime(
        request_metadata.request_time)

    return operation_id, operation_begin


class Operation(object):
    """Representation of a Google API Long-Running Operation.

    In particular, these will be the result of operations on
    instances using the Cloud Bigtable API.

    :type op_type: str
    :param op_type: The type of operation being performed. Expect
                    ``create``, ``update`` or ``undelete``.

    :type op_id: int
    :param op_id: The ID of the operation.

    :type begin: :class:`datetime.datetime`
    :param begin: The time when the operation was started.

    :type instance: :class:`Instance`
    :param instance: The instance that created the operation.
    """

    def __init__(self, op_type, op_id, begin, instance=None):
        self.op_type = op_type
        self.op_id = op_id
        self.begin = begin
        self._instance = instance
        self._complete = False

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (other.op_type == self.op_type and
                other.op_id == self.op_id and
                other.begin == self.begin and
                other._instance == self._instance and
                other._complete == self._complete)

    def __ne__(self, other):
        return not self.__eq__(other)

    def finished(self):
        """Check if the operation has finished.

        :rtype: bool
        :returns: A boolean indicating if the current operation has completed.
        :raises: :class:`ValueError <exceptions.ValueError>` if the operation
                 has already completed.
        """
        if self._complete:
            raise ValueError('The operation has completed.')

        operation_name = ('operations/' + self._instance.name +
                          '/operations/%d' % (self.op_id,))
        request_pb = operations_pb2.GetOperationRequest(name=operation_name)
        # We expect a `google.longrunning.operations_pb2.Operation`.
        operation_pb = self._instance._client._operations_stub.GetOperation(
            request_pb, self._instance._client.timeout_seconds)

        if operation_pb.done:
            self._complete = True
            return True
        else:
            return False


class Instance(object):
    """Representation of a Google Cloud Bigtable Instance.

    We can use a :class:`Instance` to:

    * :meth:`reload` itself
    * :meth:`create` itself
    * :meth:`update` itself
    * :meth:`delete` itself
    * :meth:`undelete` itself

    .. note::

        For now, we leave out the ``default_storage_type`` (an enum)
        which if not sent will end up as :data:`.data_v2_pb2.STORAGE_SSD`.

    :type instance_id: str
    :param instance_id: The ID of the instance.

    :type client: :class:`Client <gcloud.bigtable.client.Client>`
    :param client: The client that owns the instance. Provides
                   authorization and a project ID.

    :type display_name: str
    :param display_name: (Optional) The display name for the instance in the
                         Cloud Console UI. (Must be between 4 and 30
                         characters.) If this value is not set in the
                         constructor, will fall back to the instance ID.
    """

    def __init__(self, instance_id, client,
                 display_name=None):
        self.instance_id = instance_id
        self.display_name = display_name or instance_id
        self._client = client

    def table(self, table_id):
        """Factory to create a table associated with this instance.

        :type table_id: str
        :param table_id: The ID of the table.

        :rtype: :class:`Table <gcloud.bigtable.table.Table>`
        :returns: The table owned by this instance.
        """
        return Table(table_id, self)

    def _update_from_pb(self, instance_pb):
        """Refresh self from the server-provided protobuf.

        Helper for :meth:`from_pb` and :meth:`reload`.
        """
        if not instance_pb.display_name:  # Simple field (string)
            raise ValueError('Instance protobuf does not contain display_name')
        self.display_name = instance_pb.display_name

    @classmethod
    def from_pb(cls, instance_pb, client):
        """Creates a instance instance from a protobuf.

        :type instance_pb: :class:`instance_pb2.Instance`
        :param instance_pb: A instance protobuf object.

        :type client: :class:`Client <gcloud.bigtable.client.Client>`
        :param client: The client that owns the instance.

        :rtype: :class:`Instance`
        :returns: The instance parsed from the protobuf response.
        :raises: :class:`ValueError <exceptions.ValueError>` if the instance
                 name does not match
                 ``projects/{project}/instances/{instance_id}``
                 or if the parsed project ID does not match the project ID
                 on the client.
        """
        match = _INSTANCE_NAME_RE.match(instance_pb.name)
        if match is None:
            raise ValueError('Instance protobuf name was not in the '
                             'expected format.', instance_pb.name)
        if match.group('project') != client.project:
            raise ValueError('Project ID on instance does not match the '
                             'project ID on the client')

        result = cls(match.group('instance_id'), client)
        result._update_from_pb(instance_pb)
        return result

    def copy(self):
        """Make a copy of this instance.

        Copies the local data stored as simple types and copies the client
        attached to this instance.

        :rtype: :class:`.Instance`
        :returns: A copy of the current instance.
        """
        new_client = self._client.copy()
        return self.__class__(self.instance_id, new_client,
                              display_name=self.display_name)

    @property
    def name(self):
        """Instance name used in requests.

        .. note::
          This property will not change if ``instance_id`` does not,
          but the return value is not cached.

        The instance name is of the form

            ``"projects/{project}/instances/{instance_id}"``

        :rtype: str
        :returns: The instance name.
        """
        return (self._client.project_name + '/instances/' + self.instance_id)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        # NOTE: This does not compare the configuration values, such as
        #       the display_name. Instead, it only compares
        #       identifying values instance ID and client. This is
        #       intentional, since the same instance can be in different states
        #       if not synchronized. Instances with similar instance
        #       settings but different clients can't be used in the same way.
        return (other.instance_id == self.instance_id and
                other._client == self._client)

    def __ne__(self, other):
        return not self.__eq__(other)

    def reload(self):
        """Reload the metadata for this instance."""
        request_pb = messages_v1_pb2.GetInstanceRequest(name=self.name)
        # We expect `data_v2_pb2.Instance`.
        instance_pb = self._client._instance_stub.GetInstance(
            request_pb, self._client.timeout_seconds)

        # NOTE: _update_from_pb does not check that the project and
        #       instance ID on the response match the request.
        self._update_from_pb(instance_pb)

    def create(self):
        """Create this instance.

        .. note::

            Uses the ``project`` and ``instance_id`` on the current
            :class:`Instance` in addition to the ``display_name``.
            To change them before creating, reset the values via

            .. code:: python

                instance.display_name = 'New display name'
                instance.instance_id = 'i-changed-my-mind'

            before calling :meth:`create`.

        :rtype: :class:`Operation`
        :returns: The long-running operation corresponding to the
                  create operation.
        """
        request_pb = _prepare_create_request(self)
        # We expect a `google.longrunning.operations_pb2.Operation`.
        operation_pb = self._client._instance_stub.CreateInstance(
            request_pb, self._client.timeout_seconds)

        op_id, op_begin = _process_operation(operation_pb)
        return Operation('create', op_id, op_begin, instance=self)

    def update(self):
        """Update this instance.

        .. note::

            Updates the ``display_name``. To change that value before
            updating, reset its values via

            .. code:: python

                instance.display_name = 'New display name'

            before calling :meth:`update`.
        """
        request_pb = data_v2_pb2.Instance(
            name=self.name,
            display_name=self.display_name,
        )
        # Ignore the expected `data_v2_pb2.Instance`.
        self._client._instance_stub.UpdateInstance(
            request_pb, self._client.timeout_seconds)

    def delete(self):
        """Delete this instance.

        Marks a instance and all of its tables for permanent deletion in 7 days.

        Immediately upon completion of the request:

        * Billing will cease for all of the instance's reserved resources.
        * The instance's ``delete_time`` field will be set 7 days in the future.

        Soon afterward:

        * All tables within the instance will become unavailable.

        Prior to the instance's ``delete_time``:

        * The instance can be recovered with a call to ``UndeleteInstance``.
        * All other attempts to modify or delete the instance will be rejected.

        At the instance's ``delete_time``:

        * The instance and **all of its tables** will immediately and
          irrevocably disappear from the API, and their data will be
          permanently deleted.
        """
        request_pb = messages_v1_pb2.DeleteInstanceRequest(name=self.name)
        # We expect a `google.protobuf.empty_pb2.Empty`
        self._client._instance_stub.DeleteInstance(
            request_pb, self._client.timeout_seconds)

    def list_tables(self):
        """List the tables in this instance.

        :rtype: list of :class:`Table <gcloud.bigtable.table.Table>`
        :returns: The list of tables owned by the instance.
        :raises: :class:`ValueError <exceptions.ValueError>` if one of the
                 returned tables has a name that is not of the expected format.
        """
        request_pb = table_messages_v1_pb2.ListTablesRequest(name=self.name)
        # We expect a `table_messages_v1_pb2.ListTablesResponse`
        table_list_pb = self._client._table_stub.ListTables(
            request_pb, self._client.timeout_seconds)

        result = []
        for table_pb in table_list_pb.tables:
            table_prefix = self.name + '/tables/'
            if not table_pb.name.startswith(table_prefix):
                raise ValueError('Table name %s not of expected format' % (
                    table_pb.name,))
            table_id = table_pb.name[len(table_prefix):]
            result.append(self.table(table_id))

        return result
