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

from ubuntu:20.10

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
    && for PYTHON_VERSION in 3.7.8 3.8.5; do \
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

RUN wget -O /tmp/get-pip.py 'https://bootstrap.pypa.io/get-pip.py' \
  && python3.7 /tmp/get-pip.py \
  && python3.8 /tmp/get-pip.py \
  && rm /tmp/get-pip.py

CMD ["python3.7"]
