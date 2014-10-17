import unittest2


class Test_MetadataMixin(unittest2.TestCase):

    @staticmethod
    def _getTargetClass():
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
