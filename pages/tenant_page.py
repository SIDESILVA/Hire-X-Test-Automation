from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TenantPage:

    TENANT_INPUT = (By.CSS_SELECTOR, "input[type='text']")
    SET_TENANT_BTN = (By.XPATH, "//button[contains(text(),'Set Tenant')]")
    SIGN_IN_BTN = (By.XPATH,
        "//*[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'sign')]"
    )

    # spinner locator (NEW)
    SPINNER = (By.CLASS_NAME, "spinner-wrapper")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def open(self, url):
        self.driver.get(url)

    def wait_for_loader_to_disappear(self):
        try:
            self.wait.until(
                EC.invisibility_of_element_located(self.SPINNER)
            )
        except:
            pass

    def set_tenant(self, tenant_name):
        input_box = self.wait.until(
            EC.visibility_of_element_located(self.TENANT_INPUT)
        )
        input_box.clear()
        input_box.send_keys(tenant_name)

        self.wait.until(
            EC.element_to_be_clickable(self.SET_TENANT_BTN)
        ).click()

    def click_sign_in(self):
        
        self.wait_for_loader_to_disappear()

        self.wait.until(
            EC.element_to_be_clickable(self.SIGN_IN_BTN)
        ).click()