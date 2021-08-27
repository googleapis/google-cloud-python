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

# Remove the replacements below once https://github.com/googleapis/synthtool/pull/1188 is merged

# Update googleapis/repo-automation-bots repo to main in .kokoro/*.sh files
s.replace(".kokoro/*.sh", "repo-automation-bots/tree/master", "repo-automation-bots/tree/main")

# Customize CONTRIBUTING.rst to replace master with main
s.replace(
    "CONTRIBUTING.rst",
    "fetch and merge changes from upstream into master",
    "fetch and merge changes from upstream into main",
)

s.replace(
    "CONTRIBUTING.rst",
    "git merge upstream/master",
    "git merge upstream/main",
)

s.replace(
    "CONTRIBUTING.rst",
    """export GOOGLE_CLOUD_TESTING_BRANCH=\"master\"""",
    """export GOOGLE_CLOUD_TESTING_BRANCH=\"main\"""",
)

s.replace(
    "CONTRIBUTING.rst",
    "remote \(``master``\)",
    "remote (``main``)",
)

s.replace(
    "CONTRIBUTING.rst",
    "blob/master/CONTRIBUTING.rst",
    "blob/main/CONTRIBUTING.rst",
)

s.replace(
    "CONTRIBUTING.rst",
    "blob/master/noxfile.py",
    "blob/main/noxfile.py",
)

s.replace(
    "docs/conf.py",
    "master_doc",
    "root_doc",
)

s.replace(
    "docs/conf.py",
    "# The master toctree document.",
    "# The root toctree document.",
)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
