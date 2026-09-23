import pytest
import allure

from modules.booking_module import BookingModule


@pytest.mark.regression
@allure.title("Tenant + Full Booking Flow (POM Version)")
def test_booking_flow(driver):

    booking = BookingModule(driver)

    with allure.step("Open Site"):

        booking.open_site(
            "https://app-hire-x-dev-multi-tenant-angular-01-bkgee7ewapa0c5es.southeastasia-01.azurewebsites.net/webshopnotfound"
        )

        booking.step_pause(
            "Site Loaded"
        )

    with allure.step("Set Tenant"):

        booking.set_tenant(
            "MetroHaven"
        )

        booking.step_pause(
            "Tenant Set"
        )

    with allure.step("Select Product"):

        booking.click_first_product()

        booking.step_pause(
            "Product Opened"
        )

    with allure.step("Set Order Details"):

        booking.set_booking_dates()

        booking.step_pause(
            "Booking Dates Set"
        )

        booking.set_quantity()

        booking.step_pause(
            "Quantity Set"
        )

        booking.request_booking()

        booking.step_pause(
            "Request Sent"
        )

    with allure.step("Add Another Product"):

        booking.add_random_product()

        booking.step_pause(
            "Second Product Selected"
        )

    with allure.step("Configure Second Product"):

        booking.configure_second_product_booking()

        booking.step_pause(
            "Second Product Booking Completed"
        )

    with allure.step("Shipping"):

        booking.select_random_shipping()

        booking.step_pause(
            "Shipping Selected"
        )

    with allure.step("Customer"):

        booking.fill_customer()

        booking.step_pause(
            "Customer Filled"
        )

    with allure.step("Address"):

        booking.handle_addresses()

        booking.step_pause(
            "Address Completed"
        )

    with allure.step("Next"):

        booking.go_next()

        booking.step_pause(
            "Next Clicked"
        )

    with allure.step("Terms"):

        booking.accept_terms()

        booking.step_pause(
            "Terms Accepted"
        )

    with allure.step("Credit Card"):

        booking.fill_credit_card_if_enabled()

        booking.step_pause(
            "Credit Card Checked"
        )

    with allure.step("Final Submit"):

        booking.submit_booking()

        booking.step_pause(
            "Booking Submitted"
        )

    with allure.step("Close"):

        booking.close_modal()

        booking.step_pause(
            "Modal Closed"
        )