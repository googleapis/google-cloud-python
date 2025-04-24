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

        default_versions = {}
        reference_doc_includes = {}
        default_versions_extended = {}
        # For each package in pipeline_state, calculate the default version if necessary
        for pipeline_state_entry in pipeline_state["libraries"]:
            if len(pipeline_state_entry["apiPaths"]) < 2:
                continue
            trimmed_apis = [api.split("/v")[0] for api in pipeline_state_entry["apiPaths"]]
            trimmed_api_dict = {trimmed_api : trimmed_apis.count(trimmed_api) for trimmed_api in trimmed_apis}
            path_of_interest = [i for i in trimmed_api_dict if trimmed_api_dict[i] > 1]
            default_version = None
            for api_path in pipeline_state_entry["apiPaths"]:
                if path_of_interest and path_of_interest[0] + "/v" not in api_path:
                    continue
                # TODO: Move this to the service config
                # For this API, determine if we need to explicitly set it to the default version to True or False
                # If there is only 1 apiPath, then it is already the default, no need to do anything
                # A default should explicitly be set for all apis in apiPaths
                if default_version is None:
                    default_version = api_path
                elif 'beta' in api_path and 'alpha' in default_version:
                    default_version = api_path
                elif 'beta' not in api_path and 'alpha' not in api_path:
                    try:
                        parsed_version_default = int(default_version.split("/v")[-1])
                    except ValueError:
                        default_version = api_path
                        parsed_version_default = None
                    try:
                        parsed_version_current = int(api_path.split("/v")[-1])                                        
                        if parsed_version_default is None or parsed_version_current < parsed_version_default:
                            default_version = api_path
                    except ValueError:
                        pass

                reference_doc_includes_forced = None
                default_version_secondary = None
                if pipeline_state_entry["id"] == "google-cloud-trace":
                    default_version = "google/cloud/trace/v2"
                elif pipeline_state_entry["id"] == "google-cloud-workflows":
                    default_version_secondary = "google/cloud/workflows/executions/v1"
                    default_version = "google/cloud/workflows/v1"
                    reference_doc_includes_forced = "workflows_v1beta+executions_v1+executions_v1beta"
                elif pipeline_state_entry["id"] == "google-ai-generativelanguage":
                    default_version = "google/ai/generativelanguage/v1beta"
                elif pipeline_state_entry["id"] == "google-analytics-admin":
                    default_version = "google/analytics/admin/v1alpha"
                if default_version_secondary:
                    default_versions_extended[pipeline_state_entry["id"]] = default_version_secondary

                default_versions[pipeline_state_entry["id"]] = default_version
                
                import os
                if not reference_doc_includes_forced:
                    reference_doc_includes[pipeline_state_entry["id"]] = "+".join([api.replace(os.path.commonprefix(["/".join(default_version.split("/")[:-2]), api]) + "/", "").replace("/", "_") for api in pipeline_state_entry["apiPaths"] if api != default_version])
                else:
                    reference_doc_includes[pipeline_state_entry["id"]] =  reference_doc_includes_forced

        with open(api_json, "r") as apis_json_file:
            apis = json.load(apis_json_file)
            apis["apis"] = []

            for individual_api in apis_dir:
                api_entry = {
                    "apiPath": str(individual_api.relative_to(GOOGLEAPIS_DIR.resolve()))
                }

                # TODO: Remove dependency on BUILD.bazel
                # Move these to the service config
                with open(individual_api / "BUILD.bazel", "r") as build_bazel_file:
                    build_bazel = build_bazel_file.read()
                    if "py_gapic_library" in build_bazel:
                        py_gapic_library = re.search(
                            r"(?s)py_gapic_library\((.*?)\)", build_bazel
                        ).group(1)

                        py_gapic_options = [
                            "autogen-snippets",
                            "python-gapic-name",
                            "python-gapic-namespace",
                            "warehouse-package-name",
                        ]
                        for gapic_option in py_gapic_options:
                            if f"{gapic_option}=" in py_gapic_library:
                                api_entry[gapic_option] = re.search(
                                    fr"(?s){gapic_option}\=(.*?)\"", py_gapic_library
                                ).group(1)

                        if "transport" in py_gapic_library:
                            api_entry["transport"] = re.search(
                                r"(?s)\"?transport\s?\=\s?\"?(.*?)\"", py_gapic_library
                            ).group(1)

                        if  "service_yaml" in py_gapic_library:
                            service_yaml_entry = re.search(
                                r"(?s)service_yaml\s\=\s\"(.*?)\"", py_gapic_library
                            ).group(1)
                            # Some APIs have ":<serviceyaml>" instead of "<serviceyaml>". 
                            # Remove the leading colon
                            if "//" not in service_yaml_entry:
                                api_entry["service-yaml"] = service_yaml_entry.replace(":","")

                        if "rest_numeric_enums" in py_gapic_library:
                            api_entry["rest-numeric-enums"] = re.search(
                                r"(?s)rest_numeric_enums\s?\=\s?(.*?),", py_gapic_library
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
                         api_entry["gapic-version"] = pipeline_state_entry["currentVersion"]

                # TODO: Remove dependency on repo-metadata.json
                # Move these to the service config
                if "id" in api_entry:
                    with open(PACKAGES_DIR / api_entry["id"] / ".repo-metadata.json", "r") as repo_metadata_json_file:
                        repo_metadata = json.load(repo_metadata_json_file)
                        api_entry["release-level"] = repo_metadata["release_level"]
                        
                        # backfill information not in service yaml
                        if "service-yaml" in api_entry:
                            with open(individual_api / api_entry["service-yaml"], "r") as service_yaml_file:
                                service_yaml = service_yaml_file.read()
                                if "documentation_uri:" not in service_yaml and "id" in api_entry:    
                                    api_entry["documentation-uri"] = repo_metadata["product_documentation"]

                    if api_entry["id"] in default_versions:
                        if default_versions_extended and api_entry["id"] in default_versions_extended and api_entry["apiPath"].split("/")[:-1] == default_versions_extended[api_entry["id"]].split("/")[:-1]:
                                api_entry["default-proto-package"] = default_versions_extended[api_entry["id"]].replace("/", ".")
                        else:
                            api_entry["default-proto-package"] = default_versions[api_entry["id"]].replace("/", ".")
                        api_entry["reference-doc-includes"] = reference_doc_includes[api_entry["id"]]

                    if api_entry["id"] == "google-ads-marketingplatform-admin":
                        api_entry["documentation-name"] = api_entry["id"]
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
