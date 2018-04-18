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

import io
import os
from typing import Any, Callable, Iterable, Mapping, Sequence

import jinja2

from google.protobuf.compiler.plugin_pb2 import CodeGeneratorRequest
from google.protobuf.compiler.plugin_pb2 import CodeGeneratorResponse

from api_factory.schema.api import API
from api_factory.generator.loader import TemplateLoader
from api_factory import utils


class Generator:
    """A protoc code generator for client libraries.

    This class receives a :class:`~.plugin_pb2.CodeGeneratorRequest` (as per
    the protoc plugin contract), and provides an interface for getting
    a :class:`~.plugin_pb2.CodeGeneratorResponse`.

    That request with one or more protocol buffers which collectively
    describe an API.

    Args:
        request (CodeGeneratorRequest): A request protocol buffer as provided
            by protoc. See ``plugin.proto``.
    """
    def __init__(self, request: CodeGeneratorRequest) -> None:
        # Parse the CodeGeneratorRequest into this plugin's internal schema.
        self._api = API()
        for fdp in request.proto_file:
            self._api.load(fdp)

        # Create the jinja environment with which to render templates.
        self._env = jinja2.Environment(loader=TemplateLoader(
            searchpath=os.path.join(_dirname, 'templates'),
        ))

        # Add filters which templates require.
        self._env.filters['snake_case'] = utils.to_snake_case
        self._env.filters['subsequent_indent'] = utils.subsequent_indent
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
                transform_filename=service.transform_filename,
                additional_context={'service': service},
            )

        # Some files are direct files and not templates; simply read them
        # into output files directly.
        #
        # Rather than expect an enumeration of these, we simply grab everything
        # in the `files/` directory automatically.
        output_files += self._read_flat_files(os.path.join(_dirname, 'files'))

        # Return the CodeGeneratorResponse output.
        return CodeGeneratorResponse(file=output_files)

    def _render_templates(
            self,
            templates: Iterable[str], *,
            transform_filename: Callable[[str], str] = lambda fn: fn,
            additional_context: Mapping[str, Any] = None,
            ) -> Sequence[CodeGeneratorResponse.File]:
        """Render the requested templates.

        Args:
            templates (Iterable[str]): The set of templates to be rendered.
                It is expected that these come from the methods on
                :class:`~.loader.TemplateLoader`, and they should be
                able to be set to the :meth:`jinja2.Environment.get_template`
                method.
            transform_filename (Callable[str, str]): A callable to
                rename the resulting file from the template name.
                Note that the `.j2` suffix is stripped automatically.
            additional_context (Mapping[str, Any]): Additional variables
                to be sent to the templates. The ``api`` variable
                is always available.

        Returns:
            Sequence[~.CodeGeneratorResponse.File]: A sequence of File
                objects for inclusion in the final response.
        """
        answer = []
        additional_context = additional_context or {}

        # Iterate over the provided templates and generate a File object
        # for each.
        for template_name in templates:
            # Get the appropriate output filename.
            output_filename = transform_filename(template_name[:-len('.j2')])

            # Generate the File object.
            answer.append(CodeGeneratorResponse.File(
                content=self._env.get_template(template_name).render(
                    api=self._api,
                    **additional_context
                ).strip() + '\n',
                name=output_filename,
            ))

        # Done; return the File objects based on these templates.
        return answer

    def _read_flat_files(
            self,
            target_dir: str,
            ) -> Sequence[CodeGeneratorResponse.File]:
        answer = []

        # Iterate over all files in the directory.
        for path, _, filenames in os.walk(target_dir):
            relative_path = path[len(target_dir):]
            for filename in filenames:
                # Determine the "relative filename" (the filename against the
                # files/ subdirectory and repository root).
                relative_filename = filename
                if relative_path:
                    relative_filename = os.path.join(relative_path, filename)

                # Read the file from disk and create an appropriate OutputFile.
                with io.open(os.path.join(path, filename), 'r') as f:
                    answer.append(CodeGeneratorResponse.File(
                        content=f.read(),
                        name=relative_filename,
                    ))

        # Done; return the File objects.
        return answer


_dirname = os.path.realpath(os.path.dirname(__file__))


__all__ = (
    'Generator',
)
