# Copyright 2022 Google LLC
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

from pathlib import Path

import synthtool as s
import synthtool.gcp as gcp
from synthtool.languages import python

# ----------------------------------------------------------------------------
# Copy the generated client from the owl-bot staging directory
# ----------------------------------------------------------------------------

default_version = "v1"

for library in s.get_staging_dirs(default_version):
    # fix docstring formatting. See cl/435620538
    s.replace(
        library / "google/cloud/optimization_v1/types/fleet_routing.py",
        """.. code:: start_time\(previous_visit\)

               travel_duration\(previous_visit, next_visit\) > start_time\(next_visit\)```

               Arrival at next_visit will likely happen later than its current
               time window due the increased estimate of travel time
               `travel_duration\(previous_visit, next_visit\)` due to traffic. Also, a break
               may be forced to overlap with a visit due to an increase in travel time
               estimates and visit or break time window restrictions.""",
        """::

                 start_time(previous_visit) + duration(previous_visit) +
                 travel_duration(previous_visit, next_visit) > start_time(next_visit)

            Arrival at next_visit will likely happen later than its
            current time window due the increased estimate of travel
            time ``travel_duration(previous_visit, next_visit)`` due to
            traffic. Also, a break may be forced to overlap with a visit
            due to an increase in travel time estimates and visit or
            break time window restrictions."""
    )

    s.move(library, excludes=["google/cloud/optimization/", "setup.py", "README.rst"])
s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------

templated_files = gcp.CommonTemplates().py_library(
    microgenerator=True,
    versions=gcp.common.detect_versions(path="./google", default_first=True),
)
s.move(templated_files, excludes=[".coveragerc"]) # the microgenerator has a good coveragerc file

python.py_samples(skip_readmes=True)

# ----------------------------------------------------------------------------
# Run blacken session
# ----------------------------------------------------------------------------

# run blacken session for all directories which have a noxfile
for noxfile in Path(".").glob("**/noxfile.py"):
    s.shell.run(["nox", "-s", "blacken"], cwd=noxfile.parent, hide_output=False)
