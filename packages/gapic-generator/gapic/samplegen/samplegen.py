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

import dataclasses
import itertools
import jinja2
import keyword
import os
import re
import time

from gapic.samplegen_utils import types
from gapic.schema import (api, wrappers)

from collections import (defaultdict, namedtuple, ChainMap as chainmap)
from typing import (ChainMap, Dict, List, Mapping, Optional, Tuple)

from google.protobuf import descriptor_pb2

# Outstanding issues:
# * In real sample configs, many variables are
#   defined with an _implicit_ $resp variable.


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

DEFAULT_TEMPLATE_NAME = "sample.py.j2"


@dataclasses.dataclass(frozen=True)
class AttributeRequestSetup:
    """A single request-field setup description.

    If 'field' is not set, this is a top level attribute, in which case the 'base'
    parameter of the owning TransformedRequest is the attribute name.

    A True 'value_is_file' indicates that 'value' is a file path,
    and that the value of the attribute is the contents of that file.

    A non-empty 'input_parameter' indicates a formal parameter to the sample function
    that contains the value for the attribute.

    """
    value: str
    field: Optional[str] = None
    value_is_file: bool = False
    input_parameter: Optional[str] = None
    comment: Optional[str] = None


@dataclasses.dataclass(frozen=True)
class TransformedRequest:
    """Class representing a single field in a method call.

    A request block, as read in from the sample config, is a list of dicts that
    describe field setup for the API method request.

    Fields with subfields are treated as dictionaries, with subfields as keys
    and passed, read, or hardcoded subfield values as the mapped values.
    These field dictionaries are passed into the client method as positional arguments.

    Fields _without_ subfields, aka top-level-fields, are passed into the method call
    as keyword parameters, with their associated values assigned directly.

    A TransformedRequest describes a subfield of the API request.
    It is either a top level request, in which case the 'single' attribute is filled,
    or it has assigned-to subfields, in which case 'body' lists assignment setups.

    The Optional[single]/Optional[body] is workaround for not having tagged unions.
    """
    base: str
    single: Optional[AttributeRequestSetup]
    body: Optional[List[AttributeRequestSetup]]


