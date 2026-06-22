import pytest

from google.api_core.observability import options


@pytest.mark.parametrize(
    "env_vars, client_options, default_val, expected",
    [
        # Default fallback tests
        ({}, None, False, False),
        ({}, None, True, True),
        # Service-specific env var
        ({"GOOGLE_CLOUD_PYTHON_TRANSLATE_TRACES_ENABLED": "true"}, None, False, True),
        ({"GOOGLE_CLOUD_PYTHON_TRANSLATE_TRACES_ENABLED": "false"}, None, True, False),
        # Experimental fallback
        (
            {"GOOGLE_CLOUD_EXPERIMENTAL_PYTHON_TRANSLATE_TRACES_ENABLED": "true"},
            None,
            False,
            True,
        ),
        # Precedence: Service specific overrides global
        (
            {
                "GOOGLE_CLOUD_PYTHON_TRACES_ENABLED": "true",
                "GOOGLE_CLOUD_PYTHON_TRANSLATE_TRACES_ENABLED": "false",
            },
            None,
            False,
            False,
        ),
        (
            {
                "GOOGLE_CLOUD_PYTHON_TRACES_ENABLED": "false",
                "GOOGLE_CLOUD_PYTHON_TRANSLATE_TRACES_ENABLED": "true",
            },
            None,
            False,
            True,
        ),
        # Precedence: Client options override env vars
        (
            {"GOOGLE_CLOUD_PYTHON_TRANSLATE_TRACES_ENABLED": "false"},
            {"enable_traces": True},
            False,
            True,
        ),
    ],
)
def test_is_signal_enabled(
    monkeypatch, env_vars, client_options, default_val, expected
):
    # Setup environment variables using pytest's monkeypatch fixture
    for k, v in env_vars.items():
        monkeypatch.setenv(k, v)

    result = options.is_signal_enabled(
        "translate", "traces", client_options=client_options, default=default_val
    )
    assert result is expected


def test_legacy_var_with_warning(monkeypatch):
    monkeypatch.setenv("LEGACY_TRACE_VAR", "true")

    with pytest.warns(DeprecationWarning, match="LEGACY_TRACE_VAR"):
        result = options.is_signal_enabled(
            "translate", "traces", legacy_vars=["LEGACY_TRACE_VAR"]
        )
        assert result is True
