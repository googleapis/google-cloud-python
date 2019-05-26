# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys

from proto.marshal import Marshal


def compile(name, attrs):
    """Build and return a ``_DescriptorInfo`` object.

    Args:
        name (str): The name of the new class, as sent to ``type.__new__``.
        attrs (Mapping[str, Any]): The attrs for a new class, as sent
            to ``type.__new__``

    Returns:
        Tuple[Tuple[str], str, ~.Marshal]:
            - The local path of the proto component.
            - The proto package, if any (empty string otherwise).
            - The marshal object to use.
    """
    # Pull a reference to the module where this class is being
    # declared.
    module = sys.modules.get(attrs.get('__module__'))
    proto_module = getattr(module, '__protobuf__', object())

    # A package should be present; get the marshal from there.
    package = getattr(proto_module, 'package', '')
    marshal = Marshal(name=getattr(proto_module, 'marshal', package))

    # Determine the local path of this proto component within the file.
    local_path = tuple(attrs.get('__qualname__', name).split('.'))

    # Sanity check: We get the wrong full name if a class is declared
    # inside a function local scope; correct this.
    if '<locals>' in local_path:
        ix = local_path.index('<locals>')
        local_path = local_path[:ix - 1] + local_path[ix + 1:]

    # Done; return the data.
    return (local_path, package, marshal)
