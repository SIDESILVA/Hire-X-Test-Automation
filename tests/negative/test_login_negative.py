import pytest
import allure

from modules.auth_module import AuthModule


@pytest.mark.negative
@allure.title("NEG - Login with Invalid Credentials")
def test_login_invalid_credentials(driver):

    auth = AuthModule(driver)

    with allure.step("Open login page"):
        driver.delete_all_cookies()
        driver.get("https://app-hire-x-dev-multi-tenant-angular-01-bkgee7ewapa0c5es.southeastasia-01.azurewebsites.net/webshopnotfound")

    with allure.step("Try invalid login"):
        auth.login(
            url="https://app-hire-x-dev-multi-tenant-angular-01-bkgee7ewapa0c5es.southeastasia-01.azurewebsites.net/webshopnotfound",
            tenant="MetroHaven",
            username="wronguser@gmail.com",
            password="WrongPassword123",
            expect_success=False   # ⭐ IMPORTANT CHANGE
        )

    with allure.step("Verify login failed"):
        assert "/supplier/dashboard" not in driver.current_url