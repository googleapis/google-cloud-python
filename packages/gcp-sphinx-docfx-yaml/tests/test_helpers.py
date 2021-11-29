from docfx_yaml.extension import extract_keyword
from docfx_yaml.extension import indent_code_left
from docfx_yaml.extension import convert_cross_references
from docfx_yaml.extension import search_cross_references
from docfx_yaml.extension import format_code
from docfx_yaml.extension import extract_product_name

import unittest
from parameterized import parameterized

from yaml import load, Loader

class TestGenerate(unittest.TestCase):
    def test_indent_code_left(self):
        # Check that the code indents to left based on first line.
        code_want = \
"""def foo():
    print('test function for indent')
    return ('left-indented-code')
"""

        code = \
"""    def foo():
        print('test function for indent')
        return ('left-indented-code')
"""
        code = indent_code_left(code)
        self.assertEqual(code, code_want)

        # Check that if there's no whitespace, it does not indent
        code_want = \
"""
print('test function for no impact indent')
for i in range(10):
    print(i)
    if i%5 == 0:
        i += 1
    else:
        continue
"""

        code_got = indent_code_left(code_want)
        # Confirm that nothing changes.
        self.assertEqual(code_got, code_want)


    def test_extract_keyword(self):
        # Check that keyword properly gets processed.
        keyword_want = "attribute"

        keyword_line = ".. attribute:: "
        keyword_got = extract_keyword(keyword_line)

        self.assertEqual(keyword_got, keyword_want)

        # Check that keyword is not retrieved for bad formats.
        keyword_line = ".. attribute:"

        # Should raise an exception..
        with self.assertRaises(ValueError):
            keyword_got = extract_keyword(keyword_line)


    cross_references_testdata = [
        # Testing for normal input.
        [
            "google.cloud.bigquery_storage_v1.types.SplitReadStreamResponse",
            "<xref uid=\"google.cloud.bigquery_storage_v1.types.SplitReadStreamResponse\">google.cloud.bigquery_storage_v1.types.SplitReadStreamResponse</xref>"
        ],
        # Testing for no cross references to convert.
        [
            "Response message for SplitReadStreamResponse.",
            "Response message for SplitReadStreamResponse."
        ],
        # Testing for cross references to convert within longer content.
        [
            "Response message for google.cloud.bigquery_storage_v1.types.SplitReadStreamResponse.",
            "Response message for <xref uid=\"google.cloud.bigquery_storage_v1.types.SplitReadStreamResponse\">google.cloud.bigquery_storage_v1.types.SplitReadStreamResponse</xref>."
        ],
    ]
    @parameterized.expand(cross_references_testdata)
    def test_convert_cross_references(self, content, content_want):
        # Check that entries correctly turns into cross references.
        keyword_map = [
            "google.cloud.bigquery_storage_v1.types.SplitReadStreamResponse"
        ]
        current_name = "SplitRepsonse"

        content_got = convert_cross_references(content, current_name, keyword_map)
        self.assertEqual(content_got, content_want)


    # Test data used to test for processing already-processed cross references.
    cross_references_short_testdata = [
        [
            "Response message for google.cloud.bigquery_storage_v1.types.SplitReadStreamResponse.",
            "Response message for <xref uid=\"google.cloud.bigquery_storage_v1.types.SplitReadStreamResponse\">google.cloud.bigquery_storage_v1.types.SplitReadStreamResponse</xref>."
        ],
    ]
    @parameterized.expand(cross_references_short_testdata)
    def test_convert_cross_references_twice(self, content, content_want):
        keyword_map = [
            "google.cloud.bigquery_storage_v1.types.SplitReadStreamResponse"
        ]
        current_name = "SplitRepsonse"

        content_got = convert_cross_references(content, current_name, keyword_map)

        # Make sure that same entries are not processed twice.
        # The output should not be different.
        current = content_got
        current_got = convert_cross_references(current, content, keyword_map)
        self.assertEqual(content_want, current_got)

        # If shorter version of the current name exists, it should not interfere
        # unless strictly necessary.
        keyword_map.append("google.cloud.bigquery_storage_v1.types")
        long_name_got = convert_cross_references(content, current_name, keyword_map)
        self.assertEqual(long_name_got, content_want)

        shorter_name_want = "<xref uid=\"google.cloud.bigquery_storage_v1.types\">google.cloud.bigquery_storage_v1.types</xref>"
        shorter_name = "google.cloud.bigquery_storage_v1.types"
        shorter_name_got = convert_cross_references(shorter_name, current_name, keyword_map)
        self.assertEqual(shorter_name_got, shorter_name_want)


    def test_search_cross_references(self):
        # Test for a given YAML file.
        keyword_map = [
               "google.cloud.bigquery_storage_v1.types.ThrottleState",
               "google.cloud.bigquery_storage_v1.types.StreamStats.Progress",
               "google.cloud.bigquery_storage_v1.types.StreamStats",
               "google.cloud.bigquery_storage_v1.types.SplitReadStreamResponse",
               "google.cloud.bigquery_storage_v1.types.SplitReadStreamRequest",
               "google.cloud.bigquery_storage_v1.types.ReadStream",
               "google.cloud.bigquery_storage_v1.types.ReadSession.TableReadOptions",
               "google.cloud.bigquery_storage_v1.types.ReadSession.TableModifiers",
               "google.cloud.bigquery_storage_v1.types.ReadSession",
               "google.cloud.bigquery_storage_v1.types.ReadRowsResponse",
               "google.cloud.bigquery_storage_v1.types.ReadRowsRequest",
               "google.cloud.bigquery_storage_v1.types.DataFormat",
               "google.cloud.bigquery_storage_v1.types.CreateReadSessionRequest",
               "google.cloud.bigquery_storage_v1.types.AvroSchema",
               "google.cloud.bigquery_storage_v1.types.AvroRows",
               "google.cloud.bigquery_storage_v1.types.ArrowSerializationOptions.CompressionCodec",
               "google.cloud.bigquery_storage_v1.types.ArrowSerializationOptions",
               "google.cloud.bigquery_storage_v1.types.ArrowSchema",
               "google.cloud.bigquery_storage_v1.types.ArrowRecordBatch",
               "google.cloud.bigquery_storage_v1.types",
        ]
        current_name = "google.cloud.bigquery_storage_v1.types.ReadSession.TableReadOptions"
        with open('tests/cross_references_pre.yaml', 'r') as test_file:
            yaml_pre = load(test_file, Loader=Loader)

        for obj in yaml_pre['items']:
            search_cross_references(obj, current_name, keyword_map)

        with open('tests/cross_references_post.yaml', 'r') as want_file:
            yaml_post = load(want_file, Loader=Loader)

        self.assertEqual(yaml_pre, yaml_post)


    def test_format_code(self):
        # Test to ensure black formats strings properly.
        code_want = 'batch_predict(\n    *,\n    gcs_source: Optional[Union[str, Sequence[str]]] = None,\n    instances_format: str = "jsonl",\n    gcs_destination_prefix: Optional[str] = None,\n    predictions_format: str = "jsonl",\n    model_parameters: Optional[Dict] = None,\n    machine_type: Optional[str] = None,\n    accelerator_type: Optional[str] = None,\n    explanation_parameters: Optional[\n        google.cloud.aiplatform_v1.types.explanation.ExplanationParameters\n    ] = None,\n    labels: Optional[Dict[str, str]] = None,\n    sync: bool = True,\n)'

        code = 'batch_predict(*, gcs_source: Optional[Union[str, Sequence[str]]] = None, instances_format: str = "jsonl", gcs_destination_prefix: Optional[str] = None, predictions_format: str = "jsonl", model_parameters: Optional[Dict] = None, machine_type: Optional[str] = None, accelerator_type: Optional[str] = None, explanation_parameters: Optional[google.cloud.aiplatform_v1.types.explanation.ExplanationParameters] = None, labels: Optional[Dict[str, str]] = None, sync: bool = True,)'

        code_got = format_code(code)
        self.assertEqual(code_want, code_got)


    def test_extract_product_name(self):
        # Test to ensure different name formats extract product name properly.
        name_want = "scheduler_v1.types.Digest"
        name = "google.cloud.scheduler_v1.types.Digest"
        product_name = extract_product_name(name)

        self.assertEqual(name_want, product_name)

        non_cloud_name = "google.scheduler_v1.types.Digest"
        non_cloud_product_name = extract_product_name(non_cloud_name)

        self.assertEqual(name_want, non_cloud_product_name)

        short_name_want = "Digest"
        short_name = "scheduler_v1.types.Digest"
        short_product_name = extract_product_name(short_name)

        self.assertEqual(short_name_want, short_product_name)

if __name__ == '__main__':
    unittest.main()
