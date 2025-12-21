import ast
import sys
import os
import black
import pytest
import yaml

# add cross_sync to path
test_dir_name = os.path.dirname(__file__)
cross_sync_path = os.path.join(test_dir_name, "..", "..", "..", ".cross_sync")
sys.path.append(cross_sync_path)

from transformers import (  # noqa: F401 E402
    SymbolReplacer,
    AsyncToSync,
    RmAioFunctions,
    StripAsyncConditionalBranches,
    CrossSyncFileProcessor,
)


def loader():
    dir_name = os.path.join(test_dir_name, "test_cases")
    for file_name in os.listdir(dir_name):
        if not file_name.endswith(".yaml"):
            print(f"Skipping {file_name}")
            continue
        test_case_file = os.path.join(dir_name, file_name)
        # load test cases
        with open(test_case_file) as f:
            print(f"Loading test cases from {test_case_file}")
            test_cases = yaml.safe_load(f)
            for test in test_cases["tests"]:
                test["file_name"] = file_name
                yield test


@pytest.mark.parametrize(
    "test_dict", loader(), ids=lambda x: f"{x['file_name']}: {x.get('description', '')}"
)
@pytest.mark.skipif(
    sys.version_info < (3, 9), reason="ast.unparse requires python3.9 or higher"
)
def test_e2e_scenario(test_dict):
    before_ast = ast.parse(test_dict["before"])
    got_ast = before_ast
    for transformer_info in test_dict["transformers"]:
        # transformer can be passed as a string, or a dict with name and args
        if isinstance(transformer_info, str):
            transformer_class = globals()[transformer_info]
            transformer_args = {}
        else:
            transformer_class = globals()[transformer_info["name"]]
            transformer_args = transformer_info.get("args", {})
        transformer = transformer_class(**transformer_args)
        got_ast = transformer.visit(got_ast)
    if got_ast is None:
        final_str = ""
    else:
        final_str = black.format_str(ast.unparse(got_ast), mode=black.FileMode())
    if test_dict.get("after") is None:
        expected_str = ""
    else:
        expected_str = black.format_str(test_dict["after"], mode=black.FileMode())
    assert final_str == expected_str, f"Expected:\n{expected_str}\nGot:\n{final_str}"
