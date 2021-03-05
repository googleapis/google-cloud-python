# Logging Environment Tests

This repo was designed to be run as a [submodule](https://git-scm.com/book/en/v2/Git-Tools-Submodules) of the GCP Logging repositories.
It contains common tests to ensure behavioral consistency across languages and GCP platforms.

## Usage

These tests were implemented in [pytest](https://docs.pytest.org/en/stable/) triggered by [nox](https://nox.thea.codes/en/stable/)

Run the full suite of tests:

```
nox -s tests
```

Run a specific test:

```
nox --session "tests(language='python', platform='cloudrun')"
```

By default, each test will tear down and re-create the GCP environment to ensure a clean environment.
To re-use an existing environment while debugging, set the `NO_CLEAN` flag before running tests:

```
export NO_CLEAN=true
```

To allow parallel runs, envctl appends an id to each deployed resource. By default, this will be the runner's `hostname`,
but it can be customized by setting `ENVCTL_ID`

## Architecture

### deployable/

The Deployable is a frankenstein-like package of code that can be deployed to any supported GCP environment. 
It contains a pub/sub listener, and a set of snippets that can be triggered by pub/sub messages. In this way,
it allows us to trigger the same code in every GCP environment for consistency checks.

### envctl/

*envctl* is a command line tool that allows us to spin up and down deployments in an automated way.
It should accept three arguments: a language, a GCP environment name, and an action. 
*envctl* can be used to spin up and down test environments in a simple, reproducible way.

Implementation code for each language/environment pair can be found in `envctl/env_scripts`

*envctl* exposes the following sub-commands:
- `envctl <language> <environment> deploy`
  - deploys a fresh environment
- `envctl <language> <environment> verify`
  - verifies that an environment is up (returns true/false)
- `envctl <language> <environment> destroy`
  - destroys an existing environment
- `envctl <language> <environment> trigger <snippet> <optional arguments>`
  - sends a pub/sub message to trigger a snippet in an environment
  - optional arguments are embedded as [custom attributes](https://cloud.google.com/pubsub/docs/publisher#using_attributes) in Pub/Sub messages
- `envctl <language> <environment> filter-string`
  - returns a filter that finds logs created by the environment
- `envctl <language> <environment> logs`
  - returns a list of recent logs from the environment

### tests/

Contains the pytest code that tests each environment. Common logic is stored as abstract super-classes in `tests/common`.
Concrete implementations for each environment can be found in `tests/<language>/test_<environment>.py`. 
Test files in `tests/<language>` can inherit from any file in `tests/common` logic as needed, in order to share test logic between environments.

### Shared Tests

| Test Name      | Optional Input       | Description                      |
| -------------- | ----------------     | -------------------------------- |
| `simplelog`    | `logname`, `logtext` |  Logs a simple text payload      |
| `standardlog`  | `logname`, `logtext` |  Logs a simple text payload using a standard library wrapper |
