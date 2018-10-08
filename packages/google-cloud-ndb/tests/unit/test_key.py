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

import unittest.mock

from google.cloud.datastore import _app_engine_key_pb2
import google.cloud.datastore
import pytest

from google.cloud.ndb import key as key_module
import tests.unit.utils


def test___all__():
    tests.unit.utils.verify___all__(key_module)


class TestKey:
    @staticmethod
    @unittest.mock.patch("os.environ", new={})
    def test_constructor_default():
        key = key_module.Key("Kind")
        ds_key = key._key
        assert isinstance(ds_key, google.cloud.datastore.Key)
        assert ds_key._flat_path == ("Kind",)
        assert ds_key._namespace is None
        assert ds_key._parent is None
        assert ds_key._project == key_module._APP_ID_DEFAULT
        assert ds_key._path == [{"kind": "Kind"}]

    @staticmethod
    def test_constructor_with_reference():
        with pytest.raises(NotImplementedError):
            key_module.Key(reference=unittest.mock.sentinel.ref)

    @staticmethod
    def test_constructor_with_serialized():
        with pytest.raises(NotImplementedError):
            key_module.Key(serialized=b"foo")

    @staticmethod
    def test_constructor_with_urlsafe():
        with pytest.raises(NotImplementedError):
            key_module.Key(urlsafe="foo")

    @staticmethod
    def test_constructor_with_pairs():
        with pytest.raises(NotImplementedError):
            key_module.Key(pairs=[("Kind", 1)])

    @staticmethod
    @unittest.mock.patch("os.environ", new={})
    def test_constructor_with_flat():
        key = key_module.Key(flat=["Kind", 1])
        ds_key = key._key
        assert isinstance(ds_key, google.cloud.datastore.Key)
        assert ds_key._flat_path == ("Kind", 1)
        assert ds_key._namespace is None
        assert ds_key._parent is None
        assert ds_key._project == key_module._APP_ID_DEFAULT
        assert ds_key._path == [{"kind": "Kind", "id": 1}]

    @staticmethod
    def test_constructor_with_app():
        key = key_module.Key("Kind", app="foo")
        ds_key = key._key
        assert isinstance(ds_key, google.cloud.datastore.Key)
        assert ds_key._flat_path == ("Kind",)
        assert ds_key._namespace is None
        assert ds_key._parent is None
        assert ds_key._project == "foo"
        assert ds_key._path == [{"kind": "Kind"}]

    @staticmethod
    def test_constructor_with_namespace():
        key = key_module.Key("Kind", namespace="foo", app="bar")
        ds_key = key._key
        assert isinstance(ds_key, google.cloud.datastore.Key)
        assert ds_key._flat_path == ("Kind",)
        assert ds_key._namespace == "foo"
        assert ds_key._parent is None
        assert ds_key._project == "bar"
        assert ds_key._path == [{"kind": "Kind"}]

    @staticmethod
    def test_constructor_with_parent():
        with pytest.raises(NotImplementedError):
            key_module.Key(parent=unittest.mock.sentinel.key)


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


def test__from_reference():
    reference = _app_engine_key_pb2.Reference(
        app="s~sample-app",
        path=_app_engine_key_pb2.Path(
            element=[
                _app_engine_key_pb2.Path.Element(type="Parent", id=59),
                _app_engine_key_pb2.Path.Element(type="Child", name="Feather"),
            ]
        ),
        name_space="space",
    )
    ds_key = key_module._from_reference(reference)
    assert isinstance(ds_key, google.cloud.datastore.Key)
    assert ds_key._flat_path == ("Parent", 59, "Child", "Feather")
    assert ds_key._namespace == "space"
    assert ds_key._parent is None
    assert ds_key._project == "sample-app"
    assert ds_key._path == [
        {"kind": "Parent", "id": 59},
        {"kind": "Child", "name": "Feather"},
    ]


class Test__from_serialized:
    @staticmethod
    def test_basic():
        serialized = (
            b"j\x0cs~sample-appr\x1e\x0b\x12\x06Parent\x18;\x0c\x0b\x12\x05"
            b'Child"\x07Feather\x0c\xa2\x01\x05space'
        )
        ds_key = key_module._from_serialized(serialized)
        assert isinstance(ds_key, google.cloud.datastore.Key)
        assert ds_key._flat_path == ("Parent", 59, "Child", "Feather")
        assert ds_key._namespace == "space"
        assert ds_key._parent is None
        assert ds_key._project == "sample-app"
        assert ds_key._path == [
            {"kind": "Parent", "id": 59},
            {"kind": "Child", "name": "Feather"},
        ]

    @staticmethod
    def test_no_app_prefix():
        serialized = (
            b"j\x18s~sample-app-no-locationr\n\x0b\x12\x04Zorp\x18X\x0c"
        )
        ds_key = key_module._from_serialized(serialized)
        assert isinstance(ds_key, google.cloud.datastore.Key)
        assert ds_key._flat_path == ("Zorp", 88)
        assert ds_key._namespace is None
        assert ds_key._parent is None
        assert ds_key._project == "sample-app-no-location"
        assert ds_key._path == [{"kind": "Zorp", "id": 88}]


class Test__from_urlsafe:
    @staticmethod
    def test_basic():
        urlsafe = (
            "agxzfnNhbXBsZS1hcHByHgsSBlBhcmVudBg7DAsSBUNoaWxkIgdGZ"
            "WF0aGVyDKIBBXNwYWNl"
        )
        urlsafe_bytes = urlsafe.encode("ascii")
        for value in (urlsafe, urlsafe_bytes):
            ds_key = key_module._from_urlsafe(value)
            assert isinstance(ds_key, google.cloud.datastore.Key)
            assert ds_key._flat_path == ("Parent", 59, "Child", "Feather")
            assert ds_key._namespace == "space"
            assert ds_key._parent is None
            assert ds_key._project == "sample-app"
            assert ds_key._path == [
                {"kind": "Parent", "id": 59},
                {"kind": "Child", "name": "Feather"},
            ]

    @staticmethod
    def test_needs_padding():
        urlsafe = b"agZzfmZpcmVyDwsSBEtpbmQiBVRoaW5nDA"

        ds_key = key_module._from_urlsafe(urlsafe)
        assert isinstance(ds_key, google.cloud.datastore.Key)
        assert ds_key._flat_path == ("Kind", "Thing")
        assert ds_key._namespace is None
        assert ds_key._parent is None
        assert ds_key._project == "fire"
        assert ds_key._path == [{"kind": "Kind", "name": "Thing"}]


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
