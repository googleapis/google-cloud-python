"""Create / interact with gcloud datastore keys."""

import copy
from itertools import izip

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
           will be set the field to an appropriate value for keys returned
           from the datastore backend.  The application **must** treat any
           value set by the back-end as opaque.
        """
        self._path = path or [{'kind': ''}]
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

        if self._dataset_id is not None:
            key.partition_id.dataset_id = self._dataset_id

        if self._namespace:
            key.partition_id.namespace = self._namespace

        for item in self.path():
            element = key.path_element.add()
            if 'kind' in item:
                element.kind = item['kind']
            if 'id' in item:
                element.id = item['id']
            if 'name' in item:
                element.name = item['name']

        return key

    @classmethod
    def from_path(cls, *args, **kwargs):
        """Factory method for creating a key based on a path.

        :type args: :class:`tuple`
        :param args: sequence of even length, where the first of each pair is a
                     string representing the 'kind' of the path element, and
                     the second of the pair is either a string (for the path
                     element's name) or an integer (for its id).

        :type kwargs: :class:`dict`
        :param kwargs: Other named parameters which can be passed to
                       :func:`Key.__init__`.

        :rtype: :class:`gcloud.datastore.key.Key`
        :returns: a new :class:`Key` instance
        """
        if len(args) % 2:
            raise ValueError('Must pass an even number of args.')

        path = []
        items = iter(args)

        for kind, id_or_name in izip(items, items):
            entry = {'kind': kind}
            if isinstance(id_or_name, basestring):
                entry['name'] = id_or_name
            else:
                entry['id'] = id_or_name
            path.append(entry)

        kwargs['path'] = path
        return cls(**kwargs)

    def is_partial(self):
        """Boolean test: is the key fully mapped onto a backend entity?

        :rtype: :class:`bool`
        :returns: True if the last element of the key's path does not have
                  an 'id' or a 'name'.
        """
        return self.id_or_name() is None

    def namespace(self, namespace=None):
        """Namespace setter / getter.

        :type namespace: :class:`str`
        :param namespace: A namespace identifier for the key.

        :rtype: :class:`Key` (for setter); or :class:`str` (for getter)
        :returns: a new key, cloned from self., with the given namespace
                  (setter); or self's namespace (getter).
        """
        if namespace:
            clone = self._clone()
            clone._namespace = namespace
            return clone
        else:
            return self._namespace

    def path(self, path=None):
        """Path setter / getter.

        :type path: sequence of dicts
        :param path: Each dict must have keys 'kind' (a string) and optionally
                     'name' (a string) or 'id' (an integer).

        :rtype: :class:`Key` (for setter); or :class:`str` (for getter)
        :returns: a new key, cloned from self., with the given path (setter);
                 or self's path (getter).
        """
        if path:
            clone = self._clone()
            clone._path = path
            return clone
        else:
            return self._path

    def kind(self, kind=None):
        """Kind setter / getter.  Based on the last element of path.

        :type kind: :class:`str`
        :param kind: The new kind for the key.

        :rtype: :class:`Key` (for setter); or :class:`str` (for getter)
        :returns: a new key, cloned from self., with the given kind (setter);
                 or self's kind (getter).
        """
        if kind:
            clone = self._clone()
            clone._path[-1]['kind'] = kind
            return clone
        elif self.path():
            return self._path[-1]['kind']

    def id(self, id_to_set=None):
        """ID setter / getter.  Based on the last element of path.

        :type id_to_set: :class:`int`
        :param id_to_set: The new ID for the key.

        :rtype: :class:`Key` (for setter); or :class:`int` (for getter)
        :returns: a new key, cloned from self., with the given id (setter);
                  or self's id (getter).
        """
        if id_to_set:
            clone = self._clone()
            clone._path[-1]['id'] = id_to_set
            return clone
        elif self.path():
            return self._path[-1].get('id')

    def name(self, name=None):
        """Name setter / getter.  Based on the last element of path.

        :type kind: :class:`str`
        :param kind: The new name for the key.

        :rtype: :class:`Key` (for setter); or :class:`str` (for getter)
        :returns: a new key, cloned from self., with the given name (setter);
                 or self's name (getter).
        """
        if name:
            clone = self._clone()
            clone._path[-1]['name'] = name
            return clone
        elif self.path():
            return self._path[-1].get('name')

    def id_or_name(self):
        """Getter.  Based on the last element of path.

        :rtype: :class:`int` (if 'id' is set); or :class:`str` (the 'name')
        :returns: True if the last element of the key's path has either an 'id'
                  or a 'name'.
        """
        return self.id() or self.name()

    def parent(self):
        """Getter:  return a new key for the next highest element in path.

        :rtype: :class:`gcloud.datastore.key.Key`
        :returns: a new `Key` instance, whose path consists of all but the last
                  element of self's path.  If self has only one path element,
                  return None.
        """
        if len(self._path) <= 1:
            return None
        return self.path(self.path()[:-1])

    def __repr__(self):
        return '<Key%s>' % self.path()
