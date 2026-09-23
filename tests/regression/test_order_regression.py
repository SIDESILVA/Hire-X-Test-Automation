import pytest
import allure
import random

from modules.order_module import OrderModule
from utils.screenshot import take_screenshot
from data.product_data import PRODUCT_SEARCH_DATA


@pytest.mark.regression
@allure.title(
    "TC02 - Create Order - Full Regression Flow"
)
def test_create_order(driver, login):

    order = OrderModule(driver)

    # =========================================================
    # OPEN ORDERS PAGE
    # =========================================================

    with allure.step(
        "Open Orders Page"
    ):

        order.open_orders(
            "https://app-hire-x-dev-multi-tenant-angular-01-bkgee7ewapa0c5es.southeastasia-01.azurewebsites.net/supplier/orders"
        )

    # =========================================================
    # CREATE ORDER
    # =========================================================

    with allure.step(
        "Create Order Flow"
    ):

        order.click_new_order()

        order.verify_create_form()

        order.select_random_customer()

        order.click_create()

    # =========================================================
    # SEND CUSTOMER EMAIL
    # =========================================================

    with allure.step(
        "Send Customer Email With Attachment"
    ):

        order.send_customer_email_with_attachment()

    # =========================================================
    # EDIT BILLING ADDRESS
    # =========================================================

    with allure.step(
        "Edit Billing Address"
    ):

        order.edit_billing_address()

     # =========================================================
    # SET START DATE AND START TIME
    # =========================================================

    with allure.step(
        "Set Start Date (+1 Day) And Start Time"
    ):

        order.set_start_date_and_time()

    # =========================================================
    # SET END DATE AND END TIME
    # =========================================================

    with allure.step(
        "Set End Date (+2 Days) And End Time"
    ):

        order.set_end_date_plus_two_days()

    # =========================================================
    # LINK ORDER
    # =========================================================

    with allure.step(
        "Link Order If Available"
    ):

        order.link_order_if_available()

    # =========================================================
    # ADD MULTIPLE PRODUCTS
    # =========================================================

    with allure.step(
        "Add Multiple Products"
    ):

        for _ in range(2):

            product = random.choice(
                PRODUCT_SEARCH_DATA
            )

            order.add_product(
                product
            )

    # =========================================================
    # ADD RANDOM CONSUMABLE
    # =========================================================

    with allure.step(
        "Add Random Consumable"
    ):

        order.add_random_consumable()

    # =========================================================
    # ADD CUSTOM FEE
    # =========================================================

    with allure.step(
        "Add Custom Fee"
    ):

        try:

            order.add_custom_fee()

        except Exception as e:

            allure.attach(
                str(e),
                name="Custom Fee Error",
                attachment_type=(
                    allure.attachment_type.TEXT
                )
            )

            raise

    # =========================================================
    # ADD NOTES
    # =========================================================

    with allure.step(
        "Add Notes"
    ):

        order.add_notes()

    # =========================================================
    # SAVE ORDER
    # =========================================================

    with allure.step(
        "Save Order"
    ):

        order.click_save()

    # =========================================================
    # MARK AS QUOTED
    # =========================================================

    with allure.step(
        "Mark As Quoted"
    ):

        order.click_mark_as_quoted()

    # =========================================================
    # UNLINK ORDER IF AVAILABLE
    # =========================================================

    with allure.step(
        "Unlink Order If Available"
    ):

        order.unlink_order_if_available()

    # =========================================================
    # WAIT FOR UI RELOAD
    # =========================================================

    order._wait_ui_ready()

    # =========================================================
    # EDIT PRODUCT LINE
    # =========================================================

    with allure.step(
        "Edit PRODUCT Line (After Quoted)"
    ):

        order.edit_order_line()

    # =========================================================
    # DELETE ONE PRODUCT
    # =========================================================

    with allure.step(
        "Delete ONE Product Line"
    ):

        order.delete_one_product()

    # =========================================================
    # EDIT CONSUMABLE
    # =========================================================

    with allure.step(
        "Edit Consumable & Charges"
    ):

        order.edit_consumable()

    # =========================================================
    # CHANGE STATUS TO ACCEPTED
    # =========================================================

    with allure.step(
        "Change Status To Accepted"
    ):

        order.change_status_to_accepted()

    # =========================================================
    # PAYMENT MODAL
    # =========================================================

    with allure.step(
        "Fill Payment"
    ):

        order.handle_payment_modal()

    # =========================================================
    # OPEN RECORD PAYMENT DETAILS
    # =========================================================

    with allure.step(
        "Open Payment Dialog"
    ):

        order.click_record_payment_details()

    # =========================================================
    # RECORD PAYMENT DETAILS
    # =========================================================

    with allure.step(
        "Record Payment Details"
    ):

        order.handle_record_payment_details()

    # =========================================================
    # OPEN INVOICE RECORDS
    # =========================================================

    with allure.step(
        "Open Invoice Records"
    ):

        order.open_invoice_records()

     # =========================================================
    # CREATE INVOICE
    # =========================================================

    with allure.step(
        "Create Invoice"
    ):

        order.click_create_invoice()

    # =========================================================
    # CONFIRM CREATE INVOICE
    # =========================================================

    with allure.step(
        "Confirm Create Invoice"
    ):

        order.confirm_create_invoice()

     # =========================================================
    # CHANGE STATUS TO ON-HIRE
    # =========================================================

    with allure.step(
        "Change Status To On-Hire"
    ):

        order.change_status_to_on_hire()

    # =========================================================
    # OPEN ATTACHMENTS
    # =========================================================

    with allure.step(
        "Open Attachments"
    ):

        order.open_attachments()

    # =========================================================
    # UPLOAD RANDOM ATTACHMENT
    # =========================================================

    with allure.step(
        "Upload Random Attachment"
    ):

        order.upload_random_attachment()

    # =========================================================
    # OPEN DOCUMENTS
    # =========================================================

    with allure.step(
        "Open Documents"
    ):

        order.open_documents()

    # =========================================================
    # DOWNLOAD ORDER DETAILS
    # =========================================================

    with allure.step(
        "Download Order Details"
    ):

        order.download_order_details()

    # =========================================================
    # DOWNLOAD TERMS AND CONDITIONS
    # =========================================================

    with allure.step(
        "Download Terms and Conditions"
    ):

        order.download_terms_and_conditions()

    # =========================================================
    # EMAIL DOCUMENTS
    # =========================================================

    with allure.step(
        "Email Documents"
    ):

        order.click_email_documents()

    # =========================================================
    # HANDLE EMAIL DOCUMENTS MODAL
    # =========================================================

    with allure.step(
        "Send Documents By Email"
    ):

        order.handle_email_documents_modal()

    # =========================================================
    # OPEN EMAILS
    # =========================================================

    with allure.step(
        "Open Emails"
    ):

        order.open_emails()

    # =========================================================
    # CLICK NEW EMAIL
    # =========================================================

    with allure.step(
        "Click New Email"
    ):

        order.click_new_email()

    # =========================================================
    # FILL AND SEND NEW EMAIL
    # =========================================================

    with allure.step(
        "Fill And Send New Email"
    ):

        order.fill_new_email_form()

    # =========================================================
    # FILL AND CREATE NEW TASK
    # =========================================================
    with allure.step("Click New Task"):
        order.click_new_task()

    with allure.step("Fill And Save New Task"):
        order.fill_new_task_form()

    # =========================================================
    # CHANGE STATUS TO RETURNED, INVOICED, COMPLETED, AND CANCELLED
    # =========================================================

    with allure.step("Change status to Returned"):
        order.change_status_to_returned()

    with allure.step("Change status to Invoiced and Completed"):
        order.change_status_to_invoiced_completed()

    with allure.step("Change status to Cancelled"):
        order.change_status_to_cancelled()

    with allure.step("Select cancellation reason and cancel order"):
        order.fill_cancellation_reason_and_cancel()

    # =========================================================
    # FINAL VALIDATION
    # =========================================================

    with allure.step(
        "Verify Order Page"
    ):

        assert "/supplier/orders" in driver.current_url

        assert driver.title != ""

    # =========================================================
    # SCREENSHOT
    # =========================================================

    take_screenshot(
        driver,
        "order_regression_completed"
    )