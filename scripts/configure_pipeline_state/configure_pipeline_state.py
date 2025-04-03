# -*- coding: utf-8 -*-
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
from typing import List

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = Path(SCRIPT_DIR / ".." / "..").resolve()
PACKAGES_DIR = ROOT_DIR / "packages"
GENERATOR_INPUT_DIR = ROOT_DIR / "generator-input"
RELEASE_PLEASE_MANIFEST_JSON = ROOT_DIR / ".release-please-manifest.json"
GAPIC_METADATA_JSON = "gapic_metadata.json"

def configure_pipeline_state(
    package_dirs: List[Path]
) -> None:
    """
    This method updates the `pipeline-state.json` file in the directory
    `generator-input`.

    Args:
        package_dirs(List[pathlib.Path]): A list of Paths, one for each package in the
            `packages/` folder whose entry will be updated in the `pipeline-state.json`.

    Returns:
        None
    """

    pipeline_state = {}            
    with open(RELEASE_PLEASE_MANIFEST_JSON, "r") as release_please_manifest_json_file:
        release_please_manifest = json.load(release_please_manifest_json_file)
        pipeline_state["commonLibrarySourcePaths"] = []
        # We don't want to generate these APIs for historic reasons (Come back to this list if needed)
        pipeline_state["ignoredApiPaths"] = [
            "google/cloud/bigquery/storage/v1alpha",
            "google/cloud/bigquery/storage/v1beta",
            "google/cloud/confidentialcomputing/v1alpha1",
        ]
        pipeline_state["imageTag"] = "latest"
        pipeline_state["libraries"] = []
        for package_dir in package_dirs:
            api_paths = []
            for individual_metadata_file in package_dir.rglob(f"**/{GAPIC_METADATA_JSON}"):
                with open(individual_metadata_file, "r") as gapic_metadata_json_file:
                    gapic_metadata = json.load(gapic_metadata_json_file)
                    api_paths.append(gapic_metadata["protoPackage"].replace(".", "/"))
            pipeline_state["libraries"].append({
                "id" : package_dir.name,
                "currentVersion": release_please_manifest[f"packages/{package_dir.name}"],
                "generationAutomationLevel": "AUTOMATION_LEVEL_AUTOMATIC",
                "releaseAutomationLevel": "AUTOMATION_LEVEL_AUTOMATIC",
                "lastGeneratedCommit": "97a83d76a09a7f6dcab43675c87bdfeb5bcf1cb5",
                "apiPaths": api_paths,
                "sourcePaths": [f"packages/{package_dir.name}"]
            })

    with open(GENERATOR_INPUT_DIR / "pipeline-state.json", "w") as f:
        json.dump(pipeline_state, f, indent=4)
        f.write("\n")


def get_all_packages(packages_dir: Path = PACKAGES_DIR) -> List[Path]:
    """
    Walks through all API packages in the specified `packages_dir` path. 

    Args:
        packages_dir(pathlib.Path): Path to the directory which contains packages.

    Returns:
        List[pathlib.Path] where each entry corresponds to a package within the
            specified `packages_dir`.
    """
    if not Path(packages_dir).exists():
        raise FileNotFoundError(f"Directory {packages_dir} not found")
    return [obj.parents[0].resolve() for obj in packages_dir.rglob("**/.OwlBot.yaml")]

if __name__ == "__main__":
    package_dirs = get_all_packages()
    configure_pipeline_state(package_dirs)
