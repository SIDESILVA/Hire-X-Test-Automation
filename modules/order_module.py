import random
import time
import allure

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from pages.order_page import OrderPage


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

        time.sleep(1)

    # ---------------- OPEN ----------------
    def open_orders(self, url):

        self.driver.get(url)

        self.wait.until(
            EC.url_contains("/supplier/orders")
        )

        self._wait_ui_ready()

    # ---------------- NEW ORDER ----------------
    def click_new_order(self):

        self._wait_ui_ready()

        btn = self.wait.until(
            EC.element_to_be_clickable(self.page.NEW_ORDER_BTN)
        )

        btn.click()

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

        time.sleep(1)

        try:
            dropdown.click()
        except:
            self.driver.execute_script(
                "arguments[0].click();",
                dropdown
            )

        options = self.wait.until(
            EC.presence_of_all_elements_located(self.page.CUSTOMER_OPTIONS)
        )

        valid_options = []

        for opt in options:
            text = opt.text.strip().lower()

            if text == "" or "create a new customer" in text:
                continue

            valid_options.append(opt)

        if not valid_options:
            raise Exception("No valid customers available in dropdown")

        random.choice(valid_options).click()

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

        time.sleep(1)

        try:
            create_btn.click()
        except:
            self.driver.execute_script(
                "arguments[0].click();",
                create_btn
            )

        self._wait_ui_ready()

    # ---------------- ADD PRODUCT (🔥 UPDATED FOR DATA FILE) ----------------
    def add_product(self, product_data):

        product_name = product_data["product"]
        search_key = product_data["search_key"]
        quantity = product_data["quantity"]

        with allure.step(f"Add Product - {product_name}"):

            self._wait_ui_ready()

            product_input = self.wait.until(
                EC.element_to_be_clickable(self.page.PRODUCT_INPUT)
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                product_input
            )

            product_input.clear()
            product_input.send_keys(search_key)

            first_option = self.wait.until(
                EC.element_to_be_clickable(self.page.PRODUCT_OPTIONS)
            )

            self.driver.execute_script(
                "arguments[0].click();",
                first_option
            )

            self._wait_ui_ready()

            qty_input = self.wait.until(
                EC.visibility_of_element_located(self.page.QUANTITY_INPUT)
            )

            qty_input.clear()
            qty_input.send_keys(str(quantity))

            self._wait_ui_ready()

            add_btn = self.wait.until(
                EC.element_to_be_clickable(self.page.ADD_BUTTON)
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                add_btn
            )

            time.sleep(1)

            try:
                add_btn.click()
            except:
                self.driver.execute_script(
                    "arguments[0].click();",
                    add_btn
                )

            self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, f"//*[contains(text(),'{product_name}')]")
                )
            )

            self._wait_ui_ready()

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

        except:
            pass