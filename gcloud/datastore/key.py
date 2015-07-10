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
import six

from gcloud.datastore import _datastore_v1_pb2 as datastore_pb


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
      >>> Key('Child', 1234, parent=parent_key)
      <Key[{'kind': 'Parent', 'name': 'foo'}, {'kind': 'Child', 'id': 1234}]>

    To create a partial key:

      >>> Key('Parent', 'foo', 'Child')
      <Key[{'kind': 'Parent', 'name': 'foo'}, {'kind': 'Child'}]>

    :type path_args: tuple of string and integer
    :param path_args: May represent a partial (odd length) or full (even
                      length) key path.

    :type kwargs: dictionary
    :param kwargs: Keyword arguments to be passed in.

    Accepted keyword arguments are
    * namespace (string): A namespace identifier for the key.
    * dataset_id (string): The dataset ID associated with the key.
    * parent (:class:`gcloud.datastore.key.Key`): The parent of the key.

    The dataset ID argument is required unless it has been set implicitly.
    """

    def __init__(self, *path_args, **kwargs):
        self._flat_path = path_args
        parent = self._parent = kwargs.get('parent')
        self._namespace = kwargs.get('namespace')
        dataset_id = kwargs.get('dataset_id')
        self._dataset_id = _validate_dataset_id(dataset_id, parent)
        # _flat_path, _parent, _namespace and _dataset_id must be set before
        # _combine_args() is called.
        self._path = self._combine_args()

    def __eq__(self, other):
        """Compare two keys for equality.

        Incomplete keys never compare equal to any other key.

        Completed keys compare equal if they have the same path, dataset ID,
        and namespace.

        :rtype: boolean
        :returns: True if the keys compare equal, else False.
        """
        if not isinstance(other, Key):
            return NotImplemented

        if self.is_partial or other.is_partial:
            return False

        return (self.flat_path == other.flat_path and
                _dataset_ids_equal(self.dataset_id, other.dataset_id) and
                self.namespace == other.namespace)

    def __ne__(self, other):
        """Compare two keys for inequality.

        Incomplete keys never compare equal to any other key.

        Completed keys compare equal if they have the same path, dataset ID,
        and namespace.

        :rtype: boolean
        :returns: False if the keys compare equal, else True.
        """
        return not self == other

    def __hash__(self):
        """Hash a keys for use in a dictionary lookp.

        :rtype: integer
        :returns: a hash of the key's state.
        """
        return (hash(self.flat_path) +
                hash(self.dataset_id) +
                hash(self.namespace))

    @staticmethod
    def _parse_path(path_args):
        """Parses positional arguments into key path with kinds and IDs.

        :type path_args: tuple
        :param path_args: A tuple from positional arguments. Should be
                          alternating list of kinds (string) and ID/name
                          parts (int or string).

        :rtype: :class:`list` of :class:`dict`
        :returns: A list of key parts with kind and ID or name set.
        :raises: :class:`ValueError` if there are no ``path_args``, if one of
                 the kinds is not a string or if one of the IDs/names is not
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
        for kind, id_or_name in zip(kind_list, id_or_name_list):
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

    def _combine_args(self):
        """Sets protected data by combining raw data set from the constructor.

        If a ``_parent`` is set, updates the ``_flat_path`` and sets the
        ``_namespace`` and ``_dataset_id`` if not already set.

        :rtype: :class:`list` of :class:`dict`
        :returns: A list of key parts with kind and ID or name set.
        :raises: :class:`ValueError` if the parent key is not complete.
        """
        child_path = self._parse_path(self._flat_path)

        if self._parent is not None:
            if self._parent.is_partial:
                raise ValueError('Parent key must be complete.')

            # We know that _parent.path() will return a copy.
            child_path = self._parent.path + child_path
            self._flat_path = self._parent.flat_path + self._flat_path
            if (self._namespace is not None and
                    self._namespace != self._parent.namespace):
                raise ValueError('Child namespace must agree with parent\'s.')
            self._namespace = self._parent.namespace
            if (self._dataset_id is not None and
                    self._dataset_id != self._parent.dataset_id):
                raise ValueError('Child dataset ID must agree with parent\'s.')
            self._dataset_id = self._parent.dataset_id

        return child_path

    def _clone(self):
        """Duplicates the Key.

        Most attributes are simple types, so don't require copying. Other
        attributes like ``parent`` are long-lived and so we re-use them.

        :rtype: :class:`gcloud.datastore.key.Key`
        :returns: A new ``Key`` instance with the same data as the current one.
        """
        cloned_self = self.__class__(*self.flat_path,
                                     dataset_id=self.dataset_id,
                                     namespace=self.namespace)
        # If the current parent has already been set, we re-use
        # the same instance
        cloned_self._parent = self._parent
        return cloned_self

    def completed_key(self, id_or_name):
        """Creates new key from existing partial key by adding final ID/name.

        :type id_or_name: string or integer
        :param id_or_name: ID or name to be added to the key.

        :rtype: :class:`gcloud.datastore.key.Key`
        :returns: A new ``Key`` instance with the same data as the current one
                  and an extra ID or name added.
        :raises: :class:`ValueError` if the current key is not partial or if
                 ``id_or_name`` is not a string or integer.
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

    def to_protobuf(self):
        """Return a protobuf corresponding to the key.

        :rtype: :class:`gcloud.datastore._datastore_v1_pb2.Key`
        :returns: The protobuf representing the key.
        """
        key = datastore_pb.Key()
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

        :rtype: boolean
        :returns: ``True`` if the last element of the key's path does not have
                  an ``id`` or a ``name``.
        """
        return self.id_or_name is None

    @property
    def namespace(self):
        """Namespace getter.

        :rtype: string
        :returns: The namespace of the current key.
        """
        return self._namespace

    @property
    def path(self):
        """Path getter.

        Returns a copy so that the key remains immutable.

        :rtype: :class:`list` of :class:`dict`
        :returns: The (key) path of the current key.
        """
        return copy.deepcopy(self._path)

    @property
    def flat_path(self):
        """Getter for the key path as a tuple.

        :rtype: tuple of string and integer
        :returns: The tuple of elements in the path.
        """
        return self._flat_path

    @property
    def kind(self):
        """Kind getter. Based on the last element of path.

        :rtype: string
        :returns: The kind of the current key.
        """
        return self.path[-1]['kind']

    @property
    def id(self):
        """ID getter. Based on the last element of path.

        :rtype: integer
        :returns: The (integer) ID of the key.
        """
        return self.path[-1].get('id')

    @property
    def name(self):
        """Name getter. Based on the last element of path.

        :rtype: string
        :returns: The (string) name of the key.
        """
        return self.path[-1].get('name')

    @property
    def id_or_name(self):
        """Getter. Based on the last element of path.

        :rtype: integer (if ``id``) or string (if ``name``)
        :returns: The last element of the key's path if it is either an ``id``
                  or a ``name``.
        """
        return self.id or self.name

    @property
    def dataset_id(self):
        """Dataset ID getter.

        :rtype: string
        :returns: The key's dataset ID.
        """
        return self._dataset_id

    def _make_parent(self):
        """Creates a parent key for the current path.

        Extracts all but the last element in the key path and creates a new
        key, while still matching the namespace and the dataset ID.

        :rtype: :class:`gcloud.datastore.key.Key` or :class:`NoneType`
        :returns: A new ``Key`` instance, whose path consists of all but the
                  last element of current path. If the current key has only
                  one path element, returns ``None``.
        """
        if self.is_partial:
            parent_args = self.flat_path[:-1]
        else:
            parent_args = self.flat_path[:-2]
        if parent_args:
            return self.__class__(*parent_args, dataset_id=self.dataset_id,
                                  namespace=self.namespace)

    @property
    def parent(self):
        """The parent of the current key.

        :rtype: :class:`gcloud.datastore.key.Key` or :class:`NoneType`
        :returns: A new ``Key`` instance, whose path consists of all but the
                  last element of current path. If the current key has only
                  one path element, returns ``None``.
        """
        if self._parent is None:
            self._parent = self._make_parent()

        return self._parent

    def __repr__(self):
        return '<Key%s, dataset=%s>' % (self.path, self.dataset_id)


