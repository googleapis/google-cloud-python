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
    import subprocess  
    subprocess.run([f"protoc {api_path}/*.proto --python_gapic_out={output}"], cwd=api_root, shell=True)

if __name__ == "__main__":
    main()
