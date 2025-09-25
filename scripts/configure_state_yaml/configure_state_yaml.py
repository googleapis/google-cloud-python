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
import yaml

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = Path(SCRIPT_DIR / ".." / "..").resolve()
PACKAGES_DIR = ROOT_DIR / "packages"
PACKAGES_TO_ONBOARD_YAML = SCRIPT_DIR / "packages_to_onboard.yaml"
LIBRARIAN_DIR = ROOT_DIR / ".librarian"
LIBRARIAN_YAML = LIBRARIAN_DIR / "state.yaml"
RELEASE_PLEASE_MANIFEST_JSON = ROOT_DIR / ".release-please-manifest.json"
GAPIC_METADATA_JSON = "gapic_metadata.json"


def configure_state_yaml() -> None:
    """
    This method updates the `state.yaml` file in the directory
    `.librarian`.
    """

    state_dict = {}

    release_please_manifest = {}
    with open(RELEASE_PLEASE_MANIFEST_JSON, "r") as release_please_manifest_json_file:
        release_please_manifest = json.load(release_please_manifest_json_file)

    packages_to_onboard = {}
    with open(PACKAGES_TO_ONBOARD_YAML, "r") as packages_to_onboard_yaml_file:
        packages_to_onboard = yaml.safe_load(packages_to_onboard_yaml_file)

    state_dict = {}
    with open(LIBRARIAN_YAML, "r") as state_yaml_file:
        state_dict = yaml.safe_load(state_yaml_file)

    existing_library_ids = {library["id"] for library in state_dict.get("libraries", [])}

    for package_name in packages_to_onboard["packages_to_onboard"]:
        # Check for duplication
        if package_name in existing_library_ids:
            print(f"Skipping package '{package_name}' as it already exists in state.yaml.")
            continue

        package_path = Path(PACKAGES_DIR / package_name).resolve()
        api_paths = []
        for individual_metadata_file in package_path.rglob(f"**/{GAPIC_METADATA_JSON}"):
            with open(individual_metadata_file, "r") as gapic_metadata_json_file:
                gapic_metadata = json.load(gapic_metadata_json_file)
                api_paths.extend(
                    [
                        {
                            "path": gapic_metadata["protoPackage"].replace(".", "/"),
                        }
                    ]
                )

        # Skip libraries which are not present in the release please manifest as
        # these are likely libraries that have already onboarded.
        if release_please_manifest.get(f"packages/{package_name}", None):
            state_dict["libraries"].append(
                {
                    "id": package_name,
                    "version": release_please_manifest[f"packages/{package_name}"],
                    "last_generated_commit": "d300b151a973ce0425ae4ad07b3de957ca31bec6",
                    "apis": api_paths,
                    "source_roots": [f"packages/{package_path.name}"],
                    "preserve_regex": [
                        # Use the full path to avoid ambiguity with the root CHANGELOG.md
                        f"packages/{package_path.name}/CHANGELOG.md",
                        "docs/CHANGELOG.md",
                        "docs/README.rst",
                        "samples/README.txt",
                        "scripts/client-post-processing",
                        "samples/snippets/README.rst",
                        "tests/system",
                    ],
                    "remove_regex": [f"packages/{package_path.name}"],
                    "tag_format": "{id}-v{version}",
                }
            )

    with open(LIBRARIAN_YAML, "w") as f:
        yaml.dump(state_dict, f, sort_keys=False, indent=2)


if __name__ == "__main__":
    configure_state_yaml()
