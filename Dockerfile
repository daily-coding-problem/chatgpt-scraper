# Use an official Python runtime as a parent image
FROM python:3.9.18-slim

# Create a non-root user
RUN useradd -m user

# Set the working directory for user
WORKDIR /home/user

# Switch to root user to install dependencies
USER root

# Install necessary dependencies including Chrome
RUN apt-get update && \
    apt-get install -y \
        postgresql-client \
        postgresql-server-dev-all \
        build-essential \
        curl \
        wget \
        gnupg && \
    # Download and install Google Chrome
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
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

# Update the poetry lock file and install dependencies
RUN poetry lock --no-update && poetry install --no-root

# Switch to the non-root user user
USER user
