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
    def test_constructor_with_flat():
        with pytest.raises(NotImplementedError):
            key_module.Key(flat=["Kind", 1])

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
