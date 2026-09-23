from ast import arguments
from pickle import GET
from pydoc import text
from email.mime import text
import random
from select import select
import allure
from datetime import datetime, timedelta

from requests import post
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from conftest import driver
from pages.order_page import OrderPage
from utils.delay_helper import slow_down
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class OrderModule:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 40)
        self.page = OrderPage()

    # ---------------- WAIT UI READY ----------------
    def _wait_ui_ready(self):

        try:
            self.wait.until(
                EC.invisibility_of_element_located(self.page.SPINNER)
            )
        except TimeoutException:
            pass

        try:
            self.wait.until(
                EC.invisibility_of_element_located(self.page.OVERLAY)
            )
        except TimeoutException:
            pass

        slow_down()

    # ---------------- PAGE READY ----------------
    def wait_page_ready(self):

        self.wait.until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        self._wait_ui_ready()

    # ---------------- OPEN ORDERS (FIXED) ----------------
    def open_orders(self, url):

        self.driver.delete_all_cookies()
        self.driver.get(url)

        self.wait_page_ready()

        # IMPORTANT: retry logic (fixes your failure)
        try:
            self.wait.until(
                EC.visibility_of_element_located(self.page.NEW_ORDER_BTN)
            )
        except TimeoutException:
            self.driver.refresh()
            self.wait_page_ready()

            self.wait.until(
                EC.visibility_of_element_located(self.page.NEW_ORDER_BTN)
            )

    # ---------------- NEW ORDER ----------------
    def click_new_order(self):

        self._wait_ui_ready()

        btn = self.wait.until(
            EC.element_to_be_clickable(self.page.NEW_ORDER_BTN)
        )

        btn.click()
        slow_down()

    def verify_create_form(self):

        self._wait_ui_ready()

        self.wait.until(
            EC.visibility_of_element_located(self.page.CREATE_TEXT)
        )

    # ---------------- CUSTOMER ----------------
    def select_random_customer(self):

        self._wait_ui_ready()

        dropdown = self.wait.until(
            EC.element_to_be_clickable(self.page.CUSTOMER_DROPDOWN)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            dropdown
        )

        slow_down()

        try:
            dropdown.click()
        except:
            self.driver.execute_script(
                "arguments[0].click();",
                dropdown
            )

        slow_down()

        options = self.wait.until(
            EC.presence_of_all_elements_located(self.page.CUSTOMER_OPTIONS)
        )

        valid_options = [
            opt for opt in options
            if opt.text.strip()
            and "create a new customer" not in opt.text.lower()
        ]

        if not valid_options:
            raise Exception("No valid customers available in dropdown")

        random.choice(valid_options).click()
        slow_down()

    # ---------------- CREATE ORDER ----------------
    def click_create(self):

        self._wait_ui_ready()

        create_btn = self.wait.until(
            EC.presence_of_element_located(self.page.CREATE_BTN)
        )

        self.wait.until(lambda d: create_btn.is_enabled())

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            create_btn
        )

        slow_down()

        try:
            create_btn.click()
        except:
            self.driver.execute_script(
                "arguments[0].click();",
                create_btn
            )

        slow_down()

        self._wait_ui_ready()

    # ---------------- SEND CUSTOMER EMAIL ----------------
    def send_customer_email_with_attachment(self):

        self._wait_ui_ready()

        with allure.step("Send Customer Email With Attachment"):

            # =========================================================
            # WAIT FOR CUSTOMER EMAIL BUTTON
            # =========================================================

            print("Looking for Customer Email button...")

            email_button = self.wait.until(
                EC.visibility_of_element_located(
                    self.page.CUSTOMER_EMAIL_BUTTON
                )
            )

            print("✅ Customer Email button found")

            # =========================================================
            # SCROLL TO EMAIL BUTTON
            # =========================================================

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                email_button
            )

            slow_down()

            # =========================================================
            # CLICK CUSTOMER EMAIL BUTTON
            # =========================================================

            try:

                email_button = self.wait.until(
                    EC.element_to_be_clickable(
                        self.page.CUSTOMER_EMAIL_BUTTON
                    )
                )

                email_button.click()

                print("✅ Customer Email button clicked")

            except Exception as e:

                print(
                    f"Normal click failed: {repr(e)}"
                )

                email_button = self.wait.until(
                    EC.presence_of_element_located(
                        self.page.CUSTOMER_EMAIL_BUTTON
                    )
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    email_button
                )

                slow_down()

                self.driver.execute_script(
                    "arguments[0].click();",
                    email_button
                )

                print(
                    "✅ Customer Email button clicked using JavaScript"
                )

            # =========================================================
            # WAIT FOR EMAIL MODAL
            # =========================================================

            print("Waiting for email modal...")

            self.wait.until(
                EC.visibility_of_element_located(
                    self.page.EMAIL_MODAL
                )
            )

            print("✅ Email modal opened")

            slow_down()

            # =========================================================
            # SELECT EMAIL TEMPLATE
            # =========================================================

            print("Looking for email template dropdown...")

            template_dropdown = self.wait.until(
                EC.visibility_of_element_located(
                    self.page.EMAIL_TEMPLATE_DROPDOWN
                )
            )

            print("✅ Email template dropdown found")

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                template_dropdown
            )

            slow_down()

            # =========================================================
            # GET ALL TEMPLATE OPTIONS
            # =========================================================

            select = Select(template_dropdown)

            valid_templates = []

            for option in select.options:

                option_text = option.text.strip()
                option_value = (
                    option.get_attribute("value") or ""
                ).strip()

                # Skip empty option
                if not option_text:
                    continue

                # Skip "Select a template"
                if (
                    option_text.lower() == "select a template"
                    or "select a template" in option_text.lower()
                ):
                    continue

                # Skip Angular default/null value
                if option_value in (
                    "",
                    "0: null",
                    "null"
                ):
                    continue

                valid_templates.append(option)

            # =========================================================
            # VALIDATE TEMPLATE OPTIONS
            # =========================================================

            if not valid_templates:

                raise Exception(
                    "No valid email templates were found. "
                    "Only 'Select a template' or null options are available."
                )

            # =========================================================
            # CHOOSE RANDOM VALID TEMPLATE
            # =========================================================

            selected_template = random.choice(
                valid_templates
            )

            selected_template_text = (
                selected_template.text.strip()
            )

            selected_template_value = (
                selected_template.get_attribute("value")
            )

            print(
                f"Selecting email template: "
                f"{selected_template_text}"
            )

            print(
                f"Template value: "
                f"{selected_template_value}"
            )

            # =========================================================
            # SELECT TEMPLATE
            # =========================================================

            select.select_by_value(
                selected_template_value
            )

            slow_down()

            # =========================================================
            # VERIFY TEMPLATE WAS ACTUALLY SELECTED
            # =========================================================

            self.wait.until(
                lambda d: (
                    d.find_element(
                        *self.page.EMAIL_TEMPLATE_DROPDOWN
                    )
                    .get_attribute("value")
                    not in (
                        "",
                        "0: null",
                        "null"
                    )
                )
            )

            current_template = Select(
                self.driver.find_element(
                    *self.page.EMAIL_TEMPLATE_DROPDOWN
                )
            ).first_selected_option

            print(
                f"✅ Email template selected: "
                f"{current_template.text.strip()}"
            )

            # =========================================================
            # ATTACHMENT INPUT
            # =========================================================

            print("Looking for attachment input...")

            attachment_input = self.wait.until(
                EC.presence_of_element_located(
                    self.page.EMAIL_ATTACHMENT_INPUT
                )
            )

            print("✅ Attachment input found")

            # =========================================================
            # FIND IMAGE FROM data/images
            # =========================================================

            import os

            project_root = os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            )

            images_folder = os.path.join(
                project_root,
                "data",
                "images"
            )

            if not os.path.isdir(images_folder):

                raise Exception(
                    f"Images folder does not exist: "
                    f"{images_folder}"
                )

            image_files = [
                os.path.join(images_folder, file)
                for file in os.listdir(images_folder)
                if file.lower().endswith(
                    (
                        ".png",
                        ".jpg",
                        ".jpeg",
                        ".gif",
                        ".webp"
                    )
                )
            ]

            if not image_files:

                raise Exception(
                    f"No attachment images found in: "
                    f"{images_folder}"
                )

            # =========================================================
            # SELECT RANDOM IMAGE
            # =========================================================

            attachment_path = random.choice(
                image_files
            )

            print(
                f"Email Attachment: {attachment_path}"
            )

            if not os.path.isfile(attachment_path):

                raise Exception(
                    f"Attachment file does not exist: "
                    f"{attachment_path}"
                )

            # =========================================================
            # UPLOAD ATTACHMENT
            # =========================================================

            attachment_input.send_keys(
                attachment_path
            )

            print("✅ Attachment uploaded")

            slow_down()

            # =========================================================
            # WAIT FOR SEND BUTTON
            # =========================================================

            print(
                "Waiting for Send button to become enabled..."
            )

            def send_button_ready(driver):

                try:

                    button = driver.find_element(
                        *self.page.EMAIL_SEND_BUTTON
                    )

                    return (
                        button.is_displayed()
                        and button.is_enabled()
                    )

                except Exception:

                    return False

            self.wait.until(
                send_button_ready
            )

            print(
                "✅ Send button is visible and enabled"
            )

            # =========================================================
            # GET SEND BUTTON AGAIN
            # =========================================================

            send_button = self.wait.until(
                EC.visibility_of_element_located(
                    self.page.EMAIL_SEND_BUTTON
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                send_button
            )

            slow_down()

            # =========================================================
            # CLICK SEND
            # =========================================================

            try:

                send_button = self.wait.until(
                    EC.element_to_be_clickable(
                        self.page.EMAIL_SEND_BUTTON
                    )
                )

                send_button.click()

                print("✅ Send button clicked")

            except Exception as e:

                print(
                    f"Normal Send button click failed: "
                    f"{repr(e)}"
                )

                # Re-find button because Angular may have
                # re-rendered it after template/attachment changes.

                send_button = self.wait.until(
                    EC.presence_of_element_located(
                        self.page.EMAIL_SEND_BUTTON
                    )
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    send_button
                )

                slow_down()

                self.driver.execute_script(
                    "arguments[0].click();",
                    send_button
                )

                print(
                    "✅ Send button clicked using JavaScript"
                )

            # =========================================================
            # WAIT FOR EMAIL MODAL TO CLOSE
            # =========================================================

            print(
                "Waiting for email modal to close..."
            )

            self.wait.until(
                EC.invisibility_of_element_located(
                    self.page.EMAIL_MODAL
                )
            )

            self._wait_ui_ready()

            print(
                "✅ Customer email sent with attachment"
            )
    
    # =========================================================
    # EDIT BILLING ADDRESS
    # =========================================================

    def edit_billing_address(self):

        self._wait_ui_ready()

        with allure.step(
            "Edit Billing Address"
        ):

            # =================================================
            # WAIT FOR BILLING ADDRESS EDIT BUTTON
            # =================================================

            print(
                "Looking for Billing Address Edit button..."
            )

            edit_button = self.wait.until(
                EC.visibility_of_element_located(
                    self.page.BILLING_ADDRESS_EDIT_BUTTON
                )
            )

            print(
                "✅ Billing Address Edit button found"
            )

            # =================================================
            # SCROLL TO EDIT BUTTON
            # =================================================

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                edit_button
            )

            slow_down()

            # =================================================
            # CLICK EDIT
            # =================================================

            try:

                edit_button = self.wait.until(
                    EC.element_to_be_clickable(
                        self.page.BILLING_ADDRESS_EDIT_BUTTON
                    )
                )

                edit_button.click()

                print(
                    "✅ Billing Address Edit button clicked"
                )

            except Exception as e:

                print(
                    "Normal Billing Address Edit "
                    "button click failed: "
                    f"{repr(e)}"
                )

                edit_button = self.wait.until(
                    EC.presence_of_element_located(
                        self.page.BILLING_ADDRESS_EDIT_BUTTON
                    )
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    edit_button
                )

                slow_down()

                self.driver.execute_script(
                    "arguments[0].click();",
                    edit_button
                )

                print(
                    "✅ Billing Address Edit button "
                    "clicked using JavaScript"
                )

            # =================================================
            # WAIT FOR BILLING ADDRESS FORM
            # =================================================

            print(
                "Waiting for Billing Address form..."
            )

            self.wait.until(
                EC.visibility_of_element_located(
                    self.page.BILLING_ADDRESS_FORM
                )
            )

            print(
                "✅ Billing Address form opened"
            )

            slow_down()

    
    # =========================================================
    # EDIT BILLING ADDRESS
    # =========================================================

    def edit_billing_address(self):

        self._wait_ui_ready()

        with allure.step("Edit Billing Address"):

            # =================================================
            # CLICK BILLING ADDRESS EDIT
            # =================================================

            print(
                "Looking for Billing Address Edit button..."
            )

            edit_button = self.wait.until(
                EC.visibility_of_element_located(
                    self.page.BILLING_ADDRESS_EDIT_BUTTON
                )
            )

            print(
                "✅ Billing Address Edit button found"
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                edit_button
            )

            slow_down()

            try:

                edit_button = self.wait.until(
                    EC.element_to_be_clickable(
                        self.page.BILLING_ADDRESS_EDIT_BUTTON
                    )
                )

                edit_button.click()

                print(
                    "✅ Billing Address Edit button clicked"
                )

            except Exception as e:

                print(
                    "Normal Billing Address Edit "
                    f"button click failed: {repr(e)}"
                )

                edit_button = self.wait.until(
                    EC.presence_of_element_located(
                        self.page.BILLING_ADDRESS_EDIT_BUTTON
                    )
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    edit_button
                )

                slow_down()

                self.driver.execute_script(
                    "arguments[0].click();",
                    edit_button
                )

                print(
                    "✅ Billing Address Edit button "
                    "clicked using JavaScript"
                )

            # =================================================
            # WAIT FOR BILLING ADDRESS MODAL
            # =================================================

            print(
                "Waiting for Billing Address form..."
            )

            self.wait.until(
                EC.visibility_of_element_located(
                    self.page.BILLING_ADDRESS_MODAL
                )
            )

            self.wait.until(
                EC.visibility_of_element_located(
                    self.page.BILLING_ADDRESS_FORM
                )
            )

            print(
                "✅ Billing Address form opened"
            )

            slow_down()

            # =================================================
            # ADDRESS 1
            # =================================================

            print(
                "Editing Address 1..."
            )

            address_1 = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.BILLING_ADDRESS_1_INPUT
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                address_1
            )

            slow_down()

            address_1.clear()

            address_1.send_keys(
                f"{random.randint(10, 999)} "
                "Automation Street"
            )

            self.driver.execute_script(
                """
                arguments[0].dispatchEvent(
                    new Event('input', {bubbles:true})
                );

                arguments[0].dispatchEvent(
                    new Event('change', {bubbles:true})
                );
                """,
                address_1
            )

            print(
            "✅ Address 1 updated"
            )

            slow_down()

            # =================================================
            # ADDRESS 2
            # =================================================

            print(
                "Editing Address 2..."
            )

            address_2 = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.BILLING_ADDRESS_2_INPUT
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                address_2
            )

            slow_down()

            address_2.clear()

            address_2.send_keys(
                f"Unit {random.randint(1, 50)}"
            )

            self.driver.execute_script(
                """
                arguments[0].dispatchEvent(
                    new Event('input', {bubbles:true})
                );

                arguments[0].dispatchEvent(
                    new Event('change', {bubbles:true})
                );
                """,
                address_2
            )

            print(
                "✅ Address 2 updated"
            )

            slow_down()

            # =================================================
            # SUBURB
            # =================================================

            print(
                "Editing Suburb..."
            )

            suburb = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.BILLING_SUBURB_INPUT
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                suburb
            )

            slow_down()

            suburb.clear()

            suburb.send_keys(
                "Sydney"
            )

            self.driver.execute_script(
                """
                arguments[0].dispatchEvent(
                    new Event('input', {bubbles:true})
                );

                arguments[0].dispatchEvent(
                    new Event('change', {bubbles:true})
                );
                """,
                suburb
            )

            print(
                "✅ Suburb updated"
            )

            slow_down()

            # =================================================
            # STATE
            # =================================================

            print(
                "Looking for State dropdown..."
            )

            state_dropdown = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.BILLING_STATE_DROPDOWN
                )
            )
        
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                state_dropdown
            )

            slow_down()

            state_select = Select(
                state_dropdown
            )

            valid_states = []

            for option in state_select.options:

                option_text = (
                    option.text.strip()
                )

                option_value = (
                    option.get_attribute("value")
                    or ""
                ).strip()

                if not option_text:
                    continue

                if not option_value:
                    continue

                if option_text.lower() in (
                    "select",
                    "select state",
                    "please select"
                ):
                    continue

                valid_states.append(
                    option
                )

            if not valid_states:

                raise Exception(
                    "No valid State options "
                    "were found."
                )

            # =================================================
            # SELECT NSW
            # =================================================

            nsw_option = None

            for option in valid_states:

                if (
                    option.get_attribute("value")
                    == "NSW"
                    ):

                    nsw_option = option
                    break

            if nsw_option:

                selected_state = nsw_option

            else:

                selected_state = random.choice(
                    valid_states
                )

            selected_state_value = (
                selected_state.get_attribute(
                    "value"
                )
            )

            selected_state_text = (
                selected_state.text.strip()
            )

            print(
                "Selecting State: "
                f"{selected_state_text}"
            )

            state_select.select_by_value(
                selected_state_value
            )

            slow_down()

            # =================================================
            # VERIFY STATE
            # =================================================

            self.wait.until(
                lambda d:
                Select(
                    d.find_element(
                        *self.page.BILLING_STATE_DROPDOWN
                    )
                ).first_selected_option.get_attribute(
                    "value"
                ) == selected_state_value
            )

            print(
                "✅ State selected: "
                f"{selected_state_text}"
            )

            slow_down()

            # =================================================
            # POSTCODE
            # =================================================

            print(
                "Editing Postcode..."
            )

            postcode = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.BILLING_POSTCODE_INPUT
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                postcode
            )

            slow_down()

            postcode.clear()

            # NSW / Sydney postcode
            postcode.send_keys(
                "2000"
            )

            self.driver.execute_script(
                """
                arguments[0].dispatchEvent(
                    new Event('input', {bubbles:true})
                );

                arguments[0].dispatchEvent(
                    new Event('change', {bubbles:true})
                );
                """,
                postcode
            )

            print(
                "✅ Postcode updated"
            )

            slow_down()

            # =================================================
            # SAVE BILLING ADDRESS
            # =================================================

            print(
                "Looking for Billing Address Save button..."
            )

            # First confirm that the correct billing modal
            # is still visible.
            self.wait.until(
                EC.visibility_of_element_located(
                    self.page.BILLING_ADDRESS_MODAL
                )
            )

            # Re-find the Save button every time because
            # Angular can re-render the modal after field changes.
            def billing_save_button_ready(driver):

                try:

                    button = driver.find_element(
                        *self.page.BILLING_ADDRESS_SAVE_BUTTON
                    )

                    if (
                        button.is_displayed()
                        and button.is_enabled()
                    ):

                        return button

                    return False

                except Exception:

                    return False

            save_button = self.wait.until(
                billing_save_button_ready
            )

            print(
                "✅ Billing Address Save button found"
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                save_button
            )

            slow_down()

            # =================================================
            # CLICK SAVE
            # =================================================

            try:

                save_button.click()

                print(
                    "✅ Billing Address Save button clicked"
                )

            except Exception as e:

                print(
                    "Normal Billing Address Save "
                    f"button click failed: {repr(e)}"
                )

                # Re-find after possible Angular re-render
                save_button = self.wait.until(
                    billing_save_button_ready
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    save_button
                )

                slow_down()

                self.driver.execute_script(
                    "arguments[0].click();",
                    save_button
                )

                print(
                    "✅ Billing Address Save button "
                    "clicked using JavaScript"
                )

            # =================================================
            # WAIT FOR BILLING MODAL TO CLOSE
            # =================================================

            print(
                "Waiting for Billing Address form "
                "to close..."
            )

            self.wait.until(
                EC.invisibility_of_element_located(
                    self.page.BILLING_ADDRESS_MODAL
                )
            )

            self._wait_ui_ready()

            print(
                "✅ Billing Address updated successfully"
            )

    # =========================================================
    # SET START DATE AND START TIME
    # =========================================================

    def set_start_date_and_time(self):

        self._wait_ui_ready()

        with allure.step(
            "Set Start Date And Start Time"
        ):

            # =================================================
            # CALCULATE TOMORROW'S DATE
            # =================================================

            start_datetime = (
                datetime.now() +
                timedelta(days=1)
            )

            start_date = start_datetime.strftime(
                "%d/%m/%Y"
            )

            print(
                "Today's date:",
                datetime.now().strftime("%d/%m/%Y")
            )

            print(
                "Start date will be:",
                start_date
            )

            # =================================================
            # START DATE
            # =================================================

            print(
                "Looking for Start Date input..."
            )

            start_date_input = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.START_DATE_INPUT
                )
            )

            print(
                "✅ Start Date input found"
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                start_date_input
            )

            slow_down()

            # Re-find the element because Angular can re-render
            start_date_input = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.START_DATE_INPUT
                )
            )

            # =================================================
            # CLEAR EXISTING DATE
            # =================================================

            try:

                start_date_input.click()

                start_date_input.clear()

            except Exception:

                self.driver.execute_script(
                    """
                    arguments[0].value = '';
                    arguments[0].dispatchEvent(
                        new Event('input', {bubbles:true})
                    );
                    """,
                    start_date_input
                )

            slow_down()

            # =================================================
            # ENTER TOMORROW'S DATE
            # =================================================

            start_date_input.send_keys(
                start_date
            )

            # =================================================
            # TRIGGER ANGULAR CHANGE DETECTION
            # =================================================

            self.driver.execute_script(
                """
                arguments[0].dispatchEvent(
                    new Event('input', {bubbles:true})
                );

                arguments[0].dispatchEvent(
                    new Event('change', {bubbles:true})
                );

                arguments[0].dispatchEvent(
                    new Event('blur', {bubbles:true})
                );
                """,
                start_date_input
            )

            slow_down()

            # =================================================
            # VERIFY DATE
            # =================================================

            current_start_date = start_date_input.get_attribute(
                "value"
            )

            print(
                "Start Date entered:",
                current_start_date
            )

            if current_start_date != start_date:

                print(
                    "Start Date value differs from expected. "
                    "Re-applying date..."
                )

                start_date_input = self.wait.until(
                    EC.element_to_be_clickable(
                        self.page.START_DATE_INPUT
                    )
                )

                self.driver.execute_script(
                    "arguments[0].value='';",
                    start_date_input
                )

                start_date_input.send_keys(
                    start_date
                )

                self.driver.execute_script(
                    """
                    arguments[0].dispatchEvent(
                        new Event('input', {bubbles:true})
                    );

                    arguments[0].dispatchEvent(
                        new Event('change', {bubbles:true})
                    );
                    """,
                    start_date_input
                )

                slow_down()

            print(
                "✅ Start Date set:",
                start_date
            )

            # =================================================
            # START TIME DROPDOWN
            # =================================================

            print(
                "Looking for Start Time dropdown..."
            )

            start_time_dropdown = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.START_TIME_DROPDOWN
                )
            )

            print(
                "✅ Start Time dropdown found"
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                start_time_dropdown
            )

            slow_down()

            # =================================================
            # GET VALID TIME OPTIONS
            # =================================================

            start_time_select = Select(
                start_time_dropdown
            )

            valid_time_options = []

            for option in start_time_select.options:

                option_text = (
                    option.text.strip()
                )

                option_value = (
                    option.get_attribute("value")
                    or ""
                ).strip()

                # Skip empty options
                if not option_text:
                    continue

                # Skip null/empty values
                if not option_value:
                    continue

                # Skip default option
                if (
                    option_text.lower()
                    in (
                        "select time",
                        "please select",
                        "select",
                    )
                ):
                    continue

                if option_value.lower() in (
                    "null",
                    "0: null",
                    "",
                ):
                    continue

                valid_time_options.append(
                    option
                )

            # =================================================
            # VALIDATE TIME OPTIONS
            # =================================================

            if not valid_time_options:

                raise Exception(
                    "No valid Start Time options "
                    "were found in the dropdown."
                )

            # =================================================
            # SELECT RANDOM VALID START TIME
            # =================================================

            selected_time = random.choice(
                valid_time_options
            )

            selected_time_value = (
                selected_time.get_attribute(
                    "value"
                )
            )

            selected_time_text = (
                selected_time.text.strip()
            )

            print(
                "Selecting Start Time:",
                selected_time_text
            )

            print(
                "Start Time value:",
                selected_time_value
            )

            # =================================================
            # SELECT TIME
            # =================================================

            start_time_select.select_by_value(
                selected_time_value
            )

            slow_down()

            # =================================================
            # VERIFY TIME
            # =================================================

            self.wait.until(
                lambda d:
                Select(
                    d.find_element(
                        *self.page.START_TIME_DROPDOWN
                    )
                ).first_selected_option.get_attribute(
                    "value"
                ) == selected_time_value
            )

            selected_time_after = Select(
                self.driver.find_element(
                    *self.page.START_TIME_DROPDOWN
                )
            ).first_selected_option

            print(
                "✅ Start Time selected:",
                selected_time_after.text.strip()
            )

            # =================================================
            # TRIGGER CHANGE EVENT
            # =================================================

            self.driver.execute_script(
                """
                arguments[0].dispatchEvent(
                    new Event('change', {bubbles:true})
                );
                """,
                self.driver.find_element(
                    *self.page.START_TIME_DROPDOWN
                )
            )

            slow_down()

            self._wait_ui_ready()

            print(
                "✅ Start Date and Start Time "
                "updated successfully"
            )

    # =========================================================
    # SET END DATE AND END TIME
    # =========================================================

    def set_end_date_plus_two_days(self):

        self._wait_ui_ready()

        with allure.step(
            "Set End Date (+2 Days) And End Time"
        ):

            # =================================================
            # CALCULATE END DATE
            # =================================================

            end_datetime = (
                datetime.now() +
                timedelta(days=2)
            )

            end_date = end_datetime.strftime(
                "%d/%m/%Y"
            )

            print(
                "Today's date:",
                datetime.now().strftime("%d/%m/%Y")
            )

            print(
                "End date will be:",
                end_date
            )

            # =================================================
            # END DATE
            # =================================================

            print(
                "Looking for End Date input..."
            )

            end_date_input = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.END_DATE_INPUT
                )
            )

            print(
                "✅ End Date input found"
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                end_date_input
            )

            slow_down()

            # Re-find element because Angular
            # can re-render the field
            end_date_input = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.END_DATE_INPUT
                )
            )

            # =================================================
            # CLEAR EXISTING END DATE
            # =================================================

            try:

                end_date_input.click()

                end_date_input.clear()

            except Exception:

                self.driver.execute_script(
                    """
                    arguments[0].value = '';

                    arguments[0].dispatchEvent(
                        new Event('input', {bubbles:true})
                    );
                    """,
                    end_date_input
                )

            slow_down()

            # =================================================
            # ENTER END DATE
            # =================================================

            end_date_input.send_keys(
                end_date
            )

            # =================================================
            # TRIGGER ANGULAR CHANGE DETECTION
            # =================================================

            self.driver.execute_script(
                """
                arguments[0].dispatchEvent(
                    new Event('input', {bubbles:true})
                );

                arguments[0].dispatchEvent(
                    new Event('change', {bubbles:true})
                );

                arguments[0].dispatchEvent(
                    new Event('blur', {bubbles:true})
                );
                """,
                end_date_input
            )

            slow_down()

            # =================================================
            # VERIFY END DATE
            # =================================================

            current_end_date = (
                end_date_input.get_attribute(
                    "value"
                )
            )

            print(
                "End Date entered:",
                current_end_date
            )

            if current_end_date != end_date:

                print(
                    "End Date value differs from expected. "
                    "Re-applying date..."
                )

                end_date_input = self.wait.until(
                    EC.element_to_be_clickable(
                        self.page.END_DATE_INPUT
                    )
                )

                self.driver.execute_script(
                    "arguments[0].value='';",
                    end_date_input
                )

                end_date_input.send_keys(
                    end_date
                )

                self.driver.execute_script(
                    """
                    arguments[0].dispatchEvent(
                        new Event('input', {bubbles:true})
                    );

                    arguments[0].dispatchEvent(
                        new Event('change', {bubbles:true})
                    );

                    arguments[0].dispatchEvent(
                        new Event('blur', {bubbles:true})
                    );
                    """,
                    end_date_input
                )

                slow_down()

            print(
                "✅ End Date set:",
                end_date
            )

            # =================================================
            # END TIME DROPDOWN
            # =================================================

            print(
                "Looking for End Time dropdown..."
            )

            end_time_dropdown = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.END_TIME_DROPDOWN
                )
            )

            print(
                "✅ End Time dropdown found"
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                end_time_dropdown
            )

            slow_down()

            # =================================================
            # GET VALID END TIME OPTIONS
            # =================================================

            end_time_select = Select(
                end_time_dropdown
            )

            valid_time_options = []

            for option in end_time_select.options:

                option_text = (
                    option.text.strip()
                )

                option_value = (
                    option.get_attribute(
                        "value"
                    ) or ""
                ).strip()

                # ---------------------------------------------
                # SKIP EMPTY OPTIONS
                # ---------------------------------------------

                if not option_text:
                    continue

                if not option_value:
                    continue

                # ---------------------------------------------
                # SKIP DEFAULT SELECT OPTION
                # ---------------------------------------------

                if option_text.lower() in (
                    "select time",
                    "please select",
                    "select",
                ):
                    continue

                # ---------------------------------------------
                # SKIP NULL OPTIONS
                # ---------------------------------------------

                if option_value.lower() in (
                    "null",
                    "0: null",
                    "",
                ):
                    continue

                valid_time_options.append(
                    option
                )

            # =================================================
            # VALIDATE END TIME OPTIONS
            # =================================================

            if not valid_time_options:

                raise Exception(
                    "No valid End Time options "
                    "were found in the dropdown."
                )

            print(
                "Valid End Time options found:",
                len(valid_time_options)
            )

            # =================================================
            # SELECT RANDOM VALID END TIME
            # =================================================

            selected_end_time = random.choice(
                valid_time_options
            )

            selected_end_time_value = (
                selected_end_time.get_attribute(
                    "value"
                )
            )

            selected_end_time_text = (
                selected_end_time.text.strip()
            )

            print(
                "Selecting End Time:",
                selected_end_time_text
            )

            print(
                "End Time value:",
                selected_end_time_value
            )

            # =================================================
            # SELECT END TIME
            # =================================================

            end_time_select.select_by_value(
                selected_end_time_value
            )

            slow_down()

            # =================================================
            # VERIFY END TIME
            # =================================================

            self.wait.until(
                lambda d:
                Select(
                    d.find_element(
                        *self.page.END_TIME_DROPDOWN
                    )
                ).first_selected_option.get_attribute(
                    "value"
                ) == selected_end_time_value
            )

            # Re-fetch after Angular change
            selected_end_time_after = Select(
                self.driver.find_element(
                    *self.page.END_TIME_DROPDOWN
                )
            ).first_selected_option

            print(
                "✅ End Time selected:",
                selected_end_time_after.text.strip()
            )

            # =================================================
            # TRIGGER CHANGE EVENT
            # =================================================

            end_time_element = self.driver.find_element(
                *self.page.END_TIME_DROPDOWN
            )

            self.driver.execute_script(
                """
                arguments[0].dispatchEvent(
                    new Event('change', {bubbles:true})
                );
                """,
                end_time_element
            )

            slow_down()

            # =================================================
            # FINAL UI WAIT
            # =================================================

            self._wait_ui_ready()

            print(
                "✅ End Date and End Time "
                "updated successfully"
            )

    # ---------------- ADD PRODUCT ----------------
    def add_product(self, product_data):

        product_name = product_data["product"]
        search_key = product_data["search_key"]
        quantity = product_data["quantity"]

        with allure.step(f"Add Product - {product_name}"):

            self._wait_ui_ready()

            # ---------------- PRODUCT INPUT ----------------
            product_input = self.wait.until(
                EC.element_to_be_clickable(self.page.PRODUCT_INPUT)
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                product_input
            )

            
            self.driver.execute_script("arguments[0].value='';", product_input)

            product_input.send_keys(search_key)
            slow_down()

            # ---------------- SELECT FIRST OPTION ----------------
            first_option = self.wait.until(
                EC.element_to_be_clickable(self.page.PRODUCT_OPTIONS)
            )

            try:
                first_option.click()
            except:
                self.driver.execute_script("arguments[0].click();", first_option)

            slow_down()
            self._wait_ui_ready()

            # ---------------- QUANTITY ----------------
            qty_input = self.wait.until(
                EC.element_to_be_clickable(self.page.QUANTITY_INPUT)
            )

            self.driver.execute_script("arguments[0].value='';", qty_input)
            qty_input.send_keys(str(quantity))

            slow_down()

            # ---------------- ADD BUTTON ----------------
            add_btn = self.wait.until(
                EC.element_to_be_clickable(self.page.ADD_BUTTON)
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                add_btn
            )

            try:
                add_btn.click()
            except:
                self.driver.execute_script("arguments[0].click();", add_btn)

            # wait for row refresh before next product
            self._wait_ui_ready()
            slow_down()

    # ---------------- LINK ORDER (OPTIONAL) ----------------
    def link_order_if_available(self):

        self._wait_ui_ready()

        try:
            dropdown_element = self.driver.find_element(*self.page.LINK_ORDER_DROPDOWN)

        except NoSuchElementException:
            return  # optional → safe skip

        try:
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                dropdown_element
            )

            slow_down()

            select = Select(dropdown_element)

            valid_options = [
                option for option in select.options
                if option.get_attribute("value")
                and option.text.strip()
                and "select" not in option.text.lower()
            ]

            if not valid_options:
                return

            select.select_by_visible_text(random.choice(valid_options).text)

            link_button = self.wait.until(
                EC.element_to_be_clickable(self.page.LINK_ORDER_BUTTON)
            )

            self.driver.execute_script("arguments[0].click();", link_button)

            try:
                yes_button = self.wait.until(
                    EC.element_to_be_clickable(self.page.LINK_ORDER_YES_BUTTON)
                )
                self.driver.execute_script("arguments[0].click();", yes_button)
            except TimeoutException:
                pass

            self._wait_ui_ready()

        except Exception as e:
            raise Exception(f"Link Order execution failed: {repr(e)}")

    # ---------------- ADD CONSUMABLE ----------------
    def add_random_consumable(self):

        self._wait_ui_ready()

        try:
            dropdown_element = self.wait.until(
                EC.presence_of_element_located(
                    self.page.CONSUMABLE_TYPE_DROPDOWN
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                dropdown_element
            )

            slow_down()

            select = Select(dropdown_element)

            valid_options = [
                option
                for option in select.options
                if option.get_attribute("value")
                and option.get_attribute("value") != "null"
                and option.text.strip()
                and "select" not in option.text.strip().lower()
            ]

            if not valid_options:
                print("No consumable options available. Skipping...")
                return

            chosen = random.choice(valid_options)
            select.select_by_visible_text(chosen.text)

            slow_down()

            qty_input = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.CONSUMABLE_QUANTITY_INPUT
                )
            )

            qty_input.clear()

            # Random quantity between 1 and 10
            qty_input.send_keys(str(random.randint(1, 10)))

            slow_down()

            add_button = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.CONSUMABLE_ADD_BUTTON
                )
            )

            self.driver.execute_script(
                "arguments[0].click();",
                add_button
            )

            slow_down()

            self._wait_ui_ready()

        except NoSuchElementException:
            return  # optional section missing

        except Exception as e:
            raise Exception(f"Consumable step failed: {str(e)}")

    # ---------------- ADD CUSTOM FEE ----------------
    def add_custom_fee(self):

        self._wait_ui_ready()

        with allure.step("Add Custom Fee"):

            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )

            slow_down()

            header = self.wait.until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//h5[normalize-space()='Custom Fees']"
                    )
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                header
            )

            description = self.wait.until(
                EC.visibility_of_element_located(
                    self.page.CUSTOM_FEE_DESCRIPTION
                )
            )

            description.clear()
            description.send_keys(
                f"Automation Fee {random.randint(1000,9999)}"
            )

            slow_down()

            quantity = self.wait.until(
                EC.visibility_of_element_located(
                    self.page.CUSTOM_FEE_QUANTITY
                )
            )

            quantity.clear()
            quantity.send_keys(str(random.randint(1, 5)))

            slow_down()

            base_price = self.wait.until(
                EC.visibility_of_element_located(
                    self.page.CUSTOM_FEE_BASE_PRICE
                )
            )

            base_price.clear()
            base_price.send_keys(str(random.randint(50, 500)))

            slow_down()

            add_btn = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.CUSTOM_FEE_ADD_BUTTON
                )
            )

            self.driver.execute_script(
                "arguments[0].click();",
                add_btn
            )

            self._wait_ui_ready()


    # ---------------- ADD NOTES ----------------
    def add_notes(self):

        self._wait_ui_ready()

        with allure.step("Add Notes"):

            notes_box = self.wait.until(
                EC.visibility_of_element_located(self.page.NOTES_TEXTAREA)
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                notes_box
            )

            slow_down()

            try:
                notes_box.clear()
            except Exception:
                self.driver.execute_script("arguments[0].value='';", notes_box)

            note_text = f"Requested Order Note - Automation Test {random.randint(1000,9999)}"

            notes_box.send_keys(note_text)

            self.driver.execute_script(
                """
                arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
                """,
                notes_box
            )

            self._wait_ui_ready()

    # ---------------- SAVE ORDER ----------------
    def click_save(self):

        self._wait_ui_ready()

        with allure.step("Save Order"):

            save_btn = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.SAVE_BUTTON
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                save_btn
            )

            slow_down()

            try:
                save_btn.click()
            except Exception:
                self.driver.execute_script(
                    "arguments[0].click();",
                    save_btn
                )

            self._wait_ui_ready()

    # ---------------- MARK AS QUOTED ----------------
    def click_mark_as_quoted(self):

        self._wait_ui_ready()

        with allure.step("Mark Order As Quoted"):

            mark_btn = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.MARK_AS_QUOTED_BUTTON
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                mark_btn
            )

            slow_down()

            try:
                mark_btn.click()
            except Exception:
                self.driver.execute_script(
                    "arguments[0].click();",
                    mark_btn
                )

            self._wait_ui_ready()

    # ---------------- UNLINK ORDER IF AVAILABLE ----------------
    def unlink_order_if_available(self):

        self._wait_ui_ready()

        with allure.step("Unlink Order If Available"):

            print(
                "Checking whether 'Unlink Order' button is available..."
            )

            # =================================================
            # CHECK IF UNLINK ORDER BUTTON EXISTS
            # =================================================

            try:

                unlink_button = self.driver.find_element(
                    *self.page.UNLINK_ORDER_BUTTON
                )

            except NoSuchElementException:

                print(
                    "ℹ️ 'Unlink Order' button is not available. "
                    "Skipping..."
                )

                return

            # =================================================
            # CHECK VISIBILITY
            # =================================================

            if not unlink_button.is_displayed():

                print(
                    "ℹ️ 'Unlink Order' button exists but is not visible. "
                    "Skipping..."
                )

                return

            print(
                "✅ 'Unlink Order' button is available."
            )

            # =================================================
            # SCROLL TO BUTTON
            # =================================================

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                unlink_button
            )

            slow_down()

            # =================================================
            # RE-FIND BUTTON
            # =================================================

            try:

                unlink_button = self.wait.until(
                    EC.element_to_be_clickable(
                        self.page.UNLINK_ORDER_BUTTON
                    )
                )

            except TimeoutException:

                print(
                    "ℹ️ 'Unlink Order' button is not clickable. "
                    "Skipping..."
                )

                return

            # =================================================
            # CLICK UNLINK ORDER
            # =================================================

            try:

                unlink_button.click()

                print(
                    "✅ 'Unlink Order' button clicked."
                )

            except Exception as e:

                print(
                    "Normal 'Unlink Order' click failed: "
                    f"{repr(e)}"
                )

                # Re-find because Angular may have re-rendered
                unlink_button = self.wait.until(
                    EC.presence_of_element_located(
                        self.page.UNLINK_ORDER_BUTTON
                    )
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    unlink_button
                )

                slow_down()

                self.driver.execute_script(
                    "arguments[0].click();",
                    unlink_button
                )

                print(
                    "✅ 'Unlink Order' button clicked "
                    "using JavaScript."
                )

            # ========================================================= # 
            # WAIT FOR UNLINK CONFIRMATION POPUP 
            #  =========================================================

            print(
                "Waiting for Unlink Order confirmation popup..."
            )

            try:
                yes_button = self.wait.until(
                    EC.element_to_be_clickable(
                        self.page.UNLINK_ORDER_YES_BUTTON
                    )
                )

                print(
                    "✅ Unlink Order confirmation popup appeared."
                )

            except TimeoutException:
                print(
                    "⚠️ Unlink confirmation popup did not appear."
                )

                return

            # ========================================================= 
            #  SCROLL TO YES BUTTON 
            # =========================================================

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                yes_button
            )

            slow_down()

            # ========================================================= 
            # CLICK YES 
            # =========================================================  

            try:
                yes_button.click()

                print(
                    "✅ 'Yes' button clicked."
                )

            except Exception as e:

                print(
                    "Normal 'Yes' button click failed: "
                    f"{repr(e)}"
                )

                # Re-find because Angular may have re-rendered
                yes_button = self.wait.until( 
                    EC.presence_of_element_located(  
                        self.page.UNLINK_ORDER_YES_BUTTON
                    )
                )

                self.driver.execute_script( 
                    "arguments[0].scrollIntoView({block:'center'});", yes_button 
                )

                slow_down() 

                self.driver.execute_script(
                    "arguments[0].click();",
                     yes_button 
                )

                print( 
                    "✅ 'Yes' button clicked using JavaScript." 
                )

                # ========================================================= 
                # WAIT FOR CONFIRMATION POPUP TO CLOSE 
                # ========================================================= 
                
                try:
                    self.wait.until(
                        EC.invisibility_of_element_located(
                            self.page.UNLINK_ORDER_YES_BUTTON
                        ) 
                    )

                except TimeoutException: 
                    print(
                        "⚠️ Confirmation popup did not close " 
                        "within the expected time." 
                    )   

            # =================================================
            # WAIT FOR UI UPDATE
            # =================================================

            slow_down()

            self._wait_ui_ready()

            print(
                "✅ Unlink Order process completed."
            )

    # ---------------- EDIT PRODUCT LINE ----------------
    def edit_order_line(self):

        import random

        self._wait_ui_ready()

        with allure.step("Edit PRODUCT Order Line"):

            # 1. Click Edit button
            edit_btn = self.wait.until(
                EC.element_to_be_clickable(self.page.PRODUCT_EDIT_BUTTON)
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                edit_btn
            )

            slow_down()

            try:
                edit_btn.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", edit_btn)

            # wait for edit container to fully render
            self.wait.until(
                EC.presence_of_element_located(self.page.PRODUCT_EDIT_CONTAINER)
            )

            slow_down()

            # 2. WAIT + RE-FETCH quantity input
            qty_input = self.wait.until(
                EC.element_to_be_clickable(self.page.PRODUCT_QUANTITY_INPUT)
            )

            self.wait.until(lambda d: qty_input.is_displayed())

            try:
                current_qty = int(qty_input.get_attribute("value") or 0)
            except:
                current_qty = 0

            new_qty = current_qty + random.randint(2, 3)

            # safer clear method (Angular fix)
            self.driver.execute_script("arguments[0].value='';", qty_input)
            qty_input.send_keys(str(new_qty))

            self.driver.execute_script(
                "arguments[0].dispatchEvent(new Event('input', {bubbles:true}));",
                qty_input
            )

            slow_down()

            # 3. PRICE FIELD (same fix)
            price_input = self.wait.until(
                EC.element_to_be_clickable(self.page.PRODUCT_BASE_PRICE_INPUT)
            )

            try:
                current_price = float(price_input.get_attribute("value") or 0)
            except:
                current_price = 0

            new_price = round(current_price * random.uniform(1.05, 1.10), 2)

            self.driver.execute_script("arguments[0].value='';", price_input)
            price_input.send_keys(str(new_price))

            self.driver.execute_script(
                "arguments[0].dispatchEvent(new Event('input', {bubbles:true}));",
                price_input
            )

            slow_down()

            # 4. SAVE BUTTON 
            save_btn = self.wait.until(
                EC.element_to_be_clickable(self.page.PRODUCT_SAVE_BUTTON)
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                save_btn
            )

            slow_down()

            try:
                save_btn.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", save_btn)

        self._wait_ui_ready()

    # ---------------- DELETE PRODUCT LINE ----------------
    def delete_one_product(self):

        self._wait_ui_ready()

        with allure.step("Delete ONE Product Line"):

            # ---------------- GET ALL DELETE BUTTONS ----------------
            delete_buttons = self.wait.until(
                EC.presence_of_all_elements_located(
                    self.page.PRODUCT_DELETE_BUTTONS
                )
            )
            if not delete_buttons:
                raise Exception("No delete buttons found")

            # ---------------- PICK ONLY ONE ----------------
            delete_btn = delete_buttons[0]

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                delete_btn
            )

            slow_down()

            try:
                delete_btn.click()
            except:
                self.driver.execute_script("arguments[0].click();", delete_btn)

            slow_down()

            # ---------------- CONFIRM POPUP ----------------
            yes_btn = self.wait.until(
                EC.element_to_be_clickable(self.page.DELETE_CONFIRM_YES_BUTTON)
            )

            try:
                yes_btn.click()
            except:
                self.driver.execute_script("arguments[0].click();", yes_btn)

            # wait for UI refresh after deletion
            self._wait_ui_ready()
            slow_down()

    # ---------------- EDIT CONSUMABLE ----------------
    def edit_consumable(self):

        self._wait_ui_ready()

        with allure.step("Edit Consumable & Charges"):

            # Scroll to Consumables section
            edit_btn = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.CONSUMABLE_EDIT_BUTTON
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                edit_btn
            )

            slow_down()

            try:
                edit_btn.click()
            except Exception:
                self.driver.execute_script(
                    "arguments[0].click();",
                    edit_btn
                )
            

            self._wait_ui_ready()

            # ---------------- TYPE DROPDOWN ----------------

            dropdown = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.CONSUMABLE_EDIT_TYPE
                )
            )

            select = Select(dropdown)

            current_value = select.first_selected_option.get_attribute("value")

            valid_options = [
                option
                for option in select.options
                if option.get_attribute("value")
                and option.get_attribute("value") != "null"
                and option.get_attribute("value") != current_value
                and option.text.strip()
                and "select" not in option.text.lower()
            ]

            if valid_options:
                selected = random.choice(valid_options)
                select.select_by_visible_text(selected.text)

            slow_down()

            # ---------------- QUANTITY ----------------

            qty = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.CONSUMABLE_EDIT_QUANTITY
                )
            )

            try:
                current_qty = int(qty.get_attribute("value"))
            except:
                current_qty = 1

            if random.choice([True, False]):
                new_qty = current_qty + random.randint(1, 3)
            else:
                new_qty = max(1, current_qty - random.randint(1, 2))

            self.driver.execute_script(
                "arguments[0].value='';",
                qty
            )

            qty.send_keys(str(new_qty))

            self.driver.execute_script("""
                arguments[0].dispatchEvent(new Event('input',{bubbles:true}));
                arguments[0].dispatchEvent(new Event('change',{bubbles:true}));
            """, qty)

            slow_down()

            # ---------------- PRICE ----------------

            price = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.CONSUMABLE_EDIT_BASE_PRICE
                )
            )

            try:
                current_price = float(price.get_attribute("value"))
            except:
                current_price = 5.00

            multiplier = random.uniform(0.90, 1.10)
            new_price = round(current_price * multiplier, 2)

            if new_price < 0.01:
                new_price = 0.01

            self.driver.execute_script(
                "arguments[0].value='';",
                price
            )

            price.send_keys(str(new_price))

            self.driver.execute_script("""
                arguments[0].dispatchEvent(new Event('input',{bubbles:true}));
                arguments[0].dispatchEvent(new Event('change',{bubbles:true}));
            """, price)

            slow_down()

            # ---------------- SAVE ----------------

            save_btn = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.CONSUMABLE_SAVE_BUTTON
                )
            )
        
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                save_btn
            )

            slow_down()

            try:
                save_btn.click()
            except Exception:
                self.driver.execute_script(
                    "arguments[0].click();",
                    save_btn
                )

            self._wait_ui_ready()

    # ---------------- CHANGE STATUS TO ACCEPTED ----------------
    def change_status_to_accepted(self):

        self._wait_ui_ready()

        with allure.step("Change Order Status To Accepted"):

            # Click current status (Quoted)
            status_btn = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.STATUS_DROPDOWN
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                status_btn
            )

            slow_down()

            try:
                status_btn.click()
            except Exception:
                self.driver.execute_script(
                    "arguments[0].click();",
                    status_btn
                )

            slow_down()

            # Click Accepted option
            accepted_btn = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.ACCEPTED_OPTION
                )
            )

            try:
                accepted_btn.click()
            except Exception:
                self.driver.execute_script(
                    "arguments[0].click();",
                    accepted_btn
                )

            slow_down()

            # Wait for confirmation popup
            yes_btn = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.ACCEPT_YES_BUTTON
                )
            )

            try:
                yes_btn.click()
            except Exception:
                self.driver.execute_script(
                    "arguments[0].click();",
                    yes_btn
                )

            self._wait_ui_ready()

    # ---------------- PAYMENT MODAL HANDLER ----------------
    def handle_payment_modal(self):

        self._wait_ui_ready()

        with allure.step("Handle Payment Dialog"):

            # Wait until dialog opens
            self.wait.until(
                EC.visibility_of_element_located(
                    self.page.PAYMENT_MODAL
                )
            )

            # ---------------- PAYMENT TYPE ----------------
            dropdown = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.PAYMENT_TYPE_DROPDOWN
                )
            )

            select = Select(dropdown)

            valid_options = []

            for option in select.options:

                text = option.text.strip().lower()

                if (
                    "select payment type" in text
                    or "creditcard" in text
                ):
                    continue

                valid_options.append(option)

            if not valid_options:
                raise Exception("No valid payment types found.")

            chosen = random.choice(valid_options)

            select.select_by_visible_text(chosen.text)

            slow_down()

            # ---------------- PAYMENT DATE ----------------
            payment_date = (
                datetime.now() +
                timedelta(days=random.randint(1, 2))
            ).strftime("%d/%m/%Y")

            date_input = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.PAYMENT_DATE_INPUT
                )
            )

            self.driver.execute_script(
                "arguments[0].value='';",
                date_input
            )

            date_input.send_keys(payment_date)

            self.driver.execute_script("""
                arguments[0].dispatchEvent(new Event('input',{bubbles:true}));
                arguments[0].dispatchEvent(new Event('change',{bubbles:true}));
            """, date_input)

            slow_down()

            # ---------------- AMOUNT ----------------
            amount_input = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.PAYMENT_AMOUNT_INPUT
                )
            )

            max_amount = amount_input.get_attribute("max")

            try:
                max_amount = float(max_amount)
            except:
                max_amount = 1000

            new_amount = round(
                random.uniform(
                    1,
                    max_amount
                ),
                2
            )

            self.driver.execute_script(
                "arguments[0].value='';",
                amount_input
            )

            amount_input.send_keys(str(new_amount))

            self.driver.execute_script("""
                arguments[0].dispatchEvent(new Event('input',{bubbles:true}));
                arguments[0].dispatchEvent(new Event('change',{bubbles:true}));
            """, amount_input)

            slow_down()

            # ---------------- REFERENCE ----------------
            ref_input = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.PAYMENT_REFERENCE_INPUT
                )
            )

            reference = f"AUTO-{random.randint(10000,99999)}"

            ref_input.clear()
            ref_input.send_keys(reference)

            self.driver.execute_script("""
                arguments[0].dispatchEvent(new Event('input',{bubbles:true}));
                arguments[0].dispatchEvent(new Event('change',{bubbles:true}));
            """, ref_input)

            slow_down()

            # ---------------- CREATE ----------------
            create_btn = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.PAYMENT_CREATE_BUTTON
                )
            )      

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                create_btn
            )

            slow_down()

            try:
                create_btn.click()
            except:
                self.driver.execute_script(
                    "arguments[0].click();",
                    create_btn
                )

            self._wait_ui_ready()

    # ---------------- OPEN PAYMENT DIALOG ----------------
    def click_record_payment_details(self):

        self._wait_ui_ready()

        with allure.step("Click Record Payment Details"):

            payment_btn = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.RECORD_PAYMENT_BUTTON
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                payment_btn
            )

            slow_down()

            try:
                payment_btn.click()
            except Exception:
                self.driver.execute_script(
                    "arguments[0].click();",
                    payment_btn
                )

            # Wait until the payment dialog appears
            self.wait.until(
                EC.visibility_of_element_located(
                    self.page.PAYMENT_MODAL
                )
            )

            self._wait_ui_ready()

    # ---------------- RECORD PAYMENT DETAILS ----------------
    def handle_record_payment_details(self):

        self._wait_ui_ready()

        with allure.step("Handle Record Payment Details"):

            # Wait until modal opens
            self.wait.until(
                EC.visibility_of_element_located(
                    self.page.RECORD_PAYMENT_MODAL
                )
            )

            # ---------------- STORE EXISTING AMOUNT ----------------
            original_amount = None

            try:
                amount_input = self.wait.until(
                    EC.presence_of_element_located(
                        (By.NAME, "paymentAmt")
                    )
                )

                original_amount = amount_input.get_attribute("value")

                print(
                    "Original Payment Amount:",
                    original_amount
                )

            except Exception:
                print(
                    "Amount field not available"
                )

            # ---------------- PAYMENT TYPE ----------------
            dropdown = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.RECORD_PAYMENT_TYPE_DROPDOWN
                )
            )

            select = Select(dropdown)

            valid_options = []

            # Allowed payment types only
            allowed_values = [
                "1: 0",   # Cash
                "3: 2",   # DirectDeposit
                "4: 3"    # Account
            ]

            for option in select.options:

                text = option.text.strip()
                value = (
                    option.get_attribute("value") or ""
                ).strip()

                if not text:
                    continue

                if not value:
                    continue

                if value in allowed_values:
                    valid_options.append(option)

            if not valid_options:
                raise Exception(
                    "No valid payment types found."
                )

            chosen = random.choice(valid_options)

            select.select_by_value(
                chosen.get_attribute("value")
            )

            print(
                "Selected Payment Type:",
                chosen.text.strip()
            )

            slow_down()

            # ---------------- RESTORE AMOUNT ----------------
            if original_amount is not None:

                amount_input = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.NAME, "paymentAmt")
                    )
                )

                self.driver.execute_script("""
                    const input = arguments[0];
                    const value = arguments[1];

                    input.focus();

                    input.value = value;

                    input.dispatchEvent(
                        new Event('input',{bubbles:true})
                    );

                    input.dispatchEvent(
                        new Event('change',{bubbles:true})
                    );

                    input.blur();

                """, amount_input, original_amount)

                updated_amount = amount_input.get_attribute(
                    "value"
                )

                print(
                    "Final Payment Amount:",
                    updated_amount
                )

                if updated_amount != original_amount:

                    raise Exception(
                        f"Payment amount changed! "
                        f"Expected {original_amount}, "
                        f"Found {updated_amount}"
                    )

            slow_down()

            # ---------------- CREATE ----------------
            create_btn = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.RECORD_PAYMENT_CREATE_BUTTON
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                create_btn
            )

            slow_down()

            try:

                create_btn.click()

            except Exception:

                self.driver.execute_script(
                    "arguments[0].click();",
                    create_btn
                )

            self._wait_ui_ready()

    # =========================================================
    # OPEN INVOICE RECORDS
    # =========================================================

    def open_invoice_records(self):

        self._wait_ui_ready()

        with allure.step("Open Invoice Records"):

            print(
                "Looking for Invoice Records section..."
            )

            invoice_records = self.wait.until(
                EC.visibility_of_element_located(
                    self.page.INVOICE_RECORDS_SECTION
                )
            )

            print(
                "✅ Invoice Records section found"
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                invoice_records
            )

            slow_down()

            try:

                invoice_records.click()

                print(
                    "✅ Invoice Records section clicked"
                )

            except Exception as e:

                print(
                    "Normal Invoice Records click failed: "
                    f"{repr(e)}"
                )

                invoice_records = self.wait.until(
                    EC.presence_of_element_located(
                        self.page.INVOICE_RECORDS_SECTION
                    )
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    invoice_records
                )

                slow_down()

                self.driver.execute_script(
                    "arguments[0].click();",
                    invoice_records
                )

                print(
                    "✅ Invoice Records section clicked "
                    "using JavaScript"
                )

            slow_down()

            self._wait_ui_ready()

            print(
                "✅ Invoice Records section opened successfully"
            )

        # =========================================================
    # CREATE INVOICE
    # =========================================================

    def click_create_invoice(self):

        self._wait_ui_ready()

        with allure.step("Click Create Invoice"):

            print(
                "Looking for Create Invoice button..."
            )

            create_invoice_button = self.wait.until(
                EC.visibility_of_element_located(
                    self.page.CREATE_INVOICE_BUTTON
                )
            )

            print(
                "✅ Create Invoice button found"
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                create_invoice_button
            )

            slow_down()

            try:

                create_invoice_button = self.wait.until(
                    EC.element_to_be_clickable(
                        self.page.CREATE_INVOICE_BUTTON
                    )
                )

                create_invoice_button.click()

                print(
                    "✅ Create Invoice button clicked"
                )

            except Exception as e:

                print(
                    "Normal Create Invoice button click failed: "
                    f"{repr(e)}"
                )

                create_invoice_button = self.wait.until(
                    EC.presence_of_element_located(
                        self.page.CREATE_INVOICE_BUTTON
                    )
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    create_invoice_button
                )

                slow_down()

                self.driver.execute_script(
                    "arguments[0].click();",
                    create_invoice_button
                )

                print(
                    "✅ Create Invoice button clicked "
                    "using JavaScript"
                )

            slow_down()

            self._wait_ui_ready()

            print(
                "✅ Create Invoice process started successfully"
            )

        # =========================================================
    # CREATE INVOICE - CONFIRM INVOICE MODAL
    # =========================================================

    def confirm_create_invoice(self):

        self._wait_ui_ready()

        with allure.step("Confirm Create Invoice"):

            print(
                "Waiting for Invoice modal..."
            )

            self.wait.until(
                EC.visibility_of_element_located(
                    self.page.INVOICE_MODAL
                )
            )

            print(
                "✅ Invoice modal opened"
            )

            slow_down()

            print(
                "Looking for Create button inside Invoice modal..."
            )

            create_button = self.wait.until(
                EC.visibility_of_element_located(
                    self.page.INVOICE_CREATE_BUTTON
                )
            )

            print(
                "✅ Invoice modal Create button found"
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                create_button
            )

            slow_down()

            try:

                create_button = self.wait.until(
                    EC.element_to_be_clickable(
                        self.page.INVOICE_CREATE_BUTTON
                    )
                )

                create_button.click()

                print(
                    "✅ Invoice modal Create button clicked"
                )

            except Exception as e:

                print(
                    "Normal Invoice modal Create button "
                    f"click failed: {repr(e)}"
                )

                create_button = self.wait.until(
                    EC.presence_of_element_located(
                        self.page.INVOICE_CREATE_BUTTON
                    )
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    create_button
                )

                slow_down()

                self.driver.execute_script(
                    "arguments[0].click();",
                    create_button
                )

                print(
                    "✅ Invoice modal Create button clicked "
                    "using JavaScript"
                )

            slow_down()

            print(
                "Waiting for Invoice modal to close..."
            )

            self.wait.until(
                EC.invisibility_of_element_located(
                    self.page.INVOICE_MODAL
                )
            )

            self._wait_ui_ready()

            print(
                "✅ Invoice created successfully"
            )

        # =========================================================
    # CHANGE STATUS TO ON-HIRE
    # =========================================================

    def change_status_to_on_hire(self):

        self._wait_ui_ready()

        with allure.step("Change Order Status To On-Hire"):

            print(
                "Looking for Accepted status dropdown..."
            )

            status_dropdown = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.ON_HIRE_STATUS_DROPDOWN
                )
            )

            print(
                "✅ Accepted status dropdown found"
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                status_dropdown
            )

            slow_down()

            try:

                status_dropdown.click()

                print(
                    "✅ Accepted status dropdown clicked"
                )

            except Exception as e:

                print(
                    "Normal Accepted status dropdown "
                    f"click failed: {repr(e)}"
                )

                status_dropdown = self.wait.until(
                    EC.presence_of_element_located(
                        self.page.ON_HIRE_STATUS_DROPDOWN
                    )
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    status_dropdown
                )

                slow_down()

                self.driver.execute_script(
                    "arguments[0].click();",
                    status_dropdown
                )

                print(
                    "✅ Accepted status dropdown clicked "
                    "using JavaScript"
                )

            slow_down()

            print(
                "Looking for On-Hire status option..."
            )

            on_hire_option = self.wait.until(
                EC.visibility_of_element_located(
                    self.page.ON_HIRE_OPTION
                )
            )

            print(
                "✅ On-Hire status option found"
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                on_hire_option
            )

            slow_down()

            try:

                on_hire_option = self.wait.until(
                    EC.element_to_be_clickable(
                        self.page.ON_HIRE_OPTION
                    )
                )

                on_hire_option.click()

                print(
                    "✅ On-Hire status selected"
                )

            except Exception as e:

                print(
                    "Normal On-Hire option click failed: "
                    f"{repr(e)}"
                )

                on_hire_option = self.wait.until(
                    EC.presence_of_element_located(
                        self.page.ON_HIRE_OPTION
                    )
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    on_hire_option
                )

                slow_down()

                self.driver.execute_script(
                    "arguments[0].click();",
                    on_hire_option
                )

                print(
                    "✅ On-Hire status selected "
                    "using JavaScript"
                )

            slow_down()

            self._wait_ui_ready()

            print(
                "✅ Order status changed to On-Hire successfully"
            )

        # =========================================================
    # OPEN ATTACHMENTS
    # =========================================================

    def open_attachments(self):

        self._wait_ui_ready()

        with allure.step("Open Attachments"):

            print(
                "Looking for Attachments section..."
            )

            attachments_section = self.wait.until(
                EC.visibility_of_element_located(
                    self.page.ATTACHMENTS_SECTION
                )
            )

            print(
                "✅ Attachments section found"
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                attachments_section
            )

            slow_down()

            try:

                attachments_section = self.wait.until(
                    EC.element_to_be_clickable(
                        self.page.ATTACHMENTS_SECTION
                    )
                )

                attachments_section.click()

                print(
                    "✅ Attachments section clicked"
                )

            except Exception as e:

                print(
                    "Normal Attachments section click failed: "
                    f"{repr(e)}"
                )

                attachments_section = self.wait.until(
                    EC.presence_of_element_located(
                        self.page.ATTACHMENTS_SECTION
                    )
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    attachments_section
                )

                slow_down()

                self.driver.execute_script(
                    "arguments[0].click();",
                    attachments_section
                )

                print(
                    "✅ Attachments section clicked "
                    "using JavaScript"
                )

            slow_down()

            self._wait_ui_ready()

            print(
                "✅ Attachments section opened successfully"
            )

        # =========================================================
    # UPLOAD RANDOM ATTACHMENT
    # =========================================================

    def upload_random_attachment(self):

        self._wait_ui_ready()

        with allure.step("Upload Random Attachment"):

            print(
                "Looking for Upload Files button..."
            )

            upload_button = self.wait.until(
                EC.visibility_of_element_located(
                    self.page.UPLOAD_FILES_BUTTON
                )
            )

            print(
                "✅ Upload Files button found"
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                upload_button
            )

            slow_down()

            print(
                "Looking for file input..."
            )

            file_input = self.wait.until(
                EC.presence_of_element_located(
                    self.page.ATTACHMENT_FILE_INPUT
                )
            )

            print(
                "✅ Attachment file input found"
            )

            # -------------------------------------------------
            # FIND PROJECT ROOT
            # -------------------------------------------------

            import os

            project_root = os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            )

            images_folder = os.path.join(
                project_root,
                "data",
                "images"
            )

            print(
                "Images folder:",
                images_folder
            )

            # -------------------------------------------------
            # VERIFY IMAGES FOLDER
            # -------------------------------------------------

            if not os.path.isdir(images_folder):

                raise Exception(
                    f"Images folder does not exist: "
                    f"{images_folder}"
                )

            # -------------------------------------------------
            # GET IMAGE FILES
            # -------------------------------------------------

            image_files = [
                os.path.join(
                    images_folder,
                    file
                )
                for file in os.listdir(images_folder)
                if file.lower().endswith(
                    (
                        ".png",
                        ".jpg",
                        ".jpeg",
                        ".gif",
                        ".webp"
                    )
                )
            ]

            if not image_files:

                raise Exception(
                    f"No image files found in: "
                    f"{images_folder}"
                )

            print(
                "Available attachment images:",
                len(image_files)
            )

            # -------------------------------------------------
            # SELECT RANDOM IMAGE
            # -------------------------------------------------

            attachment_path = random.choice(
                image_files
            )

            print(
                "Selected attachment:",
                attachment_path
            )

            # -------------------------------------------------
            # VERIFY FILE EXISTS
            # -------------------------------------------------

            if not os.path.isfile(attachment_path):

                raise Exception(
                    f"Selected attachment does not exist: "
                    f"{attachment_path}"
                )

            # -------------------------------------------------
            # UPLOAD FILE
            # -------------------------------------------------

            file_input.send_keys(
                attachment_path
            )

            print(
                "✅ File uploaded successfully"
            )

            slow_down()

            self._wait_ui_ready()

            print(
                "✅ Random attachment upload completed"
            )

    # =========================================================
    # OPEN DOCUMENTS
    # =========================================================

    def open_documents(self):

        self._wait_ui_ready()

        with allure.step("Open Documents"):

            print(
                "Looking for Documents section..."
            )

            documents_section = self.wait.until(
                EC.visibility_of_element_located(
                    self.page.DOCUMENTS_SECTION
                )
            )

            print(
                "✅ Documents section found"
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                documents_section
            )

            slow_down()

            try:

                documents_section.click()

                print(
                    "✅ Documents section clicked"
                )

            except Exception as e:

                print(
                    "Normal Documents section click failed: "
                    f"{repr(e)}"
                )

                documents_section = self.wait.until(
                    EC.presence_of_element_located(
                        self.page.DOCUMENTS_SECTION
                    )
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    documents_section
                )

                slow_down()

                self.driver.execute_script(
                    "arguments[0].click();",
                    documents_section
                )

                print(
                    "✅ Documents section clicked "
                    "using JavaScript"
                )

            # =================================================
            # WAIT FOR DOCUMENTS ACCORDION TO EXPAND
            # =================================================

            self.wait.until(
                lambda d: d.find_element(
                    By.XPATH,
                    "//div[contains(@class,'panel-title')]"
                    "//button[@accordion-heading]"
                    "[.//div[normalize-space()='Documents']]"
                    "/ancestor::div[contains(@class,'accordion-toggle')]"
                ).get_attribute("aria-expanded") == "true"
            )

            slow_down()

            self._wait_ui_ready()

            print(
                "✅ Documents section opened successfully"
            )

    # =========================================================
    # DOWNLOAD ORDER DETAILS
    # =========================================================

    def download_order_details(self):

        self._wait_ui_ready()

        with allure.step("Download Order Details"):

            print("Looking for Order Details download icon...")

            download_icon = self.wait.until(
                EC.visibility_of_element_located(
                    self.page.ORDER_DETAILS_DOWNLOAD
                )
            )

            print("✅ Order Details download icon found")

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                download_icon
            )

            slow_down()

            try:
                download_icon.click()

                print(
                    "✅ Order Details document downloaded"
                )

            except Exception as e:

                print(
                    "Normal Order Details download click failed: "
                    f"{repr(e)}"
                )

                download_icon = self.wait.until(
                    EC.presence_of_element_located(
                        self.page.ORDER_DETAILS_DOWNLOAD
                    )
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    download_icon
                )

                slow_down()

                self.driver.execute_script(
                    "arguments[0].click();",
                    download_icon
                )

                print(
                    "✅ Order Details document downloaded "
                    "using JavaScript"
                )

            slow_down()
            self._wait_ui_ready()

    # =========================================================
    # DOWNLOAD TERMS AND CONDITIONS
    # =========================================================

    def download_terms_and_conditions(self):

        self._wait_ui_ready()

        with allure.step(
            "Download Terms and Conditions"
        ):

            print(
                "Looking for Terms and Conditions "
                "download icon..."
            )

            download_icon = self.wait.until(
                EC.visibility_of_element_located(
                    self.page.TERMS_CONDITIONS_DOWNLOAD
                )
            )

            print(
                "✅ Terms and Conditions download icon found"
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                download_icon
            )

            slow_down()

            try:
                download_icon.click()

                print(
                    "✅ Terms and Conditions document downloaded"
                )

            except Exception as e:

                print(
                    "Normal Terms and Conditions download "
                    f"click failed: {repr(e)}"
                )

                download_icon = self.wait.until(
                    EC.presence_of_element_located(
                        self.page.TERMS_CONDITIONS_DOWNLOAD
                    )
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    download_icon
                )

                slow_down()

                self.driver.execute_script(
                    "arguments[0].click();",
                    download_icon
                )

                print(
                    "✅ Terms and Conditions document downloaded "
                    "using JavaScript"
                )

            slow_down()
            self._wait_ui_ready()

    # =========================================================
    # EMAIL DOCUMENTS
    # =========================================================

    def click_email_documents(self):

        self._wait_ui_ready()

        with allure.step("Click Email Documents"):

            print("Looking for Email Documents button...")

            email_button = self.wait.until(
                EC.visibility_of_element_located(
                    self.page.EMAIL_DOCUMENTS_BUTTON
                )
            )

            print("✅ Email Documents button found")

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                email_button
            )

            slow_down()

            try:

                email_button = self.wait.until(
                    EC.element_to_be_clickable(
                        self.page.EMAIL_DOCUMENTS_BUTTON
                    )
                )

                email_button.click()

                print(
                    "✅ Email Documents button clicked"
                )

            except Exception as e:

                print(
                    "Normal Email Documents button "
                    f"click failed: {repr(e)}"
                )

                email_button = self.wait.until(
                    EC.presence_of_element_located(
                        self.page.EMAIL_DOCUMENTS_BUTTON
                    )
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    email_button
                )

                slow_down()

                self.driver.execute_script(
                    "arguments[0].click();",
                    email_button
                )

                print(
                    "✅ Email Documents button clicked "
                    "using JavaScript"
                )

            slow_down()
            self._wait_ui_ready()

            print(
                "✅ Email Documents process started successfully"
            )

    # =========================================================
    # HANDLE EMAIL DOCUMENTS MODAL
    # =========================================================

    def handle_email_documents_modal(self):

        self._wait_ui_ready()

        with allure.step("Handle Email Documents Modal"):

            # =================================================
            # WAIT FOR EMAIL MODAL
            # =================================================

            print("Waiting for Email Documents modal...")

            self.wait.until(
                EC.visibility_of_element_located(
                    self.page.EMAIL_DOCUMENTS_MODAL
                )
            )

            print(
                "✅ Email Documents modal opened"
            )

            slow_down()

            # =================================================
            # SELECT RANDOM EMAIL TEMPLATE
            # =================================================

            print(
                "Looking for Email Documents template dropdown..."
            )

            template_dropdown = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.EMAIL_DOCUMENTS_TEMPLATE_DROPDOWN
                )
            )

            print(
                "✅ Template dropdown found"
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                template_dropdown
            )

            slow_down()

            template_select = Select(
                template_dropdown
            )

            # =================================================
            # GET VALID TEMPLATES
            # =================================================

            valid_templates = []

            for option in template_select.options:

                option_text = option.text.strip()

                option_value = (
                    option.get_attribute("value") or ""
                ).strip()

                # Skip empty options
                if not option_text:
                    continue

                # Skip "Select a template"
                if (
                    option_text.lower()
                    == "select a template"
                ):
                    continue

                # Skip null/default values
                if option_value.lower() in (
                    "",
                    "null",
                    "0: null"
                ):
                    continue

                valid_templates.append(option)

            if not valid_templates:

                raise Exception(
                    "No valid Email Document templates "
                    "were found."
                )

            print(
                "Valid email templates found:",
                len(valid_templates)
            )

            # =================================================
            # SELECT RANDOM TEMPLATE
            # =================================================

            selected_template = random.choice(
                valid_templates
            )

            selected_template_text = (
                selected_template.text.strip()
            )

            selected_template_value = (
                selected_template.get_attribute("value")
            )

            print(
                "Selecting Email Document template:",
                selected_template_text
            )

            print(
                "Template value:",
                selected_template_value
            )

            template_select.select_by_value(
                selected_template_value
            )

            slow_down()

            # =================================================
            # VERIFY TEMPLATE WAS SELECTED
            # =================================================

            self.wait.until(
                lambda d:
                Select(
                    d.find_element(
                        *self.page.EMAIL_DOCUMENTS_TEMPLATE_DROPDOWN
                    )
                ).first_selected_option.get_attribute(
                    "value"
                ) == selected_template_value
            )

            selected_template_after = Select(
                self.driver.find_element(
                    *self.page.EMAIL_DOCUMENTS_TEMPLATE_DROPDOWN
                )
            ).first_selected_option

            print(
                "✅ Email template selected:",
                selected_template_after.text.strip()
            )

            slow_down()

            # =================================================
            # ADD ATTACHMENT
            # =================================================

            print(
                "Looking for Add Attachments file input..."
            )

            attachment_input = self.wait.until(
                EC.presence_of_element_located(
                    self.page.EMAIL_DOCUMENTS_ATTACHMENT_INPUT
                )
            )

            print(
                "✅ Attachment input found"
            )

            # =================================================
            # FIND PROJECT ROOT
            # =================================================

            import os

            project_root = os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            )

            images_folder = os.path.join(
                project_root,
                "data",
                "images"
            )

            print(
                "Images folder:",
                images_folder
            )

            # =================================================
            # VERIFY IMAGES FOLDER
            # =================================================

            if not os.path.isdir(images_folder):

                raise Exception(
                    f"Images folder does not exist: "
                    f"{images_folder}"
                )

            # =================================================
            # GET AVAILABLE FILES
            # =================================================

            attachment_files = [
                os.path.join(
                    images_folder,
                    file
                )
                for file in os.listdir(images_folder)
                if file.lower().endswith(
                    (
                        ".png",
                        ".jpg",
                        ".jpeg",
                        ".gif",
                        ".webp",
                        ".pdf"
                    )
                )
            ]

            if not attachment_files:

                raise Exception(
                    f"No attachment files found in: "
                    f"{images_folder}"
                )

            print(
                "Available attachment files:",
                len(attachment_files)
            )

            # =================================================
            # SELECT RANDOM FILE
            # =================================================

            attachment_path = random.choice(
                attachment_files
            )

            print(
                "Selected attachment:",
                attachment_path
            )

            if not os.path.isfile(
                attachment_path
            ):

                raise Exception(
                    f"Selected attachment does not exist: "
                    f"{attachment_path}"
                )

            # =================================================
            # UPLOAD FILE
            # =================================================

            attachment_input.send_keys(
                attachment_path
            )

            print(
                "✅ Attachment added successfully"
            )

            slow_down()

            # =================================================
            # WAIT FOR SEND BUTTON
            # =================================================

            print(
                "Waiting for Send button to become enabled..."
            )

            def send_button_ready(driver):

                try:

                    button = driver.find_element(
                        *self.page.EMAIL_DOCUMENTS_SEND_BUTTON
                    )

                    return (
                        button.is_displayed()
                        and button.is_enabled()
                    )

                except Exception:

                    return False

            self.wait.until(
                send_button_ready
            )

            print(
                "✅ Send button is visible and enabled"
            )

            # =================================================
            # CLICK SEND
            # =================================================

            send_button = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.EMAIL_DOCUMENTS_SEND_BUTTON
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                send_button
            )

            slow_down()

            try:

                send_button.click()

                print(
                    "✅ Send button clicked"
                )

            except Exception as e:

                print(
                    "Normal Send button click failed: "
                    f"{repr(e)}"
                )

                send_button = self.wait.until(
                    EC.presence_of_element_located(
                        self.page.EMAIL_DOCUMENTS_SEND_BUTTON
                    )
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    send_button
                )

                slow_down()

                self.driver.execute_script(
                    "arguments[0].click();",
                    send_button
                )

                print(
                    "✅ Send button clicked using JavaScript"
                )

            # =================================================
            # WAIT FOR MODAL TO CLOSE
            # =================================================

            print(
                "Waiting for Email Documents modal to close..."
            )

            self.wait.until(
                EC.invisibility_of_element_located(
                    self.page.EMAIL_DOCUMENTS_MODAL
                )
            )

            self._wait_ui_ready()

            print(
                "✅ Documents emailed successfully"
            )

    # =========================================================
    # OPEN EMAILS
    # =========================================================

    def open_emails(self):

        self._wait_ui_ready()

        with allure.step("Open Emails"):

            print("Looking for Emails section...")

            emails_section = self.wait.until(
                EC.visibility_of_element_located(
                    self.page.EMAILS_SECTION
                )
            )

            print("✅ Emails section found")

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                emails_section
            )

            slow_down()

            try:
                emails_section = self.wait.until(
                    EC.element_to_be_clickable(
                        self.page.EMAILS_SECTION
                    )
                )

                emails_section.click()

                print("✅ Emails section clicked")

            except Exception as e:

                print(
                    "Normal Emails section click failed: "
                    f"{repr(e)}"
                )

                emails_section = self.wait.until(
                    EC.presence_of_element_located(
                        self.page.EMAILS_SECTION
                    )
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    emails_section
                )

                slow_down()

                self.driver.execute_script(
                    "arguments[0].click();",
                    emails_section
                )

                print(
                    "✅ Emails section clicked "
                    "using JavaScript"
                )

            # =================================================
            # WAIT FOR ACCORDION TO EXPAND
            # =================================================

            self.wait.until(
                lambda d: d.find_element(
                    By.XPATH,
                    "//div[contains(@class,'panel-title')]"
                    "//button[@accordion-heading]"
                    "[.//div[normalize-space()='Emails']]"
                    "/ancestor::div[contains(@class,'accordion-toggle')]"
                ).get_attribute("aria-expanded") == "true"
            )

            slow_down()

            self._wait_ui_ready()

            print(
                "✅ Emails section opened successfully"
            )

    # =========================================================
    # CLICK NEW EMAIL
    # =========================================================

    def click_new_email(self):

        self._wait_ui_ready()

        with allure.step("Click New Email"):

            print("Looking for New Email button...")

            new_email_button = self.wait.until(
                EC.visibility_of_element_located(
                    self.page.NEW_EMAIL_BUTTON
                )
            )

            print("✅ New Email button found")

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                new_email_button
            )

            slow_down()

            try:

                new_email_button = self.wait.until(
                    EC.element_to_be_clickable(
                        self.page.NEW_EMAIL_BUTTON
                    )
                )

                new_email_button.click()

                print("✅ New Email button clicked")

            except Exception as e:

                print(
                    "Normal New Email button click failed: "
                    f"{repr(e)}"
                )

                new_email_button = self.wait.until(
                    EC.presence_of_element_located(
                        self.page.NEW_EMAIL_BUTTON
                    )
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    new_email_button
                )

                slow_down()

                self.driver.execute_script(
                    "arguments[0].click();",
                    new_email_button
                )

                print(
                    "✅ New Email button clicked "
                    "using JavaScript"
                )

            # =================================================
            # WAIT FOR EMAIL MODAL
            # =================================================

            self.wait.until(
                EC.visibility_of_element_located(
                    self.page.NEW_EMAIL_MODAL
                )
            )

            slow_down()

            print("✅ New Email modal opened")

    # =========================================================
    # FILL NEW EMAIL FORM
    # =========================================================

    def fill_new_email_form(self):

        self._wait_ui_ready()

        with allure.step("Fill New Email Form"):

            # =================================================
            # SELECT RANDOM TEMPLATE
            # =================================================

            print(
                "Looking for New Email template dropdown..."
            )

            template_dropdown = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.NEW_EMAIL_TEMPLATE_DROPDOWN
                )
            )

            print("✅ Template dropdown found")

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                template_dropdown
            )

            slow_down()

            template_select = Select(
                template_dropdown
            )

            # =================================================
            # FIND VALID TEMPLATES
            # =================================================

            valid_templates = []

            for option in template_select.options:

                option_text = option.text.strip()

                option_value = (
                    option.get_attribute("value") or ""
                ).strip()

                if not option_text:
                    continue

                # Do not select "Select a template"
                if option_text.lower() == "select a template":
                    continue

                # Do not select null/default values
                if option_value.lower() in (
                    "",
                    "null",
                    "0: null"
                ):
                    continue

                valid_templates.append(option)

            if not valid_templates:

                raise Exception(
                    "No valid email templates were found."
                )

            print(
                "Valid email templates found:",
                len(valid_templates)
            )

            # =================================================
            # SELECT RANDOM TEMPLATE
            # =================================================

            selected_template = random.choice(
                valid_templates
            )

            selected_template_text = (
                selected_template.text.strip()
            )

            selected_template_value = (
                selected_template.get_attribute("value")
            )

            print(
                "Selecting email template:",
                selected_template_text
            )

            print(
                "Template value:",
                selected_template_value
            )

            template_select.select_by_value(
                selected_template_value
            )

            slow_down()

            # =================================================
            # VERIFY TEMPLATE SELECTION
            # =================================================

            self.wait.until(
                lambda d:
                Select(
                    d.find_element(
                        *self.page.NEW_EMAIL_TEMPLATE_DROPDOWN
                    )
                ).first_selected_option.get_attribute(
                    "value"
                ) == selected_template_value
            )

            selected_after = Select(
                self.driver.find_element(
                    *self.page.NEW_EMAIL_TEMPLATE_DROPDOWN
                )
            ).first_selected_option

            print(
                "✅ Email template selected:",
                selected_after.text.strip()
            )

            slow_down()

            # =================================================
            # UPLOAD RANDOM ATTACHMENT
            # =================================================

            print(
                "Looking for Add Attachments file input..."
            )

            attachment_input = self.wait.until(
                EC.presence_of_element_located(
                    self.page.NEW_EMAIL_ATTACHMENT_INPUT
                )
            )

            print("✅ Attachment input found")

            # =================================================
            # GET PROJECT ROOT
            # =================================================

            import os

            project_root = os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            )

            images_folder = os.path.join(
                project_root,
                "data",
                "images"
            )

            print(
                "Images folder:",
                images_folder
            )

            if not os.path.isdir(images_folder):

                raise Exception(
                    f"Images folder does not exist: "
                    f"{images_folder}"
                )

            # =================================================
            # FIND FILES
            # =================================================

            image_files = [
                os.path.join(
                    images_folder,
                    file
                )
                for file in os.listdir(images_folder)
                if file.lower().endswith(
                    (
                        ".png",
                        ".jpg",
                        ".jpeg",
                        ".gif",
                        ".webp"
                    )
                )
            ]

            if not image_files:

                raise Exception(
                    f"No image files found in: "
                    f"{images_folder}"
                )

            print(
                "Available attachment files:",
                len(image_files)
            )

            # =================================================
            # SELECT RANDOM FILE
            # =================================================

            attachment_path = random.choice(
                image_files
            )

            print(
                "Selected attachment:",
                attachment_path
            )

            if not os.path.isfile(
                attachment_path
            ):

                raise Exception(
                    f"Selected attachment does not exist: "
                    f"{attachment_path}"
                )

            # =================================================
            # UPLOAD FILE
            # =================================================

            attachment_input.send_keys(
                attachment_path
            )

            print(
                "✅ Attachment uploaded successfully"
            )

            slow_down()

            # =================================================
            # WAIT FOR SEND BUTTON
            # =================================================

            print(
                "Waiting for Send button to become enabled..."
            )

            def send_button_ready(driver):

                try:

                    button = driver.find_element(
                        *self.page.NEW_EMAIL_SEND_BUTTON
                    )

                    return (
                        button.is_displayed()
                        and button.is_enabled()
                    )

                except Exception:

                    return False

            self.wait.until(
                send_button_ready
            )

            print(
                "✅ Send button is visible and enabled"
            )

            # =================================================
            # CLICK SEND
            # =================================================

            send_button = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.NEW_EMAIL_SEND_BUTTON
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                send_button
            )

            slow_down()

            try:

                send_button.click()

                print(
                    "✅ Send button clicked"
                )

            except Exception as e:

                print(
                    "Normal Send button click failed: "
                    f"{repr(e)}"
                )

                send_button = self.wait.until(
                    EC.presence_of_element_located(
                        self.page.NEW_EMAIL_SEND_BUTTON
                    )
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    send_button
                )

                slow_down()

                self.driver.execute_script(
                    "arguments[0].click();",
                    send_button
                )

                print(
                    "✅ Send button clicked using JavaScript"
                )

            # =================================================
            # WAIT FOR MODAL TO CLOSE
            # =================================================

            print(
                "Waiting for New Email modal to close..."
            )

            self.wait.until(
                EC.invisibility_of_element_located(
                    self.page.NEW_EMAIL_MODAL
                )
            )

            self._wait_ui_ready()

            print(
                "✅ New Email sent successfully"
            )

    # ---------------- Task CREATION ----------------
    def click_new_task(self):
        with allure.step("Click New Task"):
            button = WebDriverWait(self.driver, 40).until(
                EC.element_to_be_clickable(OrderPage.NEW_TASK_BUTTON)
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                button
            )

            try:
                button.click()
            except Exception:
                self.driver.execute_script(
                    "arguments[0].click();",
                    button
                )

            WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located(OrderPage.TASK_MODAL)
            )

            slow_down()

    def fill_new_task_form(self):
        with allure.step("Fill New Task form"):

            # =========================================================
            # SELECT RANDOM TASK TYPE
            # =========================================================

            print("Looking for Task Type dropdown...")

            task_type = WebDriverWait(self.driver, 40).until(
                EC.visibility_of_element_located(
                    OrderPage.TASK_TYPE_DROPDOWN
                )
            )

            print("✅ Task Type dropdown found")

            task_type_select = Select(task_type)

            task_type_options = [
                option
                for option in task_type_select.options
                if option.get_attribute("value") not in (
                    "",
                    "null",
                    "0: null"
                )
                and option.text.strip()
                and option.text.strip().lower()
                != "select task type"
            ]

            if not task_type_options:
                raise Exception(
                    "No valid Task Type options found."
                )

            selected_task_type = random.choice(
                task_type_options
            )

            print(
                f"Selecting Task Type: "
                f"{selected_task_type.text.strip()}"
            )

            task_type_select.select_by_value(
                selected_task_type.get_attribute("value")
            )

            print(
                f"✅ Task Type selected: "
                f"{selected_task_type.text.strip()}"
            )

            # =========================================================
            # WAIT FOR SPINNER AFTER TASK TYPE SELECTION
            # =========================================================

            print("Waiting for Task form loading to complete...")

            try:
                WebDriverWait(self.driver, 30).until(
                    EC.invisibility_of_element_located(
                        OrderPage.TASK_SPINNER
                    )
                )
                print("✅ Task form loading completed")
            except Exception:
                print(
                    "⚠️ Task spinner did not disappear within "
                    "the expected time."
                )

            # =========================================================
            # SET DUE DATE (+2 OR +3 DAYS)
            # =========================================================

            days_to_add = random.choice([2, 3])

            due_date = datetime.now() + timedelta(
                days=days_to_add
            )

            due_date_value = due_date.strftime(
                "%d/%m/%Y"
            )

            print(
                f"Today's date: "
                f"{datetime.now().strftime('%d/%m/%Y')}"
            )

            print(
                f"Due date will be: "
                f"{due_date_value}"
            )

            print("Looking for Due Date input...")

            due_date_input = WebDriverWait(
                self.driver,
                40
            ).until(
                EC.visibility_of_element_located(
                    OrderPage.TASK_DUE_DATE_INPUT
                )
            )

            print("✅ Due Date input found")

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                due_date_input
            )

            # ---------------------------------------------------------
            # Wait until spinner is completely gone
            # ---------------------------------------------------------

            try:
                WebDriverWait(self.driver, 30).until(
                    EC.invisibility_of_element_located(
                        OrderPage.TASK_SPINNER
                    )
                )
                print("✅ Spinner disappeared")
            except Exception:
                print(
                    "⚠️ Spinner still detected before Due Date."
                )

            # ---------------------------------------------------------
            # Click Due Date
            # ---------------------------------------------------------

            try:
                WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable(
                        OrderPage.TASK_DUE_DATE_INPUT
                    )
                ).click()

                print("✅ Due Date input clicked")

            except Exception as e:

                print(
                    f"Normal Due Date click failed: "
                    f"{type(e).__name__}"
                )

                # Re-check spinner before JS fallback
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.invisibility_of_element_located(
                            OrderPage.TASK_SPINNER
                        )
                    )
                except Exception:
                    pass

                self.driver.execute_script(
                    "arguments[0].click();",
                    due_date_input
                )

                print(
                    "✅ Due Date input clicked using JavaScript"
                )

            # ---------------------------------------------------------
            # Enter Due Date
            # ---------------------------------------------------------

            due_date_input = WebDriverWait(
                self.driver,
                20
            ).until(
                EC.visibility_of_element_located(
                    OrderPage.TASK_DUE_DATE_INPUT
                )
            )

            due_date_input.clear()
            due_date_input.send_keys(
                due_date_value
            )

            # Trigger Angular events
            self.driver.execute_script(
                """
                arguments[0].dispatchEvent(
                    new Event('input', { bubbles: true })
                );

                arguments[0].dispatchEvent(
                    new Event('change', { bubbles: true })
                );

                arguments[0].blur();
                """,
                due_date_input
            )

            print(
                f"✅ Due Date entered: "
                f"{due_date_value}"
            )

            allure.attach(
                due_date_value,
                name="Selected Due Date",
                attachment_type=allure.attachment_type.TEXT
            )

            # =========================================================
            # SELECT RANDOM RESPONSIBLE USER
            # =========================================================

            # Wait in case changing the date triggers loading
            try:
                WebDriverWait(self.driver, 30).until(
                    EC.invisibility_of_element_located(
                        OrderPage.TASK_SPINNER
                    )
                )
            except Exception:
                pass

            print("Looking for User dropdown...")

            user_dropdown = WebDriverWait(
                self.driver,
                40
            ).until(
                EC.visibility_of_element_located(
                    OrderPage.TASK_USER_DROPDOWN
                )
            )

            print("✅ User dropdown found")

            user_select = Select(
                user_dropdown
            )

            user_options = [
                option
                for option in user_select.options
                if option.get_attribute("value") not in (
                    "",
                    "null",
                    "0: null"
                )
                and option.text.strip()
                and option.text.strip().lower()
                != "select responsible user"
            ]

            print(
                f"Valid responsible users found: "
                f"{len(user_options)}"
            )

            if not user_options:
                raise Exception(
                    "No valid responsible user options found."
                )

            selected_user = random.choice(
                user_options
            )

            print(
                f"Selecting responsible user: "
                f"{selected_user.text.strip()}"
            )

            user_select.select_by_value(
                selected_user.get_attribute("value")
            )

            print(
                f"✅ Responsible user selected: "
                f"{selected_user.text.strip()}"
            )

            allure.attach(
                selected_user.text.strip(),
                name="Selected Responsible User",
                attachment_type=allure.attachment_type.TEXT
            )

            # =========================================================
            # WAIT FOR SPINNER / FORM VALIDATION
            # =========================================================

            try:
                WebDriverWait(self.driver, 30).until(
                    EC.invisibility_of_element_located(
                        OrderPage.TASK_SPINNER
                    )
                )
            except Exception:
                pass

            # =========================================================
            # SAVE
            # =========================================================

            print("Looking for Save button...")

            save_button = WebDriverWait(
                self.driver,
                40
            ).until(
                EC.presence_of_element_located(
                    OrderPage.TASK_SAVE_BUTTON
                )
            )

            print("✅ Save button found")

            WebDriverWait(
                self.driver,
                40
            ).until(
                lambda driver: save_button.is_enabled()
            )

            print("✅ Save button is enabled")

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                save_button
            )

            try:
                WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable(
                        OrderPage.TASK_SAVE_BUTTON
                    )
                ).click()

                print("✅ Save button clicked")

            except Exception as e:

                print(
                    f"Normal Save button click failed: "
                    f"{type(e).__name__}"
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    save_button
                )

                print(
                    "✅ Save button clicked using JavaScript"
                )

            # =========================================================
            # WAIT FOR MODAL TO CLOSE
            # =========================================================

            print(
                "Waiting for New Task modal to close..."
            )

            WebDriverWait(
                self.driver,
                40
            ).until(
                EC.invisibility_of_element_located(
                    OrderPage.TASK_MODAL
                )
            )

            print(
                "✅ New Task created successfully"
            )

            slow_down()

    # ---------------- STATUS CHANGE ----------------

    def change_status_to_returned(self):
        with allure.step("Change status from On-Hire to Returned"):

            print("Looking for On-Hire status dropdown...")

            status_dropdown = WebDriverWait(self.driver, 40).until(
                EC.element_to_be_clickable(
                    OrderPage.ON_HIRE_STATUS_DROPDOWN
                )
            )

            print("✅ On-Hire status dropdown found")

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                status_dropdown
            )

            try:
                status_dropdown.click()
                print("✅ Status dropdown clicked")
            except Exception as e:
                print(
                    f"Normal status dropdown click failed: "
                    f"{type(e).__name__}"
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    status_dropdown
                )

                print("✅ Status dropdown clicked using JavaScript")

            print("Waiting for page loading to complete...")

            WebDriverWait(self.driver, 40).until(
                EC.invisibility_of_element_located(
                    OrderPage.SPINNER
                )
            )

            print("✅ Page spinner disappeared")

            print("Looking for Returned status option...")

            returned_option = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located(
                    OrderPage.RETURNED_OPTION
                )
            )

            print("✅ Returned status option found")

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                returned_option
            )

            WebDriverWait(self.driver, 20).until(
                lambda d: (
                    returned_option.is_displayed()
                    and returned_option.is_enabled()
                )
            )

            try:
                returned_option.click()
                print("✅ Returned status selected")

            except Exception as e:
                print(
                    f"Normal Returned click failed: "
                    f"{type(e).__name__}"
                )

                WebDriverWait(self.driver, 20).until(
                    EC.invisibility_of_element_located(
                        OrderPage.SPINNER
                    )
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    returned_option
                )

                print("✅ Returned status selected using JavaScript")

            print("Waiting for order status to change to Returned...")

            WebDriverWait(self.driver, 40).until(
                EC.text_to_be_present_in_element(
                    OrderPage.ON_HIRE_STATUS_DROPDOWN,
                    "Returned"
                )
            )

            print("✅ Order status changed to Returned successfully")

            slow_down()


    def change_status_to_invoiced_completed(self):
        with allure.step(
            "Change status from Returned to Invoiced and Completed"
        ):

            print(
                "Looking for Returned status dropdown..."
            )

            status_dropdown = WebDriverWait(self.driver, 40).until(
                EC.element_to_be_clickable(
                    OrderPage.ON_HIRE_STATUS_DROPDOWN
                )
            )

            print("✅ Returned status dropdown found")

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                status_dropdown
            )

            try:
                status_dropdown.click()
                print("✅ Status dropdown clicked")
            except Exception as e:
                print(
                    f"Normal status dropdown click failed: "
                    f"{type(e).__name__}"
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    status_dropdown
                )

                print(
                    "✅ Status dropdown clicked using JavaScript"
                )

            print("Waiting for page loading to complete...")

            WebDriverWait(self.driver, 40).until(
                EC.invisibility_of_element_located(
                    OrderPage.SPINNER
                )
            )

            print("✅ Page spinner disappeared")

            print(
                "Looking for Invoiced and Completed status option..."
            )

            invoiced_option = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located(
                    OrderPage.INVOICED_COMPLETED_OPTION
                )
            )

            print(
                "✅ Invoiced and Completed status option found"
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                invoiced_option
            )

            WebDriverWait(self.driver, 20).until(
                lambda d: (
                    invoiced_option.is_displayed()
                    and invoiced_option.is_enabled()
                )
            )

            try:
                invoiced_option.click()
                print(
                    "✅ Invoiced and Completed status selected"
                )

            except Exception as e:
                print(
                    f"Normal Invoiced and Completed click failed: "
                    f"{type(e).__name__}"
                )

                WebDriverWait(self.driver, 20).until(
                    EC.invisibility_of_element_located(
                        OrderPage.SPINNER
                    )
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    invoiced_option
                )

                print(
                    "✅ Invoiced and Completed status "
                    "selected using JavaScript"
                )

            print(
                "Waiting for order status to change "
                "to Invoiced and Completed..."
            )

            WebDriverWait(self.driver, 40).until(
                EC.text_to_be_present_in_element(
                    OrderPage.ON_HIRE_STATUS_DROPDOWN,
                    "Invoiced and Completed"
                )
            )

            print(
                "✅ Order status changed to "
                "Invoiced and Completed successfully"
            )

            slow_down()


    def change_status_to_cancelled(self):
        with allure.step(
            "Change status from Invoiced and Completed to Cancelled"
        ):

            print(
                "Looking for Invoiced and Completed status dropdown..."
            )

            status_dropdown = WebDriverWait(self.driver, 40).until(
                EC.element_to_be_clickable(
                    OrderPage.ON_HIRE_STATUS_DROPDOWN
                )
            )

            print(
                "✅ Invoiced and Completed status dropdown found"
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                status_dropdown
            )

            try:
                status_dropdown.click()
                print("✅ Status dropdown clicked")
            except Exception as e:
                print(
                    f"Normal status dropdown click failed: "
                    f"{type(e).__name__}"
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    status_dropdown
                )

                print(
                    "✅ Status dropdown clicked using JavaScript"
                )

            print("Waiting for page loading to complete...")

            WebDriverWait(self.driver, 40).until(
                EC.invisibility_of_element_located(
                    OrderPage.SPINNER
                )
            )

            print("✅ Page spinner disappeared")

            print("Looking for Cancelled status option...")

            cancelled_option = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located(
                    OrderPage.CANCELLED_OPTION
                )
            )

            print("✅ Cancelled status option found")

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                cancelled_option
            )

            WebDriverWait(self.driver, 20).until(
                lambda d: (
                    cancelled_option.is_displayed()
                    and cancelled_option.is_enabled()
                )
            )

            try:
                cancelled_option.click()
                print("✅ Cancelled status selected")

            except Exception as e:
                print(
                    f"Normal Cancelled click failed: "
                    f"{type(e).__name__}"
                )

                WebDriverWait(self.driver, 20).until(
                    EC.invisibility_of_element_located(
                        OrderPage.SPINNER
                    )
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    cancelled_option
                )

                print(
                    "✅ Cancelled status selected using JavaScript"
                )

            print("Waiting for cancellation reason popup...")

            WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located(
                    OrderPage.CANCELLATION_MODAL
                )
            )

            print(
                "✅ Cancellation reason popup opened successfully"
            )

            slow_down()


    def fill_cancellation_reason_and_cancel(self):
        with allure.step(
            "Select random cancellation reason and cancel order"
        ):

            print(
                "Looking for Cancellation Reason dropdown..."
            )

            reason_dropdown = WebDriverWait(
                self.driver,
                40
            ).until(
                EC.visibility_of_element_located(
                    OrderPage.CANCELLATION_REASON_DROPDOWN
                )
            )

            print("✅ Cancellation Reason dropdown found")

            reason_select = Select(reason_dropdown)

            valid_reasons = [
                option
                for option in reason_select.options
                if option.get_attribute("value")
                not in ("", "null", "0: null")
                and option.text.strip()
                and option.text.strip().lower()
                != "select cancellation reason"
            ]

            if not valid_reasons:
                raise Exception(
                    "No valid cancellation reason options found."
                )

            print(
                f"Valid cancellation reasons found: "
                f"{len(valid_reasons)}"
            )

            selected_reason = random.choice(
                valid_reasons
            )

            print(
                f"Selecting cancellation reason: "
                f"{selected_reason.text.strip()}"
            )

            reason_select.select_by_value(
                selected_reason.get_attribute("value")
            )

            print(
                f"✅ Cancellation reason selected: "
                f"{selected_reason.text.strip()}"
            )

            allure.attach(
                selected_reason.text.strip(),
                name="Selected Cancellation Reason",
                attachment_type=allure.attachment_type.TEXT
            )

            print(
                "Looking for Save and cancel this order button..."
            )

            save_cancel_button = WebDriverWait(
                self.driver,
                40
            ).until(
                EC.element_to_be_clickable(
                    OrderPage.SAVE_CANCEL_ORDER_BUTTON
                )
            )

            print(
                "✅ Save and cancel this order button found"
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                save_cancel_button
            )

            WebDriverWait(self.driver, 20).until(
                lambda d: save_cancel_button.is_enabled()
            )

            print(
                "✅ Save and cancel this order button is enabled"
            )

            try:
                save_cancel_button.click()

                print(
                    "✅ Save and cancel this order button clicked"
                )

            except Exception as e:

                print(
                    f"Normal Save and cancel button click failed: "
                    f"{type(e).__name__}"
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    save_cancel_button
                )

                print(
                    "✅ Save and cancel button clicked using JavaScript"
                )

            # -----------------------------------------------------
            # DO NOT WAIT FOR THE MODAL TO BECOME INVISIBLE
            # Wait for the actual order status to become Cancelled.
            # -----------------------------------------------------

            print(
                "Waiting for order status to change to Cancelled..."
            )

            WebDriverWait(
                self.driver,
                60
            ).until(
                EC.text_to_be_present_in_element(
                    OrderPage.ON_HIRE_STATUS_DROPDOWN,
                    "Cancelled"
                )
            )

            print(
                "✅ Order status changed to Cancelled successfully"
            )

            # Wait for any page spinner to finish.
            print(
                "Waiting for page loading to complete..."
            )

            WebDriverWait(
                self.driver,
                40
            ).until(
                EC.invisibility_of_element_located(
                    OrderPage.SPINNER
                )
            )

            print(
                "✅ Page spinner disappeared"
            )

            slow_down()
            
    # ---------------- DELETE CANCELLED ORDER ----------------
    def delete_cancelled_order(self):
        with allure.step("Delete cancelled order"):

            print("Looking for Cancelled status dropdown...")

            status_dropdown = WebDriverWait(
                self.driver,
                40
            ).until(
                EC.element_to_be_clickable(
                    OrderPage.ON_HIRE_STATUS_DROPDOWN
                )
            )

            print("✅ Cancelled status dropdown found")

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                status_dropdown
            )

            try:
                status_dropdown.click()
                print("✅ Cancelled status dropdown clicked")

            except Exception as e:

                print(
                    f"Normal status dropdown click failed: "
                    f"{type(e).__name__}"
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    status_dropdown
                )

                print(
                    "✅ Cancelled status dropdown clicked "
                    "using JavaScript"
                )

            print("Waiting for page loading to complete...")

            WebDriverWait(
                self.driver,
                40
            ).until(
                EC.invisibility_of_element_located(
                    OrderPage.SPINNER
                )
            )

            print("✅ Page spinner disappeared")

            print("Looking for Delete option...")

            delete_option = WebDriverWait(
                self.driver,
                20
            ).until(
                EC.visibility_of_element_located(
                    OrderPage.DELETE_CANCELLED_ORDER_OPTION
                )
            )

            print("✅ Delete option found")

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                delete_option
            )

            WebDriverWait(
                self.driver,
                20
            ).until(
                lambda d: (
                    delete_option.is_displayed()
                    and delete_option.is_enabled()
                )
            )

            try:
                delete_option.click()
                print("✅ Delete option clicked")

            except Exception as e:

                print(
                    f"Normal Delete click failed: "
                    f"{type(e).__name__}"
                )

                WebDriverWait(
                    self.driver,
                    20
                ).until(
                    EC.invisibility_of_element_located(
                        OrderPage.SPINNER
                    )
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    delete_option
                )

                print(
                    "✅ Delete option clicked "
                    "using JavaScript"
                )

            print("Waiting for delete confirmation popup...")

            yes_button = WebDriverWait(
                self.driver,
                20
            ).until(
                EC.element_to_be_clickable(
                    OrderPage.DELETE_CONFIRM_YES_BUTTON
                )
            )

            print(
                "✅ Delete confirmation popup opened successfully"
            )

            print("Looking for Yes button...")

            print("✅ Yes button found")

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                yes_button
            )

            try:
                yes_button.click()
                print("✅ Yes button clicked")

            except Exception as e:

                print(
                    f"Normal Yes button click failed: "
                    f"{type(e).__name__}"
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    yes_button
                )

                print(
                    "✅ Yes button clicked "
                    "using JavaScript"
                )

            # -----------------------------------------------------
            # IMPORTANT:
            # Do NOT wait for DELETE_CONFIRMATION_MODAL to become
            # invisible. The application re-renders the modal/page
            # after deletion and that locator can remain present.
            # -----------------------------------------------------

            print(
                "Waiting for order deletion to complete..."
            )

            # First wait for any loading spinner to finish.
            try:

                WebDriverWait(
                    self.driver,
                    60
                ).until(
                    EC.invisibility_of_element_located(
                        OrderPage.SPINNER
                    )
                )

                print(
                    "✅ Page spinner disappeared"
                )

            except Exception:

                print(
                    "ℹ️ Spinner did not disappear within "
                    "the expected time."
                )

            # -----------------------------------------------------
            # Wait for the Delete option to disappear.
            # This confirms that the cancelled order page/status
            # is no longer available in the current UI.
            # -----------------------------------------------------

            print(
                "Verifying that the cancelled order was deleted..."
            )

            try:

                WebDriverWait(
                    self.driver,
                    30
                ).until(
                    EC.invisibility_of_element_located(
                        OrderPage.DELETE_CANCELLED_ORDER_OPTION
                    )
                )

                print(
                    "✅ Delete option disappeared"
                )

                print(
                    "✅ Cancelled order deleted successfully"
                )

            except Exception:

                # The application may redirect to another page
                # after deletion. Check the current URL.

                current_url = self.driver.current_url

                print(
                    f"ℹ️ Current URL after delete: "
                    f"{current_url}"
                )

                if "/supplier/orders" in current_url:
                    print(
                        "✅ Redirected to Orders page"
                    )

                    print(
                        "✅ Cancelled order deleted successfully"
                    )

                else:

                    raise Exception(
                        "Order deletion could not be verified. "
                        "The Yes button was clicked, but the "
                        "Delete option is still present and the "
                        "application did not redirect to the "
                        "Orders page."
                    )

            slow_down()
    
    # ---------------- CLOSE MODAL ----------------
    def close_modal(self):

        self._wait_ui_ready()

        try:
            btn = self.wait.until(
                EC.element_to_be_clickable(self.page.CLOSE_MODAL)
            )

            self.driver.execute_script(
                "arguments[0].click();",
                btn
            )

            slow_down()

        except:
            pass