# Copyright 2014 Google LLC
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

import unittest


class TestKey(unittest.TestCase):

    _DEFAULT_PROJECT = "PROJECT"
    # NOTE: This comes directly from a running (in the dev appserver)
    #       App Engine app. Created via:
    #
    #           from google.appengine.ext import ndb
    #           key = ndb.Key(
    #               'Parent', 59, 'Child', 'Feather',
    #               namespace='space', app='s~sample-app')
    #           urlsafe = key.urlsafe()
    _URLSAFE_EXAMPLE1 = (
        b"agxzfnNhbXBsZS1hcHByHgsSBlBhcmVudBg7DAsSBUNoaWxkIgdGZ" b"WF0aGVyDKIBBXNwYWNl"
    )
    _URLSAFE_APP1 = "s~sample-app"
    _URLSAFE_NAMESPACE1 = "space"
    _URLSAFE_FLAT_PATH1 = ("Parent", 59, "Child", "Feather")
    _URLSAFE_EXAMPLE2 = b"agZzfmZpcmVyDwsSBEtpbmQiBVRoaW5nDA"
    _URLSAFE_APP2 = "s~fire"
    _URLSAFE_FLAT_PATH2 = ("Kind", "Thing")
    _URLSAFE_EXAMPLE3 = b"ahhzfnNhbXBsZS1hcHAtbm8tbG9jYXRpb25yCgsSBFpvcnAYWAw"
    _URLSAFE_APP3 = "sample-app-no-location"
    _URLSAFE_FLAT_PATH3 = ("Zorp", 88)

    @staticmethod
    def _get_target_class():
        from google.cloud.datastore.key import Key

        return Key

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_ctor_empty(self):
        self.assertRaises(ValueError, self._make_one)

    def test_ctor_no_project(self):
        klass = self._get_target_class()
        self.assertRaises(ValueError, klass, "KIND")

    def test_ctor_w_explicit_project_empty_path(self):
        _PROJECT = "PROJECT"
        self.assertRaises(ValueError, self._make_one, project=_PROJECT)

    def test_ctor_parent(self):
        _PARENT_KIND = "KIND1"
        _PARENT_ID = 1234
        _PARENT_PROJECT = "PROJECT-ALT"
        _PARENT_NAMESPACE = "NAMESPACE"
        _CHILD_KIND = "KIND2"
        _CHILD_ID = 2345
        _PATH = [
            {"kind": _PARENT_KIND, "id": _PARENT_ID},
            {"kind": _CHILD_KIND, "id": _CHILD_ID},
        ]
        parent_key = self._make_one(
            _PARENT_KIND,
            _PARENT_ID,
            project=_PARENT_PROJECT,
            namespace=_PARENT_NAMESPACE,
        )
        key = self._make_one(_CHILD_KIND, _CHILD_ID, parent=parent_key)
        self.assertEqual(key.project, parent_key.project)
        self.assertEqual(key.namespace, parent_key.namespace)
        self.assertEqual(key.kind, _CHILD_KIND)
        self.assertEqual(key.path, _PATH)
        self.assertIs(key.parent, parent_key)

    def test_ctor_partial_parent(self):
        parent_key = self._make_one("KIND", project=self._DEFAULT_PROJECT)
        with self.assertRaises(ValueError):
            self._make_one("KIND2", 1234, parent=parent_key)

    def test_ctor_parent_bad_type(self):
        with self.assertRaises(AttributeError):
            self._make_one(
                "KIND2", 1234, parent=("KIND1", 1234), project=self._DEFAULT_PROJECT
            )

    def test_ctor_parent_bad_namespace(self):
        parent_key = self._make_one(
            "KIND", 1234, namespace="FOO", project=self._DEFAULT_PROJECT
        )
        with self.assertRaises(ValueError):
            self._make_one(
                "KIND2",
                1234,
                namespace="BAR",
                parent=parent_key,
                PROJECT=self._DEFAULT_PROJECT,
            )

    def test_ctor_parent_bad_project(self):
        parent_key = self._make_one("KIND", 1234, project="FOO")
        with self.assertRaises(ValueError):
            self._make_one("KIND2", 1234, parent=parent_key, project="BAR")

    def test_ctor_parent_empty_path(self):
        parent_key = self._make_one("KIND", 1234, project=self._DEFAULT_PROJECT)
        with self.assertRaises(ValueError):
            self._make_one(parent=parent_key)

    def test_ctor_explicit(self):
        _PROJECT = "PROJECT-ALT"
        _NAMESPACE = "NAMESPACE"
        _KIND = "KIND"
        _ID = 1234
        _PATH = [{"kind": _KIND, "id": _ID}]
        key = self._make_one(_KIND, _ID, namespace=_NAMESPACE, project=_PROJECT)
        self.assertEqual(key.project, _PROJECT)
        self.assertEqual(key.namespace, _NAMESPACE)
        self.assertEqual(key.kind, _KIND)
        self.assertEqual(key.path, _PATH)

    def test_ctor_bad_kind(self):
        self.assertRaises(
            ValueError, self._make_one, object(), project=self._DEFAULT_PROJECT
        )

    def test_ctor_bad_id_or_name(self):
        self.assertRaises(
            ValueError, self._make_one, "KIND", object(), project=self._DEFAULT_PROJECT
        )
        self.assertRaises(
            ValueError, self._make_one, "KIND", None, project=self._DEFAULT_PROJECT
        )
        self.assertRaises(
            ValueError,
            self._make_one,
            "KIND",
            10,
            "KIND2",
            None,
            project=self._DEFAULT_PROJECT,
        )

    def test__clone(self):
        _PROJECT = "PROJECT-ALT"
        _NAMESPACE = "NAMESPACE"
        _KIND = "KIND"
        _ID = 1234
        _PATH = [{"kind": _KIND, "id": _ID}]
        key = self._make_one(_KIND, _ID, namespace=_NAMESPACE, project=_PROJECT)
        clone = key._clone()
        self.assertEqual(clone.project, _PROJECT)
        self.assertEqual(clone.namespace, _NAMESPACE)
        self.assertEqual(clone.kind, _KIND)
        self.assertEqual(clone.path, _PATH)

    def test__clone_with_parent(self):
        _PROJECT = "PROJECT-ALT"
        _NAMESPACE = "NAMESPACE"
        _KIND1 = "PARENT"
        _KIND2 = "KIND"
        _ID1 = 1234
        _ID2 = 2345
        _PATH = [{"kind": _KIND1, "id": _ID1}, {"kind": _KIND2, "id": _ID2}]

        parent = self._make_one(_KIND1, _ID1, namespace=_NAMESPACE, project=_PROJECT)
        key = self._make_one(_KIND2, _ID2, parent=parent)
        self.assertIs(key.parent, parent)
        clone = key._clone()
        self.assertIs(clone.parent, key.parent)
        self.assertEqual(clone.project, _PROJECT)
        self.assertEqual(clone.namespace, _NAMESPACE)
        self.assertEqual(clone.path, _PATH)

    def test___eq_____ne___w_non_key(self):
        _PROJECT = "PROJECT"
        _KIND = "KIND"
        _NAME = "one"
        key = self._make_one(_KIND, _NAME, project=_PROJECT)
        self.assertFalse(key == object())
        self.assertTrue(key != object())

    def test___eq_____ne___two_incomplete_keys_same_kind(self):
        _PROJECT = "PROJECT"
        _KIND = "KIND"
        key1 = self._make_one(_KIND, project=_PROJECT)
        key2 = self._make_one(_KIND, project=_PROJECT)
        self.assertFalse(key1 == key2)
        self.assertTrue(key1 != key2)

    def test___eq_____ne___incomplete_key_w_complete_key_same_kind(self):
        _PROJECT = "PROJECT"
        _KIND = "KIND"
        _ID = 1234
        key1 = self._make_one(_KIND, project=_PROJECT)
        key2 = self._make_one(_KIND, _ID, project=_PROJECT)
        self.assertFalse(key1 == key2)
        self.assertTrue(key1 != key2)

    def test___eq_____ne___complete_key_w_incomplete_key_same_kind(self):
        _PROJECT = "PROJECT"
        _KIND = "KIND"
        _ID = 1234
        key1 = self._make_one(_KIND, _ID, project=_PROJECT)
        key2 = self._make_one(_KIND, project=_PROJECT)
        self.assertFalse(key1 == key2)
        self.assertTrue(key1 != key2)

    def test___eq_____ne___same_kind_different_ids(self):
        _PROJECT = "PROJECT"
        _KIND = "KIND"
        _ID1 = 1234
        _ID2 = 2345
        key1 = self._make_one(_KIND, _ID1, project=_PROJECT)
        key2 = self._make_one(_KIND, _ID2, project=_PROJECT)
        self.assertFalse(key1 == key2)
        self.assertTrue(key1 != key2)

    def test___eq_____ne___same_kind_and_id(self):
        _PROJECT = "PROJECT"
        _KIND = "KIND"
        _ID = 1234
        key1 = self._make_one(_KIND, _ID, project=_PROJECT)
        key2 = self._make_one(_KIND, _ID, project=_PROJECT)
        self.assertTrue(key1 == key2)
        self.assertFalse(key1 != key2)

    def test___eq_____ne___same_kind_and_id_different_project(self):
        _PROJECT1 = "PROJECT1"
        _PROJECT2 = "PROJECT2"
        _KIND = "KIND"
        _ID = 1234
        key1 = self._make_one(_KIND, _ID, project=_PROJECT1)
        key2 = self._make_one(_KIND, _ID, project=_PROJECT2)
        self.assertFalse(key1 == key2)
        self.assertTrue(key1 != key2)

    def test___eq_____ne___same_kind_and_id_different_namespace(self):
        _PROJECT = "PROJECT"
        _NAMESPACE1 = "NAMESPACE1"
        _NAMESPACE2 = "NAMESPACE2"
        _KIND = "KIND"
        _ID = 1234
        key1 = self._make_one(_KIND, _ID, project=_PROJECT, namespace=_NAMESPACE1)
        key2 = self._make_one(_KIND, _ID, project=_PROJECT, namespace=_NAMESPACE2)
        self.assertFalse(key1 == key2)
        self.assertTrue(key1 != key2)

    def test___eq_____ne___same_kind_different_names(self):
        _PROJECT = "PROJECT"
        _KIND = "KIND"
        _NAME1 = "one"
        _NAME2 = "two"
        key1 = self._make_one(_KIND, _NAME1, project=_PROJECT)
        key2 = self._make_one(_KIND, _NAME2, project=_PROJECT)
        self.assertFalse(key1 == key2)
        self.assertTrue(key1 != key2)

    def test___eq_____ne___same_kind_and_name(self):
        _PROJECT = "PROJECT"
        _KIND = "KIND"
        _NAME = "one"
        key1 = self._make_one(_KIND, _NAME, project=_PROJECT)
        key2 = self._make_one(_KIND, _NAME, project=_PROJECT)
        self.assertTrue(key1 == key2)
        self.assertFalse(key1 != key2)

    def test___eq_____ne___same_kind_and_name_different_project(self):
        _PROJECT1 = "PROJECT1"
        _PROJECT2 = "PROJECT2"
        _KIND = "KIND"
        _NAME = "one"
        key1 = self._make_one(_KIND, _NAME, project=_PROJECT1)
        key2 = self._make_one(_KIND, _NAME, project=_PROJECT2)
        self.assertFalse(key1 == key2)
        self.assertTrue(key1 != key2)

    def test___eq_____ne___same_kind_and_name_different_namespace(self):
        _PROJECT = "PROJECT"
        _NAMESPACE1 = "NAMESPACE1"
        _NAMESPACE2 = "NAMESPACE2"
        _KIND = "KIND"
        _NAME = "one"
        key1 = self._make_one(_KIND, _NAME, project=_PROJECT, namespace=_NAMESPACE1)
        key2 = self._make_one(_KIND, _NAME, project=_PROJECT, namespace=_NAMESPACE2)
        self.assertFalse(key1 == key2)
        self.assertTrue(key1 != key2)

    def test___hash___incomplete(self):
        _PROJECT = "PROJECT"
        _KIND = "KIND"
        key = self._make_one(_KIND, project=_PROJECT)
        self.assertNotEqual(hash(key), hash(_KIND) + hash(_PROJECT) + hash(None))

    def test___hash___completed_w_id(self):
        _PROJECT = "PROJECT"
        _KIND = "KIND"
        _ID = 1234
        key = self._make_one(_KIND, _ID, project=_PROJECT)
        self.assertNotEqual(
            hash(key), hash(_KIND) + hash(_ID) + hash(_PROJECT) + hash(None)
        )

    def test___hash___completed_w_name(self):
        _PROJECT = "PROJECT"
        _KIND = "KIND"
        _NAME = "NAME"
        key = self._make_one(_KIND, _NAME, project=_PROJECT)
        self.assertNotEqual(
            hash(key), hash(_KIND) + hash(_NAME) + hash(_PROJECT) + hash(None)
        )

    def test_completed_key_on_partial_w_id(self):
        key = self._make_one("KIND", project=self._DEFAULT_PROJECT)
        _ID = 1234
        new_key = key.completed_key(_ID)
        self.assertIsNot(key, new_key)
        self.assertEqual(new_key.id, _ID)
        self.assertIsNone(new_key.name)

    def test_completed_key_on_partial_w_name(self):
        key = self._make_one("KIND", project=self._DEFAULT_PROJECT)
        _NAME = "NAME"
        new_key = key.completed_key(_NAME)
        self.assertIsNot(key, new_key)
        self.assertIsNone(new_key.id)
        self.assertEqual(new_key.name, _NAME)

    def test_completed_key_on_partial_w_invalid(self):
        key = self._make_one("KIND", project=self._DEFAULT_PROJECT)
        self.assertRaises(ValueError, key.completed_key, object())

    def test_completed_key_on_complete(self):
        key = self._make_one("KIND", 1234, project=self._DEFAULT_PROJECT)
        self.assertRaises(ValueError, key.completed_key, 5678)

    def test_to_protobuf_defaults(self):
        from google.cloud.datastore_v1.types import entity as entity_pb2

        _KIND = "KIND"
        key = self._make_one(_KIND, project=self._DEFAULT_PROJECT)
        pb = key.to_protobuf()
        self.assertIsInstance(pb, entity_pb2.Key)

        # Check partition ID.
        self.assertEqual(pb.partition_id.project_id, self._DEFAULT_PROJECT)
        # Unset values are False-y.
        self.assertEqual(pb.partition_id.namespace_id, "")

        # Check the element PB matches the partial key and kind.
        (elem,) = list(pb.path)
        self.assertEqual(elem.kind, _KIND)
        # Unset values are False-y.
        self.assertEqual(elem.name, "")
        # Unset values are False-y.
        self.assertEqual(elem.id, 0)

    def test_to_protobuf_w_explicit_project(self):
        _PROJECT = "PROJECT-ALT"
        key = self._make_one("KIND", project=_PROJECT)
        pb = key.to_protobuf()
        self.assertEqual(pb.partition_id.project_id, _PROJECT)

    def test_to_protobuf_w_explicit_namespace(self):
        _NAMESPACE = "NAMESPACE"
        key = self._make_one(
            "KIND", namespace=_NAMESPACE, project=self._DEFAULT_PROJECT
        )
        pb = key.to_protobuf()
        self.assertEqual(pb.partition_id.namespace_id, _NAMESPACE)

    def test_to_protobuf_w_explicit_path(self):
        _PARENT = "PARENT"
        _CHILD = "CHILD"
        _ID = 1234
        _NAME = "NAME"
        key = self._make_one(_PARENT, _NAME, _CHILD, _ID, project=self._DEFAULT_PROJECT)
        pb = key.to_protobuf()
        elems = list(pb.path)
        self.assertEqual(len(elems), 2)
        self.assertEqual(elems[0].kind, _PARENT)
        self.assertEqual(elems[0].name, _NAME)
        self.assertEqual(elems[1].kind, _CHILD)
        self.assertEqual(elems[1].id, _ID)

    def test_to_protobuf_w_no_kind(self):
        key = self._make_one("KIND", project=self._DEFAULT_PROJECT)
        # Force the 'kind' to be unset. Maybe `to_protobuf` should fail
        # on this? The backend certainly will.
        key._path[-1].pop("kind")
        pb = key.to_protobuf()
        # Unset values are False-y.
        self.assertEqual(pb.path[0].kind, "")

    def test_to_legacy_urlsafe(self):
        key = self._make_one(
            *self._URLSAFE_FLAT_PATH1,
            project=self._URLSAFE_APP1,
            namespace=self._URLSAFE_NAMESPACE1
        )
        # NOTE: ``key.project`` is somewhat "invalid" but that is OK.
        urlsafe = key.to_legacy_urlsafe()
        self.assertEqual(urlsafe, self._URLSAFE_EXAMPLE1)

    def test_to_legacy_urlsafe_strip_padding(self):
        key = self._make_one(*self._URLSAFE_FLAT_PATH2, project=self._URLSAFE_APP2)
        # NOTE: ``key.project`` is somewhat "invalid" but that is OK.
        urlsafe = key.to_legacy_urlsafe()
        self.assertEqual(urlsafe, self._URLSAFE_EXAMPLE2)
        # Make sure it started with base64 padding.
        self.assertNotEqual(len(self._URLSAFE_EXAMPLE2) % 4, 0)

    def test_to_legacy_urlsafe_with_location_prefix(self):
        key = self._make_one(*self._URLSAFE_FLAT_PATH3, project=self._URLSAFE_APP3)
        urlsafe = key.to_legacy_urlsafe(location_prefix="s~")
        self.assertEqual(urlsafe, self._URLSAFE_EXAMPLE3)

    def test_from_legacy_urlsafe(self):
        klass = self._get_target_class()
        key = klass.from_legacy_urlsafe(self._URLSAFE_EXAMPLE1)

        self.assertEqual("s~" + key.project, self._URLSAFE_APP1)
        self.assertEqual(key.namespace, self._URLSAFE_NAMESPACE1)
        self.assertEqual(key.flat_path, self._URLSAFE_FLAT_PATH1)
        # Also make sure we didn't accidentally set the parent.
        self.assertIsNone(key._parent)
        self.assertIsNotNone(key.parent)
        self.assertIs(key._parent, key.parent)

    def test_from_legacy_urlsafe_needs_padding(self):
        klass = self._get_target_class()
        # Make sure it will have base64 padding added.
        self.assertNotEqual(len(self._URLSAFE_EXAMPLE2) % 4, 0)
        key = klass.from_legacy_urlsafe(self._URLSAFE_EXAMPLE2)

        self.assertEqual("s~" + key.project, self._URLSAFE_APP2)
        self.assertIsNone(key.namespace)
        self.assertEqual(key.flat_path, self._URLSAFE_FLAT_PATH2)

    def test_from_legacy_urlsafe_with_location_prefix(self):
        klass = self._get_target_class()
        # Make sure it will have base64 padding added.
        key = klass.from_legacy_urlsafe(self._URLSAFE_EXAMPLE3)

        self.assertEqual(key.project, self._URLSAFE_APP3)
        self.assertIsNone(key.namespace)
        self.assertEqual(key.flat_path, self._URLSAFE_FLAT_PATH3)

    def test_is_partial_no_name_or_id(self):
        key = self._make_one("KIND", project=self._DEFAULT_PROJECT)
        self.assertTrue(key.is_partial)

    def test_is_partial_w_id(self):
        _ID = 1234
        key = self._make_one("KIND", _ID, project=self._DEFAULT_PROJECT)
        self.assertFalse(key.is_partial)

    def test_is_partial_w_name(self):
        _NAME = "NAME"
        key = self._make_one("KIND", _NAME, project=self._DEFAULT_PROJECT)
        self.assertFalse(key.is_partial)

    def test_id_or_name_no_name_or_id(self):
        key = self._make_one("KIND", project=self._DEFAULT_PROJECT)
        self.assertIsNone(key.id_or_name)

    def test_id_or_name_no_name_or_id_child(self):
        key = self._make_one("KIND1", 1234, "KIND2", project=self._DEFAULT_PROJECT)
        self.assertIsNone(key.id_or_name)

    def test_id_or_name_w_id_only(self):
        _ID = 1234
        key = self._make_one("KIND", _ID, project=self._DEFAULT_PROJECT)
        self.assertEqual(key.id_or_name, _ID)

    def test_id_or_name_w_name_only(self):
        _NAME = "NAME"
        key = self._make_one("KIND", _NAME, project=self._DEFAULT_PROJECT)
        self.assertEqual(key.id_or_name, _NAME)

    def test_parent_default(self):
        key = self._make_one("KIND", project=self._DEFAULT_PROJECT)
        self.assertIsNone(key.parent)

    def test_parent_explicit_top_level(self):
        key = self._make_one("KIND", 1234, project=self._DEFAULT_PROJECT)
        self.assertIsNone(key.parent)

    def test_parent_explicit_nested(self):
        _PARENT_KIND = "KIND1"
        _PARENT_ID = 1234
        _PARENT_PATH = [{"kind": _PARENT_KIND, "id": _PARENT_ID}]
        key = self._make_one(
            _PARENT_KIND, _PARENT_ID, "KIND2", project=self._DEFAULT_PROJECT
        )
        self.assertEqual(key.parent.path, _PARENT_PATH)

    def test_parent_multiple_calls(self):
        _PARENT_KIND = "KIND1"
        _PARENT_ID = 1234
        _PARENT_PATH = [{"kind": _PARENT_KIND, "id": _PARENT_ID}]
        key = self._make_one(
            _PARENT_KIND, _PARENT_ID, "KIND2", project=self._DEFAULT_PROJECT
        )
        parent = key.parent
        self.assertEqual(parent.path, _PARENT_PATH)
        new_parent = key.parent
        self.assertIs(parent, new_parent)


