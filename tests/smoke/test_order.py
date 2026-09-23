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

    with allure.step("Set End Date (+2 Days)"):
        order.set_end_date_plus_two_days()

    with allure.step("Link Order If Available"):
        order.link_order_if_available()

    with allure.step("Add Multiple Products"):
        for _ in range(2):
            product = random.choice(PRODUCT_SEARCH_DATA)
            order.add_product(product)

    with allure.step("Add Random Consumable"):
        order.add_random_consumable()

    with allure.step("Add Custom Fee"):
        try:
            order.add_custom_fee()
        except Exception as e:
            allure.attach(
                str(e),
                name="Custom Fee Error",
                attachment_type=allure.attachment_type.TEXT
            )
            raise

    with allure.step("Add Notes"):
        order.add_notes()

    with allure.step("Save Order"):
        order.click_save()

    with allure.step("Mark As Quoted"):
        order.click_mark_as_quoted()

    # IMPORTANT WAIT FOR UI RELOAD
    order._wait_ui_ready()

    with allure.step("Edit PRODUCT Line (After Quoted)"):
        order.edit_order_line()

    with allure.step("Delete ONE Product Line"):
        order.delete_one_product()

    with allure.step("Edit Consumable & Charges"):
        order.edit_consumable()

    with allure.step("Change Status To Accepted"):
        order.change_status_to_accepted()

    with allure.step("Fill Payment"):
        order.handle_payment_modal()

    with allure.step("Open Payment Dialog"):
        order.click_record_payment_details()

    with allure.step("Record Payment Details"):
        order.handle_record_payment_details()

        

    assert "/supplier/orders" in driver.current_url

    assert driver.title != ""
    

    take_screenshot(driver, "order_completed")