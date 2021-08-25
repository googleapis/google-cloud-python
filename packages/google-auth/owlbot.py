import synthtool as s
from synthtool import gcp

common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(unit_cov_level=100, cov_level=100)


s.move(
    templated_files / ".kokoro",
    excludes=[
        "continuous/common.cfg",
        "presubmit/common.cfg",
        "build.sh",
    ],
)  # just move kokoro configs


assert 1 == s.replace(
    ".kokoro/docs/docs-presubmit.cfg",
    'value: "docs docfx"',
    'value: "docs"',
)

# Remove the replacement below once https://github.com/googleapis/synthtool/pull/1188 is merged

# Update googleapis/repo-automation-bots repo to main in .kokoro/*.sh files
assert 1 == s.replace(".kokoro/*.sh", "repo-automation-bots/tree/master", "repo-automation-bots/tree/main")

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
