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

import json
from pathlib import Path
import re
from typing import List

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = Path(SCRIPT_DIR / ".." / "..").resolve()
GENERATOR_INPUT_DIR = ROOT_DIR / "generator-input"
GOOGLEAPIS_DIR = ROOT_DIR / ".." / "googleapis"
REPO_METADATA_JSON = "repo-metadata.json"
PACKAGES_DIR = ROOT_DIR / "packages"

def configure_apis_json(apis_dir: List[Path] = GOOGLEAPIS_DIR) -> None:
    """
    This method updates the `apis.json` file in the directory
    `generator-input`.

    Args:
        apis_dir(List[pathlib.Path]): A list of Paths, one for each API
        whose entry will be updated in the `apis.json` files.

    Returns:
        None
    """

    pipeline_state_json = GENERATOR_INPUT_DIR / "pipeline-state.json"
    api_json = GENERATOR_INPUT_DIR / "apis.json"
    with open(pipeline_state_json, "r") as pipeline_state_json_file:
        pipeline_state = json.load(pipeline_state_json_file)
        with open(api_json, "r") as apis_json_file:
            apis = json.load(apis_json_file)
            apis["apis"] = []

            for individual_api in apis_dir:
                api_entry = {
                    "apiPath": str(individual_api.relative_to(GOOGLEAPIS_DIR.resolve()))
                }

                # TODO: Remove dependency on repo-metadata.json
                # Move these to the service config
                with open(individual_api / "BUILD.bazel", "r") as build_bazel_file:
                    build_bazel = build_bazel_file.read()
                    if "py_gapic_library" in build_bazel:
                        py_gapic_library = re.search(
                            r"(?s)py_gapic_library\((.*?)\)", build_bazel
                        ).group(1)

                        if "python-gapic-namespace" in py_gapic_library:
                            api_entry["python-gapic-namespace"] = re.search(
                                r"(?s)python-gapic-namespace\=(.*?)\"", build_bazel
                            ).group(1)

                        if "warehouse-package-name" in py_gapic_library:
                            api_entry["warehouse-package-name"] = re.search(
                                r"(?s)warehouse-package-name\=(.*?)\"", build_bazel
                            ).group(1)

                        if "transport" in py_gapic_library:
                            api_entry["transport"] = re.search(
                                r"(?s)\"?transport\s?\=\s?\"?(.*?)\"", py_gapic_library
                            ).group(1)

                        if "service_yaml" in py_gapic_library:
                            api_entry["service-yaml"] = re.search(
                                r"(?s)service_yaml\s\=\s\"(.*?)\"", py_gapic_library
                            ).group(1)

                        if (
                            "grpc_service_config" in py_gapic_library
                            and "grpc_service_config = None" not in py_gapic_library
                        ):
                            api_entry["retry-config"] = re.search(
                                r"(?s)grpc_service_config\s\=\s\"(.*?)\"", py_gapic_library
                            ).group(1)

                # For each corresponding API, find the package entry in pipeline state.json via `apiPaths`
                for pipeline_state_entry in pipeline_state["libraries"]:
                    if api_entry["apiPath"] in pipeline_state_entry["apiPaths"]:
                         api_entry["id"] = pipeline_state_entry["id"]

                # TODO: Remove dependency on repo-metadata.json
                # Move these to the service config
                if "id" in api_entry:
                    with open(PACKAGES_DIR / api_entry["id"] / ".repo-metadata.json", "r") as repo_metadata_json_file:
                        repo_metadata = json.load(repo_metadata_json_file)
                        api_entry["release-level"] = repo_metadata["release_level"]

                apis["apis"].append(api_entry)

    with open(api_json, "w") as apis_json_file:
        json.dump(apis, apis_json_file, indent=4, sort_keys=True)
        apis_json_file.write("\n")


def get_all_api_dirs(googleapis_dir: Path = GOOGLEAPIS_DIR) -> List[Path]:
    """
    Walks through all API directories in the specified `googleapis_dir` path with
    a correspnding BUILD.bazel file.

    Args:
        googleapis_dir(pathlib.Path): Path to the directory which contains a BUILD.bazel file.

    Returns:
        List[pathlib.Path] where each entry corresponds to a directory which contains a
            BUILD.bazel filewithin the specified `googleapis_dir`.
    """
    if not Path(googleapis_dir).exists():
        raise FileNotFoundError(f"Directory {googleapis_dir} not found")
    return [obj.parents[0].resolve() for obj in googleapis_dir.rglob("**/BUILD.bazel")]


if __name__ == "__main__":
    api_dirs = get_all_api_dirs()
    configure_apis_json(api_dirs)
