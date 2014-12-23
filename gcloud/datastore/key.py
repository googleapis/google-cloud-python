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
from itertools import izip
import six

from gcloud.datastore import datastore_v1_pb2 as datastore_pb


class Key(object):
    """An immutable representation of a datastore Key.

    To create a basic key:

      >>> Key('EntityKind', 1234)
      <Key[{'kind': 'EntityKind', 'id': 1234}]>
      >>> Key('EntityKind', 'foo')
      <Key[{'kind': 'EntityKind', 'name': 'foo'}]>

    To create a key with a parent:

      >>> Key('Parent', 'foo', 'Child', 1234)
      <Key[{'kind': 'Parent', 'name': 'foo'}, {'kind': 'Child', 'id': 1234}]>

    To create a paritial key:

      >>> Key('Parent', 'foo', 'Child')
      <Key[{'kind': 'Parent', 'name': 'foo'}, {'kind': 'Child'}]>

    .. automethod:: __init__
    """

    def __init__(self, *path_args, **kwargs):
        """Constructor / initializer for a key.

        :type path_args: tuple of strings and ints
        :param path_args: May represent a partial (odd length) or full (even
                          length) key path.

        :type namespace: :class:`str`
        :param namespace: A namespace identifier for the key. Can only be
                          passed as a keyword argument.

        :type dataset_id: string
        :param dataset_id: The dataset ID associated with the key. Can only be
                           passed as a keyword argument.

        # This note will be obsolete by the end of #451.

        .. note::
           The key's ``_dataset_id`` field must be None for keys created
           by application code.  The
           :func:`gcloud.datastore.helpers.key_from_protobuf` factory
           will be set the field to an appropriate value for keys
           returned from the datastore backend.  The application
           **must** treat any value set by the back-end as opaque.
        """
        self._path = self._parse_path(path_args)
        self._flat_path = path_args
        self._parent = None
        self._namespace = kwargs.get('namespace')
        self._dataset_id = kwargs.get('dataset_id')

    @staticmethod
    def _parse_path(path_args):
        """Parses positional arguments into key path with kinds and IDs.

        :rtype: list of dict
        :returns: A list of key parts with kind and id or name set.
        :raises: `ValueError` if there are no `path_args`, if one of the
                 kinds is not a string or if one of the IDs/names is not
                 a string or an integer.
        """
        if len(path_args) == 0:
            raise ValueError('Key path must not be empty.')

        kind_list = path_args[::2]
        id_or_name_list = path_args[1::2]
        # Dummy sentinel value to pad incomplete key to even length path.
        partial_ending = object()
        if len(path_args) % 2 == 1:
            id_or_name_list += (partial_ending,)

        result = []
        for kind, id_or_name in izip(kind_list, id_or_name_list):
            curr_key_part = {}
            if isinstance(kind, six.string_types):
                curr_key_part['kind'] = kind
            else:
                raise ValueError(kind, 'Kind was not a string.')

            if isinstance(id_or_name, six.string_types):
                curr_key_part['name'] = id_or_name
            elif isinstance(id_or_name, six.integer_types):
                curr_key_part['id'] = id_or_name
            elif id_or_name is not partial_ending:
                raise ValueError(id_or_name,
                                 'ID/name was not a string or integer.')

            result.append(curr_key_part)

        return result

    def _clone(self):
        """Duplicates the Key.

        We make a shallow copy of the :class:`gcloud.datastore.dataset.Dataset`
        because it holds a reference an authenticated connection,
        which we don't want to lose.

        :rtype: :class:`gcloud.datastore.key.Key`
        :returns: a new `Key` instance
        """
        return copy.deepcopy(self)

    def completed_key(self, id_or_name):
        """Creates new key from existing partial key by adding final ID/name.

        :rtype: :class:`gcloud.datastore.key.Key`
        :returns: A new `Key` instance with the same data as the current one
                  and an extra ID or name added.
        :raises: `ValueError` if the current key is not partial or if
                 `id_or_name` is not a string or integer.
        """
        if not self.is_partial:
            raise ValueError('Only a partial key can be completed.')

        id_or_name_key = None
        if isinstance(id_or_name, six.string_types):
            id_or_name_key = 'name'
        elif isinstance(id_or_name, six.integer_types):
            id_or_name_key = 'id'
        else:
            raise ValueError(id_or_name,
                             'ID/name was not a string or integer.')

        new_key = self._clone()
        new_key._path[-1][id_or_name_key] = id_or_name
        new_key._flat_path += (id_or_name,)
        return new_key

    def _validate_protobuf_dataset_id(self, protobuf):
        """Checks that dataset ID on protobuf matches current one.

        The value of the dataset ID may have changed from unprefixed
        (e.g. 'foo') to prefixed (e.g. 's~foo' or 'e~foo').

        :type protobuf: :class:`gcloud.datastore.datastore_v1_pb2.Key`
        :param protobuf: A protobuf representation of the key. Expected to be
                         returned after a datastore operation.

        :rtype: :class:`str`
        """
        proto_dataset_id = protobuf.partition_id.dataset_id
        if proto_dataset_id == self.dataset_id:
            return

        # Since they don't match, we check to see if `proto_dataset_id` has a
        # prefix.
        unprefixed = None
        prefix = proto_dataset_id[:2]
        if prefix in ('s~', 'e~'):
            unprefixed = proto_dataset_id[2:]

        if unprefixed != self.dataset_id:
            raise ValueError('Dataset ID on protobuf does not match.',
                             proto_dataset_id, self.dataset_id)

    def compare_to_proto(self, protobuf):
        """Checks current key against a protobuf; updates if partial.

        If the current key is partial, returns a new key that has been
        completed otherwise returns the current key.

        The value of the dataset ID may have changed from implicit (i.e. None,
        with the ID implied from the dataset.Dataset object associated with the
        Entity/Key), but if it was implicit before, we leave it as implicit.

        :type protobuf: :class:`gcloud.datastore.datastore_v1_pb2.Key`
        :param protobuf: A protobuf representation of the key. Expected to be
                         returned after a datastore operation.

        :rtype: :class:`gcloud.datastore.key.Key`
        :returns: The current key if not partial.
        :raises: `ValueError` if the namespace or dataset ID of `protobuf`
                 don't match the current values or if the path from `protobuf`
                 doesn't match.
        """
        if self.namespace is None:
            if protobuf.partition_id.HasField('namespace'):
                raise ValueError('Namespace unset on key but set on protobuf.')
        elif protobuf.partition_id.namespace != self.namespace:
            raise ValueError('Namespace on protobuf does not match.',
                             protobuf.partition_id.namespace, self.namespace)

        # Check that dataset IDs match if not implicit.
        if self.dataset_id is not None:
            self._validate_protobuf_dataset_id(protobuf)

        path = []
        for element in protobuf.path_element:
            key_part = {}
            for descriptor, value in element._fields.items():
                key_part[descriptor.name] = value
            path.append(key_part)

        if path == self.path:
            return self

        if not self.is_partial:
            raise ValueError('Proto path does not match completed key.',
                             path, self.path)

        last_part = path[-1]
        id_or_name = None
        if 'id' in last_part:
            id_or_name = last_part.pop('id')
        elif 'name' in last_part:
            id_or_name = last_part.pop('name')

        # We have edited path by popping from the last part, so check again.
        if path != self.path:
            raise ValueError('Proto path does not match partial key.',
                             path, self.path)

        return self.complete_key(id_or_name)

    def to_protobuf(self):
        """Return a protobuf corresponding to the key.

        :rtype: :class:`gcloud.datastore.datastore_v1_pb2.Key`
        :returns: The Protobuf representing the key.
        """
        key = datastore_pb.Key()

        if self.dataset_id is not None:
            key.partition_id.dataset_id = self.dataset_id

        if self.namespace:
            key.partition_id.namespace = self.namespace

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
    def flat_path(self):
        """Getter for the key path as a tuple.

        :rtype: :class:`tuple` of string and int
        :returns: The tuple of elements in the path.
        """
        return self._flat_path

    @property
    def kind(self):
        """Kind getter. Based on the last element of path.

        :rtype: :class:`str`
        :returns: The kind of the current key.
        """
        return self.path[-1]['kind']

    @property
    def id(self):
        """ID getter. Based on the last element of path.

        :rtype: :class:`int`
        :returns: The (integer) ID of the key.
        """
        return self.path[-1].get('id')

    @property
    def name(self):
        """Name getter. Based on the last element of path.

        :rtype: :class:`str`
        :returns: The (string) name of the key.
        """
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
        if self.is_partial:
            parent_args = self.flat_path[:-1]
        else:
            parent_args = self.flat_path[:-2]
        if parent_args:
            return Key(*parent_args, dataset_id=self.dataset_id,
                       namespace=self.namespace)

    @property
    def parent(self):
        """The parent of the current key.

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
