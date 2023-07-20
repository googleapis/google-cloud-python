# Copyright 2023 Google LLC
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

import argparse
import glob
import importlib.metadata
import json
import os.path
import re
import sys

import piplicenses
import requests

DEPENDENCY_INFO_SEPARATOR = "*" * 80 + "\n"
PACKAGE_NAME_EXTRACTOR = re.compile("^[a-zA-Z0-9._-]+")

# These packages don't have LICENSE files distributed in their packages,
# but we have manually confirmed they have a compatible license and
# included it manually in our `third_party` directory.
#
# TODO(swast): We can remove this workaround once these packages bundle the
# license file.
#
# ipython-genutils and recommonmark are both in an archived state with no likely updates in the future
#
# Tracking issues:
# * https://github.com/grpc/grpc/issues/33557
# * https://github.com/gsnedders/python-webencodings/issues/33
# * https://github.com/pickleshare/pickleshare/issues/34
DIRECT_LICENSE_MAPPINGS = {
    "grpcio-status": "https://raw.githubusercontent.com/grpc/grpc/master/LICENSE",
    "webencodings": "https://raw.githubusercontent.com/gsnedders/python-webencodings/master/LICENSE",
    "ipython-genutils": "https://raw.githubusercontent.com/ipython/ipython_genutils/master/COPYING.md",
    "pickleshare": "https://raw.githubusercontent.com/pickleshare/pickleshare/master/LICENSE",
    "recommonmark": "https://raw.githubusercontent.com/readthedocs/recommonmark/master/license.md",
}


def get_package_dependencies(pkg_name):
    """Get all package dependencies for a given package, both required and optional."""
    packages = set()
    requirements = importlib.metadata.requires(pkg_name)
    if requirements:
        for req in requirements:
            match = PACKAGE_NAME_EXTRACTOR.match(req)
            assert match, f"Could not parse {req} for package name"
            packages.add(match.group(0))
    return packages


# Inspired by third_party/colab/cleanup_filesets.py
def find_dependencies(
    roots: set[str], ignore_missing_metadata=False
) -> dict[str, dict[str, set[str]]]:
    """Return the transitive dependencies of a set of packages.
    Args:
        roots: List of package names, e.g. ["pkg1", "pkg2"]
    Returns:
        A dictionary of dependencies, e.g.
        {
            "pkg3" : {
                "Requires" : set(["pkg4", "pkg5", "pkg6"]),
                "RequiredBy": set(["pkg1"])
            },
            "pkg4" : {
                "Requires" : set([]),
                "RequiredBy": set(["pkg3"])
            },
            ...
        }
    """
    hops = set()
    visited = set()
    deps: dict[str, dict[str, set[str]]] = dict()

    # Initialize the start of the graph walk
    for root in roots:
        # Get the normalized package name
        try:
            pkg = importlib.metadata.metadata(root)
        except importlib.metadata.PackageNotFoundError:
            if not ignore_missing_metadata:
                raise
            continue
        hops.add(pkg["Name"])

    # Start the graph walk
    while True:
        if not hops:
            break
        hop = hops.pop()
        if hop in visited:
            continue
        visited.add(hop)

        for dep in get_package_dependencies(hop):
            # Get the normalized package name
            try:
                req_pkg = importlib.metadata.metadata(dep)
            except importlib.metadata.PackageNotFoundError:
                if not ignore_missing_metadata:
                    raise
                continue
            dep = req_pkg["Name"]

            # Create outgoing edge only for non root packages, for which an
            # entry must have been created in the deps dictionary when we
            # saw the package for the first time during the graph walk
            if hop in deps:
                deps[hop]["Requires"].add(dep)

            if dep in deps:
                # We have already seen this requirement in the graph walk.
                # Just update the incoming dependency and carry on.
                deps[dep]["RequiredBy"].add(hop)
            else:
                # This is the first time we came across this requirement.
                # Create a new entry with the incoming dependency.
                deps[dep] = {"RequiredBy": {hop}, "Requires": set()}

                # Put it in the next hops for further graph traversal
                hops.add(dep)

    return deps


def get_metadata_and_filename(
    package_name: str,
    metadata_name: str,
    metadata_file: str,
    metadata_text: str,
    ignore_missing=True,
) -> tuple[str, str] | None:
    """Get package metadata and corresponsing file name."""

    # Check metadata file
    metadata_filepath_known = metadata_file != piplicenses.LICENSE_UNKNOWN
    if not metadata_filepath_known and not ignore_missing:
        raise ValueError(f"No {metadata_name} file found for {package_name}")

    # Check metadata text
    if metadata_text != piplicenses.LICENSE_UNKNOWN:
        output_filename = metadata_name
        if metadata_filepath_known:
            output_filename = os.path.basename(metadata_file)
        if not output_filename:
            raise ValueError(
                f"Need a file name to write {metadata_name} text for {package_name}."
            )
        return metadata_text, output_filename
    elif not ignore_missing:
        raise ValueError(f"No {metadata_name} text found for {package_name}")

    return None


