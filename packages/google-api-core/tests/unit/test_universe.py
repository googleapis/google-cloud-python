# Copyright 2024 Google LLC
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

import re
import types

import pytest
from google.auth import credentials as auth_credentials
from google.auth.exceptions import MutualTLSChannelError

from google.api_core import client_options as client_options_lib
from google.api_core import universe

from ..helpers import warn_deprecated_credentials_file

TPC_UNIVERSE = "apis-tpclp.goog"
ALT_UNIVERSE = "other.goog"
CHILD_UNIVERSE = "child.goog"
PARENT_ENDPOINT = "parent.custom.test:443"
CHILD_ENDPOINT = "child.custom.test:443"
TEST_QUOTA_PROJECT = "qp-1"
TEST_API_KEY = "secret-key"
TEST_CREDENTIALS_FILE = "/path/to/creds.json"


class _Fake_Credentials:
    def __init__(self, universe_domain=None):
        if universe_domain:
            self.universe_domain = universe_domain


class _StubCredentials(auth_credentials.Credentials):
    def __init__(self, universe_domain: str = universe.DEFAULT_UNIVERSE):
        super().__init__()
        self._test_universe_domain = universe_domain

    @property
    def universe_domain(self) -> str:
        return self._test_universe_domain

    def refresh(self, request):  # pragma: NO COVER
        pass


def test_determine_domain():
    domain_client = "foo.com"
    domain_env = "bar.com"

    assert universe.determine_domain(domain_client, domain_env) == domain_client
    assert universe.determine_domain(None, domain_env) == domain_env
    assert universe.determine_domain(domain_client, None) == domain_client
    assert universe.determine_domain(None, None) == universe.DEFAULT_UNIVERSE

    with pytest.raises(universe.EmptyUniverseError):
        universe.determine_domain("", None)

    with pytest.raises(universe.EmptyUniverseError):
        universe.determine_domain(None, "")


def test_compare_domains():
    fake_domain = "foo.com"
    another_fake_domain = "bar.com"

    assert universe.compare_domains(universe.DEFAULT_UNIVERSE, _Fake_Credentials())
    assert universe.compare_domains(fake_domain, _Fake_Credentials(fake_domain))

    with pytest.raises(universe.UniverseMismatchError) as excinfo:
        universe.compare_domains(
            universe.DEFAULT_UNIVERSE, _Fake_Credentials(fake_domain)
        )
    assert str(excinfo.value).find(universe.DEFAULT_UNIVERSE) >= 0
    assert str(excinfo.value).find(fake_domain) >= 0

    with pytest.raises(universe.UniverseMismatchError) as excinfo:
        universe.compare_domains(fake_domain, _Fake_Credentials())
    assert str(excinfo.value).find(fake_domain) >= 0
    assert str(excinfo.value).find(universe.DEFAULT_UNIVERSE) >= 0

    with pytest.raises(universe.UniverseMismatchError) as excinfo:
        universe.compare_domains(fake_domain, _Fake_Credentials(another_fake_domain))
    assert str(excinfo.value).find(fake_domain) >= 0
    assert str(excinfo.value).find(another_fake_domain) >= 0


def test_get_universe_domain():
    # When universe_domain is provided
    assert (
        universe.get_universe_domain("foo.com", default_universe="default.com")
        == "foo.com"
    )
    assert (
        universe.get_universe_domain("  foo.com  ", default_universe="default.com")
        == "foo.com"
    )

    # When universe_domain is None, falls back to default_universe
    assert (
        universe.get_universe_domain(None, default_universe="default.com")
        == "default.com"
    )

    # When multiple potential universes are provided, resolves in order of preference
    assert (
        universe.get_universe_domain(
            "foo.com", "bar.com", default_universe="default.com"
        )
        == "foo.com"
    )
    assert (
        universe.get_universe_domain(None, "bar.com", default_universe="default.com")
        == "bar.com"
    )
    assert (
        universe.get_universe_domain(None, None, default_universe="default.com")
        == "default.com"
    )

    # EmptyUniverseError raised when resolved value is empty string
    with pytest.raises(universe.EmptyUniverseError) as excinfo:
        universe.get_universe_domain("", default_universe="default.com")
    assert str(excinfo.value) == "Universe Domain cannot be an empty string."

    with pytest.raises(universe.EmptyUniverseError) as excinfo:
        universe.get_universe_domain("   ", default_universe="default.com")
    assert str(excinfo.value) == "Universe Domain cannot be an empty string."

    with pytest.raises(universe.EmptyUniverseError) as excinfo:
        universe.get_universe_domain(None, "", default_universe="default.com")
    assert str(excinfo.value) == "Universe Domain cannot be an empty string."


