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

import os
from typing import Any, Iterable, Mapping, Sequence, Tuple

import jinja2

from google.protobuf.compiler.plugin_pb2 import CodeGeneratorResponse

from gapic import utils
from gapic.generator import formatter
from gapic.generator import loader
from gapic.schema import api


class Generator:
    """A protoc code generator for client libraries.

    This class receives a :class:`~.api.API`, a representation of the API
    schema, and provides an interface for getting a
    :class:`~.plugin_pb2.CodeGeneratorResponse` (which it does through
    rendering templates).

    Args:
        api_schema (~.API): An API schema object, which is sent to every
            template as the ``api`` variable.
        templates (str): Optional. Path to the templates to be
            rendered. If this is not provided, the templates included with
            this application are used.
    """
    def __init__(self, api_schema: api.API, *,
                 templates: str = None) -> None:
        self._api = api_schema

        # If explicit templates were not provided, use our default.
        if not templates:
            templates = os.path.join(
                os.path.realpath(os.path.dirname(__file__)),
                '..', 'templates',
            )

        # Create the jinja environment with which to render templates.
        self._env = jinja2.Environment(
            loader=loader.TemplateLoader(searchpath=templates),
            undefined=jinja2.StrictUndefined,
        )

        # Add filters which templates require.
        self._env.filters['snake_case'] = utils.to_snake_case
        self._env.filters['wrap'] = utils.wrap

    def get_response(self) -> CodeGeneratorResponse:
        """Return a :class:`~.CodeGeneratorResponse` for this library.

        This is a complete response to be written to (usually) stdout, and
        thus read by ``protoc``.

        Returns:
            ~.CodeGeneratorResponse: A response describing appropriate
            files and contents. See ``plugin.proto``.
        """
        output_files = []

        # Some templates are rendered once per API client library.
        # These are generally boilerplate packaging and metadata files.
        output_files += self._render_templates(self._env.loader.api_templates)

        # Some templates are rendered once per service (an API may have
        # one or more services).
        for service in self._api.services.values():
            output_files += self._render_templates(
                self._env.loader.service_templates,
                additional_context={'service': service},
            )

        # Return the CodeGeneratorResponse output.
        return CodeGeneratorResponse(file=output_files)

    def _render_templates(
            self,
            templates: Iterable[str], *,
            additional_context: Mapping[str, Any] = None,
            ) -> Sequence[CodeGeneratorResponse.File]:
        """Render the requested templates.

        Args:
            templates (Iterable[str]): The set of templates to be rendered.
                It is expected that these come from the methods on
                :class:`~.loader.TemplateLoader`, and they should be
                able to be set to the :meth:`jinja2.Environment.get_template`
                method.
            additional_context (Mapping[str, Any]): Additional variables
                to be sent to the templates. The ``api`` variable
                is always available.

        Returns:
            Sequence[~.CodeGeneratorResponse.File]: A sequence of File
                objects for inclusion in the final response.
        """
        answer = []
        context = additional_context or {}

        # Iterate over the provided templates and generate a File object
        # for each.
        for template_name in templates:
            for fn in self._get_filenames(template_name, context=context):
                # Generate the File object.
                answer.append(CodeGeneratorResponse.File(
                    content=formatter.fix_whitespace(
                        self._env.get_template(template_name).render(
                            api=self._api,
                            **context
                        ),
                    ),
                    name=fn,
                ))

        # Done; return the File objects based on these templates.
        return answer

    def _get_filenames(
            self,
            template_name: str, *,
            context: dict = None,
            ) -> Tuple[str]:
        """Return the appropriate output filenames for this template.

        This entails running the template name through a series of
        replacements to replace the "filename variables" (``$name``,
        ``$service``, etc.).

        Additionally, any of these variables may be substituted with an
        empty value, and we should do the right thing in this case.
        (The exception to this is ``$service``, which is guaranteed to be
        set if it is needed.)

        Args:
            template_name (str): The filename of the template, from the
                filesystem, relative to ``templates/``.
            context (Mapping): Additional context being sent to the template.

        Returns:
            Tuple[str]: The appropriate output filenames.
        """
        filename = template_name[:-len('.j2')]

        # Special case: If the filename is `$namespace/__init__.py`, we
        # need this exact file to be part of every individual directory
        # in the namespace tree. Handle this special case.
        #
        # For more information, see:
        # https://packaging.python.org/guides/packaging-namespace-packages/
        if filename == os.path.join('$namespace', '__init__.py'):
            return tuple([
                os.path.sep.join(i.split('.') + ['__init__.py'])
                for i in self._api.naming.namespace_packages
            ])

        # Replace the $namespace variable.
        filename = filename.replace(
            '$namespace',
            os.path.sep.join([i.lower() for i in self._api.naming.namespace]),
        ).lstrip(os.path.sep)

        # Replace the $name and $version variables.
        filename = filename.replace('$name_$version',
                                    self._api.naming.versioned_module_name)
        filename = filename.replace('$name', self._api.naming.module_name)

        # Replace the $service variable if applicable.
        if context and 'service' in context:
            filename = filename.replace('$service',
                                        context['service'].module_name)

        # Done, return the filename.
        return (filename,)


__all__ = (
    'Generator',
)
