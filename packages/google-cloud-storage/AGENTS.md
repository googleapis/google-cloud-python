# Google Cloud Storage Python Client: Project Structure and Automation

This document provides a comprehensive summary of the project structure, testing conventions, CI workflows, and developer automation for the `google-cloud-storage` client library.

## Analysis of `google-cloud-storage` Package

### 1. Testing Conventions
- **Framework:** `pytest` (leveraging plugins such as `pytest-cov`, `pytest-asyncio`, `pytest-xdist`, `pytest-rerunfailures`, `pytest-benchmark`, `pytest-timeout`, and `pytest-subtests`).
- **Environment & Isolation:** `nox` is used to manage isolated virtual environments and orchestrate test sessions.
- **Test Categories:**
  - **Unit Tests:** Fast, isolated tests mocking external calls. Tested across multiple Python versions and both `python` and `upb` Protocol Buffer implementations.
  - **System Tests:** End-to-end integration tests requiring live Google Cloud projects, credentials, and resources (GCS buckets, Pub/Sub, KMS, IAM). Supports retry logic for flake mitigation.
  - **Conformance Tests:** Shared cross-language conformance suites covering retry behavior and bi-directional gRPC streaming.
  - **Zonal VM Tests:** Specialized integration tests verifying rapid storage and zonal bucket features, executed within dedicated Compute Engine (GCE) VMs.

### 2. Placement of Tests
- **Unit Tests:** Located in `tests/unit/` and `tests/resumable_media/unit/`.
- **System Tests:** Located in `tests/system/` and `tests/resumable_media/system/`.
- **Conformance Tests:** Located in `tests/conformance/` (e.g., `test_conformance.py`, `test_bidi_reads.py`, `test_bidi_writes.py`).
- **Zonal Integration Tests:** Located in `tests/system/test_zonal.py`.

### 3. Dependency Management
- **Constraints & Lower Bounds:** Dependency versions are constrained via files in `testing/constraints-*.txt`. Lower bounds are validated using automated tools (`lower-bound-checker`).
- **Automated Bot Management:** Dependencies are actively maintained by automation (e.g., Renovate). Manual modifications to constraint files should be avoided unless updating specific test requirements or adding new dependencies.

---

## CI Workflows & Agent Instructions

Agents and developers should use the following instructions and commands to understand and replicate CI workflows for the `google-cloud-storage` package.

### 1. Prerequisites for Live Infrastructure Tests
To run system, conformance, or zonal tests, ensure the following environment variables are set:
- `GOOGLE_CLOUD_PROJECT` (or `PROJECT_ID`)
- `GOOGLE_APPLICATION_CREDENTIALS` (absolute path to a valid service account JSON key)

### 2. GitHub Actions CI (Presubmit & Merge Queue)
GitHub Actions orchestrates unit and specialized tests via `ci/run_conditional_tests.sh` and `ci/run_single_test.sh`.
- **Unit Tests Matrix:** Runs across Python versions 3.9 through 3.14.
  ```bash
  nox -s unit-<version>
  ```
- **Prerelease Dependencies:** Verifies compatibility with pre-release versions of core libraries (`google-api-core`, `protobuf`, etc.).
  ```bash
  nox -s prerelease_deps-3.14
  ```
- **Core Dependencies from Source:** Verifies compatibility against the `main` branch of upstream repositories (e.g., `google-auth`, `google-api-core`).
  ```bash
  nox -s core_deps_from_source-3.14
  ```

### 3. Kokoro CI (Continuous & Presubmit Integration)
Kokoro CI runs continuous and presubmit system tests across affected packages using `.kokoro/system.sh` and `.kokoro/system-single.sh`.
- **System Tests:** Replicates the Kokoro integration build:
  ```bash
  nox -s system-3.12
  ```

### 4. Cloud Build (Zonal VM Integration Tests)
Cloud Build executes `cloudbuild/zb-system-tests-cloudbuild.yaml` to test zonal buckets and rapid storage features:
1. Provisions an `e2-medium` GCE VM running Debian 13 in the target zone.
2. Sets high OS limits (`ulimit -n 10000`) to support intensive gRPC bi-directional streaming.
3. Clones the repository, sets up a virtual environment, and installs dependencies via `cloudbuild/run_zonal_tests.sh`.
4. Executes zonal tests:
   ```bash
   pytest -vv -s tests/system/test_zonal.py
   ```
5. Automatically tears down the GCE VM upon completion.

---

## Automation & Developer Workflows

### Nox Commands

Developers and agents can invoke `nox` directly within the `packages/google-cloud-storage` directory to perform local verification:

- **Run Unit Tests:**
  ```bash
  nox -s unit-3.12
  ```
- **Run System Tests:**
  ```bash
  nox -s system-3.12
  ```
- **Run Conformance Tests:**
  ```bash
  nox -s system-3.12 -- conformance
  ```
- **Run Bi-directional Streaming Conformance Tests:**
  ```bash
  nox -s system-3.12 -- conformance_bidi
  ```
- **Run Linting & Style Checks (Flake8 & Ruff):**
  ```bash
  nox -s lint
  ```
- **Auto-format Code & Sort Imports (Ruff):**
  ```bash
  nox -s format
  ```
- **Verify `setup.py` & RST Documentation:**
  ```bash
  nox -s lint_setup_py
  ```
- **Generate 100% Aggregate Code Coverage:**
  ```bash
  nox -s cover
  ```
- **Build Sphinx HTML Documentation:**
  ```bash
  nox -s docs
  ```
