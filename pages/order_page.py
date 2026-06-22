from selenium.webdriver.common.by import By


class OrderPage:

    # Order
    NEW_ORDER_BTN = (
        By.XPATH,
        "//button[contains(text(),'New')]"
    )

    CREATE_BTN = (
        By.XPATH,
        "//button[@type='submit' and normalize-space()='Create']"
    )

    CREATE_TEXT = (
        By.XPATH,
        "//*[contains(text(),'Create Order')]"
    )

    # Customer
    CUSTOMER_DROPDOWN = (
        By.XPATH,
        "//ng-select"
    )

    CUSTOMER_OPTIONS = (
        By.XPATH,
        "//div[contains(@class,'ng-option')]"
    )

    # Hire Details
    END_DATE_INPUT = (
        By.NAME,
        "endDate"
    )

    # Product
    PRODUCT_INPUT = (
        By.NAME,
        "productLookup"
    )

    PRODUCT_OPTIONS = (
        By.XPATH,
        "//typeahead-container//button[1]"
    )

    QUANTITY_INPUT = (
        By.NAME,
        "quantity"
    )

    ADD_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Add']"
    )

    # Modal
    CLOSE_MODAL = (
        By.XPATH,
        "//button[@aria-label='Close']"
    )

    # Loading
    SPINNER = (
        By.XPATH,
        "//div[contains(@class,'spinner-wrapper')]"
    )

    OVERLAY = (
        By.XPATH,
        "//div[contains(@class,'modal-backdrop')]"
    )

        # Link Order
    LINK_ORDER_DROPDOWN = (
        By.NAME,
        "linkcustomerOrder"
    )

    LINK_ORDER_OPTIONS = (
        By.XPATH,
        "//select[@name='linkcustomerOrder']/option"
    )

    LINK_ORDER_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Link Order']"
    )

    LINK_ORDER_YES_BUTTON = (
        By.XPATH,
        "//div[contains(@class,'modal-content')]//button[normalize-space()='Yes']"
    )