class Test__clean_app(unittest.TestCase):

    PROJECT = "my-prahjekt"

    @staticmethod
    def _call_fut(app_str):
        from google.cloud.datastore.key import _clean_app

        return _clean_app(app_str)

    def test_already_clean(self):
        app_str = self.PROJECT
        self.assertEqual(self._call_fut(app_str), self.PROJECT)

    def test_standard(self):
        app_str = "s~" + self.PROJECT
        self.assertEqual(self._call_fut(app_str), self.PROJECT)

    def test_european(self):
        app_str = "e~" + self.PROJECT
        self.assertEqual(self._call_fut(app_str), self.PROJECT)

    def test_dev_server(self):
        app_str = "dev~" + self.PROJECT
        self.assertEqual(self._call_fut(app_str), self.PROJECT)


class Test__get_empty(unittest.TestCase):
    @staticmethod
    def _call_fut(value, empty_value):
        from google.cloud.datastore.key import _get_empty

        return _get_empty(value, empty_value)

    def test_unset(self):
        for empty_value in (u"", 0, 0.0, []):
            ret_val = self._call_fut(empty_value, empty_value)
            self.assertIsNone(ret_val)

    def test_actually_set(self):
        value_pairs = ((u"hello", u""), (10, 0), (3.14, 0.0), (["stuff", "here"], []))
        for value, empty_value in value_pairs:
            ret_val = self._call_fut(value, empty_value)
            self.assertIs(ret_val, value)


