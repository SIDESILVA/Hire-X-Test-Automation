import time
from selenium.common.exceptions import StaleElementReferenceException


def safe_js_input(driver, element, value):
    try:
        driver.execute_script("""
            arguments[0].scrollIntoView({block:'center'});
            arguments[0].focus();
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        """, element, value)
    except StaleElementReferenceException:
        time.sleep(0.5)