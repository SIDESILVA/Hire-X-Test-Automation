import pytest
import allure

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from modules.customer_module import CustomerModule
from pages.customer_page import CustomerPage


@pytest.mark.smoke
@allure.title("Create Customer")
def test_create_customer(driver, login):

    driver.get(
        "https://app-hire-x-dev-multi-tenant-angular-01-bkgee7ewapa0c5es.southeastasia-01.azurewebsites.net/supplier/customers"
    )

    wait = WebDriverWait(driver, 60)

    wait.until(
        EC.visibility_of_element_located(
            CustomerPage.NEW_BUTTON
        )
    )

    customer = CustomerModule(driver)

    customer.create_customer()

    print("✅ TEST COMPLETED SUCCESSFULLY")