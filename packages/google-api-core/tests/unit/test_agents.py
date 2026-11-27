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

import re

import pytest

from google.api_core import agents

_VALID_TOKEN_RE = re.compile(r"^[a-zA-Z0-9_-]{1,64}$")


def test_detect_ai_agent_none():
    assert agents.detect_ai_agent() is None


@pytest.mark.parametrize(
    ("env_var", "env_value", "expected"),
    [
        ("AI_AGENT", "custom_agent-1", "custom_agent-1"),
        ("ANTIGRAVITY_AGENT", "1", "antigravity"),
        ("ANTIGRAVITY_AGENT", "true", "antigravity"),
        ("CLAUDECODE", "1", "claude_code"),
        ("CLAUDE_CODE", "true", "claude_code"),
        ("CURSOR_AGENT", "1", "cursor"),
        ("CURSOR_TRACE_ID", "trace-123", "cursor"),
        ("CURSOR_EXTENSION_HOST_ROLE", "agent-exec", "cursor"),
        ("GEMINI_CLI", "1", "gemini_cli"),
        ("CODEX_SANDBOX", "seatbelt", "codex_cli"),
        ("CODEX_CI", "1", "codex_cli"),
        ("CODEX_THREAD_ID", "thread-abc", "codex_cli"),
        ("CLINE_ACTIVE", "true", "cline"),
        ("OPENCODE", "1", "open_code"),
        ("OPENCODE_CLIENT", "cli", "open_code"),
        ("ANDROID_STUDIO_AGENT", "true", "android_studio_agent"),
        ("KIRO_AGENT_PATH", "/usr/local/bin/kiro", "kiro"),
        ("COPILOT_MODEL", "gpt-4o", "github_copilot"),
        ("COPILOT_ALLOW_ALL", "true", "github_copilot"),
        ("COPILOT_GITHUB_TOKEN", "ghu_token123", "github_copilot"),
        ("REPL_ID", "repl-123", "replit"),
        ("AUGMENT_AGENT", "1", "augment"),
    ],
)
def test_detect_ai_agent_known_variables(monkeypatch, env_var, env_value, expected):
    monkeypatch.setenv(env_var, env_value)
    detected = agents.detect_ai_agent()
    assert detected == expected
    assert _VALID_TOKEN_RE.match(detected) is not None


@pytest.mark.parametrize(
    ("env_var", "env_value"),
    [
        ("AI_AGENT", ""),
        ("AI_AGENT", "   "),
        ("AI_AGENT", "!@#$%^&*()"),
        ("AI_AGENT", "0"),
        ("AI_AGENT", "false"),
        ("AI_AGENT", "FALSE"),
        ("AI_AGENT", "off"),
        ("ANTIGRAVITY_AGENT", "0"),
        ("ANTIGRAVITY_AGENT", "false"),
        ("CLAUDECODE", ""),
        ("CLAUDECODE", "   "),
        ("CLAUDECODE", "0"),
        ("CLAUDECODE", "false"),
        ("CURSOR_AGENT", "0"),
        ("CURSOR_AGENT", "false"),
        ("CURSOR_AGENT", "off"),
        ("CURSOR_AGENT", "no"),
        ("CURSOR_EXTENSION_HOST_ROLE", ""),
        ("CURSOR_EXTENSION_HOST_ROLE", "   "),
        ("CURSOR_EXTENSION_HOST_ROLE", "extension-host"),
        ("GEMINI_CLI", "0"),
        ("GEMINI_CLI", "false"),
        ("CODEX_CI", "0"),
        ("CODEX_CI", "false"),
        ("CLINE_ACTIVE", "false"),
        ("CLINE_ACTIVE", "0"),
        ("COPILOT_ALLOW_ALL", "false"),
        ("COPILOT_ALLOW_ALL", "0"),
    ],
)
def test_detect_ai_agent_ignores_empty_falsy_or_non_matching_values(
    monkeypatch, env_var, env_value
):
    monkeypatch.setenv(env_var, env_value)
    assert agents.detect_ai_agent() is None


def test_detect_ai_agent_falsy_higher_priority_falls_through(monkeypatch):
    monkeypatch.setenv("CURSOR_AGENT", "0")
    monkeypatch.setenv("GEMINI_CLI", "1")
    assert agents.detect_ai_agent() == "gemini_cli"


