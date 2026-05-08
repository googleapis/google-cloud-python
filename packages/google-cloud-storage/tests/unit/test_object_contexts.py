import unittest
from mock import Mock

class TestObjectContexts(unittest.TestCase):
    def _getTargetClass(self):
        from google.cloud.storage.blob import ObjectContexts
        return ObjectContexts

    def _make_one(self, *args, **kwargs):
        return self._getTargetClass()(*args, **kwargs)

    def test_ctor(self):
        blob = Mock()
        custom = {"foo": {"value": "bar"}}
        contexts = self._make_one(blob, custom=custom)
        self.assertEqual(contexts["custom"], custom)
        self.assertIs(contexts.blob, blob)

    def test_from_api_repr(self):
        blob = Mock()
        resource = {"custom": {"foo": {"value": "bar"}}}
        contexts = self._getTargetClass().from_api_repr(resource, blob)
        self.assertEqual(contexts["custom"], resource["custom"])
        self.assertIs(contexts.blob, blob)

    def test_set_custom_context(self):
        blob = Mock()
        contexts = self._make_one(blob)
        contexts.set_custom_context("foo", "bar")
        self.assertEqual(contexts["custom"], {"foo": {"value": "bar"}})
        blob._patch_property.assert_called_with("objectContexts", contexts)

    def test_delete_custom_context(self):
        blob = Mock()
        custom = {"foo": {"value": "bar"}}
        contexts = self._make_one(blob, custom=custom)
        contexts.delete_custom_context("foo")
        self.assertIsNone(contexts["custom"]["foo"])
        blob._patch_property.assert_called_with("objectContexts", contexts)

    def test_clear_custom_contexts(self):
        blob = Mock()
        custom = {"foo": {"value": "bar"}}
        contexts = self._make_one(blob, custom=custom)
        contexts.clear_custom_contexts()
        self.assertIsNone(contexts["custom"])
        blob._patch_property.assert_called_with("objectContexts", contexts)

    def test_from_api_repr_w_timestamps(self):
        from datetime import datetime, timezone
        blob = Mock()
        resource = {
            "custom": {
                "foo": {
                    "value": "bar",
                    "createTime": "2026-01-01T00:00:00.000Z",
                    "updateTime": "2026-01-01T00:00:01.000Z",
                }
            }
        }
        contexts = self._getTargetClass().from_api_repr(resource, blob)
        self.assertEqual(
            contexts["custom"]["foo"]["create_time"],
            datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        )
        self.assertEqual(
            contexts["custom"]["foo"]["update_time"],
            datetime(2026, 1, 1, 0, 0, 1, tzinfo=timezone.utc),
        )
