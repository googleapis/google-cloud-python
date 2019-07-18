# Copyright (C) 2019  Google LLC
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

import itertools
import jinja2
import keyword
import re
import time

from gapic.samplegen import utils, yaml


from collections import defaultdict, namedtuple
from typing import Dict, List, Mapping, Optional, Set, Tuple

# Outstanding issues:
# * In real sample configs, many variables are
#   defined with an _implicit_ $resp variable.

MIN_SCHEMA_VERSION = (1, 2, 0)

VALID_CONFIG_TYPE = "com.google.api.codegen.SampleConfigProto"

# TODO: read in copyright and license from files.
FILE_HEADER: Dict[str, str] = {
    "copyright": "TODO: add a copyright",
    "license": "TODO: add a license",
}

RESERVED_WORDS = frozenset(
    itertools.chain(
        keyword.kwlist,
        dir(__builtins__),
        {
            "client",
            "f",  # parameter used in file I/O statements
            "operation",  # temporary used in LROs
            "page",  # used in paginated responses
            "page_result",  # used in paginated responses
            "response",  # basic 'response'
            "stream",  # used in server and bidi streaming
        },
    )
)

TEMPLATE_NAME = "sample.py.j2"


TransformedRequest = namedtuple("TransformedRequest", ["base", "body"])


class SampleError(Exception):
    pass


class ReservedVariableName(SampleError):
    pass


class RpcMethodNotFound(SampleError):
    pass


class UnknownService(SampleError):
    pass


class InvalidConfig(SampleError):
    pass


class InvalidStatement(SampleError):
    pass


class BadLoop(SampleError):
    pass


class MismatchedFormatSpecifier(SampleError):
    pass


class UndefinedVariableReference(SampleError):
    pass


class RedefinedVariable(SampleError):
    pass


class BadAssignment(SampleError):
    pass


class InconsistentRequestName(SampleError):
    pass


class InvalidRequestSetup(SampleError):
    pass


def coerce_response_name(s: str) -> str:
    # In the sample config, the "$resp" keyword is used to refer to the
    # item of interest as received by the corresponding calling form.
    # For a 'regular', i.e. unary, synchronous, non-long-running method,
    # it's the return value; for a server-streaming method, it's the iteration
    # variable in the for loop that iterates over the return value, and for
    # a long running promise, the user calls result on the method return value to
    # resolve the future.
    #
    # The sample schema uses '$resp' as the special variable,
    # but in the samples the 'response' variable is used instead.
    return s.replace("$resp", "response")


