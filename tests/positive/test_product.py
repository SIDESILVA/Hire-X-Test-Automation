import pytest
import allure

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from modules.product_module import ProductModule


@pytest.mark.smoke
@allure.title("Product + Task + Photos + Shipping Automation Flow")
def test_create_product(driver, login):

    wait = WebDriverWait(driver, 60)

    driver.get(
        "https://app-hire-x-dev-multi-tenant-angular-01-bkgee7ewapa0c5es.southeastasia-01.azurewebsites.net/supplier/products"
    )

    wait.until(
        EC.url_contains("/supplier/products")
    )

    new_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space()='New']")
        )
    )

    driver.execute_script(
        "arguments[0].click();",
        new_btn
    )

    wait.until(
        EC.visibility_of_element_located(
            (By.NAME, "name")
        )
    )

    product = ProductModule(driver)

    product.create_product(
        name="Test Product",
        desc="Created via Selenium",
        price_note="Day Rental",
        price="10",
        bond="2"
    )