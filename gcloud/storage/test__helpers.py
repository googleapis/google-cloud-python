import unittest2


class Test_PropertyMixin(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.storage._helpers import _PropertyMixin
        return _PropertyMixin

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def _derivedClass(self, connection=None, path=None, **custom_fields):

        class Derived(self._getTargetClass()):
            CUSTOM_PROPERTY_ACCESSORS = custom_fields

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

    def test__reload_properties(self):
        connection = _Connection({'foo': 'Foo'})
        derived = self._derivedClass(connection, '/path')()
        derived._reload_properties()
        self.assertEqual(derived._properties, {'foo': 'Foo'})
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'GET')
        self.assertEqual(kw[0]['path'], '/path')
        self.assertEqual(kw[0]['query_params'], {'projection': 'noAcl'})

    def test__get_property_eager_hit(self):
        derived = self._derivedClass()(properties={'foo': 'Foo'})
        self.assertEqual(derived._get_property('foo'), 'Foo')

    def test__get_property_eager_miss_w_default(self):
        connection = _Connection({'foo': 'Foo'})
        derived = self._derivedClass(connection, '/path')()
        default = object()
        self.assertTrue(derived._get_property('nonesuch', default) is default)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'GET')
        self.assertEqual(kw[0]['path'], '/path')
        self.assertEqual(kw[0]['query_params'], {'projection': 'noAcl'})

    def test__get_property_lazy_hit(self):
        connection = _Connection({'foo': 'Foo'})
        derived = self._derivedClass(connection, '/path')()
        self.assertTrue(derived._get_property('nonesuch') is None)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'GET')
        self.assertEqual(kw[0]['path'], '/path')
        self.assertEqual(kw[0]['query_params'], {'projection': 'noAcl'})

    def test__get_property_w_custom_field(self):
        derived = self._derivedClass(foo='get_foo')()
        try:
            derived._get_property('foo')
        except KeyError as e:
            self.assertTrue('get_foo' in str(e))
        else:  # pragma: NO COVER
            self.assert_('KeyError not raised')

    def test__patch_properties(self):
        connection = _Connection({'foo': 'Foo'})
        derived = self._derivedClass(connection, '/path')()
        self.assertTrue(derived._patch_properties({'foo': 'Foo'}) is derived)
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/path')
        self.assertEqual(kw[0]['data'], {'foo': 'Foo'})
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_properties_eager(self):
        derived = self._derivedClass()(properties={'extant': False})
        self.assertEqual(derived.properties, {'extant': False})

    def test_properties_lazy(self):
        connection = _Connection({'foo': 'Foo'})
        derived = self._derivedClass(connection, '/path')()
        self.assertEqual(derived.properties, {'foo': 'Foo'})
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'GET')
        self.assertEqual(kw[0]['path'], '/path')
        self.assertEqual(kw[0]['query_params'], {'projection': 'noAcl'})

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