def test_detect_ai_agent_priority_order(monkeypatch):
    # AI_AGENT (priority 1) takes precedence over all specific agent vars
    monkeypatch.setenv("AI_AGENT", " custom-agent ")
    monkeypatch.setenv("ANTIGRAVITY_AGENT", "1")
    monkeypatch.setenv("CLAUDECODE", "1")
    assert agents.detect_ai_agent() == "custom-agent"

    # ANTIGRAVITY_AGENT (priority 2) takes precedence over CLAUDECODE (priority 3)
    monkeypatch.delenv("AI_AGENT")
    assert agents.detect_ai_agent() == "antigravity"

    # CLAUDECODE (priority 3) takes precedence over CURSOR_AGENT (priority 4)
    monkeypatch.delenv("ANTIGRAVITY_AGENT")
    monkeypatch.setenv("CURSOR_AGENT", "1")
    assert agents.detect_ai_agent() == "claude_code"

    # CURSOR_EXTENSION_HOST_ROLE (priority 5) takes precedence over GEMINI_CLI (priority 6)
    monkeypatch.delenv("CLAUDECODE")
    monkeypatch.delenv("CURSOR_AGENT")
    monkeypatch.setenv("CURSOR_EXTENSION_HOST_ROLE", "  agent-exec  ")
    monkeypatch.setenv("GEMINI_CLI", "1")
    assert agents.detect_ai_agent() == "cursor"

    # GEMINI_CLI (priority 6) takes precedence over CODEX_SANDBOX (priority 7)
    monkeypatch.setenv("CURSOR_EXTENSION_HOST_ROLE", "other-role")
    monkeypatch.setenv("CODEX_SANDBOX", "1")
    assert agents.detect_ai_agent() == "gemini_cli"

    # CODEX_SANDBOX (priority 7) takes precedence over CLINE_ACTIVE (priority 8)
    monkeypatch.delenv("GEMINI_CLI")
    monkeypatch.setenv("CLINE_ACTIVE", "1")
    assert agents.detect_ai_agent() == "codex_cli"


def test_detect_ai_agent_falls_through_when_ai_agent_sanitizes_empty(monkeypatch):
    monkeypatch.setenv("AI_AGENT", "!!!\r\n\t")
    monkeypatch.setenv("GEMINI_CLI", "1")
    assert agents.detect_ai_agent() == "gemini_cli"


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("valid_agent-123", "valid_agent-123"),
        ("my agent/1.0\r\nX-Injected: bad", "myagent10X-Injectedbad"),
        ("a" * 100, "a" * 64),
        ("!!!" + ("b" * 70), "b" * 64),
        ("", None),
        ("   \r\n\t/@!#$%   ", None),
    ],
)
def test_sanitize_agent_name(raw, expected):
    result = agents.sanitize_agent_name(raw)
    assert result == expected
    if result is not None:
        assert _VALID_TOKEN_RE.match(result) is not None


@pytest.mark.parametrize(
    ("opt_out_var", "opt_out_val"),
    [
        ("GOOGLE_CLOUD_DISABLE_METRICS", "true"),
        ("GOOGLE_CLOUD_DISABLE_METRICS", "TRUE"),
        ("GOOGLE_CLOUD_DISABLE_METRICS", "1"),
        ("GOOGLE_CLOUD_DISABLE_METRICS", "yes"),
        ("CLOUDSDK_CORE_DISABLE_USAGE_REPORTING", "true"),
        ("CLOUDSDK_CORE_DISABLE_USAGE_REPORTING", "True"),
        ("CLOUDSDK_CORE_DISABLE_USAGE_REPORTING", "1"),
    ],
)
def test_detect_ai_agent_respects_telemetry_opt_out(
    monkeypatch, opt_out_var, opt_out_val
):
    monkeypatch.setenv("CLAUDECODE", "1")
    monkeypatch.setenv("AI_AGENT", "my_agent")
    monkeypatch.setenv(opt_out_var, opt_out_val)
    assert agents.detect_ai_agent() is None


@pytest.mark.parametrize(
    ("opt_out_var", "opt_out_val"),
    [
        ("GOOGLE_CLOUD_DISABLE_METRICS", "false"),
        ("GOOGLE_CLOUD_DISABLE_METRICS", "0"),
        ("CLOUDSDK_CORE_DISABLE_USAGE_REPORTING", "false"),
        ("CLOUDSDK_CORE_DISABLE_USAGE_REPORTING", "0"),
    ],
)
def test_detect_ai_agent_enabled_when_opt_out_is_false(
    monkeypatch, opt_out_var, opt_out_val
):
    monkeypatch.setenv("CLAUDECODE", "1")
    monkeypatch.setenv(opt_out_var, opt_out_val)
    assert agents.detect_ai_agent() == "claude_code"
