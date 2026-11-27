# Copyright 2026 Google LLC
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

"""Universe-domain conformance and BigQuery Storage sub-client routing tests."""

from types import MappingProxyType
from typing import Any
from unittest import mock
from urllib.parse import urlparse

import google.auth
import pytest
import requests
from google.api_core import client_options as client_options_lib
from google.api_core.universe import UniverseMismatchError
from google.auth import credentials as auth_credentials

from google.cloud import bigquery
from google.cloud.bigquery import _helpers, dbapi, schema
from google.cloud.bigquery import table as bq_table

DEFAULT_PROJECT_ID = "test-proj"
DEFAULT_UNIVERSE = "googleapis.com"
TPC_UNIVERSE = "apis-tpclp.goog"
OTHER_TPC_UNIVERSE = "other-tpc.goog"
TPC_BQ_API_ENDPOINT = f"https://bigquery.{TPC_UNIVERSE}"
TPC_BQSTORAGE_API_ENDPOINT = f"bigquerystorage.{TPC_UNIVERSE}:443"
EMULATOR_HOST = "http://localhost:9050"


class FakeScopedQuotaCredentials(
    auth_credentials.Scoped, auth_credentials.CredentialsWithQuotaProject
):
    """In-memory fake Credentials supporting scopes, quota project, and universe_domain."""

    def __init__(
        self,
        universe_domain: str = DEFAULT_UNIVERSE,
        quota_project_id: str | None = None,
        scopes: tuple[str, ...] | None = None,
    ) -> None:
        super().__init__()
        self._universe_domain = universe_domain
        self._quota_project_id = quota_project_id
        self._scopes = scopes
        self.token = "fake-token"

    @property
    def universe_domain(self) -> str:
        return self._universe_domain

    @property
    def requires_scopes(self) -> bool:
        return False

    def refresh(self, request) -> None:  # pragma: NO COVER
        self.token = "fake-token"

    def with_scopes(self, scopes, default_scopes=None):  # pragma: NO COVER
        return FakeScopedQuotaCredentials(
            universe_domain=self._universe_domain,
            quota_project_id=self._quota_project_id,
            scopes=tuple(scopes or default_scopes or ()),
        )

    def with_quota_project(self, quota_project_id: str | None):  # pragma: NO COVER
        return FakeScopedQuotaCredentials(
            universe_domain=self._universe_domain,
            quota_project_id=quota_project_id,
            scopes=self._scopes,
        )


def make_mock_credentials(
    universe_domain: str = DEFAULT_UNIVERSE,
) -> FakeScopedQuotaCredentials:
    """Create fake Credentials configured for the given universe_domain."""
    return FakeScopedQuotaCredentials(universe_domain=universe_domain)


def _is_googleapis_host(target_or_url: str) -> bool:
    if target_or_url.startswith(("http://", "https://")):
        host = urlparse(target_or_url).hostname
    else:
        target = target_or_url.removeprefix("dns:").lstrip("/")
        if "/" in target:
            target = target.rsplit("/", 1)[-1]
        host = urlparse(f"//{target}").hostname
    return bool(host and (host == "googleapis.com" or host.endswith(".googleapis.com")))


@pytest.fixture(autouse=True)
def clean_tpc_env(monkeypatch):
    """Clear ambient universe and endpoint environment variables for each test."""
    monkeypatch.delenv("GOOGLE_CLOUD_UNIVERSE_DOMAIN", raising=False)
    monkeypatch.delenv("GOOGLE_API_USE_MTLS_ENDPOINT", raising=False)
    monkeypatch.delenv("BIGQUERY_EMULATOR_HOST", raising=False)
    monkeypatch.delenv(
        "GOOGLE_CLOUD_ENABLE_DIRECT_PATH_XDS_OVER_INTERCONNECT", raising=False
    )


