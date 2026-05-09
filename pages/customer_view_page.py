from selenium.webdriver.common.by import By


class CustomerViewPage:

    # ---------------- TENANT ----------------

    TENANT_INPUT = (
        By.CSS_SELECTOR,
        "input[type='text']"
    )

    SET_TENANT_BUTTON = (
        By.XPATH,
        "//button[contains(text(),'Set Tenant')]"
    )

    # ---------------- PRODUCT ----------------

    VIEW_BUTTONS = (
        By.XPATH,
        "//button[contains(.,'View')]"
    )

    # ---------------- BOOKING ----------------

    HIRE_END_DATE = (
        By.NAME,
        "hireEndDate"
    )

    QUANTITY = (
        By.NAME,
        "Quantity"
    )

    REQUEST_TO_BOOK_BUTTON = (
        By.XPATH,
        "//button[contains(.,'Request to Book')]"
    )

    SHIPPING_METHOD = (
        By.NAME,
        "shippingMethod"
    )

    SPINNER = (
        By.CLASS_NAME,
        "spinner-wrapper"
    )

    # ---------------- CUSTOMER ----------------

    EMAIL = (
        By.NAME,
        "emailAddress"
    )

    PHONE = (
        By.NAME,
        "phoneNumber"
    )

    FIRST_NAME = (
        By.NAME,
        "firstName"
    )

    LAST_NAME = (
        By.NAME,
        "lastName"
    )

    # ---------------- ADDRESS ----------------

    ADDRESS_BLOCKS = (
        By.XPATH,
        "//address-input"
    )

    SAME_ADDRESS_CHECKBOX = (
        By.NAME,
        "hasCustomerAndDeliveryAddressSame"
    )

    # ---------------- FLOW ----------------

    NEXT_BUTTON = (
        By.XPATH,
        "//button[contains(text(),'Next')]"
    )

    ORDER_SUMMARY = (
        By.XPATH,
        "//h5[contains(text(),'Order Summary')]"
    )

    TERMS_CHECKBOX = (
        By.NAME,
        "hasAgreedTermsAndConditions"
    )

    REQUEST_BOOKING_BUTTON = (
        By.XPATH,
        "//button[contains(.,'Request Booking')]"
    )

    # ---------------- MODAL ----------------

    MODAL_FOOTER = (
        By.CLASS_NAME,
        "modal-footer"
    )

    CLOSE_BUTTON = (
        By.XPATH,
        "//div[contains(@class,'modal-footer')]//button[contains(.,'Close')]"
    )