# Copyright 2016 Google LLC All rights reserved.
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

"""User friendly container for Cloud Spanner Instance."""

import re

from google.api_core import page_iterator
from google.gax import INITIAL_PAGE
from google.gax.errors import GaxError
from google.gax.grpc import exc_to_code
from google.cloud.spanner_admin_instance_v1.proto import (
    spanner_instance_admin_pb2 as admin_v1_pb2)
from google.protobuf.field_mask_pb2 import FieldMask
from grpc import StatusCode

# pylint: disable=ungrouped-imports
from google.cloud.exceptions import Conflict
from google.cloud.exceptions import NotFound
from google.cloud.spanner_v1._helpers import _options_with_prefix
from google.cloud.spanner_v1.database import Database
from google.cloud.spanner_v1.pool import BurstyPool
# pylint: enable=ungrouped-imports


_INSTANCE_NAME_RE = re.compile(
    r'^projects/(?P<project>[^/]+)/'
    r'instances/(?P<instance_id>[a-z][-a-z0-9]*)$')

DEFAULT_NODE_COUNT = 1


class Instance(object):
    """Representation of a Cloud Spanner Instance.

    We can use a :class:`Instance` to:

    * :meth:`reload` itself
    * :meth:`create` itself
    * :meth:`update` itself
    * :meth:`delete` itself

    :type instance_id: str
    :param instance_id: The ID of the instance.

    :type client: :class:`~google.cloud.spanner_v1.client.Client`
    :param client: The client that owns the instance. Provides
                   authorization and a project ID.

    :type configuration_name: str
    :param configuration_name: Name of the instance configuration defining
                        how the instance will be created.
                        Required for instances which do not yet exist.

    :type node_count: int
    :param node_count: (Optional) Number of nodes allocated to the instance.

    :type display_name: str
    :param display_name: (Optional) The display name for the instance in the
                         Cloud Console UI. (Must be between 4 and 30
                         characters.) If this value is not set in the
                         constructor, will fall back to the instance ID.
    """

    def __init__(self,
                 instance_id,
                 client,
                 configuration_name=None,
                 node_count=DEFAULT_NODE_COUNT,
                 display_name=None):
        self.instance_id = instance_id
        self._client = client
        self.configuration_name = configuration_name
        self.node_count = node_count
        self.display_name = display_name or instance_id

    def _update_from_pb(self, instance_pb):
        """Refresh self from the server-provided protobuf.

        Helper for :meth:`from_pb` and :meth:`reload`.
        """
        if not instance_pb.display_name:  # Simple field (string)
            raise ValueError('Instance protobuf does not contain display_name')
        self.display_name = instance_pb.display_name
        self.configuration_name = instance_pb.config
        self.node_count = instance_pb.node_count

    @classmethod
    def from_pb(cls, instance_pb, client):
        """Creates an instance from a protobuf.

        :type instance_pb:
            :class:`google.spanner.v2.spanner_instance_admin_pb2.Instance`
        :param instance_pb: A instance protobuf object.

        :type client: :class:`~google.cloud.spanner_v1.client.Client`
        :param client: The client that owns the instance.

        :rtype: :class:`Instance`
        :returns: The instance parsed from the protobuf response.
        :raises ValueError:
            if the instance name does not match
            ``projects/{project}/instances/{instance_id}`` or if the parsed
            project ID does not match the project ID on the client.
        """
        match = _INSTANCE_NAME_RE.match(instance_pb.name)
        if match is None:
            raise ValueError('Instance protobuf name was not in the '
                             'expected format.', instance_pb.name)
        if match.group('project') != client.project:
            raise ValueError('Project ID on instance does not match the '
                             'project ID on the client')
        instance_id = match.group('instance_id')
        configuration_name = instance_pb.config

        result = cls(instance_id, client, configuration_name)
        result._update_from_pb(instance_pb)
        return result

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
        return self._client.project_name + '/instances/' + self.instance_id

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        # NOTE: This does not compare the configuration values, such as
        #       the display_name. Instead, it only compares
        #       identifying values instance ID and client. This is
        #       intentional, since the same instance can be in different states
        #       if not synchronized. Instances with similar instance
        #       settings but different clients can't be used in the same way.
        return (other.instance_id == self.instance_id and
                other._client == self._client)

    def __ne__(self, other):
        return not self == other

    def copy(self):
        """Make a copy of this instance.

        Copies the local data stored as simple types and copies the client
        attached to this instance.

        :rtype: :class:`~google.cloud.spanner_v1.instance.Instance`
        :returns: A copy of the current instance.
        """
        new_client = self._client.copy()
        return self.__class__(
            self.instance_id,
            new_client,
            self.configuration_name,
            node_count=self.node_count,
            display_name=self.display_name,
        )

    def create(self):
        """Create this instance.

        See
        https://cloud.google.com/spanner/reference/rpc/google.spanner.admin.instance.v1#google.spanner.admin.instance.v1.InstanceAdmin.CreateInstance

        .. note::

           Uses the ``project`` and ``instance_id`` on the current
           :class:`Instance` in addition to the ``display_name``.
           To change them before creating, reset the values via

           .. code:: python

              instance.display_name = 'New display name'
              instance.instance_id = 'i-changed-my-mind'

           before calling :meth:`create`.

        :rtype: :class:`google.api_core.operation.Operation`
        :returns: an operation instance
        :raises Conflict: if the instance already exists
        :raises GaxError:
            for errors other than ``ALREADY_EXISTS`` returned from the call
        """
        api = self._client.instance_admin_api
        instance_pb = admin_v1_pb2.Instance(
            name=self.name,
            config=self.configuration_name,
            display_name=self.display_name,
            node_count=self.node_count,
            )
        options = _options_with_prefix(self.name)

        try:
            future = api.create_instance(
                parent=self._client.project_name,
                instance_id=self.instance_id,
                instance=instance_pb,
                options=options,
            )
        except GaxError as exc:
            if exc_to_code(exc.cause) == StatusCode.ALREADY_EXISTS:
                raise Conflict(self.name)
            raise

        return future

    def exists(self):
        """Test whether this instance exists.

        See
        https://cloud.google.com/spanner/reference/rpc/google.spanner.admin.instance.v1#google.spanner.admin.instance.v1.InstanceAdmin.GetInstanceConfig

        :rtype: bool
        :returns: True if the instance exists, else false
        :raises GaxError:
            for errors other than ``NOT_FOUND`` returned from the call
        """
        api = self._client.instance_admin_api
        options = _options_with_prefix(self.name)

        try:
            api.get_instance(self.name, options=options)
        except GaxError as exc:
            if exc_to_code(exc.cause) == StatusCode.NOT_FOUND:
                return False
            raise

        return True

    def reload(self):
        """Reload the metadata for this instance.

        See
        https://cloud.google.com/spanner/reference/rpc/google.spanner.admin.instance.v1#google.spanner.admin.instance.v1.InstanceAdmin.GetInstanceConfig

        :raises NotFound: if the instance does not exist
        :raises GaxError: for other errors returned from the call
        """
        api = self._client.instance_admin_api
        options = _options_with_prefix(self.name)

        try:
            instance_pb = api.get_instance(self.name, options=options)
        except GaxError as exc:
            if exc_to_code(exc.cause) == StatusCode.NOT_FOUND:
                raise NotFound(self.name)
            raise

        self._update_from_pb(instance_pb)

    def update(self):
        """Update this instance.

        See
        https://cloud.google.com/spanner/reference/rpc/google.spanner.admin.instance.v1#google.spanner.admin.instance.v1.InstanceAdmin.UpdateInstance

        .. note::

           Updates the ``display_name`` and ``node_count``. To change those
           values before updating, set them via

           .. code:: python

              instance.display_name = 'New display name'
              instance.node_count = 5

            before calling :meth:`update`.

        :rtype: :class:`google.api_core.operation.Operation`
        :returns: an operation instance
        :raises NotFound: if the instance does not exist
        :raises GaxError: for other errors returned from the call
        """
        api = self._client.instance_admin_api
        instance_pb = admin_v1_pb2.Instance(
            name=self.name,
            config=self.configuration_name,
            display_name=self.display_name,
            node_count=self.node_count,
            )
        field_mask = FieldMask(paths=['config', 'display_name', 'node_count'])
        options = _options_with_prefix(self.name)

        try:
            future = api.update_instance(
                instance=instance_pb,
                field_mask=field_mask,
                options=options,
            )
        except GaxError as exc:
            if exc_to_code(exc.cause) == StatusCode.NOT_FOUND:
                raise NotFound(self.name)
            raise

        return future

    def delete(self):
        """Mark an instance and all of its databases for permanent deletion.

        See
        https://cloud.google.com/spanner/reference/rpc/google.spanner.admin.instance.v1#google.spanner.admin.instance.v1.InstanceAdmin.DeleteInstance

        Immediately upon completion of the request:

        * Billing will cease for all of the instance's reserved resources.

        Soon afterward:

        * The instance and all databases within the instance will be deleteed.
          All data in the databases will be permanently deleted.
        """
        api = self._client.instance_admin_api
        options = _options_with_prefix(self.name)

        try:
            api.delete_instance(self.name, options=options)
        except GaxError as exc:
            if exc_to_code(exc.cause) == StatusCode.NOT_FOUND:
                raise NotFound(self.name)
            raise

    def database(self, database_id, ddl_statements=(), pool=None):
        """Factory to create a database within this instance.

        :type database_id: str
        :param database_id: The ID of the instance.

        :type ddl_statements: list of string
        :param ddl_statements: (Optional) DDL statements, excluding the
                               'CREATE DATABSE' statement.

        :type pool: concrete subclass of
                    :class:`~google.cloud.spanner_v1.pool.AbstractSessionPool`.
        :param pool: (Optional) session pool to be used by database.

        :rtype: :class:`~google.cloud.spanner_v1.database.Database`
        :returns: a database owned by this instance.
        """
        return Database(
            database_id, self, ddl_statements=ddl_statements, pool=pool)

    def list_databases(self, page_size=None, page_token=None):
        """List databases for the instance.

        See
        https://cloud.google.com/spanner/reference/rpc/google.spanner.admin.database.v1#google.spanner.admin.database.v1.DatabaseAdmin.ListDatabases

        :type page_size: int
        :param page_size: (Optional) Maximum number of results to return.

        :type page_token: str
        :param page_token: (Optional) Token for fetching next page of results.

        :rtype: :class:`~google.api._ore.page_iterator.Iterator`
        :returns:
            Iterator of :class:`~google.cloud.spanner_v1.database.Database`
            resources within the current instance.
        """
        if page_token is None:
            page_token = INITIAL_PAGE
        options = _options_with_prefix(self.name, page_token=page_token)
        page_iter = self._client.database_admin_api.list_databases(
            self.name, page_size=page_size, options=options)
        iterator = page_iterator._GAXIterator(
            self._client, page_iter, _item_to_database)
        iterator.instance = self
        return iterator


def _item_to_database(iterator, database_pb):
    """Convert a database protobuf to the native object.

    :type iterator: :class:`~google.api_core.page_iterator.Iterator`
    :param iterator: The iterator that is currently in use.

    :type database_pb: :class:`~google.spanner.admin.database.v1.Database`
    :param database_pb: A database returned from the API.

    :rtype: :class:`~google.cloud.spanner_v1.database.Database`
    :returns: The next database in the page.
    """
    return Database.from_pb(database_pb, iterator.instance, pool=BurstyPool())
