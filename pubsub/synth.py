# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This script is used to synthesize generated parts of this library."""

import re
import textwrap

import synthtool as s
from synthtool import gcp

gapic = gcp.GAPICGenerator()
common = gcp.CommonTemplates()
version = "v1"

# ----------------------------------------------------------------------------
# Generate pubsub GAPIC layer
# ----------------------------------------------------------------------------
library = gapic.py_library(
    "pubsub",
    version,
    config_path="/google/pubsub/artman_pubsub.yaml",
    include_protos=True,
)
s.move(
    library,
    excludes=[
        "docs/**/*",
        "nox.py",
        "README.rst",
        "setup.py",
        "google/cloud/pubsub_v1/__init__.py",
        "google/cloud/pubsub_v1/types.py",
    ],
)

# Adjust tests to import the clients directly.
s.replace(
    "tests/unit/gapic/v1/test_publisher_client_v1.py",
    "from google.cloud import pubsub_v1",
    "from google.cloud.pubsub_v1.gapic import publisher_client",
)

s.replace(
    "tests/unit/gapic/v1/test_publisher_client_v1.py", " pubsub_v1", " publisher_client"
)

s.replace(
    "tests/unit/gapic/v1/test_subscriber_client_v1.py",
    "from google.cloud import pubsub_v1",
    "from google.cloud.pubsub_v1.gapic import subscriber_client",
)

s.replace(
    "tests/unit/gapic/v1/test_subscriber_client_v1.py",
    " pubsub_v1",
    " subscriber_client",
)

# DEFAULT SCOPES are being used. so let's force them in.
s.replace(
    "google/cloud/pubsub_v1/gapic/*er_client.py",
    "# The name of the interface for this client. This is the key used to",
    """# The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _DEFAULT_SCOPES = (
        'https://www.googleapis.com/auth/cloud-platform',
        'https://www.googleapis.com/auth/pubsub', )

    \g<0>""",
)

s.replace(
    "google/cloud/pubsub_v1/gapic/publisher_client.py",
    "import google.api_core.gapic_v1.method\n",
    "\g<0>import google.api_core.path_template\n",
)

# Doc strings are formatted poorly
s.replace(
    "google/cloud/pubsub_v1/proto/pubsub_pb2.py",
    'DESCRIPTOR = _MESSAGESTORAGEPOLICY,\n\s+__module__.*\n\s+,\n\s+__doc__ = """',
    "\g<0>A message storage policy.\n\n\n    ",
)

s.replace(
    "google/cloud/pubsub_v1/gapic/subscriber_client.py",
    "subscription \(str\): The subscription whose backlog .*\n(.*\n)+?"
    "\s+Format is .*",
    """subscription (str): The subscription whose backlog the snapshot retains.
                Specifically, the created snapshot is guaranteed to retain: \\
                 (a) The existing backlog on the subscription. More precisely, this is \\
                     defined as the messages in the subscription's backlog that are \\
                     unacknowledged upon the successful completion of the \\
                     `CreateSnapshot` request; as well as: \\
                 (b) Any messages published to the subscription's topic following the \\
                     successful completion of the CreateSnapshot request. \\

                Format is ``projects/{project}/subscriptions/{sub}``.""",
)

s.replace(
    "google/cloud/pubsub_v1/gapic/publisher_client.py",
    "import functools\n",
    "import collections\n"
    "from copy import deepcopy\n\g<0>"
)

s.replace(
    "google/cloud/pubsub_v1/gapic/publisher_client.py",
    "import pkg_resources\n",
    "\g<0>import six\n"
)

s.replace(
    "google/cloud/pubsub_v1/gapic/publisher_client.py",
    "class PublisherClient",
    """# TODO: remove conditional import after Python 2 support is dropped
if six.PY3:
    from collections.abc import Mapping
else:
    from collections import Mapping
    

def _merge_dict(d1, d2):
    # Modifies d1 in-place to take values from d2
    # if the nested keys from d2 are present in d1.
    # https://stackoverflow.com/a/10704003/4488789
    for k, v2 in d2.items():
        v1 = d1.get(k) # returns None if v1 has no such key
        if v1 is None:
            raise Exception("{} is not recognized by client_config".format(k))
        if isinstance(v1, Mapping) and isinstance(v2, Mapping):
            _merge_dict(v1, v2)
        else:
            d1[k] = v2
    return d1
    \n\n\g<0>"""
)

s.replace(
    "google/cloud/pubsub_v1/gapic/publisher_client.py",
    "client_config \(dict\): DEPRECATED.",
    "client_config (dict):"
)

s.replace(
    "google/cloud/pubsub_v1/gapic/publisher_client.py",
    "# Raise deprecation warnings .*\n.*\n.*\n.*\n.*\n.*\n",
    """default_client_config = deepcopy(publisher_client_config.config)

        if client_config is None:
            client_config = default_client_config
        else:
            client_config = _merge_dict(default_client_config, client_config)
    """
)

s.replace(
    "google/cloud/pubsub_v1/gapic/publisher_client.py",
    "~google.api_core.page_iterator.PageIterator",
    "~google.api_core.page_iterator.GRPCIterator"
)

s.replace(
    "google/cloud/pubsub_v1/gapic/subscriber_client.py",
    "~google.api_core.page_iterator.PageIterator",
    "~google.api_core.page_iterator.GRPCIterator"
)

# Temporary fixup for 'grpc-google-iam-vi 0.12.4' (before generation).
s.replace(
    "google/cloud/pubsub_v1/gapic/transports/*_grpc_transport.py",
    "from google.iam.v1 import iam_policy_pb2",
    "from google.iam.v1 import iam_policy_pb2_grpc as iam_policy_pb2",
)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = gcp.CommonTemplates().py_library(unit_cov_level=97, cov_level=100)
s.move(templated_files)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
