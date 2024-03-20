# https://hub.docker.com/_/python
FROM python:3.9-slim

RUN apt-get update && \
    apt-get install --yes --no-install-recommends git wget && \
    git --version

WORKDIR /app
COPY requirements.txt .

RUN pip install --upgrade pip wheel setuptools && \
    pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN pip install --no-cache-dir .

ENV HOME="/home/sweeper"
RUN groupadd -r -g 3001 sweeper && useradd -r -d $HOME -u 3001 -g sweeper sweeper
RUN mkdir -p $HOME
RUN chown sweeper $HOME
USER sweeper

# https://stackoverflow.com/questions/54597500/printing-not-being-logged-by-kubernetes
ENTRYPOINT [ "sweeper" ]
