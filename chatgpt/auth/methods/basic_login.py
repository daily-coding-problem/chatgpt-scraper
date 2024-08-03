from chatgpt.auth.generate_otp import generate_otp
from chatgpt.auth.login_method import LoginMethod
from chatgpt.auth.otp_auth.otp_auth import Providers
from chatgpt.browser import Browser

EMAIL_INPUT_SELECTOR = "input[id='email-input']"
CONTINUE_BUTTON_SELECTOR = "button[class='continue-btn']"
PASSWORD_INPUT_SELECTOR = "input[id='password']"
SUBMIT_BUTTON_SELECTOR = "button[type='submit']"
CODE_TOKEN_INPUT_SELECTOR = "input[id='code']"


class BasicLogin(LoginMethod):
    def __init__(self, browser: Browser, otp_uri: str = None):
        super().__init__(browser, otp_uri)

        self.otp_auth = otp_uri is not None

    def login(self, email: str, account: dict) -> bool:
        if not self.extract_account_info(email, account):
            return False

        if not self.enter_email(self.email, EMAIL_INPUT_SELECTOR, CONTINUE_BUTTON_SELECTOR):
            return False

        if not self.enter_password(self.password, PASSWORD_INPUT_SELECTOR, SUBMIT_BUTTON_SELECTOR):
            return False

        if self.otp_auth:
            otp_token = generate_otp(self.otp_auth[Providers.CHATGPT.value].get_secret())
            if not self.enter_2fa_token(otp_token, CODE_TOKEN_INPUT_SELECTOR, SUBMIT_BUTTON_SELECTOR):
                return False

        return True
