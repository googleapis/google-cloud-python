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
import glob
import json
from pathlib import Path
import os
import re
import shutil
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
    The name of the package to build.
    """,
)
def build_library(repo_root: str, library_id: str):
    """This is unused at the moment"""
    pass

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
                    "autogen-snippets",
                    "default-proto-package",
                    "documentation-name",
                    "documentation-uri",
                    "gapic-version",
                    "python-gapic-namespace",
                    "python-gapic-name",
                    "reference-doc-includes",
                    "release-level",
                    "rest-numeric-enums",
                    "retry-config",
                    "service-yaml",
                    "transport",
                    "warehouse-package-name",
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
                            f" --python_gapic_opt=metadata,"
                        )
                        for generator_option in generator_options:
                            generator_command += generator_option
                    print(generator_command)
                    subprocess.run([generator_command], cwd=api_root, shell=True)
                    subprocess.run(
                        f"isort -q --fss docs google tests noxfile.py setup.py",
                        cwd=tmp_dir,
                        shell=True,
                    )
                    subprocess.run(
                        f"black -q docs google tests noxfile.py setup.py",
                        cwd=tmp_dir,
                        shell=True,
                    )
                    subprocess.run(f"mkdir -p packages/{library_id}", cwd=output, shell=True)
                    subprocess.run(
                        f"cp -r {tmp_dir}/. packages/{library_id}", cwd=output, shell=True
                    )
    os.chdir(output)
    apply_client_specific_post_processing(
        f"/generator-input/client-post-processing", library_id
    )
    create_symlink_in_docs_dir(f"{output}/packages/{library_id}", "README.rst")


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

    files_to_preserve = [
        # TODO: remove all owlbot configs in a separate PR
        ".OwlBot.yaml",
        # TODO: auto-generate .repo-metadata.json from service config (apis.json to supplement missing information)
        ".repo-metadata.json",
        "CHANGELOG.md",
        "tests/system/__init__.py",
    ]
    # TODO: remove all *.tar.gz files in a separate PR
    files_to_preserve.extend([os.path.basename(tar_path) for tar_path in glob.glob(f"{repo_root}/packages/{library_id}/*.tar.gz")])

    with tempfile.TemporaryDirectory() as tmp_dir:
        for file in files_to_preserve:
            if Path(f"{repo_root}/packages/{library_id}/{file}").exists():
                shutil.copy(f"{repo_root}/packages/{library_id}/{file}", f"{tmp_dir}/{file}")
        shutil.rmtree(f"{repo_root}/packages/{library_id}")

        os.makedirs(f"{repo_root}/packages/{library_id}/docs")
        os.makedirs(f"{repo_root}/packages/{library_id}/tests/system")

        for file in files_to_preserve:
            if Path(f"{tmp_dir}/{file}").exists():
                shutil.copy(f"{tmp_dir}/{file}", f"{repo_root}/packages/{library_id}/{file}")
        create_symlink_in_docs_dir(f"{repo_root}/packages/{library_id}", "CHANGELOG.md")

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
                        if f"{package_name}/" in client_library_path:
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

# Copied from synthtool
# https://github.com/googleapis/synthtool/blob/906b162627b29cf10621074a5055bec0e30b5307/synthtool/languages/python_mono_repo.py#L69C1-L92C1
def create_symlink_in_docs_dir(package_dir: str, filename: str):
    """Creates a symlink in the docs directory for <filename> pointing to ../<filename>
        using the package_dir specified as the base directory.

    Args:
        package_dir (str): path to the directory for a specific package. For example
            'packages/google-cloud-video-transcoder'
        working_dir (str): the absolute path to the directory where the link should be created
        filename (str): the name of the file to link
    """

    current_dir = os.getcwd()

    os.chdir(f"{package_dir}/docs")

    relative_path_to_docs_file = Path(filename)
    relative_path_to_file = Path(f"../{filename}")

    if relative_path_to_file.exists():
        if not relative_path_to_docs_file.exists():
            Path(relative_path_to_docs_file).symlink_to(relative_path_to_file)

    os.chdir(current_dir)


if __name__ == "__main__":
    main()
