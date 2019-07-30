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

import yaml
import pytest

from typing import (Iterable, TypeVar)
from collections import namedtuple
from google.protobuf import descriptor_pb2

import gapic.schema.wrappers as wrappers
import gapic.samplegen.yaml as gapic_yaml
import gapic.samplegen.samplegen as samplegen

from common_types import (DummyField, DummyMessage,
                          DummyMethod, message_factory, enum_factory)
from gapic.samplegen import utils


# validate_response tests


def test_define():
    define = {"define": "squid=$resp"}
    v = samplegen.Validator(DummyMethod(output=message_factory("mollusc")))
    v.validate_response([define])


def test_define_undefined_var():
    define = {"define": "squid=humboldt"}
    v = samplegen.Validator(DummyMethod(output=message_factory("mollusc")))
    with pytest.raises(samplegen.UndefinedVariableReference):
        v.validate_response([define])


def test_define_reserved_varname():
    define = {"define": "class=$resp"}
    v = samplegen.Validator(DummyMethod(output=message_factory("mollusc")))
    with pytest.raises(samplegen.ReservedVariableName):
        v.validate_response([define])


def test_define_add_var():
    v = samplegen.Validator(DummyMethod(
        output=message_factory("mollusc.name")))
    v.validate_response([{"define": "squid=$resp"},
                         {"define": "name=squid.name"}])


def test_define_bad_form():
    define = {"define": "mollusc=$resp.squid=$resp.clam"}
    v = samplegen.Validator(DummyMethod(output=message_factory("mollusc")))
    with pytest.raises(samplegen.BadAssignment):
        v.validate_response([define])


def test_define_redefinition():
    statements = [
        {"define": "molluscs=$resp.molluscs"},
        {"define": "molluscs=$resp.molluscs"},
    ]
    v = samplegen.Validator(DummyMethod(output=message_factory("$resp.molluscs",
                                                               repeated_iter=[True])))
    with pytest.raises(samplegen.RedefinedVariable):
        v.validate_response(statements)


def test_define_input_param():
    v = samplegen.Validator(
        DummyMethod(input=message_factory("mollusc.squid.mantle_length")))
    v.validate_and_transform_request(
        utils.CallingForm.Request,
        [
            {
                "field": "squid.mantle_length",
                "value": "100 cm",
                "input_parameter": "mantle_length",
            }
        ],
    )
    v.validate_response([{"define": "length=mantle_length"}])


def test_define_input_param_redefinition():
    v = samplegen.Validator(DummyMethod(
        input=message_factory("mollusc.squid.mantle_length")))
    v.validate_and_transform_request(
        utils.CallingForm.Request,
        [
            {
                "field": "squid.mantle_length",
                "value": "100 cm",
                "input_parameter": "mantle_length",
            }
        ],
    )
    with pytest.raises(samplegen.RedefinedVariable):
        v.validate_response(
            [{"define": "mantle_length=mantle_length"}])


def test_print_basic():
    print_statement = {"print": ["This is a squid"]}
    samplegen.Validator(DummyMethod()).validate_response([print_statement])


def test_print_fmt_str():
    print_statement = {"print": ["This is a squid named %s", "$resp.name"]}
    v = samplegen.Validator(DummyMethod(output=message_factory("$resp.name")))
    v.validate_response([print_statement])


def test_print_fmt_mismatch():
    print_statement = {"print": ["This is a squid named %s"]}
    v = samplegen.Validator(DummyMethod(output=message_factory("$resp.name")))
    with pytest.raises(samplegen.MismatchedFormatSpecifier):
        v.validate_response([print_statement])


def test_print_fmt_mismatch2():
    print_statement = {"print": ["This is a squid", "$resp.name"]}
    v = samplegen.Validator(DummyMethod(output=message_factory("$resp.name")))
    with pytest.raises(samplegen.MismatchedFormatSpecifier):
        v.validate_response([print_statement])


def test_print_undefined_var():
    print_statement = {"print": ["This mollusc is a %s", "mollusc.type"]}
    v = samplegen.Validator(DummyMethod(output=message_factory("$resp.type")))
    with pytest.raises(samplegen.UndefinedVariableReference):
        v.validate_response([print_statement])


def test_comment():
    comment = {"comment": ["This is a mollusc"]}
    samplegen.Validator(DummyMethod()).validate_response([comment])


