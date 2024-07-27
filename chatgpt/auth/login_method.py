import logging
from abc import ABC, abstractmethod

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from chatgpt.auth.methods.basic_login import BasicLogin
from chatgpt.auth.methods.google_login import GoogleLogin
from chatgpt.auth.otp_auth.otp_auth import OTPAuth
from chatgpt.browser import Browser

LOGIN_BUTTON_SELECTOR = "button[data-testid='login-button']"


class LoginMethod(ABC):
    def __init__(self, browser: Browser, otp_uri: str = None):
        self.browser = browser
        self.email = None
        self.password = None
        self.otp_auth = OTPAuth(otp_uri) if otp_uri else None

    @abstractmethod
    def login(self, email: str, account: dict) -> bool:
        pass

    @staticmethod
    def derive_login_provider(account: dict) -> BasicLogin or GoogleLogin:
        provider = account.get("provider", "basic")

        if provider == "google":
            return GoogleLogin

        return BasicLogin

    def extract_account_info(self, email: str, account: dict) -> bool:
        if not email:
            logging.error("Email not provided.")
            return False

        if not account:
            logging.error("Account dictionary is empty.")
            return False

        self.email = email
        self.password = account.get("password")
        secret = account.get("secret")

        if not self.password:
            logging.error(f"Password not found for account {email}")
            return False

        if secret:
            otp_auth_uri = OTPAuth.construct_otp_uri(email, secret)
            self.otp_auth = OTPAuth(otp_auth_uri)

        return True

    def _enter_text_and_continue(self, text: str, input_selector: str, button_selector: str, use_xpath: bool = False) -> bool:
        """
        Enter text into an input field and click the continue/submit button.

        :param text: The text to enter.
        :param input_selector: The CSS selector or XPath for the input field.
        :param button_selector: The CSS selector or XPath for the button.
        :param use_xpath: Flag to determine if XPath should be used for button selection.
        :return: True if the text is entered and the button is clicked successfully, False otherwise.
        """
        input_field = self.browser.wait_until(
            EC.presence_of_element_located((By.CSS_SELECTOR, input_selector))
        )

        if input_field is None:
            return False

        input_field.send_keys(text)

        if use_xpath:
            button = self.browser.wait_until(
                EC.element_to_be_clickable((By.XPATH, button_selector))
            )
        else:
            button = self.browser.wait_until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, button_selector))
            )

        if button:
            button.click()
            return True

        return False

    def enter_email(self, email: str, input_selector: str, button_selector: str, use_xpath: bool = False) -> bool:
        """
        Enter the email and continue.

        :param email: The email to enter.
        :param input_selector: The CSS selector or XPath for the email input field.
        :param button_selector: The CSS selector or XPath for the "continue" button.
        :param use_xpath: Flag to determine if XPath should be used for button selection.
        :return: True if email is entered successfully, False otherwise.
        """
        return self._enter_text_and_continue(email, input_selector, button_selector, use_xpath)

    def enter_password(self, password: str, input_selector: str, button_selector: str, use_xpath: bool = False) -> bool:
        """
        Enter the password and submit.

        :param password: The password to enter.
        :param input_selector: The CSS selector or XPath for the password input field.
        :param button_selector: The CSS selector or XPath for the "submit" button.
        :param use_xpath: Flag to determine if XPath should be used for button selection.
        :return: True if password is entered successfully, False otherwise.
        """
        return self._enter_text_and_continue(password, input_selector, button_selector, use_xpath)

    def enter_2fa_token(self, token: str, code_input_selector: str, button_selector: str, use_xpath: bool = False) -> bool:
        """
        Enter the 2FA token and submit.

        :param token: The 2FA token to enter.
        :param code_input_selector: The CSS selector or XPath for the 2FA code input field.
        :param button_selector: The CSS selector or XPath for the "submit" button.
        :param use_xpath: Flag to determine if XPath should be used for button selection.
        :return: True if 2FA token is entered successfully, False otherwise.
        """
        return self._enter_text_and_continue(token, code_input_selector, button_selector, use_xpath)
