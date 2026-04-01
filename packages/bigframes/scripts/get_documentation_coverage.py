# Copyright 2023 Google LLC
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

import argparse
import importlib
import inspect
import sys
import typing

import bigframes
import bigframes.pandas as bpd

PRESENT = "present"
NOT_PRESENT = "not_present"

CLASSES = [
    bpd.DataFrame,
    bpd.Series,
    bpd.Index,
    bigframes.session.Session,
    bigframes.operations.strings.StringMethods,
    bigframes.operations.datetimes.DatetimeMethods,
    bigframes.operations.structs.StructAccessor,
]

ML_MODULE_NAMES = [
    "cluster",
    "compose",
    "decomposition",
    "ensemble",
    "linear_model",
    "metrics",
    "model_selection",
    "pipeline",
    "preprocessing",
    "llm",
    "forecasting",
    "imported",
    "remote",
]

COVERAGE_GENERATORS = {
    "documentation": lambda docstr: docstr,
    "code samples": lambda docstr: docstr and "**Examples:**" in docstr,
}

for module_name in ML_MODULE_NAMES:
    module = importlib.import_module(f"bigframes.ml.{module_name}")
    classes_ = [
        class_ for _, class_ in inspect.getmembers(module, predicate=inspect.isclass)
    ]
    CLASSES.extend(classes_)


def get_coverage_summary(
    func: typing.Callable,
) -> typing.Dict[str, typing.Dict[str, typing.List[str]]]:
    """Get Summary of the code samples coverage in BigFrames APIs.

    Args:
        func (callable):
            Function to accept documentation and return whether it satisfies
            coverage.
    Returns:
        Summary: A dictionary of the format
            {
                class_1: {
                    "present": [method1, method2, ...],
                    "not_present": [method3, method4, ...]
                },
                class_2: {
                    ...
                }
            }
    """
    summary: typing.Dict[str, typing.Dict[str, typing.List[str]]] = dict()

    for class_ in CLASSES:
        class_key = f"{class_.__module__}.{class_.__name__}"
        summary[class_key] = {PRESENT: [], NOT_PRESENT: []}

        members = inspect.getmembers(class_)

        for name, obj in members:
            # ignore private methods
            if name.startswith("_") and not name.startswith("__"):
                continue

            # ignore constructor
            if name == "__init__":
                continue

            def predicate(impl):
                return (
                    # This includes class methods like `from_dict`, `from_records`
                    inspect.ismethod(impl)
                    # This includes instance methods like `dropna`, join`
                    or inspect.isfunction(impl)
                    # This includes properties like `shape`, `values` but not
                    # generic properties like `__weakref__`
                    or (inspect.isdatadescriptor(impl) and not name.startswith("__"))
                )

            if not predicate(obj):
                continue

            # At this point we have a property or a public method
            impl = getattr(class_, name)

            docstr = inspect.getdoc(impl)
            coverage_present = func(docstr)
            key = PRESENT if coverage_present else NOT_PRESENT
            summary[class_key][key].append(name)

    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get a summary of documentation coverage in BigFrames APIs."
    )
    parser.add_argument(
        "-c",
        "--code-samples",
        type=bool,
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Whether to calculate code samples coverage. By default the tool"
        " calculates the documentation (docstring) coverage.",
    )
    parser.add_argument(
        "-d",
        "--details",
        type=bool,
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Whether to print APIs with and without the coverage.",
    )

    args = parser.parse_args(sys.argv[1:])

    scenario = "code samples" if args.code_samples else "documentation"
    summary = get_coverage_summary(COVERAGE_GENERATORS[scenario])

    total_with_code_samples = 0
    total = 0
    for class_, class_summary in summary.items():
        apis_with_code_samples = len(class_summary[PRESENT])
        total_with_code_samples += apis_with_code_samples

        apis_total = len(class_summary[PRESENT]) + len(class_summary[NOT_PRESENT])
        total += apis_total

        coverage = 100 * apis_with_code_samples / apis_total
        print(f"{class_}: {coverage:.1f}% ({apis_with_code_samples}/{apis_total})")
        if args.details:
            print(f"===> APIs WITH {scenario}: {class_summary[PRESENT]}")
            print(f"===> APIs WITHOUT {scenario}: {class_summary[NOT_PRESENT]}")

    coverage = 100 * total_with_code_samples / total
    print(f"Total: {coverage:.1f}% ({total_with_code_samples}/{total})")