def test_comment_fmt_str():
    comment = {"comment": ["This is a mollusc of class %s", "$resp.class"]}
    samplegen.Validator(DummyMethod()).validate_response([comment])


def test_comment_fmt_undefined_var():
    comment = {"comment": ["This is a mollusc of class %s", "cephalopod"]}
    v = samplegen.Validator(DummyMethod())
    with pytest.raises(samplegen.UndefinedVariableReference):
        v.validate_response([comment])


def test_comment_fmt_mismatch():
    comment = {"comment": ["This is a mollusc of class %s"]}
    v = samplegen.Validator(DummyMethod())
    with pytest.raises(samplegen.MismatchedFormatSpecifier):
        v.validate_response([comment])


def test_comment_fmt_mismatch2():
    comment = {"comment": ["This is a mollusc of class ", "$resp.class"]}
    v = samplegen.Validator(DummyMethod())
    with pytest.raises(samplegen.MismatchedFormatSpecifier):
        v.validate_response([comment])


def test_loop_collection():
    loop = {
        "loop": {
            "collection": "$resp.molluscs",
            "variable": "m",
            "body": [{"print": ["Mollusc of class: %s", "m.class"]}],
        }
    }
    v = samplegen.Validator(DummyMethod(output=message_factory(
        "$resp.molluscs", repeated_iter=[True])))
    v.validate_response([loop])


def test_loop_collection_redefinition():
    statements = [
        {"define": "m=$resp.molluscs"},
        {
            "loop": {
                "collection": "$resp.molluscs",
                "variable": "m",
                "body": [{"print": ["Mollusc of class: %s", "m.class"]}],
            }
        },
    ]
    v = samplegen.Validator(
        DummyMethod(output=message_factory("$resp.molluscs", repeated_iter=[True])))
    with pytest.raises(samplegen.RedefinedVariable):
        v.validate_response(statements)


def test_loop_undefined_collection():
    loop = {
        "loop": {
            "collection": "squid",
            "variable": "s",
            "body": [{"print": ["Squid: %s", "s"]}],
        }
    }
    v = samplegen.Validator(DummyMethod())
    with pytest.raises(samplegen.UndefinedVariableReference):
        v.validate_response([loop])


def test_loop_collection_extra_kword():
    loop = {
        "loop": {
            "collection": "$resp.molluscs",
            "squid": "$resp.squids",
            "variable": "m",
            "body": [{"print": ["Mollusc of class: %s", "m.class"]}],
        }
    }
    v = samplegen.Validator(DummyMethod())
    with pytest.raises(samplegen.BadLoop):
        v.validate_response([loop])


def test_loop_collection_missing_kword():
    loop = {
        "loop": {
            "collection": "$resp.molluscs",
            "body": [{"print": ["Mollusc of class: %s", "m.class"]}],
        }
    }
    v = samplegen.Validator(DummyMethod())
    with pytest.raises(samplegen.BadLoop):
        v.validate_response([loop])


def test_loop_collection_reserved_loop_var():
    loop = {
        "loop": {
            "collection": "$resp.molluscs",
            "variable": "class",
            "body": [{"print": ["Mollusc: %s", "class.name"]}],
        }
    }
    v = samplegen.Validator(DummyMethod(
        output=message_factory("$resp.molluscs", repeated_iter=[True])))
    with pytest.raises(samplegen.ReservedVariableName):
        v.validate_response([loop])


def test_loop_map():
    loop = {
        "loop": {
            "map": "$resp.molluscs",
            "key": "cls",
            "value": "mollusc",
            "body": [{"print": ["A %s is a %s", "mollusc", "cls"]}],
        }
    }
    samplegen.Validator(DummyMethod()).validate_response([loop])


def test_collection_loop_lexical_scope_variable():
    statements = [
        {
            "loop": {
                "collection": "$resp.molluscs",
                "variable": "m",
                "body": [{"define": "squid=m"}],
            }
        },
        {"define": "cephalopod=m"},
    ]
    v = samplegen.Validator(DummyMethod(
        output=message_factory("$resp.molluscs", repeated_iter=[True])))
    with pytest.raises(samplegen.UndefinedVariableReference):
        v.validate_response(statements)


