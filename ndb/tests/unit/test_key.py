# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64
import unittest.mock

from google.cloud.datastore import _app_engine_key_pb2
import google.cloud.datastore
import pytest

from google.cloud.ndb import key as key_module
import tests.unit.utils


def test___all__():
    tests.unit.utils.verify___all__(key_module)


class TestKey:
    URLSAFE = b"agZzfmZpcmVyDwsSBEtpbmQiBVRoaW5nDA"

    @staticmethod
    @unittest.mock.patch("os.environ", new={})
    def test_constructor_default():
        with pytest.raises(NotImplementedError):
            key_module.Key("Kind")

    @staticmethod
    def test_constructor_with_reference():
        reference = make_reference()
        key = key_module.Key(reference=reference)
        ds_key = key._key
        assert isinstance(ds_key, google.cloud.datastore.Key)
        assert ds_key._flat_path == ("Parent", 59, "Child", "Feather")
        assert ds_key._namespace == "space"
        assert ds_key._parent is None
        assert ds_key._project == "sample-app"
        assert ds_key._path == [
            {"kind": "Parent", "id": 59},
            {"kind": "Child", "name": "Feather"},
        ]

        assert key._reference is reference

    @staticmethod
    def test_constructor_with_serialized():
        serialized = (
            b"j\x18s~sample-app-no-locationr\n\x0b\x12\x04Zorp\x18X\x0c"
        )
        key = key_module.Key(serialized=serialized)
        ds_key = key._key
        assert isinstance(ds_key, google.cloud.datastore.Key)
        assert ds_key._flat_path == ("Zorp", 88)
        assert ds_key._namespace is None
        assert ds_key._parent is None
        assert ds_key._project == "sample-app-no-location"
        assert ds_key._path == [{"kind": "Zorp", "id": 88}]
        assert key._reference == make_reference(
            path=({"type": "Zorp", "id": 88},),
            app="s~sample-app-no-location",
            namespace=None,
        )

    def test_constructor_with_urlsafe(self):
        key = key_module.Key(urlsafe=self.URLSAFE)
        ds_key = key._key
        assert isinstance(ds_key, google.cloud.datastore.Key)
        assert ds_key._flat_path == ("Kind", "Thing")
        assert ds_key._namespace is None
        assert ds_key._parent is None
        assert ds_key._project == "fire"
        assert ds_key._path == [{"kind": "Kind", "name": "Thing"}]
        assert key._reference == make_reference(
            path=({"type": "Kind", "name": "Thing"},),
            app="s~fire",
            namespace=None,
        )

    @staticmethod
    def test_constructor_with_pairs():
        with pytest.raises(NotImplementedError):
            key_module.Key(pairs=[("Kind", 1)])

    @staticmethod
    @unittest.mock.patch("os.environ", new={})
    def test_constructor_with_flat():
        with pytest.raises(NotImplementedError):
            key_module.Key(flat=["Kind", 1])

    @staticmethod
    def test_constructor_with_app():
        with pytest.raises(NotImplementedError):
            key_module.Key("Kind", 10, app="foo")

    @staticmethod
    def test_constructor_with_namespace():
        with pytest.raises(NotImplementedError):
            key_module.Key("Kind", 1337, namespace="foo", app="bar")

    def test_constructor_with_parent(self):
        parent = key_module.Key(urlsafe=self.URLSAFE)
        with pytest.raises(NotImplementedError):
            key_module.Key("Kind", 10, parent=parent)

    @staticmethod
    def test_constructor_insufficient_args():
        with pytest.raises(TypeError):
            key_module.Key(app="foo")

    def test_no_subclass_for_reference(self):
        class KeySubclass(key_module.Key):
            pass

        with pytest.raises(TypeError):
            KeySubclass(urlsafe=self.URLSAFE)

    @staticmethod
    def test_invalid_argument_combination():
        with pytest.raises(TypeError):
            key_module.Key(flat=["a", "b"], urlsafe=b"foo")

    def test_colliding_reference_arguments(self):
        urlsafe = self.URLSAFE
        padding = b"=" * (-len(urlsafe) % 4)
        serialized = base64.urlsafe_b64decode(urlsafe + padding)

        with pytest.raises(TypeError):
            key_module.Key(urlsafe=urlsafe, serialized=serialized)


class Test__project_from_app:
    @staticmethod
    def test_already_clean():
        app = "my-prahjekt"
        assert key_module._project_from_app(app) == app

    @staticmethod
    def test_prefixed():
        project = "my-prahjekt"
        for prefix in ("s", "e", "dev"):
            app = "{}~{}".format(prefix, project)
            assert key_module._project_from_app(app) == project

    @staticmethod
    @unittest.mock.patch("os.environ", new={})
    def test_app_default():
        assert key_module._project_from_app(None) == key_module._APP_ID_DEFAULT

    @staticmethod
    @unittest.mock.patch(
        "os.environ", new={key_module._APP_ID_ENVIRONMENT: "s~jectpro"}
    )
    def test_app_fallback():
        assert key_module._project_from_app(None) == "jectpro"


