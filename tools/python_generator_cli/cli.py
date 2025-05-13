# Copyright 2025 Google LLC
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
#

import click
import json
from pathlib import Path
import os
import re
import subprocess
import sys
import tempfile
import yaml

from typing import Iterable, Optional, Union

PathOrStr = Union[str, Path]
ListOfPathsOrStrs = Iterable[Union[str, Path]]

@click.group()
def main():
    pass


@main.command()
@click.option(
    "--api-path",
    required=True,
    type=str,
    help="""
    Path within the API root (e.g. googleapis) to the API to 
    generate/build/configure etc. For example, for a major-versioned 
    API directory: google/cloud/functions/v2.
    """,
)
@click.option(
    "--output",
    required=True,
    type=str,
    help="""
    The location where generated files will be created.
    """,
)
@click.option(
    "--api-root",
    type=str,
    help="""
    The path to which the api definition (proto and service yaml) and its
    dependencies reside.
    """,
)
def generate_raw(api_path: str, output: str, api_root: str):
    """Generates a python client library using the given arguments."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        generator_command = f"protoc {api_path}/*.proto --python_gapic_out={tmp_dir}"
        subprocess.run([generator_command], cwd=api_root, shell=True)
        subprocess.run(
            f"isort --fss docs google tests noxfile.py setup.py",
            cwd=tmp_dir,
            shell=True,
        )
        subprocess.run(
            f"black docs google tests noxfile.py setup.py", cwd=tmp_dir, shell=True
        )
        subprocess.run(f"cp -r {tmp_dir}/. {output}", cwd=output, shell=True)


@main.command()
@click.option(
    "--api-root",
    required=True,
    type=str,
    help="""
    Path to a clone of `googleapis/googleapis`.
    """,
)
@click.option(
    "--generator-input",
    required=True,
    type=str,
    help="""
    Path within the directory which contains files necessary for client
    library generation.
    """,
)
@click.option(
    "--output",
    required=True,
    type=str,
    help="""
    The location where generated files will be created.
    """,
)
@click.option(
    "--library-id",
    required=True,
    type=str,
    help="""
    The name of the library to generate.
    """,
)
def generate_library(api_root: str, generator_input: str, output: str, library_id: str):
    """Generates a python client library using the given arguments."""

    with open(
        f"{generator_input}/pipeline-state.json", "r"
    ) as pipeline_state_json_file:
        pipeline_state = json.load(pipeline_state_json_file)
        with open(f"{generator_input}/apis.json", "r") as apis_json_file:
            all_apis_config = json.load(apis_json_file)
            library_specific_config = next(
                item for item in pipeline_state["libraries"] if item["id"] == library_id
            )
            for api_path in library_specific_config["apiPaths"]:
                api_specific_config = next(
                    item
                    for item in all_apis_config["apis"]
                    if item["apiPath"] == api_path
                )

                config_keys = [
                    "transport",
                    "python-gapic-namespace",
                    "python-gapic-name",
                    "warehouse-package-name",
                    "service-yaml",
                    "retry-config",
                    "release-level",
                    "default-proto-package",
                    "reference-doc-includes",
                    "documentation-uri",
                ]
                generator_options = []
                for key in config_keys:
                    config_value = api_specific_config.get(key, None)
                    if config_value is not None:
                        if key == "service-yaml" or key == "retry-config":
                            generator_options.append(
                                f"{key}={api_path}/{config_value},"
                            )
                        else:
                            generator_options.append(f"{key}={config_value},")

                with tempfile.TemporaryDirectory() as tmp_dir:
                    generator_command = (
                        f"protoc {api_path}/*.proto --python_gapic_out={tmp_dir}"
                    )
                    if len(generator_options):
                        generator_command += (
                            f" --python_gapic_opt=rest-numeric-enums=True,metadata,"
                        )
                        for generator_option in generator_options:
                            generator_command += generator_option
                    print(generator_command)
                    subprocess.run([generator_command], cwd=api_root, shell=True)
                    subprocess.run(
                        f"isort --fss docs google tests noxfile.py setup.py",
                        cwd=tmp_dir,
                        shell=True,
                    )
                    subprocess.run(
                        f"black docs google tests noxfile.py setup.py",
                        cwd=tmp_dir,
                        shell=True,
                    )
                    subprocess.run(
                        f"cp -r {tmp_dir}/. {output}", cwd=output, shell=True
                    )
                    # TODO: Move to scripts to generator input directory
                    apply_client_specific_post_processing(
                        f"{output}/scripts/client-post-processing", library_id
                    )


@main.command()
@click.option(
    "--repo-root",
    required=True,
    type=str,
    help="""
    Path to the root of the clone of the git repository. 
    """,
)
@click.option(
    "--library-id",
    required=True,
    type=str,
    help="""
    The name of the package to clean.
    """,
)
def clean(repo_root: str, library_id: str):
    """Deletes all automatically generated files for a given library-id."""

    subprocess.run(f"rm -rf {repo_root}/packages/{library_id}")
    subprocess.run(f"mkdir {repo_root}/packages/{library_id}")
    subprocess.run(f"git checkout {repo_root}/packages/{library_id}/tests/system")

# Copied from synthtool
# https://github.com/googleapis/synthtool/blob/6318601ed44bb99ec965bae0d46b54eba42aeb24/synthtool/languages/python_mono_repo.py#L147-L210
def apply_client_specific_post_processing(
    post_processing_dir: str, package_name: str
) -> None:
    """Applies client-specific post processing which exists in the Path `post_processing_dir`.
    This function is only called from `owlbot_main` when there is an `owl-bot-staging` folder
    which contains generated client library code. Re-running the script more than once is
    expected to be idempotent. The client-specific post processing YAML is in the following format:
    ```
        description: Verbose description about the need for the workaround.
        url: URL of the issue in gapic-generator-python tracking eventual removal of the workaround
        replacements:
          - replacement:
            paths: [<List of files where the replacement should occur relative to the monorepo root directory>]
            before: "The string to search for in the specified paths"
            after:  "The string to replace in the the specified paths",
            count: <integer indicating number of replacements that should have occurred across all files after the script is run>
    ```

    Note: The `paths` key above must only include paths for the same package so that the number of replacements
    made in a given package can be verified.

    Args:
        post_processing_dir (str): Path to the directory which contains YAML files which will
            be used to apply client-specific post processing, e.g. 'packages/<package_name>/scripts/client-post-processing'
            relative to the monorepo root directory.
        package_name (str): The name of the package where client specific post processing will be applied.
    """

    if Path(post_processing_dir).exists():
        for post_processing_path in Path(post_processing_dir).iterdir():
            with open(post_processing_path, "r") as post_processing_path_file:
                post_processing_json = yaml.safe_load(post_processing_path_file)
                all_replacements = post_processing_json["replacements"]
                # For each workaround related to the specified issue
                for replacement in all_replacements:
                    replacement_count = 0
                    number_of_paths_with_replacements = 0
                    # For each file that needs the workaround applied
                    for client_library_path in replacement["paths"]:
                        if package_name in client_library_path:
                            number_of_paths_with_replacements += 1
                            replacement_count += replace(
                                client_library_path,
                                replacement["before"],
                                replacement["after"],
                            )
                            # Ensure idempotency by checking that subsequent calls won't
                            # trigger additional replacements within the same path
                            assert (
                                replace(
                                    client_library_path,
                                    replacement["before"],
                                    replacement["after"],
                                )
                                == 0
                            )
                    if number_of_paths_with_replacements:
                        # Ensure that the numner of paths where a replacement occurred matches the number of paths.
                        assert number_of_paths_with_replacements == len(
                            replacement["paths"]
                        )
                        # Ensure that the total number of replacements matches the value specified in `count`
                        # for all paths in `replacement["paths"]`
                        assert replacement_count == replacement["count"]


# Copied from synthtool
# https://github.com/googleapis/synthtool/blob/master/synthtool/transforms.py#L70-L73
def _filter_files(paths: Iterable[Path]) -> Iterable[Path]:
    """Returns only the paths that are files (no directories)."""

    return (path for path in paths if path.is_file() and os.access(path, os.W_OK))

# Copied from synthtool
# https://github.com/googleapis/synthtool/blob/6318601ed44bb99ec965bae0d46b54eba42aeb24/synthtool/transforms.py#L268-L294
def replace(
    sources: ListOfPathsOrStrs, before: str, after: str, flags: int = re.MULTILINE
) -> int:
    """Replaces occurrences of before with after in all the given sources.

    Returns:
      The number of times the text was found and replaced across all files.
    """
    expr = re.compile(before, flags=flags or 0)
    paths = _filter_files(_expand_paths(sources, "."))
    count_replaced = 0
    for path in paths:
        replaced = replace_in_file(path, expr, after)
        count_replaced += replaced
    return count_replaced

# Copied from synthtool
# https://github.com/googleapis/synthtool/blob/6318601ed44bb99ec965bae0d46b54eba42aeb24/synthtool/transforms.py#L34C1-L67C14
def _expand_paths(
    paths: ListOfPathsOrStrs, root: Optional[PathOrStr] = None
) -> Iterable[Path]:
    """Given a list of globs/paths, expands them into a flat sequence,
    expanding globs as necessary."""
    if paths is None:
        return []

    if isinstance(paths, (str, Path)):
        paths = [paths]

    if root is None:
        root = Path(".")

    # ensure root is a path
    root = Path(root)

    # record name of synth script so we don't try to do transforms on it
    synth_script_name = sys.argv[0]

    for path in paths:
        if isinstance(path, Path):
            if path.is_absolute():
                anchor = Path(path.anchor)
                remainder = str(path.relative_to(path.anchor))
                yield from anchor.glob(remainder)
            else:
                yield from root.glob(str(path))
        else:
            yield from (
                p
                for p in root.glob(path)
                if p.absolute() != Path(synth_script_name).absolute()
            )

# Copied from synthtool
# https://github.com/googleapis/synthtool/blob/6318601ed44bb99ec965bae0d46b54eba42aeb24/synthtool/transforms.py#L243-L265
def replace_in_file(path, expr, replacement):
    try:
        with path.open("r+") as fh:
            return _replace_in_file_handle(fh, expr, replacement)
    except UnicodeDecodeError:
        pass  # It's a binary file.  Try again with a binary regular expression.
    flags = expr.flags & ~re.UNICODE
    expr = re.compile(expr.pattern.encode(), flags)
    with path.open("rb+") as fh:
        return _replace_in_file_handle(fh, expr, replacement.encode())


def _replace_in_file_handle(fh, expr, replacement):
    content = fh.read()
    content, count = expr.subn(replacement, content)

    # Don't bother writing the file if we didn't change
    # anything.
    if count:
        fh.seek(0)
        fh.write(content)
        fh.truncate()
    return count

if __name__ == "__main__":
    main()