class Test__check_database_id(unittest.TestCase):
    @staticmethod
    def _call_fut(database_id):
        from google.cloud.datastore.key import _check_database_id

        return _check_database_id(database_id)

    def test_empty_value(self):
        ret_val = self._call_fut(u"")
        # Really we are just happy there was no exception.
        self.assertIsNone(ret_val)

    def test_failure(self):
        with self.assertRaises(ValueError):
            self._call_fut(u"some-database-id")


class Test__add_id_or_name(unittest.TestCase):
    @staticmethod
    def _call_fut(flat_path, element_pb, empty_allowed):
        from google.cloud.datastore.key import _add_id_or_name

        return _add_id_or_name(flat_path, element_pb, empty_allowed)

    def test_add_id(self):
        flat_path = []
        id_ = 123
        element_pb = _make_element_pb(id=id_)

        ret_val = self._call_fut(flat_path, element_pb, False)
        self.assertIsNone(ret_val)
        self.assertEqual(flat_path, [id_])
        ret_val = self._call_fut(flat_path, element_pb, True)
        self.assertIsNone(ret_val)
        self.assertEqual(flat_path, [id_, id_])

    def test_add_name(self):
        flat_path = []
        name = "moon-shadow"
        element_pb = _make_element_pb(name=name)

        ret_val = self._call_fut(flat_path, element_pb, False)
        self.assertIsNone(ret_val)
        self.assertEqual(flat_path, [name])
        ret_val = self._call_fut(flat_path, element_pb, True)
        self.assertIsNone(ret_val)
        self.assertEqual(flat_path, [name, name])

    def test_both_present(self):
        element_pb = _make_element_pb(id=17, name="seventeen")
        flat_path = []
        with self.assertRaises(ValueError):
            self._call_fut(flat_path, element_pb, False)
        with self.assertRaises(ValueError):
            self._call_fut(flat_path, element_pb, True)

        self.assertEqual(flat_path, [])

    def test_both_empty_failure(self):
        element_pb = _make_element_pb()
        flat_path = []
        with self.assertRaises(ValueError):
            self._call_fut(flat_path, element_pb, False)

        self.assertEqual(flat_path, [])

    def test_both_empty_allowed(self):
        element_pb = _make_element_pb()
        flat_path = []
        ret_val = self._call_fut(flat_path, element_pb, True)
        self.assertIsNone(ret_val)
        self.assertEqual(flat_path, [])