class Validator:
    """Class that validates samples.

    Contains methods that validate different segments of a sample and maintains
    state that's relevant to validation across different segments.
    """

    COLL_KWORD = "collection"
    VAR_KWORD = "variable"
    MAP_KWORD = "map"
    KEY_KWORD = "key"
    VAL_KWORD = "value"
    BODY_KWORD = "body"

    def __init__(self):
        # The response ($resp) variable is special and guaranteed to exist.
        self.var_defs_: Set[str] = {"$resp"}

    # TODO: this will eventually need the method name and the proto file
    # so that it can do the correct value transformation for enums.
    def validate_and_transform_request(
        self, calling_form: utils.CallingForm, request: List[Mapping[str, str]]
    ) -> List[TransformedRequest]:
        """Validates and transforms the "request" block from a sample config.

           In the initial request, each dict has a "field" key that maps to a dotted
           variable name, e.g. clam.shell.

           The only required keys in each dict are "field" and value".
           Optional keys are "input_parameter" and "value_is_file".
           All values in the initial request are strings
           except for the value for "value_is_file", which is a bool.

           The topmost dict of the return value has two keys: "base" and "body",
           where "base" maps to a variable name, and "body" maps to a list of variable
           assignment definitions. The only difference in the bottommost dicts
           are that "field" maps only to the second part of a dotted variable name.
           Other key/value combinations in the dict are unmodified for the time being.

           Note: gRPC API methods only take one parameter (ignoring client-side streaming).
                 The reason that GAPIC client library API methods may take multiple parameters
                 is a workaround to provide idiomatic protobuf support within python.
                 The different 'bases' are really attributes for the singular request parameter.

           TODO: properly handle subfields, indexing, and so forth.

           TODO: Conduct module lookup and expansion for protobuf enums.
                 Requires proto/method/message descriptors.
           TODO: Permit single level field/oneof requst parameters.
                 Requires proto/method/message descriptors.
           TODO: Add/transform to list repeated element fields.
                 Requires proto/method/message descriptors.

           E.g. [{"field": "clam.shell", "value": "10 kg", "input_parameter": "shell"},
                 {"field": "clam.pearls", "value": "3"},
                 {"field": "squid.mantle", "value": "100 kg"}]
                  ->
                [TransformedRequest("clam",
                  [{"field": "shell", "value": "10 kg", "input_parameter": "shell"},
                   {"field": "pearls", "value": "3"}]),
                 TransformedRequest("squid", [{"field": "mantle", "value": "100 kg"}])]

           The transformation makes it easier to set up request parameters in jinja
           because it doesn't have to engage in prefix detection, validation,
           or aggregation logic.


        Args:
            request (list[dict{str:str}]): The request body from the sample config

        Returns:
            list[dict{str:(str|list[dict{str:str}])}]: The transformed request block.

        Raises:
            RedefinedVariable: If an "input_parameter" attempts to redefine a
                               previously defined variable.
            ReservedVariableName: If an "input_parameter" value or a "base" value
                                  is a reserved word.
            InvalidRequestSetup: If a dict in the request lacks a "field" key
                                 or the corresponding value is malformed.
        """
        base_param_to_attrs: Mapping[str,
                                     List[Mapping[str, str]]] = defaultdict(list)

        for field_assignment in request:
            field_assignment_copy = dict(field_assignment)
            input_param = field_assignment_copy.get("input_parameter")
            if input_param:
                self._handle_lvalue(input_param)

            field = field_assignment_copy.get("field")
            if not field:
                raise InvalidRequestSetup(
                    "No field attribute found in request setup assignment: {}".format(
                        field_assignment_copy
                    )
                )

            # TODO: properly handle top level fields
            # E.g.
            #
            #  -field: edition
            #   comment: The edition of the series.
            #   value: '123'
            #   input_parameter: edition
            m = re.match(r"^([a-zA-Z]\w*)\.([a-zA-Z]\w*)$", field)
            if not m:
                raise InvalidRequestSetup(
                    "Malformed request attribute description: {}".format(field)
                )

            base, attr = m.groups()
            if base in RESERVED_WORDS:
                raise ReservedVariableName(
                    "Tried to define '{}', which is a reserved name".format(
                        base)
                )

            field_assignment_copy["field"] = attr
            base_param_to_attrs[base].append(field_assignment_copy)

        if (
            calling_form
            in {
                utils.CallingForm.RequestStreamingClient,
                utils.CallingForm.RequestStreamingBidi,
            }
            and len(base_param_to_attrs) > 1
        ):
            raise InvalidRequestSetup(
                (
                    "There can be at most 1 base request in a sample"
                    " for a method with client side streaming"
                )
            )

        return [
            TransformedRequest(base, body) for base, body in base_param_to_attrs.items()
        ]

    def validate_response(self, response):
        """Validates a "response" block from a sample config.

        A full description of the response block is outside the scope of this code;
        refer to the samplegen documentation.


        Dispatches statements to sub-validators.

        Args:
            response: list[dict{str:Any}]: The structured data representing
                                           the sample's response.

        Raises:
            InvalidStatement: If an unexpected key is found in a statement dict
                              or a statement dict has more than or less than one key.
        """

        for statement in response:
            if len(statement) != 1:
                raise InvalidStatement(
                    "Invalid statement: {}".format(statement))

            keyword, body = next(iter(statement.items()))
            validater = self.STATEMENT_DISPATCH_TABLE.get(keyword)
            if not validater:
                raise InvalidStatement(
                    "Invalid statement keyword: {}".format(keyword))

            validater(self, body)

    def _handle_lvalue(self, lval):
        """Conducts safety checks on an lvalue and adds it to the lexical scope.

        Raises:
            ReservedVariableName: If an attempted lvalue is a reserved keyword.
        """
        if lval in RESERVED_WORDS:
            raise ReservedVariableName(
                "Tried to define a variable with reserved name: {}".format(
                    lval)
            )

        # Even though it's valid python to reassign variables to any rvalue,
        # the samplegen spec prohibits this.
        if lval in self.var_defs_:
            raise RedefinedVariable(
                "Tried to redefine variable: {}".format(lval))

        self.var_defs_.add(lval)

    def _validate_format(self, body: List[str]):
        """Validates a format string and corresponding arguments.

         The number of format tokens in the string must equal the
         number of arguments, and each argument must be a defined variable.

         TODO: the attributes of the variable must correspond to attributes
               of the variable's type.

         Raises:
             MismatchedFormatSpecifier: If the number of format string segments ("%s") in
                                        a "print" or "comment" block does not equal the
                                        size number of strings in the block minus 1.
        """
        fmt_str = body[0]
        num_prints = fmt_str.count("%s")
        if num_prints != len(body) - 1:
            raise MismatchedFormatSpecifier(
                "Expected {} expresssions in format string but received {}".format(
                    num_prints, len(body) - 1
                )
            )

        for expression in body[1:]:
            var = expression.split(".")[0]
            if var not in self.var_defs_:
                raise UndefinedVariableReference(
                    "Reference to undefined variable: {}".format(var)
                )

    def _validate_define(self, body: str):
        """"Validates 'define' statements.

        Adds the defined lvalue to the lexical scope.
        Other statements can reference it.

         Raises:
             BadAssignment: If a "define" statement is badly formed lexically.
             UndefinedVariableReference: If an attempted rvalue base is a previously
                                         undeclared variable.
        """
        # TODO: Need to validate the attributes of the response
        #       based on the method return type.
        # TODO: Need to check the defined variables
        #       if the rhs references a non-response variable.
        # TODO: Need to rework the regex to allow for subfields,
        #       indexing, and so forth.
        #
        # Note: really checking for safety would be equivalent to
        #       re-implementing the python interpreter.
        m = re.match(r"^([a-zA-Z]\w*)=([^=]+)$", body)
        if not m:
            raise BadAssignment("Bad assignment statement: {}".format(body))

        lval, rval = m.groups()
        self._handle_lvalue(lval)

        rval_base = rval.split(".")[0]
        if not rval_base in self.var_defs_:
            raise UndefinedVariableReference(
                "Reference to undefined variable: {}".format(rval_base)
            )

    def _validate_write_file(self, body):
        """Validate 'write_file' statements.

        The body of a 'write_file' statement is a two-element dict
        with known keys: 'filename' and 'contents'.
        'filename' maps to a list of strings which constitute a format string
        and variable-based rvalues defining the fields.
        'contents' maps to a single variable-based rvalue.

        Raises:
            MismatchedFormatSpecifier: If the filename formatstring is badly formed.
            UndefinedVariableReference: If any of the formatstring variables
                                        or the file contents variable are undefined.
            InvalidStatement: If either 'filename' or 'contents' are absent keys.
        """

        fname_fmt = body.get("filename")
        if not fname_fmt:
            raise InvalidStatement(
                "Missing key in 'write_file' statement: 'filename'")

        self._validate_format(fname_fmt)

        contents_var = body.get("contents")
        if not contents_var:
            raise InvalidStatement(
                "Missing key in 'write_file' statement: 'contents'")

        # TODO: check the rest of the elements for valid subfield attribute
        base = contents_var.split(".")[0]
        if base not in self.var_defs_:
            raise UndefinedVariableReference(
                "Reference to undefined variable: {}".format(base)
            )

    def _validate_loop(self, body):
        """Validates loop headers and statement bodies.

        Checks for correctly defined loop constructs,
        either 'collection' loops with a collection and iteration variable,
        or 'map' loops with a map and at least one of 'key' or 'value'.
        Loops also have a 'body', which contains statments that may
        use the variables from the header.

        The body statements are validated recursively.
        The iteration variable(s) is/are added to the lexical scope
        before validating the statements in the loop body.

        Raises:
            UndefinedVariableReference: If an attempted rvalue base is a previously
                                        undeclared variable.
            BadLoop: If a "loop" segments has unexpected keywords
                     or keyword combinatations.

        """
        segments = set(body.keys())
        map_args = {self.MAP_KWORD, self.BODY_KWORD}

        # Even though it's valid python to use a variable outside of the lexical
        # scope it was defined in,
        #
        # i.e.
        #   for m in molluscs:
        #     handle(m)
        #   print("Last mollusc: {}".format(m))
        #
        # is allowed, the samplegen spec requires that errors are raised
        # if strict lexical scoping is violated.
        previous_defs = set(self.var_defs_)

        if {self.COLL_KWORD, self.VAR_KWORD, self.BODY_KWORD} == segments:
            collection_name = body[self.COLL_KWORD].split(".")[0]
            # TODO: Once proto info is being passed in, validate the
            #       [1:] in the collection name.
            # TODO: resolve the implicit $resp dilemma
            # if collection_name.startswith("."):
            #     collection_name = "$resp" + collection_name
            if collection_name not in self.var_defs_:
                raise UndefinedVariableReference(
                    "Reference to undefined variable: {}".format(
                        collection_name)
                )

            var = body[self.VAR_KWORD]
            self._handle_lvalue(var)

        elif map_args <= segments:
            segments -= map_args
            segments -= {self.KEY_KWORD, self.VAL_KWORD}
            if segments:
                raise BadLoop(
                    "Unexpected keywords in loop statement: {}".format(
                        segments)
                )

            map_name_base = body[self.MAP_KWORD].split(".")[0]
            if map_name_base not in self.var_defs_:
                raise UndefinedVariableReference(
                    "Reference to undefined variable: {}".format(map_name_base)
                )

            key = body.get(self.KEY_KWORD)
            if key:
                self._handle_lvalue(key)

            val = body.get(self.VAL_KWORD)
            if val:
                self._handle_lvalue(val)

            if not (key or val):
                raise BadLoop(
                    "Need at least one of 'key' or 'value' in a map loop")

        else:
            raise BadLoop("Unexpected loop form: {}".format(segments))

        self.validate_response(body[self.BODY_KWORD])
        # Restore the previous lexical scope.
        # This is stricter than python scope rules
        # because the samplegen spec mandates it.
        self.var_defs_ = previous_defs

    # Add new statement keywords to this table.
    # TODO: add write_file validator and entry (and tests).
    STATEMENT_DISPATCH_TABLE = {
        "define": _validate_define,
        "print": _validate_format,
        "comment": _validate_format,
        "write_file": _validate_write_file,
        "loop": _validate_loop,
    }


