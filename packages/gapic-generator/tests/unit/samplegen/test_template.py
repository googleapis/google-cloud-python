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


import jinja2
import os.path as path
import gapic.samplegen.samplegen as samplegen
import gapic.utils as utils

from gapic.samplegen.utils import CallingForm
from textwrap import dedent


def check_template(template_fragment, expected_output, **kwargs):
    # Making a new environment for every unit test seems wasteful,
    # but the obvious alternative (make env an instance attribute
    # and passing a FunctionLoader whose load function returns
    # a constantly reassigned string attribute) isn't any faster
    # and is less clear.
    env = jinja2.Environment(
        loader=jinja2.ChoiceLoader(
            [jinja2.FileSystemLoader(
                searchpath=path.realpath(path.join(path.dirname(__file__),
                                                   "..", "..", "..",
                                                   "gapic", "templates", "examples"))),
             jinja2.DictLoader(
                 {"template_fragment": dedent(template_fragment)}),
             ]),

        undefined=jinja2.StrictUndefined,
        extensions=["jinja2.ext.do"],
        trim_blocks=True, lstrip_blocks=True
    )

    env.filters['snake_case'] = utils.to_snake_case
    env.filters['coerce_response_name'] = samplegen.coerce_response_name

    template = env.get_template("template_fragment")
    text = template.render(**kwargs)
    assert text == dedent(expected_output)


def test_render_attr_value():
    check_template(
        '''
        {% import "feature_fragments.j2" as frags %}
        {{ frags.render_request_attr("mollusc",
                                   {"field": "order",
                                    "value": "Molluscs.Cephalopoda.Coleoidea"}) }}
        ''',
        '''
        mollusc["order"] = Molluscs.Cephalopoda.Coleoidea
        '''
    )


def test_render_attr_input_parameter():
    check_template(
        '''
        {% import "feature_fragments.j2" as frags %}
        {{ frags.render_request_attr("squid", {"field": "species",
                                             "value": "Humboldt",
                                             "input_parameter": "species"}) }}
        ''',
        '''
        # species = "Humboldt"
        squid["species"] = species
        ''')


def test_render_attr_file():
    check_template(
        '''
        {% import "feature_fragments.j2" as frags %}
        {{ frags.render_request_attr("classify_mollusc_request",
                                   {"field": "mollusc_video",
                                    "value": "path/to/mollusc/video.mkv",
                                    "input_parameter" : "mollusc_video_path",
                                    "value_is_file": True}) }}
        ''',
        '''
        # mollusc_video_path = "path/to/mollusc/video.mkv"
        with open(mollusc_video_path, "rb") as f:
            classify_mollusc_request["mollusc_video"] = f.read()
        ''')


def test_render_request_basic():
    check_template(
        '''
        {% import "feature_fragments.j2" as frags %}
        {{ frags.render_request([{"base": "cephalopod",
                                 "body": [{"field": "mantle_mass",
                                           "value": "10 kg",
                                           "input_parameter": "cephalopod_mass"},
                                          {"field": "photo",
                                           "value": "path/to/cephalopod/photo.jpg",
                                           "input_parameter": "photo_path",
                                           "value_is_file": True},
                                          {"field": "order",
                                           "value": "Molluscs.Cephalopoda.Coleoidea"}, ]},
                                {"base": "gastropod",
                                 "body": [{"field": "mantle_mass",
                                           "value": "1 kg",
                                           "input_parameter": "gastropod_mass"},
                                          {"field": "order",
                                           "value": "Molluscs.Gastropoda.Pulmonata"},
                                          {"field": "movie",
                                           "value": "path/to/gastropod/movie.mkv",
                                           "input_parameter": "movie_path",
                                           "value_is_file": True}]}, ]) }}
        ''',
        '''
        cephalopod = {}
        # cephalopod_mass = "10 kg"
        cephalopod["mantle_mass"] = cephalopod_mass
        
        # photo_path = "path/to/cephalopod/photo.jpg"
        with open(photo_path, "rb") as f:
            cephalopod["photo"] = f.read()
        
        cephalopod["order"] = Molluscs.Cephalopoda.Coleoidea
        
        gastropod = {}
        # gastropod_mass = "1 kg"
        gastropod["mantle_mass"] = gastropod_mass
        
        gastropod["order"] = Molluscs.Gastropoda.Pulmonata
        
        # movie_path = "path/to/gastropod/movie.mkv"
        with open(movie_path, "rb") as f:
            gastropod["movie"] = f.read()
    
        '''
    )


