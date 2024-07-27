# ChatGPT Scraper

![Docker](https://img.shields.io/badge/-Docker-2496ED?style=flat-square&logo=Docker&logoColor=white)
![Linux](https://img.shields.io/badge/-Linux-FCC624?style=flat-square&logo=linux&logoColor=black)
![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Selenium](https://img.shields.io/badge/-Selenium-59b943?style=flat-square&logo=selenium&logoColor=white)

A Selenium-based ChatGPT interaction automation tool. This script initializes a browser session, interacts with ChatGPT using predefined prompts, and facilitates automated conversations with ChatGPT. Ideal for fetching responses and conducting tests or demonstrations.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [License](#license)

## Features

- Utilizes Selenium to scrape ChatGPT conversations.
- Supports automated interactions with ChatGPT.
- Facilitates fetching responses for predefined prompts.
- Supports multiple login methods for ChatGPT (Basic and Google).
- Supports 2FA for secure login methods.
- Utilizes Docker for easy setup and environment management.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Docker and Docker Compose installed on your machine.
- Python 3.12 or higher.

## Installation

**Clone the Repository**

```sh
git clone https://github.com/daily-coding-problem/chatgpt-scraper.git
cd chatgpt-scraper
```

**Setup Python Environment**

Use the following commands to set up the Python environment if you do not want to use Docker:

```sh
python -m venv .venv
source .venv/bin/activate
pip install poetry
poetry install --no-root
```

**Setup Docker**

If you would like to use Docker, ensure Docker and Docker Compose are installed on your machine. If not, follow the installation guides for [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/).

**Build Docker Images**

```sh
docker compose build
```

**Create the Network**

```sh
docker network create dcp
```

## Configuration

**Environment Variables**

Create a `.env` file in the project root containing the content from [`.env.example`](/.env.example). Modify the values as needed.

## Usage

Run the scraper with the specified plans:

```sh
docker compose run chatgpt-scraper
```

Or without Docker:

```sh
poetry run python main.py
```

## Running Tests

Run the tests with the following command:

```sh
poetry run pytest
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
