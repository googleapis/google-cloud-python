# Copyright 2014 Google Inc. All rights reserved.
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

"""Create / interact with a batch of updates / deletes.

Batches provide the ability to execute multiple operations
in a single request to the Cloud Datastore API.

See
https://cloud.google.com/datastore/docs/concepts/entities#Datastore_Batch_operations
"""

from gcloud.datastore import helpers
from gcloud.datastore.key import _dataset_ids_equal
from gcloud.datastore._generated import datastore_pb2 as _datastore_pb2


class Batch(object):
    """An abstraction representing a collected group of updates / deletes.

    Used to build up a bulk mutuation.

    For example, the following snippet of code will put the two ``save``
    operations and the delete operatiuon into the same mutation, and send
    them to the server in a single API request::

      >>> from gcloud.datastore.batch import Batch
      >>> batch = Batch()
      >>> batch.put(entity1)
      >>> batch.put(entity2)
      >>> batch.delete(key3)
      >>> batch.commit()

    You can also use a batch as a context manager, in which case the
    ``commit`` will be called automatically if its block exits without
    raising an exception::

      >>> with Batch() as batch:
      ...     batch.put(entity1)
      ...     batch.put(entity2)
      ...     batch.delete(key3)

    By default, no updates will be sent if the block exits with an error::

      >>> with Batch() as batch:
      ...   do_some_work(batch)
      ...   raise Exception() # rolls back

    :type client: :class:`gcloud.datastore.client.Client`
    :param client: The client used to connect to datastore.
    """
    _id = None  # "protected" attribute, always None for non-transactions

    def __init__(self, client):
        self._client = client
        self._mutation = _datastore_pb2.Mutation()
        self._partial_key_entities = []

    def current(self):
        """Return the topmost batch / transaction, or None."""
        return self._client.current_batch

    @property
    def dataset_id(self):
        """Getter for dataset ID in which the batch will run.

        :rtype: :class:`str`
        :returns: The dataset ID in which the batch will run.
        """
        return self._client.dataset_id

    @property
    def namespace(self):
        """Getter for namespace in which the batch will run.

        :rtype: :class:`str`
        :returns: The namespace in which the batch will run.
        """
        return self._client.namespace

    @property
    def connection(self):
        """Getter for connection over which the batch will run.

        :rtype: :class:`gcloud.datastore.connection.Connection`
        :returns: The connection over which the batch will run.
        """
        return self._client.connection

    def _add_partial_key_entity_pb(self):
        """Adds a new mutation for an entity with a partial key.

        :rtype: :class:`gcloud.datastore._generated.entity_pb2.Entity`
        :returns: The newly created entity protobuf that will be
                  updated and sent with a commit.
        """
        return self.mutations.insert_auto_id.add()

    def _add_complete_key_entity_pb(self):
        """Adds a new mutation for an entity with a completed key.

        :rtype: :class:`gcloud.datastore._generated.entity_pb2.Entity`
        :returns: The newly created entity protobuf that will be
                  updated and sent with a commit.
        """
        return self.mutations.upsert.add()

    def _add_delete_key_pb(self):
        """Adds a new mutation for a key to be deleted.

        :rtype: :class:`gcloud.datastore._generated.entity_pb2.Key`
        :returns: The newly created key protobuf that will be
                  deleted when sent with a commit.
        """
        return self.mutations.delete.add()

    @property
    def mutations(self):
        """Getter for the changes accumulated by this batch.

        Every batch is committed with a single Mutation
        representing the 'work' to be done as part of the batch.
        Inside a batch, calling ``batch.put()`` with an entity, or
        ``batch.delete`` with a key, builds up the mutation.
        This getter returns the Mutation protobuf that
        has been built-up so far.

        :rtype: :class:`gcloud.datastore._generated.datastore_pb2.Mutation`
        :returns: The Mutation protobuf to be sent in the commit request.
        """
        return self._mutation

    def put(self, entity):
        """Remember an entity's state to be saved during ``commit``.

        .. note::
           Any existing properties for the entity will be replaced by those
           currently set on this instance.  Already-stored properties which do
           not correspond to keys set on this instance will be removed from
           the datastore.

        .. note::
           Property values which are "text" ('unicode' in Python2, 'str' in
           Python3) map to 'string_value' in the datastore;  values which are
           "bytes" ('str' in Python2, 'bytes' in Python3) map to 'blob_value'.

        When an entity has a partial key, calling :meth:`commit`` sends it as
        an ``insert_auto_id`` mutation and the key is completed. On return, the
        key for the ``entity`` passed in as updated to match the key ID
        assigned by the server.

        :type entity: :class:`gcloud.datastore.entity.Entity`
        :param entity: the entity to be saved.

        :raises: ValueError if entity has no key assigned, or if the key's
                 ``dataset_id`` does not match ours.
        """
        if entity.key is None:
            raise ValueError("Entity must have a key")

        if not _dataset_ids_equal(self.dataset_id, entity.key.dataset_id):
            raise ValueError("Key must be from same dataset as batch")

        if entity.key.is_partial:
            entity_pb = self._add_partial_key_entity_pb()
            self._partial_key_entities.append(entity)
        else:
            entity_pb = self._add_complete_key_entity_pb()

        _assign_entity_to_pb(entity_pb, entity)

    def delete(self, key):
        """Remember a key to be deleted durring ``commit``.

        :type key: :class:`gcloud.datastore.key.Key`
        :param key: the key to be deleted.

        :raises: ValueError if key is not complete, or if the key's
                 ``dataset_id`` does not match ours.
        """
        if key.is_partial:
            raise ValueError("Key must be complete")

        if not _dataset_ids_equal(self.dataset_id, key.dataset_id):
            raise ValueError("Key must be from same dataset as batch")

        key_pb = helpers._prepare_key_for_request(key.to_protobuf())
        self._add_delete_key_pb().CopyFrom(key_pb)

    def begin(self):
        """No-op

        Overridden by :class:`gcloud.datastore.transaction.Transaction`.
        """

    def commit(self):
        """Commits the batch.

        This is called automatically upon exiting a with statement,
        however it can be called explicitly if you don't want to use a
        context manager.
        """
        _, updated_keys = self.connection.commit(
            self.dataset_id, self.mutations, self._id)
        # If the back-end returns without error, we are guaranteed that
        # the response's 'insert_auto_id_key' will match (length and order)
        # the request's 'insert_auto_id` entities, which are derived from
        # our '_partial_key_entities' (no partial success).
        for new_key_pb, entity in zip(updated_keys,
                                      self._partial_key_entities):
            new_id = new_key_pb.path_element[-1].id
            entity.key = entity.key.completed_key(new_id)

    def rollback(self):
        """No-op

        Overridden by :class:`gcloud.datastore.transaction.Transaction`.
        """
        pass

    def __enter__(self):
        self._client._push_batch(self)
        self.begin()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is None:
                self.commit()
            else:
                self.rollback()
        finally:
            self._client._pop_batch()


def _assign_entity_to_pb(entity_pb, entity):
    """Copy ``entity`` into ``entity_pb``.

    Helper method for ``Batch.put``.

    :type entity_pb: :class:`gcloud.datastore._generated.entity_pb2.Entity`
    :param entity_pb: The entity owned by a mutation.

    :type entity: :class:`gcloud.datastore.entity.Entity`
    :param entity: The entity being updated within the batch / transaction.
    """
    bare_entity_pb = helpers.entity_to_protobuf(entity)
    key_pb = helpers._prepare_key_for_request(bare_entity_pb.key)
    bare_entity_pb.key.CopyFrom(key_pb)
    entity_pb.CopyFrom(bare_entity_pb)
