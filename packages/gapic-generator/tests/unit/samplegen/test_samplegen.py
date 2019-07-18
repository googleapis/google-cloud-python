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

import pytest
import yaml
from collections import namedtuple
from textwrap import dedent

import gapic.samplegen.samplegen as samplegen
import gapic.samplegen.yaml as gapic_yaml


from gapic.samplegen import utils

# validate_response tests


def test_define():
    define = {"define": "squid=$resp"}
    samplegen.Validator().validate_response([define])


def test_define_undefined_var():
    define = {"define": "squid=humboldt"}
    with pytest.raises(samplegen.UndefinedVariableReference):
        samplegen.Validator().validate_response([define])


def test_define_reserved_varname():
    define = {"define": "class=$resp"}
    with pytest.raises(samplegen.ReservedVariableName):
        samplegen.Validator().validate_response([define])


def test_define_add_var():
    samplegen.Validator().validate_response([{"define": "squid=$resp"},
                                             {"define": "name=squid.name"}])


def test_define_bad_form():
    define = {"define": "mollusc=$resp.squid=$resp.clam"}
    with pytest.raises(samplegen.BadAssignment):
        samplegen.Validator().validate_response([define])


def test_define_redefinition():
    statements = [{"define": "molluscs=$resp.molluscs"},
                  {"define": "molluscs=$resp.molluscs"}]
    with pytest.raises(samplegen.RedefinedVariable):
        samplegen.Validator().validate_response(statements)


def test_define_input_param():
    validator = samplegen.Validator()
    validator.validate_and_transform_request(utils.CallingForm.Request,
                                             [{"field": "squid.mantle_length",
                                               "value": "100 cm",
                                               "input_parameter": "mantle_length"}])
    validator.validate_response([{"define": "length=mantle_length"}])


def test_define_input_param_redefinition():
    validator = samplegen.Validator()
    validator.validate_and_transform_request(utils.CallingForm.Request,
                                             [{"field": "squid.mantle_length",
                                               "value": "100 cm",
                                               "input_parameter": "mantle_length"}])
    with pytest.raises(samplegen.RedefinedVariable):
        validator.validate_response(
            [{"define": "mantle_length=mantle_length"}])


def test_print_basic():
    print_statement = {"print": ["This is a squid"]}
    samplegen.Validator().validate_response([print_statement])


def test_print_fmt_str():
    print_statement = {"print": ["This is a squid named %s", "$resp.name"]}
    samplegen.Validator().validate_response([print_statement])


def test_print_fmt_mismatch():
    print_statement = {"print": ["This is a squid named %s"]}
    with pytest.raises(samplegen.MismatchedFormatSpecifier):
        samplegen.Validator().validate_response([print_statement])


def test_print_fmt_mismatch2():
    print_statement = {"print": ["This is a squid", "$resp.name"]}
    with pytest.raises(samplegen.MismatchedFormatSpecifier):
        samplegen.Validator().validate_response([print_statement])


def test_print_undefined_var():
    print_statement = {"print": ["This mollusc is a %s", "mollusc.type"]}
    with pytest.raises(samplegen.UndefinedVariableReference):
        samplegen.Validator().validate_response([print_statement])


def test_comment():
    comment = {"comment": ["This is a mollusc"]}
    samplegen.Validator().validate_response([comment])


def test_comment_fmt_str():
    comment = {"comment": ["This is a mollusc of class %s", "$resp.class"]}
    samplegen.Validator().validate_response([comment])


def test_comment_fmt_undefined_var():
    comment = {"comment": ["This is a mollusc of class %s", "cephalopod"]}
    with pytest.raises(samplegen.UndefinedVariableReference):
        samplegen.Validator().validate_response([comment])


def test_comment_fmt_mismatch():
    comment = {"comment": ["This is a mollusc of class %s"]}
    with pytest.raises(samplegen.MismatchedFormatSpecifier):
        samplegen.Validator().validate_response([comment])


def test_comment_fmt_mismatch2():
    comment = {"comment": ["This is a mollusc of class ", "$resp.class"]}
    with pytest.raises(samplegen.MismatchedFormatSpecifier):
        samplegen.Validator().validate_response([comment])


def test_loop_collection():
    loop = {"loop": {"collection": "$resp.molluscs",
                     "variable": "m",
                     "body": [{"print":
                               ["Mollusc of class: %s", "m.class"]}]}}
    samplegen.Validator().validate_response([loop])


