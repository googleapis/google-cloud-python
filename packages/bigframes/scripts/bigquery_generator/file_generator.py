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

import pathlib
import subprocess
import sys

from . import constants
from . import data_models
from . import template_renderer


def _ensure_init_py(directory: pathlib.Path, limit_dir: pathlib.Path):
    """Ensures __init__.py exists in the directory and its parents up to limit_dir."""
    curr = directory
    while curr != limit_dir and curr != curr.parent:
        init_file = curr / "__init__.py"
        if not init_file.exists():
            print(f"  Creating {init_file}")
            content = constants.TEMPLATES["license"].render()
            with open(init_file, "w", encoding="utf-8") as f:
                f.write(content)
        curr = curr.parent


def _write_file(content: str, output_file: pathlib.Path, limit_dir: pathlib.Path):
    output_file.parent.mkdir(parents=True, exist_ok=True)
    _ensure_init_py(output_file.parent, limit_dir)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Generated {output_file}")


def _run_ruff():
    targets = [
        constants.OUTPUT_DIR,
        constants.TEST_OUTPUT_DIR,
        constants.CODE_ROOT / "extensions",
    ]

    subprocess.run(
        [sys.executable, "-m", "ruff"] + constants.RUFF_CHECK_ARGS + targets,
        check=True,
    )

    subprocess.run(
        [sys.executable, "-m", "ruff"] + constants.RUFF_FORMAT_ARGS + targets,
        check=True,
    )


def _generate_op_defs(bq_module: data_models.BQModule):
    content = template_renderer.render_operation(bq_module)
    if not content:
        return

    output_file = constants.OUTPUT_DIR.joinpath(bq_module.module_path).with_suffix(
        ".py"
    )

    _write_file(content, output_file, constants.OUTPUT_DIR.parent)


def _generate_tests(bq_module: data_models.BQModule):
    content = template_renderer.render_tests(bq_module)
    if not content:
        return

    output_file = constants.TEST_OUTPUT_DIR.joinpath(
        bq_module.module_path.with_name(f"test_{bq_module.module_path.name}")
    ).with_suffix(".py")

    _write_file(content, output_file, constants.TEST_OUTPUT_DIR.parent)


def _generate_accesor(bq_modules: list[data_models.BQModule]):
    (core_content, pd_content, bf_content) = template_renderer.render_accessor(
        bq_modules
    )

    core_output_file = (
        constants.CODE_ROOT / "extensions" / "core" / "series_accessor.py"
    )
    _write_file(core_content, core_output_file, constants.CODE_ROOT)

    pd_output_file = (
        constants.CODE_ROOT / "extensions" / "pandas" / "series_accessor.py"
    )
    _write_file(pd_content, pd_output_file, constants.CODE_ROOT)

    bf_output_file = (
        constants.CODE_ROOT / "extensions" / "bigframes" / "series_accessor.py"
    )
    _write_file(bf_content, bf_output_file, constants.CODE_ROOT)


def generate(bq_modules: list[data_models.BQModule]):

    for bq_module in bq_modules:
        _generate_op_defs(bq_module)
        _generate_tests(bq_module)

    _generate_accesor(bq_modules)

    # Ruff format
    _run_ruff()
