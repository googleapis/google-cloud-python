The directory contains scripts which can be used to migrate client library code from
split repositories located at http://github.com/googleapis/python-* into this mono repository.

Below is a summary of the scripts:

- [git-migrate-history.sh](git-migrate-history.sh) will prepare a branch to migrate git history from a split repo to the monorepo.
- [split-repo-post-process.api-files.sh](split-repo-post-process.api-files.sh) will apply API specific changes needed for the monorepo migration as a post processing step.
- [split-repo-post-process.common-files.sh](split-repo-post-process.common-files.sh) will apply common changes needed for the monorepo migration as a post processing step.
- [delete-everything-split-repo.sh](delete-everything-split-repo.sh) will remove almost all files from a split repository and update the README.rst file to indicate that the repository is archived.
