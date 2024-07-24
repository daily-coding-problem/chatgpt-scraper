import logging

from chatgpt.chatgpt_interaction import ChatGPTInteraction


class ChatBot:
    def __init__(self, interaction: ChatGPTInteraction):
        self.interaction = interaction

    def chat(self, system_prompt: str, user_prompts: list):
        """
        Start a chat with the ChatGPT application.

        :param system_prompt: The system prompt.
        :param user_prompts: The list of user prompts.
        """
        logging.info(f"Starting chat with system prompt: {system_prompt}")
        self.interaction.send_message(system_prompt)

        for user_prompt in user_prompts:
            logging.info(f"Sending user prompt: {user_prompt}")
            response = self.interaction.send_message(user_prompt)
            logging.info(f"response: {response}")