def test_get_default_mtls_endpoint():
    # Test valid API endpoints
    assert (
        universe.get_default_mtls_endpoint("foo.googleapis.com")
        == "foo.mtls.googleapis.com"
    )
    assert (
        universe.get_default_mtls_endpoint("foo.sandbox.googleapis.com")
        == "foo.mtls.sandbox.googleapis.com"
    )
    # Test case-insensitivity
    assert (
        universe.get_default_mtls_endpoint("foo.GoogleAPIs.com")
        == "foo.mtls.googleapis.com"
    )
    assert (
        universe.get_default_mtls_endpoint("foo.Sandbox.GoogleAPIs.com")
        == "foo.mtls.sandbox.googleapis.com"
    )

    # Test valid API endpoints with schemes
    assert (
        universe.get_default_mtls_endpoint("https://foo.googleapis.com")
        == "https://foo.mtls.googleapis.com"
    )
    assert (
        universe.get_default_mtls_endpoint("http://foo.googleapis.com:8080/v1")
        == "http://foo.mtls.googleapis.com:8080/v1"
    )

    # Test valid API endpoints with ports
    assert (
        universe.get_default_mtls_endpoint("foo.googleapis.com:443")
        == "foo.mtls.googleapis.com:443"
    )
    assert (
        universe.get_default_mtls_endpoint("foo.sandbox.googleapis.com:443")
        == "foo.mtls.sandbox.googleapis.com:443"
    )
    # Test case-insensitivity with ports
    assert (
        universe.get_default_mtls_endpoint("foo.GoogleAPIs.com:443")
        == "foo.mtls.googleapis.com:443"
    )
    assert (
        universe.get_default_mtls_endpoint("foo.Sandbox.GoogleAPIs.com:443")
        == "foo.mtls.sandbox.googleapis.com:443"
    )

    # Test endpoints that shouldn't be converted
    assert (
        universe.get_default_mtls_endpoint("foo.mtls.googleapis.com")
        == "foo.mtls.googleapis.com"
    )
    assert universe.get_default_mtls_endpoint("foo.com") == "foo.com"
    assert universe.get_default_mtls_endpoint("foo.com:8080") == "foo.com:8080"

    # Test empty/None endpoints
    assert universe.get_default_mtls_endpoint("") == ""
    assert universe.get_default_mtls_endpoint(None) is None

    # Test endpoints without host
    assert universe.get_default_mtls_endpoint("http://") == "http://"
    assert universe.get_default_mtls_endpoint("https://") == "https://"


@pytest.mark.parametrize(
    "api_override,universe_domain,default_universe,default_mtls_endpoint,default_endpoint_template,use_mtls,expected",
    [
        (
            "foo.com",
            "googleapis.com",
            "googleapis.com",
            "foo.mtls.googleapis.com",
            "foo.{UNIVERSE_DOMAIN}",
            True,
            "foo.com",
        ),
        (
            None,
            "googleapis.com",
            "googleapis.com",
            "foo.mtls.googleapis.com",
            "foo.{UNIVERSE_DOMAIN}",
            True,
            "foo.mtls.googleapis.com",
        ),
        (
            None,
            "googleapis.com",
            "googleapis.com",
            "foo.mtls.googleapis.com",
            "foo.{UNIVERSE_DOMAIN}",
            False,
            "foo.googleapis.com",
        ),
        (
            None,
            "bar.com",
            "googleapis.com",
            "foo.mtls.googleapis.com",
            "foo.{UNIVERSE_DOMAIN}",
            True,
            MutualTLSChannelError,
        ),
        (
            None,
            "googleapis.com",
            "googleapis.com",
            None,
            "foo.{UNIVERSE_DOMAIN}",
            True,
            ValueError,
        ),
    ],
)
def test_get_api_endpoint(
    api_override,
    universe_domain,
    default_universe,
    default_mtls_endpoint,
    default_endpoint_template,
    use_mtls,
    expected,
):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            universe.get_api_endpoint(
                api_override,
                universe_domain,
                default_universe,
                default_mtls_endpoint,
                default_endpoint_template,
                use_mtls,
            )
    else:
        assert (
            universe.get_api_endpoint(
                api_override,
                universe_domain,
                default_universe,
                default_mtls_endpoint,
                default_endpoint_template,
                use_mtls,
            )
            == expected
        )


