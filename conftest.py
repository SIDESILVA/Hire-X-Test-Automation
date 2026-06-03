import pytest
import os
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from modules.auth_module import AuthModule
from dotenv import load_dotenv

from modules.auth_module import AuthModule

# Load environment variables
load_dotenv()


# ---------------------------
# DRIVER FIXTURE
# ---------------------------
@pytest.fixture(scope="session")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    yield driver
    driver.quit()


# ---------------------------
# LOGIN FIXTURE (MODULE BASED)
# ---------------------------
@pytest.fixture(scope="session")
def login(driver):

    auth = AuthModule(driver)

    auth.login(
        url="https://app-hire-x-dev-multi-tenant-angular-01-bkgee7ewapa0c5es.southeastasia-01.azurewebsites.net/webshopnotfound",
        tenant="MetroHaven",
        username="himasha1@gmail.com",
        password="Abc12345"
    )

    print("✅ Login completed via AuthModule")


# ---------------------------
# GLOBAL FAILURE SCREENSHOT HOOK
# ---------------------------
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver", None)

        if driver:
            os.makedirs("reports", exist_ok=True)
            file_name = f"reports/{item.name}_failure.png"

            driver.save_screenshot(file_name)

            allure.attach.file(
                file_name,
                name="Failure Screenshot",
                attachment_type=allure.attachment_type.PNG
            )

    