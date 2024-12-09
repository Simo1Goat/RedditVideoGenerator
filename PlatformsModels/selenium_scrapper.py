from config import GECKODRIVER
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s : %(message)s', level=logging.INFO)


class SeleniumScrapper:
    driver = None
    options = None
    service = None
    screenshotDir = "../tmp/screenshots"

    def __init__(self, headless: bool = False):
        self.get_driver(headless)

    def get_driver(self, headless):
        try:
            self.options = Options()
            self.options.add_argument("--no-sandbox")
            self.options.add_argument("--disable-gpu")
            self.options.add_argument("--incognito")
            self.options.add_argument("--enable-automation")
            if headless:
                self.options.add_argument("--headless")

            # Set the geckodriver path
            self.service = Service(GECKODRIVER)
            # Initialize the webdriver
            self.driver = webdriver.Firefox(options=self.options,
                                            service=self.service)
            self.driver.maximize_window()
        except Exception as e:
            logging.error(f"Error initializing the webdriver, details: {e}")

    def screenShootSubmission(self, submission: dict):
        for key in REDDIT_SUBMISSION_PATH.keys():
            if key == "title":
                title_handles = REDDIT_SUBMISSION_PATH["title"]
                self.takeTitleScreeshot(title_handles["handle"], title_handles["value"] % submission.get("id"))
            elif key == "comments":
                comment_handle = REDDIT_SUBMISSION_PATH["comments"]
                for comment in submission.get("comments", []):
                    self.takeTitleScreeshot(comment_handle["handle"], comment_handle["value"] % comment.get("id"))

    def takeTitleScreeshot(self, handle, id_value, retry_counter=0):
        condition = ec.presence_of_element_located(locator=(handle, id_value))
        while retry_counter <= 3:
            try:
                found = self.dynamic_wait(10, condition)
                if found:
                    self.save_screen_shot(found, id_value)
                    break
                retry_counter += 1
            except NoSuchElementException:
                logging.error(f"the element {id_value} is not found")
                retry_counter += 1

    def save_screen_shot(self, element: WebElement, handle: str):
        screenshot_name = f"{self.screenshotDir}/{handle}.png"

        with open(screenshot_name, "wb") as img_file:
            img_file.write(element.screenshot_as_png)

    def dynamic_wait(self, timeout, condition):
        wait = WebDriverWait(self.driver, timeout)
        try:
            return wait.until(condition)
        except TimeoutException:
            logging.error("the element you are looking is not found yet, retrying ...")
