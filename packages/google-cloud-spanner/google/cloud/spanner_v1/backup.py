# Copyright 2020 Google LLC All rights reserved.
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

"""User friendly container for Cloud Spanner Backup."""

import re

from google.cloud.exceptions import NotFound

from google.cloud.spanner_admin_database_v1 import Backup as BackupPB
from google.cloud.spanner_v1._helpers import _metadata_with_prefix

_BACKUP_NAME_RE = re.compile(
    r"^projects/(?P<project>[^/]+)/"
    r"instances/(?P<instance_id>[a-z][-a-z0-9]*)/"
    r"backups/(?P<backup_id>[a-z][a-z0-9_\-]*[a-z0-9])$"
)


class Backup(object):
    """Representation of a Cloud Spanner Backup.

    We can use a :class`Backup` to:

    * :meth:`create` the backup
    * :meth:`update` the backup
    * :meth:`delete` the backup

    :type backup_id: str
    :param backup_id: The ID of the backup.

    :type instance: :class:`~google.cloud.spanner_v1.instance.Instance`
    :param instance: The instance that owns the backup.

    :type database: str
    :param database: (Optional) The URI of the database that the backup is
                     for. Required if the create method needs to be called.

    :type expire_time: :class:`datetime.datetime`
    :param expire_time: (Optional) The expire time that will be used to
                        create the backup. Required if the create method
                        needs to be called.
    """

    def __init__(self, backup_id, instance, database="", expire_time=None):
        self.backup_id = backup_id
        self._instance = instance
        self._database = database
        self._expire_time = expire_time
        self._create_time = None
        self._size_bytes = None
        self._state = None
        self._referencing_databases = None

    @property
    def name(self):
        """Backup name used in requests.

        The backup name is of the form

            ``"projects/../instances/../backups/{backup_id}"``

        :rtype: str
        :returns: The backup name.
        """
        return self._instance.name + "/backups/" + self.backup_id

    @property
    def database(self):
        """Database name used in requests.

        The database name is of the form

            ``"projects/../instances/../backups/{backup_id}"``

        :rtype: str
        :returns: The database name.
        """
        return self._database

    @property
    def expire_time(self):
        """Expire time used in creation requests.

        :rtype: :class:`datetime.datetime`
        :returns: a datetime object representing the expire time of
            this backup
        """
        return self._expire_time

    @property
    def create_time(self):
        """Create time of this backup.

        :rtype: :class:`datetime.datetime`
        :returns: a datetime object representing the create time of
            this backup
        """
        return self._create_time

    @property
    def size_bytes(self):
        """Size of this backup in bytes.

        :rtype: int
        :returns: the number size of this backup measured in bytes
        """
        return self._size_bytes

    @property
    def state(self):
        """State of this backup.

        :rtype: :class:`~google.cloud.spanner_admin_database_v1.Backup.State`
        :returns: an enum describing the state of the backup
        """
        return self._state

    @property
    def referencing_databases(self):
        """List of databases referencing this backup.

        :rtype: list of strings
        :returns: a list of database path strings which specify the databases still
            referencing this backup
        """
        return self._referencing_databases

    @classmethod
    def from_pb(cls, backup_pb, instance):
        """Create an instance of this class from a protobuf message.

        :type backup_pb: :class:`~google.spanner.admin.database.v1.Backup`
        :param backup_pb: A backup protobuf object.

        :type instance: :class:`~google.cloud.spanner_v1.instance.Instance`
        :param instance: The instance that owns the backup.

        :rtype: :class:`Backup`
        :returns: The backup parsed from the protobuf response.
        :raises ValueError:
            if the backup name does not match the expected format or if
            the parsed project ID does not match the project ID on the
            instance's client, or if the parsed instance ID does not match
            the instance's ID.
        """
        match = _BACKUP_NAME_RE.match(backup_pb.name)
        if match is None:
            raise ValueError(
                "Backup protobuf name was not in the expected format.", backup_pb.name
            )
        if match.group("project") != instance._client.project:
            raise ValueError(
                "Project ID on backup does not match the project ID"
                "on the instance's client"
            )
        instance_id = match.group("instance_id")
        if instance_id != instance.instance_id:
            raise ValueError(
                "Instance ID on database does not match the instance ID"
                "on the instance"
            )
        backup_id = match.group("backup_id")
        return cls(backup_id, instance)

    def create(self):
        """Create this backup within its instance.

        :rtype: :class:`~google.api_core.operation.Operation`
        :returns: a future used to poll the status of the create request
        :raises Conflict: if the backup already exists
        :raises NotFound: if the instance owning the backup does not exist
        :raises BadRequest: if the database or expire_time values are invalid
                            or expire_time is not set
        """
        if not self._expire_time:
            raise ValueError("expire_time not set")
        if not self._database:
            raise ValueError("database not set")
        api = self._instance._client.database_admin_api
        metadata = _metadata_with_prefix(self.name)
        backup = BackupPB(database=self._database, expire_time=self.expire_time,)

        future = api.create_backup(
            parent=self._instance.name,
            backup_id=self.backup_id,
            backup=backup,
            metadata=metadata,
        )
        return future

    def exists(self):
        """Test whether this backup exists.

        :rtype: bool
        :returns: True if the backup exists, else False.
        """
        api = self._instance._client.database_admin_api
        metadata = _metadata_with_prefix(self.name)

        try:
            api.get_backup(name=self.name, metadata=metadata)
        except NotFound:
            return False
        return True

    def reload(self):
        """Reload this backup.

        Refresh the stored backup properties.

        :raises NotFound: if the backup does not exist
        """
        api = self._instance._client.database_admin_api
        metadata = _metadata_with_prefix(self.name)
        pb = api.get_backup(name=self.name, metadata=metadata)
        self._database = pb.database
        self._expire_time = pb.expire_time
        self._create_time = pb.create_time
        self._size_bytes = pb.size_bytes
        self._state = BackupPB.State(pb.state)
        self._referencing_databases = pb.referencing_databases

    def update_expire_time(self, new_expire_time):
        """Update the expire time of this backup.

        :type new_expire_time: :class:`datetime.datetime`
        :param new_expire_time: the new expire time timestamp
        """
        api = self._instance._client.database_admin_api
        metadata = _metadata_with_prefix(self.name)
        backup_update = BackupPB(name=self.name, expire_time=new_expire_time,)
        update_mask = {"paths": ["expire_time"]}
        api.update_backup(
            backup=backup_update, update_mask=update_mask, metadata=metadata
        )
        self._expire_time = new_expire_time

    def is_ready(self):
        """Test whether this backup is ready for use.

        :rtype: bool
        :returns: True if the backup state is READY, else False.
        """
        return self.state == BackupPB.State.READY

    def delete(self):
        """Delete this backup."""
        api = self._instance._client.database_admin_api
        metadata = _metadata_with_prefix(self.name)
        api.delete_backup(name=self.name, metadata=metadata)