def test_collection_loop_lexical_scope_inline():
    statements = [
        {
            "loop": {
                "collection": "$resp.molluscs",
                "variable": "m",
                "body": [{"define": "squid=m"}],
            }
        },
        {"define": "cephalopod=squid"},
    ]
    v = samplegen.Validator(DummyMethod(
        output=message_factory("$resp.molluscs", repeated_iter=[True])))
    with pytest.raises(samplegen.UndefinedVariableReference):
        v.validate_response(statements)


def test_map_loop_lexical_scope_key():
    statements = [
        {
            "loop": {
                "map": "$resp.molluscs",
                "key": "cls",
                "value": "order",
                "body": [{"define": "tmp=cls"}],
            }
        },
        {"define": "last_cls=cls"},
    ]
    v = samplegen.Validator(DummyMethod())
    with pytest.raises(samplegen.UndefinedVariableReference):
        v.validate_response(statements)


def test_map_loop_lexical_scope_value():
    statements = [
        {
            "loop": {
                "map": "$resp.molluscs",
                "key": "cls",
                "value": "order",
                "body": [{"define": "tmp=order"}],
            }
        },
        {"define": "last_order=order"},
    ]
    v = samplegen.Validator(DummyMethod())
    with pytest.raises(samplegen.UndefinedVariableReference):
        v.validate_response(statements)


def test_map_loop_lexical_scope_inline():
    statements = [
        {
            "loop": {
                "map": "$resp.molluscs",
                "key": "cls",
                "value": "order",
                "body": [{"define": "tmp=order"}],
            }
        },
        {"define": "last_order=tmp"},
    ]
    v = samplegen.Validator(DummyMethod())
    with pytest.raises(samplegen.UndefinedVariableReference):
        v.validate_response(statements)


def test_loop_map_reserved_key():
    loop = {
        "loop": {
            "map": "$resp.molluscs",
            "key": "class",
            "value": "mollusc",
            "body": [{"print": ["A %s is a %s", "mollusc", "class"]}],
        }
    }
    v = samplegen.Validator(DummyMethod())
    with pytest.raises(samplegen.ReservedVariableName):
        v.validate_response([loop])


def test_loop_map_reserved_val():
    loop = {
        "loop": {
            "map": "$resp.molluscs",
            "key": "m",
            "value": "class",
            "body": [{"print": ["A %s is a %s", "m", "class"]}],
        }
    }
    v = samplegen.Validator(DummyMethod())
    with pytest.raises(samplegen.ReservedVariableName):
        v.validate_response([loop])


def test_loop_map_undefined():
    loop = {
        "loop": {
            "map": "molluscs",
            "key": "name",
            "value": "mollusc",
            "body": [{"print": ["A %s is a %s", "mollusc", "name"]}],
        }
    }
    v = samplegen.Validator(DummyMethod())
    with pytest.raises(samplegen.UndefinedVariableReference):
        v.validate_response([loop])


def test_loop_map_no_key():
    loop = {
        "loop": {
            "map": "$resp.molluscs",
            "value": "mollusc",
            "body": [{"print": ["Mollusc: %s", "mollusc"]}],
        }
    }
    samplegen.Validator(DummyMethod()).validate_response([loop])


def test_loop_map_no_value():
    loop = {
        "loop": {
            "map": "$resp.molluscs",
            "key": "mollusc",
            "body": [{"print": ["Mollusc: %s", "mollusc"]}],
        }
    }
    samplegen.Validator(DummyMethod()).validate_response([loop])


def test_loop_map_no_key_or_value():
    loop = {"loop": {"map": "$resp.molluscs",
                     "body": [{"print": ["Dead loop"]}]}}
    v = samplegen.Validator(DummyMethod())
    with pytest.raises(samplegen.BadLoop):
        v.validate_response([loop])


def test_loop_map_no_map():
    loop = {
        "loop": {
            "key": "name",
            "value": "mollusc",
            "body": [{"print": ["A %s is a %s", "mollusc", "name"]}],
        }
    }
    v = samplegen.Validator(DummyMethod())
    with pytest.raises(samplegen.BadLoop):
        v.validate_response([loop])


def test_loop_map_no_body():
    loop = {"loop": {"map": "$resp.molluscs", "key": "name", "value": "mollusc"}}
    v = samplegen.Validator(DummyMethod())
    with pytest.raises(samplegen.BadLoop):
        v.validate_response([loop])


