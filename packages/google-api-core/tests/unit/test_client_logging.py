import json
import logging

import pytest

from google.api_core import client_logging
from google.api_core._feature_gating_helpers import FeatureGatingError
from google.api_core.client_logging import (
    StructuredLogFormatter,
    initialize_logging,
    is_error_logging_enabled,
    setup_logging,
)

TEST_BASE_LOGGER_NAME = "foogle"
TEST_MODULE_LOGGER_NAME = f"{TEST_BASE_LOGGER_NAME}.bar"
TEST_CHILD_LOGGER_NAME = f"{TEST_BASE_LOGGER_NAME}.cloud.service"
DEFAULT_CONSUMER_PROJECT = "projects/123"
SAMPLE_TRACE_ID = "0123456789abcdef0123456789abcdef"
SAMPLE_SPAN_ID = "0123456789abcdef"


def reset_logger(scope):
    logger = logging.getLogger(scope)
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
        handler.close()
    logger.setLevel(logging.NOTSET)
    logger.propagate = True


@pytest.fixture
def isolated_base_logger(monkeypatch):
    """Isolates base logger state and resets mutated test loggers on teardown."""
    monkeypatch.setattr(client_logging, "_BASE_LOGGER_NAME", TEST_BASE_LOGGER_NAME)
    monkeypatch.setattr(client_logging, "_LOGGING_INITIALIZED", False)
    extra_scopes = []
    yield extra_scopes
    scopes_to_reset = {
        name
        for name, entry in logging.Logger.manager.loggerDict.items()
        if isinstance(entry, logging.Logger)
        and (
            name == TEST_BASE_LOGGER_NAME
            or name.startswith(f"{TEST_BASE_LOGGER_NAME}.")
        )
    }
    scopes_to_reset.update(extra_scopes)
    for scope in scopes_to_reset:
        reset_logger(scope)


def test_setup_logging_w_no_scopes(isolated_base_logger):
    setup_logging()
    base_logger = logging.getLogger(TEST_BASE_LOGGER_NAME)
    assert base_logger.handlers == []
    assert base_logger.propagate
    assert base_logger.level == logging.WARNING


def test_setup_logging_w_base_scope(isolated_base_logger):
    setup_logging(TEST_BASE_LOGGER_NAME)
    base_logger = logging.getLogger(TEST_BASE_LOGGER_NAME)
    assert isinstance(base_logger.handlers[0], logging.StreamHandler)
    assert not base_logger.propagate
    assert base_logger.level == logging.DEBUG


@pytest.mark.parametrize(
    ("scopes", "initial_level", "initial_propagate", "has_custom_handler"),
    [
        pytest.param(
            TEST_BASE_LOGGER_NAME,
            logging.NOTSET,
            False,
            False,
            id="propagate_false_with_base_scope",
        ),
        pytest.param(
            "",
            logging.DEBUG,
            True,
            False,
            id="custom_debug_level_with_no_scopes",
        ),
        pytest.param(
            TEST_MODULE_LOGGER_NAME,
            logging.INFO,
            True,
            False,
            id="custom_info_level_with_module_scope",
        ),
        pytest.param(
            "",
            logging.NOTSET,
            True,
            True,
            id="custom_handler_with_no_scopes",
        ),
    ],
)
def test_setup_logging_w_configured_scope(
    isolated_base_logger, scopes, initial_level, initial_propagate, has_custom_handler
):
    base_logger = logging.getLogger(TEST_BASE_LOGGER_NAME)
    base_logger.setLevel(initial_level)
    base_logger.propagate = initial_propagate
    expected_handlers = [logging.NullHandler()] if has_custom_handler else []
    for handler in expected_handlers:
        base_logger.addHandler(handler)

    setup_logging(scopes)

    assert base_logger.handlers == expected_handlers
    assert base_logger.propagate is initial_propagate
    assert base_logger.level == initial_level