@pytest.fixture
def assert_no_googleapis_calls(monkeypatch):
    """Fail if requests or gRPC channels dial *.googleapis.com during a test."""
    unexpected_calls: list[str] = []

    def _guard_host(target_or_url: str) -> None:
        if _is_googleapis_host(target_or_url):  # pragma: NO COVER
            unexpected_calls.append(target_or_url)
            raise ConnectionRefusedError(
                f"Unexpected googleapis.com call toward: {target_or_url}"
            )

    def _guarded_send(self, request, *args, **kwargs):  # pragma: NO COVER
        _guard_host(request.url)
        resp = requests.Response()
        resp.status_code = 200
        resp._content = b"{}"
        return resp

    monkeypatch.setattr(requests.Session, "send", _guarded_send)

    try:
        import grpc

        def _guarded_channel(target, *args, **kwargs):
            _guard_host(target)
            return mock.create_autospec(grpc.Channel, instance=True, spec_set=True)

        monkeypatch.setattr(grpc, "secure_channel", _guarded_channel)
        monkeypatch.setattr(grpc, "insecure_channel", _guarded_channel)
        if hasattr(grpc, "aio"):  # pragma: NO COVER

            def _guarded_aio_channel(target, *args, **kwargs):
                _guard_host(target)
                return mock.create_autospec(
                    grpc.aio.Channel, instance=True, spec_set=True
                )

            monkeypatch.setattr(grpc.aio, "secure_channel", _guarded_aio_channel)
            monkeypatch.setattr(grpc.aio, "insecure_channel", _guarded_aio_channel)
    except ImportError:  # pragma: NO COVER
        pass

    yield
    assert unexpected_calls == []


class TestGoogleapisHostParser:
    @pytest.mark.parametrize(
        ("target", "expected"),
        [
            pytest.param(
                "https://bigquery.googleapis.com/bigquery/v2",
                True,
                id="https_gdu_url",
            ),
            pytest.param("https://googleapis.com", True, id="bare_gdu_domain"),
            pytest.param(
                "bigquerystorage.googleapis.com:443",
                True,
                id="grpc_host_port",
            ),
            pytest.param(
                "dns:///bigquerystorage.googleapis.com:443",
                True,
                id="grpc_dns_triple_slash",
            ),
            pytest.param(
                "dns://8.8.8.8/bigquerystorage.googleapis.com:443",
                True,
                id="grpc_dns_with_authority",
            ),
            pytest.param(
                f"https://bigquery.{TPC_UNIVERSE}/bigquery/v2",
                False,
                id="https_tpc_url",
            ),
            pytest.param(
                f"dns:///bigquerystorage.{TPC_UNIVERSE}:443",
                False,
                id="grpc_dns_tpc_target",
            ),
            pytest.param("http://localhost:9050", False, id="local_emulator"),
        ],
    )
    def test_is_googleapis_host(self, target: str, expected: bool) -> None:
        assert _is_googleapis_host(target) is expected


