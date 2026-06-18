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
import tempfile
import subprocess
import shutil
import sys
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Tuple, Set, Any, Optional

# --- Paths Configuration ---
ROOT_DIR: Path = Path(__file__).parent.resolve()
TESTING_DIR: Path = ROOT_DIR / "gapic" / "templates" / "testing"
TEMPLATES_DIR: Path = ROOT_DIR / "gapic" / "templates"

# --- Constants ---
# TODO: We could add --exclude-newer back later if we can handle missing upload dates.


@dataclass(frozen=True)
class RuntimeConfig:
    """Configuration for a specific target runtime environment."""
    output_file: str
    display_label: str
    input_template: str
    bounds_type: str
    python_version: str
    prerelease: bool = False

@dataclass
class ResolvedRequirements:
    """The result of compiling and categorizing requirements for a runtime."""
    base_blocks: List[str] = field(default_factory=list)
    conditional_blocks: Optional[Dict[str, List[str]]] = None
    dynamic_data: Dict[str, Any] = field(default_factory=dict)

# --- Helper Functions: General ---

def get_pkg_name(block: str) -> str:
    """Extracts the package name from a requirement block.

    Args:
        block: A string containing a requirement (e.g., 'requests==2.20.0').

    Returns:
        The extracted package name (e.g., 'requests').
    """
    match = re.match(r"^([a-zA-Z0-9\-_]+(?:\[[a-zA-Z0-9\-_,]+\])?)", block)
    return match.group(1).lower() if match else ""

def parse_dynamic_packages() -> Dict[str, Dict[str, str]]:
    """Parses centrally managed package specifications out of _pypi_packages.j2.

    Returns:
        A dictionary mapping package names to their lower and upper bounds.
    """
    content: str = (TEMPLATES_DIR / "_pypi_packages.j2").read_text()
    matches = re.findall(
        r'"package_name":\s*"([^"]+)"[,\s]+"lower_bound":\s*"([^"]+)"[,\s]+"upper_bound":\s*"([^"]+)"',
        content
    )
    return {name: {"lower_bound": lb, "upper_bound": ub} for name, lb, ub in matches}

# --- Helper Functions: Template Parsing ---

def _parse_pin_line(line: str) -> Tuple[str, str]:
    """Splits a requirement line into package name and version constraint.

    Args:
        line: A single line from a requirements file.

    Returns:
        A tuple of (package_name, version_constraint).
    """
    match = re.split(r'(==|>=|<=|>|<)', line, maxsplit=1)
    if len(match) == 3:
        return match[0].strip(), match[1] + match[2].strip()
    return line.strip(), ""

def _process_inclusions(content: str, pins: Dict[str, Any]) -> None:
    """Recursively processes Jinja2 inclusions found in the template content.

    Args:
        content: The content of the template being processed.
        pins: The dictionary to populate with discovered pins.
    """
    for include in re.findall(r'{% include "testing/([^"]+)" %}', content):
        included = parse_requirements_template(TESTING_DIR / include)
        pins["common"].update(included["common"])
        pins["async_rest"]["true"].update(included["async_rest"]["true"])
        pins["async_rest"]["false"].update(included["async_rest"]["false"])

def _parse_conditional_block(lines: List[str], index: int, pins: Dict[str, Any]) -> int:
    """Parses a Jinja2 if/else/endif block for rest_async_io_enabled.

    Args:
        lines: All lines of the template.
        index: The current line index pointing to the start of the conditional.
        pins: The dictionary to populate with discovered pins.

    Returns:
        The updated line index after processing the block.
    """
    # Parse 'True' branch
    index += 1
    while index < len(lines) and not lines[index].strip().startswith("{% else %}"):
        line = lines[index].strip()
        if line and not line.startswith(("{%", "{#", "{{", "#")):
            pkg, spec = _parse_pin_line(line)
            pins["async_rest"]["true"][pkg] = spec
        index += 1
    
    # Parse 'False' branch
    index += 1
    while index < len(lines) and not lines[index].strip().startswith("{% endif %}"):
        line = lines[index].strip()
        if line and not line.startswith(("{%", "{#", "{{", "#")):
            pkg, spec = _parse_pin_line(line)
            pins["async_rest"]["false"][pkg] = spec
        index += 1
    
    return index

