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

"""Create / interact with gcloud datastore datasets."""

from gcloud.datastore import helpers
from gcloud.datastore.entity import Entity
from gcloud.datastore.query import Query
from gcloud.datastore.transaction import Transaction
from gcloud.datastore.key import Key


class Dataset(object):
    """A dataset in the Cloud Datastore.

    This class acts as an abstraction of a single dataset in the Cloud
    Datastore.

    A dataset is analogous to a database in relational database world,
    and corresponds to a single project using the Cloud Datastore.

    Typically, you would only have one of these per connection however
    it didn't seem right to collapse the functionality of a connection
    and a dataset together into a single class.

    Datasets (like :class:`gcloud.datastore.query.Query`) are immutable.
    That is, you cannot change the ID and connection references.  If you
    need to modify the connection or ID, it's recommended to construct a
    new :class:`Dataset`.

    :type id: string
    :param id: The ID of the dataset (your project ID)

    :type connection: :class:`gcloud.datastore.connection.Connection`
    :param connection: The connection to use for executing API calls.
    """

    def __init__(self, id, connection=None):
        self._connection = connection
        self._id = id

    def connection(self):
        """Get the current connection.

          >>> dataset = Dataset('dataset-id', connection=conn)
          >>> dataset.connection()
          <Connection object>

        :rtype: :class:`gcloud.datastore.connection.Connection`
        :returns: Returns the current connection.
        """

        return self._connection

    def id(self):
        """Get the current dataset ID.

          >>> dataset = Dataset('dataset-id', connection=conn)
          >>> dataset.id()
          'dataset-id'

        :rtype: string
        :returns: The current dataset ID.
        """

        return self._id

    def query(self, *args, **kwargs):
        """Create a query bound to this dataset.

        :param args: positional arguments, passed through to the Query

        :param kw: keyword arguments, passed through to the Query

        :rtype: :class:`gcloud.datastore.query.Query`
        :returns: a new Query instance, bound to this dataset.
        """
        kwargs['dataset'] = self
        return Query(*args, **kwargs)

    def entity(self, kind, exclude_from_indexes=()):
        """Create an entity bound to this dataset.

        :type kind: string
        :param kind: the "kind" of the new entity (see
                 https://cloud.google.com/datastore/docs/concepts/entities#Datastore_Kinds_and_identifiers)

        :param exclude_from_indexes: names of fields whose values are not to
                                     be indexed.

        :rtype: :class:`gcloud.datastore.entity.Entity`
        :returns: a new Entity instance, bound to this dataset.
        """
        return Entity(dataset=self, kind=kind,
                      exclude_from_indexes=exclude_from_indexes)

    def transaction(self, *args, **kwargs):
        """Create a transaction bound to this dataset.

        :param args: positional arguments, passed through to the Transaction

        :param kw: keyword arguments, passed through to the Transaction

        :rtype: :class:`gcloud.datastore.transaction.Transaction`
        :returns: a new Transaction instance, bound to this dataset.
        """
        kwargs['dataset'] = self
        return Transaction(*args, **kwargs)

    def get_entity(self, key_or_path):
        """Retrieves entity from the dataset, along with its attributes.

        :type key_or_path: :class:`gcloud.datastore.key.Key` or path
        :param key_or_path: The name of the item to retrieve or sequence
                            of even length, where the first of each pair
                            is a string representing the 'kind' of the
                            path element, and the second of the pair is
                            either a string (for the path element's name)
                            or an integer (for its id).

        :rtype: :class:`gcloud.datastore.entity.Entity` or ``None``
        :return: The requested entity, or ``None`` if there was no match found.
        """

        if isinstance(key_or_path, Key):
            entities = self.get_entities([key_or_path])
        else:
            key = Key(*key_or_path)
            entities = self.get_entities([key])

        if entities:
            return entities[0]

    def get_entities(self, keys, missing=None, deferred=None):
        """Retrieves entities from the dataset, along with their attributes.

        :type keys: list of :class:`gcloud.datastore.key.Key`
        :param keys: List of keys to be retrieved.

        :type missing: an empty list or None.
        :param missing: If a list is passed, the key-only entities returned
                        by the backend as "missing" will be copied into it.
                        Use only as a keyword param.

        :type deferred: an empty list or None.
        :param deferred: If a list is passed, the keys returned
                        by the backend as "deferred" will be copied into it.
                        Use only as a keyword param.

        :rtype: list of :class:`gcloud.datastore.entity.Entity`
        :return: The requested entities.
        """
        entity_pbs = self.connection().lookup(
            dataset_id=self.id(),
            key_pbs=[k.to_protobuf() for k in keys],
            missing=missing, deferred=deferred,
        )

        if missing is not None:
            missing[:] = [
                helpers.entity_from_protobuf(missed_pb, dataset=self)
                for missed_pb in missing]

        if deferred is not None:
            deferred[:] = [
                helpers.key_from_protobuf(deferred_pb)
                for deferred_pb in deferred]

        entities = []
        for entity_pb in entity_pbs:
            entities.append(helpers.entity_from_protobuf(
                entity_pb, dataset=self))
        return entities

    def allocate_ids(self, incomplete_key, num_ids):
        """Allocates a list of IDs from a partial key.

        :type incomplete_key: A :class:`gcloud.datastore.key.Key`
        :param incomplete_key: Partial key to use as base for allocated IDs.

        :type num_ids: A :class:`int`.
        :param num_ids: The number of IDs to allocate.

        :rtype: list of :class:`gcloud.datastore.key.Key`
        :return: The (complete) keys allocated with `incomplete_key` as root.
        :raises: `ValueError` if `incomplete_key` is not a partial key.
        """
        if not incomplete_key.is_partial:
            raise ValueError(('Key is not partial.', incomplete_key))

        incomplete_key_pb = incomplete_key.to_protobuf()
        incomplete_key_pbs = [incomplete_key_pb] * num_ids

        allocated_key_pbs = self.connection().allocate_ids(
            self.id(), incomplete_key_pbs)
        allocated_ids = [allocated_key_pb.path_element[-1].id
                         for allocated_key_pb in allocated_key_pbs]
        return [incomplete_key.complete_key(allocated_id)
                for allocated_id in allocated_ids]
