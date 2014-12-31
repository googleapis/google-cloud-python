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

"""Create / interact with gcloud datastore keys."""

import copy

from gcloud.datastore import datastore_v1_pb2 as datastore_pb


class Key(object):
    """An immutable representation of a datastore Key.

    .. automethod:: __init__
    """

    def __init__(self, path=None, namespace=None, dataset_id=None):
        """Constructor / initializer for a key.

        :type namespace: :class:`str`
        :param namespace: A namespace identifier for the key.

        :type path: sequence of dicts
        :param path: Each dict must have keys 'kind' (a string) and optionally
                     'name' (a string) or 'id' (an integer).

        :type dataset_id: string
        :param dataset: The dataset ID assigned by back-end for the key.

        .. note::
           The key's ``_dataset_id`` field must be None for keys created
           by application code.  The
           :func:`gcloud.datastore.helpers.key_from_protobuf` factory
           will be set the field to an appropriate value for keys
           returned from the datastore backend.  The application
           **must** treat any value set by the back-end as opaque.
        """
        self._path = path or [{'kind': ''}]
        self._parent = None
        self._namespace = namespace
        self._dataset_id = dataset_id

    def _clone(self):
        """Duplicates the Key.

        We make a shallow copy of the :class:`gcloud.datastore.dataset.Dataset`
        because it holds a reference an authenticated connection,
        which we don't want to lose.

        :rtype: :class:`gcloud.datastore.key.Key`
        :returns: a new `Key` instance
        """
        return copy.deepcopy(self)

    def to_protobuf(self):
        """Return a protobuf corresponding to the key.

        :rtype: :class:`gcloud.datastore.datastore_v1_pb2.Key`
        :returns: The Protobuf representing the key.
        """
        key = datastore_pb.Key()

        if self.dataset_id is not None:
            key.partition_id.dataset_id = self.dataset_id

        if self._namespace:
            key.partition_id.namespace = self._namespace

        for item in self.path:
            element = key.path_element.add()
            if 'kind' in item:
                element.kind = item['kind']
            if 'id' in item:
                element.id = item['id']
            if 'name' in item:
                element.name = item['name']

        return key

    @property
    def is_partial(self):
        """Boolean indicating if the key has an ID (or name).

        :rtype: :class:`bool`
        :returns: True if the last element of the key's path does not have
                  an 'id' or a 'name'.
        """
        return self.id_or_name is None

    @property
    def namespace(self):
        """Namespace getter.

        :rtype: :class:`str`
        :returns: The namespace of the current key.
        """
        return self._namespace

    @property
    def path(self):
        """Path getter.

        Returns a copy so that the key remains immutable.

        :rtype: :class:`str`
        :returns: The (key) path of the current key.
        """
        return copy.deepcopy(self._path)

    @property
    def kind(self):
        """Kind getter. Based on the last element of path.

        :rtype: :class:`str`
        :returns: The kind of the current key.
        """
        if self.path:
            return self.path[-1].get('kind')

    @property
    def id(self):
        """ID getter. Based on the last element of path.

        :rtype: :class:`int`
        :returns: The (integer) ID of the key.
        """
        if self.path:
            return self.path[-1].get('id')

    @property
    def name(self):
        """Name getter. Based on the last element of path.

        :rtype: :class:`str`
        :returns: The (string) name of the key.
        """
        if self.path:
            return self.path[-1].get('name')

    @property
    def id_or_name(self):
        """Getter. Based on the last element of path.

        :rtype: :class:`int` (if 'id') or :class:`str` (if 'name')
        :returns: The last element of the key's path if it is either an 'id'
                  or a 'name'.
        """
        return self.id or self.name

    @property
    def dataset_id(self):
        """Dataset ID getter.

        :rtype: :class:`str`
        :returns: The key's dataset.
        """
        return self._dataset_id

    def _make_parent(self):
        """Creates a parent key for the current path.

        Extracts all but the last element in the key path and creates a new
        key, while still matching the namespace and the dataset ID.

        :rtype: :class:`gcloud.datastore.key.Key` or `NoneType`
        :returns: a new `Key` instance, whose path consists of all but the last
                  element of self's path. If self has only one path element,
                  returns None.
        """
        parent_path = self.path[:-1]
        if parent_path:
            return Key(path=parent_path, dataset_id=self.dataset_id,
                       namespace=self.namespace)

    @property
    def parent(self):
        """Getter:  return a new key for the next highest element in path.

        :rtype: :class:`gcloud.datastore.key.Key` or `NoneType`
        :returns: a new `Key` instance, whose path consists of all but the last
                  element of self's path.  If self has only one path element,
                  returns None.
        """
        if self._parent is None:
            self._parent = self._make_parent()

        return self._parent

    def __repr__(self):
        return '<Key%s>' % self.path
