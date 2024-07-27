from chatgpt.auth.generate_otp import generate_otp
from chatgpt.auth.login_method import LoginMethod

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

GOOGLE_LOGIN_BUTTON_SELECTOR = "button[data-testid='google-login-button']"
EMAIL_INPUT_SELECTOR = "input[type='email']"
PASSWORD_INPUT_SELECTOR = "input[type='password']"
NEXT_BUTTON_XPATH = "//button[span[contains(text(), 'Next')]]"
TRY_ANOTHER_WAY_LINK_XPATH = "//button[contains(text(), 'Try another way')]"
SELECT_AUTHENTICATOR_APP_XPATH = "//div[contains(text(), 'Google Authenticator')]"
CODE_TOKEN_INPUT_SELECTOR = "input[id='totpPin']"


class GoogleLogin(LoginMethod):
    def __init__(self, browser, otp_uri: str = None):
        super().__init__(browser, otp_uri)

    def login(self, email: str, account: dict) -> bool:
        if not self.extract_account_info(email, account):
            return False

        if not self.click_google_login_button():
            return False

        if not self.enter_email(self.email, EMAIL_INPUT_SELECTOR, NEXT_BUTTON_XPATH, use_xpath=True):
            return False

        if not self.enter_password(self.password, PASSWORD_INPUT_SELECTOR, NEXT_BUTTON_XPATH, use_xpath=True):
            return False

        if self.try_another_way():
            if not self.select_authenticator_app():
                return False

            if self.otp_auth:
                otp_token = generate_otp(self.otp_auth.get_secret())
                if not self.enter_2fa_token(otp_token, CODE_TOKEN_INPUT_SELECTOR, NEXT_BUTTON_XPATH, use_xpath=True):
                    return False

            return False

        return True

    def click_google_login_button(self) -> bool:
        """
        Click the Google login button.

        :return: True if Google login button is clicked successfully, False otherwise.
        """
        if google_login_button := self.browser.wait_until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, GOOGLE_LOGIN_BUTTON_SELECTOR)
            )
        ):
            google_login_button.click()
            return True

        return False

    def try_another_way(self) -> bool:
        """
        Click the "Try another way" link.

        :return: True if the link is clicked successfully, False otherwise.
        """
        if try_another_way_link := self.browser.wait_until(
            EC.presence_of_element_located(
                (By.XPATH, TRY_ANOTHER_WAY_LINK_XPATH)
            )
        ):
            try_another_way_link.click()
            return True

        return False

    def select_authenticator_app(self) -> bool:
        """
        Select the authenticator app option.

        :return: True if the authenticator app option is selected successfully, False otherwise.
        """
        authenticator_app_option = self.browser.wait_until(
            EC.presence_of_element_located(
                (By.XPATH, SELECT_AUTHENTICATOR_APP_XPATH)
            )
        )
        if authenticator_app_option:
            authenticator_app_option.click()
            return True

        return False
