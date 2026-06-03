from selenium.webdriver.common.by import By


class BookingPage:

    # ---------------- TENANT ----------------
    TENANT_INPUT = (By.CSS_SELECTOR, "input[type='text']")
    SET_TENANT_BTN = (By.XPATH, "//button[contains(text(),'Set Tenant')]")

    # ---------------- PRODUCT ----------------
    VIEW_BUTTONS = (By.XPATH, "//button[contains(.,'View')]")

    # ---------------- DATE / ORDER ----------------
    END_DATE = (By.NAME, "hireEndDate")
    QUANTITY = (By.NAME, "Quantity")
    REQUEST_TO_BOOK_BTN = (By.XPATH, "//button[contains(.,'Request to Book')]")

    # ---------------- SHIPPING ----------------
    SHIPPING_METHOD = (By.NAME, "shippingMethod")

    # ---------------- CUSTOMER ----------------
    EMAIL = (By.NAME, "emailAddress")
    PHONE = (By.NAME, "phoneNumber")
    FIRST_NAME = (By.NAME, "firstName")
    LAST_NAME = (By.NAME, "lastName")

    # ---------------- ADDRESS ----------------
    ADDRESS_BLOCKS = (By.XPATH, "//address-input")
    SAME_ADDRESS_CHECKBOX = (By.NAME, "hasCustomerAndDeliveryAddressSame")

    # ---------------- NAVIGATION ----------------
    NEXT_BUTTON = (By.XPATH, "//button[contains(text(),'Next')]")
    TERMS_CHECKBOX = (By.NAME, "hasAgreedTermsAndConditions")
    FINAL_BOOK_BTN = (By.XPATH, "//button[contains(.,'Request Booking')]")
    CLOSE_MODAL = (By.XPATH, "//button[contains(.,'Close')]")