class TestResolveClientUniverse:
    def test_default_argument_omitted(self):
        assert universe.resolve_client_universe() == universe.DEFAULT_UNIVERSE

    @pytest.mark.parametrize(
        ("client_options", "env_val", "expected"),
        [
            pytest.param(None, None, universe.DEFAULT_UNIVERSE, id="default_none"),
            pytest.param({}, None, universe.DEFAULT_UNIVERSE, id="empty_dict"),
            pytest.param(
                client_options_lib.ClientOptions(),
                None,
                universe.DEFAULT_UNIVERSE,
                id="empty_client_options",
            ),
            pytest.param(
                None,
                TPC_UNIVERSE,
                TPC_UNIVERSE,
                id="env_var_fallback",
            ),
            pytest.param(
                {"universe_domain": None},
                f"  {TPC_UNIVERSE}  ",
                TPC_UNIVERSE,
                id="dict_none_falls_back_to_stripped_env",
            ),
            pytest.param(
                {"universe_domain": TPC_UNIVERSE},
                None,
                TPC_UNIVERSE,
                id="dict_explicit",
            ),
            pytest.param(
                types.MappingProxyType({"universe_domain": TPC_UNIVERSE}),
                ALT_UNIVERSE,
                TPC_UNIVERSE,
                id="mapping_proxy_overrides_env",
            ),
            pytest.param(
                client_options_lib.ClientOptions(universe_domain=TPC_UNIVERSE),
                ALT_UNIVERSE,
                TPC_UNIVERSE,
                id="client_options_overrides_env",
            ),
            pytest.param(
                {"universe_domain": universe.DEFAULT_UNIVERSE},
                TPC_UNIVERSE,
                universe.DEFAULT_UNIVERSE,
                id="explicit_gdu_overrides_tpc_env",
            ),
        ],
    )
    def test_precedence(self, monkeypatch, client_options, env_val, expected):
        if env_val is not None:
            monkeypatch.setenv(universe.UNIVERSE_DOMAIN_ENV, env_val)

        assert universe.resolve_client_universe(client_options) == expected

    @pytest.mark.parametrize(
        ("client_options", "env_val"),
        [
            pytest.param({"universe_domain": ""}, None, id="empty_in_dict"),
            pytest.param(
                {"universe_domain": ""},
                TPC_UNIVERSE,
                id="empty_in_dict_not_masked_by_env",
            ),
            pytest.param(
                client_options_lib.ClientOptions(universe_domain="   "),
                None,
                id="whitespace_in_client_options",
            ),
            pytest.param(None, "", id="empty_in_env"),
            pytest.param(None, "   ", id="whitespace_in_env"),
        ],
    )
    def test_empty_raises(self, monkeypatch, client_options, env_val):
        if env_val is not None:
            monkeypatch.setenv(universe.UNIVERSE_DOMAIN_ENV, env_val)

        with pytest.raises(
            universe.EmptyUniverseError,
            match="Universe Domain cannot be an empty string",
        ):
            universe.resolve_client_universe(client_options)

    def test_invalid_client_options_type_raises_type_error(self):
        with pytest.raises(TypeError, match="ClientOptions instance, Mapping, or None"):
            # Pass an invalid str on purpose to verify runtime TypeError handling;
            # mypy flags the intentional type mismatch without this ignore.
            universe.resolve_client_universe("invalid")  # type: ignore[arg-type]


