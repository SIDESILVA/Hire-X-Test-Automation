import time
import allure

from datetime import datetime

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.list_page import ListPage
from utils.screenshot import take_screenshot


class ListModule:

    def __init__(self, driver):

        self.driver = driver

        self.wait = WebDriverWait(driver, 40)

        self.page = ListPage()

    # ---------------- COMMON METHODS ----------------

    def click(self, locator):

        element = self.wait.until(
            EC.element_to_be_clickable(locator)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            element
        )

        time.sleep(0.5)

        self.driver.execute_script(
            "arguments[0].click();",
            element
        )

    def enter_text(self, locator, value):

        field = self.wait.until(
            EC.visibility_of_element_located(locator)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            field
        )

        time.sleep(0.5)

        field.clear()

        field.send_keys(value)

    # ---------------- GENERATE UNIQUE NAME ----------------

    def generate_list_name(self):

        return (
            "Test_" +
            datetime.now().strftime("%Y%m%d%H%M%S")
        )

    # ---------------- CREATE LIST ----------------

    def create_list(self):

        # ---------------- CLICK NEW BUTTON ----------------

        with allure.step("Click New List Button"):

            self.click(
                self.page.NEW_BUTTON
            )

            take_screenshot(
                self.driver,
                "new_list_button_clicked"
            )

            print("✅ SUCCESS: New List button clicked")

        # ---------------- ENTER LIST NAME ----------------

        with allure.step("Enter List Name"):

            unique_name = self.generate_list_name()

            self.enter_text(
                self.page.LIST_NAME,
                unique_name
            )

            print(
                f"✅ Using unique list name: "
                f"{unique_name}"
            )

            take_screenshot(
                self.driver,
                "list_name_entered"
            )

        # ---------------- CLICK CREATE ----------------

        with allure.step("Click Create Button"):

            self.click(
                self.page.CREATE_BUTTON
            )

            take_screenshot(
                self.driver,
                "create_button_clicked"
            )

            print("✅ SUCCESS: Create button clicked")