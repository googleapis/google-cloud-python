# Copyright 2026 Google LLC
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

import sys
import types
from unittest import mock

import google.auth
from google.auth import credentials as ga_credentials
import jinja2

from gapic import utils
from gapic.samplegen_utils.utils import coerce_response_name, render_format_string
from test_utils.test_utils import get_method, make_service
from gapic.utils import Options


def _make_jinja_env() -> jinja2.Environment:
    opts = Options.build("transport=grpc+rest")
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(searchpath=opts.templates),
        undefined=jinja2.StrictUndefined,
        extensions=["jinja2.ext.do"],
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["rst"] = utils.rst
    if hasattr(utils, "make_private"):
        env.filters["make_private"] = utils.make_private
    env.filters["snake_case"] = utils.to_snake_case
    env.filters["camel_case"] = utils.to_camel_case
    env.filters["sort_lines"] = utils.sort_lines
    env.filters["wrap"] = utils.wrap
    env.filters["coerce_response_name"] = coerce_response_name
    env.filters["render_format_string"] = render_format_string
    env.tests["str_field_pb"] = utils.is_str_field_pb
    env.tests["msg_field_pb"] = utils.is_msg_field_pb
    if hasattr(utils, "UUID4_RE"):
        env.globals["uuid4_re"] = utils.UUID4_RE
    return env


class _DummyNaming:
    module_namespace = ("google", "cloud")
    versioned_module_name = "thingdoer_v1"
    warehouse_package_name = "google-cloud-thingdoer"


class _DummyApi:
    naming = _DummyNaming()
    has_iam_mixin = False
    has_location_mixin = False
    has_operations_mixin = False
    mixin_api_methods = {}
    mixin_api_signatures = {}
    mixin_http_options = {}
    http_options = {
        "google.longrunning.Operations.GetOperation": [
            types.SimpleNamespace(
                method="get",
                uri="/v1/{name=projects/*/operations/*}",
                body=None,
            )
        ]
    }
    requires_package = ()

    @staticmethod
    def get_extended_operations_services(_service):
        return ()


def _render_and_exec_transports(has_lro: bool = False):
    env = _make_jinja_env()
    opts = Options.build("transport=grpc+rest")
    if has_lro:
        method = get_method(
            "DoThing",
            "foo.bar.ThingRequest",
            "google.longrunning.Operation",
            lro_response_type="foo.bar.ThingResponse",
            lro_metadata_type="foo.bar.ThingMetadata",
        )
    else:
        method = get_method("DoThing", "foo.bar.ThingRequest", "foo.bar.ThingResponse")
    service = make_service(
        name="ThingDoer",
        host="thingdoer.googleapis.com",
        scopes=("https://www.googleapis.com/auth/cloud-platform",),
        methods=(method,),
    )
    dummy_api = _DummyApi()

    base_code = env.get_template(
        "%namespace/%name_%version/%sub/services/%service/transports/base.py.j2"
    ).render(api=dummy_api, service=service, opts=opts)
    rest_base_code = env.get_template(
        "%namespace/%name_%version/%sub/services/%service/transports/rest_base.py.j2"
    ).render(api=dummy_api, service=service, opts=opts)
    rest_code = env.get_template(
        "%namespace/%name_%version/%sub/services/%service/transports/rest.py.j2"
    ).render(api=dummy_api, service=service, opts=opts)

    pkg_names = [
        "foo",
        "foo.bar",
        "google.cloud.thingdoer_v1",
        "google.cloud.thingdoer_v1.services",
        "google.cloud.thingdoer_v1.services.thing_doer",
        "google.cloud.thingdoer_v1.services.thing_doer.transports",
    ]
    saved = {name: sys.modules.get(name) for name in pkg_names}
    saved_base = sys.modules.get(
        "google.cloud.thingdoer_v1.services.thing_doer.transports.base"
    )
    saved_rest_base = sys.modules.get(
        "google.cloud.thingdoer_v1.services.thing_doer.transports.rest_base"
    )
    saved_rest = sys.modules.get(
        "google.cloud.thingdoer_v1.services.thing_doer.transports.rest"
    )

    try:
        for name in pkg_names:
            mod = types.ModuleType(name)
            mod.__path__ = []
            sys.modules[name] = mod

        class _DummyMsg:
            pass

        saved_longrunning = sys.modules.get("google.longrunning")
        saved_ops_pb2 = sys.modules.get("google.longrunning.operations_pb2")
        saved_google_lr_attr = getattr(sys.modules["google"], "longrunning", None)
        if saved_longrunning is None:
            lr_mod = types.ModuleType("google.longrunning")
            lr_mod.__path__ = []
            ops_pb2_mod = types.ModuleType("google.longrunning.operations_pb2")
            ops_pb2_mod.Operation = _DummyMsg
            lr_mod.operations_pb2 = ops_pb2_mod
            sys.modules["google.longrunning"] = lr_mod
            sys.modules["google.longrunning.operations_pb2"] = ops_pb2_mod
            sys.modules["google"].longrunning = lr_mod

        sys.modules["foo.bar"].bar = types.SimpleNamespace(
            ThingRequest=_DummyMsg,
            ThingResponse=_DummyMsg,
            ThingMetadata=_DummyMsg,
        )
        sys.modules["foo"].bar = sys.modules["foo.bar"]
        sys.modules["google.cloud.thingdoer_v1"].gapic_version = types.SimpleNamespace(
            __version__="0.1.0"
        )

        base_mod = types.ModuleType(
            "google.cloud.thingdoer_v1.services.thing_doer.transports.base"
        )
        base_mod.__package__ = (
            "google.cloud.thingdoer_v1.services.thing_doer.transports"
        )
        sys.modules[base_mod.__name__] = base_mod
        exec(base_code, base_mod.__dict__)

        rest_base_mod = types.ModuleType(
            "google.cloud.thingdoer_v1.services.thing_doer.transports.rest_base"
        )
        rest_base_mod.__package__ = (
            "google.cloud.thingdoer_v1.services.thing_doer.transports"
        )
        sys.modules[rest_base_mod.__name__] = rest_base_mod
        exec(rest_base_code, rest_base_mod.__dict__)

        rest_mod = types.ModuleType(
            "google.cloud.thingdoer_v1.services.thing_doer.transports.rest"
        )
        rest_mod.__package__ = (
            "google.cloud.thingdoer_v1.services.thing_doer.transports"
        )
        sys.modules[rest_mod.__name__] = rest_mod
        exec(rest_code, rest_mod.__dict__)
        return base_mod, rest_mod
    finally:
        if "saved_longrunning" in locals() and saved_longrunning is None:
            sys.modules.pop("google.longrunning", None)
            sys.modules.pop("google.longrunning.operations_pb2", None)
            if saved_google_lr_attr is None:
                delattr(sys.modules["google"], "longrunning")
        for name, orig in saved.items():
            if orig is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = orig
        for mod_key, orig_mod in (
            (
                "google.cloud.thingdoer_v1.services.thing_doer.transports.base",
                saved_base,
            ),
            (
                "google.cloud.thingdoer_v1.services.thing_doer.transports.rest_base",
                saved_rest_base,
            ),
            (
                "google.cloud.thingdoer_v1.services.thing_doer.transports.rest",
                saved_rest,
            ),
        ):
            if orig_mod is None:
                sys.modules.pop(mod_key, None)
            else:
                sys.modules[mod_key] = orig_mod


