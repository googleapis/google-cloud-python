import unittest2


class TestTransaction(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.datastore.transaction import Transaction

        return Transaction

    def _makeOne(self, dataset=None):
        return self._getTargetClass()(dataset)

    def test_ctor(self):
        from gcloud.datastore.datastore_v1_pb2 import Mutation

        _DATASET = 'DATASET'
        connection = _Connection()
        dataset = _Dataset(_DATASET, connection)
        xact = self._makeOne(dataset)
        self.assertTrue(xact.dataset() is dataset)
        self.assertEqual(xact.id(), None)
        self.assertTrue(isinstance(xact.mutation(), Mutation))
        self.assertEqual(len(xact._auto_id_entities), 0)
        self.assertTrue(xact.connection() is connection)

    def test_add_auto_id_entity(self):
        entity = _Entity()
        _DATASET = 'DATASET'
        connection = _Connection()
        dataset = _Dataset(_DATASET, connection)
        xact = self._makeOne(dataset)
        xact.add_auto_id_entity(entity)
        self.assertEqual(xact._auto_id_entities, [entity])

    def test_begin(self):
        _DATASET = 'DATASET'
        connection = _Connection(234)
        dataset = _Dataset(_DATASET, connection)
        xact = self._makeOne(dataset)
        xact.begin()
        self.assertEqual(xact.id(), 234)
        self.assertEqual(connection._begun, _DATASET)
        self.assertTrue(connection._xact is xact)

    def test_rollback(self):
        _DATASET = 'DATASET'
        connection = _Connection(234)
        dataset = _Dataset(_DATASET, connection)
        xact = self._makeOne(dataset)
        xact.begin()
        xact.rollback()
        self.assertEqual(xact.id(), None)
        self.assertEqual(connection._rolled_back, _DATASET)
        self.assertEqual(connection._xact, None)

    def test_commit_no_auto_ids(self):
        _DATASET = 'DATASET'
        connection = _Connection(234)
        dataset = _Dataset(_DATASET, connection)
        xact = self._makeOne(dataset)
        xact._mutation = mutation = object()
        xact.begin()
        xact.commit()
        self.assertEqual(connection._committed, (_DATASET, mutation))
        self.assertTrue(connection._xact is None)
        self.assertEqual(xact.id(), None)

    def test_commit_w_auto_ids(self):
        _DATASET = 'DATASET'
        _KIND = 'KIND'
        _ID = 123
        connection = _Connection(234)
        connection._commit_result = _CommitResult(_makeKey(_KIND, _ID))
        dataset = _Dataset(_DATASET, connection)
        xact = self._makeOne(dataset)
        entity = _Entity()
        xact.add_auto_id_entity(entity)
        xact._mutation = mutation = object()
        xact.begin()
        xact.commit()
        self.assertEqual(connection._committed, (_DATASET, mutation))
        self.assertTrue(connection._xact is None)
        self.assertEqual(xact.id(), None)
        self.assertEqual(entity._key._path, [{'kind': _KIND, 'id': _ID}])

    def test_commit_w_already(self):
        _DATASET = 'DATASET'
        connection = _Connection(234)
        dataset = _Dataset(_DATASET, connection)
        xact = self._makeOne(dataset)
        xact._mutation = object()
        xact.begin()
        connection.transaction(())  # Simulate previous commit via false-ish.
        xact.commit()
        self.assertEqual(connection._committed, None)
        self.assertTrue(connection._xact is None)
        self.assertEqual(xact.id(), None)

    def test_context_manager_no_raise(self):
        _DATASET = 'DATASET'
        connection = _Connection(234)
        dataset = _Dataset(_DATASET, connection)
        xact = self._makeOne(dataset)
        xact._mutation = mutation = object()
        with xact:
            self.assertEqual(xact.id(), 234)
            self.assertEqual(connection._begun, _DATASET)
            self.assertTrue(connection._xact is xact)
        self.assertEqual(connection._committed, (_DATASET, mutation))
        self.assertTrue(connection._xact is None)
        self.assertEqual(xact.id(), None)

    def test_context_manager_w_raise(self):
        class Foo(Exception):
            pass
        _DATASET = 'DATASET'
        connection = _Connection(234)
        dataset = _Dataset(_DATASET, connection)
        xact = self._makeOne(dataset)
        xact._mutation = object()
        try:
            with xact:
                self.assertEqual(xact.id(), 234)
                self.assertEqual(connection._begun, _DATASET)
                self.assertTrue(connection._xact is xact)
                raise Foo()
        except Foo:
            self.assertEqual(xact.id(), None)
            self.assertEqual(connection._rolled_back, _DATASET)
            self.assertEqual(connection._xact, None)
        self.assertEqual(connection._committed, None)
        self.assertTrue(connection._xact is None)
        self.assertEqual(xact.id(), None)


def _makeKey(kind, id):
    from gcloud.datastore.datastore_v1_pb2 import Key

    key = Key()
    elem = key.path_element.add()
    elem.kind = kind
    elem.id = id
    return key


class _Dataset(object):

    def __init__(self, id, connection=None):
        self._id = id
        self._connection = connection

    def id(self):
        return self._id

    def connection(self):
        return self._connection


class _Connection(object):
    _marker = object()
    _begun = _rolled_back = _committed = _xact = None

    def __init__(self, xact_id=123):
        self._xact_id = xact_id
        self._commit_result = _CommitResult()

    def transaction(self, xact=_marker):
        if xact is self._marker:
            return self._xact
        self._xact = xact

    def begin_transaction(self, dataset_id):
        self._begun = dataset_id
        return self._xact_id

    def rollback(self, dataset_id):
        self._rolled_back = dataset_id

    def commit(self, dataset_id, mutation):
        self._committed = (dataset_id, mutation)
        return self._commit_result


class _CommitResult(object):

    def __init__(self, *new_keys):
        self.insert_auto_id_key = new_keys


class _Key(object):
    _path = None

    def path(self, path):
        self._path = path
        return self


class _Entity(object):
    _marker = object()

    def __init__(self):
        self._key = _Key()

    def key(self, key=_marker):
        if key is self._marker:
            return self._key
        self._key = key
