# # Copyright 2026 Google LLC
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
#

import builtins
import importlib
import sys
from unittest import mock
import pytest
from google.auth.exceptions import MutualTLSChannelError
from google.protobuf import descriptor_pb2


from google.cloud.asset_v1 import _compat


def test_compat_normal_import():
    assert _compat.setup_request_id is not None


def test_compat_fallback_implementations():
    orig_import = builtins.__import__

    def custom_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name in (
            "google.api_core.universe",
            "google.api_core.gapic_v1.config",
            "google.api_core.gapic_v1.request",
            "google.api_core.rest_helpers",
        ):
            raise ImportError(f"Mocked ImportError for {name}")
        return orig_import(name, globals, locals, fromlist, level)

    with mock.patch("builtins.__import__", side_effect=custom_import):
        fallback = importlib.reload(_compat)

        # get_default_mtls_endpoint tests
        assert fallback.get_default_mtls_endpoint(None) is None
        assert fallback.get_default_mtls_endpoint("") == ""
        assert (
            fallback.get_default_mtls_endpoint("foo.googleapis.com")
            == "foo.mtls.googleapis.com"
        )
        assert (
            fallback.get_default_mtls_endpoint("foo.sandbox.googleapis.com")
            == "foo.mtls.sandbox.googleapis.com"
        )
        assert (
            fallback.get_default_mtls_endpoint("foo.mtls.googleapis.com")
            == "foo.mtls.googleapis.com"
        )
        assert (
            fallback.get_default_mtls_endpoint("custom.domain.com")
            == "custom.domain.com"
        )
        assert (
            fallback.get_default_mtls_endpoint(":::invalid-url:::")
            == ":::invalid-url:::"
        )

        # get_api_endpoint tests
        assert (
            fallback.get_api_endpoint(
                "https://override.com",
                None,
                "googleapis.com",
                "auto",
                "googleapis.com",
                "mtls.com",
                "https://{UNIVERSE_DOMAIN}",
            )
            == "https://override.com"
        )
        assert (
            fallback.get_api_endpoint(
                None,
                lambda: (b"", b""),
                "googleapis.com",
                "always",
                "googleapis.com",
                "mtls.com",
                "https://{UNIVERSE_DOMAIN}",
            )
            == "mtls.com"
        )
        assert (
            fallback.get_api_endpoint(
                None,
                lambda: (b"", b""),
                "googleapis.com",
                "auto",
                "googleapis.com",
                "mtls.com",
                "https://{UNIVERSE_DOMAIN}",
            )
            == "mtls.com"
        )
        with pytest.raises(MutualTLSChannelError):
            fallback.get_api_endpoint(
                None,
                lambda: (b"", b""),
                "otheruniverse.com",
                "always",
                "googleapis.com",
                "mtls.com",
                "https://{UNIVERSE_DOMAIN}",
            )
        assert (
            fallback.get_api_endpoint(
                None,
                None,
                "googleapis.com",
                "never",
                "googleapis.com",
                "mtls.com",
                "https://{UNIVERSE_DOMAIN}",
            )
            == "https://googleapis.com"
        )

        # get_universe_domain tests
        assert (
            fallback.get_universe_domain("custom.com", None, "googleapis.com")
            == "custom.com"
        )
        assert (
            fallback.get_universe_domain(None, "env.com", "googleapis.com") == "env.com"
        )
        assert (
            fallback.get_universe_domain(None, None, "googleapis.com")
            == "googleapis.com"
        )
        with pytest.raises(ValueError):
            fallback.get_universe_domain("   ", None, "googleapis.com")

        # use_client_cert_effective tests
        with mock.patch(
            "google.auth.transport.mtls.should_use_client_cert",
            return_value=True,
            create=True,
        ):
            assert fallback.use_client_cert_effective() is True

        with mock.patch.object(fallback, "mtls", spec=object()):
            with mock.patch.dict(
                "os.environ", {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}
            ):
                assert fallback.use_client_cert_effective() is True
            with mock.patch.dict(
                "os.environ", {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}
            ):
                assert fallback.use_client_cert_effective() is False
            with mock.patch.dict(
                "os.environ", {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "invalid"}
            ):
                with pytest.raises(ValueError):
                    fallback.use_client_cert_effective()

        # get_client_cert_source tests
        cert_fn = lambda: (b"cert", b"key")
        assert fallback.get_client_cert_source(cert_fn, True) == cert_fn
        assert fallback.get_client_cert_source(None, False) is None

        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=True,
            create=True,
        ):
            with mock.patch(
                "google.auth.transport.mtls.default_client_cert_source",
                return_value=cert_fn,
                create=True,
            ):
                assert fallback.get_client_cert_source(None, True) == cert_fn

        with mock.patch.object(fallback, "mtls", spec=object()):
            with pytest.raises(ValueError):
                fallback.get_client_cert_source(None, True)

        # read_environment_variables tests
        with mock.patch.dict(
            "os.environ",
            {
                "GOOGLE_API_USE_MTLS_ENDPOINT": "always",
                "GOOGLE_CLOUD_UNIVERSE_DOMAIN": "myuniverse.com",
            },
        ):
            use_cert, use_mtls, universe = fallback.read_environment_variables()
            assert use_mtls == "always"
            assert universe == "myuniverse.com"

        with mock.patch.dict("os.environ", {"GOOGLE_API_USE_MTLS_ENDPOINT": "invalid"}):
            with pytest.raises(MutualTLSChannelError):
                fallback.read_environment_variables()

        # setup_request_id tests
        fallback.setup_request_id(None, "request_id", False)

        d1 = {}
        fallback.setup_request_id(d1, "request_id", is_proto3_optional=True)
        assert "request_id" in d1

        d1_existing = {"request_id": None}
        fallback.setup_request_id(d1_existing, "request_id", is_proto3_optional=True)
        assert d1_existing["request_id"] is not None

        d2 = {}
        fallback.setup_request_id(d2, "request_id", is_proto3_optional=False)
        assert "request_id" in d2

        d3 = {"request_id": "existing"}
        fallback.setup_request_id(d3, "request_id", is_proto3_optional=False)
        assert d3["request_id"] == "existing"

        d4 = {"request_id": "val"}
        fallback.setup_request_id(d4, "request_id", is_proto3_optional=True)
        assert d4["request_id"] == "val"

        class DummyPopulated:
            def __init__(self):
                self.request_id = "val"

        p_existing = DummyPopulated()
        fallback.setup_request_id(p_existing, "request_id", is_proto3_optional=False)
        assert p_existing.request_id == "val"

        class NonOptPlain:
            def __init__(self):
                self.request_id = ""

        nop = NonOptPlain()
        fallback.setup_request_id(nop, "request_id", is_proto3_optional=False)
        assert nop.request_id != ""

        class DummyProto:
            def __init__(self):
                self.request_id = ""
                self._has = False

            def HasField(self, name):
                if not self._has:
                    return False
                return True

        p1 = DummyProto()
        fallback.setup_request_id(p1, "request_id", is_proto3_optional=True)
        assert p1.request_id != ""

        class DummyWrapper:
            def __init__(self):
                self._pb = DummyProto()

        w1 = DummyWrapper()
        fallback.setup_request_id(w1, "request_id", is_proto3_optional=True)
        assert (
            getattr(w1, "request_id", None) is not None
            or getattr(w1._pb, "request_id", None) != ""
        )

        class BadProto:
            def HasField(self, name):
                raise AttributeError()

        class BadWrapper:
            def __init__(self):
                self._pb = BadProto()
                self.request_id = None

        bw = BadWrapper()
        fallback.setup_request_id(bw, "request_id", is_proto3_optional=True)
        assert bw.request_id is not None

        class SetProto:
            def __init__(self):
                self.request_id = "already_set"

            def HasField(self, name):
                return True

        sp = SetProto()
        fallback.setup_request_id(sp, "request_id", is_proto3_optional=True)
        assert sp.request_id == "already_set"

        class SetProtoNonOpt:
            def __init__(self):
                self.request_id = "already_set"

        sp_non_opt = SetProtoNonOpt()
        fallback.setup_request_id(sp_non_opt, "request_id", is_proto3_optional=False)
        assert sp_non_opt.request_id == "already_set"

        class DummyPlain:
            def __init__(self):
                self.request_id = None

        pl1 = DummyPlain()
        fallback.setup_request_id(pl1, "request_id", is_proto3_optional=True)
        assert pl1.request_id is not None

        pl2 = DummyPlain()
        fallback.setup_request_id(pl2, "request_id", is_proto3_optional=False)
        assert pl2.request_id is not None

        # flatten_query_params tests
        assert fallback.flatten_query_params(None) == []
        res = fallback.flatten_query_params({"a": "val1", "b": [1, 2], "c": True})
        assert ("a", "val1") in res
        assert ("b", 1) in res
        assert ("b", 2) in res
        assert ("c", True) in res

        res_strict = fallback.flatten_query_params({"c": True}, strict=True)
        assert ("c", "true") in res_strict

        assert fallback._canonicalize(True, strict=True) == "true"
        assert fallback._canonicalize(True, strict=False) is True
        assert fallback._canonicalize(123, strict=True) == "123"
        assert fallback._canonicalize("str", strict=True) == "str"
        assert fallback._canonicalize("str", strict=False) == "str"
        assert fallback._is_primitive_value(None) is False

        with pytest.raises(TypeError):
            fallback.flatten_query_params("invalid")

        with pytest.raises(ValueError):
            fallback.flatten_query_params({"a": [{"nested": "dict"}]})

        with pytest.raises(ValueError):
            fallback._is_primitive_value([1, 2])

        # transcode_request tests
        dummy_req = descriptor_pb2.DescriptorProto()
        http_opts = [{"method": "get", "uri": "/v1/test"}]
        transcoded, body, query = fallback.transcode_request(
            http_opts,
            dummy_req,
            required_fields_default_values={"non_existent_key": "val"},
            rest_numeric_enums=True,
        )
        assert transcoded is not None
        assert query.get("non_existent_key") == "val"
        assert query.get("$alt") == "json;enum-encoding=int"

        transcoded2, body2, query2 = fallback.transcode_request(
            http_opts,
            dummy_req,
            required_fields_default_values={"name": "override_name"},
            rest_numeric_enums=False,
        )
        assert body2 is None
        assert "$alt" not in query2

    importlib.reload(_compat)