class Test__get_flat_path(unittest.TestCase):
    @staticmethod
    def _call_fut(path_pb):
        from google.cloud.datastore.key import _get_flat_path

        return _get_flat_path(path_pb)

    def test_one_pair(self):
        kind = "Widget"
        name = "Scooter"
        element_pb = _make_element_pb(type=kind, name=name)
        path_pb = _make_path_pb(element_pb)
        flat_path = self._call_fut(path_pb)
        self.assertEqual(flat_path, (kind, name))

    def test_two_pairs(self):
        kind1 = "parent"
        id1 = 59
        element_pb1 = _make_element_pb(type=kind1, id=id1)

        kind2 = "child"
        name2 = "naem"
        element_pb2 = _make_element_pb(type=kind2, name=name2)

        path_pb = _make_path_pb(element_pb1, element_pb2)
        flat_path = self._call_fut(path_pb)
        self.assertEqual(flat_path, (kind1, id1, kind2, name2))

    def test_partial_key(self):
        kind1 = "grandparent"
        name1 = "cats"
        element_pb1 = _make_element_pb(type=kind1, name=name1)

        kind2 = "parent"
        id2 = 1337
        element_pb2 = _make_element_pb(type=kind2, id=id2)

        kind3 = "child"
        element_pb3 = _make_element_pb(type=kind3)

        path_pb = _make_path_pb(element_pb1, element_pb2, element_pb3)
        flat_path = self._call_fut(path_pb)
        self.assertEqual(flat_path, (kind1, name1, kind2, id2, kind3))


