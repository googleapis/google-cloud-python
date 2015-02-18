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
"""Convenience wrapper for invoking APIs/factories w/ a dataset ID."""

from gcloud.datastore.api import delete
from gcloud.datastore.api import get
from gcloud.datastore.api import put
from gcloud.datastore.batch import Batch
from gcloud.datastore.key import Key
from gcloud.datastore.query import Query
from gcloud.datastore.transaction import Transaction


class Dataset(object):
    """Convenience wrapper for invoking APIs/factories w/ a dataset ID.

    :type dataset_id: string
    :param dataset_id: (required) dataset ID to pass to proxied API methods.

    :type connection: :class:`gcloud.datastore.connection.Connection`, or None
    :param connection: (optional) connection to pass to proxied API methods
    """

    def __init__(self, dataset_id, connection=None):
        if dataset_id is None:
            raise ValueError('dataset_id required')
        self.dataset_id = dataset_id
        self.connection = connection

    def get(self, keys, missing=None, deferred=None):
        """Proxy to :func:`gcloud.datastore.api.get`.

        Passes our ``dataset_id``.
        """
        return get(keys, missing, deferred, self.connection, self.dataset_id)

    def put(self, entities):
        """Proxy to :func:`gcloud.datastore.api.put`.

        Passes our ``dataset_id``.
        """
        return put(entities, self.connection, dataset_id=self.dataset_id)

    def delete(self, keys):
        """Proxy to :func:`gcloud.datastore.api.delete`.

        Passes our ``dataset_id``.
        """
        return delete(keys, self.connection, dataset_id=self.dataset_id)

    def key(self, *path_args, **kwargs):
        """Proxy to :func:`gcloud.datastore.key.Key`.

        Passes our ``dataset_id``.
        """
        dataset_id = kwargs.pop('dataset_id', None)
        if dataset_id not in (None, self.dataset_id):
            raise ValueError('Conflicting dataset_id')
        kwargs['dataset_id'] = self.dataset_id
        return Key(*path_args, **kwargs)

    def batch(self):
        """Proxy to :func:`gcloud.datastore.batch.Batch`.

        Passes our ``dataset_id``.
        """
        return Batch(dataset_id=self.dataset_id, connection=self.connection)

    def transaction(self):
        """Proxy to :func:`gcloud.datastore.transaction.Transaction`.

        Passes our ``dataset_id``.
        """
        return Transaction(dataset_id=self.dataset_id,
                           connection=self.connection)

    def query(self,
              kind=None,
              namespace=None,
              ancestor=None,
              filters=(),
              projection=(),
              order=(),
              group_by=()):
        """Proxy to :func:`gcloud.datastore.query.Query`.

        Passes our ``dataset_id``.
        """
        return Query(self.dataset_id, kind, namespace, ancestor, filters,
                     projection, order, group_by)
