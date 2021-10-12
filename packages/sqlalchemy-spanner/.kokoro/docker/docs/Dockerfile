# Copyright 2021 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

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
    python3-distutils \
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

RUN wget -O /tmp/get-pip.py 'https://bootstrap.pypa.io/get-pip.py' \
  && python3.8 /tmp/get-pip.py \
  && rm /tmp/get-pip.py

CMD ["python3.8"]
