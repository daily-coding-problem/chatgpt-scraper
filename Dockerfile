# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Create a non-root user
RUN useradd -m user

# Set the working directory for user
WORKDIR /home/user

# Switch to root user to install dependencies
USER root

# Install necessary dependencies
RUN apt-get update && \
    apt-get install -y \
        postgresql-client \
        postgresql-server-dev-all \
        build-essential \
        curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Switch to the non-root user user
USER user

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set up poetry environment variables
ENV PATH="/home/user/.local/bin:${PATH}"

# Upgrade pip to latest version
RUN pip install --upgrade pip

# Copy the rest of the application code
WORKDIR /usr/src/app
COPY . /usr/src/app

# Switch to root user to install dependencies
USER root

# Install Poetry dependencies
RUN poetry install --no-root

# Switch to the non-root user user
USER user
