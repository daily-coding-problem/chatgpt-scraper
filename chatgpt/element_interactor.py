import logging
import time

from selenium.common import ElementClickInterceptedException, TimeoutException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ElementInteractor:
    def __init__(self, browser, max_retries=3, retry_delay=2):
        self.browser = browser
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def wait_for_element(self, by, selector, timeout=10):
        """Wait for the element to be clickable, with a retry mechanism."""
        attempts = 0
        while attempts < self.max_retries:
            try:
                wait = WebDriverWait(self.browser.driver, timeout)
                element = wait.until(EC.element_to_be_clickable((by, selector)))
                return element
            except TimeoutException:
                logging.warning(f"Attempt {attempts + 1}: Element with {by} {selector} not found or not clickable.")
                time.sleep(self.retry_delay)
                attempts += 1

        logging.error(f"Failed to find or click element after {self.max_retries} attempts.")
        return None

    def find_element(self, by, selector, timeout=10):
        """Find an element using the given selector strategy."""
        attempts = 0
        while attempts < self.max_retries:
            try:
                wait = WebDriverWait(self.browser.driver, timeout)
                element = wait.until(EC.presence_of_element_located((by, selector)))
                return element
            except (NoSuchElementException, TimeoutException) as e:
                logging.warning(f"Attempt {attempts + 1}: Failed to find element with {by} {selector}: {e}")
                time.sleep(self.retry_delay)
                attempts += 1

        logging.error(f"Failed to find element with {by} {selector} after {self.max_retries} attempts.")
        return None

    def scroll_into_view(self, element):
        """Scroll the element into view."""
        self.browser.driver.execute_script("arguments[0].scrollIntoView();", element)
        time.sleep(0.5)  # Small delay to allow for any scrolling animation

    def click_element(self, element):
        """Click the element using ActionChains or JavaScript as a fallback."""
        try:
            ActionChains(self.browser.driver).move_to_element(element).click().perform()
        except ElementClickInterceptedException as e:
            logging.warning(f"Click intercepted, retrying with JavaScript click: {e}")
            self.browser.driver.execute_script("arguments[0].click();", element)

    def interact_with_element(self, by, selector, text=None, timeout=10):
        """Generic method to interact with an element (click or send text)."""
        attempts = 0
        while attempts < self.max_retries:
            try:
                element = self.wait_for_element(by, selector, timeout)
                if element is None:
                    return False

                self.scroll_into_view(element)

                if text:
                    element.send_keys(text)
                else:
                    self.click_element(element)

                return True

            except (ElementClickInterceptedException, TimeoutException) as e:
                logging.warning(f"Attempt {attempts + 1} failed: {e}")
                time.sleep(self.retry_delay)
                attempts += 1

        logging.error(f"Failed to interact with element after {self.max_retries} attempts.")
        return False
