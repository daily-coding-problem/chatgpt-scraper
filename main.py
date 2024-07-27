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

# Load environment variables
load_dotenv()

accounts = AccountsDeserializer()


def main(account: str, system_prompt: str, user_prompts: List[str], config: Configuration):
    browser = Browser("https://chatgpt.com")
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

    system_prompt = "You are ChatGPT, a helpful assistant."
    user_prompts = [
        "What is the meaning of life?",
        "How do you handle multiple requests?",
        "Can you give me some advice on productivity?"
    ]

    config = Configuration()

    # Add arguments for the system prompt and user prompts
    parser.add_argument(
        "--system-prompt",
        default=system_prompt,
        type=str,
        required=False,
        help="System prompt for the chatbot."
    )
    parser.add_argument(
        "--user-prompts",
        default=user_prompts,
        type=str,
        nargs='+',
        required=False,
        help="User prompts for the chatbot."
    )
    parser.add_argument(
        "--account",
        default=os.getenv("CHATGPT_ACCOUNT"),
        type=str,
        required=False,
        help="Account for authentication."
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
        default=os.getenv("CHATGPT_TEMPORARY_CHAT"),
        help="Enable temporary chat mode."
    )

    args = parser.parse_args()

    # Update the configuration with the provided arguments
    config.use_temporary_chat = args.temporary_chat
    config.accounts = args.accounts.get_all_accounts() or accounts.get_all_accounts()

    # Pass the arguments to the main function
    main(args.account, args.system_prompt, args.user_prompts, config)
