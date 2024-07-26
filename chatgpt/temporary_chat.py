import logging

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from chatgpt.browser import Browser

# Constants for CSS Selectors
TEMP_CHAT_MENU_SELECTOR = "div[id^='radix-'][type='button']"
TEMP_CHAT_SWITCH_SELECTOR = "button[role='switch'][aria-label='Temporary']"
TEMP_CHAT_CONTINUE_BUTTON_SELECTOR = "button.btn-primary"
TEMP_CHAT_VERIFICATION_TEXT = "Temporary Chat"


class TemporaryChat:
    """
    Class to handle enabling temporary chat mode.
    """

    def __init__(self, browser: Browser):
        self.browser = browser

    def enable_temporary_chat(self) -> bool:
        """
        Enable temporary chat mode.
        """
        logging.info("Enabling temporary chat mode")
        if not self.click_temp_chat_menu():
            return False
        if not self.click_temp_chat_switch():
            return False
        if not self.click_temp_chat_continue_button():
            return False
        return self.verify_temporary_chat_enabled()

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

    def click_temp_chat_menu(self) -> bool:
        """
        Click the menu to open temporary chat options.
        """
        return self.click_element(TEMP_CHAT_MENU_SELECTOR, "Temporary chat menu button not found")

    def click_temp_chat_switch(self) -> bool:
        """
        Click the switch to enable temporary chat.
        """
        return self.click_element(TEMP_CHAT_SWITCH_SELECTOR, "Temporary chat switch not found")

    def click_temp_chat_continue_button(self) -> bool:
        """
        Click the "continue" button in the temporary chat popup.
        """
        return self.click_element(TEMP_CHAT_CONTINUE_BUTTON_SELECTOR, "Temporary chat continue button not found")

    def click_element(self, selector: str, error_message: str) -> bool:
        """
        Click an element identified by the given selector.

        :param selector: The CSS selector of the element to click.
        :param error_message: The error message to log if the element is not found.
        :return: True if the element was clicked successfully, False otherwise.
        """
        if element := self.wait_for_element(By.CSS_SELECTOR, selector):
            element.click()
            return True
        logging.error(error_message)
        return False

    def verify_temporary_chat_enabled(self) -> bool:
        """
        Verify that temporary chat is enabled by checking for the presence of specific text.
        """
        if self.wait_for_element(By.XPATH, f"//div[text()='{TEMP_CHAT_VERIFICATION_TEXT}']"):
            logging.info("Temporary chat mode enabled successfully")
            return True
        logging.error("Temporary chat verification text not found")
        return False
