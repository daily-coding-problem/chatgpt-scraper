import logging
import random
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from chatgpt.auth.login_method import LoginMethod, LOGIN_BUTTON_SELECTOR
from chatgpt.browser import Browser
from chatgpt.configuration import Configuration
from chatgpt.temporary_chat import TemporaryChat

# Constants for CSS Selectors
CHAT_INPUT_SELECTOR = "textarea[id='prompt-textarea']"
SEND_BUTTON_SELECTOR = "button[data-testid='send-button']"
STOP_BUTTON_SELECTOR = "button[data-testid='stop-button']"
RESPONSE_SELECTOR = "div[data-message-author-role='assistant']"


class ChatGPTInteraction:
    """
    Class to interact with the ChatGPT application.
    """

    def __init__(self, browser: Browser, config: Configuration):
        self.browser = browser
        self.config = config

        self.temporary_chat = TemporaryChat(browser)

    def wait_for_element(self, by: str, value: str, timeout: int = 30):
        """
        Wait for an element to be present on the page.

        :param by: The locator strategy.
        :param value: The locator value.
        :param timeout: The maximum time to wait for the element.
        :return: The web element if found, None otherwise.
        """
        try:
            logging.info(f"Waiting for element: {value}")
            return self.browser.wait_until(EC.presence_of_element_located((by, value)), timeout)
        except TimeoutException:
            logging.error(f"Element not found: {value}")
            return None

    def wait_for_element_disappear(self, by: str, value: str, timeout: int = 30):
        """
        Wait for an element to disappear from the page.

        :param by: The locator strategy.
        :param value: The locator value.
        :param timeout: The maximum time to wait for the element to disappear.
        :return: True if the element disappears, False otherwise.
        """
        try:
            logging.info(f"Waiting for element to disappear: {value}")
            return self.browser.wait_until(EC.invisibility_of_element_located((by, value)), timeout)
        except TimeoutException:
            logging.error(f"Element did not disappear: {value}")
            return False

    def send_message(self, message: str) -> str or None:
        """
        Send a message to the ChatGPT application.

        :param message: The message to send.
        :return: The response that was received.
        """
        logging.info(f"Sending message: {message}")

        chat_input = self.wait_for_element(By.CSS_SELECTOR, CHAT_INPUT_SELECTOR)
        if chat_input is None:
            return None

        for char in message:
            chat_input.send_keys(char)
            time.sleep(random.uniform(0.05, 0.2))

        send_button = self.browser.find_element(By.CSS_SELECTOR, SEND_BUTTON_SELECTOR)
        initial_responses_count = len(self.browser.find_elements(By.CSS_SELECTOR, RESPONSE_SELECTOR))

        send_button.click()

        self.wait_for_element(By.CSS_SELECTOR, STOP_BUTTON_SELECTOR)

        if not self.wait_for_element_disappear(By.CSS_SELECTOR, STOP_BUTTON_SELECTOR):
            logging.error("Stop button did not disappear")
            return None

        self.browser.wait_until(
            lambda driver: len(self.browser.find_elements(By.CSS_SELECTOR, RESPONSE_SELECTOR)) > initial_responses_count
        )

        all_responses = self.browser.find_elements(By.CSS_SELECTOR, RESPONSE_SELECTOR)
        latest_response = all_responses[-1]
        return latest_response.text

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
        if login_button := self.wait_for_element(By.CSS_SELECTOR, LOGIN_BUTTON_SELECTOR):
            login_button.click()
        else:
            logging.error("Login button not found")

    def enable_temporary_chat(self) -> bool:
        """
        Enable temporary chat mode.
        """
        return self.temporary_chat.enable_temporary_chat()
