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

    def test_properties_eager(self):
        derived = self._derivedClass()(properties={'extant': False})
        self.assertEqual(derived.properties, {'extant': False})

    def test_batch(self):
        connection = _Connection({'foo': 'Qux', 'bar': 'Baz'})
        derived = self._derivedClass(connection, '/path')()
        with derived.batch:
            derived._patch_properties({'foo': 'Foo'})
            derived._patch_properties({'bar': 'Baz'})
            derived._patch_properties({'foo': 'Qux'})
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/path')
        self.assertEqual(kw[0]['data'], {'foo': 'Qux', 'bar': 'Baz'})
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})

    def test_properties_lazy(self):
        connection = _Connection({'foo': 'Foo'})
        derived = self._derivedClass(connection, '/path')()
        self.assertEqual(derived.properties, {'foo': 'Foo'})
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'GET')
        self.assertEqual(kw[0]['path'], '/path')
        self.assertEqual(kw[0]['query_params'], {'projection': 'noAcl'})

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


class TestPropertyBatch(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.storage._helpers import _PropertyBatch
        return _PropertyBatch

    def _makeOne(self, wrapped):
        return self._getTargetClass()(wrapped)

    def _makeWrapped(self, connection=None, path=None, **custom_fields):
        from gcloud.storage._helpers import _PropertyMixin

        class Wrapped(_PropertyMixin):
            CUSTOM_PROPERTY_ACCESSORS = custom_fields

            @property
            def connection(self):
                return connection

            @property
            def path(self):
                return path

        return Wrapped()

    def test_ctor_does_not_intercept__patch_properties(self):
        wrapped = self._makeWrapped()
        before = wrapped._patch_properties
        batch = self._makeOne(wrapped)
        after = wrapped._patch_properties
        self.assertEqual(before, after)
        self.assertTrue(batch._wrapped is wrapped)

    def test_cm_intercepts_restores__patch_properties(self):
        wrapped = self._makeWrapped()
        before = wrapped._patch_properties
        batch = self._makeOne(wrapped)
        with batch:
            # No deferred patching -> no call to the real '_patch_properties'
            during = wrapped._patch_properties
        after = wrapped._patch_properties
        self.assertNotEqual(before, during)
        self.assertEqual(before, after)

    def test___exit___w_error_skips__patch_properties(self):
        class Testing(Exception):
            pass
        wrapped = self._makeWrapped()
        batch = self._makeOne(wrapped)
        try:
            with batch:
                # deferred patching
                wrapped._patch_properties({'foo': 'Foo'})
                # but error -> no call to the real '_patch_properties'
                raise Testing('testing')
        except Testing:
            pass

    def test___exit___no_error_aggregates__patch_properties(self):
        connection = _Connection({'foo': 'Foo'})
        wrapped = self._makeWrapped(connection, '/path')
        batch = self._makeOne(wrapped)
        kw = connection._requested
        with batch:
            # deferred patching
            wrapped._patch_properties({'foo': 'Foo'})
            wrapped._patch_properties({'bar': 'Baz'})
            wrapped._patch_properties({'foo': 'Qux'})
            self.assertEqual(len(kw), 0)
        # exited w/o error -> call to the real '_patch_properties'
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/path')
        self.assertEqual(kw[0]['data'], {'foo': 'Qux', 'bar': 'Baz'})
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})


class Test__scalar_property(unittest2.TestCase):

    def _callFUT(self, fieldName):
        from gcloud.storage._helpers import _scalar_property
        return _scalar_property(fieldName)

    def test_getter(self):

        class Test(object):
            def __init__(self, **kw):
                self.properties = kw.copy()
            do_re_mi = self._callFUT('solfege')

        test = Test(solfege='Latido')
        self.assertEqual(test.do_re_mi, 'Latido')

    def test_setter(self):

        class Test(object):
            def _patch_properties(self, mapping):
                self._patched = mapping.copy()
            do_re_mi = self._callFUT('solfege')

        test = Test()
        test.do_re_mi = 'Latido'
        self.assertEqual(test._patched, {'solfege': 'Latido'})


class Test__base64_md5hash(unittest2.TestCase):

    def _callFUT(self, bytes_to_sign):
        from gcloud.storage._helpers import _base64_md5hash
        return _base64_md5hash(bytes_to_sign)

    def test_it(self):
        from io import BytesIO
        BYTES_TO_SIGN = b'FOO'
        BUFFER = BytesIO()
        BUFFER.write(BYTES_TO_SIGN)
        BUFFER.seek(0)

        SIGNED_CONTENT = self._callFUT(BUFFER)
        self.assertEqual(SIGNED_CONTENT, b'kBiQqOnIz21aGlQrIp/r/w==')

    def test_it_with_stubs(self):
        from gcloud._testing import _Monkey
        from gcloud.storage import _helpers as MUT

        class _Buffer(object):

            def __init__(self, return_vals):
                self.return_vals = return_vals
                self._block_sizes = []

            def read(self, block_size):
                self._block_sizes.append(block_size)
                return self.return_vals.pop()

        BASE64 = _Base64()
        DIGEST_VAL = object()
        BYTES_TO_SIGN = b'BYTES_TO_SIGN'
        BUFFER = _Buffer([b'', BYTES_TO_SIGN])
        MD5 = _MD5(DIGEST_VAL)

        with _Monkey(MUT, base64=BASE64, MD5=MD5):
            SIGNED_CONTENT = self._callFUT(BUFFER)

        self.assertEqual(BUFFER._block_sizes, [8192, 8192])
        self.assertTrue(SIGNED_CONTENT is DIGEST_VAL)
        self.assertEqual(BASE64._called_b64encode, [DIGEST_VAL])
        self.assertEqual(MD5._new_called, [None])
        self.assertEqual(MD5.hash_obj.num_digest_calls, 1)
        self.assertEqual(MD5.hash_obj._blocks, [BYTES_TO_SIGN])


class _Connection(object):

    def __init__(self, *responses):
        self._responses = responses
        self._requested = []

    def api_request(self, **kw):
        self._requested.append(kw)
        response, self._responses = self._responses[0], self._responses[1:]
        return response


class _MD5Hash(object):

    def __init__(self, digest_val):
        self.digest_val = digest_val
        self.num_digest_calls = 0
        self._blocks = []

    def update(self, block):
        self._blocks.append(block)

    def digest(self):
        self.num_digest_calls += 1
        return self.digest_val


class _MD5(object):

    def __init__(self, digest_val):
        self.hash_obj = _MD5Hash(digest_val)
        self._new_called = []

    def new(self, data=None):
        self._new_called.append(data)
        return self.hash_obj


class _Base64(object):

    def __init__(self):
        self._called_b64encode = []

    def b64encode(self, value):
        self._called_b64encode.append(value)
        return value
