import logging

from chatgpt.auth.login_method import LoginMethod, APPLE_LOGIN_BUTTON_SELECTOR

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class AppleLogin(LoginMethod):
    def login(self, accounts: dict) -> bool:
        if apple_login_button := self.browser.wait_until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, APPLE_LOGIN_BUTTON_SELECTOR)
            )
        ):
            apple_login_button.click()
            logging.info("Apple login process completed")
            return True
        else:
            logging.error("Apple login button not found")
            return False
