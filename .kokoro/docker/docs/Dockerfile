# Copyright 2020 Google LLC
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

from ubuntu:24.04

ENV DEBIAN_FRONTEND noninteractive

# Ensure local Python is preferred over distribution Python.
ENV PATH /usr/local/bin:$PATH

# Install dependencies.
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    apt-transport-https \
    build-essential \
    ca-certificates \
    curl \
    dirmngr \
    git \
    gpg-agent \
    graphviz \
    libbz2-dev \
    libdb5.3-dev \
    libexpat1-dev \
    libffi-dev \
    liblzma-dev \
    libreadline-dev \
    libsnappy-dev \
    libssl-dev \
    libsqlite3-dev \
    portaudio19-dev \
    redis-server \
    software-properties-common \
    ssh \
    sudo \
    tcl \
    tcl-dev \
    tk \
    tk-dev \
    uuid-dev \
    wget \
    zlib1g-dev \
  && add-apt-repository universe \
  && apt-get update \
  && apt-get -y install jq \
  && apt-get clean autoclean \
  && apt-get autoremove -y \
  && rm -rf /var/lib/apt/lists/* \
  && rm -f /var/cache/apt/archives/*.deb

###################### Install python 3.10.14 for docs/docfx session

# Download python 3.10.14
RUN wget https://www.python.org/ftp/python/3.10.14/Python-3.10.14.tgz

# Extract files
RUN tar -xvf Python-3.10.14.tgz

# Install python 3.10.14
RUN ./Python-3.10.14/configure --enable-optimizations
RUN make altinstall

ENV PATH /usr/local/bin/python3.10:$PATH

###################### Install pip
RUN wget -O /tmp/get-pip.py 'https://bootstrap.pypa.io/get-pip.py' \
  && python3.10 /tmp/get-pip.py \
  && rm /tmp/get-pip.py

# Test pip
RUN python3.10 -m pip

# Install build requirements
COPY requirements.txt /requirements.txt
RUN python3.10 -m pip install --require-hashes -r requirements.txt

CMD ["python3.10"]
