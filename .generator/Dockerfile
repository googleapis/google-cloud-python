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
    # ------------------------------------------------------
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install multiple Python versions from source. `make altinstall` is used to
# prevent replacing the system's default python binary.
# TODO(http://github.com/googleapis/gapic-generator-python/issues/2435): Remove `3.10.18` when the linked issue is resolved.
RUN for PYTHON_VERSION in 3.9.23 3.10.18 3.13.7 3.14.0; do \
    wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz && \
    tar -xvf Python-${PYTHON_VERSION}.tgz && \
    cd Python-${PYTHON_VERSION} && \
    ./configure --enable-optimizations --prefix=/usr/local && \
    make -j$(nproc) && \
    make altinstall && \
    cd / && \
    rm -rf Python-${PYTHON_VERSION}* \
    ; done

# Install pip for each python version
# TODO(http://github.com/googleapis/gapic-generator-python/issues/2435): Remove `3.10` when the linked issue is resolved.
RUN wget --no-check-certificate -O /tmp/get-pip.py 'https://bootstrap.pypa.io/get-pip.py' && \
    for PYTHON_VERSION in 3.9 3.10 3.13 3.14; do \
        python${PYTHON_VERSION} /tmp/get-pip.py; \
    done && \
    rm /tmp/get-pip.py

RUN /usr/local/bin/python3.9 -m venv bazel_env
RUN . bazel_env/bin/activate

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
RUN git clone https://github.com/googleapis/synthtool.git synthtool
RUN cd synthtool && git checkout 35313ccd8cdd2d12d2447ccdc497a7919aae1e3e

# --- Final Stage ---
# This stage creates the lightweight final image, copying only the
# necessary artifacts from the builder stage.
FROM marketplace.gcr.io/google/ubuntu2404

# Tell synthtool to pull templates from this docker image instead of from
# the live repo.
ENV SYNTHTOOL_TEMPLATES="/synthtool/synthtool/gcp/templates"

# Install only the essential runtime libraries for Python.
# These are the non "-dev" versions of the libraries used in the builder.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
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

# Copy all Python interpreters, their pip executables, and their standard libraries from the builder.
COPY --from=builder /usr/local/bin/python3.9 /usr/local/bin/
COPY --from=builder /usr/local/lib/python3.9 /usr/local/lib/python3.9

# TODO(http://github.com/googleapis/gapic-generator-python/issues/2435): Remove `3.10` when the linked issue is resolved.
COPY --from=builder /usr/local/bin/python3.10 /usr/local/bin/
COPY --from=builder /usr/local/lib/python3.10 /usr/local/lib/python3.10

COPY --from=builder /usr/local/bin/python3.13 /usr/local/bin/
COPY --from=builder /usr/local/lib/python3.13 /usr/local/lib/python3.13

COPY --from=builder /usr/local/bin/python3.14 /usr/local/bin/
COPY --from=builder /usr/local/lib/python3.14 /usr/local/lib/python3.14

# Set the working directory in the container.
WORKDIR /app

# Install dependencies of the CLI such as click.
# Install gapic-generator which is used to generate libraries.
# Install nox which is used for running client library tests.
# Install starlark-pyo3 which is used to parse BUILD.bazel files.
COPY .generator/requirements.in .
RUN python3.9 -m pip install -r requirements.in
RUN python3.9 -m pip install /synthtool

# Install build which is used to get the metadata of package config files.
COPY .generator/requirements.in .
RUN python3.9 -m pip install -r requirements.in

# Copy the CLI script into the container.
COPY .generator/cli.py .
RUN chmod a+rx ./cli.py

# Copy the script used to parse BUILD.bazel files.
COPY .generator/parse_googleapis_content.py .
RUN chmod a+rx ./parse_googleapis_content.py

ENTRYPOINT ["python3.9", "./cli.py"]
