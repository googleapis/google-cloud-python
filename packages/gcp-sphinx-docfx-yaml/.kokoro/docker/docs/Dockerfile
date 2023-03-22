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
  && apt-get update \
  && apt-get -y install jq \
  && apt-get clean autoclean \
  && apt-get autoremove -y \
  && rm -rf /var/lib/apt/lists/* \
  && rm -f /var/cache/apt/archives/*.deb

COPY fetch_gpg_keys.sh /tmp
# Install the desired versions of Python.
RUN set -ex \
  && export GNUPGHOME="$(mktemp -d)" \
  && echo "disable-ipv6" >> "${GNUPGHOME}/dirmngr.conf" \
  && /tmp/fetch_gpg_keys.sh \
  && for PYTHON_VERSION in 3.9.13; do \
  wget --no-check-certificate -O python-${PYTHON_VERSION}.tar.xz "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz" \
  && wget --no-check-certificate -O python-${PYTHON_VERSION}.tar.xz.asc "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz.asc" \
  && gpg --batch --verify python-${PYTHON_VERSION}.tar.xz.asc python-${PYTHON_VERSION}.tar.xz \
  && rm -r python-${PYTHON_VERSION}.tar.xz.asc \
  && mkdir -p /usr/src/python-${PYTHON_VERSION} \
  && tar -xJC /usr/src/python-${PYTHON_VERSION} --strip-components=1 -f python-${PYTHON_VERSION}.tar.xz \
  && rm python-${PYTHON_VERSION}.tar.xz \
  && cd /usr/src/python-${PYTHON_VERSION} \
  && ./configure \
  --enable-shared \
  # This works only on Python 2.7 and throws a warning on every other
  # version, but seems otherwise harmless.
  --enable-unicode=ucs4 \
  --with-system-ffi \
  --without-ensurepip \
  && make -j$(nproc) \
  && make install \
  && ldconfig \
  ; done \
  && rm -rf "${GNUPGHOME}" \
  && rm -rf /usr/src/python* \
  && rm -rf ~/.cache/

# Install pip on Python 3.9 only.
# If the environment variable is called "PIP_VERSION", pip explodes with
# "ValueError: invalid truth value '<VERSION>'"
ENV PYTHON_PIP_VERSION 23.0
RUN wget --no-check-certificate -O /tmp/get-pip.py 'https://bootstrap.pypa.io/get-pip.py' \
  && python3.9 /tmp/get-pip.py "pip==$PYTHON_PIP_VERSION" \
  # we use "--force-reinstall" for the case where the version of pip we're trying to install is the same as the version bundled with Python
  # ("Requirement already up-to-date: pip==8.1.2 in /usr/local/lib/python3.10/site-packages")
  # https://github.com/docker-library/python/pull/143#issuecomment-241032683
  && pip3 install --no-cache-dir --upgrade --force-reinstall "pip==$PYTHON_PIP_VERSION" \
  # then we use "pip list" to ensure we don't have more than one pip version installed
  # https://github.com/docker-library/python/pull/100
  && [ "$(pip list |tac|tac| awk -F '[ ()]+' '$1 == "pip" { print $2; exit }')" = "$PYTHON_PIP_VERSION" ]

# Install Google Cloud SDK
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg  add - && apt-get update -y && apt-get install google-cloud-sdk -y

CMD ["python3"]
