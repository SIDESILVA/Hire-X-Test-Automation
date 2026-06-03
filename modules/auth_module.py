from pages.tenant_page import TenantPage
from pages.login_page import LoginPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.delay_helper import slow_down


class AuthModule:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

        self.tenant_page = TenantPage(driver)
        self.login_page = LoginPage(driver)

    def login(self, url, tenant, username, password, expect_success=True):

        self.driver.get(url)
        slow_down()

        self.tenant_page.wait_for_loader_to_disappear()
        slow_down()

        self.tenant_page.set_tenant(tenant)
        slow_down()

        self.tenant_page.click_sign_in()
        slow_down()

        self.wait.until(EC.url_contains("/login"))

        self.login_page.login(username, password)
        slow_down()

        if expect_success:
            self.wait.until(EC.url_contains("/supplier/dashboard"))
        else:
            try:
                self.wait.until(EC.url_contains("/supplier/dashboard"))
            except:
                pass