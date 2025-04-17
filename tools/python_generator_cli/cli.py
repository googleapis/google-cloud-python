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
def generate(
    api_path: str, output: str, api_root: str
):
    """ Generates a python client library using the given arguments."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        with open("/generator-input/apis.json", "r") as apis_json_file:
            all_apis_config = json.load(apis_json_file)
            api_specific_config = next(item for item in all_apis_config["apis"] if item["apiPath"] == api_path)
            config_keys = ["transport", "warehouse-package-name", "service-yaml", "retry-config", "release-level"]
            generator_options = []
            for key in config_keys:
                config_value = api_specific_config.get(key, None)
                if config_value:
                    if key == "service-yaml" or key == "retry-config":
                        generator_options.append(f"{key}={api_path}/{config_value},")
                    else:
                        generator_options.append(f"{key}={config_value},")    
            
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

if __name__ == "__main__":
    main()
