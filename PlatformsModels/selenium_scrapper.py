from config import GECKODRIVER, REDDIT_SUBMISSION_PATH
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
import os

logging.basicConfig(format='%(asctime)s - %(levelname)s : %(message)s', level=logging.INFO)


class SeleniumScrapper:
    driver = None
    options = None
    service = None
    screenshotDir = None

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

    def set_screenshot_dir(self, submission_id: str):
        self.screenshotDir = f"../tmp/{submission_id}"

        if not os.path.exists(self.screenshotDir):
            os.mkdir(self.screenshotDir)
            logging.info(f"Created directory {self.screenshotDir}")
            return True
        logging.info("Screenshot directory already exists")

    def screen_shoot_submission(self, submission: dict):
        for key, path_info in REDDIT_SUBMISSION_PATH.items():
            if key == "title":
                self.take_title_screenshot(path_info, submission.get("id"), False)
            elif key == "comments":
                comments_ids = [comment.get("id") for comment in submission["comments"][:3]]
                for comment_id in comments_ids:
                    self.take_title_screenshot(path_info, comment_id, True)

    def take_title_screenshot(self, path_info, id_value, is_comment: bool, retry_counter=0):
        locator = (path_info["handle"], path_info["value"] % id_value)
        condition = ec.presence_of_element_located(locator)
        while retry_counter <= 3:
            try:
                found = self.dynamic_wait(10, condition)
                if found:
                    self.save_screen_shot(found, id_value, is_comment)
                    break
                retry_counter += 1
            except NoSuchElementException:
                logging.error(f"the element {id_value} is not found")
                retry_counter += 1

    def save_screen_shot(self, element: WebElement, handle: str, is_comment: bool):
        screenshot_name = f"{self.screenshotDir}/{'comment' if is_comment else 'title'}_{handle}.png"

        with open(screenshot_name, "wb") as img_file:
            img_file.write(element.screenshot_as_png)

    def dynamic_wait(self, timeout, condition):
        wait = WebDriverWait(self.driver, timeout)
        try:
            return wait.until(condition)
        except TimeoutException:
            logging.error("the element you are looking is not found yet, retrying ...")
