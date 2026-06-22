import random
import time
import allure
import os

from selenium.webdriver.common.by import By   # ✅ required
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from pages.customer_page import CustomerPage
from utils.delay_helper import slow_down


class CustomerModule:

    def __init__(self, driver):

        self.driver = driver
        self.wait = WebDriverWait(driver, 60)
        self.page = CustomerPage()
        self.typing_speed = 0.3

    # ==================================================
    # RANDOM DATA
    # ==================================================

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
        streets = ["Main Road", "High Street", "Lake Road", "Station Road"]
        return f"No.{random.randint(1,200)}/A, {random.choice(streets)}"

    def random_suburb(self):
        return random.choice(["Colombo", "Kaduwela", "Malabe", "Nugegoda", "Dehiwala"])

    def random_postcode(self):
        return str(random.randint(10000, 99999))

    def random_payment_days(self):
        return str(random.randint(7, 60))
    
    def get_random_image_path(self):

        base_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "data",
            "images"
        )

        images = [
            os.path.join(base_dir, f)
            for f in os.listdir(base_dir)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        ]

        if not images:
            raise Exception("No images found in data/images folder")

        return random.choice(images)

    # ==================================================
    # COMMON METHODS
    # ==================================================

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

        time.sleep(1)

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

    # ==================================================
    # SELECT RANDOM STATE
    # ==================================================

    def select_random_state(self):

        dropdown = self.wait.until(
            EC.presence_of_element_located(self.page.STATE)
        )

        select = Select(dropdown)

        valid_options = [
            opt.get_attribute("value")
            for opt in select.options
            if opt.get_attribute("value") and "select" not in opt.text.lower()
        ]

        select.select_by_value(random.choice(valid_options))

    # ==================================================
    # SELECT RANDOM LIST
    # ==================================================

    def select_random_customer_list(self):

        dropdown = self.wait.until(
            EC.presence_of_element_located(self.page.CUSTOMER_LIST_DROPDOWN)
        )

        select = Select(dropdown)

        valid_options = [
            opt.get_attribute("value")
            for opt in select.options
            if opt.get_attribute("value") and "select" not in opt.text.lower()
        ]

        selected = random.choice(valid_options)

        select.select_by_value(selected)

        print(f"✅ Random list selected: {selected}")

    # ==================================================
    # CLICK ADDRESS EDIT BUTTON
    # ==================================================

    def click_address_edit(self):

        with allure.step("Click Address Edit Button"):

            edit_btn = self.wait.until(
                EC.element_to_be_clickable(self.page.ADDRESS_EDIT_BUTTON)
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                edit_btn
            )

            slow_down()

            self.driver.execute_script(
                "arguments[0].click();",
                edit_btn
            )

            print("✅ Address Edit button clicked")

    # ==================================================
    # UPDATE ADDRESS MODAL
    # ==================================================

    def update_address_modal(self):

        with allure.step("Update Address Modal"):

            self.wait.until(
                EC.visibility_of_element_located(self.page.ADDRESS_MODAL)
            )

            self.enter_text(self.page.ADDRESS_MODAL_SUBURB, self.random_suburb())
            self.enter_text(self.page.ADDRESS_MODAL_POSTCODE, self.random_postcode())

            self.click(self.page.ADDRESS_MODAL_SAVE_BUTTON)

            print("✅ Address modal updated and saved")

    # ==================================================
    # CREATE NEW ADDRESS
    # ==================================================

    def create_new_address(self):

        with allure.step("Click New Address Button"):
            self.click(self.page.NEW_ADDRESS_BUTTON)

        with allure.step("Wait New Address Modal"):
            self.wait.until(
                EC.visibility_of_element_located(self.page.ADDRESS_MODAL)
            )

        with allure.step("Fill New Address Form"):
            self.enter_text(self.page.NEW_ADDRESS_MODAL_ADDRESS1, self.random_address())
            self.enter_text(self.page.NEW_ADDRESS_MODAL_SUBURB, self.random_suburb())

            state_dropdown = self.wait.until(
                EC.presence_of_element_located(self.page.NEW_ADDRESS_MODAL_STATE)
            )

            Select(state_dropdown).select_by_index(random.randint(1, 5))

            self.enter_text(self.page.NEW_ADDRESS_MODAL_POSTCODE, self.random_postcode())

            country_dropdown = self.wait.until(
                EC.presence_of_element_located(self.page.NEW_ADDRESS_MODAL_COUNTRY)
            )

            country_select = Select(country_dropdown)

            valid_countries = [
                opt.get_attribute("value")
                for opt in country_select.options
                if opt.get_attribute("value")
            ]

            country_select.select_by_value(random.choice(valid_countries))

        with allure.step("Save New Address"):
            self.click(self.page.NEW_ADDRESS_MODAL_SAVE_BUTTON)

            print("✅ New address created successfully")

    # ==================================================
    # DELETE ADDRESS (FIXED - ONLY NEWLY ADDED ONE)
    # ==================================================

    def delete_address(self):

        with allure.step("Delete ONLY newly added address"):

            self.wait.until(EC.presence_of_element_located(self.page.ADDRESS_SECTION))

            delete_buttons = self.wait.until(
                EC.presence_of_all_elements_located(self.page.ADDRESS_DELETE_BUTTONS)
            )

            delete_btn = delete_buttons[-1]

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                delete_btn
            )

            slow_down()

            self.driver.execute_script("arguments[0].click();", delete_btn)

            print("✅ Newly added address delete clicked")

        with allure.step("Confirm Delete Popup (YES)"):

            yes_btn = self.wait.until(
                EC.element_to_be_clickable(self.page.ADDRESS_DELETE_CONFIRM_YES_BUTTON)
            )

            self.driver.execute_script("arguments[0].click();", yes_btn)

            print("✅ Address deletion confirmed (YES clicked)")

    # ==================================================
    # ADD PHONE NUMBER
    # ==================================================

    def add_phone_number(self):

        with allure.step("Select Phone Number Type"):

            dropdown = self.wait.until(
                EC.presence_of_element_located(self.page.PHONE_NUMBER_TYPE)
            )

            select = Select(dropdown)

            valid_options = [
                opt.get_attribute("value")
                for opt in select.options
                if opt.get_attribute("value")
            ]

            select.select_by_value(random.choice(valid_options))

        with allure.step("Enter Phone Number"):
            self.enter_text(self.page.PHONE_NUMBER_INPUT, self.random_phone())

        with allure.step("Click Add Phone Number Button"):
            self.click(self.page.PHONE_NUMBER_ADD_BUTTON)

            print("✅ Phone number added successfully")

    # ==================================================
    # EDIT PHONE NUMBER
    # ==================================================

    def edit_phone_number(self):

        with allure.step("Click Phone Number Edit Button"):
            self.click(self.page.PHONE_NUMBER_EDIT_BUTTON)

        with allure.step("Update Phone Number"):
            self.enter_text(self.page.PHONE_NUMBER_EDIT_INPUT, self.random_phone())

        with allure.step("Save Updated Phone Number"):
            self.click(self.page.PHONE_NUMBER_SAVE_BUTTON)

            print("✅ Phone number updated successfully")

    # ==================================================
    # DELETE PHONE NUMBER
    # ==================================================

    def delete_phone_number(self):

        with allure.step("Delete Phone Number"):

            # 1. Click delete button
            delete_btn = self.wait.until(
                EC.element_to_be_clickable(self.page.PHONE_NUMBER_DELETE_BUTTON)
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                delete_btn
            )

            self.driver.execute_script("arguments[0].click();", delete_btn)

            print("✅ Phone number delete clicked")

        with allure.step("Confirm Phone Delete Popup (YES)"):

            # 2. WAIT for popup
            yes_btn = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[contains(@class,'modal-content')]//button[normalize-space()='Yes']")
                )
            )

            self.driver.execute_script("arguments[0].click();", yes_btn)

            print("✅ Phone delete confirmed (YES clicked)")

        with allure.step("Wait popup closed"):

            self.wait.until(
                EC.invisibility_of_element_located(
                    (By.XPATH, "//div[contains(@class,'modal-content')]")
                )
            )

            print("✅ Phone delete modal closed")

    # ==================================================
    # CLICK NEW TASK BUTTON
    # ==================================================

    def click_new_task_button(self):

        with allure.step("Click New Task Button"):

            new_task_btn = self.wait.until(
                EC.element_to_be_clickable(self.page.NEW_TASK_BUTTON)
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                new_task_btn
            )

            slow_down()

            self.driver.execute_script("arguments[0].click();", new_task_btn)

            print("✅ New Task button clicked")

    # ==================================================
    # FILL NEW TASK FORM (FIXED USER DROPDOWN ISSUE)
    # ==================================================

    def fill_new_task_form(self):

        with allure.step("Fill New Task Form"):

            # ✅ FIX: wait stronger for modal + DOM render
            self.wait.until(
                EC.visibility_of_element_located(self.page.MODAL_CONTAINER)
            )

            time.sleep(2)  # 🔥 important for Angular render

            # ================= TASK TYPE =================
            type_dropdown = self.wait.until(
                EC.presence_of_element_located((By.NAME, "noteTypeId"))
            )

            type_select = Select(type_dropdown)

            valid_task_types = [
                opt.get_attribute("value")
                for opt in type_select.options
                if opt.get_attribute("value") and "select" not in opt.text.lower()
            ]

            type_select.select_by_value(random.choice(valid_task_types))

            print("✅ Task type selected")

            # ================= USER (FIXED) =================

            user_dropdown = self.wait.until(
                EC.presence_of_element_located((By.NAME, "user"))
            )

            self.wait.until(
                lambda d: len(Select(user_dropdown).options) > 1
            )

            user_select = Select(user_dropdown)

            valid_users = []

            for opt in user_select.options:

                value = opt.get_attribute("value")
                text = opt.text.strip().lower()

                if (
                    value
                    and value != "0: null"
                    and "select responcible user" not in text
                    and "select responsible user" not in text
                ):
                    valid_users.append(value)

            if not valid_users:
                raise Exception("No valid users found in dropdown")

            selected_user = random.choice(valid_users)

            user_select.select_by_value(selected_user)

            print(f"✅ Responsible user selected: {selected_user}")

    # ==================================================
    # CLICK NEW EMAIL BUTTON (FIXED)
    # ==================================================

    def click_new_email_button(self):

        with allure.step("Click New Email Button"):

            new_email_btn = self.wait.until(
                EC.presence_of_element_located(
                    self.page.NEW_EMAIL_BUTTON
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                new_email_btn
            )

            slow_down()

            # Same click style you use successfully elsewhere
            self.driver.execute_script(
                "arguments[0].click();",
                new_email_btn
            )

            slow_down()

            print("✅ New Email button clicked")

    def fill_new_email_form(self):

        with allure.step("Fill New Email Form"):

            self.wait.until(
                EC.visibility_of_element_located(self.page.MODAL_CONTAINER)
            )

            time.sleep(1)

            template_dropdown = self.wait.until(
                EC.presence_of_element_located(
                    self.page.EMAIL_TEMPLATE_DROPDOWN
                )
            )

            select = Select(template_dropdown)

            # =========================
            # GET VALID OPTIONS
            # =========================
            options = select.options

            valid_options = []

            for opt in options:
                value = opt.get_attribute("value")
                text = opt.text.strip().lower()

                if value and "null" not in value and "select" not in text:
                    valid_options.append(opt)

            if not valid_options:
                raise Exception("No valid email templates found")

            chosen_option = random.choice(valid_options)

            value = chosen_option.get_attribute("value")

            # =========================
            # FORCE USER-LIKE ACTION
            # =========================

            select.select_by_value(value)

            # 🔥 IMPORTANT: trigger Angular change event manually
            self.driver.execute_script(
                "arguments[0].dispatchEvent(new Event('change'))",
                template_dropdown
            )

            time.sleep(1)

            print(f"✅ Email template selected: {value}")

    def upload_email_attachment(self):

        with allure.step("Upload Email Attachment"):

            # wait for modal stable
            self.wait.until(
                EC.visibility_of_element_located(self.page.MODAL_CONTAINER)
            )

            time.sleep(1)

            # click attach button (important for some UIs)
            try:
                attach_btn = self.wait.until(
                    EC.element_to_be_clickable(self.page.EMAIL_ADD_ATTACHMENT_BUTTON)
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    attach_btn
                )

                self.driver.execute_script("arguments[0].click();", attach_btn)

                print("📎 Add Attachment clicked")

            except Exception:
                print("⚠️ Attachment button not required")

            # file input
            file_input = self.wait.until(
                EC.presence_of_element_located(self.page.EMAIL_ATTACHMENT_INPUT)
            )

            file_path = self.get_random_image_path()

            # 🔥 CRITICAL FIX 1: ensure visible
            self.driver.execute_script(
                "arguments[0].style.display='block';",
                file_input
            )

            # send file
            file_input.send_keys(file_path)

            # 🔥 CRITICAL FIX 2: force Angular change detection
            self.driver.execute_script("""
                arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            """, file_input)

            # 🔥 CRITICAL FIX 3: wait UI update
            time.sleep(2)

            print(f"✅ File uploaded: {file_path}")
            print(file_input.get_attribute("value"))

    def click_send_email(self):

        with allure.step("Click Send Email Button"):

            send_btn = self.wait.until(
                EC.element_to_be_clickable(self.page.SEND_EMAIL_BUTTON)
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                send_btn
            )

            time.sleep(1)

            send_btn.click()

            print("Send clicked")

            # REAL CONFIRMATION (choose one)
            self.wait.until(
                EC.invisibility_of_element_located(self.page.MODAL_CONTAINER)
            )

            print("✅ EMAIL SEND CONFIRMED (modal closed)")

    # ==================================================
    # CLICK NEW ORDER BUTTON
    # ==================================================

    def click_new_order_button(self):

        with allure.step("Click New Order Button"):

            new_order_btn = self.wait.until(
                EC.element_to_be_clickable(self.page.NEW_ORDER_BUTTON)
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                new_order_btn
            )

            time.sleep(1)

            self.driver.execute_script("arguments[0].click();", new_order_btn)

            print("New Order clicked")

            # REAL VALIDATION
            self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//h3[normalize-space()='Orders']")
                )
            )

            print("✅ Orders section reached successfully")

    # ==================================================
    # MAIN FLOW
    # ==================================================

    def create_customer(self):

        with allure.step("Open Customer Form"):
            self.click(self.page.NEW_BUTTON)

        first, last = self.generate_name()

        with allure.step("Fill Customer Form"):
            self.enter_text(self.page.FIRST_NAME, first)
            self.enter_text(self.page.LAST_NAME, last)
            self.enter_text(self.page.EMAIL, self.random_email())
            self.enter_text(self.page.PHONE, self.random_phone())
            self.enter_text(self.page.ADDRESS, self.random_address())
            self.enter_text(self.page.SUBURB, self.random_suburb())
            self.enter_text(self.page.POSTCODE, self.random_postcode())

        with allure.step("Select State"):
            self.select_random_state()

        with allure.step("Create Customer"):
            old_url = self.driver.current_url

            self.click(self.page.CREATE_BUTTON)

            self.wait.until(lambda d: d.current_url != old_url)
            self.wait.until(EC.url_contains("/customers/"))
            self.wait.until(EC.presence_of_element_located(self.page.CUSTOMER_DETAILS_CONTAINER))

            print("✅ Customer details page loaded")

        with allure.step("Update First Name"):
            self.enter_text(self.page.FIRST_NAME, "UpdatedCustomer")

        with allure.step("Click Add To List"):
            self.click(self.page.ADD_TO_LIST_BUTTON)

        with allure.step("Wait Modal"):
            self.wait.until(EC.visibility_of_element_located(self.page.MODAL_CONTAINER))

        with allure.step("Select Random Customer List"):
            self.select_random_customer_list()

        with allure.step("Click Final Add Button"):
            self.click(self.page.MODAL_ADD_BUTTON)

        with allure.step("Wait After Modal Close"):
            self.wait.until(EC.invisibility_of_element_located(self.page.MODAL_CONTAINER))
            slow_down(2)

        with allure.step("Enable Account Customer"):
            checkbox = self.wait.until(
                EC.presence_of_element_located(self.page.ACCOUNT_CUSTOMER_CHECKBOX)
            )

            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", checkbox)

            if not checkbox.is_selected():
                self.driver.execute_script("arguments[0].click();", checkbox)

            print("✅ Account Customer enabled")

        with allure.step("Enter Payment Terms Days"):
            payment_input = self.wait.until(
                EC.visibility_of_element_located(self.page.PAYMENT_TERMS_DAYS)
            )

            payment_input.clear()
            payment_input.send_keys(self.random_payment_days())

        with allure.step("Click Save Button"):
            self.click(self.page.SAVE_BUTTON)

            slow_down(3)

        # ==================================================
        # ADDRESS FLOW
        # ==================================================

        self.click_address_edit()
        self.update_address_modal()
        self.create_new_address()
        self.delete_address()

        # ==================================================
        # PHONE FLOW
        # ==================================================

        self.add_phone_number()
        self.edit_phone_number()
        self.delete_phone_number()

        # ==================================================
        # TASK FLOW (UPDATED)
        # ==================================================

        self.click_new_task_button()
        self.fill_new_task_form()

        with allure.step("Click Task Save Button"):
            task_save_btn = self.wait.until(
                EC.element_to_be_clickable(self.page.TASK_SAVE_BUTTON)
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                task_save_btn
            )

            slow_down()

            self.driver.execute_script("arguments[0].click();", task_save_btn)

            print("✅ Task Save button clicked successfully")

        # wait after save
        self.wait.until(
            EC.invisibility_of_element_located(self.page.MODAL_CONTAINER)
        )

        slow_down(3)

        # ---------------- EMAIL FLOW (NEW ONLY) ----------------
        self.click_new_email_button()
        self.fill_new_email_form()
        self.upload_email_attachment()
        self.click_send_email()

        # ---------------- ORDER FLOW (NEW) ----------------
        self.click_new_order_button()
        