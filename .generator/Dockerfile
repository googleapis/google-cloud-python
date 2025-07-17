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
#

# Stage 1: The "builder" stage, used to compile and install tools.
FROM marketplace.gcr.io/google/ubuntu2404 AS builder

# Install all build dependencies and necessary tools.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    xz-utils \
    bzip2 \
    gdb \
    lcov \
    pkg-config \
    # the below two lines are copied from googleapis dockerfile:
    python-dev-is-python3 \
    libbz2-dev \
    libffi-dev \
    libgdbm-dev \
    libgdbm-compat-dev \
    liblzma-dev \
    libncurses5-dev \
    libreadline-dev \
    libsqlite3-dev \
    libssl-dev \
    lzma \
    lzma-dev \
    tk-dev \
    uuid-dev \
    zlib1g-dev \
    wget \
    zip \
    unzip \
    git \
    ca-certificates \
    openjdk-17-jdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set up environment variables for tool versions to make updates easier.
ENV PYTHON_VERSION=3.11.5
ENV PROTOC_VERSION=25.3
ENV BAZELISK_VERSION=v1.26.0

# Install protoc
RUN wget https://github.com/protocolbuffers/protobuf/releases/download/v${PROTOC_VERSION}/protoc-${PROTOC_VERSION}-linux-x86_64.zip -O protoc.zip && \
    unzip protoc.zip -d /usr/local && \
    chmod +x /usr/local/bin/protoc && \
    rm protoc.zip

# Install Bazelisk
RUN wget https://github.com/bazelbuild/bazelisk/releases/download/${BAZELISK_VERSION}/bazelisk-linux-amd64 -O /usr/local/bin/bazelisk && \
    chmod +x /usr/local/bin/bazelisk

# Install Python from source
RUN wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz && \
    tar -xvf Python-${PYTHON_VERSION}.tgz && \
    cd Python-${PYTHON_VERSION} && \
    ./configure --enable-optimizations && \
    make altinstall && \
    cd / && \
    rm -rf Python-${PYTHON_VERSION}*

# Create a symbolic link for `python3` to point to our specific version.
# RUN ln -s /usr/local/bin/python3.11 /usr/local/bin/python3
ENV PATH /usr/local/bin/python3.11:$PATH

# Install only necessary runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    openjdk-17-jdk \
    git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# --- Create a dedicated non-root user ---
# Use arguments to make the user and group IDs configurable from the build command.
ARG UID=1000
ARG GID=1000

# Create the group and user, but only if they don't already exist.
RUN if ! getent group $GID > /dev/null; then \
        groupadd -g $GID myuser; \
    fi && \
    if ! getent passwd $UID > /dev/null; then \
        useradd -u $UID -g $GID -ms /bin/bash myuser; \
    fi

# Set ownership of the app directory now, before we copy files into it.
RUN mkdir -p /app && chown $UID:$GID /app

# Switch to the non-root user. All subsequent commands will run as this user.
USER $UID

# Set the working directory.
WORKDIR /app

# Disable Python's output buffering so logs appear in real-time.
ENV PYTHONUNBUFFERED=1

#  Install Python dependencies from requirements.in
COPY --chown=$UID:$GID requirements.in .
RUN python3.11 -m pip install --no-cache-dir -r requirements.in

# # Install synthtool by cloning its repo, as it's not on PyPI.
RUN git clone --depth 1 https://github.com/googleapis/synthtool.git /tmp/synthtool && \
    python3.11 -m pip install /tmp/synthtool && \
    rm -rf /tmp/synthtool

# Copy your CLI script into the container and make it executable.
COPY --chown=$UID:$GID cli.py .
RUN chmod a+rx ./cli.py

# Run Bazel build:
RUN git clone --depth 1 https://github.com/googleapis/googleapis.git /tmp/googleapis

# target=/root/.cache/bazel
RUN --mount=type=cache,target=$HOME/.cache/bazel \
    cd /tmp/googleapis && \
    bazelisk build //google/cloud/language/v1:language-v1-py

RUN rm -rf /tmp/googleapis

# Set the entrypoint for the container.
# NOTE: 3.13 does not work.
ENTRYPOINT ["python3.11", "./cli.py"]