#  Copyright 2026 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import argparse
import importlib
import inspect
import os
import sys
from typing import Dict, Type

connection_string = (
    "projects/my-project/instances/my-instance/databases/my-database"
    "?autoConfigEmulator=true"
)

def discover_samples() -> Dict[str, Type]:
    """Discovers sample classes in the snippets directory."""
    samples: Dict[str, Type] = {}
    snippets_dir = os.path.join(os.path.dirname(__file__), 'snippets')
    
    if not os.path.exists(snippets_dir):
        print(f"Snippets directory not found: {snippets_dir}")
        return samples

    # Add the current directory to sys.path to ensure snippets can be imported
    current_dir = os.path.dirname(__file__)
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)

    for filename in os.listdir(snippets_dir):
        if filename.endswith('.py') and not filename.startswith('__'):
            module_name = f"snippets.{filename[:-3]}"
            try:
                module = importlib.import_module(module_name)
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    # Check if the class has a 'run' method and is defined in the module
                    if obj.__module__ == module_name and hasattr(obj, 'run'):
                        samples[name] = obj
            except ImportError as e:
                print(f"Failed to import {module_name}: {e}")
            except Exception as e:
                print(f"Error loading {module_name}: {e}")
    return samples

def run_sample(name: str, sample_class: Type, conn_string: str) -> None:
    """Runs a single sample."""
    print(f"Running {name}...")
    try:
        sample_class().run(conn_string)
    except Exception as e:
        print(f"Error running {name}: {e}")

def main() -> None:
    samples = discover_samples()
    
    if not samples:
        print("No samples found.")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Run Spanner DBAPI samples.")
    parser.add_argument(
        "sample",
        help="The name of the sample class to run, or 'All' to run all samples.",
        choices=list(samples.keys()) + ["All"],
    )
    
    args = parser.parse_args()
    
    if args.sample == "All":
        print("Running all samples...")
        for name, sample_class in samples.items():
            print(f"\n--- Running {name} ---")
            run_sample(name, sample_class, connection_string)
    else:
        sample_class = samples.get(args.sample)
        if sample_class:
            run_sample(args.sample, sample_class, connection_string)
        else:
            print(f"Sample {args.sample} not found.")
            sys.exit(1)

if __name__ == "__main__":
    main()