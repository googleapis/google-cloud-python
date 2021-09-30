# Copyright 2021 Google LLC
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

from typing import Any, Generator, Dict, List, Tuple
import re


def _sample_names() -> Generator[str, None, None]:
    sample_num: int = 0
    while True:
        sample_num += 1
        yield "sample{}".format(sample_num)


def add_field(obj, path, value):
    """Insert a field into a nested dict and return the (outer) dict.
     Keys and sub-dicts are inserted if necessary to create the path.
     e.g. if obj, as passed in, is {}, path is "a.b.c", and value is
     "hello", obj will be updated to:
      {'a':
         {'b':
          {
          'c': 'hello'
          }
         }
      }

    Args:
      obj: a (possibly) nested dict (parsed json)
      path: a segmented field name, e.g. "a.b.c"
        where each part is a dict key.
      value: the value of the new key.
    Returns:
          obj, possibly modified
    Raises:
          AttributeError if the path references a key that is
      not a dict.: e.g. path='a.b', obj = {'a':'abc'}
    """
    segments = path.split('.')
    leaf = segments.pop()
    subfield = obj
    for segment in segments:
        subfield = subfield.setdefault(segment, {})
    subfield[leaf] = value
    return obj


def sample_from_path_fields(paths: List[Tuple[str, str]]) -> Dict[Any, Any]:
    """Construct a dict for a sample request object from a list of fields
       and template patterns.

    Args:
          paths: a list of tuples, each with a (segmented) name and a pattern.
    Returns:
          A new nested dict with the templates instantiated.
    """

    request: Dict[str, Any] = {}
    sample_names = _sample_names()

    for path, template in paths:
        sample_value = re.sub(
            r"(\*\*|\*)", lambda n: next(sample_names), template)
        add_field(request, path, sample_value)
    return request
