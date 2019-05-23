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

import collections
import os
import re
from typing import Mapping, Sequence

import jinja2

from google.protobuf.compiler.plugin_pb2 import CodeGeneratorResponse

from gapic import utils
from gapic.generator import formatter
from gapic.generator import options
from gapic.schema import api


class Generator:
    """A protoc code generator for client libraries.

    This class provides an interface for getting a
    :class:`~.plugin_pb2.CodeGeneratorResponse` for an :class:`~api.API`
    schema object (which it does through rendering templates).

    Args:
        opts (~.options.Options): An options instance.
        templates (str): Optional. Path to the templates to be
            rendered. If this is not provided, the templates included with
            this application are used.
    """
    def __init__(self, opts: options.Options) -> None:
        # Create the jinja environment with which to render templates.
        self._env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(searchpath=opts.templates),
            undefined=jinja2.StrictUndefined,
        )

        # Add filters which templates require.
        self._env.filters['rst'] = utils.rst
        self._env.filters['snake_case'] = utils.to_snake_case
        self._env.filters['sort_lines'] = utils.sort_lines
        self._env.filters['wrap'] = utils.wrap

    def get_response(self, api_schema: api.API) -> CodeGeneratorResponse:
        """Return a :class:`~.CodeGeneratorResponse` for this library.

        This is a complete response to be written to (usually) stdout, and
        thus read by ``protoc``.

        Args:
            api_schema (~api.API): An API schema object.

        Returns:
            ~.CodeGeneratorResponse: A response describing appropriate
            files and contents. See ``plugin.proto``.
        """
        output_files = collections.OrderedDict()

        # Iterate over each template and add the appropriate output files
        # based on that template.
        for template_name in self._env.loader.list_templates():
            # Sanity check: Skip "private" templates.
            filename = template_name.split('/')[-1]
            if filename.startswith('_') and filename != '__init__.py.j2':
                continue

            # Append to the output files dictionary.
            output_files.update(self._render_template(template_name,
                api_schema=api_schema,
            ))

        # Return the CodeGeneratorResponse output.
        return CodeGeneratorResponse(file=[i for i in output_files.values()])

    def _render_template(
            self,
            template_name: str, *,
            api_schema: api.API,
            ) -> Sequence[CodeGeneratorResponse.File]:
        """Render the requested templates.

        Args:
            template_name (str): The template to be rendered.
                It is expected that these come from
                :class:`jinja2.FileSystemLoader`, and they should be
                able to be sent to the :meth:`jinja2.Environment.get_template`
                method.
            api_schema (~.api.API): An API schema object.

        Returns:
            Sequence[~.CodeGeneratorResponse.File]: A sequence of File
                objects for inclusion in the final response.
        """
        answer = collections.OrderedDict()
        skip_subpackages = False

        # Sanity check: Rendering per service and per proto would be a
        # combinatorial explosion and is almost certainly not what anyone
        # ever wants. Error colorfully on it.
        if '$service' in template_name and '$proto' in template_name:
            raise ValueError('Template files may live under a $proto or '
                             '$service directory, but not both.')

        # If this template should be rendered for subpackages, process it
        # for all subpackages and set the strict flag (restricting what
        # services and protos we pull from for the remainder of the method).
        if '$sub' in template_name:
            for subpackage in api_schema.subpackages.values():
                answer.update(self._render_template(template_name,
                    api_schema=subpackage,
                ))
            skip_subpackages = True

        # If this template should be rendered once per proto, iterate over
        # all protos to be rendered
        if '$proto' in template_name:
            for proto in api_schema.protos.values():
                if (skip_subpackages and proto.meta.address.subpackage !=
                        api_schema.subpackage_view):
                    continue
                answer.update(self._get_file(template_name,
                    api_schema=api_schema,
                    proto=proto
                ))
            return answer

        # If this template should be rendered once per service, iterate
        # over all services to be rendered.
        if '$service' in template_name:
            for service in api_schema.services.values():
                if (skip_subpackages and service.meta.address.subpackage !=
                        api_schema.subpackage_view):
                    continue
                answer.update(self._get_file(template_name,
                    api_schema=api_schema,
                    service=service,
                ))
            return answer

        # This file is not iterating over anything else; return back
        # the one applicable file.
        answer.update(self._get_file(template_name, api_schema=api_schema))
        return answer

    def _get_file(self, template_name: str, *,
            api_schema=api.API,
            **context: Mapping):
        """Render a template to a protobuf plugin File object."""
        # Determine the target filename.
        fn = self._get_filename(template_name,
            api_schema=api_schema,
            context=context,
        )

        # Render the file contents.
        cgr_file = CodeGeneratorResponse.File(
            content=formatter.fix_whitespace(
                self._env.get_template(template_name).render(
                    api=api_schema,
                    **context
                ),
            ),
            name=fn,
        )

        # Sanity check: Do not render empty files.
        if utils.empty(cgr_file.content) and not fn.endswith('__init__.py'):
            return {}

        # Return the filename and content in a length-1 dictionary
        # (because we track output files overall in a dictionary).
        return {fn: cgr_file}

    def _get_filename(
            self,
            template_name: str, *,
            api_schema: api.API,
            context: dict = None,
            ) -> str:
        """Return the appropriate output filename for this template.

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
            api_schema (~.api.API): An API schema object.
            context (Mapping): Additional context being sent to the template.

        Returns:
            str: The appropriate output filename.
        """
        filename = template_name[:-len('.j2')]

        # Replace the $namespace variable.
        filename = filename.replace(
            '$namespace',
            os.path.sep.join([i.lower() for i in api_schema.naming.namespace]),
        ).lstrip(os.path.sep)

        # Replace the $name, $version, and $sub variables.
        filename = filename.replace('$name_$version',
                                    api_schema.naming.versioned_module_name)
        filename = filename.replace('$version', api_schema.naming.version)
        filename = filename.replace('$name', api_schema.naming.module_name)
        filename = filename.replace('$sub',
                                    '/'.join(api_schema.subpackage_view))

        # Replace the $service variable if applicable.
        if context and 'service' in context:
            filename = filename.replace(
                '$service',
                context['service'].module_name,
            )

        # Replace the $proto variable if appliable.
        # In the cases of protos, we also honor subpackages.
        if context and 'proto' in context:
            filename = filename.replace(
                '$proto',
                context['proto'].module_name,
            )

        # Paths may have empty path segments if components are empty
        # (e.g. no $version); handle this.
        filename = re.sub(r'/+', '/', filename)

        # Done, return the filename.
        return filename


__all__ = (
    'Generator',
)
