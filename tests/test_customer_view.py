import allure

from modules.customer_view_module import CustomerViewModule


@allure.title("Customer View Booking Flow")
def test_customer_view_flow(driver):

    driver.get(
        "https://app-hire-x-dev-multi-tenant-angular-01-bkgee7ewapa0c5es.southeastasia-01.azurewebsites.net/webshopnotfound"
    )

    customer_view = CustomerViewModule(driver)

    customer_view.complete_booking_flow()

    print(
        "✅ Customer booking flow completed successfully"
    )