# Copyright 2017, Google Inc. All rights reserved.
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

from __future__ import absolute_import
import sys

from google.cloud.proto.vision.v1 import geometry_pb2
from google.cloud.proto.vision.v1 import image_annotator_pb2
from google.cloud.proto.vision.v1 import text_annotation_pb2
from google.cloud.proto.vision.v1 import web_detection_pb2

from google.gax.utils.messages import get_messages


names = []
for module in (geometry_pb2, image_annotator_pb2,
               text_annotation_pb2, web_detection_pb2):
    for name, message in get_messages(module).items():
        message.__module__ = 'google.cloud.vision_v1.types'
        setattr(sys.modules[__name__], name, message)
        names.append(name)


__all__ = tuple(sorted(names))
