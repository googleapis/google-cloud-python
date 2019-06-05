import nox


@nox.session(python="3.6")
def cover(session):
    session.install("mock", "pytest", "pytest-cov", "futures", "click")
    session.install(".")
    session.run(
        "py.test", "--cov=google_auth_oauthlib", "--cov=tests", "--cov-report=", "tests"
    )
    session.run("coverage", "report", "--show-missing", "--fail-under=100")


@nox.session(python="3.6")
def docgen(session):
    session.env["SPHINX_APIDOC_OPTIONS"] = "members,inherited-members,show-inheritance"
    session.install("mock", "pytest", "pytest-cov", "futures", "click", "sphinx")
    session.install(".")
    session.run("rm", "-rf", "docs/reference")
    session.run(
        "sphinx-apidoc",
        "--output-dir",
        "docs/reference",
        "--separate",
        "--module-first",
        "google_auth_oauthlib",
    )


@nox.session(python="3.6")
def docs(session):
    session.install("sphinx", "-r", "docs/requirements-docs.txt")
    session.install(".")
    session.run("make", "-C", "docs", "html")


@nox.session(python="3.5")
def lint(session):
    session.install(
        "flake8",
        "flake8-import-order",
        "pylint",
        "docutils",
        "gcp-devrel-py-tools>=0.0.3",
    )
    session.install(".")
    session.run(
        "python", "setup.py", "check", "--metadata", "--restructuredtext", "--strict"
    )
    session.run(
        "flake8",
        "--import-order-style=google",
        "--application-import-names=google_auth_oauthlib,tests",
        "google_auth_oauthlib",
        "tests",
    )
    session.run(
        "gcp-devrel-py-tools",
        "run-pylint",
        "--config",
        "pylint.config.py",
        "--library-filesets",
        "google_auth_oauthlib",
        "--test-filesets",
        "tests",
    )


@nox.session(python=["2.7", "3.5", "3.6", "3.7", "pypy"])
def test(session):
    session.install("mock", "pytest", "pytest-cov", "futures", "click")
    session.install(".")
    session.run("py.test", "--cov=google_auth_oauthlib", "--cov=tests", "tests")