def fetch_license_and_notice_metadata(packages: list[str]):
    """Fetch metadata including license and notice for given packages.
    Returns a json object.
    """
    parser = piplicenses.create_parser()
    args = parser.parse_args(
        [
            "--format",
            "json",
            "--with-license-file",
            "--with-notice-file",
            "--with-urls",
            "--with-description",
            "--packages",
            *packages,
        ]
    )
    output_str = piplicenses.create_output_string(args)
    metadatas = json.loads(output_str)
    return metadatas


def write_lines_without_trailing_spaces(file, text: str, key: str):
    """Write text lines to a file without the trailing spaces.
    This will stop complaints by the trailing-whitespace pre-commit hook."""
    text = "\n".join([line.rstrip() for line in text.split("\n")])
    file.write(f"{key}:\n{text}\n")


def write_metadata_to_file(
    file, metadata, with_version=False, requires_packages=[], packages_required_by=[]
):
    """Write package metadata to a file object."""
    file.write(DEPENDENCY_INFO_SEPARATOR)

    info_keys = ["Name"]
    if with_version:
        info_keys.append("Version")
    info_keys.extend(["License", "URL"])
    file.writelines([f"{key}: {metadata[key]}\n" for key in info_keys])

    if requires_packages:
        file.write(f"Requires: {', '.join(sorted(requires_packages))}\n")

    if packages_required_by:
        file.write(f"Required By: {', '.join(sorted(packages_required_by))}\n")

    # Try to generate third party license

    license_info = get_metadata_and_filename(
        metadata["Name"],
        "LICENSE",
        metadata["LicenseFile"],
        metadata["LicenseText"],
        ignore_missing=metadata["Name"] in DIRECT_LICENSE_MAPPINGS,
    )

    license_text = ""
    if license_info:
        license_text = license_info[0]
    else:
        license_text_response = requests.get(DIRECT_LICENSE_MAPPINGS[metadata["Name"]])
        license_text = license_text_response.text

    write_lines_without_trailing_spaces(file, license_text, "License")

    # Try to generate third party notice
    notice_info = get_metadata_and_filename(
        metadata["Name"],
        "NOTICE",
        metadata["NoticeFile"],
        metadata["NoticeText"],
        ignore_missing=True,
    )

    if notice_info:
        write_lines_without_trailing_spaces(file, notice_info[0], "Notice")

    file.write(DEPENDENCY_INFO_SEPARATOR)


def write_third_party_vendored_license(file, path):
    """Write license of a vendored third party library to notices file."""
    file.write(DEPENDENCY_INFO_SEPARATOR)
    file.write(f"Vendored Code: {os.path.dirname(path)}\n")
    notice_key = f"Notice ({os.path.basename(path)})"
    write_lines_without_trailing_spaces(file, open(path).read(), notice_key)
    file.write(DEPENDENCY_INFO_SEPARATOR)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate third party notices for bigframes dependencies."
    )
    parser.add_argument(
        "--with-version",
        action="store_true",
        default=False,
        help="Include the version information for each package.",
    )
    parser.add_argument(
        "--with-requires",
        action="store_true",
        default=False,
        help="Include for each package the packages it requires.",
    )
    parser.add_argument(
        "--with-required-by",
        action="store_true",
        default=False,
        help="Include for each package the packages that require it.",
    )
    parser.add_argument(
        "--output-file",
        action="store",
        default="THIRD_PARTY_NOTICES",
        help="The output file to write third party notices in.",
    )
    args = parser.parse_args(sys.argv[1:])

    # Initialize the root package
    roots = {"bigframes"}

    # Find dependencies
    # Let's ignore the packages that are not installed assuming they are
    # just the optional dependencies that bigframes does not require.
    # One example is the dependency path bigframes -> SQLAlchemy -> pg8000,
    # where pg8000 is only an optional dependency for SQLAlchemy which bigframes
    # is not depending on
    # https://github.com/sqlalchemy/sqlalchemy/blob/7bc81947e22dc32368b0c49a41c398cd251d94af/setup.cfg#LL62C21-L62C27
    deps = find_dependencies(roots, ignore_missing_metadata=True)

    # Use third party solution to fetch dependency metadata
    deps_metadata = fetch_license_and_notice_metadata(list(deps))
    deps_metadata = sorted(deps_metadata, key=lambda m: m["Name"])

    # Write the file
    with open(args.output_file, "w") as f:
        # Generate third party metadata for each dependency
        for metadata in deps_metadata:
            dep = deps[metadata["Name"]]
            write_metadata_to_file(
                f,
                metadata,
                args.with_version,
                dep["Requires"] if args.with_requires else [],
                dep["RequiredBy"] if args.with_required_by else [],
            )

        # Generate third party vendored notices
        notices = set()
        for filename in [
            "LICENCE",
            "LICENCE.txt",
            "LICENSE",
            "LICENSE.txt",
            "NOTICE",
            "NOTICE.txt",
            "COPYING",
            "COPYING.txt",
        ]:
            notices.update(glob.glob(f"third_party/bigframes_vendored/*/{filename}"))
        for path in sorted(notices):
            write_third_party_vendored_license(f, path)