def test_loop_collection_redefinition():
    statements = [{"define": "m=$resp.molluscs"},
                  {"loop": {"collection": "$resp.molluscs",
                            "variable": "m",
                            "body": [{"print": ["Mollusc of class: %s",
                                                "m.class"]}]}}]
    with pytest.raises(samplegen.RedefinedVariable):
        samplegen.Validator().validate_response(statements)


def test_loop_undefined_collection():
    loop = {"loop": {"collection": "squid",
                     "variable": "s",
                     "body": [{"print":
                               ["Squid: %s", "s"]}]}}
    with pytest.raises(samplegen.UndefinedVariableReference):
        samplegen.Validator().validate_response([loop])


def test_loop_collection_extra_kword():
    loop = {"loop": {"collection": "$resp.molluscs",
                     "squid": "$resp.squids",
                     "variable": "m",
                     "body": [{"print":
                               ["Mollusc of class: %s", "m.class"]}]}}
    with pytest.raises(samplegen.BadLoop):
        samplegen.Validator().validate_response([loop])


def test_loop_collection_missing_kword():
    loop = {"loop": {"collection": "$resp.molluscs",
                     "body": [{"print":
                               ["Mollusc of class: %s", "m.class"]}]}}
    with pytest.raises(samplegen.BadLoop):
        samplegen.Validator().validate_response([loop])


def test_loop_collection_reserved_loop_var():
    loop = {"loop": {"collection": "$resp.molluscs",
                     "variable": "class",
                     "body": [{"print":
                               ["Mollusc: %s", "class.name"]}]}}
    with pytest.raises(samplegen.ReservedVariableName):
        samplegen.Validator().validate_response([loop])


def test_loop_map():
    loop = {"loop": {"map": "$resp.molluscs",
                     "key": "cls",
                     "value": "mollusc",
                     "body": [{"print": ["A %s is a %s", "mollusc", "cls"]}]}}
    samplegen.Validator().validate_response([loop])


def test_collection_loop_lexical_scope_variable():
    statements = [{"loop": {"collection": "$resp.molluscs",
                            "variable": "m",
                            "body": [{"define": "squid=m"}]}},
                  {"define": "cephalopod=m"}]
    with pytest.raises(samplegen.UndefinedVariableReference):
        samplegen.Validator().validate_response(statements)


def test_collection_loop_lexical_scope_inline():
    statements = [{"loop": {"collection": "$resp.molluscs",
                            "variable": "m",
                            "body": [{"define": "squid=m"}]}},
                  {"define": "cephalopod=squid"}]
    with pytest.raises(samplegen.UndefinedVariableReference):
        samplegen.Validator().validate_response(statements)


def test_map_loop_lexical_scope_key():
    statements = [{"loop": {"map": "$resp.molluscs",
                            "key": "cls",
                            "value": "order",
                            "body": [{"define": "tmp=cls"}]}},
                  {"define": "last_cls=cls"}]
    with pytest.raises(samplegen.UndefinedVariableReference):
        samplegen.Validator().validate_response(statements)


def test_map_loop_lexical_scope_value():
    statements = [{"loop": {"map": "$resp.molluscs",
                            "key": "cls",
                            "value": "order",
                            "body": [{"define": "tmp=order"}]}},
                  {"define": "last_order=order"}]
    with pytest.raises(samplegen.UndefinedVariableReference):
        samplegen.Validator().validate_response(statements)


def test_map_loop_lexical_scope_inline():
    statements = [{"loop": {"map": "$resp.molluscs",
                            "key": "cls",
                            "value": "order",
                            "body": [{"define": "tmp=order"}]}},
                  {"define": "last_order=tmp"}]
    with pytest.raises(samplegen.UndefinedVariableReference):
        samplegen.Validator().validate_response(statements)


def test_loop_map_reserved_key():
    loop = {"loop": {"map": "$resp.molluscs",
                     "key": "class",
                     "value": "mollusc",
                     "body": [{"print": ["A %s is a %s", "mollusc", "class"]}]}}
    with pytest.raises(samplegen.ReservedVariableName):
        samplegen.Validator().validate_response([loop])


def test_loop_map_reserved_val():
    loop = {"loop": {"map": "$resp.molluscs",
                     "key": "m",
                     "value": "class",
                     "body": [{"print": ["A %s is a %s", "m", "class"]}]}}
    with pytest.raises(samplegen.ReservedVariableName):
        samplegen.Validator().validate_response([loop])


def test_loop_map_undefined():
    loop = {"loop": {"map": "molluscs",
                     "key": "name",
                     "value": "mollusc",
                     "body": [{"print": ["A %s is a %s", "mollusc", "name"]}]}}
    with pytest.raises(samplegen.UndefinedVariableReference):
        samplegen.Validator().validate_response([loop])


