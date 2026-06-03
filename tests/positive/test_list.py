import pytest
import allure

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from modules.list_module import ListModule


@pytest.mark.smoke
@allure.title("Full Flow + Create + Zero Member Selection")
def test_open_random_list_email(driver, login):

    driver.get(
        "https://app-hire-x-dev-multi-tenant-angular-01-bkgee7ewapa0c5es.southeastasia-01.azurewebsites.net/supplier/lists"
    )

    wait = WebDriverWait(driver, 40)

    # VERIFY LIST PAGE LOAD
    wait.until(
        EC.url_contains("/supplier/lists")
    )

    list_module = ListModule(driver)

    # ======================================================
    # EXISTING FLOW
    # ======================================================
    list_module.open_random_list()

    list_module.email_flow()

    list_module.update_list_name_and_save()

    # ======================================================
    # NEW FLOW
    # ======================================================
    list_module.click_view_and_open_customer()

    # ======================================================
    # FINAL SUCCESS
    # ======================================================
    print("✅ SUCCESS: FULL FLOW COMPLETED")