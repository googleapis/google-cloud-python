# Ad-Hoc Package Testing

## Overview
Ad-hoc package testing allows you to run CI tests for a specific subset of packages or predefined package groups without the need for intrusive and/or temporary mods to the package code to trigger a CI job run. This is useful for verifying:
* local changes or remote changes (i.e. on GitHub)
* debugging specific package failures
* testing CI infrastructure updates without wasting resources.

## How It Works
The ad-hoc testing system reads configuration files in the `/ci/adhoc` directory to determine which packages to test. It can be triggered via CI labels (e.g., `test:adhoc`).

## Configuration Files

### 1. `.standalone_package_list.txt`
This file lists the specific packages or groups you want to test.

*   **To test an individual package:** Add a line starting with `package: ` (be sure to include the colon and space) followed by the package directory name.
    *   *Example:* `package: google-cloud-dns`
*   **To test a group of packages:** Add a line starting with `group: ` (be sure to include the colon and space) followed by the group name. NOTE: groups are defined in the file: `.package_groups.txt`
    *   *Example:* `group: handwritten`

### 2. `.package_groups.txt`
This file defines groups of commonly tested packages for convenience of the team. Groups such as all handwritten, all core, all hybrids, etc. can be defined here.

#### 💡 Pro Tip
You can mix packages and groups in `.standalone_package_list.txt`. The system will automatically deduplicate the list so each package is tested only once!

*   **Format:** Each package in a group should be on its own line, prefixed by the group name, colon, and a space.
    *   *Example:*
        ```text
        handwritten: google-cloud-translate
        handwritten: google-cloud-logging
        core: google-api-core
        ```

## Usage

1.  **Edit Configuration:** Open `.standalone_package_list.txt` and add the packages or groups you want to test.
2.  **Trigger Tests:**
    * Issue a Pull Request (PR) with the updated `.standalone_package_list.txt` file.
    * **In GitHub UI:** Add the `test:adhoc` label to your PR.

## ⚠️ Best Practices & Warnings

*   **Do Not Pollute Packages:** Do not modify package code just to trigger tests. Use the ad-hoc configuration files instead.
*   **Revert Temporary Changes:** If you add temporary print statements or dummy tests for debugging, ensure they are reverted before merging.
*   **Clean Up:** Keep the configuration files clean and remove unused entries.
