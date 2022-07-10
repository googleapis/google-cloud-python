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

import synthtool as s
from synthtool import gcp
from synthtool.languages import python

common = gcp.CommonTemplates()

default_version = "v1"

for library in s.get_staging_dirs(default_version):
    if library.name == "v1":
        s.replace(
            library / "google/cloud/vision/__init__.py",
            "from google.cloud.vision_v1.services.image_annotator.client import ImageAnnotatorClient",
            "from google.cloud.vision_v1 import ImageAnnotatorClient"
        )

    # Add vision helpers to each version
    s.replace(
        library / f"google/cloud/vision_{library.name}/__init__.py",
        "from .services.image_annotator import ImageAnnotatorClient",
        "from google.cloud.vision_helpers.decorators import "
        "add_single_feature_methods\n"
        "from google.cloud.vision_helpers import VisionHelpers\n\n"
        "from .services.image_annotator import ImageAnnotatorClient as IacImageAnnotatorClient",
    )

    s.replace(
        library / f"google/cloud/vision_{library.name}/__init__.py",
        "__all__ = \(",
        "@add_single_feature_methods\n"
        "class ImageAnnotatorClient(VisionHelpers, IacImageAnnotatorClient):\n"
        "\t__doc__ = IacImageAnnotatorClient.__doc__\n"
        "\tFeature = Feature\n\n"
        "__all__ = (",
    )

    # Temporary workaround due to bug https://github.com/googleapis/proto-plus-python/issues/135
    s.replace(
        library / f"google/cloud/vision_{library.name}/services/image_annotator/client.py",
        "request = image_annotator.BatchAnnotateImagesRequest\(request\)",
        "request = image_annotator.BatchAnnotateImagesRequest(request)\n"
        "            if requests is not None:\n"
        "                for i in range(len(requests)):\n"
        "                    requests[i] = image_annotator.AnnotateImageRequest(requests[i])"
    )

    s.replace(
        library / f"google/cloud/vision_{library.name}/services/image_annotator/client.py",
        "request = image_annotator.BatchAnnotateFilesRequest\(request\)",
        "request = image_annotator.BatchAnnotateFilesRequest(request)\n"
        "            if requests is not None:\n"
        "                for i in range(len(requests)):\n"
        "                    requests[i] = image_annotator.AnnotateFileRequest(requests[i])"
    )

    s.replace(
        library / f"google/cloud/vision_{library.name}/services/image_annotator/client.py",
        "request = image_annotator.AsyncBatchAnnotateImagesRequest\(request\)",
        "request = image_annotator.AsyncBatchAnnotateImagesRequest(request)\n"
        "            if requests is not None:\n"
        "                for i in range(len(requests)):\n"
        "                    requests[i] = image_annotator.AnnotateImageRequest(requests[i])"
    )

    s.replace(
        library / f"google/cloud/vision_{library.name}/services/image_annotator/client.py",
        "request = image_annotator.AsyncBatchAnnotateFilesRequest\(request\)",
        "request = image_annotator.AsyncBatchAnnotateFilesRequest(request)\n"
        "            if requests is not None:\n"
        "                for i in range(len(requests)):\n"
        "                    requests[i] = image_annotator.AsyncAnnotateFileRequest(requests[i])"
    )

    s.move(library / f"google/cloud/vision_{library.name}/proto")
    s.move(library / f"google/cloud/vision_{library.name}/services")
    s.move(library / f"google/cloud/vision_{library.name}/types")
    s.move(library / f"google/cloud/vision_{library.name}/__init__.py")
    s.move(library / f"google/cloud/vision_{library.name}/py.typed")
    s.move(library / f"tests/unit/gapic/vision_{library.name}")

    # don't publish docs for these versions
    if library.name != "v1p1beta1":
        s.move(library / f"docs/vision_{library.name}")

    # Move docs configuration
    s.move(library / f"docs/conf.py")
    s.move(library / "samples")

s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
   samples=True,
   microgenerator=True,
   cov_level=99,
   system_test_external_dependencies=["google-cloud-storage"]
)
s.move(templated_files, excludes=[".coveragerc", "README.rst"])

python.configure_previous_major_version_branches()

# ----------------------------------------------------------------------------
# Samples templates
# ----------------------------------------------------------------------------
python.py_samples(skip_readmes=True)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
