import os
import random
import allure
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.list_page import ListPage
from utils.delay_helper import slow_down


class ListModule:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 40)
        self.page = ListPage()

    # ======================================================
    # COMMON ACTIONS
    # ======================================================
    def click(self, locator):

        element = self.wait.until(
            EC.element_to_be_clickable(locator)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            element
        )

        slow_down()

        self.driver.execute_script(
            "arguments[0].click();",
            element
        )

        slow_down()

    def enter_text(self, locator, value):

        field = self.wait.until(
            EC.visibility_of_element_located(locator)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            field
        )

        field.clear()

        field.send_keys(value)

        slow_down()

    # ======================================================
    # CREATE LIST (UNCHANGED)
    # ======================================================
    def create_list(self):

        with allure.step("Click New List Button"):
            self.click(self.page.NEW_BUTTON)

        with allure.step("Enter List Name"):

            unique_name = (
                "Test_" +
                datetime.now().strftime("%Y%m%d%H%M%S")
            )

            self.enter_text(
                self.page.LIST_NAME,
                unique_name
            )

        with allure.step("Click Create Button"):
            self.click(self.page.CREATE_BUTTON)

    # ======================================================
    # OPEN RANDOM LIST
    # ======================================================
    def open_random_list(self):

        with allure.step("Fetch list rows"):

            rows = self.wait.until(
                EC.presence_of_all_elements_located(
                    self.page.LIST_ROWS
                )
            )

        random_row = random.choice(rows)

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            random_row
        )

        slow_down()

        self.driver.execute_script(
            "arguments[0].click();",
            random_row
        )

        slow_down()

    # ======================================================
    # EMAIL FLOW
    # ======================================================
    def click_email_button(self):

        btn = self.wait.until(
            EC.element_to_be_clickable(
                self.page.EMAIL_BUTTON
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            btn
        )

        slow_down()

    def select_random_template(self):

        dropdown = self.wait.until(
            EC.element_to_be_clickable(
                self.page.TEMPLATE_DROPDOWN
            )
        )

        dropdown.click()

        slow_down()

        options = self.driver.find_elements(
            By.XPATH,
            "//select[@name='templateId']/option"
        )

        valid = [
            o for o in options
            if o.get_attribute("value")
            not in ["0: null", "0", "Select template"]
        ]

        random.choice(valid).click()

        slow_down()

    def upload_random_attachment(self):

        project_root = os.path.dirname(
            os.path.dirname(__file__)
        )

        img_folder = os.path.join(
            project_root,
            "data",
            "images"
        )

        images = [
            os.path.join(img_folder, f)
            for f in os.listdir(img_folder)
            if f.endswith((".png", ".jpg", ".jpeg"))
        ]

        file_input = self.wait.until(
            EC.presence_of_element_located(
                self.page.ATTACHMENT_INPUT
            )
        )

        file_input.send_keys(
            random.choice(images)
        )

        slow_down()

    def click_send_button(self):

        btn = self.wait.until(
            EC.element_to_be_clickable(
                self.page.SEND_BUTTON
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            btn
        )

        slow_down()

    def email_flow(self):

        self.click_email_button()

        self.select_random_template()

        self.upload_random_attachment()

        self.click_send_button()

    # ======================================================
    # UPDATE LIST NAME
    # ======================================================
    def update_list_name_and_save(self):

        with allure.step("Replace List Name Completely"):

            field = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.LIST_NAME
                )
            )

            new_value = (
                f"List_{random.randint(10000,99999)}"
            )

            field.clear()

            slow_down()

            field.send_keys(new_value)

            slow_down()

        with allure.step("Save Changes"):

            save_btn = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.SAVE_BUTTON
                )
            )

            self.driver.execute_script(
                "arguments[0].click();",
                save_btn
            )

            slow_down()

    # ======================================================
    # FULL FLOW
    # ======================================================
    def click_view_and_open_customer(self):

        # ==================================================
        # OPEN VIEW
        # ==================================================
        with allure.step("Open View → Customer"):

            view_btn = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.VIEW_BUTTON
                )
            )

            self.driver.execute_script(
                "arguments[0].click();",
                view_btn
            )

            slow_down()

        # ==================================================
        # RETURN TO LIST PAGE
        # ==================================================
        with allure.step("Return to Lists"):

            try:

                sidebar = WebDriverWait(
                    self.driver,
                    8
                ).until(
                    EC.element_to_be_clickable(
                        self.page.SIDEBAR_LISTS
                    )
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    sidebar
                )

                WebDriverWait(
                    self.driver,
                    10
                ).until(
                    EC.presence_of_element_located(
                        self.page.LIST_ROWS
                    )
                )

            except Exception:

                self.driver.execute_script(
                    "window.location.href='/supplier/lists';"
                )

                WebDriverWait(
                    self.driver,
                    10
                ).until(
                    EC.url_contains("/supplier/lists")
                )

        # ==================================================
        # STEP 1: CLICK NEW
        # ==================================================
        with allure.step("Click NEW Button"):

            new_btn = WebDriverWait(
                self.driver,
                10
            ).until(
                EC.element_to_be_clickable(
                    self.page.NEW_BUTTON
                )
            )

            self.driver.execute_script(
                "arguments[0].click();",
                new_btn
            )

            slow_down()

        # ==================================================
        # STEP 2: CREATE NEW LIST
        # ==================================================
        with allure.step("Create New List in Modal"):

            name_input = WebDriverWait(
                self.driver,
                10
            ).until(
                EC.visibility_of_element_located(
                    self.page.MODAL_LIST_NAME_INPUT
                )
            )

            new_list_name = (
                f"List_{random.randint(1000,9999)}"
            )

            name_input.clear()

            name_input.send_keys(new_list_name)

            slow_down()

            create_btn = WebDriverWait(
                self.driver,
                10
            ).until(
                EC.element_to_be_clickable(
                    self.page.MODAL_CREATE_BUTTON
                )
            )

            self.driver.execute_script(
                "arguments[0].click();",
                create_btn
            )

            slow_down(2)

        # ==================================================
        # STEP 3: CLICK ZERO MEMBER ROW
        # ==================================================
        with allure.step("Open ONLY list where Members = 0"):

            zero_row = WebDriverWait(
                self.driver,
                15
            ).until(
                EC.element_to_be_clickable(
                    self.page.ZERO_MEMBER_ROW
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                zero_row
            )

            slow_down()

            self.driver.execute_script(
                "arguments[0].click();",
                zero_row
            )

            slow_down(2)

            print(
                "🚀 CLICKED ZERO MEMBER LIST SUCCESSFULLY"
            )

        # ==================================================
        # STEP 4: CLICK DELETE BUTTON
        # ==================================================
        with allure.step("Click Delete Button"):

            delete_btn = WebDriverWait(
                self.driver,
                15
            ).until(
                EC.element_to_be_clickable(
                    self.page.DELETE_BUTTON
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                delete_btn
            )

            slow_down()

            self.driver.execute_script(
                "arguments[0].click();",
                delete_btn
            )

            slow_down(2)

            print(
                "🗑 DELETE BUTTON CLICKED SUCCESSFULLY"
            )

        # ==================================================
        # STEP 5: CLICK YES BUTTON IN POPUP
        # ==================================================
        with allure.step("Click YES Button in Delete Popup"):

            yes_btn = WebDriverWait(
                self.driver,
                15
            ).until(
                EC.element_to_be_clickable(
                    self.page.YES_BUTTON
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                yes_btn
            )

            slow_down()

            self.driver.execute_script(
                "arguments[0].click();",
                yes_btn
            )

            slow_down(2)

            print(
                "✅ YES BUTTON CLICKED SUCCESSFULLY"
            )