class TestValidateCredentialsUniverse:
    @pytest.mark.parametrize(
        ("client_universe", "credentials"),
        [
            pytest.param(
                universe.DEFAULT_UNIVERSE,
                None,
                id="none_in_default_universe",
            ),
            pytest.param(TPC_UNIVERSE, None, id="none_in_custom_universe"),
            pytest.param(
                universe.DEFAULT_UNIVERSE,
                auth_credentials.AnonymousCredentials(),
                id="anonymous_in_default_universe",
            ),
            pytest.param(
                TPC_UNIVERSE,
                auth_credentials.AnonymousCredentials(),
                id="anonymous_in_custom_universe",
            ),
        ],
    )
    def test_exempts_none_and_anonymous(self, client_universe, credentials):
        assert (
            universe.validate_credentials_universe(client_universe, credentials) is None
        )

    @pytest.mark.parametrize(
        ("client_universe", "credentials"),
        [
            pytest.param(
                universe.DEFAULT_UNIVERSE,
                _StubCredentials(universe.DEFAULT_UNIVERSE),
                id="default_universe",
            ),
            pytest.param(
                TPC_UNIVERSE,
                _StubCredentials(TPC_UNIVERSE),
                id="custom_universe",
            ),
            pytest.param(
                universe.DEFAULT_UNIVERSE,
                _Fake_Credentials(),
                id="legacy_credentials_without_attr_default_to_gdu",
            ),
        ],
    )
    def test_matching_universes_succeed(self, client_universe, credentials):
        assert (
            universe.validate_credentials_universe(client_universe, credentials) is None
        )

    @pytest.mark.parametrize(
        ("client_universe", "cred_universe"),
        [
            pytest.param(
                universe.DEFAULT_UNIVERSE,
                TPC_UNIVERSE,
                id="gdu_vs_tpc",
            ),
            pytest.param(
                TPC_UNIVERSE,
                universe.DEFAULT_UNIVERSE,
                id="tpc_vs_gdu",
            ),
            pytest.param(
                TPC_UNIVERSE,
                ALT_UNIVERSE,
                id="tpc_vs_other_tpc",
            ),
        ],
    )
    def test_mismatch_raises(self, client_universe, cred_universe):
        creds = _StubCredentials(cred_universe)
        expected_pattern = (
            rf"configured universe domain \({re.escape(client_universe)}\)"
            rf".*credentials \({re.escape(cred_universe)}\)"
        )

        with pytest.raises(universe.UniverseMismatchError, match=expected_pattern):
            universe.validate_credentials_universe(client_universe, creds)

    def test_legacy_credentials_without_universe_attr_mismatch_custom_universe(self):
        with pytest.raises(
            universe.UniverseMismatchError,
            match=r"configured universe domain \(apis-tpclp\.goog\).*credentials \(googleapis\.com\)",
        ):
            # Verify runtime getattr fallback for legacy custom credential objects;
            # mypy expects google.auth.credentials.Credentials.
            universe.validate_credentials_universe(
                TPC_UNIVERSE,
                _Fake_Credentials(),  # type: ignore[arg-type]
            )


