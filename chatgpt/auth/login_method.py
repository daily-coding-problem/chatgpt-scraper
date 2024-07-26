from abc import ABC, abstractmethod

from chatgpt.browser import Browser

LOGIN_BUTTON_SELECTOR = "button[data-testid='login-button']"
EMAIL_INPUT_SELECTOR = "input[id='email-input']"
CONTINUE_BUTTON_SELECTOR = "button[class='continue-btn']"
PASSWORD_INPUT_SELECTOR = "input[id='password']"
SUBMIT_BUTTON_SELECTOR = "button[type='submit']"
GOOGLE_LOGIN_BUTTON_SELECTOR = "button[data-testid='google-login-button']"
MICROSOFT_LOGIN_BUTTON_SELECTOR = "button[data-testid='microsoft-login-button']"
APPLE_LOGIN_BUTTON_SELECTOR = "button[data-testid='apple-login-button']"


class LoginMethod(ABC):
    def __init__(self, browser: Browser):
        self.browser = browser

    @abstractmethod
    def login(self, accounts: dict) -> bool:
        pass
