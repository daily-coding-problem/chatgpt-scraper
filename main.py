import argparse
import os

from dotenv import load_dotenv

from chatgpt.auth.accounts_deserializer import AccountsDeserializer
from chatgpt.auth.methods.basic_login import BasicLogin
from chatgpt.configuration import Configuration
from utilities import print_random_banner
from utilities.poetry import get_name, get_description, get_authors, get_version
from chatgpt.browser import Browser
from chatgpt.chatbot import ChatBot
from chatgpt.chatgpt_interaction import ChatGPTInteraction

# Load environment variables
load_dotenv()

accounts = AccountsDeserializer()


def main(account: str, system_prompt: str, user_prompts: [str], config: Configuration):
    browser = Browser("https://chatgpt.com")
    interaction = ChatGPTInteraction(browser, config)

    # Log in if an account is provided
    if account and config.get_account(account):
        logged_in = interaction.login(login_method=BasicLogin(browser), email=account)
        if not logged_in:
            print("Failed to log in.")
            return

    chatbot = ChatBot(interaction)

    # Run the chat with the provided prompts
    chatbot.chat(system_prompt, user_prompts)

    # Clean up by quitting the browser
    browser.quit()


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
        default=False,
        help="Enable temporary chat mode."
    )

    args = parser.parse_args()

    # Update the configuration with the provided arguments
    config.use_temporary_chat = args.temporary_chat
    config.accounts = args.accounts.get_all_accounts() or accounts.get_all_accounts()

    # Pass the arguments to the main function
    main(args.account, args.system_prompt, args.user_prompts, config)
