from selenium.webdriver.common.by import By


class BookingPage:

    # =========================================================
    # TENANT
    # =========================================================

    TENANT_INPUT = (
        By.CSS_SELECTOR,
        "input[type='text']"
    )

    SET_TENANT_BTN = (
        By.XPATH,
        "//button[contains(text(),'Set Tenant')]"
    )

    # =========================================================
    # PRODUCT
    # =========================================================

    VIEW_BUTTONS = (
        By.XPATH,
        "//button[contains(.,'View')]"
    )

    # =========================================================
    # DATE / ORDER
    # =========================================================

    START_DATE = (
        By.NAME,
        "hireStartDate"
    )

    START_TIME = (
        By.NAME,
        "startTime"
    )

    END_DATE = (
        By.NAME,
        "hireEndDate"
    )

    END_TIME = (
        By.NAME,
        "endTime"
    )

    QUANTITY = (
        By.NAME,
        "Quantity"
    )

    REQUEST_TO_BOOK_BTN = (
        By.XPATH,
        "//button[contains(normalize-space(),'Request to Book')]"
    )

    # =========================================================
    # CART
    # =========================================================

    ADD_MORE_PRODUCTS = (
        By.XPATH,
        "//a[contains(normalize-space(),'Add More Products')]"
    )

    # =========================================================
    # BOOKING BUTTONS
    # =========================================================

    ADD_TO_BOOKING_BTN = (
        By.XPATH,
        "//button[contains(normalize-space(),'Add to Booking')]"
    )

    # =========================================================
    # SHIPPING
    # =========================================================

    SHIPPING_METHOD = (
        By.NAME,
        "shippingMethod"
    )

    # =========================================================
    # CUSTOMER
    # =========================================================

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

    # =========================================================
    # ADDRESS
    # =========================================================

    ADDRESS_BLOCKS = (
        By.XPATH,
        "//address-input"
    )

    SAME_ADDRESS_CHECKBOX = (
        By.NAME,
        "hasCustomerAndDeliveryAddressSame"
    )

    # =========================================================
    # NAVIGATION
    # =========================================================

    NEXT_BUTTON = (
        By.XPATH,
        "//button[contains(text(),'Next')]"
    )

    TERMS_CHECKBOX = (
        By.NAME,
        "hasAgreedTermsAndConditions"
    )

    # =========================================================
    # FINAL BOOKING
    # =========================================================

    FINAL_BOOK_BTN = (
        By.XPATH,
        "//button[contains(.,'Request Booking')]"
    )

    # =========================================================
    # CREDIT CARD
    # =========================================================

    CREDIT_CARD_SECTION = (
        By.XPATH,
        "//label[contains(normalize-space(),'Credit Card Details')]"
    )

    # Stripe iframe
    STRIPE_CARD_IFRAME = (
        By.CSS_SELECTOR,
        "iframe[title='Secure card payment input frame']"
    )

    # Card number
    STRIPE_CARD_NUMBER = (
        By.CSS_SELECTOR,
        "input[name='cardnumber']"
    )

    # Expiry
    STRIPE_CARD_EXPIRY = (
        By.CSS_SELECTOR,
        "input[name='exp-date']"
    )

    # CVC
    STRIPE_CARD_CVC = (
        By.CSS_SELECTOR,
        "input[name='cvc']"
    )

    # =========================================================
    # IMPORTANT:
    # Stripe ZIP field is:
    #
    # name="postal"
    #
    # NOT:
    #
    # name="postalCode"
    # =========================================================

    STRIPE_CARD_POSTAL = (
        By.CSS_SELECTOR,
        "input[name='postal']"
    )

    # =========================================================
    # OPTIONAL ALERT POPUP
    # =========================================================

    ALERT_BOX = (
        By.CSS_SELECTOR,
        "div.alert-box"
    )

    ALERT_OK_BTN = (
        By.CSS_SELECTOR,
        "div.alert-box button.btn.btn-primary"
    )

    # =========================================================
    # CLOSE MODAL
    # =========================================================

    CLOSE_MODAL = (
        By.XPATH,
        "//button[contains(.,'Close')]"
    )