def test_loop_map_extra_kword():
    loop = {
        "loop": {
            "map": "$resp.molluscs",
            "key": "name",
            "value": "mollusc",
            "phylum": "$resp.phylum",
            "body": [{"print": ["A %s is a %s", "mollusc", "name"]}],
        }
    }
    v = samplegen.Validator(DummyMethod())
    with pytest.raises(samplegen.BadLoop):
        v.validate_response([loop])


def test_loop_map_redefined_key():
    statements = [
        {"define": "mollusc=$resp.molluscs"},
        {
            "loop": {
                "map": "$resp.molluscs",
                "key": "mollusc",
                "body": [{"print": ["Mollusc: %s", "mollusc"]}],
            }
        },
    ]
    v = samplegen.Validator(DummyMethod(
        output=message_factory("mollusc.molluscs")))
    with pytest.raises(samplegen.RedefinedVariable):
        v.validate_response(statements)


def test_loop_map_redefined_value():
    statements = [
        {"define": "mollusc=$resp.molluscs"},
        {
            "loop": {
                "map": "$resp.molluscs",
                "value": "mollusc",
                "body": [{"print": ["Mollusc: %s", "mollusc"]}],
            }
        },
    ]
    v = samplegen.Validator(DummyMethod(
        output=message_factory("mollusc.molluscs")))
    with pytest.raises(samplegen.RedefinedVariable):
        v.validate_response(statements)


def test_validate_write_file():
    statements = [
        {
            "write_file": {
                "filename": ["specimen-%s", "$resp.species"],
                "contents": "$resp.photo",
            }
        }
    ]
    samplegen.Validator(DummyMethod()).validate_response(statements)


def test_validate_write_file_fname_fmt():
    statements = [{"write_file":
                   {"filename": ["specimen-%s"], "contents": "$resp.photo"}}]
    v = samplegen.Validator(DummyMethod())
    with pytest.raises(samplegen.MismatchedFormatSpecifier):
        v.validate_response(statements)


def test_validate_write_file_fname_bad_var():
    statements = [{
        "write_file": {
            "filename": ["specimen-%s", "squid.species"],
            "contents": "$resp.photo",
        }
    }]
    v = samplegen.Validator(DummyMethod())
    with pytest.raises(samplegen.UndefinedVariableReference):
        v.validate_response(statements)


def test_validate_write_file_missing_fname():
    statements = [{"write_file": {"contents": "$resp.photo"}}]
    v = samplegen.Validator(DummyMethod())
    with pytest.raises(samplegen.InvalidStatement):
        v.validate_response(statements)


def test_validate_write_file_missing_contents():
    statements = [{"write_file": {"filename": ["specimen-%s",
                                               "$resp.species"]}}]
    v = samplegen.Validator(DummyMethod())
    with pytest.raises(samplegen.InvalidStatement):
        v.validate_response(statements)


def test_validate_write_file_bad_contents_var():
    statements = [{
        "write_file": {
            "filename": ["specimen-%s", "$resp.species"],
            "contents": "squid.photo",
        }
    }]
    v = samplegen.Validator(DummyMethod())
    with pytest.raises(samplegen.UndefinedVariableReference):
        v.validate_response(statements)


def test_invalid_statement():
    statements = [{"print": ["Name"], "comment": ["Value"]}]
    v = samplegen.Validator(DummyMethod())
    with pytest.raises(samplegen.InvalidStatement):
        v.validate_response(statements)


def test_invalid_statement2():
    statements = [{"squidify": ["Statement body"]}]
    v = samplegen.Validator(DummyMethod())
    with pytest.raises(samplegen.InvalidStatement):
        v.validate_response(statements)


# validate_and_transform_request tests
def test_validate_request_basic():
    input_type = DummyMessage(
        fields={
            "squid": DummyField(
                message=DummyMessage(
                    fields={
                        "mantle_length": DummyField(
                            message=DummyMessage(type="LENGTH_TYPE")),
                        "mantle_mass": DummyField(
                            message=DummyMessage(type="MASS_TYPE"))},
                    type="SQUID_TYPE"
                )
            )
        },
        type="REQUEST_TYPE"
    )

    v = samplegen.Validator(DummyMethod(input=input_type))
    actual = v.validate_and_transform_request(
        utils.CallingForm.Request,
        [
            {"field": "squid.mantle_length", "value": "100 cm"},
            {"field": "squid.mantle_mass", "value": "10 kg"},
        ],
    )
    expected = [samplegen.TransformedRequest(
        base="squid",
        body=[
                samplegen.AttributeRequestSetup(field="mantle_length",
                                                value="100 cm"),
                samplegen.AttributeRequestSetup(field="mantle_mass",
                                                value="10 kg"),
                ],
        single=None
    )]

    assert actual == expected


