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

    def _derivedClass(self, path=None):

        class Derived(self._getTargetClass()):

            @property
            def path(self):
                return path

        return Derived

    def test_path_is_abstract(self):
        mixin = self._makeOne()
        self.assertRaises(NotImplementedError, lambda: mixin.path)

    def test_client_is_abstract(self):
        mixin = self._makeOne()
        self.assertRaises(NotImplementedError, lambda: mixin.client)

    def test_reload(self):
        connection = _Connection({'foo': 'Foo'})
        client = _Client(connection)
        derived = self._derivedClass('/path')()
        # Make sure changes is not a set, so we can observe a change.
        derived._changes = object()
        derived.reload(client=client)
        self.assertEqual(derived._properties, {'foo': 'Foo'})
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'GET')
        self.assertEqual(kw[0]['path'], '/path')
        self.assertEqual(kw[0]['query_params'], {'projection': 'noAcl'})
        # Make sure changes get reset by reload.
        self.assertEqual(derived._changes, set())

    def test__set_properties(self):
        mixin = self._makeOne()
        self.assertEqual(mixin._properties, {})
        VALUE = object()
        mixin._set_properties(VALUE)
        self.assertEqual(mixin._properties, VALUE)

    def test__patch_property(self):
        derived = self._derivedClass()()
        derived._patch_property('foo', 'Foo')
        self.assertEqual(derived._properties, {'foo': 'Foo'})

    def test_patch(self):
        connection = _Connection({'foo': 'Foo'})
        client = _Client(connection)
        derived = self._derivedClass('/path')()
        # Make sure changes is non-empty, so we can observe a change.
        BAR = object()
        BAZ = object()
        derived._properties = {'bar': BAR, 'baz': BAZ}
        derived._changes = set(['bar'])  # Ignore baz.
        derived.patch(client=client)
        self.assertEqual(derived._properties, {'foo': 'Foo'})
        kw = connection._requested
        self.assertEqual(len(kw), 1)
        self.assertEqual(kw[0]['method'], 'PATCH')
        self.assertEqual(kw[0]['path'], '/path')
        self.assertEqual(kw[0]['query_params'], {'projection': 'full'})
        # Since changes does not include `baz`, we don't see it sent.
        self.assertEqual(kw[0]['data'], {'bar': BAR})
        # Make sure changes get reset by patch().
        self.assertEqual(derived._changes, set())


class Test__scalar_property(unittest2.TestCase):

    def _callFUT(self, fieldName):
        from gcloud.storage._helpers import _scalar_property
        return _scalar_property(fieldName)

    def test_getter(self):

        class Test(object):
            def __init__(self, **kw):
                self._properties = kw.copy()
            do_re_mi = self._callFUT('solfege')

        test = Test(solfege='Latido')
        self.assertEqual(test.do_re_mi, 'Latido')

    def test_setter(self):

        class Test(object):
            def _patch_property(self, name, value):
                self._patched = (name, value)
            do_re_mi = self._callFUT('solfege')

        test = Test()
        test.do_re_mi = 'Latido'
        self.assertEqual(test._patched, ('solfege', 'Latido'))


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


class _Client(object):

    def __init__(self, connection):
        self.connection = connection
