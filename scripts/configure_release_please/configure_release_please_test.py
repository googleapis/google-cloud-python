from pathlib import Path
import shutil
import unittest

import configure_release_please

SCRIPT_DIR = Path(__file__).parent.resolve()
PACKAGES_DIR = SCRIPT_DIR / "test_resources" / "packages"


class TestChangeSummary(unittest.TestCase):
    def test_get_version_for_package(self):
        path_to_gapic_version_py = (
            PACKAGES_DIR / "google-cloud-ids/google/cloud/ids/gapic_version.py"
        )
        version = configure_release_please.get_version_for_package(
            path_to_gapic_version_py
        )
        self.assertEqual(version, (1, 5, 1))

    def test_get_version_for_package_raises_when_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            configure_release_please.get_version_for_package(Path("does/not/exist"))

    def test_walk_through_owlbot_dirs(self):
        expected_result = [PACKAGES_DIR / "google-cloud-ids"]
        self.assertEqual(
            configure_release_please.walk_through_owlbot_dirs(PACKAGES_DIR),
            expected_result,
        )

    def test_walk_through_owlbot_dirs_bad_path(self):
        with self.assertRaises(FileNotFoundError):
            configure_release_please.walk_through_owlbot_dirs(Path("does/not/exist"))

    def test_configure_release_please_manifest(self):
        expected_result = """{
    "packages/google-cloud-ids": "1.5.1"
}\n"""
        package_dirs = configure_release_please.walk_through_owlbot_dirs(PACKAGES_DIR)
        configure_release_please.configure_release_please_manifest(
            package_dirs=package_dirs, root_dir=SCRIPT_DIR
        )
        self.assertEqual(
            (SCRIPT_DIR / ".release-please-manifest.json").read_text(), expected_result
        )

    def test_configure_release_please_config(self):
        expected_result = """{
    "packages": {
        "packages/google-cloud-ids": {
            "component": "google-cloud-ids",
            "extra-files": [
                "google/cloud/ids/gapic_version.py",
                "google/cloud/ids_v1/gapic_version.py"
            ],
            "release-type": "python"
        }
    }
}\n"""
        package_dirs = configure_release_please.walk_through_owlbot_dirs(PACKAGES_DIR)
        configure_release_please.configure_release_please_config(
            package_dirs=package_dirs, root_dir=SCRIPT_DIR
        )
        self.assertEqual(
            (SCRIPT_DIR / "release-please-config.json").read_text(), expected_result
        )
