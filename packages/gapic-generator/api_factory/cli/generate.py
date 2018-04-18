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
import typing

import click

from google.protobuf.compiler import plugin_pb2

from api_factory import generator


@click.command()
@click.option('--request', type=click.File('rb'), default=sys.stdin.buffer,
              help='Location of the `CodeGeneratorRequest` to be processed. '
                   'This defaults to stdin (which is what protoc uses) '
                   'but this option can be set for testing/debugging.')
@click.option('--output', type=click.File('wb'), default=sys.stdout.buffer,
              help='Where to output the `CodeGeneratorResponse`. '
                   'Defaults to stdout.')
def generate(
        request: typing.BinaryIO,
        output: typing.BinaryIO) -> None:
    """Generate a full API client description."""

    # Load the protobuf CodeGeneratorRequest.
    req = plugin_pb2.CodeGeneratorRequest.FromString(request.read())

    # Translate into a protobuf CodeGeneratorResponse;
    # if there are issues, error out appropriately.
    res = generator.Generator(req).get_response()

    # Output the serialized response.
    output.write(res.SerializeToString())