def _validate_dataset_id(dataset_id, parent):
    """Ensure the dataset ID is set appropriately.

    If ``parent`` is passed, skip the test (it will be checked / fixed up
    later).

    If ``dataset_id`` is unset, attempt to infer the ID from the environment.

    :type dataset_id: string
    :param dataset_id: A dataset ID.

    :type parent: :class:`gcloud.datastore.key.Key` or ``NoneType``
    :param parent: The parent of the key or ``None``.

    :rtype: string
    :returns: The ``dataset_id`` passed in, or implied from the environment.
    :raises: :class:`ValueError` if ``dataset_id`` is ``None`` and no dataset
             can be inferred from the parent.
    """
    if parent is None:
        if dataset_id is None:
            raise ValueError("A Key must have a dataset ID set.")

    return dataset_id


def _dataset_ids_equal(dataset_id1, dataset_id2):
    """Compares two dataset IDs for fuzzy equality.

    Each may be prefixed or unprefixed (but not null, since dataset ID
    is required on a key). The only allowed prefixes are 's~' and 'e~'.

    Two identical prefixed match

      >>> 's~foo' == 's~foo'
      >>> 'e~bar' == 'e~bar'

    while non-identical prefixed don't

      >>> 's~foo' != 's~bar'
      >>> 's~foo' != 'e~foo'

    As for non-prefixed, they can match other non-prefixed or
    prefixed:

      >>> 'foo' == 'foo'
      >>> 'foo' == 's~foo'
      >>> 'foo' == 'e~foo'
      >>> 'foo' != 'bar'
      >>> 'foo' != 's~bar'

    (Ties are resolved since 'foo' can only be an alias for one of
    s~foo or e~foo in the backend.)

    :type dataset_id1: string
    :param dataset_id1: A dataset ID.

    :type dataset_id2: string
    :param dataset_id2: A dataset ID.

    :rtype: boolean
    :returns: Boolean indicating if the IDs are the same.
    """
    if dataset_id1 == dataset_id2:
        return True

    if dataset_id1.startswith('s~') or dataset_id1.startswith('e~'):
        # If `dataset_id1` is prefixed and not matching, then the only way
        # they can match is if `dataset_id2` is unprefixed.
        return dataset_id1[2:] == dataset_id2
    elif dataset_id2.startswith('s~') or dataset_id2.startswith('e~'):
        # Here we know `dataset_id1` is unprefixed and `dataset_id2`
        # is prefixed.
        return dataset_id1 == dataset_id2[2:]

    return False