@pytest.mark.parametrize(
    "scope",
    [
        pytest.param(TEST_MODULE_LOGGER_NAME, id="child_module_scope"),
        # TODO(https://github.com/googleapis/python-api-core/issues/759): update test once we add logic to ignore an incorrect scope.
        pytest.param("abc", id="non_google_scope"),
    ],
)
def test_setup_logging_w_non_base_scope(isolated_base_logger, scope):
    isolated_base_logger.append(scope)

    setup_logging(scope)

    base_logger = logging.getLogger(TEST_BASE_LOGGER_NAME)
    assert base_logger.handlers == []
    assert base_logger.propagate
    assert base_logger.level == logging.WARNING

    scoped_logger = logging.getLogger(scope)
    assert isinstance(scoped_logger.handlers[0], logging.StreamHandler)
    assert not scoped_logger.propagate
    assert scoped_logger.level == logging.DEBUG


def test_initialize_logging_default_unscoped_env(isolated_base_logger, monkeypatch):
    monkeypatch.delenv("GOOGLE_SDK_PYTHON_LOGGING_SCOPE", raising=False)

    initialize_logging()

    base_logger = logging.getLogger(TEST_BASE_LOGGER_NAME)
    assert base_logger.handlers == []
    assert base_logger.propagate
    assert base_logger.level == logging.WARNING


def test_initialize_logging_configures_scoped_and_base_loggers(
    isolated_base_logger, monkeypatch
):
    monkeypatch.setenv("GOOGLE_SDK_PYTHON_LOGGING_SCOPE", TEST_MODULE_LOGGER_NAME)

    initialize_logging()

    base_logger = logging.getLogger(TEST_BASE_LOGGER_NAME)
    assert base_logger.handlers == []
    assert base_logger.propagate
    assert base_logger.level == logging.WARNING

    module_logger = logging.getLogger(TEST_MODULE_LOGGER_NAME)
    assert isinstance(module_logger.handlers[0], logging.StreamHandler)
    assert not module_logger.propagate
    assert module_logger.level == logging.DEBUG


def test_initialize_logging_is_idempotent_after_first_call(
    isolated_base_logger, monkeypatch
):
    monkeypatch.setenv("GOOGLE_SDK_PYTHON_LOGGING_SCOPE", TEST_MODULE_LOGGER_NAME)
    initialize_logging()

    # Reset loggers to unconfigured defaults and change env scope so a second
    # execution of setup_logging() would mutate all three loggers:
    reset_logger(TEST_BASE_LOGGER_NAME)
    reset_logger(TEST_MODULE_LOGGER_NAME)
    monkeypatch.setenv(
        "GOOGLE_SDK_PYTHON_LOGGING_SCOPE", f"{TEST_BASE_LOGGER_NAME}.baz"
    )

    initialize_logging()

    assert logging.getLogger(TEST_BASE_LOGGER_NAME).level == logging.NOTSET
    assert logging.getLogger(TEST_MODULE_LOGGER_NAME).handlers == []
    assert logging.getLogger(f"{TEST_BASE_LOGGER_NAME}.baz").handlers == []


@pytest.mark.parametrize(
    ("level", "expected_enabled"),
    [
        pytest.param(logging.DEBUG, False, id="debug_disabled"),
        pytest.param(logging.INFO, False, id="info_disabled"),
        pytest.param(logging.WARNING - 1, False, id="below_warning_boundary_disabled"),
        pytest.param(logging.WARNING, True, id="warning_enabled"),
        pytest.param(logging.ERROR, True, id="error_enabled"),
    ],
)
def test_setup_logging_prevents_root_debug_from_enabling_child_debug(
    isolated_base_logger, caplog, level, expected_enabled
):
    """Verify root DEBUG does not enable DEBUG on unconfigured child loggers."""
    # Regression test for https://github.com/googleapis/google-cloud-python/issues/15149
    with caplog.at_level(logging.DEBUG):
        child_logger = logging.getLogger(TEST_CHILD_LOGGER_NAME)

        setup_logging()

        assert child_logger.isEnabledFor(level) is expected_enabled


