# Plan for EOL Python Runtime Migration (3.7, 3.8, 3.9)

## Overview

This plan outlines the approach to update approximately 20 handwritten library packages to drop support for end-of-life Python runtimes (3.7, 3.8, 3.9) and ensure they are configured for modern versions (switching to 3.10 as minimum where appropriate).

## Strategy

### 1. Branching & PRs
- **One Branch Per Package:** To keep PRs manageable and isolated, we will create a dedicated worktree and branch for each package (e.g., `feat/drop-python-3.7-3.9-<package-name>`).
- **Standardized PRs:** We will use a template for PR titles and descriptions to maintain consistency and speed up the process.
  - *Title:* `feat(<package>): Drop support for Python 3.7, 3.8, and 3.9`
  - *Description:* see the PR template below. Use a scratch file to ensure that markdown and newlines are preserved.

### 2. Commit Strategy (Small & Reversible)
To make reviews easier and allow for selective reverts, changes will be grouped into small, logical commits following Conventional Commits:
- **Commit 1:** `feat(<package>): Update setup.py metadata and python_requires`
- **Commit 2:** `feat(<package>): Update Nox sessions to remove old versions`
- **Commit 3:** `docs(<package>): Update README and CONTRIBUTING documentation`
- **Commit 4:** `feat(<package>): Remove compatibility code and fallbacks for old versions`
- **Commit 5:** `test(<package>): Remove version-specific skips or conditions in tests`

### 3. Per-Package Workflow

For each package in the target list:

1.  **Sync & Branch:**
    -   Ensure `main` is up to date.
    -   Create the feature branch: `git checkout -b feat/drop-python-3.7-3.9-<package-name>`.
2.  **Scan (Baseline):**
    -   Run the `version_scanner` for the package to get a list of all occurrences of 3.7, 3.8, and 3.9.
3.  **Apply Changes:**
    -   Follow the commit strategy to make targeted changes across the repository.
    -   **Sync Documentation**: If the package has a `docs` folder containing a `README.rst`, copy the updated top-level `README.rst` to overwrite the one in the `docs` folder (unless it is a symlink).
4.  **Verify (Post-Scan):**
    -   Run the `version_scanner` again. The result should be 0 matches (or only valid ignores/false positives).
5.  **Local Test:**
    -   Run the unit tests using Nox (e.g., `nox -s unit`) to ensure no regressions.
    -   Run the blacken and lint nox sesssions to ensure that the code is formatted correctly.
6.  **Push & PR:**
    -   Push the branch and create the PR.

## Quality Assurance (Minimizing Mistakes)

-   **Double Scanning:** Using the `version_scanner` both *before* and *after* changes ensures no references are missed.
-   **Standardized Checklists:** We can maintain a `work_state.md` file to track the progress of each package and ensure no step is skipped.
-   **Automated Verification:** The post-change scan and `nox` sessions serve as an automated check that the work is complete.

## Constraints File Handling

- **Lowest Runtime Constraints:** The constraint file associated with the lowest version of accepted runtime must always have versioned constraints that match the lowest acceptable versions found in `setup.py` or `pyproject.toml`.
- **Migration on Drop:** When dropping a Python runtime, copy the lowest versioned constraints from the current lowest constraints file into what will become the new lowest constraint file before deleting the now deprecated constraints file.
- **Deletion:** Deprecated constraints files must be deleted.
- **Higher Versions:** Higher versioned constraints files are allowed to be empty, but the lowest must always be populated.

## Agreed Standards and Preferred Approaches for Code Refactoring
All matches will need to be dispositioned; below are some approaches for handling common patterns that appear:

### 1. Runtime Version Checks
* **Standard**: `sys.version_info < (X, Y)` (Supports all common variations: `<`, `<=`, `>`, `>=`, `==`, `!=`)
* **Rationale**: Highly idiomatic. Python compares tuples lexicographically, allowing native and robust handling of major, minor, and micro version segments.
* **Patterns to Hunt & Replace**: 
  * `sys.version_info.major == 3 and sys.version_info.minor < Y`
  * `sys.version_info[:2] < (X, Y)`
  * `sys.hexversion < ...`

### 2. Pytest Skips
* **Standard**: `@pytest.mark.skipif(sys.version_info < (X, Y), reason="Requires Python X.Y+")`
* **Rationale**: Direct evaluation is explicit, avoiding the overhead and fragility of string condition evaluations.
* **Patterns to Hunt & Replace**:
  * `@pytest.mark.skipif("sys.version_info < (X, Y)"...)` (string-based)
  * Custom helper conditional skips (e.g., `helpers.is_py37()`)

### 3. Noxfile Version Matches
* **Standard**: `session.python == "X.Y"`
* **Rationale**: Nox sessions inherently represent Python versions as strings (e.g., `"3.10"`), so direct string comparison is the most reliable mechanism.
* **Patterns to Hunt & Replace**:
  * `float(session.python) < X.Y` (Dangerous for things like `3.10` evaluating as `3.1`)
  * Tuple conversions of the string

