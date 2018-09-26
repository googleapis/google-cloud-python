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

import typing

import jinja2

from gapic.utils import cached_property


class TemplateLoader(jinja2.FileSystemLoader):
    """A jinja2 template loader that tracks what is left to be loaded.

    This class behaves identically to :class:`jinja2.FileSystemLoader`
    but provides methods to return templates segmented by type.

    There are two types of templates: templates that describe the API as a
    whole (and for which the template is rendered once per API), and templates
    describing a service (which are rendered once per service in the API).
    """
    @cached_property
    def api_templates(self) -> typing.Set[str]:
        """Return the (public) templates tied to the API as a whole.

        All templates in the ``templates/`` directory are included except:

          * Templates corresponding to services (in a ``$service/``
            subdirectory) are excluded. See :meth:`service_templates`.
          * Templates beginning with ``_`` are excluded.

        When these templates are rendered, they are expected to be sent
        one and only one variable: an :class:`~.API` object spelled ``api``.

        Returns:
            Set[str]: A set of templates.
        """
        # Start with the full list of templates, excluding private ones,
        # but exclude templates from other methods on this loader.
        return set(
            [t for t in self.list_templates() if not self.is_private(t)]
        ).difference(self.service_templates).difference(self.proto_templates)

    @cached_property
    def service_templates(self):
        """Return the templates specific to each service.

        This corresponds to all of the templates with ``$service``
        in the filename or path.

        When these templates are rendered, they are expected to be sent
        two variables: an :class:`~.API` object spelled ``api``, and the
        :class:`~.wrappers.Service` object being iterated over, spelled
        ``service``. These templates are rendered once per service, with
        a distinct ``service`` variable each time.

        Returns:
            Set[str]: A list of service templates.
        """
        return set(
            [t for t in self.list_templates() if '$service' in t]
        )

    @cached_property
    def proto_templates(self):
        """Return the templates specific to each proto.

        This corresponds to all of the templates with ``$proto``
        in the filename or path.

        When these templates are rendered, they are expected to be sent
        two variables: an :class:`~.API` object spelled ``api``, and the
        :class:`~.wrappers.Proto` object being iterated over, spelled
        ``proto``. These templates are rendered once per proto, with
        a distinct ``proto`` variable each time.

        Returns:
            Set[str]: A list of proto templates.
        """
        return set(
            [t for t in self.list_templates() if '$proto' in t]
        )

    def is_private(self, path):
        """Return True if ``path`` is a private template, False otherwise."""
        filename = path.split('/')[-1]
        return filename != '__init__.py.j2' and filename.startswith('_')
