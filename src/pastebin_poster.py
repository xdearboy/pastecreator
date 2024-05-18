from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
)
import time
import platform


class PastebinPoster:
    def __init__(self):
        options = Options()
        self.operating_system = platform.system()
        options.headless = True
        if self.operating_system == "Linux":
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=2560,1080")
        service = Service(ChromeDriverManager().install())
        self.browser = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.browser, 10)

    def post_to_pastebin(self, content, title):
        try:
            self.browser.get("https://pastebin.com")
            assert "Pastebin" in self.browser.title

            text_area = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//textarea[@id="postform-text"]')
                )
            )
            self.browser.execute_script("arguments[0].scrollIntoView(true);", text_area)
            text_area.send_keys(content)

            title_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input#postform-name"))
            )
            self.browser.execute_script(
                "arguments[0].scrollIntoView(true);", title_input
            )
            title_input.send_keys(title)

            submit_button = self.wait.until(
                EC.element_to_be_clickable((By.CLASS_NAME, "btn.-big"))
            )
            self.browser.execute_script(
                "arguments[0].scrollIntoView(true);", submit_button
            )
            self.wait.until(EC.visibility_of(submit_button))
            self.browser.execute_script("arguments[0].click();", submit_button)

            self.browser.implicitly_wait(5)
            time.sleep(1)
            print(f"Post created: {self.browser.current_url}")
            return self.browser.current_url
        except (
            TimeoutException,
            NoSuchElementException,
            ElementNotInteractableException,
        ) as e:
            print(f"Error: {e}")
        finally:
            self.browser.quit()