## Code Cleanup Rules
* **Polyfills**: Remove dead `try/except` blocks guarding polyfills for features that are now standard (e.g., falling back to `typing_extensions` when standard `typing` now supports the feature).
* **Obsolete Skips**: Remove pytest skips that check for Python features that are now universally available in our supported versions.
* **Comments**: Update all accompanying comments and docstrings to reflect the dropped support and match the new reality.
* **Established Features**: Drop old comments describing a feature that has since become an established component of the language (e.g., removing mentions of "Python 3.8+ uses `add_dll_directory`").

## Reference Disposition Rules

Every reference to Python 3.7, 3.8, or 3.9 found by the scanner in any file (except those in `.scannerignore`) must be dispositioned in one of the following ways:

1.  **Update**: Update the reference because it remains necessary to successfully use the library (e.g., swapping `3.9` to `3.10` in `setup.py` or build scripts).
2.  **Delete**: Delete the reference because it is no longer relevant. This includes dead code, obsolete fallback blocks, and comments about features that are now standard.
3.  **Pragma Ignore**: Mark the line with a version scanner pragma (e.g., `# version-scanner: ignore`) so it no longer flags the scanner. Use this ONLY when the reference is never expected to change (e.g., true false positives like port numbers, or immutable historical facts). Do NOT use pragmas for references expected to change in future upgrades (e.g., warning filters for current runtimes); let the scanner flag them so we are forced to evaluate them every time we upgrade!
4.  **Manual Ignore**: If the file format does not support comments (and thus pragmas cannot be used), manually ignore the match and document it as part of reporting in.
5. **Ask**: When in doubt, ask.


## PR Template

Use the following template for PR descriptions, adapting the specific changes:

```
This PR updates `package-name` to establish Python 3.10 as the minimum supported version, dropping support for Python 3.9 and below.

### Changes

* Configuration: Updated `setup.py` and `noxfile.py` to require Python 3.10+ and remove references to Python 3.7, 3.8, and 3.9.
* Cleanup: Removed dead code in `noxfile.py` that was skipping Python 3.7.

Fixes internal issue: http://b/482126936 🦕
```

## AI & LLM Assistant Guidelines for Verification
To safely perform an "after" scan across PR branches without switching branches, risking context poisoning, or polluting the working directory:
- **Use Git Worktrees**: Check out the feature branch into a parallel worktree (e.g., `git worktree add ../worktree-branch-name branch-name`).
- **Run Scanner from Main Branch**: Run the scanner script from your primary working directory, but point the scan path to the worktree directory (e.g., `-p ../worktree-branch-name/packages/package-name`).
- **Bypass Env Artifacts**: Worktrees only check out tracked files. This automatically avoids scanning `.nox/` or `.venv/` folders and sidesteps hundreds of false-positive hits from third-party packages.
- **Clean Up**: Once the scan confirms `0` results, remove the worktree using `git worktree remove ../worktree-branch-name`.

## Scale and Complexity

-   **Package Count:** ~20 packages.
-   **Change Volume:** 15 to 250 changes per package.
-   **Estimation:** Packages with fewer changes (mostly metadata and docs) can be processed quickly. Packages with compatibility code or complex test skips will take longer and require more care.

## Lessons Learned from Batch A (May 2026)

- **Docker Container Freshness:** The `python-multi` Docker container needs to be refreshed (`docker pull`) periodically to ensure it has all modern Python interpreters (e.g., Python 3.10) fully installed. 
- **Version-Specific Dependency Bugs:** Dependencies (like `aiohttp`, `pytz`) that are pinned to very old minimum bounds can cause `ImportError` or API failures on newer runtimes (e.g., `from collections import Mapping` failing on Python 3.10). When this occurs, bump the lower-bound in both `setup.py` and the lowest constraints file to the minimum version that safely supports the runtime.
- **Version Scanner Pragmas:** Use `# version-scanner: ignore` OR where needed, `version-scanner: ignore-next-line`to silence false-positives in the repository to maintain clean scan reports.
- **PR Description Files:** Format the PR body in a separate file and use `gh pr create --body-file` (along with `--head` and `--base`) to avoid interactive prompts and preserve all markdown formatting.
- **Scanner Globbing Support**: Discovered that the scanner initially used exact string matching for ignores. We updated it to use `fnmatch` to support shell-style wildcards (like `*.csv`) in `.scannerignore`.
- **False Positives in Data/Generated Files**: Data files (like `museum_art.csv`) and generated files (like `.coverage` and `package-lock.json`) can cause many false positives. They should be added to `.scannerignore` or categorized appropriately.

## Lessons Learned from Batch C (May 2026)

