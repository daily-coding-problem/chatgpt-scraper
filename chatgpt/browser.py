import random
import time

import undetected_chromedriver as uc

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement

from .utilities.is_linux import is_linux


class Browser:
    """
    Class to interact with a Selenium browser.
    """
    def __init__(self, application_url: str, headless: bool = False):
        self.application_url = application_url
        self.driver = self._init_driver(headless)
        self.wait = WebDriverWait(self.driver, 30)
        self._visit_page(self.application_url)

    @staticmethod
    def _init_driver(headless: bool = False):
        """
        Initialize the Selenium driver.

        :return: The Selenium driver.
        """
        options = uc.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-extensions")

        if headless:
            options.add_argument("--headless")

        # Allow clipboard access for specific sites.
        options.add_experimental_option(
            "prefs", {
                "profile.managed_default_content_settings.clipboard": 1,
                "profile.content_settings.exceptions.clipboard": {
                    "https://chatgpt.com:443,*": {"setting": 1}  # Allow clipboard access for chatgpt.com.
                }
            }
        )

        if is_linux():
            options.add_argument("--headless")

        driver = uc.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver

    def _visit_page(self, url: str):
        """
        Visit the application URL.

        :param url: The URL to visit.
        """
        if not url:
            raise ValueError("URL is required.")

        self.driver.get(url)
        time.sleep(random.uniform(2, 5))

    def find_element(self, by: str, value: str) -> WebElement:
        """
        Find an element on the page.

        :param by: The locator strategy.
        :param value: The locator value.
        :return: The element.
        """
        return self.driver.find_element(by, value)

    def find_elements(self, by: str, value: str) -> list[WebElement]:
        """
        Find multiple elements on the page.

        :param by: The locator strategy.
        :param value: The locator value.
        :return: The elements.
        """
        return self.driver.find_elements(by, value)

    def wait_until(self, condition, timeout=30) -> WebElement:
        """
        Wait until a condition is met.

        :param condition: The condition to wait for.
        :param timeout: The timeout in seconds.
        :return: The element.
        """
        return WebDriverWait(self.driver, timeout).until(condition)

    def quit(self):
        """
        Quit the browser.
        """
        self.driver.quit()
