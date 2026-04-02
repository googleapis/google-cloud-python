# Copyright 2026 Google LLC
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


def inherit_docs(source_class):
    """
    A class decorator that copies docstrings from source_class to the
    decorated class for any methods or attributes that match names.
    """

    def decorator(target_class):
        if not target_class.__doc__ and source_class.__doc__:
            target_class.__doc__ = source_class.__doc__

        for name, source_item in vars(source_class).items():
            if name in vars(target_class):
                target_item = getattr(target_class, name)

                if hasattr(target_item, "__doc__") and not target_item.__doc__:
                    if hasattr(source_item, "__doc__") and source_item.__doc__:
                        try:
                            target_item.__doc__ = source_item.__doc__
                        except AttributeError:
                            pass

        return target_class

    return decorator