def _process_template_lines(lines: List[str], pins: Dict[str, Any]) -> None:
    """Iterates through template lines and populates the pins dictionary.

    Args:
        lines: All lines of the template.
        pins: The dictionary to populate with discovered pins.
    """
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line or line.startswith(("{#", "#")):
            i += 1
            continue
            
        if line.startswith("{% if rest_async_io_enabled %}"):
            i = _parse_conditional_block(lines, i, pins)
        elif not line.startswith(("{%", "{{")):
            pkg, spec = _parse_pin_line(line)
            pins["common"][pkg] = spec
        i += 1

def parse_requirements_template(template_path: Path) -> Dict[str, Any]:
    """Parses a Jinja2 requirements template into a structured dictionary of pins.

    Args:
        template_path: The path to the Jinja2 requirements template file.

    Returns:
        A dictionary containing 'common' pins and 'async_rest' pins (true/false branches).
    """
    pins: Dict[str, Any] = {"common": {}, "async_rest": {"true": {}, "false": {}}}
    if not template_path.exists():
        return pins
        
    content = template_path.read_text()
    _process_inclusions(content, pins)
    _process_template_lines(content.splitlines(), pins)
            
    return pins

# --- Helper Functions: Compilation ---

def _write_requirements_in(all_pins: Dict[str, str], in_file: Path) -> None:
    """Generates the requirements.in file content from pinned specifications.

    Args:
        all_pins: A dictionary of package names and their version constraints.
        in_file: The path where the requirements.in file will be written.
    """
    lines = []
    for pkg, spec in all_pins.items():
        if not spec:
            lines.append(pkg)
        elif any(op in spec for op in ("==", ">=", "<=", ">", "<")):
            lines.append(f"{pkg}{spec}")
        else:
            lines.append(f"{pkg}=={spec}")
    in_file.write_text("\n".join(lines) + "\n")