class TestInheritUniverseInClientOptions:
    @pytest.mark.parametrize(
        "env_val",
        [
            pytest.param(None, id="env_unset"),
            pytest.param(universe.DEFAULT_UNIVERSE, id="env_matches_gdu"),
            pytest.param(f"  {universe.DEFAULT_UNIVERSE}  ", id="env_padded_gdu"),
        ],
    )
    def test_none_options_in_default_universe_returns_none(self, monkeypatch, env_val):
        if env_val is not None:
            monkeypatch.setenv(universe.UNIVERSE_DOMAIN_ENV, env_val)

        assert (
            universe.inherit_universe_in_client_options(universe.DEFAULT_UNIVERSE, None)
            is None
        )

    @pytest.mark.parametrize(
        ("parent_universe", "env_val", "expected_universe"),
        [
            pytest.param(
                TPC_UNIVERSE,
                None,
                TPC_UNIVERSE,
                id="custom_parent_creates_options",
            ),
            pytest.param(
                universe.DEFAULT_UNIVERSE,
                TPC_UNIVERSE,
                universe.DEFAULT_UNIVERSE,
                id="explicit_gdu_parent_overrides_tpc_env",
            ),
            pytest.param(
                universe.DEFAULT_UNIVERSE,
                "",
                universe.DEFAULT_UNIVERSE,
                id="explicit_gdu_parent_overrides_empty_env",
            ),
            pytest.param(
                universe.DEFAULT_UNIVERSE,
                "   ",
                universe.DEFAULT_UNIVERSE,
                id="explicit_gdu_parent_overrides_whitespace_env",
            ),
        ],
    )
    def test_none_options_propagates_universe(
        self, monkeypatch, parent_universe, env_val, expected_universe
    ):
        if env_val is not None:
            monkeypatch.setenv(universe.UNIVERSE_DOMAIN_ENV, env_val)

        opts = universe.inherit_universe_in_client_options(parent_universe, None)

        assert opts is not None
        assert opts.universe_domain == expected_universe

    @pytest.mark.parametrize(
        ("parent_universe", "input_dict", "expected_universe"),
        [
            pytest.param(
                TPC_UNIVERSE,
                {"quota_project_id": TEST_QUOTA_PROJECT},
                TPC_UNIVERSE,
                id="custom_parent_inherits_onto_unset_mapping",
            ),
            pytest.param(
                universe.DEFAULT_UNIVERSE,
                {"quota_project_id": TEST_QUOTA_PROJECT},
                None,
                id="default_parent_leaves_unset_mapping_none",
            ),
            pytest.param(
                TPC_UNIVERSE,
                {
                    "quota_project_id": TEST_QUOTA_PROJECT,
                    "universe_domain": CHILD_UNIVERSE,
                },
                CHILD_UNIVERSE,
                id="preserves_explicit_child_universe",
            ),
            pytest.param(
                TPC_UNIVERSE,
                {"quota_project_id": TEST_QUOTA_PROJECT, "universe_domain": ""},
                "",
                id="preserves_explicit_empty_string_in_mapping",
            ),
        ],
    )
    def test_mapping_options_universe_inheritance(
        self, parent_universe, input_dict, expected_universe
    ):
        caller_dict = dict(input_dict)

        opts = universe.inherit_universe_in_client_options(parent_universe, caller_dict)

        assert opts is not None
        assert opts.universe_domain == expected_universe
        assert opts.quota_project_id == TEST_QUOTA_PROJECT
        assert caller_dict == input_dict

    @pytest.mark.parametrize(
        "cred_entry",
        [
            pytest.param(
                {"credentials_file": TEST_CREDENTIALS_FILE},
                id="clears_credentials_file",
            ),
            pytest.param({"api_key": TEST_API_KEY}, id="clears_api_key"),
        ],
    )
    def test_mapping_clears_credentials_when_requested(self, cred_entry):
        caller_dict = {"universe_domain": CHILD_UNIVERSE, **cred_entry}

        opts = universe.inherit_universe_in_client_options(
            TPC_UNIVERSE,
            caller_dict,
            clear_credentials=True,
        )

        assert opts is not None
        assert opts.universe_domain == CHILD_UNIVERSE
        assert opts.credentials_file is None
        assert opts.api_key is None
        assert caller_dict == {"universe_domain": CHILD_UNIVERSE, **cred_entry}

    def test_mapping_preserves_credentials_when_clear_credentials_false(self):
        opts = universe.inherit_universe_in_client_options(
            TPC_UNIVERSE,
            {
                "credentials_file": TEST_CREDENTIALS_FILE,
                "api_key": TEST_API_KEY,
            },
            clear_credentials=False,
        )

        assert opts is not None
        assert opts.universe_domain == TPC_UNIVERSE
        assert opts.credentials_file == TEST_CREDENTIALS_FILE
        assert opts.api_key == TEST_API_KEY

    @pytest.mark.parametrize(
        ("parent_universe", "initial_universe", "clear_credentials"),
        [
            pytest.param(
                universe.DEFAULT_UNIVERSE,
                None,
                False,
                id="default_parent_unset_child",
            ),
            pytest.param(
                universe.DEFAULT_UNIVERSE,
                None,
                True,
                id="clear_credentials_without_creds_set",
            ),
            pytest.param(
                TPC_UNIVERSE,
                CHILD_UNIVERSE,
                False,
                id="explicit_child_universe_preserved",
            ),
            pytest.param(
                TPC_UNIVERSE,
                "",
                False,
                id="explicit_empty_child_universe_preserved",
            ),
        ],
    )
    def test_client_options_obj_no_changes_returns_same_instance(
        self, parent_universe, initial_universe, clear_credentials
    ):
        original = client_options_lib.ClientOptions(
            universe_domain=initial_universe,
            quota_project_id=TEST_QUOTA_PROJECT,
        )

        result = universe.inherit_universe_in_client_options(
            parent_universe,
            original,
            clear_credentials=clear_credentials,
        )

        assert result is original
        assert result.universe_domain == initial_universe

    def test_client_options_obj_inherits_via_shallow_copy(self):
        original = client_options_lib.ClientOptions(
            quota_project_id=TEST_QUOTA_PROJECT,
            api_key=TEST_API_KEY,
        )

        result = universe.inherit_universe_in_client_options(TPC_UNIVERSE, original)

        assert result is not original
        assert result is not None
        assert result.universe_domain == TPC_UNIVERSE
        assert result.quota_project_id == TEST_QUOTA_PROJECT
        assert result.api_key == TEST_API_KEY
        assert original.universe_domain is None

    @pytest.mark.parametrize(
        ("initial_universe", "expected_universe"),
        [
            pytest.param(CHILD_UNIVERSE, CHILD_UNIVERSE, id="clear_api_key_only"),
            pytest.param(None, TPC_UNIVERSE, id="inherit_universe_and_clear_api_key"),
        ],
    )
    def test_client_options_obj_clears_api_key(
        self, initial_universe, expected_universe
    ):
        original = client_options_lib.ClientOptions(
            universe_domain=initial_universe,
            api_key=TEST_API_KEY,
        )

        result = universe.inherit_universe_in_client_options(
            TPC_UNIVERSE,
            original,
            clear_credentials=True,
        )

        assert result is not original
        assert result is not None
        assert result.universe_domain == expected_universe
        assert result.api_key is None
        assert original.universe_domain == initial_universe
        assert original.api_key == TEST_API_KEY

    def test_client_options_obj_clears_credentials_file(self):
        with warn_deprecated_credentials_file():
            original = client_options_lib.ClientOptions(
                credentials_file=TEST_CREDENTIALS_FILE,
            )

        result = universe.inherit_universe_in_client_options(
            TPC_UNIVERSE,
            original,
            clear_credentials=True,
        )

        assert result is not original
        assert result is not None
        assert result.universe_domain == TPC_UNIVERSE
        assert result.credentials_file is None
        assert original.credentials_file == TEST_CREDENTIALS_FILE

    @pytest.mark.parametrize(
        ("parent_universe", "expected_universe"),
        [
            pytest.param(universe.DEFAULT_UNIVERSE, None, id="default_parent"),
            pytest.param(TPC_UNIVERSE, TPC_UNIVERSE, id="custom_parent"),
        ],
    )
    def test_none_options_inherits_parent_api_endpoint(
        self, parent_universe, expected_universe
    ):
        opts = universe.inherit_universe_in_client_options(
            parent_universe,
            None,
            parent_api_endpoint=PARENT_ENDPOINT,
        )

        assert opts is not None
        assert opts.api_endpoint == PARENT_ENDPOINT
        assert opts.universe_domain == expected_universe

    @pytest.mark.parametrize(
        ("child_dict", "expected_endpoint", "expected_universe"),
        [
            pytest.param(
                {"quota_project_id": TEST_QUOTA_PROJECT},
                PARENT_ENDPOINT,
                TPC_UNIVERSE,
                id="unset_child_inherits_parent_endpoint_and_universe",
            ),
            pytest.param(
                {"api_endpoint": CHILD_ENDPOINT},
                CHILD_ENDPOINT,
                TPC_UNIVERSE,
                id="explicit_child_endpoint_wins_and_inherits_universe",
            ),
            pytest.param(
                {"universe_domain": CHILD_UNIVERSE},
                None,
                CHILD_UNIVERSE,
                id="explicit_child_universe_blocks_parent_endpoint",
            ),
            pytest.param(
                {"universe_domain": universe.DEFAULT_UNIVERSE},
                None,
                universe.DEFAULT_UNIVERSE,
                id="explicit_gdu_child_universe_blocks_parent_endpoint",
            ),
        ],
    )
    def test_mapping_parent_api_endpoint_precedence(
        self, child_dict, expected_endpoint, expected_universe
    ):
        caller_dict = dict(child_dict)

        opts = universe.inherit_universe_in_client_options(
            TPC_UNIVERSE,
            caller_dict,
            parent_api_endpoint=PARENT_ENDPOINT,
        )

        assert opts is not None
        assert opts.api_endpoint == expected_endpoint
        assert opts.universe_domain == expected_universe
        assert caller_dict == child_dict

    @pytest.mark.parametrize(
        (
            "parent_universe",
            "child_endpoint",
            "child_universe",
            "expected_endpoint",
            "expected_universe",
            "expect_same_instance",
        ),
        [
            pytest.param(
                universe.DEFAULT_UNIVERSE,
                None,
                None,
                PARENT_ENDPOINT,
                None,
                False,
                id="default_parent_copies_only_parent_endpoint",
            ),
            pytest.param(
                TPC_UNIVERSE,
                None,
                None,
                PARENT_ENDPOINT,
                TPC_UNIVERSE,
                False,
                id="custom_parent_copies_both_endpoint_and_universe",
            ),
            pytest.param(
                TPC_UNIVERSE,
                CHILD_ENDPOINT,
                None,
                CHILD_ENDPOINT,
                TPC_UNIVERSE,
                False,
                id="child_endpoint_preserved_while_universe_inherited",
            ),
            pytest.param(
                TPC_UNIVERSE,
                None,
                CHILD_UNIVERSE,
                None,
                CHILD_UNIVERSE,
                True,
                id="child_universe_blocks_parent_endpoint_returns_same_obj",
            ),
            pytest.param(
                universe.DEFAULT_UNIVERSE,
                CHILD_ENDPOINT,
                None,
                CHILD_ENDPOINT,
                None,
                True,
                id="default_parent_with_child_endpoint_returns_same_obj",
            ),
        ],
    )
    def test_client_options_obj_parent_api_endpoint_precedence(
        self,
        parent_universe,
        child_endpoint,
        child_universe,
        expected_endpoint,
        expected_universe,
        expect_same_instance,
    ):
        original = client_options_lib.ClientOptions(
            api_endpoint=child_endpoint,
            universe_domain=child_universe,
        )

        result = universe.inherit_universe_in_client_options(
            parent_universe,
            original,
            parent_api_endpoint=PARENT_ENDPOINT,
        )

        assert result is not None
        assert (result is original) is expect_same_instance
        assert result.api_endpoint == expected_endpoint
        assert result.universe_domain == expected_universe
        assert original.api_endpoint == child_endpoint
        assert original.universe_domain == child_universe

    def test_invalid_client_options_type_raises_type_error(self):
        with pytest.raises(TypeError, match="ClientOptions instance, Mapping, or None"):
            # Pass an invalid str on purpose to verify runtime TypeError handling;
            # mypy flags the intentional type mismatch without this ignore.
            universe.inherit_universe_in_client_options(
                universe.DEFAULT_UNIVERSE,
                "invalid",  # type: ignore[arg-type]
            )