def test_render_print():
    check_template(
        '''
        {% import "feature_fragments.j2" as frags %}
        {{ frags.render_print(["Mollusc"]) }}
        ''',
        '''
        print("Mollusc")
        '''
    )


def test_render_print_args():
    check_template(
        '''
        {% import "feature_fragments.j2" as frags %}
        {{ frags.render_print(["$resp %s %s", "$resp.squids", "$resp.clams"]) }}
        ''',
        '''
        print("$resp {} {}".format(response.squids, response.clams))
        '''
    )


def test_render_comment():
    check_template(
        '''
        {% import "feature_fragments.j2" as frags %}
        {{ frags.render_comment(["Mollusc"]) }}
        ''',
        '''
        # Mollusc
        '''
    )


def test_render_comment_args():
    check_template(
        '''
        {% import "feature_fragments.j2" as frags %}
        {{ frags.render_comment(["$resp %s %s", "$resp.squids", "$resp.clams"]) }}
        ''',
        '''
        # $resp response.squids response.clams
        '''
    )


def test_define():
    check_template(
        '''
        {% import "feature_fragments.j2" as frags %}
        {{ frags.render_define("squid=humboldt") }}
        ''',
        '''
        squid = humboldt
        '''
    )


def test_define_resp():
    check_template(
        '''
        {% import "feature_fragments.j2" as frags %}
        {{ frags.render_define("squid=$resp.squid") }}
        ''',
        '''
        squid = response.squid
        '''
    )


def test_dispatch_print():
    check_template(
        '''
        {% import "feature_fragments.j2" as frags %}
        {{ frags.dispatch_statement({"print" : ["Squid"] }) }}
        ''',
        '''
        print("Squid")
        '''
    )


def test_dispatch_comment():
    check_template(
        '''
        {% import "feature_fragments.j2" as frags %}
        {{ frags.dispatch_statement({"comment" : ["Squid"] }) }}
        ''',
        '''
        # Squid
        '''
    )


def test_write_file():
    check_template(
        '''
        {% import "feature_fragments.j2" as frags %}
        {{ frags.render_write_file({"filename": ["specimen-%s",
                                                 "$resp.species"],
                                    "contents": "$resp.photo"}) }}
        ''',
        '''
        with open("specimen-{}".format(response.species), "wb") as f:
            f.write(response.photo)
      
        '''
    )


def test_dispatch_write_file():
    check_template(
        '''
        {% import "feature_fragments.j2" as frags %}
        {{ frags.dispatch_statement({"write_file": 
                                       {"filename": ["specimen-%s",
                                                     "$resp.species"],
                                        "contents": "$resp.photo"}})}}
        ''',
        '''
        with open("specimen-{}".format(response.species), "wb") as f:
            f.write(response.photo)
      
        '''
    )


def test_collection_loop():
    check_template(
        '''
        {% import "feature_fragments.j2" as frags %}
        {{ frags.render_collection_loop({"collection": "$resp.molluscs",
                                       "variable": "m",
                                       "body": {"print": ["Mollusc: %s", "m"]}})}}
        ''',
        '''
        for m in response.molluscs:
            print("Mollusc: {}".format(m))
        '''
    )


