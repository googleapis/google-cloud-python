import unittest2


class Test_MetadataMixin(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.storage._helpers import _MetadataMixin
        return _MetadataMixin

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def _derivedClass(self, connection=None, path=None, **custom_fields):

        class Derived(self._getTargetClass()):
            CUSTOM_METADATA_FIELDS = custom_fields

            @property
            def connection(self):
                return connection

            @property
            def path(self):
                return path

        return Derived

    def test_connetction_is_abstract(self):
        mixin = self._makeOne()
        self.assertRaises(NotImplementedError, lambda: mixin.connection)

    def test_path_is_abstract(self):
        mixin = self._makeOne()
        self.assertRaises(NotImplementedError, lambda: mixin.path)

    def test_has_metadata_not_loaded(self):
        mixin = self._makeOne()
        self.assertEqual(mixin.has_metadata('nonesuch'), False)

    def test_has_metadata_loaded_no_field(self):
        mixin = self._makeOne(metadata={'foo': 'Foo'})
        self.assertEqual(mixin.has_metadata(), True)

    def test_has_metadata_loaded_miss(self):
        mixin = self._makeOne(metadata={'foo': 'Foo'})
        self.assertEqual(mixin.has_metadata('nonesuch'), False)

    def test_has_metadata_loaded_hit(self):
        mixin = self._makeOne(metadata={'extant': False})
        self.assertEqual(mixin.has_metadata('extant'), True)

    def test_reload_metadata(self):
        connection = _Connection({'foo': 'Foo'})
        derived = self._derivedClass(connection, '/path')()
        derived.reload_metadata()
        self.assertEqual(derived.metadata, {'foo': 'Foo'})
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'GET')
        self.assertEqual(kw[0]['path'], '/path')
        self.assertEqual(kw[0]['query_params'], {'projection': 'noAcl'})

    def test_get_metadata_eager_no_field(self):
        derived = self._derivedClass()(metadata={'extant': False})
        self.assertEqual(derived.get_metadata(), {'extant': False})

    def test_get_metadata_eager_hit(self):
        derived = self._derivedClass()(metadata={'foo': 'Foo'})
        self.assertEqual(derived.get_metadata('foo'), 'Foo')

    def test_get_metadata_lazy_hit(self):
        connection = _Connection({'foo': 'Foo'})
        derived = self._derivedClass(connection, '/path')()
        self.assertEqual(derived.get_metadata('foo'), 'Foo')
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'GET')
        self.assertEqual(kw[0]['path'], '/path')
        self.assertEqual(kw[0]['query_params'], {'projection': 'noAcl'})

    def test_get_metadata_w_custom_field(self):
        derived = self._derivedClass(foo='get_foo')()
        try:
            derived.get_metadata('foo')
        except KeyError as e:
            self.assertTrue('get_foo' in str(e))
        else:  # pragma: NO COVER
            self.assert_('KeyError not raised')

    def test_patch_metadata(self):
        connection = _Connection({'foo': 'Foo'})
        derived = self._derivedClass(connection, '/path')()
        self.assertTrue(derived.patch_metadata({'foo': 'Foo'}) is derived)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/path')
        self.assertEqual(kw[0]['data'], {'foo': 'Foo'})
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_get_acl_not_yet_loaded(self):
        class ACL(object):
            loaded = False

            def reload(self):
                self.loaded = True

        mixin = self._makeOne()
        acl = mixin.acl = ACL()
        self.assertTrue(mixin.get_acl() is acl)
        self.assertTrue(acl.loaded)

    def test_get_acl_already_loaded(self):
        class ACL(object):
            loaded = True
        mixin = self._makeOne()
        acl = mixin.acl = ACL()
        self.assertTrue(mixin.get_acl() is acl)  # no 'reload'


class _Connection(object):

    def __init__(self, *responses):
        self._responses = responses
        self._requested = []

    def api_request(self, **kw):
        self._requested.append(kw)
        response, self._responses = self._responses[0], self._responses[1:]
        return response
