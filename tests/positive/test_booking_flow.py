import pytest
import allure

from modules.booking_module import BookingModule


@pytest.mark.smoke
@allure.title("Tenant + Full Booking Flow (POM Version)")
def test_booking_flow(driver):

    booking = BookingModule(driver)

    with allure.step("Open Site"):
        booking.open_site(
            "https://app-hire-x-dev-multi-tenant-angular-01-bkgee7ewapa0c5es.southeastasia-01.azurewebsites.net/webshopnotfound"
        )

    with allure.step("Set Tenant"):
        booking.set_tenant("MetroHaven")

    with allure.step("Select Product"):
        booking.click_first_product()

    with allure.step("Set Order Details"):
        booking.set_end_date()
        booking.set_quantity()
        booking.request_booking()

    with allure.step("Shipping"):
        booking.select_random_shipping()

    with allure.step("Customer"):
        booking.fill_customer()

    with allure.step("Address"):
        booking.handle_addresses()

    with allure.step("Next"):
        booking.go_next()

    with allure.step("Terms"):
        booking.accept_terms()

    with allure.step("Final Submit"):
        booking.submit_booking()

    with allure.step("Close"):
        booking.close_modal()