def test_dispatch_collection_loop():
    check_template(
        '''
        {% import "feature_fragments.j2" as frags %}
        {{ frags.dispatch_statement({"loop": {"collection": "molluscs",
                                    "variable": "m",
                                    "body": {"print": ["Mollusc: %s", "m"]}}}) }}''',
        '''
        for m in molluscs:
            print("Mollusc: {}".format(m))
        '''
    )


def test_map_loop():
    check_template(
        '''
        {% import "feature_fragments.j2" as frags %}
        {{ frags.render_map_loop({"map": "$resp.molluscs",
                                "key":"cls",
                                "value":"example",
                                "body": {"print": ["A %s is a %s", "example", "cls"] }})
        }}''',
        '''
        for cls, example in response.molluscs.items():
            print("A {} is a {}".format(example, cls))
        '''
    )


def test_map_loop_no_key():
    check_template(
        '''
        {% import "feature_fragments.j2" as frags %}
        {{ frags.render_map_loop({"map": "$resp.molluscs",
                                "value":"example",
                                "body": {"print": ["A %s is a mollusc", "example"] }})
        }}
        ''',
        '''
        for example in response.molluscs.values():
            print("A {} is a mollusc".format(example))
        '''
    )


def test_map_loop_no_value():
    check_template(
        '''
        {% import "feature_fragments.j2" as frags %}
        {{ frags.render_map_loop({"map": "$resp.molluscs",
                                "key":"cls",
                                "body": {"print": ["A %s is a mollusc", "cls"] }})
        }}
        ''',
        '''
        for cls in response.molluscs.keys():
            print("A {} is a mollusc".format(cls))
        '''
    )


def test_dispatch_map_loop():
    check_template(
        '''
        {% import "feature_fragments.j2" as frags %}
        {{ frags.dispatch_statement({"loop":{"map": "molluscs",
                                            "key":"cls",
                                            "value":"example",
                                            "body": {
                                              "print": ["A %s is a %s", "example", "cls"] }}})
        }}
        ''',
        '''
        for cls, example in molluscs.items():
            print("A {} is a {}".format(example, cls))
        '''
    )


def test_print_input_params():
    check_template(
        '''
        {% import "feature_fragments.j2" as frags %}
        {{ frags.print_input_params([{"base": "squid",
                                    "body": [{"field": "mass",
                                              "value": "10 kg",
                                              "input_parameter": "mass"},
                                             {"field": "length",
                                              "value": "20 m",
                                              "input_parameter": "length"}]},
                                    {"base": "clam",
                                     "body": [{"field": "diameter",
                                               "value": "10 cm"}]},
                                    {"base": "whelk",
                                     "body": [{"field": "color",
                                               "value": "red",
                                               "input_parameter": "color"}]},
                                    ]) }}
        ''',
        '''
        mass, length, color'''
    )


CALLING_FORM_TEMPLATE_TEST_STR = '''
        {% import "feature_fragments.j2" as frags %}
        {{ frags.render_calling_form("TEST_INVOCATION_TXT", calling_form,
                                   calling_form_enum,
                                   [{"print": ["Test print statement"]}]) }}
        '''


def test_render_calling_form_request():
    check_template(CALLING_FORM_TEMPLATE_TEST_STR,
                   '''
                   response = TEST_INVOCATION_TXT
                   print("Test print statement")
                   
                   ''',
                   calling_form_enum=CallingForm,
                   calling_form=CallingForm.Request)


def test_render_calling_form_paged_all():
    check_template(CALLING_FORM_TEMPLATE_TEST_STR,
                   '''
                   page_result = TEST_INVOCATION_TXT
                   for response in page_result:
                       print("Test print statement")

                   ''',
                   calling_form_enum=CallingForm,
                   calling_form=CallingForm.RequestPagedAll)


def test_render_calling_form_paged():
    check_template(CALLING_FORM_TEMPLATE_TEST_STR,
                   '''
                    page_result = TEST_INVOCATION_TXT
                    for page in page_result.pages():
                        for response in page:
                            print("Test print statement")

                    ''',
                   calling_form_enum=CallingForm,
                   calling_form=CallingForm.RequestPaged)