def test_validate_request_no_field_parameter():
    # May need to remeove this test because it doesn't necessarily make sense any more.
    v = samplegen.Validator(DummyMethod())
    with pytest.raises(samplegen.InvalidRequestSetup):
        v.validate_and_transform_request(
            utils.CallingForm.Request, [{"squid": "humboldt",
                                         "value": "teuthida"}]
        )


def test_validate_request_no_such_attribute():
    v = samplegen.Validator(DummyMethod(
        input=message_factory("mollusc.squid.mantle")))
    with pytest.raises(samplegen.BadAttributeLookup):
        v.validate_and_transform_request(
            utils.CallingForm.Request,
            [{"field": "clam.shell", "value": "20"}]
        )


def test_validate_request_top_level_field():
    v = samplegen.Validator(DummyMethod(
        input=message_factory("mollusc.squid")))
    actual = v.validate_and_transform_request(
        utils.CallingForm.Request,
        [{"field": "squid", "value": "humboldt"}]
    )

    expected = [
        samplegen.TransformedRequest(base="squid",
                                     body=None,
                                     single=samplegen.AttributeRequestSetup(
                                         value="humboldt"
                                     ))
    ]

    assert actual == expected


def test_validate_request_missing_keyword(kword="field"):
    v = samplegen.Validator(DummyMethod(
        input=message_factory("mollusc.squid")))
    with pytest.raises(samplegen.InvalidRequestSetup):
        v.validate_and_transform_request(
            utils.CallingForm.Request,
            [{kword: "squid"}]
        )


def test_validate_request_missing_value():
    test_validate_request_missing_keyword(kword="value")


def test_validate_request_spurious_kword():
    v = samplegen.Validator(
        DummyMethod(input=message_factory("mollusc.squid")))
    with pytest.raises(samplegen.InvalidRequestSetup):
        v.validate_and_transform_request(
            utils.CallingForm.Request,
            [{"field": "mollusc.squid", "value": "humboldt", "order": "teuthida"}]
        )


def test_validate_request_unknown_field_type():
    v = samplegen.Validator(DummyMethod(
        input=DummyMessage(fields={"squid": DummyField()})))
    with pytest.raises(TypeError):
        v.validate_and_transform_request(
            utils.CallingForm.Request,
            [{"field": "squid", "value": "humboldt"}]
        )


def test_validate_request_duplicate_top_level_fields():
    v = samplegen.Validator(DummyMethod(
        input=message_factory("mollusc.squid")))
    with pytest.raises(samplegen.InvalidRequestSetup):
        v.validate_and_transform_request(
            utils.CallingForm.Request,
            [{"field": "squid", "value": "humboldt"},
             {"field": "squid", "value": "bobtail"}]
        )


def test_validate_request_multiple_arguments():
    input_type = DummyMessage(
        fields={
            "squid": DummyField(
                message=DummyMessage(
                    fields={"mantle_length": DummyField(
                        message=DummyMessage(type="LENGTH_TYPE"))},
                    type="SQUID_TYPE"
                )
            ),
            "clam": DummyField(
                message=DummyMessage(
                    fields={"shell_mass": DummyField(
                        message=DummyMessage(type="MASS_TYPE"))},
                    type="CLAM_TYPE"
                )
            ),
        },
        type="REQUEST_TYPE"
    )

    v = samplegen.Validator(DummyMethod(input=input_type))
    actual = v.validate_and_transform_request(
        utils.CallingForm.Request,
        [
            {
                "field": "squid.mantle_length",
                "value": "100 cm", "value_is_file": True
            },
            {
                "field": "clam.shell_mass",
                "value": "100 kg",
                "comment": "Clams can be large",
            },
        ],
    )
    expected = [
        samplegen.TransformedRequest(
            base="squid",
            body=[samplegen.AttributeRequestSetup(
                field="mantle_length",
                value="100 cm",
                value_is_file=True)],
            single=None
        ),
        samplegen.TransformedRequest(
            base="clam",
            body=[samplegen.AttributeRequestSetup(
                field="shell_mass",
                value="100 kg",
                comment="Clams can be large")],
            single=None
        ),
    ]

    assert actual == expected


