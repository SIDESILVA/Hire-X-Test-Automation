import random
import time

from datetime import datetime, timedelta

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from pages.customer_view_page import CustomerViewPage


class CustomerViewModule:

    def __init__(self, driver):

        self.driver = driver

        self.wait = WebDriverWait(driver, 30)

        self.page = CustomerViewPage()

    # ---------------- INPUT HELPER ----------------

    def set_input(self, element, value):

        self.driver.execute_script("""
            arguments[0].focus();
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));
        """, element, value)

    # ---------------- CLICK HELPER ----------------

    def click(self, locator):

        element = self.wait.until(
            EC.element_to_be_clickable(locator)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            element
        )

        time.sleep(1)

        self.driver.execute_script(
            "arguments[0].click();",
            element
        )

    # ---------------- ADDRESS HANDLER ----------------

    def fill_address_block(self, address_block, prefix="Test"):

        def get_visible_inputs():

            return [
                i for i in address_block.find_elements(
                    By.XPATH,
                    ".//input"
                )
                if i.is_displayed()
            ]

        def get_visible_selects():

            return [
                s for s in address_block.find_elements(
                    By.XPATH,
                    ".//select"
                )
                if s.is_displayed()
            ]

        # ---------------- AUTOCOMPLETE ----------------

        try:

            inputs = get_visible_inputs()

            inputs[0].send_keys("Colombo")

            time.sleep(1)

            inputs[0].send_keys(
                Keys.ARROW_DOWN,
                Keys.ENTER
            )

        except Exception as e:

            print(f"Autocomplete skipped: {e}")

        # WAIT FOR DOM REFRESH

        time.sleep(2)

        # ---------------- TEXT INPUTS ----------------

        try:

            inputs = get_visible_inputs()

            if len(inputs) > 1:

                self.set_input(
                    inputs[1],
                    f"{prefix} Street"
                )

            time.sleep(1)

            inputs = get_visible_inputs()

            if len(inputs) > 2:

                self.set_input(
                    inputs[2],
                    f"{prefix} Line 2"
                )

            time.sleep(1)

            inputs = get_visible_inputs()

            if len(inputs) > 3:

                self.set_input(
                    inputs[3],
                    "Colombo"
                )

            time.sleep(1)

            inputs = get_visible_inputs()

            if len(inputs) > 4:

                self.set_input(
                    inputs[4],
                    "10000"
                )

        except Exception as e:

            print(f"Input error: {e}")

        # ---------------- DROPDOWNS ----------------

        try:

            selects = get_visible_selects()

            country_select = None
            state_select = None

            for s in selects:

                attr = (
                    s.get_attribute("autocomplete") or ""
                ).lower()

                if "country" in attr:

                    country_select = s

                else:

                    state_select = s

            # ---------------- COUNTRY ----------------

            if country_select:

                select = Select(country_select)

                select.select_by_value("AU")

                print("🌍 Country selected")

            time.sleep(2)

            # REFRESH SELECTS AFTER COUNTRY CHANGE

            selects = get_visible_selects()

            for s in selects:

                attr = (
                    s.get_attribute("autocomplete") or ""
                ).lower()

                if "country" not in attr:

                    state_select = s

            # ---------------- STATE ----------------

            if state_select:

                select = Select(state_select)

                self.wait.until(
                    lambda d: len(select.options) > 1
                )

                select.select_by_index(1)

                print("📍 State selected")

        except Exception as e:

            print(f"Dropdown error: {e}")

    # ---------------- MAIN FLOW ----------------

    def complete_booking_flow(self):

        # TENANT

        tenant_input = self.wait.until(
            EC.visibility_of_element_located(
                self.page.TENANT_INPUT
            )
        )

        tenant_input.clear()

        tenant_input.send_keys("GrandRest")

        self.click(
            self.page.SET_TENANT_BUTTON
        )

        self.wait.until(
            EC.url_contains("/home")
        )

        print("✅ Tenant loaded")

        time.sleep(2)

        # PRODUCT

        buttons = self.wait.until(
            EC.presence_of_all_elements_located(
                self.page.VIEW_BUTTONS
            )
        )

        visible = [
            b for b in buttons if b.is_displayed()
        ]

        random.shuffle(visible)

        self.driver.execute_script(
            "arguments[0].click();",
            visible[0]
        )

        print("✅ Product selected")

        time.sleep(2)

        # DATE

        end_date = self.wait.until(
            EC.element_to_be_clickable(
                self.page.HIRE_END_DATE
            )
        )

        tomorrow = (
            datetime.now() + timedelta(days=1)
        )

        self.set_input(
            end_date,
            tomorrow.strftime("%d/%m/%Y")
        )

        # QUANTITY

        qty = self.wait.until(
            EC.element_to_be_clickable(
                self.page.QUANTITY
            )
        )

        qty.clear()

        qty.send_keys("3")

        # REQUEST BOOKING

        self.click(
            self.page.REQUEST_TO_BOOK_BUTTON
        )

        # SHIPPING

        self.wait.until(
            EC.invisibility_of_element_located(
                self.page.SPINNER
            )
        )

        dropdown = self.wait.until(
            EC.element_to_be_clickable(
                self.page.SHIPPING_METHOD
            )
        )

        select = Select(dropdown)

        option = random.choice(
            select.options[1:]
        )

        select.select_by_visible_text(
            option.text
        )

        print(
            f"🚚 Shipping selected: {option.text}"
        )

        # CUSTOMER DETAILS

        email = (
            f"test_"
            f"{datetime.now().strftime('%Y%m%d%H%M%S')}"
            f"@mail.com"
        )

        phone = (
            f"077{random.randint(1000000,9999999)}"
        )

        self.set_input(
            next(
                i for i in self.driver.find_elements(
                    *self.page.EMAIL
                )
                if i.is_displayed()
            ),
            email
        )

        self.set_input(
            next(
                i for i in self.driver.find_elements(
                    *self.page.PHONE
                )
                if i.is_displayed()
            ),
            phone
        )

        self.set_input(
            next(
                i for i in self.driver.find_elements(
                    *self.page.FIRST_NAME
                )
                if i.is_displayed()
            ),
            "Test"
        )

        self.set_input(
            next(
                i for i in self.driver.find_elements(
                    *self.page.LAST_NAME
                )
                if i.is_displayed()
            ),
            "User"
        )

        print("✅ Customer details entered")

        # ADDRESS

        blocks = self.driver.find_elements(
            *self.page.ADDRESS_BLOCKS
        )

        visible_blocks = [
            b for b in blocks if b.is_displayed()
        ]

        print(
            f"📦 Address blocks: {len(visible_blocks)}"
        )

        if len(visible_blocks) == 1:

            self.fill_address_block(
                visible_blocks[0],
                "Pickup"
            )

        elif len(visible_blocks) >= 2:

            try:

                checkbox = self.driver.find_element(
                    *self.page.SAME_ADDRESS_CHECKBOX
                )

                if checkbox.is_selected():

                    self.driver.execute_script(
                        "arguments[0].click();",
                        checkbox
                    )

                    time.sleep(1)

            except:
                pass

            self.fill_address_block(
                visible_blocks[0],
                "Customer"
            )

            self.fill_address_block(
                visible_blocks[1],
                "Delivery"
            )

        # NEXT

        self.click(
            self.page.NEXT_BUTTON
        )

        self.wait.until(
            EC.presence_of_element_located(
                self.page.ORDER_SUMMARY
            )
        )

        print("✅ Order summary opened")

        # TERMS

        checkbox = self.wait.until(
            EC.presence_of_element_located(
                self.page.TERMS_CHECKBOX
            )
        )

        if not checkbox.is_selected():

            self.driver.execute_script(
                "arguments[0].click();",
                checkbox
            )

        print("✅ Terms accepted")

        # FINAL REQUEST

        buttons = self.wait.until(
            EC.presence_of_all_elements_located(
                self.page.REQUEST_BOOKING_BUTTON
            )
        )

        final_btn = next(
            b for b in buttons if b.is_displayed()
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            final_btn
        )

        time.sleep(1)

        self.driver.execute_script(
            "arguments[0].click();",
            final_btn
        )

        print("✅ Final booking clicked")

        # CLOSE MODAL

        self.wait.until(
            EC.visibility_of_element_located(
                self.page.MODAL_FOOTER
            )
        )

        close_buttons = self.driver.find_elements(
            *self.page.CLOSE_BUTTON
        )

        close_btn = next(
            b for b in close_buttons if b.is_displayed()
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            close_btn
        )

        time.sleep(1)

        self.driver.execute_script(
            "arguments[0].click();",
            close_btn
        )

        print("✅ Modal closed")