def test_loop_map_no_key():
    loop = {"loop": {"map": "$resp.molluscs",
                     "value": "mollusc",
                     "body": [{"print": ["Mollusc: %s", "mollusc"]}]}}
    samplegen.Validator().validate_response([loop])


def test_loop_map_no_value():
    loop = {"loop": {"map": "$resp.molluscs",
                     "key": "mollusc",
                     "body": [{"print": ["Mollusc: %s", "mollusc"]}]}}
    samplegen.Validator().validate_response([loop])


def test_loop_map_no_key_or_value():
    loop = {"loop": {"map": "$resp.molluscs",
                     "body": [{"print": ["Dead loop"]}]}}
    with pytest.raises(samplegen.BadLoop):
        samplegen.Validator().validate_response([loop])


def test_loop_map_no_map():
    loop = {"loop": {"key": "name",
                     "value": "mollusc",
                     "body": [{"print": ["A %s is a %s", "mollusc", "name"]}]}}
    with pytest.raises(samplegen.BadLoop):
        samplegen.Validator().validate_response([loop])


def test_loop_map_no_body():
    loop = {"loop": {"map": "$resp.molluscs",
                     "key": "name",
                     "value": "mollusc"}}
    with pytest.raises(samplegen.BadLoop):
        samplegen.Validator().validate_response([loop])


def test_loop_map_extra_kword():
    loop = {"loop": {"map": "$resp.molluscs",
                     "key": "name",
                     "value": "mollusc",
                     "phylum": "$resp.phylum",
                     "body": [{"print": ["A %s is a %s", "mollusc", "name"]}]}}
    with pytest.raises(samplegen.BadLoop):
        samplegen.Validator().validate_response([loop])


def test_loop_map_redefined_key():
    statements = [{"define": "mollusc=$resp.molluscs"},
                  {"loop": {"map": "$resp.molluscs",
                            "key": "mollusc",
                            "body": [{"print": ["Mollusc: %s", "mollusc"]}]}}]
    with pytest.raises(samplegen.RedefinedVariable):
        samplegen.Validator().validate_response(statements)


def test_loop_map_redefined_value():
    statements = [{"define": "mollusc=$resp.molluscs"},
                  {"loop": {"map": "$resp.molluscs",
                            "value": "mollusc",
                            "body": [{"print": ["Mollusc: %s", "mollusc"]}]}}]
    with pytest.raises(samplegen.RedefinedVariable):
        samplegen.Validator().validate_response(statements)


def test_validate_write_file():
    samplegen.Validator().validate_response(
        [{"write_file": {"filename": ["specimen-%s", "$resp.species"],
                         "contents": "$resp.photo"}}])


def test_validate_write_file_fname_fmt():
    with pytest.raises(samplegen.MismatchedFormatSpecifier):
        samplegen.Validator().validate_response(
            [{"write_file": {"filename": ["specimen-%s"],
                             "contents": "$resp.photo"}}])


def test_validate_write_file_fname_bad_var():
    with pytest.raises(samplegen.UndefinedVariableReference):
        samplegen.Validator().validate_response(
            [{"write_file": {"filename": ["specimen-%s", "squid.species"],
                             "contents": "$resp.photo"}}])


def test_validate_write_file_missing_fname():
    with pytest.raises(samplegen.InvalidStatement):
        samplegen.Validator().validate_response(
            [{"write_file": {"contents": "$resp.photo"}}]
        )


def test_validate_write_file_missing_contents():
    with pytest.raises(samplegen.InvalidStatement):
        samplegen.Validator().validate_response(
            [{"write_file": {"filename": ["specimen-%s", "$resp.species"]}}]
        )


def test_validate_write_file_bad_contents_var():
    with pytest.raises(samplegen.UndefinedVariableReference):
        samplegen.Validator().validate_response(
            [{"write_file": {"filename": ["specimen-%s", "$resp.species"],
                             "contents": "squid.photo"}}])


def test_invalid_statement():
    statement = {"print": ["Name"], "comment": ["Value"]}
    with pytest.raises(samplegen.InvalidStatement):
        samplegen.Validator().validate_response([statement])


def test_invalid_statement2():
    statement = {"squidify": ["Statement body"]}
    with pytest.raises(samplegen.InvalidStatement):
        samplegen.Validator().validate_response([statement])


