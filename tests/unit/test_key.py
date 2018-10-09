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
from google.cloud.ndb import model
import tests.unit.utils


def test___all__():
    tests.unit.utils.verify___all__(key_module)


class TestKey:
    URLSAFE = b"agZzfmZpcmVyDwsSBEtpbmQiBVRoaW5nDA"

    @staticmethod
    @unittest.mock.patch("os.environ", new={})
    def test_constructor_default():
        key = key_module.Key("Kind", 42)

        assert key._key == google.cloud.datastore.Key(
            "Kind", 42, project=key_module._APP_ID_DEFAULT
        )
        assert key._reference is None

    @staticmethod
    @unittest.mock.patch("os.environ", new={})
    def test_constructor_empty_path():
        with pytest.raises(TypeError):
            key_module.Key(pairs=())

    @staticmethod
    @unittest.mock.patch("os.environ", new={})
    def test_constructor_partial():
        with pytest.raises(ValueError):
            key_module.Key("Kind")

        key = key_module.Key("Kind", None)

        assert key._key.is_partial
        assert key._key.flat_path == ("Kind",)
        assert key._key.project == key_module._APP_ID_DEFAULT
        assert key._reference is None

    @staticmethod
    def test_constructor_invalid_id_type():
        with pytest.raises(TypeError):
            key_module.Key("Kind", object())
        with pytest.raises(key_module._BadArgumentError):
            key_module.Key("Kind", None, "Also", 10)

    @staticmethod
    def test_constructor_invalid_kind_type():
        with pytest.raises(TypeError):
            key_module.Key(object(), 47)
        with pytest.raises(AttributeError):
            key_module.Key(object, 47)

    @staticmethod
    @unittest.mock.patch("os.environ", new={})
    def test_constructor_kind_as_model():
        class Simple(model.Model):
            pass

        key = key_module.Key(Simple, 47)
        assert key._key == google.cloud.datastore.Key(
            "Simple", 47, project=key_module._APP_ID_DEFAULT
        )
        assert key._reference is None

    @staticmethod
    def test_constructor_with_reference():
        reference = make_reference()
        key = key_module.Key(reference=reference)

        assert key._key == google.cloud.datastore.Key(
            "Parent",
            59,
            "Child",
            "Feather",
            project="sample-app",
            namespace="space",
        )
        assert key._reference is reference

    @staticmethod
    def test_constructor_with_serialized():
        serialized = (
            b"j\x18s~sample-app-no-locationr\n\x0b\x12\x04Zorp\x18X\x0c"
        )
        key = key_module.Key(serialized=serialized)

        assert key._key == google.cloud.datastore.Key(
            "Zorp", 88, project="sample-app-no-location"
        )
        assert key._reference == make_reference(
            path=({"type": "Zorp", "id": 88},),
            app="s~sample-app-no-location",
            namespace=None,
        )

    def test_constructor_with_urlsafe(self):
        key = key_module.Key(urlsafe=self.URLSAFE)

        assert key._key == google.cloud.datastore.Key(
            "Kind", "Thing", project="fire"
        )
        assert key._reference == make_reference(
            path=({"type": "Kind", "name": "Thing"},),
            app="s~fire",
            namespace=None,
        )

    @staticmethod
    @unittest.mock.patch("os.environ", new={})
    def test_constructor_with_pairs():
        key = key_module.Key(pairs=[("Kind", 1)])

        assert key._key == google.cloud.datastore.Key(
            "Kind", 1, project=key_module._APP_ID_DEFAULT
        )
        assert key._reference is None

    @staticmethod
    @unittest.mock.patch("os.environ", new={})
    def test_constructor_with_flat():
        key = key_module.Key(flat=["Kind", 1])

        assert key._key == google.cloud.datastore.Key(
            "Kind", 1, project=key_module._APP_ID_DEFAULT
        )
        assert key._reference is None

    @staticmethod
    def test_constructor_with_flat_and_pairs():
        with pytest.raises(TypeError):
            key_module.Key(pairs=[("Kind", 1)], flat=["Kind", 1])

    @staticmethod
    def test_constructor_with_app():
        key = key_module.Key("Kind", 10, app="s~foo")

        assert key._key == google.cloud.datastore.Key(
            "Kind", 10, project="foo"
        )
        assert key._reference is None

    @staticmethod
    @unittest.mock.patch("os.environ", new={})
    def test_constructor_with_namespace():
        key = key_module.Key("Kind", 1337, namespace="foo")

        assert key._key == google.cloud.datastore.Key(
            "Kind", 1337, project=key_module._APP_ID_DEFAULT, namespace="foo"
        )
        assert key._reference is None

    def test_constructor_with_parent(self):
        parent = key_module.Key(urlsafe=self.URLSAFE)
        key = key_module.Key("Zip", 10, parent=parent)

        assert key._key == google.cloud.datastore.Key(
            "Kind", "Thing", "Zip", 10, project="fire"
        )
        assert key._reference is None

    def test_constructor_with_parent_bad_type(self):
        parent = unittest.mock.sentinel.parent
        with pytest.raises(key_module._BadValueError):
            key_module.Key("Zip", 10, parent=parent)

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

    @staticmethod
    @unittest.mock.patch("google.cloud.ndb.key.Key.__init__")
    def test__from_ds_key(key_init):
        ds_key = google.cloud.datastore.Key("a", "b", project="c")
        key = key_module.Key._from_ds_key(ds_key)
        assert key._key is ds_key
        assert key._reference is None

        key_init.assert_not_called()

    @staticmethod
    @unittest.mock.patch("os.environ", new={})
    def test___repr__defaults():
        key = key_module.Key("a", "b")
        assert repr(key) == "Key('a', 'b')"
        assert str(key) == "Key('a', 'b')"

    @staticmethod
    @unittest.mock.patch("os.environ", new={})
    def test___repr__non_defaults():
        key = key_module.Key("X", 11, app="foo", namespace="bar")
        assert repr(key) == "Key('X', 11, app='foo', namespace='bar')"
        assert str(key) == "Key('X', 11, app='foo', namespace='bar')"

    @staticmethod
    def test_parent():
        key = key_module.Key("a", "b", "c", "d")
        parent = key.parent()
        assert parent._key == key._key.parent
        assert parent._reference is None

    @staticmethod
    def test_parent_top_level():
        key = key_module.Key("This", "key")
        assert key.parent() is None

    @staticmethod
    def test_root():
        key = key_module.Key("a", "b", "c", "d")
        root = key.root()
        assert root._key == key._key.parent
        assert root._reference is None

    @staticmethod
    def test_root_top_level():
        key = key_module.Key("This", "key")
        assert key.root() is key

    @staticmethod
    def test_namespace():
        namespace = "my-space"
        key = key_module.Key("abc", 1, namespace=namespace)
        assert key.namespace() == namespace

    @staticmethod
    def test_app():
        app = "s~example"
        key = key_module.Key("X", 100, app=app)
        assert key.app() != app
        assert key.app() == app[2:]

    @staticmethod
    def test_id():
        for id_or_name in ("x", 11, None):
            key = key_module.Key("Kind", id_or_name)
            assert key.id() == id_or_name

    @staticmethod
    def test_string_id():
        pairs = (("x", "x"), (11, None), (None, None))
        for id_or_name, expected in pairs:
            key = key_module.Key("Kind", id_or_name)
            assert key.string_id() == expected

    @staticmethod
    def test_integer_id():
        pairs = (("x", None), (11, 11), (None, None))
        for id_or_name, expected in pairs:
            key = key_module.Key("Kind", id_or_name)
            assert key.integer_id() == expected

    @staticmethod
    def test_flat():
        key = key_module.Key("This", "key")
        assert key.flat() == ("This", "key")

    @staticmethod
    def test_flat_partial_key():
        key = key_module.Key("Kind", None)
        assert key.flat() == ("Kind", None)


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
        assert ds_key == google.cloud.datastore.Key(
            "Parent",
            59,
            "Child",
            "Feather",
            project="sample-app",
            namespace="space",
        )

    def test_matching_app(self):
        reference = make_reference()
        ds_key = key_module._from_reference(reference, "s~sample-app", None)
        assert ds_key == google.cloud.datastore.Key(
            "Parent",
            59,
            "Child",
            "Feather",
            project="sample-app",
            namespace="space",
        )

    def test_differing_app(self):
        reference = make_reference()
        with pytest.raises(RuntimeError):
            key_module._from_reference(reference, "pickles", None)

    def test_matching_namespace(self):
        reference = make_reference()
        ds_key = key_module._from_reference(reference, None, "space")
        assert ds_key == google.cloud.datastore.Key(
            "Parent",
            59,
            "Child",
            "Feather",
            project="sample-app",
            namespace="space",
        )

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
        assert ds_key == google.cloud.datastore.Key(
            "Parent",
            59,
            "Child",
            "Feather",
            project="sample-app",
            namespace="space",
        )
        assert reference == make_reference()

    @staticmethod
    def test_no_app_prefix():
        serialized = (
            b"j\x18s~sample-app-no-locationr\n\x0b\x12\x04Zorp\x18X\x0c"
        )
        ds_key, reference = key_module._from_serialized(serialized, None, None)
        assert ds_key == google.cloud.datastore.Key(
            "Zorp", 88, project="sample-app-no-location"
        )
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
            assert ds_key == google.cloud.datastore.Key(
                "Parent",
                59,
                "Child",
                "Feather",
                project="sample-app",
                namespace="space",
            )
            assert reference == make_reference()

    @staticmethod
    def test_needs_padding():
        urlsafe = b"agZzfmZpcmVyDwsSBEtpbmQiBVRoaW5nDA"

        ds_key, reference = key_module._from_urlsafe(urlsafe, None, None)
        assert ds_key == google.cloud.datastore.Key(
            "Kind", "Thing", project="fire"
        )
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
