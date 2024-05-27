# Copyright 2024 Google LLC
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

from datetime import datetime
import json
from pathlib import Path
from typing import List
import re

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = Path(SCRIPT_DIR / ".." / "..").resolve()
PACKAGES_DIR = ROOT_DIR / "packages"


def get_stable_clients(packages_dir: Path = PACKAGES_DIR) -> List[Path]:
    """
    Walks through all API packages and returns paths to versions which appear
    to be stable in the specified `packages_dir`.
    """
    return [
        obj.relative_to(packages_dir)
        for obj in packages_dir.rglob(r"**/google/**/*v[0-9]/")
    ]


def days_since_library_launch(package_name: str) -> int:
    """
    Returns the number of days since the initial version of the library.

    Args:
        package_name(str): Name of the package to be checked.

    Returns:
        int: The number of days since the initial version of the library
    """
    days_since_library_launch = 0
    with open(PACKAGES_DIR / package_name / "CHANGELOG.md", "r") as changelog_file:
        changelog = changelog_file.read()
        initial_version = re.findall(r"(?<=## 0.1.0\s\().*(?=\))", changelog)
        if len(initial_version) == 0:
            initial_version = re.findall(r"(?<=## 0.2.0\s\().*(?=\))", changelog)
        if len(initial_version) == 1:
            initial_version_date = datetime.fromisoformat(initial_version[0])
            days_since_library_launch = (datetime.now() - initial_version_date).days
    return days_since_library_launch


def is_library_major_version_zero(package_name: str) -> bool:
    """
    Returns true if the package has a major version of zero.

    Args:
        package_name(str): Name of the package to be checked.

    Returns:
        bool: Whether or not the package has a major version of 0.
    """
    with open(
        ROOT_DIR / ".release-please-manifest.json", "r"
    ) as release_please_manifest_file:
        release_please_manifest_json = json.loads(release_please_manifest_file.read())
        return release_please_manifest_json[f"packages/{package_name}"][0:2] == "0."


def protote_to_stable_in_repo_metadata(repo_metadata_path: Path) -> bool:
    """
    Updates the `release_level` in the given repo_metadata_path from
    `preview` to `stable`.

    Args:
        repo_metadata_path(pathlib.Path): Path to the .repo-metadata.json file to be updated.

    Returns:
        bool: Whether or not the package was promoted to stable
    """
    promoted = False
    with open(repo_metadata_path, "r") as repo_file:
        repo_json = json.loads(repo_file.read())

    STABLE_VERSION_REGEX = re.compile("^v\d+$")
    if repo_json["release_level"] == "preview" \
        and STABLE_VERSION_REGEX.search(repo_json["default_version"],):
        repo_json["release_level"] = "stable"
        promoted = True
        with open(repo_metadata_path, "w") as repo_file:
            json.dump(repo_json, repo_file, indent=4)
            repo_file.write("\n")
    return promoted


def is_package_release_level_pinned(package_name: str) -> bool:
    """
    Returns true if the package release level is pinned.

    Args:
        package_name(str): Name of the package to be checked.

    Returns:
        bool: Whether or not the package release level is pinned.
    """
    
    # TODO (Add logic to check for pinned release level)
    return False

def promote_packages_to_stable(packages_dir: Path = PACKAGES_DIR) -> List[Path]:
    """
    Walks through all API packages with versions which appear to be stable
    in the specified `packages_dir` and promotes them to stable if they
    meet the following conditions:
        - There is at least 1 stable client without a `beta` or `alpha` suffix
        - The major version of the library is currently at 0
        - More than 60 days has elapsed since the initial creation of the library

    Args:
        packages_dir(pathlib.Path): Path to the directory which contains packages.

    Returns:
        List[pathlib.Path] where each entry corresponds to a package within the
            specified `packages_dir`, which appear to be stable.
    """
    if not Path(packages_dir).exists():
        raise FileNotFoundError(f"Directory {packages_dir} not found")

    # TODO once https://github.com/googleapis/google-cloud-python/pull/12734 is merged,
    # get packages which have the release level pinned and skip them in the for loop below.
    for version_path in get_stable_clients():
        package_name: Path = version_path.parts[0]
        package_path: Path = PACKAGES_DIR / package_name

        if (
            is_library_major_version_zero(package_name)
            and days_since_library_launch(package_name) > 30
            and not is_package_release_level_pinned(package_name)
        ):
            if protote_to_stable_in_repo_metadata(package_path / ".repo-metadata.json"):
                owl_bot_staging_dir = Path(ROOT_DIR / "owl-bot-staging")
                Path(owl_bot_staging_dir).mkdir(exist_ok=True)
                Path(owl_bot_staging_dir / package_name).mkdir(exist_ok=True)
                open(owl_bot_staging_dir / package_name / "trigger-post-processor.txt", "w").close()


if __name__ == "__main__":
    promote_packages_to_stable()