# validate_and_transform_request tests
def test_validate_request_basic():
    assert samplegen.Validator().validate_and_transform_request(utils.CallingForm.Request,
                                                                [{"field": "squid.mantle_length",
                                                                  "value": "100 cm"},
                                                                 {"field": "squid.mantle_mass",
                                                                  "value": "10 kg"}]) == [
        samplegen.TransformedRequest("squid",
                                     [{"field": "mantle_length",
                                       "value": "100 cm"},
                                      {"field": "mantle_mass",
                                       "value": "10 kg"}])]


def test_validate_request_no_field_parameter():
    with pytest.raises(samplegen.InvalidRequestSetup):
        samplegen.Validator().validate_and_transform_request(utils.CallingForm.Request,
                                                             [{"squid": "humboldt"}])


def test_validate_request_malformed_field_attr():
    with pytest.raises(samplegen.InvalidRequestSetup):
        samplegen.Validator().validate_and_transform_request(utils.CallingForm.Request,
                                                             [{"field": "squid"}])


def test_validate_request_multiple_arguments():
    assert samplegen.Validator().validate_and_transform_request(utils.CallingForm.Request,
                                                                [{"field": "squid.mantle_length",
                                                                  "value": "100 cm",
                                                                  "value_is_file": True},
                                                                 {"field": "clam.shell_mass",
                                                                  "value": "100 kg",
                                                                  "comment": "Clams can be large"}]) == [
        samplegen.TransformedRequest("squid",
                                     [{"field": "mantle_length",
                                       "value": "100 cm",
                                       "value_is_file": True}]),
        samplegen.TransformedRequest("clam",
                                     [{"field": "shell_mass",
                                       "value": "100 kg",
                                       "comment": "Clams can be large"}])]


def test_validate_request_reserved_request_name():
    with pytest.raises(samplegen.ReservedVariableName):
        samplegen.Validator().validate_and_transform_request(utils.CallingForm.Request,
                                                             [{"field": "class.order", "value": "coleoidea"}])


def test_validate_request_duplicate_input_param():
    with pytest.raises(samplegen.RedefinedVariable):
        samplegen.Validator().validate_and_transform_request(utils.CallingForm.Request,
                                                             [{"field": "squid.mantle_mass",
                                                               "value": "10 kg",
                                                               "input_parameter": "mantle_mass"},
                                                              {"field": "clam.mantle_mass",
                                                               "value": "1 kg",
                                                               "input_parameter": "mantle_mass"}])


def test_validate_request_reserved_input_param():
    with pytest.raises(samplegen.ReservedVariableName):
        samplegen.Validator().validate_and_transform_request(utils.CallingForm.Request,
                                                             [{"field": "mollusc.class",
                                                               "value": "cephalopoda",
                                                               "input_parameter": "class"}])


def test_single_request_client_streaming():
    # Each API client method really only takes one parameter:
    # either a single protobuf message or an iterable of protobuf messages.
    # With unary request methods, python lets us describe attributes as positional
    # and keyword parameters, which simplifies request construction.
    # The 'base' in the transformed request refers to an attribute, and the
    # 'field's refer to sub-attributes.
    # Client streaming and bidirectional streaming methods can't use this notation,
    # and generate an exception if there is more than one 'base'.
    with pytest.raises(samplegen.InvalidRequestSetup):
        samplegen.Validator().validate_and_transform_request(
            utils.CallingForm.RequestStreamingClient,
            [{"field": "cephalopod.order",
              "value": "cephalopoda"},
             {"field": "gastropod.order",
              "value": "pulmonata"}])


def test_single_request_bidi_streaming():
    # Each API client method really only takes one parameter:
    # either a single protobuf message or an iterable of protobuf messages.
    # With unary request methods, python lets us describe attributes as positional
    # and keyword parameters, which simplifies request construction.
    # The 'base' in the transformed request refers to an attribute, and the
    # 'field's refer to sub-attributes.
    # Client streaming and bidirectional streaming methods can't use this notation,
    # and generate an exception if there is more than one 'base'.
    with pytest.raises(samplegen.InvalidRequestSetup):
        samplegen.Validator().validate_and_transform_request(
            utils.CallingForm.RequestStreamingBidi,
            [{"field": "cephalopod.order",
              "value": "cephalopoda"},
             {"field": "gastropod.order",
              "value": "pulmonata"}])


def test_validate_request_calling_form():
    DummyMethod = namedtuple("DummyMethod",
                             ["lro",
                              "paged_result_field",
                              "client_streaming",
                              "server_streaming"])

    assert utils.CallingForm.method_default(DummyMethod(
        True, False, False, False)) == utils.CallingForm.LongRunningRequestPromise

    assert utils.CallingForm.method_default(DummyMethod(
        False, True, False, False)) == utils.CallingForm.RequestPagedAll

    assert utils.CallingForm.method_default(DummyMethod(
        False, False, True, False)) == utils.CallingForm.RequestStreamingClient

    assert utils.CallingForm.method_default(DummyMethod(
        False, False, False, True)) == utils.CallingForm.RequestStreamingServer

    assert utils.CallingForm.method_default(DummyMethod(
        False, False, False, False)) == utils.CallingForm.Request

    assert utils.CallingForm.method_default(DummyMethod(
        False, False, True, True)) == utils.CallingForm.RequestStreamingBidi


