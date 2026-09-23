import random
import allure

from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from pages.company_details_page import CompanyDetailsPage
from utils.delay_helper import slow_down


class CompanyDetailsModule:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 40)
        self.page = CompanyDetailsPage()

    # ======================================================
    # COMMON CLICK
    # ======================================================
    def click(self, locator):

        element = self.wait.until(
            EC.presence_of_element_located(locator)
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

    # ======================================================
    # OPEN COMPANY DETAILS
    # ======================================================
    def open_company_details(self):

        with allure.step("Click Company Details from Sidebar"):

            self.click(
                self.page.COMPANY_DETAILS_SIDEBAR
            )

        with allure.step("Verify Company Details Page is Opened"):

            self.wait.until(
                EC.url_contains("/supplier/details")
            )

            self.wait.until(
                EC.presence_of_element_located(
                    self.page.ABN_INPUT
                )
            )

        print(
            "✅ Company Details page opened successfully"
        )

    # ======================================================
    # GET VISIBLE ABN FIELD
    # ======================================================
    def _get_visible_abn_field(self):

        def find_visible_abn(driver):

            elements = driver.find_elements(
                *self.page.ABN_INPUT
            )

            for element in elements:

                if element.is_displayed() and element.is_enabled():
                    return element

            return False

        return self.wait.until(
            find_visible_abn
        )

    # ======================================================
    # CHANGE ABN
    # ======================================================
    def change_abn(self):

        with allure.step("Change ABN to New Number"):

            abn_field = self._get_visible_abn_field()

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                abn_field
            )

            slow_down()

            # Generate a new 11-digit ABN
            new_abn = str(
                random.randint(
                    10000000000,
                    99999999999
                )
            )

            # Clear existing ABN
            abn_field.clear()

            slow_down()

            # Enter new ABN
            abn_field.send_keys(new_abn)

            slow_down()

            print(
                f"✅ ABN changed to: {new_abn}"
            )

    # ======================================================
    # TOGGLE REGISTERED FOR GST
    # ======================================================
    def toggle_registered_for_gst(self):

        with allure.step(
            "Toggle Registered for GST"
        ):

            gst_dropdown = self.wait.until(
                EC.visibility_of_element_located(
                    self.page.REGISTERED_FOR_GST_SELECT
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                gst_dropdown
            )

            slow_down()

            select = Select(
                gst_dropdown
            )

            current_option = select.first_selected_option

            current_value = current_option.get_attribute(
                "value"
            )

            current_text = current_option.text.strip()

            # YES -> NO
            # NO -> YES
            if current_value == "Yes":

                new_value = "No"

            elif current_value == "No":

                new_value = "Yes"

            else:

                raise Exception(
                    "Unexpected Registered for GST value: "
                    f"'{current_value}'"
                )

            select.select_by_value(
                new_value
            )

            slow_down()

            print(
                f"✅ Registered for GST changed "
                f"from '{current_text}' to '{new_value}'"
            )

    # ======================================================
    # SELECT BUSINESS TYPE
    # ======================================================
    def select_business_type(self):

        with allure.step(
            "Select Business Type"
        ):

            business_type_dropdown = self.wait.until(
                EC.visibility_of_element_located(
                    self.page.BUSINESS_TYPE_SELECT
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                business_type_dropdown
            )

            slow_down()

            select = Select(
                business_type_dropdown
            )

            valid_values = [
                "Sole Trader",
                "Company",
                "Partnership",
                "Trust"
            ]

            valid_options = [
                option
                for option in select.options
                if option.get_attribute("value")
                in valid_values
            ]

            if not valid_options:

                raise Exception(
                    "No valid Business Type options were found."
                )

            selected_option = random.choice(
                valid_options
            )

            selected_value = selected_option.get_attribute(
                "value"
            )

            select.select_by_value(
                selected_value
            )

            slow_down()

            print(
                f"✅ Business Type selected: "
                f"{selected_value}"
            )

    # ======================================================
    # SAVE COMPANY DETAILS
    # ======================================================
    def save_company_details(self):

        with allure.step(
            "Click Save Button"
        ):

            save_button = self.wait.until(
                EC.presence_of_element_located(
                    self.page.SAVE_BUTTON
                )
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

            slow_down(2)

            print(
                "✅ Save button clicked successfully"
            )

    # ======================================================
    # CLICK ORGANISATION ADDRESS EDIT
    # ======================================================
    def click_organisation_address_edit(self):

        with allure.step(
            "Click Edit Button in Organisation Addresses"
        ):

            edit_button = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.ORGANISATION_ADDRESS_EDIT_BUTTON
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

            slow_down()

            print(
                "✅ Organisation Address Edit button clicked successfully"
            )

        # ======================================================
    # UPDATE ORGANISATION ADDRESS
    # ======================================================
    def update_organisation_address(self):

        with allure.step(
            "Update Organisation Address"
        ):

            # --------------------------------------------------
            # Wait for address modal
            # --------------------------------------------------
            self.wait.until(
                EC.visibility_of_element_located(
                    self.page.ADDRESS_MODAL
                )
            )

            print(
                "✅ Organisation Address modal opened successfully"
            )

            # --------------------------------------------------
            # ADDRESS 1
            # --------------------------------------------------
            address_1 = self.wait.until(
                EC.visibility_of_element_located(
                    self.page.ADDRESS_1_INPUT
                )
            )   

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                address_1
            )

            slow_down()

            address_1.clear()

            real_addresses = [
                ("George Street", "Sydney", "NSW", "2000"),
                ("Collins Street", "Melbourne", "VIC", "3000"),
                ("Queen Street", "Brisbane", "QLD", "4000"),
                ("King William Street", "Adelaide", "SA", "5000"),
                ("St Georges Terrace", "Perth", "WA", "6000"),
                ("Elizabeth Street", "Hobart", "TAS", "7000"),
                ("Northbourne Avenue", "Canberra", "ACT", "2612"),
                ("Macquarie Street", "Parramatta", "NSW", "2150")
            ]

            selected_address = random.choice(real_addresses)

            address_1_value = selected_address[0]
            suburb_value = selected_address[1]
            state_value = selected_address[2]
            postcode_value = selected_address[3]

            address_1.send_keys(
                address_1_value
            )

            slow_down()

            print(
                f"✅ Address 1 updated: {address_1_value}"
            )


            # --------------------------------------------------
            # ADDRESS 2
            # --------------------------------------------------
            address_2 = self.wait.until(
                EC.visibility_of_element_located(
                    self.page.ADDRESS_2_INPUT
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                address_2
            )

            slow_down()

            address_2.clear()

            unit_numbers = [
                "Unit 2",
                "Unit 5",
                "Unit 8",
                "Unit 12",
                "Unit 15",
                "Suite 3",
                "Suite 7"
            ]

            address_2_value = random.choice(unit_numbers)

            address_2.send_keys(
                address_2_value
            )

            slow_down()

            print(
                f"✅ Address 2 updated: {address_2_value}"
            )


            # --------------------------------------------------
            # SUBURB
            # --------------------------------------------------
            suburb = self.wait.until(
                EC.visibility_of_element_located(
                    self.page.SUBURB_INPUT
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                suburb
            )

            slow_down()

            suburb.clear()

            suburb.send_keys(
                suburb_value
            )

            slow_down()

            print(
                f"✅ Suburb updated: {suburb_value}"
            )

            # --------------------------------------------------
            # STATE
            # --------------------------------------------------
            state_dropdown = self.wait.until(
                EC.visibility_of_element_located(
                    self.page.STATE_SELECT
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

            # Get all valid non-empty options
            valid_state_options = [
                option
                for option in state_select.options
                if option.get_attribute("value")
                and option.text.strip()
            ]

            if not valid_state_options:

                raise Exception(
                    "No valid State options were found."
                )

            # Randomly choose one State
            selected_state = random.choice(
                valid_state_options
            )

            selected_state_value = (
                selected_state.get_attribute("value")
            )

            selected_state_text = (
                selected_state.text.strip()
            )

            state_select.select_by_value(
                selected_state_value
            )

            slow_down()

            print(
                f"✅ State selected randomly: "
                f"{selected_state_text}"
            )

            # --------------------------------------------------
            # POSTCODE
            # --------------------------------------------------
            postcode = self.wait.until(
                EC.visibility_of_element_located(
                    self.page.POSTCODE_INPUT
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                postcode
            )

            slow_down()

            postcode.clear()

            random_postcode = str(random.randint(1000, 9999))

            postcode.send_keys(
                random_postcode
            )

            slow_down()

            print(
                f"✅ Postcode updated randomly: {random_postcode}"
            )

    # ======================================================
    # SAVE ORGANISATION ADDRESS
    # ======================================================
    def save_organisation_address(self):

        with allure.step(
            "Save Organisation Address"
        ):

            save_button = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.ADDRESS_MODAL_SAVE_BUTTON
                )
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

            slow_down(2)

            print(
                "✅ Organisation Address saved successfully"
            )

        # ======================================================
    # CLICK NEW ADDRESS
    # ======================================================
    def click_new_address(self):

        with allure.step(
            "Click New Address Button"
        ):

            new_address_button = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.NEW_ADDRESS_BUTTON
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                new_address_button
            )

            slow_down()

            self.driver.execute_script(
                "arguments[0].click();",
                new_address_button
            )

            slow_down()

            print(
                "✅ New Address button clicked successfully"
            )

    # ======================================================
    # FILL NEW ADDRESS FORM
    # ======================================================
    def fill_new_address(self):

        with allure.step(
            "Fill New Organisation Address Form"
        ):

            # --------------------------------------------------
            # WAIT FOR NEW ADDRESS MODAL
            # --------------------------------------------------
            self.wait.until(
                EC.visibility_of_element_located(
                    self.page.ADDRESS_MODAL
                )
            )

            print(
                "✅ New Address modal opened successfully"
            )

            # --------------------------------------------------
            # ADDRESS
            # --------------------------------------------------
            address = self.wait.until(
                EC.visibility_of_element_located(
                    self.page.NEW_ADDRESS_INPUT
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
            address
    )

            slow_down()

            address.clear()

            new_addresses = [
                ("Flinders Street", "Melbourne", "VIC", "3000"),
                ("George Street", "Sydney", "NSW", "2000"),
                ("Queen Street", "Brisbane", "QLD", "4000"),
                ("Grenfell Street", "Adelaide", "SA", "5000"),
                ("Hay Street", "Perth", "WA", "6000"),
                ("Liverpool Street", "Hobart", "TAS", "7000"),
                ("Bunda Street", "Canberra", "ACT", "2601"),
                ("Church Street", "Parramatta", "NSW", "2150")
            ]

            selected_new_address = random.choice(new_addresses)

            new_address_value = selected_new_address[0]
            new_suburb_value = selected_new_address[1]
            new_state_value = selected_new_address[2]
            new_postcode_value = selected_new_address[3]

            address.send_keys(
                new_address_value
            )

            slow_down()

            print(
                f"✅ New Address updated: {new_address_value}"
            )

            # --------------------------------------------------
            # ADDRESS 2
            # --------------------------------------------------
            address_2 = self.wait.until(
                EC.visibility_of_element_located(
                    self.page.NEW_ADDRESS_2_INPUT
                )   
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                address_2
            )   

            slow_down()

            address_2.clear()

            new_unit_numbers = [
                "Unit 1",
                "Unit 4",
                "Unit 6",
                "Unit 9",
                "Unit 14",
                "Suite 2",
                "Suite 5"
            ]

            new_address_2_value = random.choice(new_unit_numbers)

            address_2.send_keys(
                new_address_2_value
            )

            slow_down()

            print(
                f"✅ New Address 2 updated: {new_address_2_value}"
            )


            # --------------------------------------------------
            # SUBURB
            # --------------------------------------------------
            suburb = self.wait.until(
                EC.visibility_of_element_located(
                    self.page.NEW_SUBURB_INPUT
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                suburb
            )

            slow_down()

            suburb.clear()

            suburb.send_keys(
                new_suburb_value
            )

            slow_down()

            print(
                f"✅ New Suburb updated: {new_suburb_value}"
            )

            # --------------------------------------------------
            # STATE
            # --------------------------------------------------
            state_dropdown = self.wait.until(
                EC.visibility_of_element_located(
                    self.page.NEW_STATE_SELECT
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

            # Get available non-empty state options
            valid_state_options = [
                option
                for option in state_select.options
                if option.get_attribute("value")
                and option.text.strip()
            ]

            if not valid_state_options:

                raise Exception(
                    "No valid State options were found "
                    "for the New Address form."
                )

            # Randomly select a State
            selected_state = random.choice(
                valid_state_options
            )

            selected_state_value = (
                selected_state.get_attribute("value")
            )

            selected_state_text = (
                selected_state.text.strip()
            )

            state_select.select_by_value(
                selected_state_value
            )

            slow_down()

            print(
                f"✅ New Address State selected randomly: "
                f"{selected_state_text}"
            )

            # --------------------------------------------------
            # POSTCODE
            # --------------------------------------------------
            postcode = self.wait.until(
                EC.visibility_of_element_located(
                    self.page.NEW_POSTCODE_INPUT
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                postcode
            )

            slow_down()

            postcode.clear()

            random_postcode = str(random.randint(1000, 9999))

            postcode.send_keys(
                random_postcode
            )

            slow_down()

            print(
                f"✅ New Address Postcode updated randomly: {random_postcode}"
            )

    # ======================================================
    # SAVE NEW ADDRESS
    # ======================================================
    def save_new_address(self):

        with allure.step(
            "Save New Organisation Address"
        ):

            save_button = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.NEW_ADDRESS_SAVE_BUTTON
                )
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

            slow_down(2)

            print(
                "✅ New Organisation Address saved successfully"
            )

    # ======================================================
    # CLICK THE MAKE PRIMARY BUTTON FOR THE NEW ADDRESS
    # ======================================================

    def click_make_primary_randomly(self):
        with allure.step("Make a Random Organisation Address Primary"):

            make_primary_buttons = self.wait.until(
                lambda driver: [
                    button
                    for button in driver.find_elements(
                        *self.page.MAKE_PRIMARY_BUTTONS
                    )
                    if button.is_displayed() and button.is_enabled()
                ]
            )

            if not make_primary_buttons:
                raise Exception(
                    "No visible 'Make Primary' buttons were found."
                )

            selected_button = random.choice(
                make_primary_buttons
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                selected_button
            )

            slow_down()

            self.driver.execute_script(
                "arguments[0].click();",
                selected_button
            )

            slow_down(2)

            print(
                f"✅ Random 'Make Primary' button clicked "
                f"from {len(make_primary_buttons)} available address(es)"
            )

    # --------------------------------------------------
    # CLICK THE DELETE BUTTON FOR A ORGANISATION ADDRESS
    # --------------------------------------------------        
    def delete_random_organisation_address(self):
        with allure.step(
            "Delete a Random Organisation Address"
        ):

            # --------------------------------------------------
            # FIND ALL DELETE BUTTONS
            # --------------------------------------------------
            delete_buttons = self.wait.until(
                lambda driver: [
                    button
                    for button in driver.find_elements(
                        *self.page.DELETE_ADDRESS_BUTTONS
                    )
                    if button.is_displayed() and button.is_enabled()
                ]
            )

            if not delete_buttons:
                raise Exception(
                    "No visible 'Delete' buttons were found."
                )

            # --------------------------------------------------
            # SELECT ONE DELETE BUTTON RANDOMLY
            # --------------------------------------------------
            selected_button = random.choice(
                delete_buttons
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                selected_button
            )

            slow_down()

            self.driver.execute_script(
                "arguments[0].click();",
                selected_button
            )

            slow_down()

            print(
                f"✅ Random 'Delete' button clicked "
                f"from {len(delete_buttons)} available address(es)"
            )

            # --------------------------------------------------
            # WAIT FOR CONFIRMATION POPUP
            # --------------------------------------------------
            yes_button = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.DELETE_CONFIRM_YES_BUTTON
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                yes_button
            )

            slow_down()

            self.driver.execute_script(
                "arguments[0].click();",
                yes_button
            )

            slow_down(2)

            print(
                "✅ Delete confirmation 'Yes' button clicked successfully"
            )
    # ======================================================
    # SUBSCRIPTION DETAILS EXPAND
    # ======================================================
    
    def expand_webshop_table(self):
        with allure.step(
            "Expand Webshop Subscription Table"
        ):

            # --------------------------------------------------
            # FIND WEBSHOP EXPAND ARROW
            # --------------------------------------------------
            expand_arrow = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.WEBSHOP_EXPAND_ARROW
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                expand_arrow
            )

            slow_down()

            self.driver.execute_script(
                "arguments[0].click();",
                expand_arrow
            )

            slow_down()

            print(
                "✅ Webshop table expanded successfully"
            )

    # ======================================================
    # EXPLORE ALL SUBSCRIPTIONS BUTTON
    # ======================================================

    def explore_all_subscriptions_and_close(self):
        with allure.step("Explore All Subscriptions"):

            explore_button = self.wait.until(
                EC.presence_of_element_located(
                    self.page.EXPLORE_ALL_SUBSCRIPTIONS_BUTTON
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                explore_button
            )

            slow_down()

            self.wait.until(
                lambda driver: (
                    explore_button.is_displayed()
                    and explore_button.is_enabled()
                )
            )

            self.driver.execute_script(
                "arguments[0].click();",
                explore_button
            )

            slow_down(2)

            print(
                "✅ Explore All Subscriptions button clicked successfully"
            )

            # --------------------------------------------------
            # FIND CLOSE X BUTTON
            # --------------------------------------------------
            close_button = self.wait.until(
                EC.element_to_be_clickable(
                    self.page.SUBSCRIPTION_DETAILS_CLOSE_BUTTON
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                close_button
            )

            slow_down()

            # --------------------------------------------------
            # CLICK CLOSE X
            # --------------------------------------------------
            self.driver.execute_script(
                "arguments[0].click();",
                close_button
            )

            slow_down(2)

            print(
                "✅ Subscription details form closed successfully"
            )

    # ======================================================
    # CHANGE SUBSCRIPTION RANDOMLY - DROWNGRADE
    # ======================================================

    def change_subscription_randomly(self):
        with allure.step("Change Subscription Randomly"):

            try:
                # ==================================================
                # STEP 1 - FIND SUBSCRIPTION DROPDOWN
                # ==================================================
                subscription_dropdown = self.wait.until(
                    EC.presence_of_element_located(
                        self.page.CHANGE_SUBSCRIPTION_SELECT
                    )
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    subscription_dropdown
                )

                slow_down()

                select = Select(subscription_dropdown)

                # ==================================================
                # STEP 2 - GET ENABLED SUBSCRIPTION OPTIONS
                # ==================================================
                valid_options = [
                    option
                    for option in select.options
                    if option.is_enabled()
                    and option.get_attribute("value") != "0: null"
                    and option.text.strip().lower()
                    != "select subscription"
                ]

                if not valid_options:
                    print(
                        "⚠️ No enabled subscription options available. "
                        "Skipping subscription change."
                    )
                    return

                # ==================================================
                # STEP 3 - SELECT RANDOM SUBSCRIPTION
                # ==================================================
                selected_option = random.choice(valid_options)

                selected_text = selected_option.text.strip()
                selected_value = selected_option.get_attribute("value")

                select.select_by_value(selected_value)

                slow_down()

                print(
                    f"✅ Random subscription selected: "
                    f"{selected_text}"
                )

                # ==================================================
                # STEP 4 - FIND CHANGE SUBSCRIPTION BUTTON
                # ==================================================
                change_button = self.wait.until(
                    EC.presence_of_element_located(
                        self.page.CHANGE_SUBSCRIPTION_BUTTON
                    )
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    change_button
                )

                slow_down()

                # ==================================================
                # STEP 5 - CHECK WHETHER BUTTON IS ENABLED
                # ==================================================
                if not change_button.is_enabled():
                    print(
                        "⚠️ Change Subscription button is disabled. "
                        "Skipping subscription change."
                    )
                    return

                # ==================================================
                # STEP 6 - CLICK CHANGE SUBSCRIPTION
                # ==================================================
                self.driver.execute_script(
                    "arguments[0].click();",
                    change_button
                )

                slow_down(2)

                print(
                    "✅ Change Subscription button clicked successfully"
                )

                # ==================================================
                # STEP 7 - WAIT FOR CONFIRMATION POPUP
                # ==================================================
                confirm_button = self.wait.until(
                    EC.element_to_be_clickable(
                        self.page.CONFIRM_CHANGE_SUBSCRIPTION_BUTTON
                    )
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    confirm_button
                )

                slow_down()

                # ==================================================
                # STEP 8 - CLICK CONFIRM
                # ==================================================
                self.driver.execute_script(
                    "arguments[0].click();",
                    confirm_button
                )

                slow_down(2)

                print(
                    f"✅ Subscription change confirmed successfully: "
                    f"{selected_text}"
                )

            except Exception as e:

                print(
                    "⚠️ Subscription change step could not be completed. "
                    "Skipping this step."
                )
                print(f"   Reason: {e}")

    def click_billing_portal(self):
        with allure.step("Click Billing Portal"):

            try:
                billing_button = self.wait.until(
                    EC.presence_of_element_located(
                        self.page.BILLING_PORTAL_BUTTON
                    )
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    billing_button
                )

                slow_down()

                if not billing_button.is_enabled():
                    print(
                        "⚠️ Billing Portal button is disabled. "
                        "Skipping this step."
                    )
                    return

                self.driver.execute_script(
                    "arguments[0].click();",
                    billing_button
                )

                slow_down(2)

                print(
                    "✅ Billing Portal button clicked successfully"
                )

            except Exception as e:
                print(
                    "⚠️ Billing Portal step could not be completed. "
                    "Skipping this step."
                )
                print(f"   Reason: {e}")

         # =========================================================
    # CHANGE STATUS TO ON-HIRE
    # =========================================================

    def change_status_to_on_hire(self):

        self._wait_ui_ready()

        with allure.step("Change Order Status To On-Hire"):

            print(
                "Looking for current Accepted status dropdown..."
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
                    "Normal status dropdown click failed: "
                    f"{repr(e)}"
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
                "Looking for On-Hire option..."
            )

            on_hire_option = self.wait.until(
                EC.visibility_of_element_located(
                    self.page.ON_HIRE_OPTION
                )
            )

            print(
                "✅ On-Hire option found"
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                on_hire_option
            )

            slow_down()

            try:

                on_hire_option.click()

                print(
                    "✅ On-Hire option clicked"
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
                    "arguments[0].click();",
                    on_hire_option
                )

                print(
                    "✅ On-Hire option clicked "
                    "using JavaScript"
                )

            slow_down()

            # -------------------------------------------------
            # OPTIONAL CONFIRMATION
            # -------------------------------------------------

            print(
                "Checking for On-Hire confirmation popup..."
            )

            try:

                yes_button = WebDriverWait(
                    self.driver,
                    5
                ).until(
                    EC.element_to_be_clickable(
                        self.page.ON_HIRE_YES_BUTTON
                    )
                )

                print(
                    "✅ On-Hire confirmation popup appeared"
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    yes_button
                )

                slow_down()

                try:

                    yes_button.click()

                    print(
                        "✅ On-Hire confirmation Yes button clicked"
                    )

                except Exception as e:

                    print(
                        "Normal Yes button click failed: "
                        f"{repr(e)}"
                    )

                    yes_button = self.wait.until(
                        EC.presence_of_element_located(
                            self.page.ON_HIRE_YES_BUTTON
                        )
                    )

                    self.driver.execute_script(
                        "arguments[0].click();",
                        yes_button
                    )

                    print(
                        "✅ On-Hire confirmation Yes button "
                        "clicked using JavaScript"
                    )

            except TimeoutException:

                print(
                    "ℹ️ No confirmation popup appeared. "
                    "Continuing..."
                )

            slow_down()

            self._wait_ui_ready()

            print(
                "Waiting for order status to become On-Hire..."
            )

            self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//button[contains(@class,'dropdown-toggle') "
                        "and normalize-space()='On-Hire']"
                    )
                )
            )

            print(
                "✅ Order status changed to On-Hire successfully"
            )

    # ======================================================
    # COMPLETE COMPANY DETAILS FLOW
    # ======================================================
    def update_company_details(self):

        self.change_abn()

        self.toggle_registered_for_gst()

        self.select_business_type()

        self.save_company_details()

        self.click_organisation_address_edit()