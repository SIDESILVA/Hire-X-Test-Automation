import random
import allure

from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from pages.product_page import ProductPage
from utils.image_provider import ImageProvider
from utils.delay_helper import slow_down


class ProductModule:

    def __init__(self, driver):

        self.driver = driver
        self.wait = WebDriverWait(driver, 40)
        self.page = ProductPage()
        self.image_provider = ImageProvider()

    # ---------------- SAFE CLICK ----------------
    def safe_click(self, locator):

        element = self.wait.until(
            EC.presence_of_element_located(locator)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            element
        )

        slow_down(1)

        try:
            element.click()
        except:
            self.driver.execute_script("arguments[0].click();", element)

    # ---------------- ENTER TEXT ----------------
    def enter_text(self, locator, value):

        field = self.wait.until(
            EC.element_to_be_clickable(locator)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            field
        )

        field.clear()
        field.send_keys(value)

    # ---------------- CATEGORY ----------------
    def select_category_meals_breakfast(self):

        with allure.step("Select Category"):

            self.safe_click(self.page.CATEGORY_DROPDOWN)
            slow_down(1)

            self.safe_click(self.page.MEALS_EXPAND_ICON)
            slow_down(1)

            self.safe_click(self.page.BREAKFAST_OPTION)
            slow_down(1)

            print("✅ Breakfast category selected")

    # ---------------- PRODUCT IMAGE ----------------
    def upload_image(self):

        with allure.step("Upload Product Image"):

            image_file = self.image_provider.get_next_image_file()

            file_input = self.wait.until(
                EC.presence_of_element_located(self.page.IMAGE_UPLOAD)
            )

            file_input.send_keys(image_file)

            slow_down(2)

            print(f"✅ Product image uploaded: {image_file}")
            return image_file

    # ---------------- PHOTOS TAB IMAGE ----------------
    def upload_photos_tab_images(self):

        with allure.step("Upload Photos Tab Images"):

            image_file = self.image_provider.get_next_image_file()

            upload_input = self.wait.until(
                EC.presence_of_element_located(self.page.PHOTOS_UPLOAD_INPUT)
            )

            self.driver.execute_script(
                "arguments[0].style.display='block';",
                upload_input
            )

            upload_input.send_keys(image_file)

            slow_down(3)

            print(f"✅ Photos tab image uploaded: {image_file}")

    # ---------------- FINALISE FLOW ----------------
    def finalise_product_flow(self):

        with allure.step("Finalise Product"):

            self.safe_click(self.page.FINALISE_NOW)
            slow_down(1)

            try:
                self.wait.until(
                    EC.invisibility_of_element_located(
                        (By.CLASS_NAME, "spinner-wrapper")
                    )
                )
            except:
                pass

            qty = self.wait.until(
                EC.visibility_of_element_located(self.page.QTY)
            )

            qty.clear()
            qty.send_keys("15")

            slow_down(1)

            self.safe_click(self.page.IS_FEATURED)
            slow_down(1)

            self.safe_click(self.page.SAVE_BTN)

            slow_down(3)

            print("✅ Product finalised")

    # ---------------- TABS ----------------
    def open_orders_tab(self):
        with allure.step("Open Orders Tab"):
            self.safe_click(self.page.ORDERS_TAB)
            slow_down(2)

    def open_tasks_tab(self):
        with allure.step("Open Tasks Tab"):
            self.safe_click(self.page.TASKS_TAB)
            slow_down(2)

    def open_photos_tab(self):
        with allure.step("Open Photos Tab"):
            self.safe_click(self.page.PHOTOS_TAB)
            slow_down(2)

    def open_shipping_tab(self):
        with allure.step("Open Shipping Tab"):
            self.safe_click(self.page.SHIPPING_TAB)
            slow_down(2)

    def open_pricing_tab(self):

        with allure.step("Open Pricing Tab"):

            pricing_tab = self.wait.until(
                EC.presence_of_element_located(self.page.PRICING_TAB)
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                pricing_tab
            )

            slow_down(1)

            try:
                pricing_tab.click()
            except:
                self.driver.execute_script(
                    "arguments[0].click();",
                    pricing_tab
                )

            slow_down(2)

            self.wait.until(
                EC.visibility_of_element_located(
                    self.page.PRICING_SECURITY_DEPOSIT
                )
            )

            print("✅ Pricing tab opened")

    # ---------------- STOCK TAB ----------------
    def open_stock_tab(self):

        with allure.step("Open Stock Tab"):

            stock_tab = self.wait.until(
                EC.presence_of_element_located(self.page.STOCK_TAB)
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                stock_tab
            )

            slow_down(1)

            try:
                stock_tab.click()
            except:
                self.driver.execute_script(
                    "arguments[0].click();",
                    stock_tab
                )

            slow_down(2)

            print("✅ Stock tab opened")

            # CLICK NEW BUTTON
            new_btn = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//tab[contains(@class,'active')]//button[normalize-space()='New']")
                )
            )

            self.driver.execute_script(
                "arguments[0].click();",
                new_btn
            )

            slow_down(2)

            print("✅ Stock NEW button clicked")

            # 🆕 OPEN STOCK ITEM FORM (ADDED)
            self.create_stock_item()

    # ---------------- STOCK ITEM FLOW (NEW - ADDED) ----------------
    def create_stock_item(self):

        with allure.step("Create Stock Item"):

            self.wait.until(
                EC.visibility_of_element_located(self.page.STOCK_SKU)
            )

            sku = f"SKU-{random.randint(10000, 99999)}"
            serial = f"SN-{random.randint(100000, 999999)}"
            barcode = f"BC-{random.randint(10000000, 99999999)}"
            value = str(round(random.uniform(1, 999), 2))

            self.enter_text(self.page.STOCK_SKU, sku)
            self.enter_text(self.page.STOCK_SERIAL_NUMBER, serial)
            self.enter_text(self.page.STOCK_BARCODE, barcode)
            self.enter_text(self.page.STOCK_VALUE, value)

            # LOCATION DROPDOWN
            location_dropdown = self.wait.until(
                EC.element_to_be_clickable(self.page.STOCK_LOCATION_DROPDOWN)
            )

            select = Select(location_dropdown)

            valid_options = [
                o for o in select.options
                if o.get_attribute("value")
                and "select" not in o.text.lower()
            ]

            if valid_options:
                chosen = random.choice(valid_options)
                select.select_by_value(chosen.get_attribute("value"))

            slow_down(1)

            # CREATE BUTTON
            create_btn = self.wait.until(
                EC.element_to_be_clickable(self.page.STOCK_CREATE_BTN)
            )

            self.driver.execute_script(
                "arguments[0].click();",
                create_btn
            )

            slow_down(2)

            print(f"✅ Stock Item Created | SKU={sku}, SERIAL={serial}, BARCODE={barcode}")

    # ---------------- SHIPPING FLOW ----------------
    def set_shipping_toggle(self, state: str):

        with allure.step(f"Set Shipping Toggle → {state.upper()}"):

            self.safe_click(self.page.SHIPPING_EDIT_BTN)
            slow_down(2)

            toggle = self.wait.until(
                EC.presence_of_element_located(self.page.SHIPPING_TOGGLE)
            )

            is_checked = toggle.is_selected()

            if state.lower() == "no":
                if is_checked:
                    self.driver.execute_script("arguments[0].click();", toggle)

            elif state.lower() == "yes":
                if not is_checked:
                    self.driver.execute_script("arguments[0].click();", toggle)

            slow_down(1)

            self.safe_click(self.page.SHIPPING_SAVE_BTN)
            slow_down(3)

            print(f"✅ Shipping set to {state.upper()}")

    # ---------------- PRICING FLOW ----------------
    def update_pricing_details(self):

        with allure.step("Update Pricing Details"):

            random_bond = str(random.randint(10, 500))
            random_note = f"Test Pricing {random.randint(1000, 9999)}"

            self.enter_text(self.page.PRICING_SECURITY_DEPOSIT, random_bond)
            self.enter_text(self.page.PRICING_NOTE, random_note)

            save_btn = self.wait.until(
                EC.element_to_be_clickable(self.page.PRICING_SAVE_BTN)
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                save_btn
            )

            slow_down(0.5)

            self.driver.execute_script(
                "arguments[0].click();",
                save_btn
            )

            slow_down(2)

            print("✅ Pricing details updated")

    def toggle_public_private_pricing(self):

        with allure.step("Toggle Public ↔ Private Pricing"):

            edit_btn = self.wait.until(
                EC.element_to_be_clickable(self.page.PRICING_EDIT_BTN)
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                edit_btn
            )

            slow_down(1)

            self.driver.execute_script("arguments[0].click();", edit_btn)

            toggle = self.wait.until(
                EC.presence_of_element_located(self.page.PRICING_TOGGLE)
            )

            slow_down(1)

            is_public = toggle.is_selected()

            if is_public:
                self.driver.execute_script("arguments[0].click();", toggle)
                print("🔁 Public → Private")
            else:
                print("ℹ️ Already Private")

            slow_down(1)

            save_btn = self.wait.until(
                EC.element_to_be_clickable(self.page.PRICING_SAVE_BTN)
            )

            self.driver.execute_script("arguments[0].click();", save_btn)

            slow_down(2)

            edit_btn_again = self.wait.until(
                EC.element_to_be_clickable(self.page.PRICING_EDIT_BTN)
            )

            self.driver.execute_script("arguments[0].click();", edit_btn_again)

            slow_down(1)

            toggle_again = self.wait.until(
                EC.presence_of_element_located(self.page.PRICING_TOGGLE)
            )

            is_public_again = toggle_again.is_selected()

            if not is_public_again:
                self.driver.execute_script("arguments[0].click();", toggle_again)
                print("🔁 Private → Public")
            else:
                print("ℹ️ Already Public")

            slow_down(1)

            final_save_btn = self.wait.until(
                EC.element_to_be_clickable(self.page.PRICING_SAVE_BTN)
            )

            self.driver.execute_script("arguments[0].click();", final_save_btn)

            slow_down(2)

            print("✅ Pricing toggle flow completed")

    # ---------------- TASK FLOW ----------------
    def click_new_task(self):

        with allure.step("Click New Task"):
            self.safe_click(self.page.NEW_TASK_BTN)
            slow_down(2)

            self.wait.until(
                EC.visibility_of_element_located(self.page.TASK_TYPE_DROPDOWN)
            )

    def select_random_dropdown(self, locator):

        element = self.wait.until(
            EC.element_to_be_clickable(locator)
        )

        select = Select(element)

        valid_options = [
            o for o in select.options
            if o.get_attribute("value")
            and "select" not in o.text.lower()
        ]

        chosen = random.choice(valid_options)
        select.select_by_value(chosen.get_attribute("value"))

        slow_down(1)
        return chosen.text

    def create_task_flow(self):

        with allure.step("Create Task"):

            task_type = self.select_random_dropdown(self.page.TASK_TYPE_DROPDOWN)
            user = self.select_random_dropdown(self.page.USER_DROPDOWN)

            save_btn = self.wait.until(
                EC.element_to_be_clickable(self.page.TASK_MODAL_SAVE_BTN)
            )

            self.driver.execute_script("arguments[0].click();", save_btn)

            slow_down(2)

            print("✅ Task saved successfully")

    # ---------------- MAIN FLOW ----------------
    def create_product(self, name, desc, price_note, price, bond):

        self.select_category_meals_breakfast()

        self.enter_text(self.page.NAME, name)
        self.enter_text(self.page.SHORT_DESC, desc)
        self.enter_text(self.page.PRICE_NOTE, price_note)
        self.enter_text(self.page.BASE_PRICE, price)
        self.enter_text(self.page.BOND, bond)

        slow_down(2)

        self.upload_image()

        self.safe_click(self.page.CREATE_BTN)

        slow_down(2)

        self.finalise_product_flow()

        self.open_orders_tab()

        self.open_tasks_tab()
        self.click_new_task()
        self.create_task_flow()

        self.open_photos_tab()
        self.upload_photos_tab_images()

        self.open_shipping_tab()

        self.set_shipping_toggle("no")
        self.set_shipping_toggle("yes")

        # PRICING
        self.open_pricing_tab()
        self.toggle_public_private_pricing()
        self.update_pricing_details()

        # STOCK TAB
        self.open_stock_tab()

        print("✅ FULL FLOW COMPLETED")