class Test__to_legacy_path(unittest.TestCase):
    @staticmethod
    def _call_fut(dict_path):
        from google.cloud.datastore.key import _to_legacy_path

        return _to_legacy_path(dict_path)

    def test_one_pair(self):
        kind = "Widget"
        name = "Scooter"
        dict_path = [{"kind": kind, "name": name}]
        path_pb = self._call_fut(dict_path)

        element_pb = _make_element_pb(type=kind, name=name)
        expected_pb = _make_path_pb(element_pb)
        self.assertEqual(path_pb, expected_pb)

    def test_two_pairs(self):
        kind1 = "parent"
        id1 = 59

        kind2 = "child"
        name2 = "naem"

        dict_path = [{"kind": kind1, "id": id1}, {"kind": kind2, "name": name2}]
        path_pb = self._call_fut(dict_path)

        element_pb1 = _make_element_pb(type=kind1, id=id1)
        element_pb2 = _make_element_pb(type=kind2, name=name2)
        expected_pb = _make_path_pb(element_pb1, element_pb2)
        self.assertEqual(path_pb, expected_pb)

    def test_partial_key(self):
        kind1 = "grandparent"
        name1 = "cats"

        kind2 = "parent"
        id2 = 1337

        kind3 = "child"

        dict_path = [
            {"kind": kind1, "name": name1},
            {"kind": kind2, "id": id2},
            {"kind": kind3},
        ]
        path_pb = self._call_fut(dict_path)

        element_pb1 = _make_element_pb(type=kind1, name=name1)
        element_pb2 = _make_element_pb(type=kind2, id=id2)
        element_pb3 = _make_element_pb(type=kind3)
        expected_pb = _make_path_pb(element_pb1, element_pb2, element_pb3)
        self.assertEqual(path_pb, expected_pb)


def _make_element_pb(**kwargs):
    from google.cloud.datastore import _app_engine_key_pb2

    return _app_engine_key_pb2.Path.Element(**kwargs)


def _make_path_pb(*element_pbs):
    from google.cloud.datastore import _app_engine_key_pb2

    return _app_engine_key_pb2.Path(element=element_pbs)
