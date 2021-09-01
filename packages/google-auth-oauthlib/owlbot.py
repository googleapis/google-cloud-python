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
    unit_test_python_versions=["3.6", "3.7", "3.8", "3.9"],
)
s.move(templated_files, excludes=[
    "docs/multiprocessing.rst"
])

# Change black paths
s.replace(
    "noxfile.py",
    """BLACK_PATHS =.*""",
    """BLACK_PATHS = ["docs", "google_auth_oauthlib", "tests", "noxfile.py", "setup.py"]""",
)

# Change flake8 paths
s.replace(
    "noxfile.py",
    'session.run\("flake8", "google", "tests"\)',
    'session.run("flake8", *BLACK_PATHS)',
)

s.replace(
    "noxfile.py",
    '"--cov=google/cloud",',
    '"--cov=google_auth_oauthlib",',
)

# Block pushing non-cloud libraries to Cloud RAD
s.replace(
    ".kokoro/docs/common.cfg",
    r'value: "docs-staging-v2"',
    r'value: "docs-staging-v2-staging"'
)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
