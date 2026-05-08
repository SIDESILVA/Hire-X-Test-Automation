import pytest
import allure

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from modules.customer_module import CustomerModule


@pytest.mark.smoke
@allure.title("Create Customer")
def test_create_customer(driver):

    driver.get(
        "https://app-hire-x-dev-multi-tenant-angular-01-bkgee7ewapa0c5es.southeastasia-01.azurewebsites.net/supplier/customers"
    )

    wait = WebDriverWait(driver, 40)

    wait.until(
        EC.url_contains("/supplier/customers")
    )

    customer = CustomerModule(driver)

    customer.create_customer()