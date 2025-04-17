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
import subprocess
import tempfile

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
def generate_raw(
    api_path: str, output: str, api_root: str
):
    """ Generates a python client library using the given arguments."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        generator_command = f"protoc {api_path}/*.proto --python_gapic_out={tmp_dir}"
        subprocess.run([generator_command], cwd=api_root, shell=True)
        subprocess.run(f"isort --fss docs google tests noxfile.py setup.py", cwd=tmp_dir, shell=True)
        subprocess.run(f"black docs google tests noxfile.py setup.py", cwd=tmp_dir, shell=True)
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
def generate_library(
    api_root: str, generator_input: str, output: str, library_id: str
):
    """ Generates a python client library using the given arguments."""

    with open(f"{generator_input}/pipeline-state.json", "r") as pipeline_state_json_file:
        pipeline_state = json.load(pipeline_state_json_file)
        with open(f"{generator_input}/apis.json", "r") as apis_json_file:
            all_apis_config = json.load(apis_json_file)
            library_specific_config = next(item for item in pipeline_state["libraries"] if item["id"] == library_id)
            for api_path in library_specific_config["apiPaths"]:
                api_specific_config = next(item for item in all_apis_config["apis"] if item["apiPath"] == api_path)
                print(api_path)
                config_keys = ["transport", "python-gapic-namespace", "python-gapic-name", "warehouse-package-name", "service-yaml", "retry-config", "release-level", "default-version", "non-default-versions", "documentation-uri"]
                generator_options = []
                for key in config_keys:
                    config_value = api_specific_config.get(key, None)
                    if config_value:
                        if key == "service-yaml" or key == "retry-config":
                            generator_options.append(f"{key}={api_path}/{config_value},")
                        else:
                            generator_options.append(f"{key}={config_value},")

                with tempfile.TemporaryDirectory() as tmp_dir:                    
                    generator_command = f"protoc {api_path}/*.proto --python_gapic_out={tmp_dir}"
                    if len(generator_options):
                        generator_command += f" --python_gapic_opt=rest-numeric-enums=True,metadata,"
                        for generator_option in generator_options:
                            generator_command += generator_option

                    print(generator_command)

                    subprocess.run([generator_command], cwd=api_root, shell=True)
                    subprocess.run(f"isort --fss docs google tests noxfile.py setup.py", cwd=tmp_dir, shell=True)
                    subprocess.run(f"black docs google tests noxfile.py setup.py", cwd=tmp_dir, shell=True)
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
    The name of the package to clean.
    """,
)
def clean(
    repo_root: str, library_id: str
):
    """ Deletes all automatically generated files for a given library-id."""

    # Delete entire package directory
    subprocess.run(f"rm -rf {repo_root}/packages/{library_id}")
    subprocess.run(f"mkdir {repo_root}/packages/{library_id}")
    subprocess.run(f"git checkout {repo_root}/packages/{library_id}/tests/system")
    #subprocess.run(f"git checkout {repo_root}/packages/{library_id}/tests/")

if __name__ == "__main__":
    main()
