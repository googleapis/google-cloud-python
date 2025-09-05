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

# TODO(https://github.com/googleapis/librarian/issues/901): Install the necssary dependencies and build tools.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    # Essential for compiling C code
    build-essential \
    # For downloading secure files
    git \
    wget \
    ca-certificates \
    # For running bazelisk commands
    openjdk-17-jdk \
    zip \
    unzip \ 
    # To avoid bazel error
    # "python interpreter `python3` not found in PATH"
    python3-dev \
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

# Install multiple Python versions from source. `make altinstall` is used to
# prevent replacing the system's default python binary.
# TODO(http://github.com/googleapis/gapic-generator-python/issues/2435): Remove `3.10.18` when the linked issue is resolved.
RUN for PYTHON_VERSION in 3.9.23 3.10.18 3.13.5; do \
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
    for PYTHON_VERSION in 3.9 3.10 3.13; do \
        python${PYTHON_VERSION} /tmp/get-pip.py; \
    done && \
    rm /tmp/get-pip.py

# Install Bazelisk
RUN wget https://github.com/bazelbuild/bazelisk/releases/download/${BAZELISK_VERSION}/bazelisk-linux-amd64 -O /usr/local/bin/bazelisk && \
    chmod +x /usr/local/bin/bazelisk

# Set the working directory for build-related tasks.
WORKDIR /app

# Create the group and user, but only if they don't already exist.
ARG UID=1000
ARG GID=1000

RUN if ! getent group $GID > /dev/null; then \
        groupadd -g $GID myuser; \
    fi && \
    if ! getent passwd $UID > /dev/null; then \
        useradd -u $UID -g $GID -ms /bin/bash myuser; \
    fi

# Set ownership of the app directory now, before we copy files into it.
RUN mkdir -p /app && chown $UID:$GID /app

# We'll point both to the /bazel_cache directory which will be mounted as a volume.
ENV BAZELISK_HOME="/bazel_cache/bazelisk"
ENV BAZEL_HOME="/bazel_cache/bazel"

# Ensure the cache directories within the non-root user's context exist and are writable.
# This is crucial as Bazel creates subdirectories under BAZEL_HOME.
RUN mkdir -p ${BAZEL_HOME}/_bazel_ubuntu/cache/repos \
             ${BAZEL_HOME}/_bazel_ubuntu/output_base \
             ${BAZELISK_HOME} && \
    chown -R $UID:$GID ${BAZEL_HOME} ${BAZELISK_HOME}

RUN /usr/local/bin/python3.9 -m venv bazel_env
RUN . bazel_env/bin/activate

RUN git clone https://github.com/googleapis/googleapis.git \
    && cd googleapis \
    && bazelisk --output_base=/bazel_cache/_bazel_ubuntu/output_base build --disk_cache=/bazel_cache/_bazel_ubuntu/cache/repos  --incompatible_strict_action_env //google/cloud/language/v1:language-v1-py

# TODO(https://github.com/googleapis/librarian/issues/904): Install protoc for gencode.

# --- Final Stage ---
# This stage creates the lightweight final image, copying only the
# necessary artifacts from the builder stage.
FROM marketplace.gcr.io/google/ubuntu2404

# Install only the essential runtime libraries for Python.
# These are the non "-dev" versions of the libraries used in the builder.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    git \
    libssl3 \
    zlib1g \
    libbz2-1.0 \
    libffi8 \
    libsqlite3-0 \
    libreadline8 \
    # For running bazelisk commands
    openjdk-17-jdk \
    # To avoid bazel error
    # "python interpreter `python3` not found in PATH"
    python3-dev \
    # To avoid bazel error
    # "Cannot find gcc or CC; either correct your path or set the CC environment variable"
    build-essential \
    # To avoid bazel error
    # unzip command not found
    unzip \ 
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy all Python interpreters, their pip executables, and their standard libraries from the builder.
COPY --from=builder /usr/local/bin/python3.9 /usr/local/bin/
COPY --from=builder /usr/local/lib/python3.9 /usr/local/lib/python3.9

# TODO(http://github.com/googleapis/gapic-generator-python/issues/2435): Remove `3.10` when the linked issue is resolved.
COPY --from=builder /usr/local/bin/python3.10 /usr/local/bin/
COPY --from=builder /usr/local/lib/python3.10 /usr/local/lib/python3.10

COPY --from=builder /usr/local/bin/python3.13 /usr/local/bin/
COPY --from=builder /usr/local/lib/python3.13 /usr/local/lib/python3.13

# Copy the bazelisk executable from the builder.
COPY --from=builder /usr/local/bin/bazelisk /usr/local/bin/

# Copy bazel cache from the builder.
COPY --from=builder /bazel_cache /bazel_cache
RUN chmod -R 777 /bazel_cache

# Set the working directory in the container.
WORKDIR /app

# Create a virtual env and set the Path to fix the missing nox error
# when running the post processor changes.
RUN /usr/local/bin/python3.9 -m venv bazel_env
RUN . bazel_env/bin/activate

ENV PATH=/app/bazel_env/bin:$PATH

RUN git clone --depth 1 https://github.com/googleapis/synthtool.git /tmp/synthtool && \
bazel_env/bin/python3.9 -m pip install /tmp/synthtool nox && \
rm -rf /tmp/synthtool

# Copy the CLI script into the container.
COPY .generator/cli.py .
RUN chmod a+rx ./cli.py

ENTRYPOINT ["python3.9", "./cli.py"]
