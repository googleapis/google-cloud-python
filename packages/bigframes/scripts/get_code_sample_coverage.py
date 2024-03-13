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
from typing import Dict, List

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

for module_name in ML_MODULE_NAMES:
    module = importlib.import_module(f"bigframes.ml.{module_name}")
    classes_ = [
        class_ for _, class_ in inspect.getmembers(module, predicate=inspect.isclass)
    ]
    CLASSES.extend(classes_)


def get_code_samples_summary() -> Dict[str, Dict[str, List[str]]]:
    """Get Summary of the code samples coverage in BigFrames APIs.

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
    summary: Dict[str, Dict[str, List[str]]] = dict()

    for class_ in CLASSES:
        class_key = f"{class_.__module__}.{class_.__name__}"
        summary[class_key] = {PRESENT: [], NOT_PRESENT: []}

        members = inspect.getmembers(class_)

        for name, obj in members:
            # ignore private methods
            if name.startswith("_") and not name.startswith("__"):
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
            code_samples_present = docstr and "**Examples:**" in docstr
            key = PRESENT if code_samples_present else NOT_PRESENT
            summary[class_key][key].append(name)

    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get a summary of code samples coverage in BigFrames APIs."
    )
    parser.add_argument(
        "-d",
        "--details",
        type=bool,
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Whether to print APIs with and without code samples.",
    )

    args = parser.parse_args(sys.argv[1:])

    summary = get_code_samples_summary()

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
            print(f"===> APIs WITH code samples: {class_summary[PRESENT]}")
            print(f"===> APIs WITHOUT code samples: {class_summary[NOT_PRESENT]}")

    coverage = 100 * total_with_code_samples / total
    print(f"Total: {coverage:.1f}% ({total_with_code_samples}/{total})")
