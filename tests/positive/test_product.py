import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from modules.product_module import ProductModule


@pytest.mark.smoke
@allure.title("Product Creation with Image Rotation Upload")
def test_create_product(driver, login):

    wait = WebDriverWait(driver, 60)

    # ✅ STEP 1: Go to PRODUCTS LIST (NOT /new page)
    driver.get(
        "https://app-hire-x-dev-multi-tenant-angular-01-bkgee7ewapa0c5es.southeastasia-01.azurewebsites.net/supplier/products"
    )

    # ✅ STEP 2: Wait for Products page
    wait.until(
        EC.url_contains("/supplier/products")
    )

    # ✅ STEP 3: Click NEW button (IMPORTANT FIX)
    new_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='New']"))
    )
    driver.execute_script("arguments[0].click();", new_btn)

    # ✅ STEP 4: NOW wait for form field
    wait.until(
        EC.visibility_of_element_located((By.NAME, "name"))
    )

    # ✅ STEP 5: Continue using module
    product = ProductModule(driver)

    product.create_product(
        name="Automation Product",
        desc="Created via Selenium framework",
        price="10",
        bond="2"
    )