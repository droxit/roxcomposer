FROM beevelop/nodejs:latest

# Install Python.
RUN \
  apt-get update && \
  apt-get install -y python3 python3-dev python3-pip python3-virtualenv && \
  rm -rf /var/lib/apt/lists/*

EXPOSE 3000

WORKDIR /opt/app
ADD . /opt/app

RUN node -v
RUN python3 --version
