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
        :returns: The requested entities.
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
