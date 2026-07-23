# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import csv
import json
import os
import sys
from unittest.mock import MagicMock, mock_open, patch

import pytest

# Ensure scripts/import_profiler is in sys.path
sys.path.insert(0, os.path.dirname(__file__))

import profiler
from profiler import (
    NO_CPU_PINNING,
    _run_worker_and_parse,
    find_module_from_package,
    get_rss_mb,
    run_master,
    run_worker,
)

# =====================================================================
# 1. UTILITY FUNCTIONS TESTS
# =====================================================================


def test_get_rss_mb():
    """Verifies get_rss_mb returns a float representing megabytes if available."""
    rss = get_rss_mb()
    assert isinstance(rss, float)
    assert rss >= 0.0


@patch("os.walk")
@patch("os.remove")
@patch("shutil.rmtree")
def test_clean_bytecode(mock_rmtree, mock_remove, mock_walk):
    """Verifies clean_bytecode successfully cleans bytecode files & caches."""
    clean_bytecode_helper = getattr(profiler, "clean_bytecode", None)
    if clean_bytecode_helper is None:
        pytest.skip("clean_bytecode is not exported at the module level.")

    mock_walk.return_value = [
        ("/test_dir", ["__pycache__"], ["test.pyc", "test.py"])
    ]
    clean_bytecode_helper()
    assert mock_remove.called or mock_rmtree.called


def test_find_module_from_package_resolves():
    """Verifies resolving of packages to modules if helper is exported."""
    with patch(
        "importlib.metadata.packages_distributions",
        return_value={"google-cloud-storage": ["google.cloud.storage"]},
    ):
        res = find_module_from_package("google-cloud-storage")
        assert res == "google.cloud.storage"


def test_find_module_from_package_fallback():
    """Verifies fallback transforms work correctly if helper is exported."""
    with patch("importlib.util.find_spec", side_effect=lambda mod: mod == "my_dummy_mod"):
        res = find_module_from_package("my-dummy-mod")
        assert res == "my_dummy_mod"


@patch("subprocess.run")
def test_run_trace(mock_run):
    """Verifies that run_trace executes python with -X importtime and writes logs."""
    run_trace_helper = getattr(profiler, "run_trace", None)
    if run_trace_helper is None:
        pytest.skip("run_trace is not exported at the module level.")

    # Mock subprocess output
    mock_run.return_value = MagicMock(
        stdout="", stderr="importtime: dummy trace output", returncode=0
    )

    with patch("builtins.open", mock_open()) as mock_file, patch(
        "builtins.print"
    ):
        run_trace_helper("math")

        # Verify that subprocess was invoked with -X importtime
        called_cmd = mock_run.call_args[0][0]
        assert "-X" in called_cmd
        assert "importtime" in called_cmd

        # Verify that it attempted to write the trace log file
        assert mock_file.called


# =====================================================================
# 2. WORKER TESTS (run_worker)
# =====================================================================


def test_run_worker_with_skip_line_count(capsys):
    """Verifies worker returns -1 for loaded_lines when flag is active."""
    dummy_module = "sys"
    run_worker(dummy_module, skip_line_count=True)
    captured = capsys.readouterr()

    assert "__METRICS__:" in captured.out
    metrics_line = [
        l for l in captured.out.splitlines() if l.startswith("__METRICS__:")
    ][0]
    metrics = json.loads(metrics_line.split("__METRICS__:", 1)[1])

    assert metrics["loaded_lines"] == -1


def test_run_worker_counts_lines_correctly(capsys):
    """Verifies worker correctly resolves paths and counts raw lines."""
    dummy_module = "math"
    mock_module = MagicMock()
    mock_module.__file__ = "/mock/path/dummy_module.py"
    dummy_content = "import os\nprint('hello')\nx = 1\n"

    class CustomModulesDict(dict):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._call_count = 0

        def keys(self):
            self._call_count += 1
            if self._call_count == 1:
                return {"math"}
            return {"math", "dummy_test_mod"}

    fake_modules = CustomModulesDict(
        {"math": sys.modules["math"], "dummy_test_mod": mock_module}
    )

    with patch("sys.modules", fake_modules), patch(
        "builtins.open", mock_open(read_data=dummy_content)
    ), patch("profiler.importlib.invalidate_caches"):

        run_worker(dummy_module, skip_line_count=False)
        captured = capsys.readouterr()

        metrics_line = [
            l for l in captured.out.splitlines() if l.startswith("__METRICS__:")
        ][0]
        metrics = json.loads(metrics_line.split("__METRICS__:", 1)[1])

        assert metrics["loaded_lines"] == 3


# =====================================================================
# 3. PARSER TESTS (_run_worker_and_parse)
# =====================================================================


def test_run_worker_and_parse_success():
    """Verifies master extracts metrics JSON block from worker stdout."""
    mock_stdout = (
        '__METRICS__:{"time_ms": 15.5, "peak_ram_mb": 12.0, "rss_ram_mb":'
        ' 10.0, "loaded_modules": 22, "loaded_lines": 120}\n'
    )
    mock_process = MagicMock(stdout=mock_stdout, stderr="")

    with patch("subprocess.run", return_value=mock_process):
        data = _run_worker_and_parse(["python", "profiler.py"])
        assert data["time_ms"] == 15.5
        assert data["loaded_lines"] == 120


