import copy
from itertools import izip

from gcloud.datastore import datastore_v1_pb2 as datastore_pb
from gcloud.datastore.dataset import Dataset


class Key(object):
    """An immutable representation of a datastore Key.

    .. automethod:: __init__
    """

    def __init__(self, dataset=None, namespace=None, path=None):
        """Constructor / initializer for a key.

        :type dataset: :class:`gcloud.datastore.dataset.Dataset`
        :param dataset: A dataset instance for the key.

        :type namespace: :class:`str`
        :param namespace: A namespace identifier for the key.

        :type path: sequence of dicts
        :param path: Each dict must have keys 'kind' (a string) and optionally
                     'name' (a string) or 'id' (an integer).
        """
        self._dataset = dataset
        self._namespace = namespace
        self._path = path or [{'kind': ''}]

    def _clone(self):
        """Duplicates the Key.

        We make a shallow copy of the :class:`gcloud.datastore.dataset.Dataset`
        because it holds a reference an authenticated connection,
        which we don't want to lose.

        :rtype: :class:`gcloud.datastore.key.Key`
        :returns: a new `Key` instance
        """
        clone = copy.deepcopy(self)
        clone._dataset = self._dataset  # Make a shallow copy of the Dataset.
        return clone

    @classmethod
    def from_protobuf(cls, pb, dataset=None):
        """Factory method for creating a key based on a protobuf.

        The protobuf should be one returned from the Cloud Datastore
        Protobuf API.

        :type pb: :class:`gcloud.datastore.datastore_v1_pb2.Key`
        :param pb: The Protobuf representing the key.

        :type dataset: :class:`gcloud.datastore.dataset.Dataset`
        :param dataset: A dataset instance.  If not passed, defaults to an
                        instance whose ID is derived from pb.

        :rtype: :class:`gcloud.datastore.key.Key`
        :returns: a new `Key` instance
        """
        path = []
        for element in pb.path_element:
            element_dict = {'kind': element.kind}

            if element.HasField('id'):
                element_dict['id'] = element.id

            elif element.HasField('name'):
                element_dict['name'] = element.name

            path.append(element_dict)

        if not dataset:
            dataset = Dataset(id=pb.partition_id.dataset_id)
            namespace = pb.partition_id.namespace
        else:
            namespace = None

        return cls(dataset, namespace, path)

    def to_protobuf(self):
        """Return a protobuf corresponding to the key.

        :rtype: :class:`gcloud.datastore.datastore_v1_pb2.Key`
        :returns: The Protobuf representing the key.
        """
        key = datastore_pb.Key()

        # Technically a dataset is required to do anything with the key,
        # but we shouldn't throw a cryptic error if one isn't provided
        # in the initializer.
        if self.dataset():
            # Apparently 's~' is a prefix for High-Replication and is necessary
            # here. Another valid preflix is 'e~' indicating EU datacenters.
            dataset_id = self.dataset().id()
            if dataset_id:
                if dataset_id[:2] not in ['s~', 'e~']:
                    dataset_id = 's~' + dataset_id

                key.partition_id.dataset_id = dataset_id

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
        return (self.id_or_name() is None)

    def dataset(self, dataset=None):
        """Dataset setter / getter.

        :type dataset: :class:`gcloud.datastore.dataset.Dataset`
        :param dataset: A dataset instance for the key.

        :rtype: :class:`Key` (for setter); or
                :class:`gcloud.datastore.dataset.Dataset` (for getter)
        :returns: a new key, cloned from self., with the given dataset
                  (setter); or self's dataset (getter).
        """
        if dataset:
            clone = self._clone()
            clone._dataset = dataset
            return clone
        else:
            return self._dataset

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

    def id(self, id=None):
        """ID setter / getter.  Based on the last element of path.

        :type kind: :class:`str`
        :param kind: The new kind for the key.

        :rtype: :class:`Key` (for setter); or :class:`int` (for getter)
        :returns: a new key, cloned from self., with the given id (setter);
                 or self's id (getter).
        """
        if id:
            clone = self._clone()
            clone._path[-1]['id'] = id
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

    def parent(self):  # pragma NO COVER
        """Getter:  return a new key for the next highest element in path.

        :rtype: :class:`gcloud.datastore.key.Key`
        :returns: a new `Key` instance, whose path consists of all but the last
                  element of self's path.  If self has only one path element,
                  return None.
        """
        if len(self._path) <= 1:
            return None
        return self.path(self.path()[:-1])

    def __repr__(self):  # pragma NO COVER
        return '<Key%s>' % self.path()
