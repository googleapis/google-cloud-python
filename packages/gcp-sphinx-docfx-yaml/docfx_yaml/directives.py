# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# coding: utf-8

"""
This module is used to add extra supported directives to sphinx.
"""

from docutils.parsers.rst.directives.admonitions import BaseAdmonition
from docutils.parsers.rst import Directive
from docutils import nodes

from .nodes import remarks


class RemarksDirective(BaseAdmonition):
    """
    Class to enable remarks directive.
    """
    node_class = remarks

class TodoDirective(Directive):
    """
    Class to ignore todo directive.
    """

    # Enable content in the directive
    has_content = True

    # Directive class must override run function.
    def run(self):
        return_nodes = []

        return return_nodes