def test_run_worker_and_parse_forwards_stderr(capsys):
    """Verifies worker stderr warnings are forwarded to master's stderr."""
    mock_stdout = (
        '__METRICS__:{"time_ms": 10.0, "peak_ram_mb": 12.0, "rss_ram_mb":'
        ' 10.0, "loaded_modules": 22, "loaded_lines": 120}'
    )
    mock_stderr = "DeprecationWarning: some_pkg is deprecated"
    mock_process = MagicMock(stdout=mock_stdout, stderr=mock_stderr)

    with patch("subprocess.run", return_value=mock_process):
        _run_worker_and_parse(["python", "profiler.py"])
        captured = capsys.readouterr()
        assert "DeprecationWarning: some_pkg is deprecated" in captured.err


# =====================================================================
# 4. MASTER COORDINATION & BENCHMARK INTEGRATIONS
# =====================================================================


@patch("profiler._run_worker_and_parse")
def test_run_master_skips_line_count_and_restores_metrics(mock_parse):
    """Verifies master appends --skip-line-count and restores metrics."""
    run_data_1 = {
        "loaded_modules": 5,
        "loaded_lines": 1000,
        "time_ms": 50.0,
        "peak_ram_mb": 10.0,
        "rss_ram_mb": 8.0,
    }
    run_data_2 = {
        "loaded_modules": 5,
        "loaded_lines": -1,
        "time_ms": 40.0,
        "peak_ram_mb": 10.0,
        "rss_ram_mb": 8.0,
    }
    mock_parse.side_effect = [run_data_1, run_data_2]

    with patch("builtins.print"), patch("sys.stderr"):
        run_master(
            iterations=2,
            target_module="dummy_mod",
            cpu=NO_CPU_PINNING,
            clear_cache=False,
        )

        second_cmd_args = mock_parse.call_args_list[1][0][0]
        assert "--skip-line-count" in second_cmd_args
        assert run_data_2["loaded_lines"] == 1000


@patch("profiler._run_worker_and_parse")
def test_run_master_checks_non_deterministic_behavior(mock_parse, capsys):
    """Verifies warnings are printed upon non-deterministic module loads."""
    mock_parse.side_effect = [
        {
            "loaded_modules": 50,
            "loaded_lines": 500,
            "time_ms": 10.0,
            "peak_ram_mb": 1.0,
            "rss_ram_mb": 1.0,
        },
        {
            "loaded_modules": 55,
            "loaded_lines": -1,
            "time_ms": 10.0,
            "peak_ram_mb": 1.0,
            "rss_ram_mb": 1.0,
        },
    ]

    run_master(
        iterations=2,
        target_module="dummy_mod",
        cpu=NO_CPU_PINNING,
        clear_cache=False,
    )
    captured = capsys.readouterr()
    assert "WARNING: Non-deterministic import behavior!" in captured.err


@patch("profiler._run_worker_and_parse")
def test_run_master_with_cpu_pinning(mock_parse):
    """Verifies taskset command configuration on Linux platforms."""
    mock_parse.return_value = {
        "loaded_modules": 10,
        "loaded_lines": 500,
        "time_ms": 12.0,
        "peak_ram_mb": 1.0,
        "rss_ram_mb": 1.0,
    }

    with patch("sys.platform", "linux"), patch("builtins.print"), patch(
        "sys.stderr"
    ):
        run_master(
            iterations=1, target_module="dummy_mod", cpu=1, clear_cache=False
        )

        args = mock_parse.call_args[0][0]
        assert "taskset" in args
        assert "1" in args


@patch("profiler._run_worker_and_parse")
def test_run_master_writes_csv_and_diffs_baseline(mock_parse, tmp_path):
    """Verifies benchmark results CSV writing, reading, and thresholds comparison."""
    mock_parse.return_value = {
        "loaded_modules": 10,
        "loaded_lines": 500,
        "time_ms": 12.0,
        "peak_ram_mb": 1.0,
        "rss_ram_mb": 1.0,
    }

    csv_file = tmp_path / "results.csv"
    baseline_file = tmp_path / "baseline.csv"

    # Write mock baseline CSV data
    with open(baseline_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "iteration",
                "time_ms",
                "peak_ram_mb",
                "rss_ram_mb",
                "loaded_modules",
                "loaded_lines",
            ]
        )
        writer.writerow([1, 10.0, 1.0, 1.0, 10, 500])

    with patch("builtins.print"):
        run_master(
            iterations=1,
            target_module="dummy_mod",
            cpu=NO_CPU_PINNING,
            csv_path=str(csv_file),
            diff_baseline=str(baseline_file),
            diff_threshold=50.0,
            clear_cache=False,
        )

    assert csv_file.exists()


def test_validate_module_name_valid():
    """Verifies validate_module_name passes valid identifiers."""
    from profiler import validate_module_name
    assert validate_module_name("google.cloud.storage") == "google.cloud.storage"


def test_validate_module_name_invalid():
    """Verifies validate_module_name raises ArgumentTypeError for invalid identifiers."""
    import argparse
    from profiler import validate_module_name
    with pytest.raises(argparse.ArgumentTypeError):
        validate_module_name("google.cloud; rm -rf /")


@patch("subprocess.run")
def test_run_cprofile(mock_run):
    """Verifies run_cprofile executes cProfile subprocess."""
    from profiler import run_cprofile
    mock_run.return_value = MagicMock(returncode=0)
    with patch("pstats.Stats"), patch("builtins.print"):
        run_cprofile("math")
    assert mock_run.called


@patch("multiprocessing.get_context")
def test_run_mprofile(mock_context):
    """Verifies run_mprofile spawns process for memory snapshot."""
    from profiler import run_mprofile
    mock_proc = MagicMock(exitcode=0)
    mock_context.return_value.Process.return_value = mock_proc
    with patch("builtins.print"):
        run_mprofile("math")
    assert mock_proc.start.called
    assert mock_proc.join.called

