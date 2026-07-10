# Mypy Activation Readiness Plan 🏴󠁧󠁢󠁳󠁣󠁴󠁿

This plan outlines the steps to ensure all libraries in PR #17409 are prepared for easy Mypy activation. The goal is to have the `def mypy(session):` block fully populated with installation logic and the centralized `session.run` command, but kept inactive via `session.skip()` or commented-out code.

## 📋 Current State Summary
- All PR files have `MYPY_CONFIG_FILE` defined.
- Several packages (`logging`, `storage`, `proto-plus`, etc.) are skipped but **lack the session boilerplate** (installations + `session.run`).
- Some packages are heavily modified by **Client Post-Processing** (YAMLs), meaning direct edits to `noxfile.py` will be clobbered.

---

## 🛠️ Action Plan

### Phase 1: Update Post-Processing YAMLs (Managed Handwritten Libraries)
For libraries whose `noxfile.py` is generated or heavily modified by pipeline scripts, we must update the YAML files in `.librarian/generator-input/client-post-processing/`.

#### 1. `google-cloud-logging`
- **File**: `logging-integration.yaml`
- **Current**: Replaces the session body with `session.skip(...)`.
- **Target**: Update the `after:` block to include standard Mypy installations and the `session.run` command (pointing to `MYPY_CONFIG_FILE`), with `session.skip` at the top of the body.

#### 2. `google-cloud-storage`
- **File**: `storage-integration.yaml`
- **Current**: Replaces the session body with `session.skip(...)`.
- **Target**: Same as logging. Inject full boilerplate below the skip.

#### 3. `google-cloud-pubsub`
- **File**: `pubsub-integration.yaml`
- **Current**: Has boilerplate, but `session.run` is commented out.
- **Target**: Keep commented out as requested (to respect convention), but ensure it uses `{MYPY_CONFIG_FILE}`. (✅ *Already updated in previous step*).

#### 4. `google-cloud-bigtable`
- **File**: `bigtable-integration.yaml`
- **Current**: Heavily customized, active session.
- **Target**: Ensure it uses `{MYPY_CONFIG_FILE}`. (✅ *Already updated in previous step*).

---

### Phase 2: Update Static Handwritten Libraries (No Post-Processing)
For libraries that are purely handwritten and not touched by the Librarian pipeline, we can edit `noxfile.py` directly.

#### 1. `proto-plus`
- Populate `def mypy(session):` with standard installations and `session.run("mypy", f"--config-file={MYPY_CONFIG_FILE}", ...)` below the `session.skip` call.

#### 2. `bigquery-magics`
- Populate session with boilerplate below `session.skip`.

#### 3. `django-google-spanner`
- Populate session with boilerplate below `session.skip`.

#### 4. `gcp-sphinx-docfx-yaml`
- Populate session with boilerplate below `session.skip`.

---

### Phase 3: Verification
1. Run `nox -s mypy` (or equivalent) in a couple of updated packages to verify they skip correctly.
2. Verify the `MYPY_CONFIG_FILE` path is correctly derived in various execution contexts (monorepo root vs package dir).

---

> [!TIP]
> **Enabling Mypy Later**: Once this plan is executed, turning on Mypy for any of these packages is as simple as removing the `session.skip()` line or uncommenting the `session.run` command in the respective YAML or `noxfile.py`.
