FROM debian:9

RUN apt-get update && apt-get install -y \
    build-essential \
    python2.7 \
    python-pip \
    python-dev \
    python-numpy \
    python-scipy \
    python-matplotlib \
    git \
  && pip install --upgrade pip \
  && pip install 'setuptools >=14.0' \
  && git clone https://github.com/minepy/mictools.git /tmp/mictools/ \
  && pip install /tmp/mictools/ \
  && rm -rf /var/lib/apt/lists/* /tmp/mictools
