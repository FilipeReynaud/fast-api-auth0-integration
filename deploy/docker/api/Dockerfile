# Globally defined build args
ARG USER=docker_user

#
# Build first docker layer for python images
#
FROM python:3.11.2 AS base-python

ARG UID=10000
ARG USER

# Set working dir
WORKDIR /app

# Continue the work with the less privileged user
RUN adduser --disabled-password --gecos '' --uid $UID $USER

#
# Build second docker layer for needed dependencies
#
FROM base-python AS base-dependencies

# Copy configuration files and install poetry
COPY pyproject.toml .
RUN pip install poetry

# Install packages
RUN poetry config virtualenvs.create false
RUN poetry install

#
# Build third layer for the actual code
#
FROM base-dependencies

# Runs server by default
ENV ENV_SERVICE="app"

# Builds for development by default
ENV ENV="development"

# Get all src code into the container
COPY ./src src

# Get env file
COPY .env .env

# No virtualenvs inside Docker
RUN poetry config virtualenvs.create false

ENTRYPOINT [ "poetry", "run", "uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "3000", "--reload" ]
