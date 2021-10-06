import synthtool as s
from synthtool import gcp
from synthtool.languages import python

AUTOSYNTH_MULTIPLE_PRS = True

common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(unit_cov_level=100, cov_level=100)
python.py_samples(skip_readmes=True)
s.move(templated_files / '.kokoro')  # just move kokoro configs
s.move(templated_files / '.trampolinerc')

s.replace([".kokoro/publish-docs.sh", ".kokoro/build.sh"], "cd github/python-ndb", 
"""cd github/python-ndb

# Need enchant for spell check
sudo apt-get update
sudo apt-get -y install dictionaries-common aspell aspell-en \\
                        hunspell-en-us libenchant1c2a enchant""")

s.replace(".kokoro/build.sh", """(export PROJECT_ID=.*)""", """\g<1>

if [[ -f "${KOKORO_GFILE_DIR}/service-account.json" ]]; then
  # Configure local Redis to be used
  export REDIS_CACHE_URL=redis://localhost
  redis-server &

  # Configure local memcached to be used
  export MEMCACHED_HOSTS=127.0.0.1
  service memcached start

  # Some system tests require indexes. Use gcloud to create them.
  gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS --project=$PROJECT_ID
  gcloud --quiet --verbosity=debug datastore indexes create tests/system/index.yaml
fi
""")

s.replace(".kokoro/build.sh", 
  """# Setup service account credentials.
export GOOGLE_APPLICATION_CREDENTIALS=\$\{KOKORO_GFILE_DIR\}/service-account.json""",
  """if [[ -f "${KOKORO_GFILE_DIR}/service-account.json" ]]; then
  # Setup service account credentials.
  export GOOGLE_APPLICATION_CREDENTIALS=${KOKORO_GFILE_DIR}/service-account.json
fi"""
)

s.replace(
    ".kokoro/docker/docs/Dockerfile",
    "libsqlite3-dev.*\n",
    "\g<0>    memcached \\\n"\
)

s.replace(
    ".kokoro/docker/docs/Dockerfile",
    "# Install dependencies.\n",
    """\g<0># Spell check related
RUN apt-get update && apt-get install -y dictionaries-common aspell aspell-en \\
  hunspell-en-us libenchant1c2a enchant
"""
)

assert 1 == s.replace(
    ".kokoro/docs/docs-presubmit.cfg",
    'value: "docs docfx"',
    'value: "docs"',
)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
