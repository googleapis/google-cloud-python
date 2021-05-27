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
    find gapic tests -name "*.py" -not -path 'tests/integration/goldens/*' | xargs autopep8 --diff --exit-code
    ```

## Integration Tests

-   Run a single integration test for one API. This generates Python source code
    with the microgenerator and compares them to the golden files in
    `test/integration/goldens/asset`.

    ```sh
    bazel test //test/integration:asset
    ```

-   Update goldens files. This overwrites the golden files in
    `test/integration/goldens/asset`.

    ```sh
    bazel run //test/integration:asset_update
    ```