def test_coerce_response_name():
    # Don't really need a test, but it shuts up code coverage.
    assert samplegen.coerce_response_name("$resp.squid") == "response.squid"
    assert samplegen.coerce_response_name("mollusc.squid") == "mollusc.squid"


def test_generate_manifest():
    DummyNaming = namedtuple("DummyNaming", ["name", "version"])
    DummyApiSchema = namedtuple("DummyApiSchema", ["naming"])

    fpath_to_dummy_sample = {
        "squid_fpath.py": {"id": "squid_sample"},
        "clam_fpath.py": {"id": "clam_sample",
                          "region_tag": "giant_clam_sample"},
    }

    fname, info = samplegen.generate_manifest(
        fpath_to_dummy_sample.items(),
        DummyApiSchema(DummyNaming("Mollusc", "v1")),
        # Empirically derived number such that the
        # corresponding time_struct tests the zero
        # padding in the returned filename.
        manifest_time=4486525628
    )

    assert fname == "Mollusc.v1.python.21120304.090708.manifest.yaml"

    expected_info = [
        gapic_yaml.KeyVal("type", "manifest/samples"),
        gapic_yaml.KeyVal("schema_version", "3"),
        gapic_yaml.Map(name="python",
                       anchor_name="python",
                       elements=[
                           gapic_yaml.KeyVal(
                               "environment", "python"),
                           gapic_yaml.KeyVal(
                               "bin", "python3"),
                           gapic_yaml.KeyVal(
                               "base_path", "sample/base/directory"),
                           gapic_yaml.KeyVal(
                               "invocation", "'{bin} {path} @args'"),
                       ]),
        gapic_yaml.Collection(name="samples",
                              elements=[
                                  [
                                      gapic_yaml.Anchor(
                                          "python"),
                                      gapic_yaml.KeyVal(
                                          "sample", "squid_sample"),
                                      gapic_yaml.KeyVal(
                                          "path", "'{base_path}/squid_fpath.py'"),
                                      gapic_yaml.KeyVal(
                                          "region_tag", ""),
                                  ],
                                  [
                                      gapic_yaml.Anchor("python"),
                                      gapic_yaml.KeyVal(
                                          "sample", "clam_sample"),
                                      gapic_yaml.KeyVal(
                                          "path", "'{base_path}/clam_fpath.py'"),
                                      gapic_yaml.KeyVal(
                                          "region_tag", "giant_clam_sample")
                                  ],
                              ])
    ]

    assert info == expected_info

    expected_rendering = dedent("""
                                type: manifest/samples
                                schema_version: 3
                                python: &python
                                  environment: python
                                  bin: python3
                                  base_path: sample/base/directory
                                  invocation: '{bin} {path} @args'
                                samples:
                                - <<: *python
                                  sample: squid_sample
                                  path: '{base_path}/squid_fpath.py'
                                  region_tag: 
                                - <<: *python
                                  sample: clam_sample
                                  path: '{base_path}/clam_fpath.py'
                                  region_tag: giant_clam_sample""".lstrip("\n"))

    rendered_yaml = "\n".join(e.render() for e in info)
    assert rendered_yaml == expected_rendering

    expected_parsed_manifest = {
        "type": "manifest/samples",
        "schema_version": 3,
        "python": {
            "environment": "python",
            "bin": "python3",
            "base_path": "sample/base/directory",
            "invocation": "{bin} {path} @args",
        },
        "samples": [
            {
                "environment": "python",
                "bin": "python3",
                "base_path": "sample/base/directory",
                "invocation": "{bin} {path} @args",
                "sample": "squid_sample",
                "path": "{base_path}/squid_fpath.py",
                "region_tag": None,
            },
            {
                "environment": "python",
                "bin": "python3",
                "base_path": "sample/base/directory",
                "invocation": "{bin} {path} @args",
                "sample": "clam_sample",
                "path": "{base_path}/clam_fpath.py",
                "region_tag": "giant_clam_sample",
            },
        ],
    }

    parsed_manifest = yaml.safe_load(rendered_yaml)
    assert parsed_manifest == expected_parsed_manifest
