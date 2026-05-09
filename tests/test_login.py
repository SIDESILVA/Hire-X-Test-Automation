# tests/test_login.py

import pytest
import allure

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.screenshot import take_screenshot


@pytest.mark.smoke
@allure.title("TC01 - Verify Login and Dashboard Load")
def test_login_grandrest(driver):

    wait = WebDriverWait(driver, 40)

    # ---------------- OPEN TENANT PAGE ----------------
    driver.get(
        "https://app-hire-x-dev-multi-tenant-angular-01-bkgee7ewapa0c5es.southeastasia-01.azurewebsites.net/webshopnotfound"
    )

    # ---------------- SET TENANT ----------------
    tenant_input = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "input[type='text']")
        )
    )

    tenant_input.clear()
    tenant_input.send_keys("GrandRest")

    wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(),'Set Tenant')]")
        )
    ).click()

    wait.until(EC.url_contains("/home"))

    # ---------------- CLICK SIGN IN ----------------
    wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//*[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'sign')]"
        ))
    ).click()

    # ---------------- LOGIN ----------------
    wait.until(EC.url_contains("/login"))

    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//input[@type='email']")
        )
    ).send_keys("suchini@ateamsoftware.com")

    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//input[@type='password']")
        )
    ).send_keys("Abc12345")

    wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(),'Login')]")
        )
    ).click()

    # ---------------- VERIFY DASHBOARD ----------------
    wait.until(
        EC.url_contains("/supplier/dashboard")
    )

    take_screenshot(driver, "dashboard_success")

    print("✅ Login successful")