def run_pip_compile(all_pins: Dict[str, str], python_version: str, prerelease: bool) -> str:
    """Executes `uv pip compile` to generate a requirements.txt with hashes.

    Args:
        all_pins: A dictionary of package names and their version constraints.
        python_version: The Python version to compile for.
        prerelease: Whether to allow prerelease versions.

    Returns:
        The content of the compiled requirements.txt file.
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        in_file = tmp_path / "requirements.in"
        
        _write_requirements_in(all_pins, in_file)
        
        cmd = [
            "uv", "pip", "compile",
            "--python", python_version,
            "--generate-hashes",
            "--no-strip-extras",
            in_file.name
        ]
        if prerelease:
            cmd.append("--pre")
        
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True, cwd=tmp_path)
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error compiling requirements for Python {python_version}:\n{e.stderr}")
            raise

def parse_compiled_output(text: str, dynamic_names: Set[str]) -> Tuple[List[str], Dict[str, Any]]:
    """Deconstructs the uv output into distinct package blocks and dynamic metadata.

    Args:
        text: The content of the compiled requirements.txt file.
        dynamic_names: A set of package names that should be treated as dynamic metadata.

    Returns:
        A tuple containing a list of requirement blocks and a dictionary of dynamic data.
    """
    blocks: List[str] = []
    current_block: List[str] = []
    for line in text.splitlines():
        if not line.strip() or line.startswith(("#", "--")):
            if current_block:
                blocks.append("\n".join(current_block))
                current_block = []
            continue
        if not line.startswith(" ") and current_block:
            blocks.append("\n".join(current_block))
            current_block = []
        current_block.append(line)
        
    if current_block:
        blocks.append("\n".join(current_block))
        
    base_blocks: List[str] = []
    dynamic_data: Dict[str, Any] = {}
    for block in blocks:
        match = re.match(r"^([a-zA-Z0-9\-_]+(?:\[[a-zA-Z0-9\-_,]+\])?)==([^\s\\]+)", block)
        if not match:
            base_blocks.append(block)
            continue
        
        pkg_name = match.group(1).lower()
        version = match.group(2)
        
        if pkg_name in [n.lower() for n in dynamic_names]:
            dynamic_data[pkg_name] = {
                "version": version,
                "hashes": re.findall(r"--hash=sha256:([a-f0-9]{64})", block)
            }
        else:
            base_blocks.append(block)
            
    return base_blocks, dynamic_data

def compile_and_parse(pins: Dict[str, str], config: RuntimeConfig, dynamic_names: Set[str]) -> Tuple[List[str], Dict[str, Any]]:
    """Helper to run pip compile and parse the results in one go.

    Args:
        pins: A dictionary of package names and their version constraints.
        config: The runtime configuration.
        dynamic_names: A set of package names that should be treated as dynamic metadata.

    Returns:
        A tuple containing a list of requirement blocks and a dictionary of dynamic data.
    """
    output = run_pip_compile(pins, config.python_version, config.prerelease)
    return parse_compiled_output(output, dynamic_names)

# --- Resolution Logic ---

def _compare_and_categorize_blocks(blocks_true: List[str], blocks_false: List[str]) -> Tuple[List[str], Dict[str, List[str]]]:
    """Compares requirement blocks from two branches and categorizes them as base or conditional.

    Args:
        blocks_true: Requirement blocks from the branch where rest_async_io_enabled is true.
        blocks_false: Requirement blocks from the branch where rest_async_io_enabled is false.

    Returns:
        A tuple containing base blocks (present in both) and a dictionary of conditional blocks.
    """
    pkgs_true = {get_pkg_name(b): b for b in blocks_true}
    pkgs_false = {get_pkg_name(b): b for b in blocks_false}
    
    base_blocks: List[str] = []
    conditional: Dict[str, List[str]] = {"async_true": [], "async_false": []}
    
    # Process packages present in both branches
    for pkg_name in set(pkgs_true.keys()) & set(pkgs_false.keys()):
        if pkgs_true[pkg_name] == pkgs_false[pkg_name]:
            base_blocks.append(pkgs_true[pkg_name])
        else:
            conditional["async_true"].append(pkgs_true[pkg_name])
            conditional["async_false"].append(pkgs_false[pkg_name])
    
    # Process packages unique to one branch
    for pkg_name in set(pkgs_true.keys()) - set(pkgs_false.keys()):
        conditional["async_true"].append(pkgs_true[pkg_name])
    for pkg_name in set(pkgs_false.keys()) - set(pkgs_true.keys()):
        conditional["async_false"].append(pkgs_false[pkg_name])
        
    return base_blocks, conditional

def _resolve_conditional_requirements(config: RuntimeConfig, raw_pins: Dict[str, Any], dynamic_names: Set[str]) -> ResolvedRequirements:
    """Handles requirements that differ based on rest_async_io_enabled.

    Args:
        config: The runtime configuration.
        raw_pins: The raw pins parsed from the template.
        dynamic_names: A set of package names that should be treated as dynamic metadata.

    Returns:
        A ResolvedRequirements object containing categorized blocks.
    """
    # 1. Compile for 'True'
    pins_true = {**raw_pins["common"], **raw_pins["async_rest"]["true"]}
    for pkg in dynamic_names: pins_true.setdefault(pkg, "")
    blocks_true, dyn_true = compile_and_parse(pins_true, config, dynamic_names)
    
    # 2. Compile for 'False'
    pins_false = {**raw_pins["common"], **raw_pins["async_rest"]["false"]}
    for pkg in dynamic_names: pins_false.setdefault(pkg, "")
    blocks_false, dyn_false = compile_and_parse(pins_false, config, dynamic_names)
    
    # 3. Categorize results
    base, conditional = _compare_and_categorize_blocks(blocks_true, blocks_false)
        
    return ResolvedRequirements(
        base_blocks=base,
        conditional_blocks=conditional,
        dynamic_data={**dyn_true, **dyn_false}
    )

def resolve_requirements(config: RuntimeConfig, dynamic_packages: Dict[str, Dict[str, str]]) -> ResolvedRequirements:
    """Parses input pins and performs compilation, handling conditional branches if necessary.

    Args:
        config: The runtime configuration.
        dynamic_packages: A dictionary of centrally managed package specifications.

    Returns:
        A ResolvedRequirements object.
    """
    raw_pins = parse_requirements_template(TESTING_DIR / config.input_template)
    dynamic_names = set(dynamic_packages.keys())
    
    # Check if we have conditional logic
    if raw_pins.get("async_rest", {}).get("true") or raw_pins.get("async_rest", {}).get("false"):
        return _resolve_conditional_requirements(config, raw_pins, dynamic_names)
    
    # Standard flow
    pins = raw_pins["common"].copy()
    if config.bounds_type == "lower_bound":
        pins.update({pkg: f"=={info['lower_bound']}" for pkg, info in dynamic_packages.items()})
    elif config.bounds_type == "latest":
        pins.update({pkg: f"=={int(info['upper_bound'].split('.')[0]) - 1}.*" for pkg, info in dynamic_packages.items()})
    else:
        for pkg in dynamic_names: pins.setdefault(pkg, "")
            
    base_blocks, dynamic_data = compile_and_parse(pins, config, dynamic_names)
    return ResolvedRequirements(base_blocks=base_blocks, dynamic_data=dynamic_data)

# --- Generation Logic ---

def format_dynamic_metadata(dynamic_data: Dict[str, Any]) -> str:
    """Formats the dynamic package data as a Jinja2 metadata dictionary.

    Args:
        dynamic_data: A dictionary of dynamic package metadata.

    Returns:
        A string containing the formatted Jinja2 metadata.
    """
    lines = ["{% set pypi_package_data = {"]
    pkg_entries = []
    for pkg_name, data in sorted(dynamic_data.items()):
        entry = [
            f'    "{pkg_name}": {{',
            f'        "version": "{data["version"]}",',
            '        "hashes": ['
        ]
        hash_lines = [f'            "{h}"' for h in data["hashes"]]
        entry.append(",\n".join(hash_lines))
        entry.extend(['        ]', '    }'])
        pkg_entries.append("\n".join(entry))
    lines.append(",\n".join(pkg_entries))
    lines.append("} %}")
    return "\n".join(lines)

def _generate_template_header(config: RuntimeConfig) -> List[str]:
    """Generates the file header for the autogenerated template.

    Args:
        config: The runtime configuration.

    Returns:
        A list of header lines.
    """
    return [
        "#",
        f"# This file is autogenerated by uv with {config.display_label}.",
        "{# To re-generate, run: nox -s update_hashes #}",
        "#",
        "{% from '_pypi_packages.j2' import pypi_packages %}"
    ]

def _generate_conditional_section(conditional_blocks: Dict[str, List[str]], written_packages: Set[str]) -> List[str]:
    """Generates the Jinja2 if/else section for branch-specific requirements.

    Args:
        conditional_blocks: A dictionary of branch-specific requirement blocks.
        written_packages: A set of package names already written to the template.

    Returns:
        A list of Jinja2 template lines.
    """
    lines = [
        "{% set rest_async_io_enabled = api.all_library_settings[api.naming.proto_package].python_settings.experimental_features.rest_async_io_enabled %}",
        "{% if rest_async_io_enabled %}"
    ]
    for block in conditional_blocks["async_true"]:
        lines.extend([block, ""])
        written_packages.add(get_pkg_name(block))
    lines.append("{% else %}")
    for block in conditional_blocks["async_false"]:
        lines.extend([block, ""])
        written_packages.add(get_pkg_name(block))
    lines.append("{% endif %}")
    return lines

def generate_output_content(config: RuntimeConfig, resolved: ResolvedRequirements) -> str:
    """Constructs the final autogenerated Jinja2 template content.

    Args:
        config: The runtime configuration.
        resolved: The resolved requirements.

    Returns:
        The complete content of the autogenerated template.
    """
    lines = _generate_template_header(config)
    written_packages: Set[str] = set()
    
    if resolved.conditional_blocks:
        lines.extend(_generate_conditional_section(resolved.conditional_blocks, written_packages))

    for block in resolved.base_blocks:
        name = get_pkg_name(block)
        if name not in written_packages:
            lines.extend([block, ""])
            written_packages.add(name)
            
    lines.append(format_dynamic_metadata(resolved.dynamic_data))
    lines.append(LOOP_TEMPLATE)
    
    return "\n".join(lines) + "\n"

LOOP_TEMPLATE = """{% for package_tuple, package_info in pypi_packages.items() %}
{% if api.naming.warehouse_package_name != package_info.package_name %}
{% if api.requires_package(package_tuple) %}
{{ package_info.package_name }}=={{ pypi_package_data[package_info.package_name].version }} \\
{% for h in pypi_package_data[package_info.package_name].hashes %}
    --hash=sha256:{{ h }}{% if not loop.last %} \\{% endif %}
{% endfor %}