class Test__from_reference:
    def test_basic(self):
        reference = make_reference()
        ds_key = key_module._from_reference(reference, None, None)
        assert isinstance(ds_key, google.cloud.datastore.Key)
        assert ds_key._flat_path == ("Parent", 59, "Child", "Feather")
        assert ds_key._namespace == "space"
        assert ds_key._parent is None
        assert ds_key._project == "sample-app"
        assert ds_key._path == [
            {"kind": "Parent", "id": 59},
            {"kind": "Child", "name": "Feather"},
        ]

    def test_matching_app(self):
        reference = make_reference()
        ds_key = key_module._from_reference(reference, "s~sample-app", None)
        assert isinstance(ds_key, google.cloud.datastore.Key)
        assert ds_key._flat_path == ("Parent", 59, "Child", "Feather")
        assert ds_key._namespace == "space"
        assert ds_key._parent is None
        assert ds_key._project == "sample-app"
        assert ds_key._path == [
            {"kind": "Parent", "id": 59},
            {"kind": "Child", "name": "Feather"},
        ]

    def test_differing_app(self):
        reference = make_reference()
        with pytest.raises(RuntimeError):
            key_module._from_reference(reference, "pickles", None)

    def test_matching_namespace(self):
        reference = make_reference()
        ds_key = key_module._from_reference(reference, None, "space")
        assert isinstance(ds_key, google.cloud.datastore.Key)
        assert ds_key._flat_path == ("Parent", 59, "Child", "Feather")
        assert ds_key._namespace == "space"
        assert ds_key._parent is None
        assert ds_key._project == "sample-app"
        assert ds_key._path == [
            {"kind": "Parent", "id": 59},
            {"kind": "Child", "name": "Feather"},
        ]

    def test_differing_namespace(self):
        reference = make_reference()
        with pytest.raises(RuntimeError):
            key_module._from_reference(reference, None, "pickles")


class Test__from_serialized:
    @staticmethod
    def test_basic():
        serialized = (
            b"j\x0cs~sample-appr\x1e\x0b\x12\x06Parent\x18;\x0c\x0b\x12\x05"
            b'Child"\x07Feather\x0c\xa2\x01\x05space'
        )
        ds_key, reference = key_module._from_serialized(serialized, None, None)
        assert isinstance(ds_key, google.cloud.datastore.Key)
        assert ds_key._flat_path == ("Parent", 59, "Child", "Feather")
        assert ds_key._namespace == "space"
        assert ds_key._parent is None
        assert ds_key._project == "sample-app"
        assert ds_key._path == [
            {"kind": "Parent", "id": 59},
            {"kind": "Child", "name": "Feather"},
        ]
        assert reference == make_reference()

    @staticmethod
    def test_no_app_prefix():
        serialized = (
            b"j\x18s~sample-app-no-locationr\n\x0b\x12\x04Zorp\x18X\x0c"
        )
        ds_key, reference = key_module._from_serialized(serialized, None, None)
        assert isinstance(ds_key, google.cloud.datastore.Key)
        assert ds_key._flat_path == ("Zorp", 88)
        assert ds_key._namespace is None
        assert ds_key._parent is None
        assert ds_key._project == "sample-app-no-location"
        assert ds_key._path == [{"kind": "Zorp", "id": 88}]
        assert reference == make_reference(
            path=({"type": "Zorp", "id": 88},),
            app="s~sample-app-no-location",
            namespace=None,
        )


class Test__from_urlsafe:
    @staticmethod
    def test_basic():
        urlsafe = (
            "agxzfnNhbXBsZS1hcHByHgsSBlBhcmVudBg7DAsSBUNoaWxkIgdGZ"
            "WF0aGVyDKIBBXNwYWNl"
        )
        urlsafe_bytes = urlsafe.encode("ascii")
        for value in (urlsafe, urlsafe_bytes):
            ds_key, reference = key_module._from_urlsafe(value, None, None)
            assert isinstance(ds_key, google.cloud.datastore.Key)
            assert ds_key._flat_path == ("Parent", 59, "Child", "Feather")
            assert ds_key._namespace == "space"
            assert ds_key._parent is None
            assert ds_key._project == "sample-app"
            assert ds_key._path == [
                {"kind": "Parent", "id": 59},
                {"kind": "Child", "name": "Feather"},
            ]
            assert reference == make_reference()

    @staticmethod
    def test_needs_padding():
        urlsafe = b"agZzfmZpcmVyDwsSBEtpbmQiBVRoaW5nDA"

        ds_key, reference = key_module._from_urlsafe(urlsafe, None, None)
        assert isinstance(ds_key, google.cloud.datastore.Key)
        assert ds_key._flat_path == ("Kind", "Thing")
        assert ds_key._namespace is None
        assert ds_key._parent is None
        assert ds_key._project == "fire"
        assert ds_key._path == [{"kind": "Kind", "name": "Thing"}]
        assert reference == make_reference(
            path=({"type": "Kind", "name": "Thing"},),
            app="s~fire",
            namespace=None,
        )


class Test__constructor_handle_positional:
    @staticmethod
    def test_with_path():
        args = ("Kind", 1)
        kwargs = {}
        key_module._constructor_handle_positional(args, kwargs)
        assert kwargs == {"flat": args}

    @staticmethod
    def test_path_collide_flat():
        args = ("Kind", 1)
        kwargs = {"flat": ("OtherKind", "Cheese")}
        with pytest.raises(TypeError):
            key_module._constructor_handle_positional(args, kwargs)

    @staticmethod
    def test_dict_positional():
        args = ({"flat": ("OtherKind", "Cheese"), "app": "ehp"},)
        kwargs = {}
        key_module._constructor_handle_positional(args, kwargs)
        assert kwargs == args[0]

    @staticmethod
    def test_dict_positional_with_other_kwargs():
        args = ({"flat": ("OtherKind", "Cheese"), "app": "ehp"},)
        kwargs = {"namespace": "over-here"}
        with pytest.raises(TypeError):
            key_module._constructor_handle_positional(args, kwargs)


def make_reference(
    path=({"type": "Parent", "id": 59}, {"type": "Child", "name": "Feather"}),
    app="s~sample-app",
    namespace="space",
):
    elements = [
        _app_engine_key_pb2.Path.Element(**element) for element in path
    ]
    return _app_engine_key_pb2.Reference(
        app=app,
        path=_app_engine_key_pb2.Path(element=elements),
        name_space=namespace,
    )
