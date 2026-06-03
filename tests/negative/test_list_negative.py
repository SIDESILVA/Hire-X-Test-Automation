import pytest
import allure

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from modules.list_module import ListModule


@pytest.mark.negative
@allure.title("NEG - Create List with Empty Fields Validation")
def test_create_list_negative(driver, login):

    driver.get(
        "https://app-hire-x-dev-multi-tenant-angular-01-bkgee7ewapa0c5es.southeastasia-01.azurewebsites.net/supplier/lists"
    )

    wait = WebDriverWait(driver, 40)

    wait.until(
        EC.url_contains("/supplier/lists")
    )

    print("✅ Navigated to List section")

    list_module = ListModule(driver)

    # Step 1: Click create without filling required fields
    list_module.create_list()

    # Step 2: Validate negative behavior
    error_found = (
        "required" in driver.page_source.lower() or
        "error" in driver.page_source.lower()
    )

    assert error_found, "❌ Validation message NOT shown for empty fields"

    print("✅ Negative validation working correctly")