def test_rest_transport_forwards_quota_scopes_and_credentials_file():
    _, rest_mod = _render_and_exec_transports()
    rest_cls = rest_mod.ThingDoerRestTransport

    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        rest_cls(quota_project_id="billing-proj", scopes=["https://scope/a"])
        adc.assert_called_once_with(
            scopes=["https://scope/a"],
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="billing-proj",
        )

    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds:
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        rest_cls(
            credentials_file="/tmp/creds.json",
            quota_project_id="billing-proj",
            scopes=["https://scope/b"],
        )
        load_creds.assert_called_once_with(
            "/tmp/creds.json",
            scopes=["https://scope/b"],
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="billing-proj",
        )


class _FakeScopedQuotaCredentials(
    ga_credentials.Scoped, ga_credentials.CredentialsWithQuotaProject
):
    def __init__(self, scopes=None, quota_project_id=None):
        super().__init__()
        self._scopes = scopes
        self._quota_project_id = quota_project_id

    @property
    def requires_scopes(self):
        return not self._scopes

    def with_scopes(self, scopes, default_scopes=None):
        return _FakeScopedQuotaCredentials(
            scopes=scopes or default_scopes,
            quota_project_id=self._quota_project_id,
        )

    def with_quota_project(self, quota_project_id):
        return _FakeScopedQuotaCredentials(
            scopes=self._scopes,
            quota_project_id=quota_project_id,
        )

    def refresh(self, request):
        self.token = "tok"


def test_base_and_rest_transport_apply_quota_and_scopes_to_explicit_credentials():
    _, rest_mod = _render_and_exec_transports()
    rest_cls = rest_mod.ThingDoerRestTransport

    explicit = _FakeScopedQuotaCredentials()
    transport = rest_cls(
        credentials=explicit,
        quota_project_id="quota-override",
        scopes=["https://custom/scope"],
    )
    assert transport._credentials._quota_project_id == "quota-override"
    assert transport._credentials._scopes == ["https://custom/scope"]


def test_rest_transport_forwards_mtls_cert_to_operations_client():
    _, rest_mod = _render_and_exec_transports(has_lro=True)
    rest_cls = rest_mod.ThingDoerRestTransport

    cert_cb = lambda: (b"cert", b"key")
    with mock.patch.object(
        rest_mod.AuthorizedSession, "configure_mtls_channel"
    ) as cfg_mtls, mock.patch.object(
        rest_mod.operations_v1, "OperationsRestTransport"
    ) as ops_rest_cls, mock.patch.object(
        rest_mod.operations_v1, "AbstractOperationsClient"
    ) as ops_client_cls:
        transport = rest_cls(
            credentials=ga_credentials.AnonymousCredentials(),
            client_cert_source_for_mtls=cert_cb,
        )
        cfg_mtls.assert_called_once_with(cert_cb)
        _ = transport.operations_client
        ops_rest_cls.assert_called_once()
        assert (
            ops_rest_cls.call_args.kwargs["client_cert_source_for_mtls"]
            is cert_cb
        )
        ops_client_cls.assert_called_once()


def test_generated_service_test_template_parses_for_all_transports():
    env = _make_jinja_env()
    for tpl_path in (
        "%namespace/%name_%version/%sub/services/%service/transports/base.py.j2",
        "%namespace/%name_%version/%sub/services/%service/transports/rest_base.py.j2",
        "%namespace/%name_%version/%sub/services/%service/transports/rest.py.j2",
        "tests/unit/gapic/%name_%version/%sub/test_%service.py.j2",
    ):
        tmpl = env.get_template(tpl_path)
        assert tmpl is not None
