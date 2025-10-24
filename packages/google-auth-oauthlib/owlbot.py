import synthtool as s
from synthtool import gcp

common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    microgenerator=True,
    cov_level=99,
    unit_test_external_dependencies=["click"],
    unit_test_python_versions=["3.7", "3.8", "3.9", "3.10", "3.11", "3.12", "3.13"],
    default_python_version="3.10",
)
s.move(templated_files, excludes=[
    "docs/multiprocessing.rst",
    "README.rst",
    "noxfile.py",
    ".kokoro/samples/**", # this repository has no samples
])

# Change black paths
s.replace(
    "noxfile.py",
    """LINT_PATHS =.*""",
    """LINT_PATHS = ["docs", "google_auth_oauthlib", "tests", "noxfile.py", "setup.py"]""",
)

# Change flake8 paths
s.replace(
    "noxfile.py",
    'session.run\("flake8", "google", "tests"\)',
    'session.run("flake8", *LINT_PATHS)',
)

s.replace(
    "noxfile.py",
    '"--cov=google",',
    '"--cov=google_auth_oauthlib",',
)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
