#!/bin/bash

set -eo pipefail

env

if [[ -f /bazel-cache.tar.gz ]]; then
    echo "unzipping bazel cache"
    # temp_dir=$(mktmp -d)
    tar -zxf /bazel-cache.tar.gz -C /bazel/.cache --strip-components=2
    # tar -zxf /bazel-cache.tar.gz -C "${temp_dir}" --strip-components=1
    # mv "${temp_dir}"
fi

# bazelisk build //google/cloud/language/v1:language-v1-py
# cd /

python3.9 cli.py $@
