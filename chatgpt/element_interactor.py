import logging
import time

from selenium.common import ElementClickInterceptedException, TimeoutException, NoSuchElementException, \
    JavascriptException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from undetected_chromedriver import WebElement


class ElementInteractor:
    def __init__(self, browser, max_retries=3, retry_delay=2):
        self.browser = browser
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def wait_for_element(self, by, selector, timeout=10) -> (WebElement or None):
        """
        Wait for the element to be clickable, with a retry mechanism.

        :param by: The type of selection to use (By.CSS_SELECTOR or By.XPATH).
        :param selector: The CSS selector or XPath for the element to wait for.
        :param timeout: The maximum time to wait for the element to be clickable.
        :return: The element if found and clickable, None otherwise.
        """
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

    def find_element(self, by, selector, timeout=10) -> (WebElement or None):
        """
        Find an element using the given selector strategy.

        :param by: The type of selection to use (By.CSS_SELECTOR or By.XPATH).
        :param selector: The CSS selector or XPath for the element to find.
        :param timeout: The maximum time to wait for the element to be present.
        :return: The element if found, None otherwise.
        """
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
        """
        Click the element using ActionChains or JavaScript as a fallback.

        :param element: The element to click.
        """
        time.sleep(2)  # Small delay to allow for the element to be fully visible

        # Check if the element is visible and clickable
        if not element.is_displayed() or not element.is_enabled():
            # Scroll the element into view
            self.scroll_into_view(element)

            # Check if the element is now visible and clickable
            if not element.is_displayed() or not element.is_enabled():
                logging.error(f"Element not clickable: {element.get_attribute('outerHTML')}")
                return

        try:
            ActionChains(self.browser.driver).move_to_element(element).click().perform()
        except (ElementClickInterceptedException, JavascriptException) as e:
            logging.warning(f"Click intercepted, retrying with JavaScript click: {e}")
            try:
                self.browser.driver.execute_script("arguments[0].click();", element)
            except JavascriptException as e:
                logging.error(f"Failed to click element: {element}) with JavaScript: {e}")

    def interact_with_element(self, by, selector, text=None, timeout=10):
        """
        Generic method to interact with an element (click or send text).

        :param by: The type of selection to use (By.CSS_SELECTOR or By.XPATH).
        :param selector: The CSS selector or XPath for the element to interact with.
        :param text: The text to send to the element (if any).
        :param timeout: The maximum time to wait for the element to be clickable.
        :return: True if the interaction was successful, False otherwise.
        """
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

    def wait_for_element_disappear(self, by, selector, timeout=10):
        """
        Wait for an element to disappear from the page.

        :param by: The type of selection to use (By.CSS_SELECTOR or By.XPATH).
        :param selector: The CSS selector or XPath for the element to wait for.
        :param timeout: The maximum time to wait for the element to disappear.
        :return: True if the element disappeared, False otherwise
        """
        try:
            logging.info(f"Waiting for element to disappear: {selector}")
            self.browser.wait_until(EC.invisibility_of_element_located((by, selector)), timeout)
            return True
        except TimeoutException:
            logging.error("Element did not disappear.")
            return False

    def find_elements(self, by, selector):
        """
        Helper method to find elements.

        :param by: The type of selection to use (By.CSS_SELECTOR or By.XPATH).
        :param selector: The CSS selector or XPath for the element to find.
        :return: The elements if found, None otherwise.
        """
        return self.browser.find_elements(by, selector)

