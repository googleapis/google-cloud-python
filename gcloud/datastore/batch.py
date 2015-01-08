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

"""Create / interact with a batch of updates / deletes."""

from gcloud.datastore import _implicit_environ
from gcloud.datastore import datastore_v1_pb2 as datastore_pb


class Batch(object):
    """An abstraction representing a collected group of updates / deletes.

    Used to build up a bulk mutuation.

    For example, the following snippet of code will put the two ``save``
    operations and the delete operatiuon into the same mutation, and send
    them to the server in a single API request::

      >>> from gcloud import datastore
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

      >>> from gcloud import datastore
      >>> dataset = datastore.get_dataset('dataset-id')
      >>> with Batch as batch:
      ...   do_some_work(batch)
      ...   raise Exception() # rolls back
    """

    def __init__(self, dataset_id=None, connection=None):
        """ Construct a batch.

        :type dataset_id: :class:`str`.
        :param dataset_id: The ID of the dataset.

        :type connection: :class:`gcloud.datastore.connection.Connection`
        :param connection: The connection used to connect to datastore.

        :raises: :class:`ValueError` if either a connection or dataset ID
                 are not set.
        """
        self._connection = connection or _implicit_environ.CONNECTION
        self._dataset_id = dataset_id or _implicit_environ.DATASET_ID

        if self._connection is None or self._dataset_id is None:
            raise ValueError('A batch must have a connection and '
                             'a dataset ID set.')

        self._id = None
        self._mutation = datastore_pb.Mutation()

    @property
    def dataset_id(self):
        """Getter for dataset ID in which the batch will run.

        :rtype: :class:`str`
        :returns: The dataset ID in which the batch will run.
        """
        return self._dataset_id

    @property
    def connection(self):
        """Getter for connection over which the batch will run.

        :rtype: :class:`gcloud.datastore.connection.Connection`
        :returns: The connection over which the batch will run.
        """
        return self._connection

    @property
    def mutation(self):
        """Getter for the current mutation.

        Every batch is committed with a single Mutation
        representing the 'work' to be done as part of the batch.
        Inside a batch, calling ``batch.put()`` with an entity, or
        ``batch.delete`` with a key, builds up the mutation.
        This getter returns the Mutation protobuf that
        has been built-up so far.

        :rtype: :class:`gcloud.datastore.datastore_v1_pb2.Mutation`
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

        :type entity: :class:`gcloud.datastore.entity.Entity`
        :param entity: the entity to be saved.

        :raises: ValueError if entity has no key assigned.
        """
        if entity.key is None:
            raise ValueError("Entity must have a key")

        key_pb = entity.key.to_protobuf()
        properties = dict(entity)
        exclude = tuple(entity.exclude_from_indexes)

        self.connection.save_entity(
            self.dataset_id, key_pb, properties,
            exclude_from_indexes=exclude, mutation=self.mutation)

    def delete(self, key):
        """Remember a key to be deleted durring ``commit``.

        :type key: :class:`gcloud.datastore.key.Key`
        :param key: the key to be deleted.

        :raises: ValueError if key is not complete.
        """
        if key.is_partial:
            raise ValueError("Key must be complete")

        key_pb = key.to_protobuf()
        self.connection.delete_entities(
            self.dataset_id, [key_pb], mutation=self.mutation)

    def commit(self):
        """Commits the batch.

        This is called automatically upon exiting a with statement,
        however it can be called explicitly if you don't want to use a
        context manager.
        """
        self.connection.commit(self._dataset_id, self.mutation)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.commit()