- **Pure Reflection for Constraints**: The constraints file for the lowest supported runtime (e.g., `constraints-3.10.txt`) should strictly match the minimum versions specified in `setup.py`. Avoid adding transitive dependencies to it.
- **Conflict Resolution via Bumping**: If testing with strict minimum constraints fails due to transitive dependency conflicts, the correct approach is to bump the minimum version of the *direct* dependency in `setup.py` that is pulling it in.
- **Setuptools and `pkg_resources`**: `setuptools >= 82.0.0` dropped `pkg_resources`. For older libraries that still rely on it, we must pin `setuptools < 81` (e.g., `79.0.0`) in the test constraints file to avoid both `ModuleNotFoundError` and deprecation warnings.
- **Targeted Test Runs**: When debugging a specific runtime failure (like Python 3.10), use `nox -s unit-3.10` to run only that session instead of the full suite. It saves a massive amount of time!

## Batched Packages by Complexity (Post-Assessment)

Based on the scan of remaining active packages (assessed for 3.7, 3.8, and 3.9 references on May 5, 2026), the following batches are proposed to conquer the remaining work.

> [!NOTE]
> The full package list file of active packages is stored in worktree `main`, branch `feat/add-version-scanner`, at `scripts/version_scanner/full_package_list.txt`.

### Batch 0 (Initial experiments and low hanging fruit):
- [x] `packages/gapic-generator`
- [x] `packages/proto-plus`
- [x] `packages/django-google-spanner`
- [x] `packages/google-auth-oauthlib`
- [x] `packages/google-auth-httplib2`
- [x] `packages/google-resumable-media`
- [x] `packages/pandas-gbq`
- [x] `packages/google-auth`
- [?] `packages/sqlalchemy-spanner` # Failing tests in PR. 

### Batch A: The "Trivial 4" 
- [x] `packages/google-cloud-runtimeconfig` (12 matches)
- [x] `packages/google-cloud-testutils` (13 matches)
- [x] `packages/bigquery-magics` (14 matches)
- [x] `packages/google-cloud-ndb` (15 matches)

### Batch B: The "Next 4" 
- [x] `packages/google-cloud-core` (16 matches)
- [x] `packages/google-cloud-dns` (16 matches)
- [x] `packages/google-crc32c` (17 matches)
- [x] `packages/sqlalchemy-bigquery` (23 matches)
  
### Batch C: The "Heavier 4"
- [~] `packages/db-dtypes` (25 matches) # Awaiting code review
- [~] `packages/google-cloud-documentai-toolbox` (28 matches) # Awaiting code review
- [~] `packages/google-api-core` (28 matches) # Awaiting code review
- [x] `packages/bigframes` (82 matches)

## Lessons Learned (2026-05-07)

- **Philosophy on Constraints & Warnings**: When dropping Python runtimes, avoid simply blocking warnings (like `ImportWarning` from `six` or `DeprecationWarning` from `pkg_resources`) by adding ignore rules. Instead, **bump the lower bounds** of dependencies to versions that do not trigger warnings on the new minimum supported runtime (e.g., 3.10+). This ensures a clean experience for customers who use strict warning filters in their own tests.
- **Bisect Strategy & Nox Optimization**: Automated bisection is highly effective for finding lowest workable dependency versions. To optimize time during install-heavy bisect experiments, we can abort tests early as soon as test collection succeeds and execution starts (dots appear).
- **Variable Package Structures**: Not all packages use constraints files in a `testing/` directory. Some use `pip-compile` with `requirements.in`/`.txt`. The migration process must adapt to these differences.
- **SQLAlchemy Transition**: For libraries supporting both SQLAlchemy 1.4 and 2.0, use environment variables like `SQLALCHEMY_SILENCE_UBER_WARNING=1` in specific Nox sessions (like `compliance_test_14`) to silence transition warnings without hiding them globally or affecting 2.0 sessions.

## Future Work

- **Scanner Pipeline Refactor**: A design doc for refactoring the version scanner to use a pipeline pattern for data enrichment is available at [scanner_pipeline_design.md](file:///usr/local/google/home/chalmerlowe/titan-src/projects/google-cloud-python/main/scripts/version_scanner/scanner_pipeline_design.md). We plan to implement this after completing the current EOL migration for all packages.
- **Multiple Dependencies and Versions Support**: Add the ability to provide a file with multiple dependencies and versions to scan for in a single run (e.g., scanning for both `python,3.9` and `protobuf,4.25.8`).

## Current Status & Next Steps (2026-05-07)

- **Today's Status**: 
  - Completed EOL drops for `google-api-core` (Batch C).
  - Resolved `six` warning conflicts and `pkg_resources` build failures by bumping lower bounds for `grpcio` and `requests`.
  - Addressed SQLAlchemy 2.0 warning in `sqlalchemy-spanner` by setting session-specific environment variable.
- **Next Steps**:
  - Complete the PR for `documentai-toolbox` by removing unnecessary `setuptools` references in Noxfile.

