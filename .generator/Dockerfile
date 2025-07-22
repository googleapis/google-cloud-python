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

FROM marketplace.gcr.io/google/ubuntu2404 AS builder

# TODO(https://github.com/googleapis/librarian/issues/901): Install the necssary dependencies and build tools.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    # Essential for compiling C code
    build-essential \
    # For downloading secure files
    wget \
    ca-certificates \
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

# Set up environment variables for tool versions to make updates easier.
ENV PYTHON_VERSION=3.11.5

# Create a symbolic link for `python3` to point to our specific version.
ENV PATH /usr/local/bin/python3.11:$PATH

# Install Python from source
RUN wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz && \
    tar -xvf Python-${PYTHON_VERSION}.tgz && \
    cd Python-${PYTHON_VERSION} && \
    ./configure --enable-optimizations && \
    make altinstall && \
    cd / && \
    rm -rf Python-${PYTHON_VERSION}*

# TODO(https://github.com/googleapis/librarian/issues/904): Install protoc for gencode.

# TODO(https://github.com/googleapis/librarian/issues/903): Install Bazelisk for building a client library.

# TODO(https://github.com/googleapis/librarian/issues/902): Create a dedicate non-root user and 
# switch to the non-root user to run subsequent commands.

# Set the working directory in the container.
WORKDIR /app

# TODO(https://github.com/googleapis/librarian/issues/907): Install Python dependencies from requirements.in.
# TODO(https://github.com/googleapis/librarian/issues/905): Install Synthtool by cloning its repo.
# TODO(https://github.com/googleapis/librarian/issues/906): Clone googleapis and run bazelisk build.

# Copy the CLI script into the container and set ownership.
COPY .generator/cli.py .

# Set the entrypoint for the container to run the script.
ENTRYPOINT ["python3.11", "./cli.py"]
