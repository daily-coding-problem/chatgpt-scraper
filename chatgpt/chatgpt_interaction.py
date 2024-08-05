import logging
import random
import time

import pyperclip

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from chatgpt.auth.login_method import LoginMethod, LOGIN_BUTTON_SELECTOR
from chatgpt.browser import Browser
from chatgpt.configuration import Configuration
from chatgpt.element_interactor import ElementInteractor
from chatgpt.temporary_chat import TemporaryChat

# Constants for CSS Selectors
CHAT_INPUT_SELECTOR = "textarea[id='prompt-textarea']"
SEND_BUTTON_SELECTOR = "button[data-testid='send-button']"
STOP_BUTTON_SELECTOR = "button[data-testid='stop-button']"
RESPONSE_SELECTOR = "div[data-message-author-role='assistant']"


class ResponseRetriever:
    def retrieve_response(self, element_interactor):
        """
        Retrieve the response from the given element interactor.

        :param element_interactor: The element interactor to use.
        """
        raise NotImplementedError


class DOMResponseRetriever(ResponseRetriever):
    def retrieve_response(self, element_interactor: ElementInteractor):
        """
        Retrieve the response from the DOM.

        :param element_interactor: The element interactor to use.
        """
        logging.info("Obtaining the response from the DOM.")
        all_responses = element_interactor.find_elements(By.CSS_SELECTOR, RESPONSE_SELECTOR)
        latest_response = all_responses[-1] if all_responses else None
        return latest_response.text if latest_response else None


class CopyButtonResponseRetriever(ResponseRetriever):
    COPY_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" class="icon-md-heavy"><path fill="currentColor" fill-rule="evenodd" d="M7 5a3 3 0 0 1 3-3h9a3 3 0 0 1 3 3v9a3 3 0 0 1-3 3h-2v2a3 3 0 0 1-3 3H5a3 3 0 0 1-3-3v-9a3 3 0 0 1 3-3h2zm2 2h5a3 3 0 0 1 3 3v5h2a1 1 0 0 0 1-1V5a1 1 0 0 0-1-1h-9a1 1 0 0 0-1 1zM5 9a1 1 0 0 0-1 1v9a1 1 0 0 0 1 1h9a1 1 0 0 0 1-1v-9a1 1 0 0 0-1-1z" clip-rule="evenodd"></path></svg>
""".strip()

    def retrieve_response(self, element_interactor: ElementInteractor):
        logging.info("Using copy button to obtain the response.")
        latest_response_element = self.get_latest_response_element(element_interactor)
        if not latest_response_element:
            logging.error("Failed to obtain the latest response element.")
            return None

        parent_element = self.get_parent_element(latest_response_element)
        if not parent_element:
            return None

        copy_button = self.find_copy_button(parent_element)
        if not copy_button:
            return None

        element_interactor.click_element(copy_button)
        logging.info("Clicked the copy button.")
        return pyperclip.paste()

    @staticmethod
    def get_latest_response_element(element_interactor):
        all_responses = element_interactor.find_elements(By.CSS_SELECTOR, RESPONSE_SELECTOR)
        return all_responses[-1] if all_responses else None

    @staticmethod
    def get_parent_element(latest_response_element):
        try:
            return latest_response_element.find_element(By.XPATH, "../..")
        except NoSuchElementException as e:
            logging.error(f"Failed to find parent element: {e}")
            return None

    def find_copy_button(self, parent_element):
        """
        Find the copy button within the parent element using index-based XPath.
        """

        try:
            # Locate the index of the specific parent element within the entire DOM structure.
            parent_xpath = self.construct_xpath(parent_element)
            buttons_xpath = f"{parent_xpath}//button"

            # Find the copy button using the constructed XPath
            buttons = parent_element.find_elements(By.XPATH, buttons_xpath)
            for button in buttons:
                if self.is_copy_button(button):
                    return button
        except NoSuchElementException:
            logging.error("No matching button with the specified SVG was found.")
            return None

    @staticmethod
    def construct_xpath(element):
        """
        Construct the XPath to a given element.
        """
        components = []
        while element is not None and element.tag_name.lower() != 'html':
            parent = element.find_element(By.XPATH, "..")
            children = parent.find_elements(By.XPATH, f"./{element.tag_name.lower()}")

            index = 1 + children.index(element)  # 1-based index
            components.append(f"{element.tag_name.lower()}[{index}]")
            element = parent

        components.reverse()
        return '//' + '/'.join(components)

    @staticmethod
    def is_copy_button(button):
        return CopyButtonResponseRetriever.COPY_SVG in button.get_attribute("outerHTML")


class ChatGPTInteraction:
    """
    Class to interact with the ChatGPT application.
    """

    def __init__(self, browser: Browser, config: Configuration):
        self.browser = browser
        self.config = config

        self.element_interactor = ElementInteractor(browser)
        self.temporary_chat = TemporaryChat(browser)

    def send_message(self, message: str, use_copy_button: bool = True) -> str or None:
        """
        Send a message to the ChatGPT application and retrieve the response.

        :param message: The message to send.
        :param use_copy_button: Whether to use the copy button to obtain the response.
        :return: The response that was received.
        """
        self._type_message(message)
        self._click_send_button()

        self.element_interactor.wait_for_element(By.CSS_SELECTOR, STOP_BUTTON_SELECTOR)
        if not self.element_interactor.wait_for_element_disappear(By.CSS_SELECTOR, STOP_BUTTON_SELECTOR):
            logging.error("Stop button did not disappear.")
            return None

        # Wait for ChatGPT to generate a response
        time.sleep(2)

        response_retriever = CopyButtonResponseRetriever() if use_copy_button else DOMResponseRetriever()
        return response_retriever.retrieve_response(self.element_interactor)

    def _type_message(self, message: str):
        """
        Type the message into the chat input field.

        :param message: The message to type.
        """
        chat_input = self.element_interactor.wait_for_element(By.CSS_SELECTOR, CHAT_INPUT_SELECTOR)
        if chat_input is None:
            logging.error("Chat input element not found.")
            return

        for char in message:
            chat_input.send_keys(char)
            time.sleep(random.uniform(0.05, 0.2))

    def _click_send_button(self):
        """
        Click the "send" button.
        """
        send_button = self.element_interactor.find_element(By.CSS_SELECTOR, SEND_BUTTON_SELECTOR)
        if send_button:
            self.element_interactor.click_element(send_button)
        else:
            logging.error("Send button not found.")

    def login(self, login_method: LoginMethod, email: str) -> bool:
        """
        Perform the login sequence using the provided login method.

        :param login_method: An instance of a class inherited from LoginMethod.
        :param email: The email to use for login.
        :return: True if login is successful, False otherwise.
        """
        logging.info("Starting login process")

        self.click_login_button()

        account = self.config.accounts.get(email)
        if not account:
            logging.error(f"Account details not found for email: {email}")
            return False

        return login_method.login(email, account)

    def click_login_button(self):
        """
        Click the login button.
        """
        logging.info("Clicking the login button")
        if login_button := self.element_interactor.wait_for_element(By.CSS_SELECTOR, LOGIN_BUTTON_SELECTOR):
            login_button.click()
        else:
            logging.error("Login button not found")

    def enable_temporary_chat(self) -> bool:
        """
        Enable temporary chat mode.
        """
        return self.temporary_chat.enable_temporary_chat()
