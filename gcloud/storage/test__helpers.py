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


class Test_ACLMetadataMixin(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.storage._helpers import _ACLMetadataMixin
        return _ACLMetadataMixin

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_abstract_properties(self):
        acl_mixin_object = self._makeOne()
        self.assertRaises(NotImplementedError,
                          lambda: acl_mixin_object.connection)
        self.assertRaises(NotImplementedError,
                          lambda: acl_mixin_object.path)
