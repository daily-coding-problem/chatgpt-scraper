import logging
from abc import ABC, abstractmethod

from selenium.webdriver.common.by import By

from chatgpt.auth.otp_auth.otp_auth import OTPAuth
from chatgpt.browser import Browser
from chatgpt.element_interactor import ElementInteractor

LOGIN_BUTTON_SELECTOR = "button[data-testid='login-button']"


class LoginMethod(ABC):
    def __init__(self, browser: Browser, otp_uri: str = None):
        self.browser = browser
        self.email = None
        self.password = None
        self.otp_auth = {}
        self.element_interactor = ElementInteractor(browser)

        if otp_uri:
            _opt_auth = OTPAuth(otp_uri)
            issuer = _opt_auth.issuer.lower()
            self.otp_auth[issuer] = _opt_auth

    @abstractmethod
    def login(self, email: str, account: dict) -> bool:
        raise NotImplementedError

    @staticmethod
    def derive_login_provider(account: dict):
        # Delayed import to avoid circular dependency
        from chatgpt.auth.methods.basic_login import BasicLogin
        from chatgpt.auth.methods.google_login import GoogleLogin

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
        secrets = account.get("secret", {})

        if not self.password:
            logging.error(f"Password not found for account {email}")
            return False

        if secrets:
            # Iterate over each provider-specific secret and create OTPAuth instances
            self.otp_auth = {}
            for provider, secret in secrets.items():
                if secret:
                    issuer = OTPAuth.derive_issuer_by_provider(provider)
                    otp_auth_uri = OTPAuth.construct_otp_uri(email, secret, issuer=issuer)
                    self.otp_auth[provider] = OTPAuth(otp_auth_uri)
                else:
                    logging.warning(f"No secret found for provider {provider} in account {email}")

        return True

    def find_element(self, by_type: str, selector: str):
        """
        Helper method to find an element.

        :param by_type: The type of selection to use (By.CSS_SELECTOR or By.XPATH).
        :param selector: The CSS selector or XPath for the element to find.
        :return: The element if found, None otherwise.
        """
        return self.element_interactor.find_element(by_type or By.CSS_SELECTOR, selector)

    def click_element(self, by_type: str, selector: str) -> bool:
        """
        Helper method to click an element.

        :param by_type: The type of selection to use (By.CSS_SELECTOR or By.XPATH).
        :param selector: The CSS selector or XPath for the element to click.
        :return: True if an element is clicked successfully, False otherwise.
        """
        return self.element_interactor.interact_with_element(by_type or By.CSS_SELECTOR, selector)

    def _enter_and_click(self, text: str, input_selector: str, button_selector: str, use_xpath: bool) -> bool:
        """
        Helper method to enter text and click the continue/submit button.

        :param text: The text to enter.
        :param input_selector: The CSS selector or XPath for the input field.
        :param button_selector: The CSS selector or XPath for the button.
        :param use_xpath: Flag to determine if XPath should be used for selection.
        :return: True if interaction is successful, False otherwise.
        """
        by_type = By.CSS_SELECTOR if not use_xpath else By.XPATH

        return self.element_interactor.interact_with_element(
            by_type, input_selector, text=text
        ) and self.element_interactor.interact_with_element(
            by_type, button_selector
        )

    def enter_email(self, email: str, input_selector: str, button_selector: str, use_xpath: bool = False) -> bool:
        """
        Enter the email and continue.

        :param email: The email to enter.
        :param input_selector: The CSS selector or XPath for the email input field.
        :param button_selector: The CSS selector or XPath for the "continue" button.
        :param use_xpath: Flag to determine if XPath should be used for button selection.
        :return: True if email is entered successfully, False otherwise.
        """
        return self._enter_and_click(email, input_selector, button_selector, use_xpath)

    def enter_password(self, password: str, input_selector: str, button_selector: str, use_xpath: bool = False) -> bool:
        """
        Enter the password and submit.

        :param password: The password to enter.
        :param input_selector: The CSS selector or XPath for the password input field.
        :param button_selector: The CSS selector or XPath for the "submit" button.
        :param use_xpath: Flag to determine if XPath should be used for button selection.
        :return: True if password is entered successfully, False otherwise.
        """
        return self._enter_and_click(password, input_selector, button_selector, use_xpath)

    def enter_2fa_token(self, token: str, code_input_selector: str, button_selector: str, use_xpath: bool = False) -> bool:
        """
        Enter the 2FA token and submit.

        :param token: The 2FA token to enter.
        :param code_input_selector: The CSS selector or XPath for the 2FA code input field.
        :param button_selector: The CSS selector or XPath for the "submit" button.
        :param use_xpath: Flag to determine if XPath should be used for button selection.
        :return: True if 2FA token is entered successfully, False otherwise.
        """
        return self._enter_and_click(token, code_input_selector, button_selector, use_xpath)
