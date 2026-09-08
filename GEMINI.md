# Google Cloud Python Workspace Rules

These guidelines are automatically applied to Python development tasks within this repository.

---

## 1. Filesystem and Path Resolution
* **Dynamic Configuration Directories:** Never hardcode paths like `~/.config/gcloud/` or standard user directories. Always utilize existing SDK helpers (such as `_cloud_sdk.get_config_path()`) to dynamically locate system and configuration files.
* **Path Normalization:** When comparing path strings (especially paths retrieved from environment variables or dynamically built), always normalize them using `os.path.normpath` or `pathlib.Path` to prevent Windows vs Unix slash mismatch issues (`\` vs `/`).

## 2. Input Validation (Defensive Programming)
* **Untrusted File Inputs:** Any data loaded from external configuration files (JSON, YAML, CSV) is untrusted. Always type-validate structure (e.g. check `isinstance(data, dict)` and `isinstance(data.get("sub_key"), dict)`) *before* indexing or calling dictionary lookup keys, avoiding `TypeError` exceptions.

## 3. Exception Contract Compliance
* **Public Interface Contracts:** When introducing new exception pathways in internal helpers, always trace their propagation. If a public-facing API method (e.g. `refresh()`) is documented to raise a specific base exception class (like `RefreshError`), wrap lower-level custom exceptions (like `ClientCertError`) or system exceptions (like `OSError`) and re-raise them under the correct interface exception types.
* **Self-Contained Fallbacks:** Fallback logic must be resilient and self-contained. Always wrap fallback configuration loading in try-except blocks to catch expected exceptions (like `ClientCertError` or `OSError`) and bypass failures gracefully.

## 4. Unit Testing and Mock Hygiene
* **Localized Mocking:** When mocking standard functions or filesystem checks (like `path.exists`), mock the local module import path (e.g., `google.auth.transport._mtls_helper.path.exists`) instead of patching builtins globally (e.g., `os.path.exists`), ensuring mocks are isolated.
* **Fallback Verification:** Fallback test cases must explicitly verify execution flow by asserting the expected call sequence and arguments of mocked helpers using `assert_called_once_with` or `assert_has_calls`.
