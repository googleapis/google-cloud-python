# Copyright 2025 Google LLC
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

# --- Builder Stage ---
# This stage installs all build dependencies and compiles all Python versions.
FROM marketplace.gcr.io/google/ubuntu2404 AS builder

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    # Essential for compiling C code
    build-essential \
    # For downloading and extracting secure files
    git \
    wget \
    ca-certificates \
    unzip \
    # --- Critical libraries for a complete Python build ---
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libffi-dev \
    libsqlite3-dev \
    libreadline-dev \
    # Needed for `google-cloud-bigquery-storage` to avoid
    # the error `ModuleNotFoundError: No module named '_lzma'`
    # described in https://github.com/googleapis/google-cloud-python/issues/14884
    liblzma-dev \
    # ------------------------------------------------------
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHON_VERSION=3.14

# The full Python version, including the minor version, is needed for download/install
ENV PYTHON_VERSION_WITH_MINOR=3.14.2

# `make altinstall` is used to prevent replacing the system's default python binary.
RUN wget https://www.python.org/ftp/python/${PYTHON_VERSION_WITH_MINOR}/Python-${PYTHON_VERSION_WITH_MINOR}.tgz && \
    tar -xvf Python-${PYTHON_VERSION_WITH_MINOR}.tgz && \
    cd Python-${PYTHON_VERSION_WITH_MINOR} && \
    ./configure --enable-optimizations --prefix=/usr/local && \
    make -j$(nproc) && \
    make altinstall && \
    cd / && \
    rm -rf Python-${PYTHON_VERSION_WITH_MINOR}*


RUN wget --no-check-certificate -O /tmp/get-pip.py 'https://bootstrap.pypa.io/get-pip.py' && \
    python${PYTHON_VERSION} /tmp/get-pip.py && \
    rm /tmp/get-pip.py

# Download/extract protoc
RUN wget https://github.com/protocolbuffers/protobuf/releases/download/v25.3/protoc-25.3-linux-x86_64.zip
RUN unzip protoc-25.3-linux-x86_64.zip -d protoc

# Download/extract pandoc
# Pandoc is required by gapic-generator-python for parsing documentation
ENV PANDOC_VERSION=3.8.2
RUN mkdir pandoc-binary
RUN wget https://github.com/jgm/pandoc/releases/download/${PANDOC_VERSION}/pandoc-${PANDOC_VERSION}-linux-amd64.tar.gz
RUN tar -xvf pandoc-${PANDOC_VERSION}-linux-amd64.tar.gz -C pandoc-binary --strip-components=1

# Pin synthtool for a more hermetic build
# This needs to be a single command so that the git clone command is not cached
RUN git clone https://github.com/googleapis/synthtool.git synthtool && \
    cd synthtool && \
    git checkout 6702a344265de050bceaff45d62358bb0023ba7d

# --- Final Stage ---
# This stage creates the lightweight final image, copying only the
# necessary artifacts from the builder stage.
FROM marketplace.gcr.io/google/ubuntu2404

# Tell synthtool to pull templates from this docker image instead of from
# the live repo.
ENV SYNTHTOOL_TEMPLATES="/synthtool/synthtool/gcp/templates"

ENV PYTHON_VERSION_DEFAULT=3.14

# Install only the essential runtime libraries for Python.
# These are the non "-dev" versions of the libraries used in the builder.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    # TODO(https://github.com/googleapis/google-cloud-python/issues/14992): Remove gdb
    # Once this bug is fixed.
    # Temporarily add gdb to assist with remote debugging for issue 14992.
    gdb \
    # This is needed to avoid the following error:
    # `ImportError: libsqlite3.so.0: cannot open shared object file: No such file or directory`.
    # `libsqlite3-0` is used by the `coverage` PyPI package which is used when testing libraries
    libsqlite3-0 \
    && apt-get clean autoclean \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* \
    && rm -f /var/cache/apt/archives/*.deb

COPY --from=builder protoc/bin /usr/local/bin
COPY --from=builder protoc/include /usr/local/include

COPY --from=builder pandoc-binary/bin /usr/local/bin
COPY --from=builder synthtool /synthtool

COPY --from=builder /usr/local/bin/python${PYTHON_VERSION_DEFAULT}  /usr/local/bin/
COPY --from=builder /usr/local/lib/python${PYTHON_VERSION_DEFAULT}  /usr/local/lib/python${PYTHON_VERSION_DEFAULT}

# Set the working directory in the container.
WORKDIR /app

# Install dependencies of the CLI such as click.
# Install gapic-generator which is used to generate libraries.
# Install nox which is used for running client library tests.
# Install starlark-pyo3 which is used to parse BUILD.bazel files.
COPY .generator/requirements.in .
RUN python${PYTHON_VERSION_DEFAULT} -m pip install -r requirements.in
RUN python${PYTHON_VERSION_DEFAULT} -m pip install /synthtool

# Install build which is used to get the metadata of package config files.
COPY .generator/requirements.in .
RUN python${PYTHON_VERSION_DEFAULT} -m pip install -r requirements.in

# Copy the CLI script into the container.
COPY .generator/cli.py .
RUN chmod a+rx ./cli.py

# Copy the script used to parse BUILD.bazel files.
COPY .generator/parse_googleapis_content.py .
RUN chmod a+rx ./parse_googleapis_content.py

ENTRYPOINT ["python3.14", "./cli.py"]
