import pytest
import allure

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from modules.auth_module import AuthModule
from utils.screenshot import take_screenshot

# ----------Skip decorator(Login skipped)--------------------
@pytest.mark.skip(reason="Login already handled by session fixture")
@allure.title("TC01 - Verify Login and Dashboard Load")
def test_login_grandrest(driver):

    auth = AuthModule(driver)

    # ---------------- LOGIN ----------------
    auth.login(
        url="https://app-hire-x-dev-multi-tenant-angular-01-bkgee7ewapa0c5es.southeastasia-01.azurewebsites.net/webshopnotfound",
        tenant="MetroHaven",
        username="himasha1@gmail.com",
        password="Abc12345"
    )

    # ---------------- VERIFY DASHBOARD ----------------
    wait = WebDriverWait(driver, 40)

    wait.until(
        EC.url_contains("/supplier/dashboard")
    )

    take_screenshot(driver, "dashboard_success")

    print("✅ Login successful")