def generate_sample(
    sample, id_is_unique: bool, env: jinja2.environment.Environment, api_schema
) -> Tuple[str, jinja2.environment.TemplateStream]:
    sample_template = env.get_template(TEMPLATE_NAME)

    service_name = sample["service"]
    service = api_schema.services.get(service_name)
    if not service:
        raise UnknownService("Unknown service: {}", service_name)

    rpc_name = sample["rpc"]
    rpc = service.methods.get(rpc_name)
    if not rpc:
        raise RpcMethodNotFound(
            "Could not find rpc in service {}: {}".format(
                service_name, rpc_name)
        )

    calling_form = utils.CallingForm.method_default(rpc)

    v = Validator()
    sample["request"] = v.validate_and_transform_request(
        calling_form, sample["request"]
    )
    v.validate_response(sample["response"])

    sample_fpath = (
        sample["id"] + (str(calling_form) if not id_is_unique else "") + ".py"
    )

    sample["package_name"] = api_schema.naming.warehouse_package_name

    return (
        sample_fpath,
        sample_template.stream(
            file_header=FILE_HEADER,
            sample=sample,
            imports=[],
            calling_form=calling_form,
            calling_form_enum=utils.CallingForm,
        ),
    )


def generate_manifest(fpaths_and_samples, api_schema, *, manifest_time: int = None):
    """Generate a samplegen manifest for use by sampletest

    Args:
        fpaths_and_samples (Iterable[Tuple[str, Mapping[str, Any]]]):
                         The file paths and samples to be listed in the manifest

        api_schema (~.api.API): An API schema object.
        manifest_time (int): Optional. An override for the timestamp in the name of the manifest filename.
                             Primarily used for testing.

    Returns:
        Tuple[str, Dict[str,Any]]: The filename of the manifest and the manifest data as a dictionary.

    """
    all_info = [
        yaml.KeyVal("type", "manifest/samples"),
        yaml.KeyVal("schema_version", "3"),
        yaml.Map(
            name="python",
            anchor_name="python",
            elements=[
                yaml.KeyVal("environment", "python"),
                yaml.KeyVal("bin", "python3"),
                # TODO: make this the real sample base directory
                yaml.KeyVal("base_path", "sample/base/directory"),
                yaml.KeyVal("invocation", "'{bin} {path} @args'"),
            ],
        ),
        yaml.Collection(
            name="samples",
            elements=[
                [
                    yaml.Anchor("python"),
                    yaml.KeyVal("sample", sample["id"]),
                    yaml.KeyVal("path", "'{base_path}/%s'" % fpath),
                    yaml.KeyVal("region_tag", sample.get("region_tag", "")),
                ]
                for fpath, sample in fpaths_and_samples
            ],
        ),
    ]

    dt = time.gmtime(manifest_time)
    manifest_fname_template = (
        "{api}.{version}.python."
        "{year:04d}{month:02d}{day:02d}."
        "{hour:02d}{minute:02d}{second:02d}."
        "manifest.yaml"
    )

    manifest_fname = manifest_fname_template.format(
        api=api_schema.naming.name,
        version=api_schema.naming.version,
        year=dt.tm_year,
        month=dt.tm_mon,
        day=dt.tm_mday,
        hour=dt.tm_hour,
        minute=dt.tm_min,
        second=dt.tm_sec,
    )

    return manifest_fname, all_info
