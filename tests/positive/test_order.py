import pytest
import allure
import random

from modules.order_module import OrderModule
from utils.screenshot import take_screenshot
from data.product_data import PRODUCT_SEARCH_DATA


@pytest.mark.smoke
@allure.title("TC02 - Create Order Flow")
def test_create_order(driver, login):

    order = OrderModule(driver)

    product = random.choice(PRODUCT_SEARCH_DATA)

    with allure.step("Open Orders Page"):
        order.open_orders(
            "https://app-hire-x-dev-multi-tenant-angular-01-bkgee7ewapa0c5es.southeastasia-01.azurewebsites.net/supplier/orders"
        )

    with allure.step("Create Order Flow"):
        order.click_new_order()
        order.verify_create_form()
        order.select_random_customer()
        order.click_create()

    # Set End Date once
    with allure.step("Set End Date (+2 Days)"):
        order.set_end_date_plus_two_days()

    # Link Order if available
    with allure.step("Link Order If Available"):
        order.link_order_if_available()

    # Add Product once
    with allure.step("Add Product (Random Data)"):
        order.add_product(product)

    take_screenshot(driver, "order_completed")