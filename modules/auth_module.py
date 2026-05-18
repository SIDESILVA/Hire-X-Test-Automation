from pages.tenant_page import TenantPage
from pages.login_page import LoginPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AuthModule:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

        self.tenant_page = TenantPage(driver)
        self.login_page = LoginPage(driver)

    # ---------------- NORMAL LOGIN ----------------
    def login(self, url, tenant, username, password, expect_success=True):

        self.driver.get(url)

        self.tenant_page.wait_for_loader_to_disappear()
        self.tenant_page.set_tenant(tenant)
        self.tenant_page.click_sign_in()

        self.wait.until(EC.url_contains("/login"))

        self.login_page.login(username, password)

        # ---------------- CONDITIONAL CHECK ----------------
        if expect_success:
            self.wait.until(EC.url_contains("/supplier/dashboard"))
        else:
            # small wait to allow error message / stay on page
            try:
                self.wait.until(EC.url_contains("/supplier/dashboard"))
            except:
                pass