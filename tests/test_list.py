import pytest
import allure

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from modules.list_module import ListModule


@pytest.mark.smoke
@allure.title("Create List")
def test_create_list(driver):

    driver.get(
        "https://app-hire-x-dev-multi-tenant-angular-01-bkgee7ewapa0c5es.southeastasia-01.azurewebsites.net/supplier/lists"
    )

    wait = WebDriverWait(driver, 40)

    # ---------------- WAIT FOR PAGE LOAD ----------------

    wait.until(
        EC.url_contains("/supplier/lists")
    )

    print("✅ SUCCESS: Navigated to List section")

    # ---------------- CREATE LIST ----------------

    list_module = ListModule(driver)

    list_module.create_list()