def test_validate_request_duplicate_input_param():
    input_type = DummyMessage(
        fields={
            "squid": DummyField(
                message=DummyMessage(
                    fields={"mantle_mass": DummyField(
                        message=DummyMessage(type="MASS_TYPE"))},
                    type="SQUID_TYPE"
                )
            ),
            "clam": DummyField(
                message=DummyMessage(
                    fields={"mantle_mass": DummyField(
                        message=DummyMessage(type="MASS_TYPE"))},
                    type="CLAM_TYPE"
                )
            ),
        },
        type="REQUEST_TYPE"
    )

    v = samplegen.Validator(DummyMethod(input=input_type))
    with pytest.raises(samplegen.RedefinedVariable):
        v.validate_and_transform_request(
            utils.CallingForm.Request,
            [
                {
                    "field": "squid.mantle_mass",
                    "value": "10 kg",
                    "input_parameter": "mantle_mass",
                },
                {
                    "field": "clam.mantle_mass",
                    "value": "1 kg",
                    "input_parameter": "mantle_mass",
                },
            ],
        )


def test_validate_request_reserved_input_param():
    v = samplegen.Validator(DummyMethod())
    with pytest.raises(samplegen.ReservedVariableName):
        v.validate_and_transform_request(
            utils.CallingForm.Request,
            [
                {
                    "field": "mollusc.class",
                    "value": "cephalopoda",
                    "input_parameter": "class",
                }
            ],
        )


def test_single_request_client_streaming(
        calling_form=utils.CallingForm.RequestStreamingClient):
    # Each API client method really only takes one parameter:
    # either a single protobuf message or an iterable of protobuf messages.
    # With unary request methods, python lets us describe attributes as positional
    # and keyword parameters, which simplifies request construction.
    # The 'base' in the transformed request refers to an attribute, and the
    # 'field's refer to sub-attributes.
    # Client streaming and bidirectional streaming methods can't use this notation,
    # and generate an exception if there is more than one 'base'.
    input_type = DummyMessage(
        fields={
            "cephalopod": DummyField(
                message=DummyMessage(
                    fields={
                        "order": DummyField(
                            message=DummyMessage(type="ORDER_TYPE")
                        )
                    },
                    type="CEPHALOPOD_TYPE"
                )
            ),
            "gastropod": DummyField(
                message=DummyMessage(
                    fields={
                        "order": DummyField(
                            message=DummyMessage(type="ORDER_TYPE")
                        )
                    },
                    type="GASTROPOD_TYPE"
                )
            )
        },
        type="MOLLUSC_TYPE"
    )
    v = samplegen.Validator(DummyMethod(input=input_type))
    with pytest.raises(samplegen.InvalidRequestSetup):
        v.validate_and_transform_request(
            utils.CallingForm.RequestStreamingClient,
            [
                {"field": "cephalopod.order", "value": "cephalopoda"},
                {"field": "gastropod.order", "value": "pulmonata"},
            ],
        )


def test_single_request_bidi_streaming():
    test_single_request_client_streaming(
        utils.CallingForm.RequestStreamingBidi)


def test_validate_request_calling_form():
    assert (
        utils.CallingForm.method_default(DummyMethod(lro=True))
        == utils.CallingForm.LongRunningRequestPromise
    )

    assert (
        utils.CallingForm.method_default(DummyMethod(paged_result_field=True))
        == utils.CallingForm.RequestPagedAll
    )

    assert (
        utils.CallingForm.method_default(DummyMethod(client_streaming=True))
        == utils.CallingForm.RequestStreamingClient
    )

    assert (
        utils.CallingForm.method_default(DummyMethod(server_streaming=True))
        == utils.CallingForm.RequestStreamingServer
    )

    assert utils.CallingForm.method_default(
        DummyMethod()) == utils.CallingForm.Request

    assert (
        utils.CallingForm.method_default(
            DummyMethod(client_streaming=True, server_streaming=True)
        )
        == utils.CallingForm.RequestStreamingBidi
    )


def test_coerce_response_name():
    # Don't really need a test, but it shuts up code coverage.
    assert samplegen.coerce_response_name("$resp.squid") == "response.squid"
    assert samplegen.coerce_response_name("mollusc.squid") == "mollusc.squid"


