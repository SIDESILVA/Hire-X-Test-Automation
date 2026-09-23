import time
import random

from datetime import datetime, timedelta

import allure

from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException
)

from pages.booking_page import BookingPage

from utils.delay_helper import slow_down


class BookingModule:

    def __init__(self, driver):

        self.driver = driver

        self.wait = WebDriverWait(driver, 30)

        self.page = BookingPage()

    # =========================================================
    # SAFE INPUT
    # =========================================================

    def set_input(self, element, value):

        try:

            self.driver.execute_script("""
                arguments[0].scrollIntoView({
                    block: 'center'
                });

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

    # =========================================================
    # OPTIONAL ALERT POPUP
    # =========================================================

    def handle_alert_popup(self):

        """
        Handles the optional alert popup.

        If the popup appears:
            div.alert-box
                -> button.btn.btn-primary
                    -> Ok

        If the popup does not appear:
            Continue without failing the test.
        """

        try:

            short_wait = WebDriverWait(
                self.driver,
                3
            )

            ok_button = short_wait.until(
                EC.element_to_be_clickable(
                    self.page.ALERT_OK_BTN
                )
            )

            self.driver.execute_script(
                """
                arguments[0].scrollIntoView({
                    block: 'center'
                });
                """,
                ok_button
            )

            slow_down(0.5)

            self.driver.execute_script(
                "arguments[0].click();",
                ok_button
            )

            print("✅ Alert popup appeared - OK clicked")

            # Wait until popup disappears
            try:

                short_wait.until(
                    EC.invisibility_of_element_located(
                        self.page.ALERT_BOX
                    )
                )

            except TimeoutException:

                print(
                    "⚠️ Alert popup OK clicked, "
                    "but popup did not disappear immediately"
                )

            slow_down()

            return True

        except TimeoutException:

            # Popup did not appear.
            print("ℹ️ No alert popup appeared")

            return False

        except Exception as e:

            print(
                f"⚠️ Alert popup handling skipped: {e}"
            )

            return False

    # =========================================================
    # OPEN SITE
    # =========================================================

    def open_site(self, url):

        self.driver.get(url)

        slow_down()

    # =========================================================
    # TENANT
    # =========================================================

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

        # Handle popup if it appears after tenant loading
        self.handle_alert_popup()

    # =========================================================
    # STEP PAUSE
    # =========================================================

    def step_pause(self, msg=None):

        if msg:

            print(msg)

        slow_down(0.8)

    # =========================================================
    # PRODUCT
    # =========================================================

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

        if not visible:

            raise Exception(
                "No visible product View button found."
            )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            visible[0]
        )

        slow_down()

        self.driver.execute_script(
            "arguments[0].click();",
            visible[0]
        )

        print("✅ Product Selected")

        slow_down()

        # Handle popup if it appears
        self.handle_alert_popup()

    # =========================================================
    # START DATE / TIME / END DATE / TIME
    # =========================================================

    def set_booking_dates(self):

        # Random Start Date
        # 1-10 days from today

        self.selected_start_date = (
            datetime.now()
            + timedelta(
                days=random.randint(1, 10)
            )
        )

        # End Date
        # 1-3 days after Start Date

        self.selected_end_date = (
            self.selected_start_date
            + timedelta(
                days=random.randint(1, 3)
            )
        )

        # =====================================================
        # START DATE
        # =====================================================

        start_date = self.wait.until(
            EC.element_to_be_clickable(
                self.page.START_DATE
            )
        )

        self.set_input(
            start_date,
            self.selected_start_date.strftime(
                "%d/%m/%Y"
            )
        )

        self.driver.find_element(
            By.TAG_NAME,
            "body"
        ).click()

        print(
            f"✅ Start Date : "
            f"{self.selected_start_date.strftime('%d/%m/%Y')}"
        )

        slow_down()

        # =====================================================
        # START TIME
        # =====================================================

        start_dropdown = self.wait.until(
            EC.element_to_be_clickable(
                self.page.START_TIME
            )
        )

        start_select = Select(start_dropdown)

        start_options = []

        for option in start_select.options:

            text = option.text.strip().lower()

            value = (
                option.get_attribute("value")
                or ""
            ).strip()

            if (
                value
                and "select" not in text
                and option.is_enabled()
            ):

                start_options.append(option)

        if not start_options:

            raise Exception(
                "No valid start-time options found."
            )

        selected_start_time = random.choice(
            start_options
        )

        start_select.select_by_visible_text(
            selected_start_time.text
        )

        print(
            f"✅ Start Time : "
            f"{selected_start_time.text}"
        )

        slow_down()

        # =====================================================
        # END DATE
        # =====================================================

        end_date = self.wait.until(
            EC.element_to_be_clickable(
                self.page.END_DATE
            )
        )

        self.set_input(
            end_date,
            self.selected_end_date.strftime(
                "%d/%m/%Y"
            )
        )

        self.driver.find_element(
            By.TAG_NAME,
            "body"
        ).click()

        print(
            f"✅ End Date : "
            f"{self.selected_end_date.strftime('%d/%m/%Y')}"
        )

        slow_down()

        # =====================================================
        # END TIME
        # =====================================================

        end_dropdown = self.wait.until(
            EC.element_to_be_clickable(
                self.page.END_TIME
            )
        )

        end_select = Select(end_dropdown)

        end_options = []

        for option in end_select.options:

            text = option.text.strip().lower()

            value = (
                option.get_attribute("value")
                or ""
            ).strip()

            if (
                value
                and "select" not in text
                and option.is_enabled()
            ):

                end_options.append(option)

        if not end_options:

            raise Exception(
                "No valid end-time options found."
            )

        selected_end_time = random.choice(
            end_options
        )

        end_select.select_by_visible_text(
            selected_end_time.text
        )

        print(
            f"✅ End Time : "
            f"{selected_end_time.text}"
        )

        slow_down()

        print(
            "✅ Booking Date & Time Selection Completed"
        )

    # =========================================================
    # END DATE - SMOKE TEST
    # =========================================================

    def set_end_date(self):

        end_date_value = (
            datetime.now()
            + timedelta(days=1)
        ).strftime("%d/%m/%Y")

        end_date = self.wait.until(
            EC.element_to_be_clickable(
                self.page.END_DATE
            )
        )

        self.set_input(
            end_date,
            end_date_value
        )

        self.driver.find_element(
            By.TAG_NAME,
            "body"
        ).click()

        print(
            f"✅ End Date : {end_date_value}"
        )

        slow_down()

    # =========================================================
    # QUANTITY
    # =========================================================

    def set_quantity(self, qty="3"):

        qty_input = self.wait.until(
            EC.element_to_be_clickable(
                self.page.QUANTITY
            )
        )

        qty_input.clear()

        qty_input.send_keys(qty)

        slow_down()

    # =========================================================
    # REQUEST / ADD TO BOOKING
    # =========================================================

    def request_booking(
        self,
        second_product=False
    ):

        if second_product:

            locator = self.page.ADD_TO_BOOKING_BTN

            button_name = "Add to Booking"

        else:

            locator = self.page.REQUEST_TO_BOOK_BTN

            button_name = "Request to Book"

        button = self.wait.until(
            EC.element_to_be_clickable(
                locator
            )
        )

        self.driver.execute_script(
            """
            arguments[0].scrollIntoView({
                block:'center'
            });
            """,
            button
        )

        slow_down()

        self.driver.execute_script(
            "arguments[0].click();",
            button
        )

        print(
            f"✅ Clicked {button_name}"
        )

        slow_down(2)

        # =====================================================
        # IMPORTANT
        # Check whether alert popup appeared
        # =====================================================

        self.handle_alert_popup()

    # =========================================================
    # ADD MORE PRODUCTS
    # =========================================================

    def add_random_product(self):

        self.wait.until(
            EC.element_to_be_clickable(
                self.page.ADD_MORE_PRODUCTS
            )
        )

        add_btn = self.driver.find_element(
            *self.page.ADD_MORE_PRODUCTS
        )

        self.driver.execute_script(
            """
            arguments[0].scrollIntoView({
                block:'center'
            });
            """,
            add_btn
        )

        slow_down()

        self.driver.execute_script(
            "arguments[0].click();",
            add_btn
        )

        print(
            "✅ Clicked Add More Products"
        )

        slow_down(3)

        # =====================================================
        # WAIT PRODUCT PAGE
        # =====================================================

        self.wait.until(
            EC.presence_of_all_elements_located(
                self.page.VIEW_BUTTONS
            )
        )

        products = [
            button
            for button in self.driver.find_elements(
                *self.page.VIEW_BUTTONS
            )
            if button.is_displayed()
            and button.is_enabled()
        ]

        if not products:

            raise Exception(
                "No products available for second product."
            )

        selected_product = random.choice(
            products
        )

        self.driver.execute_script(
            """
            arguments[0].scrollIntoView({
                block:'center'
            });
            """,
            selected_product
        )

        slow_down()

        self.driver.execute_script(
            "arguments[0].click();",
            selected_product
        )

        print(
            "✅ Second Product Selected"
        )

        slow_down(4)

        # Handle popup if it appears
        self.handle_alert_popup()

    # =========================================================
    # SECOND PRODUCT BOOKING DETAILS
    # =========================================================

    def configure_second_product_booking(self):

        print(
            "✅ Configuring second product booking details"
        )

        slow_down(2)

        self.set_booking_dates()

        slow_down()

        self.set_quantity()

        slow_down()

        self.request_booking(
            second_product=True
        )

    # =========================================================
    # SHIPPING
    # =========================================================

    def select_random_shipping(self):

        try:

            self.wait.until(
                EC.invisibility_of_element_located(
                    (By.CLASS_NAME, "spinner-wrapper")
                )
            )

        except TimeoutException:

            print(
                "⚠️ Spinner still visible, continuing..."
            )

        dropdown = self.wait.until(
            EC.element_to_be_clickable(
                self.page.SHIPPING_METHOD
            )
        )

        select = Select(dropdown)

        valid_options = [
            option
            for option in select.options[1:]
            if option.is_enabled()
        ]

        if not valid_options:

            raise Exception(
                "No valid shipping options found."
            )

        option = random.choice(
            valid_options
        )

        select.select_by_visible_text(
            option.text
        )

        print(
            f"✅ Shipping Selected: "
            f"{option.text}"
        )

        slow_down(2)

        # Handle popup if it appears
        self.handle_alert_popup()

    # =========================================================
    # CUSTOMER
    # =========================================================

    def fill_customer(self):

        email = (
            f"test_"
            f"{datetime.now().strftime('%Y%m%d%H%M%S')}"
            f"@mail.com"
        )

        phone = (
            f"077"
            f"{random.randint(1000000, 9999999)}"
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

        last_name_input.send_keys(
            Keys.TAB
        )

        slow_down()

        print(
            "✅ Customer Details Filled"
        )

    # =========================================================
    # ADDRESS
    # =========================================================

    def fill_address(
        self,
        block,
        prefix="Test"
    ):

        def get_inputs():

            return [
                i
                for i in block.find_elements(
                    By.XPATH,
                    ".//input"
                )
                if i.is_displayed()
            ]

        def get_selects():

            return [
                s
                for s in block.find_elements(
                    By.XPATH,
                    ".//select"
                )
                if s.is_displayed()
            ]

        slow_down()

        inputs = get_inputs()

        selects = get_selects()

        # =====================================================
        # AUTOCOMPLETE
        # =====================================================

        if inputs:

            try:

                inputs[0].clear()

                inputs[0].send_keys(
                    "Colombo"
                )

                slow_down(1)

                inputs[0].send_keys(
                    Keys.ARROW_DOWN,
                    Keys.ENTER
                )

                slow_down()

            except Exception:

                pass

        inputs = get_inputs()

        # =====================================================
        # INPUTS
        # =====================================================

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

        # =====================================================
        # DROPDOWNS
        # =====================================================

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

        # =====================================================
        # COUNTRY
        # =====================================================

        if country_select:

            try:

                Select(
                    country_select
                ).select_by_value("AU")

                print(
                    "✅ Country Selected"
                )

            except Exception:

                pass

        slow_down()

        # IMPORTANT:
        # Re-fetch dropdowns because Angular may recreate them.

        selects = get_selects()

        if state_select:

            try:

                Select(
                    state_select
                ).select_by_index(1)

                print(
                    "✅ State Selected"
                )

            except Exception:

                pass

    # =========================================================
    # ADDRESS HANDLER
    # =========================================================

    def handle_addresses(self):

        blocks = self.driver.find_elements(
            *self.page.ADDRESS_BLOCKS
        )

        visible_blocks = [
            b
            for b in blocks
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

            except Exception:

                pass

            self.fill_address(
                visible_blocks[1],
                "Delivery"
            )

            slow_down()

        # Handle popup if it appears
        self.handle_alert_popup()

    # =========================================================
    # NEXT
    # =========================================================

    def go_next(self):

        time.sleep(2)

        next_btn = self.wait.until(
            EC.element_to_be_clickable(
                self.page.NEXT_BUTTON
            )
        )

        self.driver.execute_script(
            """
            arguments[0].scrollIntoView({
                block:'center'
            });
            """,
            next_btn
        )

        slow_down()

        self.driver.execute_script(
            "arguments[0].click();",
            next_btn
        )

        print(
            "✅ Next Clicked"
        )

        slow_down()

        # Handle optional popup
        self.handle_alert_popup()

    # =========================================================
    # CREDIT CARD - STRIPE TEST CARD
    # =========================================================

    def fill_credit_card_if_enabled(self):

        """
        Automatically fills Stripe test card details
        if the Credit Card section is available.

        Stripe Test Card:

            Card Number : 4242424242424242
            Expiry      : 12/34
            CVC         : 123
            ZIP         : 10000

        If Credit Card is not required,
        the booking flow continues normally.
        """

        print(
            "Checking whether Credit Card is required..."
        )

        try:

            # =================================================
            # CHECK CREDIT CARD SECTION
            # =================================================

            short_wait = WebDriverWait(
                self.driver,
                3
            )

            short_wait.until(
                EC.visibility_of_element_located(
                    self.page.CREDIT_CARD_SECTION
                )
            )

            print(
                "💳 Credit Card section detected"
            )

            # =================================================
            # FIND STRIPE IFRAME
            # =================================================

            stripe_iframe = short_wait.until(
                EC.presence_of_element_located(
                    self.page.STRIPE_CARD_IFRAME
                )
            )

            self.driver.execute_script(
                """
                arguments[0].scrollIntoView({
                    block: 'center'
                });
                """,
                stripe_iframe
            )

            slow_down()

            # =================================================
            # SWITCH TO STRIPE IFRAME
            # =================================================

            self.driver.switch_to.frame(
                stripe_iframe
            )

            print(
                "✅ Switched to Stripe Credit Card iframe"
            )

            # =================================================
            # CARD NUMBER
            # =================================================

            card_number = WebDriverWait(
                self.driver,
                10
            ).until(
                EC.visibility_of_element_located(
                    self.page.STRIPE_CARD_NUMBER
                )
            )

            card_number.click()

            card_number.send_keys(
                "4242424242424242"
            )

            print(
                "✅ Card Number Entered"
            )

            slow_down()

            # =================================================
            # EXPIRY DATE
            # =================================================

            expiry = WebDriverWait(
                self.driver,
                10
            ).until(
                EC.visibility_of_element_located(
                    self.page.STRIPE_CARD_EXPIRY
                )
            )

            expiry.click()

            expiry.send_keys(
                "12/34"
            )

            print(
                "✅ Expiry Date Entered"
            )

            slow_down()

            # =================================================
            # CVC
            # =================================================

            cvc = WebDriverWait(
                self.driver,
                10
            ).until(
                EC.visibility_of_element_located(
                    self.page.STRIPE_CARD_CVC
                )
            )

            cvc.click()

            cvc.send_keys(
                "123"
            )

            print(
                "✅ CVC Entered"
            )

            slow_down()

            # =================================================
            # ZIP / POSTAL CODE
            # =================================================

            postal = WebDriverWait(
                self.driver,
                10
            ).until(
                EC.visibility_of_element_located(
                    self.page.STRIPE_CARD_POSTAL
                )
            )

            postal.click()

            postal.send_keys(
                "10000"
            )

            print(
                "✅ ZIP / Postal Code Entered: 10000"
            )

            slow_down()

            # =================================================
            # VERIFY CARD FIELDS
            # =================================================

            print(
                "Verifying Stripe card fields..."
            )

            try:

                card_number_value = (
                    card_number.get_attribute(
                        "value"
                    )
                )

                expiry_value = (
                    expiry.get_attribute(
                        "value"
                    )
                )

                cvc_value = (
                    cvc.get_attribute(
                        "value"
                    )
                )

                postal_value = (
                    postal.get_attribute(
                        "value"
                    )
                )

                # ---------------------------------------------
                # CARD NUMBER
                # ---------------------------------------------

                if card_number_value:

                    print(
                        "   Card Number field: "
                        f"{'*' * 12}"
                        f"{card_number_value[-4:]}"
                    )

                else:

                    print(
                        "   Card Number field: EMPTY"
                    )

                # ---------------------------------------------
                # EXPIRY
                # ---------------------------------------------

                print(
                    f"   Expiry field: "
                    f"{expiry_value}"
                )

                # ---------------------------------------------
                # CVC
                # ---------------------------------------------

                if cvc_value:

                    print(
                        "   CVC field: "
                        f"{'*' * len(cvc_value)}"
                    )

                else:

                    print(
                        "   CVC field: EMPTY"
                    )

                # ---------------------------------------------
                # ZIP
                # ---------------------------------------------

                print(
                    f"   ZIP field: "
                    f"{postal_value}"
                )

            except Exception as e:

                print(
                    f"⚠️ Could not verify Stripe fields: {e}"
                )

            # =================================================
            # SWITCH BACK TO MAIN PAGE
            # =================================================

            self.driver.switch_to.default_content()

            print(
                "✅ Switched back to main page"
            )

            slow_down(2)

            # =================================================
            # OPTIONAL POPUP
            # =================================================

            self.handle_alert_popup()

            print(
                "✅ Credit Card Details Filled Successfully"
            )

            return True

        # =====================================================
        # CREDIT CARD NOT REQUIRED
        # =====================================================

        except TimeoutException:

            try:

                self.driver.switch_to.default_content()

            except Exception:

                pass

            print(
                "ℹ️ Credit Card is not required - continuing"
            )

            return False

        # =====================================================
        # OTHER ERROR
        # =====================================================

        except Exception as e:

            try:

                self.driver.switch_to.default_content()

            except Exception:

                pass

            print(
                f"❌ Credit Card filling failed: {e}"
            )

            raise


    # =========================================================
    # TERMS
    # =========================================================

    def accept_terms(self):

        checkbox = self.wait.until(
            EC.visibility_of_element_located(
                self.page.TERMS_CHECKBOX
            )
        )

        self.driver.execute_script(
            """
            arguments[0].scrollIntoView({
                block:'center'
            });
            """,
            checkbox
        )

        slow_down()

        self.driver.execute_script(
            "arguments[0].click();",
            checkbox
        )

        print(
            "✅ Terms Accepted"
        )

        slow_down()

    # =========================================================
    # FINAL SUBMIT
    # =========================================================

    def submit_booking(self):

        btn = self.wait.until(
            EC.element_to_be_clickable(
                self.page.FINAL_BOOK_BTN
            )
        )

        self.driver.execute_script(
            """
            arguments[0].scrollIntoView({
                block:'center'
            });
            """,
            btn
        )

        slow_down()

        self.driver.execute_script(
            "arguments[0].click();",
            btn
        )

        print(
            "✅ Booking Submitted"
        )

        slow_down(2)

        # =====================================================
        # IMPORTANT:
        # If the alert popup appears after submitting,
        # click OK automatically.
        # =====================================================

        self.handle_alert_popup()

    # =========================================================
    # CLOSE MODAL
    # =========================================================

    def close_modal(self):

        try:

            close = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.CLOSE_MODAL
                )
            )

            self.driver.execute_script(
                """
                arguments[0].scrollIntoView({
                    block:'center'
                });
                """,
                close
            )

            self.driver.execute_script(
                "arguments[0].click();",
                close
            )

            print(
                "✅ Modal Closed"
            )

        except Exception as e:

            print(
                f"Close modal skipped: {e}"
            )

        slow_down()