{% endif %}
{% endif %}
{% endfor %}"""

# --- Orchestration ---

def update_runtime(config: RuntimeConfig, dynamic_packages: Dict[str, Dict[str, str]]) -> None:
    """Orchestrates the resolution and generation process for a single runtime configuration.

    Args:
        config: The runtime configuration.
        dynamic_packages: A dictionary of centrally managed package specifications.
    """
    resolved = resolve_requirements(config, dynamic_packages)
    content = generate_output_content(config, resolved)
    (TESTING_DIR / config.output_file).write_text(content)

def update_root_requirements(python_version: str) -> None:
    """Updates the root requirements-<python_version>.txt file.

    If python_version is '3.10', also updates requirements.txt.
    """
    in_file = ROOT_DIR / "requirements.in"
    out_file = ROOT_DIR / f"requirements-{python_version}.txt"
    display_label = f"Python {python_version}"

    print(f"Updating root requirements for {display_label}...")

    cmd = [
        "uv", "pip", "compile",
        "--python", python_version,
        "--generate-hashes",
        "--no-strip-extras",
        in_file.name
    ]

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, cwd=ROOT_DIR)
        content = result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error compiling root requirements for {display_label}:\n{e.stderr}")
        raise

    out_file.write_text(content)

    if python_version == "3.10":
        print(f"Updating root requirements.txt (syncing with {out_file.name})...")
        shutil.copy(out_file, ROOT_DIR / "requirements.txt")

def update(python_version: str, prerelease: bool = False) -> None:
    """Updates requirements hashes for a given Python version.

    Args:
        python_version: The Python version to update (e.g., '3.10').
        prerelease: Whether to update the prerelease configuration.
    """
    dynamic_packages = parse_dynamic_packages()
    configs = [
        RuntimeConfig("requirements-3.10.txt.j2", "Python 3.10", "requirements-3.10.in.j2", "lower_bound", "3.10"),
        RuntimeConfig("requirements-3.11.txt.j2", "Python 3.11", "requirements-default.in.j2", "default", "3.11"),
        RuntimeConfig("requirements-3.12.txt.j2", "Python 3.12", "requirements-default.in.j2", "default", "3.12"),
        RuntimeConfig("requirements-3.13.txt.j2", "Python 3.13", "requirements-latest.in.j2", "latest", "3.13"),
        RuntimeConfig("requirements-3.14.txt.j2", "Python 3.14", "requirements-latest.in.j2", "latest", "3.14"),
        RuntimeConfig("requirements-3.15.txt.j2", "Python 3.15", "requirements-latest.in.j2", "latest", "3.15"),
        RuntimeConfig("requirements-prerelease.txt.j2", "Python 3.15 (Prerelease)", "requirements-default.in.j2", "default", "3.15", True),
    ]

    target_configs = [
        cfg for cfg in configs
        if cfg.python_version == python_version and cfg.prerelease == prerelease
    ]

    if not target_configs:
        raise ValueError(f"No configuration found for Python version {python_version} (prerelease={prerelease})")

    for cfg in target_configs:
        print(f"Updating hashes for {cfg.display_label}...")
        update_runtime(cfg, dynamic_packages)

    if not prerelease:
        update_root_requirements(python_version)
