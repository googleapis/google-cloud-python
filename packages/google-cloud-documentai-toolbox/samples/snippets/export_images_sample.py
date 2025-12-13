# Copyright 2023 Google LLC
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
#


# [START documentai_toolbox_export_images]

from google.cloud.documentai_toolbox import document

# TODO(developer): Uncomment these variables before running the sample.
# Given a local document.proto or sharded document.proto from an identity processor in path
# document_path = "path/to/local/document.json"
# output_path = "resources/output/"
# output_file_prefix = "exported_photo"
# output_file_extension = "png"


def export_images_sample(
    document_path: str,
    output_path: str,
    output_file_prefix: str,
    output_file_extension: str,
) -> None:
    wrapped_document = document.Document.from_document_path(document_path=document_path)

    output_files = wrapped_document.export_images(
        output_path=output_path,
        output_file_prefix=output_file_prefix,
        output_file_extension=output_file_extension,
    )
    print("Images Successfully Exported")
    for output_file in output_files:
        print(output_file)


# [END documentai_toolbox_export_images]