def test_render_calling_form_streaming_server():
    check_template(CALLING_FORM_TEMPLATE_TEST_STR,
                   '''
                   stream = TEST_INVOCATION_TXT
                   for response in stream:
                       print("Test print statement")
                   
                   ''',
                   calling_form_enum=CallingForm,
                   calling_form=CallingForm.RequestStreamingServer)


def test_render_calling_form_streaming_bidi():
    check_template(CALLING_FORM_TEMPLATE_TEST_STR,
                   '''
                   stream = TEST_INVOCATION_TXT
                   for response in stream:
                       print("Test print statement")
                   
                   ''',
                   calling_form_enum=CallingForm,
                   calling_form=CallingForm.RequestStreamingBidi)


def test_render_calling_form_longrunning():
    check_template(CALLING_FORM_TEMPLATE_TEST_STR,
                   '''
                   operation = TEST_INVOCATION_TXT
                   
                   print("Waiting for operation to complete...")
                   
                   response = operation.result()
                   print("Test print statement")
                   
                   ''',
                   calling_form_enum=CallingForm,
                   calling_form=CallingForm.LongRunningRequestPromise)


def test_render_method_call_basic():
    # The callingForm and callingFormEnum parameters are dummies,
    # which we can get away with because of duck typing in the template.
    check_template(
        '''
        {% import "feature_fragments.j2" as frags %}
        {{ frags.render_method_call({"rpc": "CategorizeMollusc", "request": [{"base": "video"},
                                                                    {"base": "audio"},
                                                                    {"base": "guess"}]},
                                  calling_form, calling_form_enum) }}
        ''',
        '''
        client.categorize_mollusc(video, audio, guess)
        ''',
        calling_form_enum=CallingForm,
        calling_form=CallingForm.Request
    )


def test_render_method_call_bidi():
    # The callingForm and callingFormEnum parameters are dummies,
    # which we can get away with because of duck typing in the template.
    check_template(
        '''
        {% import "feature_fragments.j2" as frags %}
        {{ frags.render_method_call({"rpc": "CategorizeMollusc", "request": [{"base": "video"}]},
                                  calling_form, calling_form_enum) }}
        ''',
        '''
        client.categorize_mollusc([video])
        ''',
        calling_form_enum=CallingForm,
        calling_form=CallingForm.RequestStreamingBidi
    )


def test_render_method_call_client():
    # The callingForm and callingFormEnum parameters are dummies,
    # which we can get away with because of duck typing in the template.
    check_template(
        '''
        {% import "feature_fragments.j2" as frags %}
        {{ frags.render_method_call({"rpc": "CategorizeMollusc", "request": [{"base": "video"}]},
        calling_form, calling_form_enum) }}
        ''',
        '''
        client.categorize_mollusc([video])
        ''',
        calling_form_enum=CallingForm,
        calling_form=CallingForm.RequestStreamingClient
    )


def test_main_block():
    check_template(
        '''
        {% import "feature_fragments.j2" as frags %}
        {{ frags.render_main_block("ListMolluscs", [{"field": "list_molluscs.order",
                                                   "value": "coleoidea",
                                                   "input_parameter": "order"},
                                                  {"field ": "list_molluscs.mass",
                                                   "value": "60kg",
                                                   "input_parameter": "mass"},
                                                  {"field": "list_molluscs.zone",
                                                   "value": "MESOPELAGIC"},]) }}
        ''',
        '''
        def main():
            import argparse

            parser = argparse.ArgumentParser()
            parser.add_argument("--order",
                                type=str,
                                default="coleoidea")
            parser.add_argument("--mass",
                                type=str,
                                default="60kg")
            args = parser.parse_args()

            sample_list_molluscs(args.order, args.mass)


        if __name__ == "__main__":
            main()
        '''
    )
