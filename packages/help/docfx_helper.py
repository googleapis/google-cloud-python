# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import pathlib
import shutil
import sys
import yaml
import pypandoc

def build_docfx(current_dir, repo_root, docs_map):
    current_dir = pathlib.Path(current_dir)
    repo_root = pathlib.Path(repo_root)
    output_dir = current_dir / "docs" / "_build"

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    # Ensure pandoc is available (pypandoc will download it if not found in PATH)
    try:
        pypandoc.get_pandoc_version()
    except OSError:
        print("Pandoc not found. Downloading...")
        pypandoc.download_pandoc()

    toc = []

    for title, source in docs_map.items():
        source_path = pathlib.Path(source)
        if not source_path.is_absolute():
            source_path = current_dir / source_path

        filename = source_path.name

        if filename.endswith(".rst"):
            target_filename = filename.replace(".rst", ".md")
            print(f"Converting {filename} -> {target_filename} using pandoc")
            if source_path.exists():
                # Use pandoc to convert RST to GFM (GitHub Flavored Markdown)
                output = pypandoc.convert_file(
                    str(source_path),
                    'gfm',
                    format='rst'
                )
                (output_dir / target_filename).write_text(output)
            else:
                print(f"Warning: Source {source_path} not found.")
                (output_dir / target_filename).write_text(f"# {title}\n\nContent missing.")
            href = target_filename
        else:
            print(f"Copying {filename}")
            if source_path.exists():
                shutil.copy(source_path, output_dir / filename)
            else:
                print(f"Warning: Source {source_path} not found.")
                (output_dir / filename).write_text(f"# {title}\n\nContent missing.")
            href = filename

        toc.append({"name": title, "href": href})

    # Write toc.yaml
    toc_path = output_dir / "toc.yaml"
    with open(toc_path, "w") as f:
        yaml.dump(toc, f, default_flow_style=False)

    print(f"DocFX build complete in {output_dir}")
    print(f"Generated TOC: {toc}")

if __name__ == "__main__":
    # Simple argument parsing: current_dir, repo_root, then pairs of Title,Source
    curr = sys.argv[1]
    root = sys.argv[2]
    d_map = {}
    for i in range(3, len(sys.argv), 2):
        d_map[sys.argv[i]] = sys.argv[i+1]

    build_docfx(curr, root, d_map)