class TestIsGoogleapisHost:
    @pytest.mark.parametrize(
        ("target", "expected"),
        [
            pytest.param("storage.googleapis.com:443", True, id="grpc_host_port"),
            pytest.param("storage.googleapis.com", True, id="bare_service_host"),
            pytest.param("googleapis.com:443", True, id="root_domain_port"),
            pytest.param("googleapis.com", True, id="root_domain"),
            pytest.param(
                "storage-direct.googleapis.com:443", True, id="directpath_host"
            ),
            pytest.param("us-east1-pubsub.googleapis.com:443", True, id="zonal_host"),
            pytest.param("storage.mtls.googleapis.com:443", True, id="mtls_host"),
            pytest.param(
                "storage.mtls.sandbox.googleapis.com:443",
                True,
                id="mtls_sandbox_host",
            ),
            pytest.param(
                "us-central1-bigquery.rep.googleapis.com", True, id="rep_host"
            ),
            pytest.param("bigquery-psc.p.googleapis.com", True, id="psc_host"),
            pytest.param("oauth2.googleapis.com:443", True, id="label_trailing_digit"),
            pytest.param("3p.googleapis.com:443", True, id="label_leading_digit"),
            pytest.param("STORAGE.GOOGLEAPIS.COM:443", True, id="uppercase_host"),
            pytest.param(
                "dns:///storage.googleapis.com:443", True, id="dns_triple_slash"
            ),
            pytest.param(
                "DNS:///storage.googleapis.com:443",
                True,
                id="uppercase_dns_triple_slash",
            ),
            pytest.param("dns:storage.googleapis.com:443", True, id="dns_no_slash"),
            pytest.param(
                "dns://8.8.8.8/storage.googleapis.com:443",
                True,
                id="dns_with_authority",
            ),
            pytest.param(
                "https://storage.googleapis.com:443/v1?alt=json",
                True,
                id="https_url_with_path_and_query",
            ),
            pytest.param(
                "HTTPS://storage.googleapis.com:443/v1",
                True,
                id="uppercase_https_url",
            ),
            pytest.param("http://storage.googleapis.com:443", True, id="http_url"),
            pytest.param(
                "google-c2p:///storage-direct.googleapis.com?force-xds",
                True,
                id="google_c2p_directpath",
            ),
            pytest.param(
                "GOOGLE-C2P:///storage-direct.googleapis.com?force-xds",
                True,
                id="uppercase_google_c2p_directpath",
            ),
            pytest.param("storage.apis-tpclp.goog:443", False, id="tpc_host_port"),
            pytest.param(
                "dns:///storage.apis-tpclp.goog:443", False, id="dns_tpc_triple_slash"
            ),
            pytest.param(
                "dns://8.8.8.8/storage.apis-tpclp.goog:443",
                False,
                id="dns_tpc_with_authority",
            ),
            pytest.param("dns://8.8.8.8", False, id="dns_authority_without_target"),
            pytest.param(
                "dns://storage.googleapis.com:443",
                False,
                id="dns_googleapis_authority_without_target",
            ),
            pytest.param(
                "dns://storage.googleapis.com/storage.apis-tpclp.goog:443",
                False,
                id="dns_googleapis_authority_with_tpc_target",
            ),
            pytest.param(
                "dns:////storage.googleapis.com:443",
                False,
                id="dns_quad_slash_extra_path",
            ),
            pytest.param(
                "https://storage.apis-tpclp.goog:443/v1", False, id="https_tpc_url"
            ),
            pytest.param(
                "http:storage.googleapis.com",
                False,
                id="http_scheme_missing_slashes",
            ),
            pytest.param(
                "google-c2p:///storage.apis-tpclp.goog", False, id="c2p_tpc_target"
            ),
            pytest.param(
                "google-c2p://storage.googleapis.com",
                False,
                id="c2p_double_slash_authority",
            ),
            pytest.param(
                "google-c2p:storage.googleapis.com",
                False,
                id="c2p_no_slashes",
            ),
            pytest.param("evilgoogleapis.com:443", False, id="missing_dot_boundary"),
            pytest.param(
                "storage.googleapis.com.example.com:443",
                False,
                id="spoofed_trailing_suffix",
            ),
            pytest.param(
                "storage.googleapis.com:evil.com",
                False,
                id="invalid_non_numeric_port",
            ),
            pytest.param(
                "storage.googleapis.com:443:80",
                False,
                id="double_port_suffix",
            ),
            pytest.param(
                "storage.googleapis.com:443/evil.com",
                False,
                id="non_http_path_segment",
            ),
            pytest.param(".googleapis.com:443", False, id="leading_dot_label"),
            pytest.param("-direct.googleapis.com:443", False, id="leading_hyphen"),
            pytest.param("storage-.googleapis.com:443", False, id="trailing_hyphen"),
            pytest.param("a..b.googleapis.com:443", False, id="empty_middle_label"),
            pytest.param("https://?.googleapis.com", False, id="query_before_host"),
            pytest.param(
                "https://[invalid.googleapis.com", False, id="malformed_https_ipv6"
            ),
            pytest.param("[invalid.googleapis.com", False, id="malformed_bare_ipv6"),
            pytest.param("user@storage.googleapis.com:443", False, id="userinfo_at"),
            pytest.param(
                "storage.example.com:443@storage.googleapis.com",
                False,
                id="spoofed_userinfo_host",
            ),
            pytest.param(
                "storage.googleapis.com#example.com", False, id="fragment_hash"
            ),
            pytest.param(
                "another-c2p:///storage.googleapis.com", False, id="unknown_scheme"
            ),
            pytest.param("http://localhost:8080", False, id="localhost_emulator"),
            pytest.param("[::1]:8080", False, id="ipv6_loopback"),
            pytest.param("", False, id="empty_string"),
            # Verify runtime guard returns False if None is passed dynamically;
            # mypy expects str for url_or_target.
            pytest.param(None, False, id="none_input"),  # type: ignore[arg-type]
            # Verify runtime isinstance(str) guard rejects truthy non-str inputs;
            # mypy expects str for url_or_target.
            pytest.param(
                b"storage.googleapis.com:443",  # type: ignore[arg-type]
                False,
                id="bytes_input",
            ),
        ],
    )
    def test_is_googleapis_host(self, target, expected):
        assert universe.is_googleapis_host(target) is expected
