import pytest
import allure

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from modules.list_module import ListModule


@pytest.mark.smoke
@allure.title("Create List")
def test_create_list(driver, login):

    driver.get(
        "https://app-hire-x-dev-multi-tenant-angular-01-bkgee7ewapa0c5es.southeastasia-01.azurewebsites.net/supplier/lists"
    )

    wait = WebDriverWait(driver, 40)

    #Wait for Page load

    wait.until(
        EC.url_contains("/supplier/lists")
    )

    print("✅ SUCCESS: Navigated to List section")

    #Create List

    list_module = ListModule(driver)

    list_module.create_list()