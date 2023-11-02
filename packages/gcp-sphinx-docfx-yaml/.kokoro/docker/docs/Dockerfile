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

from ubuntu:20.04

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
  && add-apt-repository ppa:deadsnakes/ppa \
  && apt-get update \
  && apt-get -y install jq \
  && apt-get clean autoclean \
  && apt-get autoremove -y \
  && apt install -y python3.10-distutils \
  && rm -rf /var/lib/apt/lists/* \
  && rm -f /var/cache/apt/archives/*.deb

# Install Google Cloud SDK
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg  add - && apt-get update -y && apt-get install google-cloud-sdk -y


###################### Install python 3.10.13

# Download python 3.10.13
RUN wget https://www.python.org/ftp/python/3.10.13/Python-3.10.13.tgz

# Extract files
RUN tar -xvf Python-3.10.13.tgz

# Install python 3.10.13
RUN ./Python-3.10.13/configure --enable-optimizations
RUN make altinstall

###################### Install pip
RUN apt install -y python3-pip

# Test pip
RUN python3.10 -m pip

# Make Python3.10 the default version
RUN unlink /usr/bin/python3 && ln -s /usr/local/bin/python3.10 /usr/bin/python3

# Test version
RUN python3 --version

CMD ["python3"]