def test_setup_logging_propagates_warning_and_error_to_root(
    isolated_base_logger, caplog
):
    """Verify child WARNING and ERROR logs propagate to root handlers."""
    # Regression test for https://github.com/googleapis/google-cloud-python/issues/15693
    child_logger = logging.getLogger(TEST_CHILD_LOGGER_NAME)
    setup_logging()

    with caplog.at_level(logging.DEBUG):
        child_logger.debug("debug message")
        child_logger.info("info message")
        child_logger.warning("warning message")
        child_logger.error("error message")

    assert caplog.record_tuples == [
        (TEST_CHILD_LOGGER_NAME, logging.WARNING, "warning message"),
        (TEST_CHILD_LOGGER_NAME, logging.ERROR, "error message"),
    ]

    # Post-initialization override allows DEBUG logs to propagate to root:
    caplog.clear()
    logging.getLogger(TEST_BASE_LOGGER_NAME).setLevel(logging.DEBUG)
    with caplog.at_level(logging.DEBUG):
        child_logger.debug("post-override debug")

    assert caplog.record_tuples == [
        (TEST_CHILD_LOGGER_NAME, logging.DEBUG, "post-override debug"),
    ]


def test_structured_log_formatter():
    # TODO(https://github.com/googleapis/python-api-core/issues/761): Test additional fields when implemented.
    record = logging.LogRecord(
        name="Appelation",
        level=logging.DEBUG,
        msg="This is a test message.",
        pathname="some/path",
        lineno=25,
        args=None,
        exc_info=None,
    )

    # Extra fields:
    record.rpcName = "bar"

    formatted_msg = StructuredLogFormatter().format(record)
    parsed_msg = json.loads(formatted_msg)

    assert parsed_msg["name"] == "Appelation"
    assert parsed_msg["severity"] == "DEBUG"
    assert parsed_msg["message"] == "This is a test message."
    assert parsed_msg["rpcName"] == "bar"


def test_structured_log_formatter_json_fields_and_wildcard_metadata():
    record = logging.LogRecord(
        name="google.cloud.secretmanager_v1",
        level=logging.ERROR,
        msg="RPC failed for /google.cloud.secretmanager.v1.SecretManagerService/GetSecret",
        pathname="some/path",
        lineno=42,
        args=None,
        exc_info=None,
    )
    extra_fields = {
        "rpcName": "/google.cloud.secretmanager.v1.SecretManagerService/GetSecret",
        "retryAttempt": 0,
        "rpc.system.name": "grpc",
        "rpc.response.status_code": "NOT_FOUND",
        "error.type": "RESOURCE_NOT_FOUND",
        "status.message": "Secret not found",
        "gcp.errors.domain": "googleapis.com",
        "gcp.errors.metadata": {"service": "secretmanager.googleapis.com"},
        "gcp.errors.metadata.service": "secretmanager.googleapis.com",
        "gcp.errors.metadata.consumer": DEFAULT_CONSUMER_PROJECT,
        "gcp.errors.metadata.is_retryable": False,
        "trace_id": SAMPLE_TRACE_ID,
        "span_id": SAMPLE_SPAN_ID,
        "logging.googleapis.com/trace": SAMPLE_TRACE_ID,
        "logging.googleapis.com/spanId": SAMPLE_SPAN_ID,
        "logging.googleapis.com/trace_sampled": False,
    }
    for k, v in extra_fields.items():
        setattr(record, k, v)
    record.json_fields = {"custom_json_field": "from_json_fields"}
    record.unrecognized_field = "should_be_ignored"

    formatted_msg = StructuredLogFormatter().format(record)
    parsed_msg = json.loads(formatted_msg)

    for k, v in extra_fields.items():
        assert parsed_msg[k] == v
    assert parsed_msg["custom_json_field"] == "from_json_fields"
    assert "json_fields" not in parsed_msg
    assert "unrecognized_field" not in parsed_msg


