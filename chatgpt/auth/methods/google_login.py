from chatgpt.auth.generate_otp import generate_otp
from chatgpt.auth.login_method import LoginMethod

from selenium.webdriver.common.by import By

from chatgpt.auth.otp_auth.otp_auth import Providers

GOOGLE_LOGIN_BUTTON_XPATH = "//button[span[contains(text(), 'Continue with Google')]]"
EMAIL_INPUT_XPATH = "//input[@type='email']"
PASSWORD_INPUT_XPATH = "//input[@type='password']"
NEXT_BUTTON_XPATH = "//button[span[contains(text(), 'Next')]]"
TRY_ANOTHER_WAY_LINK_XPATH = "//button[span[text()='Try another way']]"
SELECT_AUTHENTICATOR_APP_XPATH = "//li[contains(.,'Google Authenticator')]"
CODE_TOKEN_INPUT_XPATH = "//input[@id='totpPin']"

# Additional 2FA handling for ChatGPT
# There is an additional 2FA screen for ChatGPT even after entering Google Authenticator code.
# This is because you could configure your ChatGPT account to have a separate 2FA code.
VERIFY_YOUR_IDENTITY_XPATH = "//*[contains(text(), 'Verify Your Identity')]"
CHATGPT_CODE_TOKEN_INPUT_XPATH = "//input[@name='code']"
SUBMIT_BUTTON_XPATH = "//button[@type='submit']"


class GoogleLogin(LoginMethod):
    def __init__(self, browser, otp_uri: str = None):
        super().__init__(browser, otp_uri)

    def login(self, email: str, account: dict) -> bool:
        # Extract account info and check for success
        if not self.extract_account_info(email, account):
            return False

        # Perform Google login steps and return status
        return (
            self._click_element(By.XPATH, GOOGLE_LOGIN_BUTTON_XPATH) and
            self.enter_email(self.email, EMAIL_INPUT_XPATH, NEXT_BUTTON_XPATH, use_xpath=True) and
            self.enter_password(self.password, PASSWORD_INPUT_XPATH, NEXT_BUTTON_XPATH, use_xpath=True) and
            self._handle_2fa()
        )

    def _handle_2fa(self) -> bool:
        """
        Handle Two-Factor Authentication (2FA) if needed.
        :return: True if 2FA is handled successfully or not needed, False otherwise.
        """
        if (
            self._click_element(By.XPATH, TRY_ANOTHER_WAY_LINK_XPATH) and
            self._click_element(By.XPATH, SELECT_AUTHENTICATOR_APP_XPATH)
        ):
            if self.otp_auth:
                otp_token = generate_otp(self.otp_auth[Providers.GOOGLE.value].get_secret())
                if self.enter_2fa_token(
                    otp_token,
                    CODE_TOKEN_INPUT_XPATH,
                    NEXT_BUTTON_XPATH,
                    use_xpath=True
                ):
                    # We could be brought to another 2FA screen.
                    # So, we check if the page contains "Verify Your Identity"
                    # to handle the additional 2FA.
                    if self._find_element(By.XPATH, VERIFY_YOUR_IDENTITY_XPATH):
                        otp_token = generate_otp(self.otp_auth[Providers.CHATGPT.value].get_secret())
                        self.enter_2fa_token(
                            otp_token,
                            CHATGPT_CODE_TOKEN_INPUT_XPATH,
                            SUBMIT_BUTTON_XPATH,
                            use_xpath=True
                        )

            return True

        return False

