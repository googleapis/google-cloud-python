import json
from pathlib import Path
from typing import Union, Dict, List, Tuple
import re

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = Path(SCRIPT_DIR / ".." / "..").resolve()
PACKAGES_DIR = ROOT_DIR / "packages"


def get_version_for_package(version_path: Path) -> Tuple[int]:
    """
    Given a `version_path` to a `gapic_version.py` file,
    return Tuple<int> which contains the version.

    Args:
        version_path(pathlib.Path): Path to the gapic_version.py file

    Returns:
        Tuple[int] in the format (<major>, <minor>, <patch>)
    """
    VERSION_REGEX = r"__version__\s=\s\"(?P<major_version>\d+)\.(?P<minor_version>\d+)\.(?P<patch_version>\d+)\""
    match = re.search(VERSION_REGEX, version_path.read_text())

    if match is None:
        raise Exception("Could not detect version")

    major_version = int(match.group("major_version"))
    minor_version = int(match.group("minor_version"))
    patch_version = int(match.group("patch_version"))

    if any(elem is None for elem in [major_version, minor_version, patch_version]):
        raise Exception("could not detect version")

    return (major_version, minor_version, patch_version)


def get_packages_with_owlbot_yaml(packages_dir: Path = PACKAGES_DIR) -> List[Path]:
    """
    Walks through all API packages in the specified `packages_dir` path. 

    Args:
        packages_dir(pathlib.Path): Path to the directory which contains packages.

    Returns:
        List[pathlib.Path] where each entry corresponds to a package within the
            specified `packages_dir`, which has a corresponding .OwlBot.yaml file.
    """
    if not Path(packages_dir).exists():
        raise FileNotFoundError(f"Directory {packages_dir} not found")
    return [obj.parents[0].resolve() for obj in packages_dir.rglob("**/.OwlBot.yaml")]


def configure_release_please_manifest(
    package_dirs: List[Path], root_dir: Path = ROOT_DIR
) -> None:
    """
    This method updates the `.release-please-manifest.json` file in the directory
    `root_dir`.

    Args:
        package_dirs(List[pathlib.Path]): A list of Paths, one for each package in the
            `packages/` folder whose entry will be updated in the release-please manifest.
        root_dir(pathlib.Path): The directory to update the `.release-please-manifest.json`

    Returns:
        None
    """
    release_please_manifest = root_dir / ".release-please-manifest.json"
    with open(release_please_manifest, "r") as f:
        manifest_json = json.load(f)
        for package_dir in package_dirs:
            if f"packages/{package_dir.name}" not in manifest_json:
                manifest_json[f"packages/{package_dir.name}"] = "0.0.0"

            gapic_version_file = next(package_dir.rglob("**/gapic_version.py"), None)
            if gapic_version_file is None:
                raise Exception("Failed to find gapic_version.py")
            version = get_version_for_package(gapic_version_file)
            # check the version in gapic_version.py and update if newer than the default which is
            # 0.0.0 or 0.1.0.
            if version != (0, 0, 0) and version != (0, 1, 0):
                manifest_json[
                    f"packages/{package_dir.name}"
                ] = f"{version[0]}.{version[1]}.{version[2]}"

    with open(release_please_manifest, "w") as f:
        json.dump(manifest_json, f, indent=4, sort_keys=True)
        f.write("\n")


def configure_release_please_config(
    package_dirs: List[Path], root_dir: Path = ROOT_DIR
) -> None:
    """
        This method updates the `release-please-config.json` file in the directory
        `root_dir`. If `root_dir` is not provided, `google-cloud-python` will be used as the root.

        Args:
            package_dirs(List[pathlib.Path]): A list of Paths, one for each package in
                the `packages/` folder whose entry will be updated in the release-please config.
            root_dir(pathlib.Path): The directory to update the `release-please-config.json`

        Returns:
            None
    """
    release_please_config = root_dir / "release-please-config.json"
    config_json = {"packages": {}}
    for package_dir in package_dirs:
        extra_files: List[Union[str, Dict[str, str]]] = [
            str(file.relative_to(package_dir))
            for file in sorted(package_dir.rglob("**/gapic_version.py"))
        ]
        if len(extra_files) < 1:
            raise Exception("Failed to find gapic_version.py")
        for json_file in sorted(package_dir.glob("samples/**/*.json")):
            sample_json = {}
            sample_json["jsonpath"] = "$.clientLibrary.version"
            sample_json["path"] = str(json_file.relative_to(package_dir))
            sample_json["type"] = "json"
            extra_files.append(sample_json)

        config_json["packages"][f"packages/{package_dir.name}"] = {
            "component": f"{package_dir.name}",
            "release-type": "python",
            "extra-files": extra_files,
            "bump-minor-pre-major": True,
            "bump-patch-for-minor-pre-major": True,
        }

    with open(release_please_config, "w") as f:
        json.dump(config_json, f, indent=4, sort_keys=True)
        f.write("\n")


if __name__ == "__main__":
    owlbot_dirs = get_packages_with_owlbot_yaml()
    configure_release_please_manifest(owlbot_dirs)
    configure_release_please_config(owlbot_dirs)