def test_regular_response_type():
    OutputType = TypeVar("OutputType")
    method = DummyMethod(output=OutputType)

    v = samplegen.Validator(method)
    assert v.var_field("$resp").message == OutputType


def test_paged_response_type():
    OutputType = TypeVar("OutputType")
    PagedType = TypeVar("PagedType")
    method = DummyMethod(output=OutputType, paged_result_field=PagedType)

    v = samplegen.Validator(method)
    assert v.var_field("$resp").message == PagedType


def test_lro_response_type():
    OutputType = TypeVar("OutputType")
    LroType = TypeVar("LroType")
    method = DummyMethod(
        output=OutputType, lro=namedtuple(
            "operation", ["response_type"])(LroType)
    )

    v = samplegen.Validator(method)
    assert v.var_field("$resp").message == LroType


def test_validate_expression():
    exp = "$resp.coleoidea.octopodiformes.octopus"
    OutputType = message_factory(exp)
    method = DummyMethod(output=OutputType)
    v = samplegen.Validator(method)

    exp_type = v.validate_expression(exp)
    assert exp_type.message.type == "OCTOPUS_TYPE"


def test_validate_expression_undefined_base():
    exp = "$resp.coleoidea.octopodiformes.octopus"
    OutputType = message_factory(exp)
    method = DummyMethod(output=OutputType)
    v = samplegen.Validator(method)

    with pytest.raises(samplegen.UndefinedVariableReference):
        v.validate_expression("mollusc")


def test_validate_expression_no_such_attr():
    OutputType = message_factory("$resp.coleoidea")
    method = DummyMethod(output=OutputType)
    v = samplegen.Validator(method)

    with pytest.raises(samplegen.BadAttributeLookup):
        v.validate_expression("$resp.nautiloidea")


def test_validate_expression_predefined():
    # TODO: can't remember what this test does
    exp = "$resp.coleoidea.octopodiformes.octopus"
    OutputType = message_factory(exp)
    method = DummyMethod(output=OutputType)
    v = samplegen.Validator(method)

    with pytest.raises(samplegen.BadAttributeLookup):
        v.validate_response([{"define": "nautilus=$resp.nautiloidea"}])


def test_validate_expression_repeated_attrs():
    # This is a little tricky: there's an attribute hierarchy
    # of response/coleoidea/octopodiformes, but coleoidea is a repeated field,
    # so accessing $resp.coleoidea.octopodiformes doesn't make any sense.
    exp = "$resp.coleoidea.octopodiformes"
    OutputType = message_factory(exp, repeated_iter=[True, False])
    method = DummyMethod(output=OutputType)
    v = samplegen.Validator(method)

    with pytest.raises(samplegen.BadAttributeLookup):
        v.validate_response(
            [{"define": "octopus=$resp.coleoidea.octopodiformes"}])


def test_validate_expression_collection():
    exp = "$resp.molluscs"
    OutputType = message_factory(exp, repeated_iter=[True])
    method = DummyMethod(output=OutputType)
    v = samplegen.Validator(method)
    v.validate_response(
        [
            {
                "loop": {
                    "collection": "$resp.molluscs",
                    "variable": "m",
                    "body": [{"print": ["%s", "m"]}],
                }
            }
        ]
    )


def test_validate_expression_collection_error():
    exp = "$resp.molluscs.mollusc"
    OutputType = message_factory(exp)
    method = DummyMethod(output=OutputType)

    statement = {
        "loop": {
            "collection": "$resp.molluscs",
            "variable": "m",
            "body": [{"print": ["%s", "m"]}],
        }
    }

    v = samplegen.Validator(method)

    # Because 'molluscs' isn't repeated
    with pytest.raises(samplegen.BadLoop):
        v.validate_response([statement])


def test_validate_expression_repeated_lookup():
    exp = "$resp.molluscs.mantle"
    OutputType = message_factory(exp, repeated_iter=[True, False])
    method = DummyMethod(output=OutputType)
    v = samplegen.Validator(method)
    v.validate_expression("$resp.molluscs[0].mantle")


def test_validate_expression_repeated_lookup_nested():
    exp = "$resp.molluscs.tentacles.club"
    OutputType = message_factory(exp, [True, True, False])
    method = DummyMethod(output=OutputType)
    v = samplegen.Validator(method)
    v.validate_expression("$resp.molluscs[0].tentacles[0].club")


