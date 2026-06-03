import random
import time
import allure

from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from pages.customer_page import CustomerPage
from utils.delay_helper import slow_down


class CustomerModule:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 60)
        self.page = CustomerPage()
        self.typing_speed = 0.3

    # ---------------- RANDOM DATA ----------------

    def generate_name(self):
        first_names = [
            "John", "Clara", "David",
            "Emma", "Michael", "Sophia",
            "Daniel", "Olivia"
        ]

        last_names = [
            "Smith", "Brown", "Taylor",
            "Wilson", "Lee", "Walker",
            "Hall", "Allen"
        ]

        return f"test{random.choice(first_names)}", random.choice(last_names)

    def random_phone(self):
        return "07" + ''.join(random.choices("0123456789", k=8))

    def random_email(self):
        return f"testuser{int(time.time())}@test.com"

    def random_address(self):
        streets = [
            "Main Road",
            "High Street",
            "Lake Road",
            "Station Road"
        ]

        return f"No.{random.randint(1,200)}/A, {random.choice(streets)}"

    def random_suburb(self):
        return random.choice([
            "Colombo",
            "Kaduwela",
            "Malabe",
            "Nugegoda",
            "Dehiwala"
        ])

    def random_postcode(self):
        return str(random.randint(10000, 99999))

    # ---------------- COMMON ----------------

    def enter_text(self, locator, value):

        field = self.wait.until(
            EC.visibility_of_element_located(locator)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            field
        )

        time.sleep(self.typing_speed)

        field.clear()
        field.send_keys(value)

        time.sleep(self.typing_speed)

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

    # ---------------- STATE ----------------

    def select_random_state(self):

        dropdown = self.wait.until(
            EC.presence_of_element_located(
                self.page.STATE
            )
        )

        select = Select(dropdown)

        valid_options = [
            opt.get_attribute("value")
            for opt in select.options
            if opt.get_attribute("value")
            and "select" not in opt.text.lower()
        ]

        select.select_by_value(
            random.choice(valid_options)
        )

    # ---------------- CREATE CUSTOMER ----------------

    def create_customer(self):

        with allure.step("Open New Customer Form"):
            self.click(self.page.NEW_BUTTON)

        first, last = self.generate_name()
        email = self.random_email()
        phone = self.random_phone()

        with allure.step("Fill Customer Form"):

            self.enter_text(self.page.FIRST_NAME, first)
            self.enter_text(self.page.LAST_NAME, last)
            self.enter_text(self.page.EMAIL, email)
            self.enter_text(self.page.PHONE, phone)

            self.enter_text(
                self.page.ADDRESS,
                self.random_address()
            )

            self.enter_text(
                self.page.SUBURB,
                self.random_suburb()
            )

            self.enter_text(
                self.page.POSTCODE,
                self.random_postcode()
            )

        with allure.step("Select State"):
            self.select_random_state()

        # ==================================================
        # CREATE BUTTON + WAIT FOR DETAILS PAGE
        # ==================================================

        with allure.step("Create Customer"):

            old_url = self.driver.current_url

            create_btn = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.CREATE_BUTTON
                )
            )

            # scroll
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                create_btn
            )

            slow_down(1)

            # click create
            self.driver.execute_script(
                "arguments[0].click();",
                create_btn
            )

            print("✅ Create button clicked")

            # WAIT URL CHANGE
            self.wait.until(
                lambda d: d.current_url != old_url
            )

            print("✅ URL changed")

            # WAIT CUSTOMER DETAILS URL
            self.wait.until(
                EC.url_contains("/customers/")
            )

            print("✅ Navigated to customer details page")

            # WAIT PAGE LOAD
            self.wait.until(
                EC.presence_of_element_located(
                    self.page.CUSTOMER_DETAILS_CONTAINER
                )
            )

            print("✅ Customer details page fully loaded")

            # ==================================================
            # KEEP BROWSER OPEN FOR UI DEMO
            # ==================================================

            print("👀 Keeping browser open for verification...")

            time.sleep(10)

            print("✅ Customer creation flow completed")