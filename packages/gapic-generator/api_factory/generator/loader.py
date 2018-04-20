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

from api_factory.utils import cached_property


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
            [t for t in self.list_templates() if not t.startswith('_')]
        ).difference(self.service_templates)

    @cached_property
    def service_templates(self):
        """Return the templates specific to each service.

        This corresponds to all of the templates in a ``$service/``
        subdirectory (this does _not_ need to be at the top level).

        When these templates are rendered, they are expected to be sent
        two variables: an :class:`~.API` object spelled ``api``, and the
        :class:`~.wrappers.Service` object being iterated over, spelled
        ``service``. These templates are rendered once per service, with
        a distinct ``service`` variable each time.

        Returns:
            Set[str]: A list of service templates.
        """
        return set(
            [t for t in self.list_templates() if '$service/' in t]
        )
