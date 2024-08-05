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
  - [Environment Variables](#environment-variables)
  - [Configuring TEST_ACCOUNTS](#configuring-test_accounts)
  - [Target a Specific ChatGPT Account](#target-a-specific-chatgpt-account)
  - [Use Temporary Chat Mode](#use-temporary-chat-mode)
  - [Configure Headless Mode](#configure-headless-mode)
  - [Configure Log Level](#configure-log-level)
- [Usage](#usage)
- [License](#license)

## Features

- Uses Selenium to scrape ChatGPT conversations.
- Supports automated interactions with ChatGPT.
- Facilitates fetching responses for predefined prompts.
- Supports multiple login methods for ChatGPT (Basic and Google).
- Supports 2FA for secure login methods.
- Utilizes Docker for easy setup and environment management.
- Supports temporary chat mode for ChatGPT.
- Provides mechanisms to copy ChatGPT responses in Markdown or Plain Text format.

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

### Environment Variables

Create a .env file in the project root containing the content from [.env.example](/.env.example). Modify the values as needed.

#### Configuring `TEST_ACCOUNTS`

The `TEST_ACCOUNTS` environment variable is used to securely store and pass credentials for test accounts to the ChatGPT scraper. These credentials need to be formatted as a base64-encoded JSON structure.

You can use the [Accounts Serializer](https://github.com/daily-coding-problem/accounts-serializer) tool to generate this JSON structure and encode it.

**Steps to Configure `TEST_ACCOUNTS`:**

1. **Clone the Accounts Serializer Repository**

   ```sh
   git clone https://github.com/daily-coding-problem/accounts-serializer.git
   cd accounts-serializer
   ```

2. **Install Dependencies**

   Ensure you have Python 3.11 or higher and Poetry installed. Then run:

   ```sh
   poetry install
   ```

3. **Generate the JSON Structure**

   Run the `accounts_serializer.py` script with your account details:

   ```sh
   poetry run python accounts_serializer.py \
       --emails test@company.com user@anothercompany.com \
       --passwords password123 userpassword456 \
       --providers basic google \
       --secrets google:google-secret-abc chatgpt:chatgpt-secret-xyz github:github-secret-123 aws:aws-secret-789
   ```

   This command will output a JSON structure like the following:

   ```json
   {
       "test@company.com": {
           "provider": "basic",
           "password": "password123",
           "secret": {
               "google": "google-secret-abc",
               "chatgpt": "chatgpt-secret-xyz"
           }
       },
       "user@anothercompany.com": {
           "provider": "google",
           "password": "userpassword456",
           "secret": {
               "github": "github-secret-123",
               "aws": "aws-secret-789"
           }
       }
   }
   ```

4. **Base64 Encode the JSON Structure**

   Use a tool or script to base64 encode the JSON structure:

   ```sh
   echo -n '{"test@company.com": {"provider": "basic", "password": "password123", "secret": {"google": "google-secret-abc", "chatgpt": "chatgpt-secret-xyz"}}, "user@anothercompany.com": {"provider": "basic", "password": "userpassword456", "secret": {"github": "github-secret-123", "aws": "aws-secret-789"}}}' | base64
   ```

5. **Set the `TEST_ACCOUNTS` Environment Variable**

   Copy the base64-encoded string and set it as the value of the `TEST_ACCOUNTS` environment variable in your `.env` file or directly in your shell environment.

   ```sh
   export TEST_ACCOUNTS="eyJ0ZXN0QGNvbXBhbnkuY29tIjogeyJwcm92aWRlciI6ICJiYXNpYyIsICJwYXNzd29yZCI6ICJwYXNzd29yZDEyMyIsICJzZWNyZXQiOiB7Imdvb2dsZSI6ICJnb29nbGUtc2VjcmV0LWFiYyIsICJjaGF0Z3B0IjogImNoYXRncHQtc2VjcmV0LXh5eiJ9fSwgInVzZXJAYW5vdGhlcmNvbXBhbnkuY29tIjogeyJwcm92aWRlciI6ICJiYXNpYyIsICJwYXNzd29yZCI6ICJ1c2VycGFzc3dvcmQ0NTYiLCAic2VjcmV0IjogeyJnaXRodWIiOiAiZ2l0aHViLXNlY3JldC0xMjMiLCAiYXdzIjogImF3cy1zZWNyZXQtNzg5In19fQ=="
   ```

   Now, `TEST_ACCOUNTS` is configured and ready to be used by the ChatGPT scraper.

#### Target a Specific ChatGPT Account

   If you want to target a specific account, you can set the `CHATGPT_ACCOUNT` environment variable with the email of the account you want to use.

   ```sh
   export CHATGPT_ACCOUNT="some-email@company.com"
   ```

   The email should be one of the emails in the `TEST_ACCOUNTS` JSON structure.

#### Use Temporary Chat Mode

   If you want to use the _Temporary Chat_ mode, set the `TEMPORARY_CHAT` environment variable to `true`.

   ```sh
   export TEMPORARY_CHAT="true"
   ```

   If set to `true`, this will toggle the _temporary chat_ mode in ChatGPT's interface and not store any chat history.

#### Configure Headless Mode

You can set the `CHATGPT_HEADLESS` environment variable to `true` to run the scraper in headless mode.

   ```sh
   export CHATGPT_HEADLESS="true"
   ```

If set to `true`, the scraper will run in headless mode, which means the browser will not be visible during the scraping process.

#### Configure Log Level

   You can set the log level for the scraper by setting the `LOG_LEVEL` environment variable. The default log level is `INFO`.

   ```sh
   export LOG_LEVEL="DEBUG"
   ```

   The available log levels are `DEBUG`, `INFO`, `WARNING`, `ERROR`, and `CRITICAL`.

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
