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

"""Telemetry Semantic Contract Validator for OpenTelemetry Spans.

Provides formal contract definitions and assertions for validating OpenTelemetry
spans across Tier 3 (Client API Method Spans) and Tier 4 (Transport Wire Spans).

Key Architectural Principles:
1. Strict Floor vs. Open/Strict Ceiling:
   - Tier 3 (Client API Method Spans): Strict floor AND strict ceiling.
     Tier 3 is 100% owned by `google-api-core`. No upstream package injects
     uncontrolled attributes into Tier 3. Any unexpected attribute indicates
     untracked drift or an unvetted addition ("weirdo" attribute).
   - Tier 4 (Transport Wire Spans): Strict floor with open ceiling.
     Tier 4 is instrumented by `opentelemetry-instrumentation-grpc` (and future
     HTTP instrumentors). Upstream Semantic Conventions evolve across minor
     releases (e.g., adding `network.transport`, `server.socket.address`).
     Enforcing a strict ceiling on Tier 4 would cause brittle test failures
     on upstream upgrades. Enforcing a strict floor guarantees that our required
     MVP attributes are always present without breaking on upstream churn.
2. Dynamic Namespaces:
   - Attributes with dynamic keys (such as `gcp.errors.metadata.<key>` flattened
     from Google Cloud `ErrorInfo.metadata`) are validated via `allowed_prefixes`.
3. Actionable Diagnostic Errors:
   - Failures explicitly indicate whether required attributes were missing,
     forbidden attributes were leaked, unexpected "weirdo" attributes appeared,
     or specific values failed equality or custom validator checks.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Mapping, Set, Tuple


@dataclass(frozen=True)
class SpanContract:
    """Semantic contract specification for OpenTelemetry spans.

    Attributes:
        required: Set of attribute keys that MUST be present on the span.
        optional: Set of known attribute keys that MAY be present on the span
            (e.g., non-default `server.port`, `gcp.grpc.resend_count`).
        allowed_prefixes: Tuple of prefix strings for dynamic attribute keys
            (e.g., `("gcp.errors.metadata.",)`).
        forbidden: Set of attribute keys that MUST NOT be present on the span
            (e.g., legacy `rpc.system` duplicate, or error attributes on success spans).
        strict_ceiling: If True, any attribute present on the span that is not in
            `required`, `optional`, or matched by `allowed_prefixes` will trigger
            a contract violation error.
    """

    required: Set[str] = field(default_factory=set)
    optional: Set[str] = field(default_factory=set)
    allowed_prefixes: Tuple[str, ...] = field(default_factory=tuple)
    forbidden: Set[str] = field(default_factory=set)
    strict_ceiling: bool = False


# ---------------------------------------------------------------------------
# Pre-defined Contracts
# ---------------------------------------------------------------------------

# Tier 3 (Client API Method Span) - Success Contract
# Strict floor and strict ceiling. Owned entirely by google-api-core.
T3_SUCCESS_CONTRACT = SpanContract(
    required={
        "rpc.system.name",
        "rpc.method",
        "rpc.response.status_code",
    },
    forbidden={
        "gcp.errors.domain",
        "error.type",
        "status.message",
        "rpc.system",
    },
    strict_ceiling=True,
)

# Tier 3 (Client API Method Span) - Error Contract
# Strict floor and strict ceiling with dynamic metadata prefix support.
T3_ERROR_CONTRACT = SpanContract(
    required={
        "rpc.system.name",
        "rpc.method",
        "rpc.response.status_code",
        "error.type",
        "status.message",
    },
    optional={
        "gcp.errors.domain",
    },
    allowed_prefixes=("gcp.errors.metadata.",),
    forbidden={
        "rpc.system",
    },
    strict_ceiling=True,
)

# Tier 4 (gRPC Transport Wire Span) - Success Contract
# Strict floor, open ceiling (absorbs upstream OTel gRPC semconv additions).
T4_GRPC_SUCCESS_CONTRACT = SpanContract(
    required={
        "rpc.system.name",
        "rpc.method",
        "rpc.response.status_code",
        "url.domain",
    },
    optional={
        "server.address",
        "server.port",
        "gcp.grpc.resend_count",
        "rpc.service",
        "rpc.system",  # Emitted natively by upstream opentelemetry-instrumentation-grpc
        "rpc.grpc.status_code",
        "net.peer.name",
        "net.peer.port",
    },
    forbidden=set(),
    strict_ceiling=False,
)

# Tier 4 (gRPC Transport Wire Span) - Error Contract
# Strict floor, open ceiling.
T4_GRPC_ERROR_CONTRACT = SpanContract(
    required={
        "rpc.system.name",
        "rpc.method",
        "url.domain",
    },
    optional={
        "server.address",
        "server.port",
        "gcp.grpc.resend_count",
        "rpc.service",
        "rpc.system",  # Emitted natively by upstream opentelemetry-instrumentation-grpc
        "rpc.grpc.status_code",
        "rpc.response.status_code",
        "net.peer.name",
        "net.peer.port",
    },
    forbidden=set(),
    strict_ceiling=False,
)

# Tier 4 (HTTP Transport Wire Span) - Success Contract
# Strict floor, open ceiling.
T4_HTTP_SUCCESS_CONTRACT = SpanContract(
    required={
        "http.request.method",
        "http.response.status_code",
        "url.domain",
    },
    optional={
        "server.address",
        "server.port",
        "url.template",
        "url.full",
        "http.request.body.size",
        "http.response.body.size",
    },
    forbidden={
        "error.type",
        "rpc.system.name",
    },
    strict_ceiling=False,
)

# Tier 4 (HTTP Transport Wire Span) - Error Contract
# Strict floor, open ceiling.
T4_HTTP_ERROR_CONTRACT = SpanContract(
    required={
        "http.request.method",
        "url.domain",
        "error.type",
    },
    optional={
        "http.response.status_code",
        "server.address",
        "server.port",
        "url.template",
        "url.full",
        "http.request.body.size",
        "http.response.body.size",
        "status.message",
    },
    forbidden={
        "rpc.system.name",
    },
    strict_ceiling=False,
)


def assert_span_contract(
    span_or_attrs: Any,
    contract: SpanContract,
    *,
    exact_values: Mapping[str, Any] | None = None,
    custom_validators: Mapping[str, Callable[[Any], bool]] | None = None,
    label: str | None = None,
) -> None:
    """Validates an OpenTelemetry span against a semantic contract specification.

    Args:
        span_or_attrs: A `ReadableSpan` instance or a dictionary of attribute key-value pairs.
        contract: The `SpanContract` defining required, optional, forbidden, and prefix rules.
        exact_values: Optional dictionary of attributes that must match exact expected values.
        custom_validators: Optional dictionary of attribute keys mapped to predicate callables.
        label: Optional human-readable description for debugging (e.g. "T3 Method Span").

    Raises:
        AssertionError: If any contract rule (required, forbidden, ceiling, or value) is violated.
    """
    if hasattr(span_or_attrs, "attributes"):
        actual_attrs: Mapping[str, Any] = span_or_attrs.attributes or {}
        span_name = getattr(span_or_attrs, "name", "unknown")
    elif isinstance(span_or_attrs, Mapping):
        actual_attrs = span_or_attrs
        span_name = "attribute_dict"
    else:
        raise TypeError(
            f"Expected ReadableSpan or Mapping, got {type(span_or_attrs).__name__}"
        )

    context_str = (
        f"[{label}] (span: '{span_name}')" if label else f"(span: '{span_name}')"
    )
    actual_keys = set(actual_attrs.keys())

    # 1. Floor Validation: All required attributes must be present
    missing_required = contract.required - actual_keys
    if missing_required:
        raise AssertionError(
            f"{context_str} Span contract floor violation: missing required attributes: "
            f"{sorted(missing_required)}. Present attributes: {sorted(actual_keys)}"
        )

    # 2. Forbidden Validation: No forbidden attributes must be present
    forbidden_found = contract.forbidden & actual_keys
    if forbidden_found:
        raise AssertionError(
            f"{context_str} Span contract forbidden violation: found disallowed attributes: "
            f"{sorted(forbidden_found)}."
        )

    # 3. Ceiling Validation (Drift / 'Weirdo' Detection):
    if contract.strict_ceiling:
        unrecognized: set[str] = set()
        for key in actual_keys:
            if key in contract.required or key in contract.optional:
                continue
            if any(key.startswith(prefix) for prefix in contract.allowed_prefixes):
                continue
            unrecognized.add(key)

        if unrecognized:
            raise AssertionError(
                f"{context_str} Span contract ceiling violation: unrecognized / untracked attributes "
                f"detected: {sorted(unrecognized)}. If these are intentional, register them in "
                f"`required`, `optional`, or `allowed_prefixes` of the contract."
            )

    # 4. Exact Value Validation
    if exact_values:
        for key, expected_val in exact_values.items():
            if key not in actual_attrs:
                raise AssertionError(
                    f"{context_str} Expected attribute '{key}' not found on span."
                )
            actual_val = actual_attrs[key]
            if actual_val != expected_val:
                raise AssertionError(
                    f"{context_str} Attribute value mismatch for '{key}': "
                    f"expected {expected_val!r}, got {actual_val!r}."
                )

    # 5. Custom Validator Predicates
    if custom_validators:
        for key, validator in custom_validators.items():
            if key not in actual_attrs:
                raise AssertionError(
                    f"{context_str} Expected attribute '{key}' for custom validation not found on span."
                )
            actual_val = actual_attrs[key]
            if not validator(actual_val):
                raise AssertionError(
                    f"{context_str} Attribute '{key}' with value {actual_val!r} "
                    f"failed custom validation predicate."
                )