class TPCClientConformanceMixin:
    """Reusable baseline conformance suite for client and veneer classes."""

    def _make_client(self, **kwargs):  # pragma: NO COVER
        raise NotImplementedError

    def _get_effective_endpoint(self, client) -> str:  # pragma: NO COVER
        raise NotImplementedError

    @pytest.mark.parametrize(
        "client_options",
        [
            pytest.param(
                {"universe_domain": TPC_UNIVERSE},
                id="dict_options",
            ),
            pytest.param(
                MappingProxyType({"universe_domain": TPC_UNIVERSE}),
                id="mapping_proxy_options",
            ),
            pytest.param(
                client_options_lib.ClientOptions(universe_domain=TPC_UNIVERSE),
                id="client_options_object",
            ),
        ],
    )
    def test_explicit_tpc_client_options_routes_to_tpc(
        self, assert_no_googleapis_calls, client_options
    ):
        creds = make_mock_credentials(TPC_UNIVERSE)

        client = self._make_client(
            credentials=creds,
            client_options=client_options,
        )

        endpoint = self._get_effective_endpoint(client)
        assert client.universe_domain == TPC_UNIVERSE
        assert TPC_UNIVERSE in endpoint
        assert "googleapis.com" not in endpoint
        with pytest.raises(AttributeError):
            setattr(client, "universe_domain", DEFAULT_UNIVERSE)

    def test_env_var_universe_with_adc_routes_to_tpc(
        self, monkeypatch, assert_no_googleapis_calls
    ):
        monkeypatch.setenv("GOOGLE_CLOUD_UNIVERSE_DOMAIN", TPC_UNIVERSE)
        tpc_adc = make_mock_credentials(TPC_UNIVERSE)

        with mock.patch.object(
            google.auth,
            "default",
            autospec=True,
            spec_set=True,
            return_value=(tpc_adc, DEFAULT_PROJECT_ID),
        ):
            client = self._make_client()

        endpoint = self._get_effective_endpoint(client)
        assert client.universe_domain == TPC_UNIVERSE
        assert TPC_UNIVERSE in endpoint
        assert "googleapis.com" not in endpoint

    @pytest.mark.parametrize(
        ("creds_universe", "client_options", "expected_pattern"),
        [
            pytest.param(
                TPC_UNIVERSE,
                None,
                rf"\(googleapis\.com\).*\({TPC_UNIVERSE}\)",
                id="tpc_creds_on_default_gdu_client",
            ),
            pytest.param(
                DEFAULT_UNIVERSE,
                client_options_lib.ClientOptions(universe_domain=TPC_UNIVERSE),
                rf"\({TPC_UNIVERSE}\).*\(googleapis\.com\)",
                id="gdu_creds_on_tpc_client_options",
            ),
            pytest.param(
                TPC_UNIVERSE,
                {"api_endpoint": TPC_BQ_API_ENDPOINT},
                rf"\(googleapis\.com\).*\({TPC_UNIVERSE}\)",
                id="tpc_creds_with_custom_api_endpoint_only",
            ),
        ],
    )
    def test_mismatched_credentials_and_client_universe_fails_closed(
        self,
        assert_no_googleapis_calls,
        creds_universe,
        client_options,
        expected_pattern,
    ):
        creds = make_mock_credentials(creds_universe)

        with pytest.raises(UniverseMismatchError, match=expected_pattern):
            self._make_client(credentials=creds, client_options=client_options)

    def test_empty_client_options_and_bare_mock_creds_default_to_gdu(self):
        bare_mock = mock.create_autospec(
            FakeScopedQuotaCredentials, instance=True, spec_set=True
        )
        bare_mock.requires_scopes = False
        bare_mock.with_scopes.return_value = bare_mock

        client = self._make_client(
            credentials=bare_mock,
            client_options=client_options_lib.ClientOptions(),
        )

        assert client.universe_domain == DEFAULT_UNIVERSE

    def test_anonymous_credentials_exempt_in_tpc(self, assert_no_googleapis_calls):
        anon = auth_credentials.AnonymousCredentials()

        client = self._make_client(
            credentials=anon,
            client_options={"universe_domain": TPC_UNIVERSE},
        )

        assert client.universe_domain == TPC_UNIVERSE
        assert TPC_UNIVERSE in self._get_effective_endpoint(client)


class TestBigQueryClientTPCConformance(TPCClientConformanceMixin):
    def _make_client(self, **kwargs):
        return bigquery.Client(project=DEFAULT_PROJECT_ID, **kwargs)

    def _get_effective_endpoint(self, client) -> str:
        return client._connection.API_BASE_URL


