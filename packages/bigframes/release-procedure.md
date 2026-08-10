# BigQuery DataFrames (bigframes) release procedure

*(Note: bigframes releases are marked with `skip_release: true` in `librarian.yaml` and must be kicked off manually using legacylibrarian.)*

## Setup (First Time Only)

*   Install `legacylibrarian`:

        go install github.com/googleapis/librarian/cmd/legacylibrarian@latest

*   Authenticate with GitHub CLI:

        gh auth login

## Release Steps

*   Obtain GitHub token:

        export LIBRARIAN_GITHUB_TOKEN=$(gh auth token)

*   Stash changes (repo must be clean):

        git stash -u

*   Fetch and checkout base:

        git fetch origin main
        git fetch origin --tags
        git checkout origin/main

*   Check image updates:

        legacylibrarian update-image --push

*   Create release PR:

        # Option A: Push directly
        legacylibrarian release stage --repo=https://github.com/googleapis/google-cloud-python --library=bigframes --library-version=X.X.X --push

        # Option B: Manual edit first (omit --push, edit files in /tmp/librarian-*, commit/push from there)
        legacylibrarian release stage --repo=https://github.com/googleapis/google-cloud-python --library=bigframes --library-version=X.X.X
        # In /tmp repository:
        git commit -a -m "chore: create release" --no-verify  # keep librarian config pristine
        git push origin HEAD
        gh pr create --fill --label "release:pending"

*   Post-release restore:

        # Move back any stashed/relocated files (like .vscode)
        git checkout main
        git stash pop
