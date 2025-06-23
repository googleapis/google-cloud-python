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
import shlex
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

    subprocess.run(
        f"rm -rf {output}/owl-bot-staging", cwd=output, shell=True
    )
    with open(
        f"{generator_input}/pipeline-state.json", "r"
    ) as pipeline_state_json_file:
        pipeline_state = json.load(pipeline_state_json_file)
        with open(f"{generator_input}/apis.json", "r") as apis_json_file:
            library_specific_config = next(
                item for item in pipeline_state["libraries"] if item["id"] == library_id
            )
            for api_path in library_specific_config["apiPaths"]:
                api_version = api_path.split("/")[-1]
                with tempfile.TemporaryDirectory() as tmp_dir:
                    bazel_command = f"gbazelisk query 'filter(\"-py$\", kind(\"rule\", //{api_path}/...:*))'"                    
                    
                    bazel_rule = subprocess.check_output(bazel_command, cwd=api_root, shell=True).decode("utf-8").strip()
                    bazel_command = f"gbazelisk build --nofetch  {bazel_rule}"
                    
                    subprocess.run([bazel_command], cwd=api_root, shell=True)
                    bazel_command = "gbazelisk info bazel-bin"
                    bazel_bin = subprocess.check_output(bazel_command, cwd=api_root, shell=True).decode("utf-8").strip()
                    # subprocess.run(
                    #     f"cp -r {bazel_bin}/. {tmp_dir}", cwd=tmp_dir, shell=True
                    # )
                    bazel_rule_split = bazel_rule.split(":")
                    parent_dir = bazel_rule_split[0].replace("//", "")
                    print(parent_dir)
                    subprocess.run(
                        f"ls {parent_dir}", cwd=bazel_bin, shell=True
                    )
                    tar_gz_file = bazel_rule_split[1] + ".tar.gz"
                    print(tar_gz_file)

                    # For some APIs like `google-cloud-workflows`, we will be adding to the same directory, so don't fail if the directory exists
                    os.makedirs(f"{output}/owl-bot-staging/{library_id}/{api_version}", exist_ok=True)
                    
                    subprocess.run(
                        f"tar -xvf {bazel_bin}/{parent_dir}/{tar_gz_file} --strip-components=1", cwd=f"{output}/owl-bot-staging/{library_id}/{api_version}", shell=True
                    )

                    subprocess.run(
                        f"rm -rf *.tar.gz", cwd=tmp_dir, shell=True
                    )

    os.chdir(f"{generator_input}/client-post-processing")
    # Add post-processing files
    for post_processing_file in glob.glob(f"*.yaml"):
        with open(post_processing_file, "r") as post_processing_path_file:
            if f"packages/{library_id}/" in post_processing_path_file.read():
                os.makedirs(f"{output}/packages/{library_id}/scripts/client-post-processing", exist_ok=True)       
                create_symlink_in_dir(f"{generator_input}/client-post-processing", f"{output}/packages/{library_id}/scripts/client-post-processing", post_processing_file, 4)

    os.chdir(output)
    subprocess.run("python3 -m synthtool.languages.python_mono_repo", cwd=output, shell=True)
    # apply_client_specific_post_processing(
    #     f"/generator-input/client-post-processing", library_id
    # )
    # os.chdir(f"{output}/packages/{library_id}")
    # create_symlink_in_dir(".", f"{output}/packages/{library_id}/docs", "README.rst", 1)


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
        "tests/system/smoke_test.py",
    ]
    # TODO: remove all *.tar.gz files in a separate PR
    files_to_preserve.extend([os.path.basename(tar_path) for tar_path in glob.glob(f"{repo_root}/packages/{library_id}/*.tar.gz")])

    with tempfile.TemporaryDirectory() as tmp_dir:
        os.makedirs(f"{tmp_dir}/tests/system")
        for file in files_to_preserve:
            if Path(f"{repo_root}/packages/{library_id}/{file}").exists():
                shutil.copy(f"{repo_root}/packages/{library_id}/{file}", f"{tmp_dir}/{file}")
        shutil.rmtree(f"{repo_root}/packages/{library_id}")

        os.makedirs(f"{repo_root}/packages/{library_id}/docs")
        os.makedirs(f"{repo_root}/packages/{library_id}/tests/system")

        for file in files_to_preserve:
            if Path(f"{tmp_dir}/{file}").exists():
                shutil.copy(f"{tmp_dir}/{file}", f"{repo_root}/packages/{library_id}/{file}")
        os.chdir(f"{repo_root}/packages/{library_id}")


def create_symlink_in_dir(src_path: str, dest_path: str, filename: str, relative_level=0):
    """Creates a symlink in the given directory for <filename> pointing to <relative_level>/<filename>.

    Args:
        src_path (str): 
        dest_path (str): 
        filename (str): the name of the file to link
        relative_level (str): the level of the directory structure where the link should point to
    """
    current_dir = os.getcwd()

    os.chdir(dest_path)

    prefix = ""
    for i in range(relative_level):
        prefix += "../"

    relative_path_to_src_file = Path(f"{prefix}{src_path}/{filename}")

    print(dest_path)
    print(relative_path_to_src_file)
    print(Path(dest_path / relative_path_to_src_file).exists())
    if relative_path_to_src_file.exists():
        if not Path(filename).exists():
            Path(filename).symlink_to(relative_path_to_src_file)

    os.chdir(current_dir)


if __name__ == "__main__":
    main()
