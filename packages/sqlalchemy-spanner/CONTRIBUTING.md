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

## Code Reviews

All submissions, including submissions by project members, require review. We
use GitHub pull requests for this purpose. Consult
[GitHub Help](https://help.github.com/articles/about-pull-requests/) for more
information on using pull requests.

## Community Guidelines

This project follows [Google's Open Source Community
Guidelines](https://opensource.google/conduct/).

## Running tests

SQLAlchemy Spanner dialect includes a test suite, which can be executed both on a live service and Spanner emulator.

**Using pytest**
To execute the test suite with standard `pytest` package you only need to checkout to the package folder and run:
```
pytest -v
```

**Using nox**
The package includes a configuration file for `nox` package, which allows to execute the dialect test suite in an isolated virtual environment. To execute all the `nox` sessions checkout to the dialect folder and then run command:
```
nox
```
To execute only the dialect compliance test suite execute command:
```
nox -s compliance_test
```

**Live service**
To run the test suite on a live service use [setup.cfg](https://github.com/cloudspannerecosystem/python-spanner-sqlalchemy/blob/main/setup.cfg) `db.default` attribute to set URI of the project, instance and database, where the tests should be executed.

**Emulator**
As the dialect is built on top of the Spanner DB API, it also supports running on Spanner emulator. To make it happen you need to set an environment variable, pointing to the emulator service, for example `SPANNER_EMULATOR_HOST=localhost:9010`