class Validator:
    """Class that validates a sample.

    Contains methods that validate different segments of a sample and maintains
    state that's relevant to validation across different segments.
    """

    COLL_KWORD = "collection"
    VAR_KWORD = "variable"
    MAP_KWORD = "map"
    KEY_KWORD = "key"
    VAL_KWORD = "value"
    BODY_KWORD = "body"

    def __init__(self, method: wrappers.Method):
        # The response ($resp) variable is special and guaranteed to exist.
        self.request_type_ = method.input
        response_type = method.output
        if method.paged_result_field:
            response_type = method.paged_result_field
        elif method.lro:
            response_type = method.lro.response_type

        # This is a shameless hack to work around the design of wrappers.Field
        MockField = namedtuple("MockField", ["message", "repeated"])

        # TODO: pass var_defs_ around during response verification
        #       instead of assigning/restoring.
        self.var_defs_: ChainMap[str, wrappers.Field] = chainmap(
            # When validating expressions we need to store the Field,
            # not just the message type, because there are additional data we need:
            # whether a name refers to a repeated value (or a map),
            # and whether it's an enum or a message or a primitive type.
            # The method call response isn't a field, so construct an artificial
            # field that wraps the response.
            {  # type: ignore
                "$resp": MockField(response_type, False)
            }
        )

    @staticmethod
    def preprocess_sample(sample, api_schema):
        """Modify a sample to set default or missing fields.

        Args:
           sample (Any): A definition for a single sample generated from parsed yaml.
           api_schema (api.API): The schema that defines the API to which the sample belongs.
        """
        sample["package_name"] = api_schema.naming.warehouse_package_name
        sample.setdefault("response", [{"print": ["%s", "$resp"]}])

    def var_field(self, var_name: str) -> Optional[wrappers.Field]:
        return self.var_defs_.get(var_name)

    def validate_and_transform_request(self,
                                       calling_form: types.CallingForm,
                                       request: List[Mapping[str, str]]) -> List[TransformedRequest]:
        """Validates and transforms the "request" block from a sample config.

           In the initial request, each dict has a "field" key that maps to a dotted
           variable name, e.g. clam.shell.

           The only required keys in each dict are "field" and value".
           Optional keys are "input_parameter", "value_is_file". and "comment".
           All values in the initial request are strings except for the value
           for "value_is_file", which is a bool.

           The TransformedRequest structure of the return value has three fields:
           "base", "body", and "single", where "base" maps to the top level attribute name,
           "body" maps to a list of subfield assignment definitions, and "single"
           maps to a singleton attribute assignment structure with no "field" value.
           The "field" attribute in the requests in a "body" list have their prefix stripped;
           the request in a "single" attribute has no "field" attribute.

           Note: gRPC API methods only take one parameter (ignoring client-side streaming).
                 The reason that GAPIC client library API methods may take multiple parameters
                 is a workaround to provide idiomatic protobuf support within python.
                 The different 'bases' are really attributes for the singular request parameter.

           TODO: properly handle subfields, indexing, and so forth.
           TODO: Add/transform to list repeated element fields.
                 Requires proto/method/message descriptors.

           E.g. [{"field": "clam.shell", "value": "10 kg", "input_parameter": "shell"},
                 {"field": "clam.pearls", "value": "3"},
                 {"field": "squid.mantle", "value": "100 kg"},
                 {"field": "whelk", "value": "speckled"}]
                  ->
                [TransformedRequest(
                     base="clam",
                     body=[AttributeRequestSetup(field="shell",
                                                 value="10 kg",
                                                 input_parameter="shell"),
                           AttributeRequestSetup(field="pearls", value="3")],
                     single=None),
                 TransformedRequest(base="squid",
                                    body=[AttributeRequestSetup(field="mantle",
                                                                value="100 kg")],
                                    single=None),
                 TransformedRequest(base="whelk",
                                    body=None,
                                    single=AttributeRequestSetup(value="speckled))]

           The transformation makes it easier to set up request parameters in jinja
           because it doesn't have to engage in prefix detection, validation,
           or aggregation logic.


        Args:
            request (list[dict{str:str}]): The request body from the sample config

        Returns:
            List[TransformedRequest]: The transformed request block.

        Raises:
            InvalidRequestSetup: If a dict in the request lacks a "field" key,
                                 a "value" key, if there is an unexpected keyword,
                                 or if more than one base parameter is given for
                                 a client-side streaming calling form.
            BadAttributeLookup: If a request field refers to a non-existent field
                                in the request message type.

        """
        base_param_to_attrs: Dict[str,
                                  List[AttributeRequestSetup]] = defaultdict(list)

        for r in request:
            duplicate = dict(r)
            val = duplicate.get("value")
            if not val:
                raise types.InvalidRequestSetup(
                    "Missing keyword in request entry: 'value'")

            field = duplicate.get("field")
            if not field:
                raise types.InvalidRequestSetup(
                    "Missing keyword in request entry: 'field'")

            spurious_keywords = set(duplicate.keys()) - {"value",
                                                         "field",
                                                         "value_is_file",
                                                         "input_parameter",
                                                         "comment"}
            if spurious_keywords:
                raise types.InvalidRequestSetup(
                    "Spurious keyword(s) in request entry: {}".format(
                        ", ".join(f"'{kword}'" for kword in spurious_keywords)))

            input_parameter = duplicate.get("input_parameter")
            if input_parameter:
                self._handle_lvalue(input_parameter, wrappers.Field(
                    field_pb=descriptor_pb2.FieldDescriptorProto()))

            attr_chain = field.split(".")
            base = self.request_type_
            for i, attr_name in enumerate(attr_chain):
                attr = base.fields.get(attr_name)
                if not attr:
                    raise types.BadAttributeLookup(
                        "Method request type {} has no attribute: '{}'".format(
                            self.request_type_.type, attr_name))

                if attr.message:
                    base = attr.message
                elif attr.enum:
                    # A little bit hacky, but 'values' is a list, and this is the easiest
                    # way to verify that the value is a valid enum variant.
                    witness = any(e.name == val for e in attr.enum.values)
                    if not witness:
                        raise types.InvalidEnumVariant(
                            "Invalid variant for enum {}: '{}'".format(attr, val))
                    # Python code can set protobuf enums from strings.
                    # This is preferable to adding the necessary import statement
                    # and requires less munging of the assigned value
                    duplicate["value"] = f"'{val}'"
                    break
                else:
                    raise TypeError

            if i != len(attr_chain) - 1:
                # We broke out of the loop after processing an enum.
                extra_attrs = ".".join(attr_chain[i:])
                raise types.InvalidEnumVariant(
                    f"Attempted to reference attributes of enum value: '{extra_attrs}'")

            if len(attr_chain) > 1:
                duplicate["field"] = ".".join(attr_chain[1:])
            else:
                # Because of the way top level attrs get rendered,
                # there can't be duplicates.
                # This is admittedly a bit of a hack.
                if attr_chain[0] in base_param_to_attrs:
                    raise types.InvalidRequestSetup(
                        "Duplicated top level field in request block: '{}'".format(
                            attr_chain[0]))
                del duplicate["field"]

            # Mypy isn't smart enough to handle dictionary unpacking,
            # so disable it for the AttributeRequestSetup ctor call.
            base_param_to_attrs[attr_chain[0]].append(
                AttributeRequestSetup(**duplicate))  # type: ignore

        client_streaming_forms = {
            types.CallingForm.RequestStreamingClient,
            types.CallingForm.RequestStreamingBidi,
        }

        if len(base_param_to_attrs) > 1 and calling_form in client_streaming_forms:
            raise types.InvalidRequestSetup(
                "Too many base parameters for client side streaming form")

        return [
            (TransformedRequest(base=key, body=val, single=None) if val[0].field
             else TransformedRequest(base=key, body=None, single=val[0]))
            for key, val in base_param_to_attrs.items()
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
                raise types.InvalidStatement(
                    "Invalid statement: {}".format(statement))

            keyword, body = next(iter(statement.items()))
            validater = self.STATEMENT_DISPATCH_TABLE.get(keyword)
            if not validater:
                raise types.InvalidStatement(
                    "Invalid statement keyword: {}".format(keyword))

            validater(self, body)

    def validate_expression(self, exp: str) -> wrappers.Field:
        """Validate an attribute chain expression.

        Given a lookup expression, e.g. squid.clam.whelk,
        recursively validate that each base has an attr with the name of the
        next lookup lower down and repeated attributes are indexed.

        Args:
            expr: str: The attribute expression.

        Raises:
            UndefinedVariableReference: If the root of the expression is not
                                        a previously defined lvalue.
            BadAttributeLookup: If an attribute other than the final is repeated OR
                                if an attribute in the chain is not a field of its parent.

        Returns:
            wrappers.Field: The final field in the chain.
        """
        # TODO: Add resource name handling, i.e. %
        chain_link_re = re.compile(
            r"""
            (?P<attr_name>\$?\w+)(?:\[(?P<index>\d+)\]|\{["'](?P<key>[^"']+)["']\})?$
            """.strip())

        def validate_recursively(expression, scope, depth=0):
            first_dot = expression.find(".")
            base = expression[:first_dot] if first_dot > 0 else expression
            match = chain_link_re.match(base)
            if not match:
                raise types.BadAttributeLookup(
                    f"Badly formed attribute expression: {expression}")

            name, idxed, mapped = (match.groupdict()["attr_name"],
                                   bool(match.groupdict()["index"]),
                                   bool(match.groupdict()["key"]))
            field = scope.get(name)
            if not field:
                exception_class = (types.BadAttributeLookup if depth else
                                   types.UndefinedVariableReference)
                raise exception_class(f"No such variable or attribute: {name}")

            # Invalid input
            if (idxed or mapped) and not field.repeated:
                raise types.BadAttributeLookup(
                    f"Collection lookup on non-repeated field: {base}")

            # Can only ignore indexing or mapping in an indexed (or mapped) field
            # if it is the terminal point in the expression.
            if field.repeated and not (idxed or mapped) and first_dot != -1:
                raise types.BadAttributeLookup(
                    ("Accessing attribute on a non-terminal collection without"
                     f"indexing into the collection: {base}")
                )

            message = field.message
            scope = dict(message.fields) if message else {}
            # Can only map message types, not enums
            if mapped:
                # See https://github.com/protocolbuffers/protobuf/blob/master/src/google/protobuf/descriptor.proto#L496
                # for a better understanding of how map attributes are handled in protobuf
                if not message or not message.options.map_field:
                    raise types.BadAttributeLookup(
                        f"Badly formed mapped field: {base}")

                value_field = message.fields.get("value")
                if not value_field:
                    raise types.BadAttributeLookup(
                        f"Mapped attribute has no value field: {base}")

                value_message = value_field.message
                if not value_message:
                    raise types.BadAttributeLookup(
                        f"Mapped value field is not a message: {base}")

                if first_dot != -1:
                    scope = value_message.fields

            # Terminus of the expression.
            if first_dot == -1:
                return field

            # Enums and primitives are only allowed at the tail of an expression.
            if not message:
                raise types.BadAttributeLookup(
                    f"Non-terminal attribute is not a message: {base}")

            return validate_recursively(expression[first_dot + 1:],
                                        scope,
                                        depth + 1)

        return validate_recursively(exp, self.var_defs_)

    def _handle_lvalue(self, lval: str, type_: wrappers.Field):
        """Conducts safety checks on an lvalue and adds it to the lexical scope.

        Raises:
            ReservedVariableName: If an attempted lvalue is a reserved keyword.
        """
        if lval in RESERVED_WORDS:
            raise types.ReservedVariableName(
                "Tried to define a variable with reserved name: {}".format(
                    lval)
            )

        # Even though it's valid python to reassign variables to any rvalue,
        # the samplegen spec prohibits this.
        if lval in self.var_defs_:
            raise types.RedefinedVariable(
                "Tried to redefine variable: {}".format(lval))

        self.var_defs_[lval] = type_

    def _validate_format(self, body: List[str]):
        """Validates a format string and corresponding arguments.

         The number of format tokens in the string must equal the
         number of arguments, and each argument must be a defined variable.

         Raises:
             MismatchedFormatSpecifier: If the number of format string segments ("%s") in
                                        a "print" or "comment" block does not equal the
                                        size number of strings in the block minus 1.
             UndefinedVariableReference: If the base lvalue in an expression chain
                                         is not a previously defined lvalue.
        """
        fmt_str = body[0]
        num_prints = fmt_str.count("%s")
        if num_prints != len(body) - 1:
            raise types.MismatchedFormatSpecifier(
                "Expected {} expresssions in format string but received {}".format(
                    num_prints, len(body) - 1
                )
            )

        for expression in body[1:]:
            self.validate_expression(expression)

    def _validate_define(self, body: str):
        """"Validates 'define' statements.

        Adds the defined lvalue to the lexical scope.
        Other statements can reference it.

         Raises:
             BadAssignment: If a "define" statement is badly formed lexically.
             UndefinedVariableReference: If an attempted rvalue base is a previously
                                         undeclared variable.
        """
        # Note: really checking for safety would be equivalent to
        #       re-implementing the python interpreter.
        m = re.match(r"^([a-zA-Z]\w*)=([^=]+)$", body)
        if not m:
            raise types.BadAssignment(f"Bad assignment statement: {body}")

        lval, rval = m.groups()

        rval_type = self.validate_expression(rval)
        self._handle_lvalue(lval, rval_type)

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
            raise types.InvalidStatement(
                "Missing key in 'write_file' statement: 'filename'")

        self._validate_format(fname_fmt)

        contents_var = body.get("contents")
        if not contents_var:
            raise types.InvalidStatement(
                "Missing key in 'write_file' statement: 'contents'")

        self.validate_expression(contents_var)

    @dataclasses.dataclass(frozen=True)
    class LoopParameterField(wrappers.Field):
        # This class is a hack for assigning the iteration variable in a collection loop.
        # In protobuf, the concept of collection<T> is manifested as a repeated
        # field of message type T. Therefore, in order to assign the correct type
        # to a loop iteration parameter, we copy the field that is the collection
        # but remove 'repeated'.
        repeated: bool = False

    def _validate_loop(self, loop):
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
        segments = set(loop.keys())
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
        self.var_defs_ = self.var_defs_.new_child()

        if {self.COLL_KWORD, self.VAR_KWORD, self.BODY_KWORD} == segments:
            tokens = loop[self.COLL_KWORD].split(".")

            # TODO: resolve the implicit $resp dilemma
            # if collection_name.startswith("."):
            #     collection_name = "$resp" + collection_name
            collection_field = self.validate_expression(
                loop[self.COLL_KWORD])

            if not collection_field.repeated:
                raise types.BadLoop(
                    "Tried to use a non-repeated field as a collection: {}".format(
                        tokens[-1]))

            var = loop[self.VAR_KWORD]
            # The collection_field is repeated,
            # but the iteration parameter should not be.
            self._handle_lvalue(
                var,
                self.LoopParameterField(
                    field_pb=collection_field.field_pb,
                    message=collection_field.message,
                    enum=collection_field.enum,
                    meta=collection_field.meta
                )
            )

        elif map_args <= segments:
            segments -= map_args
            segments -= {self.KEY_KWORD, self.VAL_KWORD}
            if segments:
                raise types.BadLoop(
                    "Unexpected keywords in loop statement: {}".format(
                        segments)
                )

            map_field = self.validate_expression(loop[self.MAP_KWORD])

            key = loop.get(self.KEY_KWORD)
            if key:
                self._handle_lvalue(key, map_field.message.fields["key"])

            val = loop.get(self.VAL_KWORD)
            if val:
                self._handle_lvalue(val, map_field.message.fields["value"])

            if not (key or val):
                raise types.BadLoop(
                    "Need at least one of 'key' or 'value' in a map loop")

        else:
            raise types.BadLoop("Unexpected loop form: {}".format(segments))

        self.validate_response(loop[self.BODY_KWORD])
        # Restore the previous lexical scope.
        # This is stricter than python scope rules
        # because the samplegen spec mandates it.
        self.var_defs_ = self.var_defs_.parents

    # Add new statement keywords to this table.
    STATEMENT_DISPATCH_TABLE = {
        "define": _validate_define,
        "print": _validate_format,
        "comment": _validate_format,
        "write_file": _validate_write_file,
        "loop": _validate_loop,
    }


def generate_sample(sample,
                    env: jinja2.environment.Environment,
                    api_schema: api.API,
                    template_name: str = DEFAULT_TEMPLATE_NAME) -> str:
    """Generate a standalone, runnable sample.

    Rendering and writing the rendered output is left for the caller.

    Args:
        sample (Any): A definition for a single sample generated from parsed yaml.
        env (jinja2.environment.Environment): The jinja environment used to generate
                                              the filled template for the sample.
        api_schema (api.API): The schema that defines the API to which the sample belongs.
        template_name (str): An optional override for the name of the template
                             used to generate the sample.

    Returns:
        str: The rendered sample.
    """
    sample_template = env.get_template(template_name)

    service_name = sample["service"]
    service = api_schema.services.get(service_name)
    if not service:
        raise types.UnknownService("Unknown service: {}", service_name)

    rpc_name = sample["rpc"]
    rpc = service.methods.get(rpc_name)
    if not rpc:
        raise types.RpcMethodNotFound(
            "Could not find rpc in service {}: {}".format(
                service_name, rpc_name)
        )

    calling_form = types.CallingForm.method_default(rpc)

    v = Validator(rpc)
    # Tweak some small aspects of the sample to set sane defaults for optional
    # fields, add fields that are required for the template, and so forth.
    v.preprocess_sample(sample, api_schema)
    sample["request"] = v.validate_and_transform_request(calling_form,
                                                         sample["request"])
    v.validate_response(sample["response"])

    return sample_template.render(
        file_header=FILE_HEADER,
        sample=sample,
        imports=[],
        calling_form=calling_form,
        calling_form_enum=types.CallingForm,
    )
