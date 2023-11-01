from docfx_yaml import extension

import unittest
from parameterized import parameterized

from yaml import load, Loader

import tempfile

class TestGenerate(unittest.TestCase):
    code_testdata = [
        # Check that the code indents to left based on first line.
        [
            \
"""    def foo():
        print('test function for indent')
        return ('left-indented-code')
""",
            \
"""def foo():
    print('test function for indent')
    return ('left-indented-code')
"""
        ],
        # Check that if there's no whitespace, it does not indent
        [
            \
"""
print('test function for no impact indent')
for i in range(10):
    print(i)
    if i%5 == 0:
        i += 1
    else:
        continue
""",
            \
"""
print('test function for no impact indent')
for i in range(10):
    print(i)
    if i%5 == 0:
        i += 1
    else:
        continue
"""
        ],
    ]
    @parameterized.expand(code_testdata)
    def test_indent_code_left(self, code, code_want):
        parts = code.split("\n")
        tab_space = len(parts[0]) - len(parts[0].lstrip(" "))
        code_got = extension.indent_code_left(code, tab_space)
        self.assertEqual(code_got, code_want)


    def test_indent_code_blocks_left(self):
        # Check code blocks are indented properly.
        code_want = \
"""def foo():

    print('test function for indent')

    return ('left-indented-blocks')
"""

        # Test with how blocks would appear in the code block
        code = [
            "    def foo():",
            "        print('test function for indent')",
            "        return ('left-indented-blocks')\n"
        ]
        tab_space = len(code[0]) - len(code[0].lstrip(" "))
        code_got = "\n\n".join([extension.indent_code_left(part, tab_space) for part in code])
        self.assertEqual(code_got, code_want)


    def test_extract_keyword(self):
        # Check that keyword properly gets processed.
        keyword_want = "attribute"

        keyword_line = ".. attribute:: "
        keyword_got = extension.extract_keyword(keyword_line)

        self.assertEqual(keyword_got, keyword_want)

        # Check that keyword is not retrieved for bad formats.
        keyword_line = ".. attribute:"

        # Should raise an exception..
        with self.assertRaises(ValueError):
            keyword_got = extension.extract_keyword(keyword_line)


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
        # Testing for cross reference to not be converted for its own object.
        [
            "Response message for google.cloud.bigquery_storage_v1.types.SplitResponse.",
            "Response message for google.cloud.bigquery_storage_v1.types.SplitResponse."
        ],
        # TODO(https://github.com/googleapis/sphinx-docfx-yaml/issues/208):
        # remove this when it is not needed anymore.
        # Testing for hardcoded reference.
        [
            "google.iam.v1.iam_policy_pb2.GetIamPolicyRequest",
            "<a href=\"http://github.com/googleapis/python-grpc-google-iam-v1/blob/8e73b45993f030f521c0169b380d0fbafe66630b/google/iam/v1/iam_policy_pb2_grpc.py#L111-L118\">google.iam.v1.iam_policy_pb2.GetIamPolicyRequest</a>"
        ],
    ]
    @parameterized.expand(cross_references_testdata)
    def test_convert_cross_references(self, content, content_want):
        # Check that entries correctly turns into cross references.
        keyword_map = [
            "google.cloud.bigquery_storage_v1.types.SplitReadStreamResponse",
            "google.cloud.bigquery_storage_v1.types.SplitResponse"
        ]
        current_object_name = "google.cloud.bigquery_storage_v1.types.SplitResponse"

        content_got = extension.convert_cross_references(content, current_object_name, keyword_map)
        self.assertEqual(content_got, content_want)

    cross_references_test_data = [
        [
            """
            Examples:
              google.cloud.bigquery_storage_v1.types.SplitReadStreamResponse: test content.
            """,
            """
            Examples:
              google.cloud.bigquery_storage_v1.types.SplitReadStreamResponse: test content.
            """,
        ],
    ]
    @parameterized.expand(cross_references_testdata)
    def test_does_not_convert_for_examples(self, content, content_want):
        # Check that entries correctly turns into cross references.
        keyword_map = [
            "google.cloud.bigquery_storage_v1.types.SplitReadStreamResponse",
            "google.cloud.bigquery_storage_v1.types.SplitResponse"
        ]
        current_object_name = "google.cloud.bigquery_storage_v1.types.SplitResponse"

        content_got = extension.convert_cross_references(content, current_object_name, keyword_map, ignore_examples=True)
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

        content_got = extension.convert_cross_references(content, current_name, keyword_map)

        # Make sure that same entries are not processed twice.
        # The output should not be different.
        current = content_got
        current_got = extension.convert_cross_references(current, content, keyword_map)
        self.assertEqual(content_want, current_got)

        # If shorter version of the current name exists, it should not interfere
        # unless strictly necessary.
        keyword_map.append("google.cloud.bigquery_storage_v1.types")
        long_name_got = extension.convert_cross_references(content, current_name, keyword_map)
        self.assertEqual(long_name_got, content_want)

        shorter_name_want = "<xref uid=\"google.cloud.bigquery_storage_v1.types\">google.cloud.bigquery_storage_v1.types</xref>"
        shorter_name = "google.cloud.bigquery_storage_v1.types"
        shorter_name_got = extension.convert_cross_references(shorter_name, current_name, keyword_map)
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
            extension.search_cross_references(obj, current_name, keyword_map)

        with open('tests/cross_references_post.yaml', 'r') as want_file:
            yaml_post = load(want_file, Loader=Loader)

        self.assertEqual(yaml_pre, yaml_post)


    def test_format_code(self):
        # Test to ensure black formats strings properly.
        code_want = 'batch_predict(\n    *,\n    gcs_source: Optional[Union[str, Sequence[str]]] = None,\n    instances_format: str = "jsonl",\n    gcs_destination_prefix: Optional[str] = None,\n    predictions_format: str = "jsonl",\n    model_parameters: Optional[Dict] = None,\n    machine_type: Optional[str] = None,\n    accelerator_type: Optional[str] = None,\n    explanation_parameters: Optional[\n        google.cloud.aiplatform_v1.types.explanation.ExplanationParameters\n    ] = None,\n    labels: Optional[Dict[str, str]] = None,\n    sync: bool = True,\n)'

        code = 'batch_predict(*, gcs_source: Optional[Union[str, Sequence[str]]] = None, instances_format: str = "jsonl", gcs_destination_prefix: Optional[str] = None, predictions_format: str = "jsonl", model_parameters: Optional[Dict] = None, machine_type: Optional[str] = None, accelerator_type: Optional[str] = None, explanation_parameters: Optional[google.cloud.aiplatform_v1.types.explanation.ExplanationParameters] = None, labels: Optional[Dict[str, str]] = None, sync: bool = True,)'

        code_got = extension.format_code(code)
        self.assertEqual(code_want, code_got)


    def test_extract_product_name(self):
        # Test to ensure different name formats extract product name properly.
        name_want = "scheduler_v1.types.Digest"
        name = "google.cloud.scheduler_v1.types.Digest"
        product_name = extension.extract_product_name(name)

        self.assertEqual(name_want, product_name)

        non_cloud_name = "google.scheduler_v1.types.Digest"
        non_cloud_product_name = extension.extract_product_name(non_cloud_name)

        self.assertEqual(name_want, non_cloud_product_name)

        short_name_want = "Digest"
        short_name = "scheduler_v1.types.Digest"
        short_product_name = extension.extract_product_name(short_name)

        self.assertEqual(short_name_want, short_product_name)


    test_reference_params = [
        [
            # If no reference keyword is found, check for None
            "google.cloud.resourcemanager_v3.ProjectsClient",
            ["google.cloud.resourcemanager_v1.ProjectsClient"],
            ["The", "following", "constraints", "apply", "when", "using"],
            None
        ],
        [
            # If keyword reference is found, validate proper cross reference
            "google.cloud.resourcemanager_v3.set_iam_policy",
            ["google.cloud.resourcemanager_v3.set_iam_policy"],
            ["A", "Policy", "is", "a", "collection", "of", "bindings", "from"],
            "google.cloud.resourcemanager_v3.set_iam_policy"
        ],
        [
            # If keyword reference has already been converted, do not convert
            # again.
            "uid=\"google.cloud.resourcemanager_v3.set_iam_policy\">documentation</xref>",
            ["google.cloud.resourcemanager_v3.set_iam_policy"],
            ["Take", "a", "look", "at", "<xref"],
            None
        ],
        [
            # If no reference keyword is found, check for None
            "google.cloud.resourcemanager_v3.ProjectsClient",
            ["google.cloud.resourcemanager_v3.ProjectsClient"],
            ["The", "following", "constraints", "apply", "when", "using"],
            None
        ],
    ]
    @parameterized.expand(test_reference_params)
    def test_find_uid_to_convert(self, current_word, uids, visited_words, cross_reference_want):
        current_object_name = "google.cloud.resourcemanager_v3.ProjectsClient"
        content ="""Sets the IAM access control policy for the specified project.

The following constraints apply when using google.cloud.resourcemanager_v3.ProjectsClient

A Policy is a collection of bindings from google.cloud.resourcemanager_v3.set_iam_policy

Take a look at <xref uid="google.cloud.resourcemanager_v3.set_iam_policy">documentation</xref> for more information.
"""
        # Break up the paragraph into sanitized list of words as shown in Sphinx.
        words = " ".join(content.split("\n")).split(" ")

        index = words.index(current_word)

        cross_reference_got = extension.find_uid_to_convert(
            current_word, words, index, uids, current_object_name, visited_words
        )
        self.assertEqual(cross_reference_got, cross_reference_want)

    test_summary = [
        [
            """Retrieve the ``ID`` for the object.

See https://cloud.google.com/storage/docs/json_api/v1/objects

The ID consists of the bucket name, object name, and generation number.
            """,
            """Retrieve the `ID` for the object.

See https://cloud.google.com/storage/docs/json_api/v1/objects

The ID consists of the bucket name, object name, and generation number.
            """,
        ],
        [
            # Test that codeblocks don't get formatted.
            """The ID of the blob or `None`.

if the blob's resource has not been loaded from the server.

For example:
```
    ID or None
```
            """,
            """The ID of the blob or `None`.

if the blob's resource has not been loaded from the server.

For example:
```
    ID or None
```
            """,
        ],
    ]
    @parameterized.expand(test_summary)
    def test_reformat_summary(self, summary, summary_want):
        summary_got = extension.reformat_summary(summary)
        self.assertEqual(summary_want, summary_got)


    syntax_testdata = [
        [
            'None',
        ],
        [
            \
"""
google.cloud.pubsub_v1.message.Message
""",
        ],
        [
            'Callable[[], int]',
        ],
    ]
    @parameterized.expand(syntax_testdata)
    def test_is_valid_python_code(self, syntax):
        result = extension.is_valid_python_code(syntax)
        self.assertTrue(result)


    invalid_syntax_testdata = [
        [
            'This should not be considered valid Python code.',
        ],
        [
            # Typo in code
            'Callable[]',
        ],
    ]
    @parameterized.expand(invalid_syntax_testdata)
    def test_is_not_valid_python_code(self, invalid_syntax):
        result = extension.is_valid_python_code(invalid_syntax)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
