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
        "docs/common.cfg",
        "presubmit/common.cfg",
        "build.sh",
    ],
)  # just move kokoro configs


assert 1 == s.replace(
    ".kokoro/docs/docs-presubmit.cfg",
    'value: "docs docfx"',
    'value: "docs"',
)

assert 1 == s.replace(
    ".kokoro/docker/docs/Dockerfile",
    """\
CMD \["python3\.8"\]""",
    """\
# Install gcloud SDK
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | \\
    tee -a /etc/apt/sources.list.d/google-cloud-sdk.list \\
  && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | \\
    apt-key --keyring /usr/share/keyrings/cloud.google.gpg  add - \\
  && apt-get update -y \\
  && apt-get install python2 google-cloud-sdk -y

CMD ["python3.8"]""",
)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
