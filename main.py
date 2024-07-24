import argparse
from dotenv import load_dotenv
from utilities import print_random_banner
from utilities.poetry import get_name, get_description, get_authors, get_version
from chatgpt.browser import Browser
from chatgpt.chatbot import ChatBot
from chatgpt.chatgpt_interaction import ChatGPTInteraction

# Load environment variables
load_dotenv()


def main(system_prompt: str, user_prompts: [str]):
    browser = Browser("https://chatgpt.com")
    interaction = ChatGPTInteraction(browser)
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

    # Add arguments for the system prompt and user prompts
    parser.add_argument(
        "--system-prompt",
        default=system_prompt,
        type=str,
        required=True,
        help="System prompt for the chatbot."
    )
    parser.add_argument(
        "--user-prompts",
        default=user_prompts,
        type=str,
        nargs='+',
        required=True,
        help="User prompts for the chatbot."
    )

    args = parser.parse_args()

    # Pass the arguments to the main function
    main(args.system_prompt, args.user_prompts)
