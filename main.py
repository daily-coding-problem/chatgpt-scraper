import logging
import argparse
import os
from typing import List

from dotenv import load_dotenv

from chatgpt.auth.accounts_deserializer import AccountsDeserializer
from chatgpt.auth.login_method import LoginMethod
from chatgpt.configuration import Configuration
from utilities import print_random_banner
from utilities.poetry import get_name, get_description, get_authors, get_version
from chatgpt.browser import Browser
from chatgpt.chatbot import ChatBot
from chatgpt.chatgpt_interaction import ChatGPTInteraction

# In order, for our logging configuration to take effect, we need to import the logger_config module.
import chatgpt.logger_config

# Load environment variables
load_dotenv()

accounts = AccountsDeserializer()


def main(account: str, system_prompt: str, user_prompts: List[str], config: Configuration):
    if not account and config.use_temporary_chat:
        logging.warning("Temporary chat mode is enabled but no account is provided. Disabling temporary chat mode.")
        config.use_temporary_chat = False

    browser = Browser("https://chatgpt.com", config.headless)
    interaction = ChatGPTInteraction(browser, config)

    if not handle_login(account, config, interaction):
        logging.error("Failed to log in.")
        return

    chatbot = ChatBot(interaction)
    chatbot.chat(system_prompt, user_prompts)
    browser.quit()


def handle_login(account: str, config: Configuration, interaction: ChatGPTInteraction) -> bool:
    """
    Handle the login process if an account is provided.

    :param account: The account email or identifier.
    :param config: The configuration object.
    :param interaction: The ChatGPTInteraction object.
    :return: True if login is successful, False otherwise.
    """
    if not account:
        logging.info("No account provided. Skipping login.")
        return True

    account_details = config.get_account(account)

    if not account_details:
        logging.error(f"Account details not found for email: {account}")
        return False

    login_method = LoginMethod.derive_login_provider(account_details)

    return interaction.login(login_method=login_method(interaction.browser), email=account)


if __name__ == "__main__":
    project_name = get_name().replace("-", " ")
    print_random_banner(project_name)
    print(f"{get_name()} v{get_version()}")
    print(f"{get_description()}")
    print(f"Author(s): {get_authors()}")
    print(
        "====================================================================================================="
    )

    parser = argparse.ArgumentParser(
        description="""
        A Selenium-based ChatGPT interaction automation tool.
        This script initializes a browser session, interacts with ChatGPT
        using predefined prompts, and facilitates automated conversations with ChatGPT.
        Ideal for fetching responses and conducting tests or demonstrations.
        """
    )

    config = Configuration()

    user_prompts_default = os.getenv("CHATGPT_USER_PROMPTS")  # Default user prompts from the environment
    if user_prompts_default:
        user_prompts_default = user_prompts_default.split(",")

    # Add arguments for the system prompt and user prompts
    parser.add_argument(
        "--system-prompt",
        default=os.getenv("CHATGPT_SYSTEM_PROMPT"),
        type=str,
        required=False,
        help="System prompt for the chatbot. Provide a single prompt or set "
             "CHATGPT_SYSTEM_PROMPT environment variable with a prompt."
    )
    parser.add_argument(
        "--user-prompts",
        default=user_prompts_default,
        type=str,
        nargs='+',
        required=user_prompts_default is None,  # Require user prompts if not provided in the environment
        help="User prompts for the chatbot. Provide multiple prompts separated by spaces or set the "
             "CHATGPT_USER_PROMPTS environment variable with prompts separated by commas."
    )
    parser.add_argument(
        "--account",
        default=os.getenv("CHATGPT_ACCOUNT"),
        type=str,
        required=False,
        help="Account for authentication. Provide an email or identifier for the account."
             "Set CHATGPT_ACCOUNT environment variable with the account email or identifier."
    )
    parser.add_argument(
        "--accounts",
        default=accounts,
        type=AccountsDeserializer,
        required=False,
        help="Accounts for authentication."
    )
    parser.add_argument(
        "--temporary-chat",
        type=bool,
        default=os.getenv("CHATGPT_TEMPORARY_CHAT") or False,
        required=False,
        help="Enable temporary chat mode. Set CHATGPT_TEMPORARY_CHAT environment variable to 'True' to enable."
    )
    parser.add_argument(
        "--headless",
        type=bool,
        default=os.getenv("CHATGPT_HEADLESS") or False,
        required=False,
        help="Run the browser in headless mode. Set CHATGPT_HEADLESS environment variable to 'True' to enable."
    )

    args = parser.parse_args()

    # Update the configuration with the provided arguments
    config.use_temporary_chat = args.temporary_chat
    config.accounts = args.accounts.get_all_accounts() or accounts.get_all_accounts()
    config.headless = args.headless

    # Pass the arguments to the main function
    main(args.account, args.system_prompt, args.user_prompts, config)
