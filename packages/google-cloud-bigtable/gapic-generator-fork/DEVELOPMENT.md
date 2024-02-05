# Development

## Setup

1.  Clone this repo.

2.  Copy the Git pre-commit hooks. This will automatically check the build, run
    tests, and perform linting before each commit. (Symlinks don't seem to work,
    but if you find a way, please add it here!)

    ```sh
    cp .githooks/pre-commit .git/hooks/pre-commit
    ```

3.  Install dependencies with `pip install .`

## Unit Tests

Execute unit tests by running one of the sessions prefixed with `unit-`.

-   Example: `nox -s unit-3.8`
-   See all Nox sessions with `nox -l`.

## Formatting

-   Lint sources by running `autopep8`. The specific command is the following.

    ```
    find gapic tests -name "*.py" -not -path 'tests/**/goldens/*' | xargs autopep8 --diff --exit-code
    ```

-  Format sources in place:

    ```
    find gapic tests -name "*.py" -not -path 'tests/**/goldens/*' | xargs autopep8 --in-place
    ```

## Integration Tests

-   Run a single integration test for one API. This generates Python source code
    with the microgenerator and compares them to the golden files in
    `tests/integration/goldens/asset`.

    ```sh
    bazel test //tests/integration:asset
    ```

-   Run integration tests for all APIs.

    ```sh
    bazel test //tests/integration:all
    ```

-   Update all goldens files. This overwrites the golden files in
    `tests/integration/goldens/`.

    ```sh
    bazel run //tests/integration:asset_update
    bazel run //tests/integration:credentials_update
    bazel run //tests/integration:eventarc_update
    bazel run //tests/integration:logging_update
    bazel run //tests/integration:redis_update
    ```

