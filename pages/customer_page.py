from selenium.webdriver.common.by import By


class CustomerPage:

    # ---------------- BUTTONS ----------------

    NEW_BUTTON = (
        By.XPATH,
        "//button[text()='New']"
    )

    CREATE_BUTTON = (
        By.XPATH,
        "//button[text()='Create']"
    )

    # ---------------- INPUTS ----------------

    FIRST_NAME = (
        By.NAME,
        "firstName"
    )

    LAST_NAME = (
        By.NAME,
        "lastName"
    )

    EMAIL = (
        By.NAME,
        "emailAddress"
    )

    PHONE = (
        By.NAME,
        "phoneNumber"
    )

    ADDRESS = (
        By.CSS_SELECTOR,
        "input[autocomplete='address-line1']"
    )

    SUBURB = (
        By.XPATH,
        "//label[normalize-space()='Suburb']/following::input[1]"
    )

    STATE = (
        By.XPATH,
        "//label[normalize-space()='State']/following::select[1]"
    )

    POSTCODE = (
        By.CSS_SELECTOR,
        "input[autocomplete='postal-code']"
    )