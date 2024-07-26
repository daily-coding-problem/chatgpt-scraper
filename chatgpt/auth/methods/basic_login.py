import logging

from chatgpt.auth.generate_otp import generate_otp
from chatgpt.auth.login_method import LoginMethod, EMAIL_INPUT_SELECTOR, PASSWORD_INPUT_SELECTOR, \
    SUBMIT_BUTTON_SELECTOR, CONTINUE_BUTTON_SELECTOR
from chatgpt.auth.otp_auth.otp_auth import OTPAuth
from chatgpt.browser import Browser

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class BasicLogin(LoginMethod):
    def __init__(self, browser: Browser, otp_uri: str = None):
        super().__init__(browser)
        self.email = None
        self.password = None
        self.otp_auth = OTPAuth(otp_uri) if otp_uri else None

    def login(self, email: str, account: dict) -> bool:
        if not email:
            logging.error("Email not provided.")
            return False

        # Extract password, and secret from account dictionary
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

        if not self.enter_email():
            return False
        if not self.enter_password():
            return False
        if self.otp_auth:
            otp_token = generate_otp(self.otp_auth.get_secret())
            if not self.enter_2fa_token(otp_token):
                return False
        logging.info("Basic login process completed")
        return True

    def enter_email(self) -> bool:
        email_input = self.browser.wait_until(
            EC.presence_of_element_located((By.CSS_SELECTOR, EMAIL_INPUT_SELECTOR))
        )
        if email_input is None:
            logging.error("Email input not found")
            return False
        email_input.send_keys(self.email)
        if continue_button := self.browser.wait_until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, CONTINUE_BUTTON_SELECTOR)
            )
        ):
            continue_button.click()
            return True
        else:
            logging.error("Continue button not found")
            return False

    def enter_password(self) -> bool:
        password_input = self.browser.wait_until(
            EC.presence_of_element_located((By.CSS_SELECTOR, PASSWORD_INPUT_SELECTOR))
        )
        if password_input is None:
            logging.error("Password input not found")
            return False
        password_input.send_keys(self.password)
        if submit_button := self.browser.wait_until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, SUBMIT_BUTTON_SELECTOR)
            )
        ):
            submit_button.click()
            return True
        else:
            logging.error("Submit button not found")
            return False

    def enter_2fa_token(self, token: str) -> bool:
        """
        Enter the 2FA token and submit.

        :return: True if 2FA token is entered successfully, False otherwise.
        """
        code_input_selector = "input[id='code']"
        code_input = self.browser.wait_until(
            EC.presence_of_element_located((By.CSS_SELECTOR, code_input_selector))
        )
        if code_input is None:
            logging.error("2FA code input not found")
            return False
        code_input.send_keys(token)
        if submit_button := self.browser.wait_until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, SUBMIT_BUTTON_SELECTOR)
            )
        ):
            submit_button.click()
            return True
        else:
            logging.error("2FA submit button not found")
            return False
