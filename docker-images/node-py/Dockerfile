FROM beevelop/nodejs:latest

# Install Python.
RUN \
  apt-get update && \
  apt-get install -y python-software-properties && \
  apt-get install -y software-properties-common && \
  apt-get update && \
  add-apt-repository ppa:jonathonf/python-3.6 && \
  apt-get update && \
  apt-get install -y make && \
  apt-get install -y python3.6 python3.6-dev python3.6-venv && \
  rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
	apt-get install -y openssh-client

EXPOSE 3000

WORKDIR /opt/app
ADD . /opt/app

RUN node -v
RUN python3.6 --version
