# Copyright 2019 Google LLC
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

import synthtool as s
from synthtool import gcp

gapic = gcp.GAPICMicrogenerator()
versions = ["v1beta1"]
common = gcp.CommonTemplates()


# ----------------------------------------------------------------------------
# Generate Cloud Recommender
# ----------------------------------------------------------------------------
for version in versions:
    library = gapic.py_library(
        "recommender", version, proto_path=f"google/cloud/recommender/{version}",
    )
    s.move(library, excludes="noxfile.py")

# https://github.com/googleapis/gapic-generator-python/pull/175
s.replace("google/cloud/**/*.py",
""",
(\s+)\) ->""",
"""
\g<1>) ->""")

# Fix lint errors about unused variables in tests
# TODO: Add GitHub issue here
s.replace("tests/**/test_recommender.py",
"""(\s+)call\.return_value = recommender_service\.ListRecommendationsResponse\(\)
(\s+)response = client\.list_recommendations\(request\)""",
"""\g<1>call.return_value = recommender_service.ListRecommendationsResponse()
\g<2>client.list_recommendations(request)""")

s.replace("tests/**/test_recommender.py",
"""(\s+)call\.return_value = recommendation\.Recommendation\(\)
(\s+)response = client\.get_recommendation\(request\)""",
"""\g<1>call.return_value = recommendation.Recommendation()
\g<2>client.get_recomemndation(request)""")


s.replace("tests/**/test_recommender.py",
"""(\s+)with pytest\.raises\(ValueError\):
(\s+)client = Recommender\(
(\s+)credentials=credentials\.AnonymousCredentials\(\),
(\s+)transport=transport,
(\s+)\)
""",
"""\g<1>with pytest.raises(ValueError):
\g<2>Recommender(
\g<3>credentials=credentials.AnonymousCredentials(),
\g<4>transport=transport
\g<5>)
""")

s.replace("tests/**/test_recommender.py",
"""(\s+)client = Recommender\(\)
(\s+)adc\.assert_called_once_with\(""",
"""\g<1>Recommender()
\g<2>adc.assert_called_once_with(""")

# Fix formatting in docstring
s.replace("google/cloud/**/recommendation.py",
"""(Example:\s+\{.+?\})""",
"""``\g<1>``""", flags=re.DOTALL)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(unit_cov_level=97, cov_level=100)
s.move(templated_files, excludes=["noxfile.py"])

s.shell.run(["nox", "-s", "blacken"], hide_output=False) 