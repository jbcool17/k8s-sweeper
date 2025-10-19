# https://hub.docker.com/_/python
FROM python:3.10-slim

# Use a virtual environment to not pollute the global python environment
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /opt/app
COPY pyproject.toml .

# Install dependencies first to leverage Docker layer caching
RUN pip install --no-cache-dir .
COPY . /opt/app/
# Install the application itself
RUN pip install --no-cache-dir .

ENV HOME="/home/sweeper"
RUN groupadd -r -g 3001 sweeper && useradd -r -d $HOME -u 3001 -g sweeper sweeper
RUN mkdir -p $HOME && chown -R sweeper:sweeper $HOME /opt/app
USER sweeper

ENTRYPOINT [ "sweeper" ]
