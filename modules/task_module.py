import os
import json
import time
import allure

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from pages.task_page import TaskPage
from utils.delay_helper import slow_down


ROTATION_FILE = "task_type_index.json"


class TaskModule:

    def __init__(self, driver):

        self.driver = driver
        self.wait = WebDriverWait(driver, 40)
        self.page = TaskPage()

    # ---------------- WAIT UI READY ----------------
    def _wait_ui_ready(self):

        try:
            self.wait.until(
                EC.invisibility_of_element_located(self.page.SPINNER)
            )
        except TimeoutException:
            pass

        slow_down()

    # ---------------- OPEN TASK PAGE ----------------
    def open_tasks(self, url):

        self.driver.get(url)

        self.wait.until(
            EC.url_contains("/supplier/tasks")
        )

        self._wait_ui_ready()

    # ---------------- CLICK NEW ----------------
    def click_new_task(self):

        self._wait_ui_ready()

        btn = self.wait.until(
            EC.element_to_be_clickable(self.page.NEW_BUTTON)
        )

        btn.click()

        slow_down()

    # ---------------- SELECT TASK TYPE ----------------
    def select_rotating_task_type(self):

        with allure.step("Select rotating task type"):

            dropdown = self.wait.until(
                EC.element_to_be_clickable(self.page.TASK_TYPE_DROPDOWN)
            )

            dropdown.click()

            slow_down()

            options = self.wait.until(
                EC.presence_of_all_elements_located(self.page.TASK_TYPE_OPTIONS)
            )

            task_types = [
                opt.text.strip()
                for opt in options
                if opt.text.strip()
            ]

            # load saved index
            if os.path.exists(ROTATION_FILE):

                with open(ROTATION_FILE, "r") as f:
                    index = json.load(f).get("index", 0)

            else:
                index = 0

            selected_type = task_types[index % len(task_types)]

            # save next index
            with open(ROTATION_FILE, "w") as f:
                json.dump({"index": index + 1}, f)

            for opt in options:

                if opt.text.strip() == selected_type:
                    opt.click()
                    slow_down()
                    break

            print(f"✅ Selected Task Type: {selected_type}")

    # ---------------- SELECT USER ----------------
    def select_rotating_user(self):

        with allure.step("Select rotating user"):

            dropdown = self.wait.until(
                EC.element_to_be_clickable(self.page.USER_DROPDOWN)
            )

            dropdown.click()

            slow_down()

            options = self.wait.until(
                EC.presence_of_all_elements_located(self.page.USER_OPTIONS)
            )

            users = [
                opt.text.strip()
                for opt in options
                if opt.text.strip()
            ]

            index = int(time.time()) % len(users)

            selected_user = users[index]

            for opt in options:

                if opt.text.strip() == selected_user:
                    opt.click()
                    slow_down()
                    break

            print(f"✅ Selected User: {selected_user}")

    # ---------------- CREATE TASK ----------------
    def click_create(self):

        self._wait_ui_ready()

        btn = self.wait.until(
            EC.element_to_be_clickable(self.page.CREATE_BUTTON)
        )

        btn.click()

        slow_down()

        self._wait_ui_ready()