def test_validate_expression_repeated_lookup_invalid():
    exp = "$resp.molluscs.mantle"
    OutputType = message_factory(exp)
    method = DummyMethod(output=OutputType)
    v = samplegen.Validator(method)
    with pytest.raises(samplegen.BadAttributeLookup):
        v.validate_expression("$resp.molluscs[0].mantle")


def test_validate_expression_base_attr_is_repeated():
    exp = "$resp.molluscs.mantle"
    OutputType = message_factory(exp, repeated_iter=[True, False])
    method = DummyMethod(output=OutputType)
    v = samplegen.Validator(method)
    v.validate_response([{"define": "molluscs=$resp.molluscs"}])
    v.validate_expression("molluscs[0].mantle")


def test_validate_expresssion_lookup_unrepeated_base():
    exp = "$resp.molluscs"
    OutputType = message_factory(exp)
    method = DummyMethod(output=OutputType)
    v = samplegen.Validator(method)
    with pytest.raises(samplegen.BadAttributeLookup):
        v.validate_response([{"define": "m=$resp[0]"}])


def test_validate_expression_malformed_base():
    # Note the mistype
    exp = "r$esp.mollusc"
    OutputType = message_factory(exp)
    method = DummyMethod(OutputType)
    v = samplegen.Validator(method)
    with pytest.raises(samplegen.BadAttributeLookup):
        v.validate_expression(exp)


def test_validate_expression_malformed_attr():
    # Note the mistype
    exp = "$resp.mollu$c"
    OutputType = message_factory(exp)
    method = DummyMethod(OutputType)
    v = samplegen.Validator(method)
    with pytest.raises(samplegen.BadAttributeLookup):
        v.validate_expression(exp)


def test_validate_request_enum():
    enum = enum_factory("subclass", ["AMMONOIDEA", "COLEOIDEA", "NAUTILOIDEA"])
    request_type = message_factory("mollusc.cephalopod.subclass", enum=enum)

    v = samplegen.Validator(DummyMethod(input=request_type))
    actual = v.validate_and_transform_request(
        utils.CallingForm.Request,
        [{"field": "cephalopod.subclass", "value": "COLEOIDEA"}]
    )
    expected = [samplegen.TransformedRequest(
        "cephalopod",
        body=[samplegen.AttributeRequestSetup(field="subclass",
                                              value="'COLEOIDEA'")],
        single=None)]
    assert actual == expected


def test_validate_request_enum_top_level():
    enum = enum_factory("subclass", ["AMMONOIDEA", "COLEOIDEA", "NAUTILOIDEA"])
    request_type = message_factory("mollusc.subclass", enum=enum)

    v = samplegen.Validator(DummyMethod(input=request_type))
    actual = v.validate_and_transform_request(
        utils.CallingForm.Request,
        [{"field": "subclass", "value": "COLEOIDEA"}]
    )
    expected = [samplegen.TransformedRequest(
        "subclass",
        single=samplegen.AttributeRequestSetup(value="'COLEOIDEA'"),
        body=None)]
    assert actual == expected


def test_validate_request_enum_invalid_value():
    enum = enum_factory("subclass", ["AMMONOIDEA", "COLEOIDEA", "NAUTILOIDEA"])
    request_type = message_factory("mollusc.cephalopod.subclass", enum=enum)
    v = samplegen.Validator(DummyMethod(output=message_factory("mollusc_result"),
                                        input=request_type))
    with pytest.raises(samplegen.InvalidEnumVariant):
        v.validate_and_transform_request(
            utils.CallingForm.Request,
            # Heterodonta are bivalves, not cephalopods
            [{"field": "cephalopod.subclass", "value": "HETERODONTA"}]
        )


def test_validate_request_enum_not_last_attr():
    enum = enum_factory("subclass", ["AMMONOIDEA", "COLEOIDEA", "NAUTILOIDEA"])
    request_type = message_factory("mollusc.subclass", enum=enum)
    v = samplegen.Validator(DummyMethod(output=message_factory("mollusc_result"),
                                        input=request_type))
    with pytest.raises(samplegen.InvalidEnumVariant):
        v.validate_and_transform_request(
            utils.CallingForm.Request,
            [{"field": "subclass.order", "value": "COLEOIDEA"}]
        )
