# -*- coding: utf-8 -*-
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

"""Helpers for detecting AI agents from ambient environment variables."""

import os
import re
from typing import Optional

MAX_AGENT_TOKEN_LENGTH = 64
_INVALID_AGENT_CHARS_RE = re.compile(r"[^a-zA-Z0-9_-]")

_TRUTHY_ENV_VALUES = frozenset({"1", "true", "t", "yes", "y", "on"})
_METRICS_OPT_OUT_ENV_VARS = (
    "GOOGLE_CLOUD_DISABLE_METRICS",
    "CLOUDSDK_CORE_DISABLE_USAGE_REPORTING",
)

# Evaluated in fixed priority order during client construction.
# Tuple structure: (ENV_VAR, OPTIONAL_ASSERTED_VALUE, OPTIONAL_CANONICAL_TOKEN)
# - If OPTIONAL_ASSERTED_VALUE is None, any non-empty string matches.
# - If OPTIONAL_CANONICAL_TOKEN is None, the sanitized env var value is used.
AI_AGENTS: tuple[tuple[str, Optional[str], Optional[str]], ...] = (
    ("AI_AGENT", None, None),
    ("ANTIGRAVITY_AGENT", None, "antigravity"),
    ("CLAUDECODE", None, "claude_code"),
    ("CLAUDE_CODE", None, "claude_code"),
    ("CURSOR_AGENT", None, "cursor"),
    ("CURSOR_TRACE_ID", None, "cursor"),
    ("CURSOR_EXTENSION_HOST_ROLE", "agent-exec", "cursor"),
    ("GEMINI_CLI", None, "gemini_cli"),
    ("CODEX_SANDBOX", None, "codex_cli"),
    ("CODEX_CI", None, "codex_cli"),
    ("CLINE_ACTIVE", None, "cline"),
    ("OPENCODE", None, "open_code"),
    ("OPENCODE_CLIENT", None, "open_code"),
    ("ANDROID_STUDIO_AGENT", None, "android_studio_agent"),
    ("KIRO_AGENT_PATH", None, "kiro"),
    ("COPILOT_MODEL", None, "github_copilot"),
    ("COPILOT_ALLOW_ALL", None, "github_copilot"),
    ("REPL_ID", None, "replit"),
    ("AUGMENT_AGENT", None, "augment"),
)


def _is_usage_reporting_disabled() -> bool:
    """Returns True if the user has opted out of metrics/usage reporting."""
    return any(
        os.environ.get(env_var, "").strip().lower() in _TRUTHY_ENV_VALUES
        for env_var in _METRICS_OPT_OUT_ENV_VARS
    )


def sanitize_agent_name(value: str) -> Optional[str]:
    """Sanitizes a custom agent name into a canonical header-safe token.

    Non-alphanumeric characters (except ``_`` and ``-``) are removed to prevent
    HTTP header injection, and the result is truncated to 64 characters so any
    returned token matches ``^[a-zA-Z0-9_-]{1,64}$``.

    Args:
        value (str): Raw agent identifier string.

    Returns:
        Optional[str]: The sanitized agent token, or ``None`` if no valid
            characters remain.
    """
    sanitized = _INVALID_AGENT_CHARS_RE.sub("", value)[:MAX_AGENT_TOKEN_LENGTH]
    return sanitized or None


def detect_ai_agent() -> Optional[str]:
    """Detects an active AI agent from ambient process environment variables.

    Evaluates known AI agent environment variables in priority order and returns
    the canonical agent token for the first matching non-empty variable. Returns
    ``None`` if metrics/usage reporting is disabled or no agent environment
    variable matches.

    Returns:
        Optional[str]: The canonical or sanitized AI agent token, or ``None``.
    """
    if _is_usage_reporting_disabled():
        return None

    for env_var, asserted_value, canonical_token in AI_AGENTS:
        raw_val = os.environ.get(env_var)
        if raw_val is None:
            continue
        val = raw_val.strip()
        if not val:
            continue
        if asserted_value is not None and val != asserted_value:
            continue
        if canonical_token is not None:
            return canonical_token
        sanitized = sanitize_agent_name(val)
        if sanitized is not None:
            return sanitized

    return None
