import logging

from chatgpt.auth.login_method import LoginMethod, MICROSOFT_LOGIN_BUTTON_SELECTOR

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class MicrosoftLogin(LoginMethod):
    def login(self, email: str, accounts: dict) -> bool:
        if microsoft_login_button := self.browser.wait_until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, MICROSOFT_LOGIN_BUTTON_SELECTOR)
            )
        ):
            microsoft_login_button.click()
            logging.info("Microsoft login process completed")
            return True
        else:
            logging.error("Microsoft login button not found")
            return False
