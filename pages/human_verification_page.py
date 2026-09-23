from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class HumanVerificationPage:

    IFRAME = (
        By.CSS_SELECTOR,
        "iframe[src*='turnstile']"
    )

    CHECKBOX = (
        By.CSS_SELECTOR,
        "body"
    )

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def complete_turnstile(self):

        try:

            iframe = self.wait.until(
                EC.presence_of_element_located(self.IFRAME)
            )

            self.driver.switch_to.frame(iframe)

            checkbox = self.wait.until(
                EC.element_to_be_clickable(self.CHECKBOX)
            )

            checkbox.click()

            self.driver.switch_to.default_content()

            print("Turnstile clicked.")

        except Exception as e:

            self.driver.switch_to.default_content()

            print("Turnstile not completed:", e)