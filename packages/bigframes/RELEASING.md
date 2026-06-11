# Releasing BigQuery DataFrames (BigFrames) on GitHub

This onboarding documentation describes how to release a new version of the `bigframes` package.

---

## Why is this a manual step?
By default in this monorepo, BigQuery DataFrames releases are marked with `skip_release: true`. This prevents automatic release pipelines from triggering on every commit. Instead, a library maintainer must explicitly trigger the release staging process using the `legacylibrarian` tool.

---

## Quick Onboarding Checklist (First Time Only)

1.  **Install the legacylibrarian CLI tool**:
    ```bash
    go install github.com/googleapis/librarian/cmd/legacylibrarian@latest
    ```
    *(Ensure `~/go/bin` is in your system `PATH`)*.

2.  **Authenticate with GitHub CLI**:
    Ensure the `gh` tool is installed and logged in:
    ```bash
    gh auth login
    ```

---

## How to Trigger a Release

Follow these general steps to release a new version (e.g., `X.X.X`):

1.  **Set your GitHub Auth Token**:
    ```bash
    export LIBRARIAN_GITHUB_TOKEN=$(gh auth token)
    ```

2.  **Checkout the main branch**:
    ```bash
    git fetch origin main && git checkout origin/main
    ```

3.  **Run the staging command with push**:
    ```bash
    legacylibrarian release stage \
      --repo=https://github.com/googleapis/google-cloud-python \
      --library=bigframes \
      --library-version=X.X.X \
      --push
    ```
    *   This automatically clones the repo in a temp folder, updates version references, creates a commit, pushes the release branch, and generates a Pull Request on GitHub.
    *   Review the generated PR on GitHub, verify the `release:pending` label, and squash-merge it once tests pass.

---

## Detailed Step-by-Step & Troubleshooting

For the detailed step-by-step cheatsheet, including troubleshooting common errors like:
*   Context-Aware Access (CAA) credential blocks
*   Git `insteadOf` redirection errors in `~/.gitconfig`
*   `go-git` cleanliness errors caused by local `.vscode/` or `venv` directories

Refer to the cheat-sheet document:
👉 **[packages/bigframes/release-procedure.md](file:///usr/local/google/home/shuowei/src/google-cloud-python/google-cloud-python/packages/bigframes/release-procedure.md)**
