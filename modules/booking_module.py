import time
import random
from datetime import datetime, timedelta

import allure

from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.common.exceptions import (
    StaleElementReferenceException
)

from pages.booking_page import BookingPage

from utils.delay_helper import slow_down


class BookingModule:

    def __init__(self, driver):

        self.driver = driver

        self.wait = WebDriverWait(driver, 30)

        self.page = BookingPage()

    # ---------------- SAFE INPUT ----------------
    def set_input(self, element, value):

        try:

            self.driver.execute_script("""
                arguments[0].scrollIntoView({block:'center'});
                arguments[0].focus();
                arguments[0].value = arguments[1];
                arguments[0].dispatchEvent(
                    new Event('input', { bubbles: true })
                );
                arguments[0].dispatchEvent(
                    new Event('change', { bubbles: true })
                );
            """, element, value)

        except StaleElementReferenceException:

            slow_down()

    # ---------------- OPEN SITE ----------------
    def open_site(self, url):

        self.driver.get(url)
        slow_down()

    # ---------------- TENANT ----------------
    def set_tenant(self, tenant):

        tenant_input = self.wait.until(
            EC.visibility_of_element_located(
                self.page.TENANT_INPUT
            )
        )

        tenant_input.clear()

        tenant_input.send_keys(tenant)

        self.wait.until(
            EC.element_to_be_clickable(
                self.page.SET_TENANT_BTN
            )
        ).click()

        self.wait.until(
            EC.url_contains("/home")
        )

        print("✅ Tenant Loaded")
        slow_down()

    # ---------------- PRODUCT ----------------
    def click_first_product(self):

        buttons = self.wait.until(
            EC.presence_of_all_elements_located(
                self.page.VIEW_BUTTONS
            )
        )

        visible = [
            b for b in buttons
            if b.is_displayed()
        ]

        self.driver.execute_script(
            "arguments[0].click();",
            visible[0]
        )

        print("✅ Product Selected")
        slow_down()

    # ---------------- DATE ----------------
    def set_end_date(self):

        end_date = self.wait.until(
            EC.element_to_be_clickable(
                self.page.END_DATE
            )
        )

        tomorrow = datetime.now() + timedelta(days=1)

        self.set_input(
            end_date,
            tomorrow.strftime("%d/%m/%Y")
        )

        self.driver.find_element(
            By.TAG_NAME,
            "body"
        ).click()

        slow_down()

    # ---------------- QUANTITY ----------------
    def set_quantity(self, qty="3"):

        qty_input = self.wait.until(
            EC.element_to_be_clickable(
                self.page.QUANTITY
            )
        )

        qty_input.clear()

        qty_input.send_keys(qty)

        slow_down()

    # ---------------- REQUEST ----------------
    def request_booking(self):

        self.wait.until(
            EC.element_to_be_clickable(
                self.page.REQUEST_TO_BOOK_BTN
            )
        ).click()

        slow_down()

    # ---------------- SHIPPING ----------------
    def select_random_shipping(self):

        self.wait.until(
            EC.invisibility_of_element_located(
                (By.CLASS_NAME, "spinner-wrapper")
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
            f"✅ Shipping Selected: {option.text}"
        )

        slow_down(2)

    # ---------------- CUSTOMER ----------------
    def fill_customer(self):

        email = (
            f"test_"
            f"{datetime.now().strftime('%Y%m%d%H%M%S')}"
            f"@mail.com"
        )

        phone = (
            f"077"
            f"{random.randint(1000000,9999999)}"
        )

        email_input = self.wait.until(
            EC.visibility_of_element_located(
                self.page.EMAIL
            )
        )

        phone_input = self.driver.find_element(
            *self.page.PHONE
        )

        first_name_input = self.driver.find_element(
            *self.page.FIRST_NAME
        )

        last_name_input = self.driver.find_element(
            *self.page.LAST_NAME
        )

        self.set_input(
            email_input,
            email
        )

        self.set_input(
            phone_input,
            phone
        )

        self.set_input(
            first_name_input,
            "Test"
        )

        self.set_input(
            last_name_input,
            "User"
        )

        # IMPORTANT FIX
        # Trigger blur event properly

        last_name_input.send_keys(Keys.TAB)

        slow_down()

        print("✅ Customer Details Filled")

    # ---------------- ADDRESS ----------------
    def fill_address(self, block, prefix="Test"):

        def get_inputs():

            return [
                i for i in block.find_elements(
                    By.XPATH,
                    ".//input"
                )
                if i.is_displayed()
            ]

        def get_selects():

            return [
                s for s in block.find_elements(
                    By.XPATH,
                    ".//select"
                )
                if s.is_displayed()
            ]

        slow_down()

        inputs = get_inputs()

        selects = get_selects()

        # ---------------- AUTOCOMPLETE ----------------
        if inputs:

            try:

                inputs[0].clear()

                inputs[0].send_keys("Colombo")

                slow_down(1)

                inputs[0].send_keys(
                    Keys.ARROW_DOWN,
                    Keys.ENTER
                )

                slow_down()

            except:
                pass

        # IMPORTANT REFRESH
        inputs = get_inputs()

        # ---------------- INPUTS ----------------
        if len(inputs) > 1:

            self.set_input(
                inputs[1],
                f"{prefix} Street"
            )

        if len(inputs) > 2:

            self.set_input(
                inputs[2],
                f"{prefix} Line 2"
            )

        if len(inputs) > 3:

            self.set_input(
                inputs[3],
                "Colombo"
            )

        if len(inputs) > 4:

            self.set_input(
                inputs[4],
                "10000"
            )

        # ---------------- DROPDOWNS ----------------
        country_select = None

        state_select = None

        for s in selects:

            attr = (
                s.get_attribute("autocomplete")
                or ""
            ).lower()

            if "country" in attr:

                country_select = s

            else:

                state_select = s

        # COUNTRY
        if country_select:

            try:

                Select(country_select).select_by_value("AU")

                print("✅ Country Selected")

            except:
                pass

        slow_down()

        # IMPORTANT REFETCH
        selects = get_selects()

        if state_select:

            try:

                Select(state_select).select_by_index(1)

                print("✅ State Selected")

            except:
                pass

    # ---------------- ADDRESS HANDLER ----------------
    def handle_addresses(self):

        blocks = self.driver.find_elements(
            *self.page.ADDRESS_BLOCKS
        )

        visible_blocks = [
            b for b in blocks
            if b.is_displayed()
        ]

        print(
            f"✅ Visible Address Blocks: "
            f"{len(visible_blocks)}"
        )

        if len(visible_blocks) >= 1:

            self.fill_address(
                visible_blocks[0],
                "Customer"
            )

        if len(visible_blocks) >= 2:

            try:

                checkbox = self.driver.find_element(
                    *self.page.SAME_ADDRESS_CHECKBOX
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    checkbox
                )

            except:
                pass

            self.fill_address(
                visible_blocks[1],
                "Delivery"
            )

            slow_down()

    # ---------------- NEXT ----------------
    def go_next(self):

        time.sleep(2)

        next_btn = self.wait.until(
            EC.element_to_be_clickable(
                self.page.NEXT_BUTTON
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            next_btn
        )

        print("✅ Next Clicked")
        slow_down()

    # ---------------- TERMS ----------------
    def accept_terms(self):

        checkbox = self.wait.until(
            EC.visibility_of_element_located(
                self.page.TERMS_CHECKBOX
            )
        )

        self.driver.execute_script("""
            arguments[0].scrollIntoView({
                block:'center'
            });
        """, checkbox)

        slow_down()

        self.driver.execute_script(
            "arguments[0].click();",
            checkbox
        )

        print("✅ Terms Accepted")

        slow_down()

    # ---------------- FINAL SUBMIT ----------------
    def submit_booking(self):

        btn = self.wait.until(
            EC.element_to_be_clickable(
                self.page.FINAL_BOOK_BTN
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            btn
        )

        print("✅ Booking Submitted")

        slow_down()

    # ---------------- CLOSE MODAL ----------------
    def close_modal(self):

        try:

            close = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.CLOSE_MODAL
                )
            )

            self.driver.execute_script(
                "arguments[0].click();",
                close
            )

            print("✅ Modal Closed")

        except Exception as e:

            print(
                f"Close modal skipped: {e}"
            )
        
        slow_down()