def test_structured_log_formatter_json_fields_only():
    record = logging.LogRecord(
        name="google.cloud.secretmanager_v1",
        level=logging.DEBUG,
        msg="Attempt failed",
        pathname="some/path",
        lineno=10,
        args=None,
        exc_info=None,
    )
    record.rpcName = "default_rpc"
    setattr(record, "gcp.errors.metadata.service", "default_service")
    record.json_fields = {
        "rpcName": "override_rpc",
        "gcp.errors.metadata.service": "override_service",
        "custom_from_json_fields": "preserved",
        "none_value": None,
    }

    formatted_msg = StructuredLogFormatter().format(record)
    parsed_msg = json.loads(formatted_msg)

    assert parsed_msg["rpcName"] == "override_rpc"
    assert parsed_msg["gcp.errors.metadata.service"] == "override_service"
    assert parsed_msg["custom_from_json_fields"] == "preserved"
    assert "none_value" not in parsed_msg
    assert "json_fields" not in parsed_msg
    assert list(parsed_msg.keys()) == [
        "timestamp",
        "severity",
        "name",
        "message",
        "rpcName",
        "gcp.errors.metadata.service",
        "custom_from_json_fields",
    ]


@pytest.mark.parametrize(
    "env_var_name,env_val,kwargs,expected",
    [
        pytest.param(
            "GOOGLE_SDK_EXPERIMENTAL_PYTHON_LOGGING_ENABLED",
            None,
            {},
            False,
            id="experimental_env_missing_default_false",
        ),
        pytest.param(
            "GOOGLE_SDK_EXPERIMENTAL_PYTHON_LOGGING_ENABLED",
            "true",
            {},
            True,
            id="experimental_env_true",
        ),
        pytest.param(
            "GOOGLE_SDK_EXPERIMENTAL_PYTHON_LOGGING_ENABLED",
            "true",
            {"client_options": {"logger_provider": object()}},
            True,
            id="experimental_env_true_with_logger_provider",
        ),
        pytest.param(
            "GOOGLE_SDK_EXPERIMENTAL_PYTHON_LOGGING_ENABLED",
            "false",
            {},
            False,
            id="experimental_env_false",
        ),
        pytest.param(
            "GOOGLE_SDK_PYTHON_LOGGING_ENABLED",
            None,
            {"env_var": "GOOGLE_SDK_PYTHON_LOGGING_ENABLED"},
            False,
            id="ga_env_missing_default_false",
        ),
        pytest.param(
            "GOOGLE_SDK_PYTHON_LOGGING_ENABLED",
            None,
            {
                "client_options": {"logger_provider": object()},
                "env_var": "GOOGLE_SDK_PYTHON_LOGGING_ENABLED",
            },
            True,
            id="ga_enabled_via_logger_provider",
        ),
        pytest.param(
            "GOOGLE_SDK_PYTHON_LOGGING_ENABLED",
            "true",
            {"env_var": "GOOGLE_SDK_PYTHON_LOGGING_ENABLED"},
            True,
            id="ga_enabled_via_env_var",
        ),
    ],
)
def test_is_error_logging_enabled(monkeypatch, env_var_name, env_val, kwargs, expected):
    if env_val is None:
        monkeypatch.delenv(env_var_name, raising=False)
    else:
        monkeypatch.setenv(env_var_name, env_val)

    assert is_error_logging_enabled(**kwargs) is expected


@pytest.mark.parametrize("env_val", [None, "false"], ids=["env_missing", "env_false"])
def test_is_error_logging_enabled_experimental_requires_env_var(monkeypatch, env_val):
    if env_val is None:
        monkeypatch.delenv(
            "GOOGLE_SDK_EXPERIMENTAL_PYTHON_LOGGING_ENABLED", raising=False
        )
    else:
        monkeypatch.setenv("GOOGLE_SDK_EXPERIMENTAL_PYTHON_LOGGING_ENABLED", env_val)

    with pytest.raises(FeatureGatingError):
        is_error_logging_enabled({"logger_provider": object()})
