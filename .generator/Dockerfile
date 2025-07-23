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
    # For running bazelisk commands
    openjdk-17-jdk \
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
ENV BAZELISK_VERSION=v1.26.0


RUN for PYTHON_VERSION in 3.9.23 3.10.18 3.11.13 3.12.11 3.13.5; do \
# Install Python from source
    wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz && \
    tar -xvf Python-${PYTHON_VERSION}.tgz && \
    cd Python-${PYTHON_VERSION} && \
    ./configure --enable-optimizations && \
    make altinstall && \
    cd / && \
    rm -rf Python-${PYTHON_VERSION}* \
    ; done

ENV PYTHON_PIP_VERSION 25.1.1
RUN wget --no-check-certificate -O /tmp/get-pip.py 'https://bootstrap.pypa.io/get-pip.py' \
    && python3.10 /tmp/get-pip.py "pip==$PYTHON_PIP_VERSION" \

  # we use "--force-reinstall" for the case where the version of pip we're trying to install is the same as the version bundled with Python
  # ("Requirement already up-to-date: pip==8.1.2 in /usr/local/lib/python3.6/site-packages")
  # https://github.com/docker-library/python/pull/143#issuecomment-241032683
    && pip3 install --no-cache-dir --upgrade --force-reinstall "pip==$PYTHON_PIP_VERSION" \

  # then we use "pip list" to ensure we don't have more than one pip version installed
  # https://github.com/docker-library/python/pull/100
    && [ "$(pip list |tac|tac| awk -F '[ ()]+' '$1 == "pip" { print $2; exit }')" = "$PYTHON_PIP_VERSION" ]

# Ensure Pip for all python3 versions
RUN python3.9 /tmp/get-pip.py
RUN python3.11 /tmp/get-pip.py
RUN python3.12 /tmp/get-pip.py
RUN python3.13 /tmp/get-pip.py

RUN rm /tmp/get-pip.py

# Test Pip
RUN python3.9 -m pip
RUN python3.10 -m pip
RUN python3.11 -m pip
RUN python3.12 -m pip
RUN python3.13 -m pip


# TODO(https://github.com/googleapis/librarian/issues/904): Install protoc for gencode.

# Install Bazelisk
RUN wget https://github.com/bazelbuild/bazelisk/releases/download/${BAZELISK_VERSION}/bazelisk-linux-amd64 -O /usr/local/bin/bazelisk && \
    chmod +x /usr/local/bin/bazelisk

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