class TestEnsureBqStorageClientTPC:
    """Tests for _ensure_bqstorage_client universe propagation and endpoint routing."""

    @pytest.mark.parametrize(
        "make_options",
        [
            pytest.param(lambda: None, id="none_options"),
            pytest.param(dict, id="empty_dict_options"),
            pytest.param(
                lambda: {"universe_domain": ""},
                id="empty_string_universe_dict",
            ),
            pytest.param(
                client_options_lib.ClientOptions,
                id="empty_client_options_obj",
            ),
            pytest.param(
                lambda: client_options_lib.ClientOptions(universe_domain=""),
                id="empty_string_universe_obj",
            ),
        ],
    )
    def test_inherits_parent_tpc_universe_when_child_universe_unset(
        self, assert_no_googleapis_calls, make_options
    ):
        pytest.importorskip("google.cloud.bigquery_storage")
        creds = make_mock_credentials(TPC_UNIVERSE)
        client = bigquery.Client(
            project=DEFAULT_PROJECT_ID,
            credentials=creds,
            client_options={"universe_domain": TPC_UNIVERSE},
        )

        bqstorage_client = client._ensure_bqstorage_client(
            client_options=make_options()
        )

        assert bqstorage_client is not None
        assert bqstorage_client.universe_domain == TPC_UNIVERSE
        assert TPC_UNIVERSE in bqstorage_client.api_endpoint
        assert "googleapis.com" not in bqstorage_client.api_endpoint

    def test_preserves_sibling_options_without_mutating_caller_inputs(
        self, assert_no_googleapis_calls
    ):
        pytest.importorskip("google.cloud.bigquery_storage")
        creds = make_mock_credentials(TPC_UNIVERSE)
        client = bigquery.Client(
            project=DEFAULT_PROJECT_ID,
            credentials=creds,
            client_options={"universe_domain": TPC_UNIVERSE},
        )
        caller_options = client_options_lib.ClientOptions(quota_project_id="qp-1")
        caller_dict: dict[str, Any] = {"quota_project_id": "qp-2"}

        propagated_obj = _helpers._inherit_universe_in_client_options(
            TPC_UNIVERSE, caller_options
        )
        propagated_dict = _helpers._inherit_universe_in_client_options(
            TPC_UNIVERSE, caller_dict
        )
        bqs_from_obj = client._ensure_bqstorage_client(client_options=caller_options)
        bqs_from_dict = client._ensure_bqstorage_client(client_options=caller_dict)

        assert propagated_obj is not None
        assert propagated_obj.universe_domain == TPC_UNIVERSE
        assert propagated_obj.quota_project_id == "qp-1"
        assert propagated_dict is not None
        assert propagated_dict.universe_domain == TPC_UNIVERSE
        assert propagated_dict.quota_project_id == "qp-2"
        assert bqs_from_obj is not None
        assert bqs_from_obj.universe_domain == TPC_UNIVERSE
        assert bqs_from_dict is not None
        assert bqs_from_dict.universe_domain == TPC_UNIVERSE
        assert caller_options.universe_domain is None
        assert caller_options.quota_project_id == "qp-1"
        assert caller_dict == {"quota_project_id": "qp-2"}

    @pytest.mark.parametrize(
        "make_options",
        [
            pytest.param(lambda: None, id="none_options"),
            pytest.param(dict, id="empty_dict_options"),
            pytest.param(
                client_options_lib.ClientOptions,
                id="empty_client_options_obj",
            ),
        ],
    )
    def test_explicit_gdu_parent_overrides_tpc_env_var_in_bqstorage_client(
        self, monkeypatch, make_options
    ):
        pytest.importorskip("google.cloud.bigquery_storage")
        monkeypatch.setenv("GOOGLE_CLOUD_UNIVERSE_DOMAIN", TPC_UNIVERSE)
        gdu_creds = make_mock_credentials(DEFAULT_UNIVERSE)
        client = bigquery.Client(
            project=DEFAULT_PROJECT_ID,
            credentials=gdu_creds,
            client_options={"universe_domain": DEFAULT_UNIVERSE},
        )

        bqstorage_client = client._ensure_bqstorage_client(
            client_options=make_options()
        )

        assert bqstorage_client is not None
        assert bqstorage_client.universe_domain == DEFAULT_UNIVERSE
        assert "googleapis.com" in bqstorage_client.api_endpoint

    def test_default_gdu_parent_without_env_var_leaves_child_universe_unset(self):
        empty_obj = client_options_lib.ClientOptions()
        from_none = _helpers._inherit_universe_in_client_options(DEFAULT_UNIVERSE, None)
        from_dict = _helpers._inherit_universe_in_client_options(DEFAULT_UNIVERSE, {})
        from_obj = _helpers._inherit_universe_in_client_options(
            DEFAULT_UNIVERSE, empty_obj
        )

        assert from_none is None
        assert from_dict is not None
        assert from_dict.universe_domain is None
        assert from_obj is empty_obj
        assert from_obj.universe_domain is None

    @pytest.mark.parametrize(
        "child_options",
        [
            pytest.param(
                client_options_lib.ClientOptions(universe_domain=OTHER_TPC_UNIVERSE),
                id="client_options_obj",
            ),
            pytest.param(
                {"universe_domain": OTHER_TPC_UNIVERSE},
                id="client_options_dict",
            ),
        ],
    )
    def test_explicit_child_universe_domain_is_preserved_with_anon_creds(
        self, assert_no_googleapis_calls, child_options
    ):
        pytest.importorskip("google.cloud.bigquery_storage")
        anon = auth_credentials.AnonymousCredentials()
        client = bigquery.Client(
            project=DEFAULT_PROJECT_ID,
            credentials=anon,
            client_options={"universe_domain": TPC_UNIVERSE},
        )

        bqstorage_client = client._ensure_bqstorage_client(client_options=child_options)

        assert bqstorage_client is not None
        assert bqstorage_client.universe_domain == OTHER_TPC_UNIVERSE
        assert OTHER_TPC_UNIVERSE in bqstorage_client.api_endpoint

    def test_conflicting_child_universe_domain_fails_closed(
        self, assert_no_googleapis_calls
    ):
        pytest.importorskip("google.cloud.bigquery_storage")
        creds = make_mock_credentials(TPC_UNIVERSE)
        client = bigquery.Client(
            project=DEFAULT_PROJECT_ID,
            credentials=creds,
            client_options={"universe_domain": TPC_UNIVERSE},
        )

        with pytest.raises(
            UniverseMismatchError,
            match=rf"\({OTHER_TPC_UNIVERSE}\).*\({TPC_UNIVERSE}\)",
        ):
            client._ensure_bqstorage_client(
                client_options={"universe_domain": OTHER_TPC_UNIVERSE}
            )

    @pytest.mark.parametrize(
        "api_endpoint",
        [
            pytest.param(TPC_BQ_API_ENDPOINT, id="exact_default_tpc_endpoint"),
            pytest.param(
                f"{TPC_BQ_API_ENDPOINT}/",
                id="trailing_slash_default_tpc_endpoint",
            ),
        ],
    )
    def test_default_universe_api_endpoint_is_not_treated_as_custom(
        self, monkeypatch, assert_no_googleapis_calls, recwarn, api_endpoint
    ):
        pytest.importorskip("google.cloud.bigquery_storage")
        monkeypatch.setenv("BIGQUERY_EMULATOR_HOST", EMULATOR_HOST)
        creds = make_mock_credentials(TPC_UNIVERSE)
        client = bigquery.Client(
            project=DEFAULT_PROJECT_ID,
            credentials=creds,
            client_options={
                "universe_domain": TPC_UNIVERSE,
                "api_endpoint": api_endpoint,
            },
        )

        bqstorage_client = client._ensure_bqstorage_client()

        assert len(recwarn) == 0
        assert bqstorage_client is not None
        assert bqstorage_client.universe_domain == TPC_UNIVERSE
        assert TPC_UNIVERSE in bqstorage_client.api_endpoint

    def test_empty_emulator_host_env_var_is_not_treated_as_custom(
        self, monkeypatch, assert_no_googleapis_calls, recwarn
    ):
        pytest.importorskip("google.cloud.bigquery_storage")
        monkeypatch.setenv("BIGQUERY_EMULATOR_HOST", "")
        creds = make_mock_credentials(TPC_UNIVERSE)
        client = bigquery.Client(
            project=DEFAULT_PROJECT_ID,
            credentials=creds,
            client_options={"universe_domain": TPC_UNIVERSE},
        )

        bqstorage_client = client._ensure_bqstorage_client()

        assert len(recwarn) == 0
        assert bqstorage_client is not None
        assert bqstorage_client.universe_domain == TPC_UNIVERSE

    def test_custom_api_endpoint_without_bqstorage_endpoint_warns_via_dbapi(
        self, assert_no_googleapis_calls
    ):
        pytest.importorskip("google.cloud.bigquery_storage")
        untagged_creds = make_mock_credentials(DEFAULT_UNIVERSE)
        client = bigquery.Client(
            project=DEFAULT_PROJECT_ID,
            credentials=untagged_creds,
            client_options={"api_endpoint": TPC_BQ_API_ENDPOINT},
        )

        with pytest.warns(UserWarning, match=r"custom BigQuery api_endpoint.*REST"):
            conn = dbapi.connect(client=client)

        assert conn._bqstorage_client is None

    def test_emulator_host_in_tpc_universe_warns_and_falls_back_to_rest(
        self, monkeypatch, assert_no_googleapis_calls
    ):
        pytest.importorskip("google.cloud.bigquery_storage")
        monkeypatch.setenv("BIGQUERY_EMULATOR_HOST", EMULATOR_HOST)
        anon = auth_credentials.AnonymousCredentials()
        client = bigquery.Client(
            project=DEFAULT_PROJECT_ID,
            credentials=anon,
            client_options={"universe_domain": TPC_UNIVERSE},
        )

        assert client._connection.API_BASE_URL == EMULATOR_HOST
        with pytest.warns(UserWarning, match=r"BIGQUERY_EMULATOR_HOST.*REST"):
            bqstorage_client = client._ensure_bqstorage_client()

        assert bqstorage_client is None

    @pytest.mark.parametrize(
        "bqs_options",
        [
            pytest.param(
                client_options_lib.ClientOptions(
                    api_endpoint=TPC_BQSTORAGE_API_ENDPOINT
                ),
                id="client_options_obj",
            ),
            pytest.param(
                {"api_endpoint": TPC_BQSTORAGE_API_ENDPOINT},
                id="client_options_dict",
            ),
        ],
    )
    def test_custom_api_endpoint_allows_explicit_bqstorage_api_endpoint(
        self, assert_no_googleapis_calls, bqs_options
    ):
        pytest.importorskip("google.cloud.bigquery_storage")
        untagged_creds = make_mock_credentials(DEFAULT_UNIVERSE)
        client = bigquery.Client(
            project=DEFAULT_PROJECT_ID,
            credentials=untagged_creds,
            client_options={"api_endpoint": TPC_BQ_API_ENDPOINT},
        )

        bqstorage_client = client._ensure_bqstorage_client(client_options=bqs_options)

        assert bqstorage_client is not None
        assert TPC_UNIVERSE in bqstorage_client.api_endpoint
        assert "googleapis.com" not in bqstorage_client.api_endpoint

    def test_custom_api_endpoint_preserves_explicit_bqstorage_client_without_warning(
        self, assert_no_googleapis_calls, recwarn
    ):
        bigquery_storage = pytest.importorskip("google.cloud.bigquery_storage")
        untagged_creds = make_mock_credentials(DEFAULT_UNIVERSE)
        client = bigquery.Client(
            project=DEFAULT_PROJECT_ID,
            credentials=untagged_creds,
            client_options={"api_endpoint": TPC_BQ_API_ENDPOINT},
        )
        existing_bqs = mock.create_autospec(
            bigquery_storage.BigQueryReadClient, instance=True, spec_set=True
        )

        result = client._ensure_bqstorage_client(bqstorage_client=existing_bqs)

        assert len(recwarn) == 0
        assert result is existing_bqs

    def test_to_arrow_falls_back_cleanly_to_rest_on_custom_api_endpoint(
        self, assert_no_googleapis_calls
    ):
        pytest.importorskip("numpy")
        pyarrow = pytest.importorskip("pyarrow")
        pytest.importorskip("google.cloud.bigquery_storage")

        untagged_creds = make_mock_credentials(DEFAULT_UNIVERSE)
        client = bigquery.Client(
            project=DEFAULT_PROJECT_ID,
            credentials=untagged_creds,
            client_options={"api_endpoint": TPC_BQ_API_ENDPOINT},
        )
        fields = [schema.SchemaField("name", "STRING", mode="REQUIRED")]
        rows = [{"f": [{"v": "Alice"}]}]
        api_request = mock.create_autospec(
            client._connection.api_request,
            spec_set=True,
            return_value={"rows": rows},
        )

        row_iter = bq_table.RowIterator(
            client,
            api_request,
            "/projects/test-proj/datasets/ds/tables/tbl/data",
            fields,
            table=bq_table.TableReference.from_string("test-proj.ds.tbl"),
            total_rows=1,
        )

        with pytest.warns(UserWarning, match=r"custom BigQuery api_endpoint.*REST"):
            arrow_tbl = row_iter.to_arrow(create_bqstorage_client=True)

        assert isinstance(arrow_tbl, pyarrow.Table)
        assert arrow_tbl.to_pydict() == {"name": ["Alice"]}
