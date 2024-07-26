import logging

from chatgpt.auth.login_method import LoginMethod, GOOGLE_LOGIN_BUTTON_SELECTOR

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class GoogleLogin(LoginMethod):
    def login(self, accounts: dict) -> bool:
        if google_login_button := self.browser.wait_until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, GOOGLE_LOGIN_BUTTON_SELECTOR)
            )
        ):
            google_login_button.click()
            logging.info("Google login process completed")
            return True
        else:
            logging.error("Google login button not found")
            return False
