import unittest2


class Test_MetadataMixin(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.storage._helpers import _MetadataMixin
        return _MetadataMixin

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_abstract_properties(self):
        metadata_object = self._makeOne()
        self.assertRaises(NotImplementedError,
                          lambda: metadata_object.connection)
        self.assertRaises(NotImplementedError,
                          lambda: metadata_object.path)

    def test_get_metadata_w_custom_field(self):
        class Derived(self._getTargetClass()):
            CUSTOM_METADATA_FIELDS = {'foo': 'get_foo'}

            @property
            def connection(self):  # pragma: NO COVER
                return None

            @property
            def path(self):  # pragma: NO COVER
                return None

        derived = Derived()
        try:
            derived.get_metadata('foo')
        except KeyError as e:
            self.assertTrue('get_foo' in str(e))
        else:  # pragma: NO COVER
            self.assert_('KeyError not raised')
