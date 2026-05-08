import random
import time
import allure

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC

from pages.customer_page import CustomerPage
from utils.screenshot import take_screenshot


class CustomerModule:

    def __init__(self, driver):

        self.driver = driver
        self.wait = WebDriverWait(driver, 40)
        self.page = CustomerPage()

    # ---------------- RANDOM DATA ----------------

    def generate_name(self):

        first_names = [
            "John", "Clara", "David", "Emma",
            "Michael", "Sophia", "Daniel", "Olivia"
        ]

        last_names = [
            "Smith", "Brown", "Taylor", "Wilson",
            "Lee", "Walker", "Hall", "Allen"
        ]

        first = random.choice(first_names)
        last = random.choice(last_names)

        return f"test{first}", last

    def random_phone(self):

        return "07" + ''.join(
            random.choices("0123456789", k=8)
        )

    def random_email(self):

        return f"testuser{int(time.time())}@test.com"

    def random_address(self):

        streets = [
            "Main Road",
            "High Street",
            "Lake Road",
            "Station Road"
        ]

        return (
            f"No.{random.randint(1,200)}/A, "
            f"{random.choice(streets)}"
        )

    def random_suburb(self):

        suburbs = [
            "Colombo",
            "Kaduwela",
            "Malabe",
            "Nugegoda",
            "Dehiwala"
        ]

        return random.choice(suburbs)

    def random_postcode(self):

        return str(random.randint(10000, 99999))

    # ---------------- COMMON METHODS ----------------

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

    # ---------------- RANDOM STATE SELECTION ----------------

    def select_random_state(self):

        dropdown = self.wait.until(
            EC.presence_of_element_located(
                self.page.STATE
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            dropdown
        )

        time.sleep(1)

        select = Select(dropdown)

        valid_options = []

        for option in select.options:

            value = option.get_attribute("value")

            text = option.text.strip()

            if value and text.lower() != "select":

                valid_options.append(value)

        random_state = random.choice(valid_options)

        select.select_by_value(random_state)

        print(f"✅ Random State Selected → {random_state}")

        time.sleep(1)

    # ---------------- CREATE CUSTOMER ----------------

    def create_customer(self):

        # ---------------- CLICK NEW ----------------

        with allure.step("Click New Customer Button"):

            self.click(self.page.NEW_BUTTON)

            take_screenshot(
                self.driver,
                "new_customer_clicked"
            )

        # ---------------- GENERATE DATA ----------------

        first_name, last_name = self.generate_name()

        email = self.random_email()

        phone = self.random_phone()

        address = self.random_address()

        suburb = self.random_suburb()

        postcode = self.random_postcode()

        print(
            f"Generated Customer → "
            f"{first_name} {last_name}"
        )

        # ---------------- ENTER DETAILS ----------------

        with allure.step("Enter Customer Details"):

            self.enter_text(
                self.page.FIRST_NAME,
                first_name
            )

            self.enter_text(
                self.page.LAST_NAME,
                last_name
            )

            self.enter_text(
                self.page.EMAIL,
                email
            )

            self.enter_text(
                self.page.PHONE,
                phone
            )

            self.enter_text(
                self.page.ADDRESS,
                address
            )

            self.enter_text(
                self.page.SUBURB,
                suburb
            )

            self.enter_text(
                self.page.POSTCODE,
                postcode
            )

            take_screenshot(
                self.driver,
                "customer_details_entered"
            )

        # ---------------- SELECT RANDOM STATE ----------------

        with allure.step("Select Random State"):

            self.select_random_state()

            take_screenshot(
                self.driver,
                "state_selected"
            )

        # ---------------- WAIT BEFORE CREATE ----------------

        time.sleep(2)

        # ---------------- CREATE CUSTOMER ----------------

        with allure.step("Create Customer"):

            create_btn = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.CREATE_BUTTON
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                create_btn
            )

            time.sleep(1)

            self.driver.execute_script(
                "arguments[0].click();",
                create_btn
            )

            take_screenshot(
                self.driver,
                "customer_created"
            )

            print("✅ SUCCESS: Customer created")