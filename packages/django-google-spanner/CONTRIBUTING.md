# How to Contribute

We'd love to accept your patches and contributions to this project. There are
just a few small guidelines you need to follow.

## Contributor License Agreement

Contributions to this project must be accompanied by a Contributor License
Agreement. You (or your employer) retain the copyright to your contribution;
this simply gives us permission to use and redistribute your contributions as
part of the project. Head over to <https://cla.developers.google.com/> to see
your current agreements on file or to sign a new one.

You generally only need to submit a CLA once, so if you've already submitted one
(even if it was for a different project), you probably don't need to do it
again.

## Code reviews

All submissions, including submissions by project members, require review. We
use GitHub pull requests for this purpose. Consult
[GitHub Help](https://help.github.com/articles/about-pull-requests/) for more
information on using pull requests.

## Community Guidelines

This project follows [Google's Open Source Community
Guidelines](https://opensource.google/conduct/).

## Tests

### Functional tests
We have functional tests for individual components that can be run by
```shell
tox
```

### Django integration tests
We run full integration tests with continuous integration on Google Cloud Build with Kokoro.

The tests to be run are specified in file [django_test_apps.txt](./django_test_apps.txt)

There are 2 ways to run the tests:

#### django_test_suite.sh

This method requires an already existing Cloud Spanner instance.
Expected environment variables:

##### Environment variables
Variable|Description|Comment
---|---|---
`GOOGLE_APPLICATION_CREDENTIALS`|The Google Application Credentials file|For example `GOOGLE_APPLICATION_CREDENTIALS=~/Downloads/creds.json`
`PROJECT_ID`|The project id of the Google Application credentials being used|For example `PROJECT_ID=appdev-soda-spanner-staging`
`DJANGO_TEST_APPS`|The Django test suite apps to run|For example `DJANGO_TEST_APPS="basic i18n admin_views"`
`SPANNER_TEST_INSTANCE`|The Cloud Spanner instance to use, it MUST exist before running tests|For example `SPANNER_TEST_INSTANCE="django-tests"`
`DJANGO_TESTS_DIR`|The directory into which Django has been cloned to run the test suite|For example `DJANGO_TESTS_DIR=django_tests`

##### Example run
```shell
GOOGLE_APPLICATION_CREDENTIALS=~/Downloads/creds.json \
PROJECT_ID=appdev-soda DJANGO_TEST_APPS="expressions i18n" \
SPANNER_TEST_INSTANCE=django-tests ./django_tests_suite.sh
```

#### Parallelization script

This method shards tests over multiple builds, and over available cores.

##### Environment variables
To run the tests locally, you'll need the following environment variables.

Variable|Description|Comment
---|---|---
`GOOGLE_APPLICATION_CREDENTIALS`|The Google Application Credentials file|For example `GOOGLE_APPLICATION_CREDENTIALS=~/Downloads/creds.json`
`PROJECT_ID`|The project id of the Google Application credentials being used|For example `PROJECT_ID=appdev-soda-spanner-staging`
`DJANGO_WORKER_COUNT`|The number of parallel jobs to split the tests amongst|To get all the tests run by one process, use a cout of 1, so `DJANGO_WORKER_COUNT=1`
`DJANGO_WORKER_INDEX`|The zero based index of the parallel job number, to run tests, it is correlated with `DJANGO_WORKER_COUNT` and an offset to figure out  which tests to run with this job|
`django_test_apps.txt`|The listing of Django apps to run|Set the apps you'd like to be run in parallel

##### Example run
```shell
GOOGLE_APPLICATION_CREDENTIALS=~/Downloads/creds.json \
PROJECT_ID=appdev-soda DJANGO_TEST_APPS="expressions i18n" \
DJANGO_WORKER_COUNT=1 DJANGO_WORKER_INDEX=0SPANNER_TEST_INSTANCE=django-tests ./bin/parallelize_tests_linux
```
