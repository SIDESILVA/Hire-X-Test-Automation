from selenium.webdriver.common.by import By


class CustomerPage:

    # ==================================================
    # BUTTONS
    # ==================================================

    NEW_BUTTON = (By.XPATH, "//button[text()='New']")
    CREATE_BUTTON = (By.XPATH, "//button[text()='Create']")
    SAVE_BUTTON = (By.XPATH, "//button[text()='Save']")

    ADD_TO_LIST_BUTTON = (By.XPATH, "//a[contains(text(),'Add to List')]")

    MODAL_ADD_BUTTON = (
        By.XPATH,
        "//div[contains(@class,'modal-footer')]//button[text()='Add']"
    )

    # ➕ NEW TASK BUTTON
    NEW_TASK_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='New Task']"
    )

    # ==================================================
    # TASK SAVE BUTTON (FIXED + STABLE)
    # ==================================================

    TASK_SAVE_BUTTON = (
        By.XPATH,
        "//div[contains(@class,'modal-content')]"
        "//button[@type='submit' and contains(.,'Save')]"
    )

    # ==================================================
    # FORM FIELDS
    # ==================================================

    FIRST_NAME = (By.NAME, "firstName")
    LAST_NAME = (By.NAME, "lastName")
    EMAIL = (By.NAME, "emailAddress")
    PHONE = (By.NAME, "phoneNumber")

    ADDRESS = (By.CSS_SELECTOR, "input[autocomplete='address-line1']")
    SUBURB = (By.XPATH, "//label[normalize-space()='Suburb']/following::input[1]")
    STATE = (By.XPATH, "//label[normalize-space()='State']/following::select[1]")
    POSTCODE = (By.CSS_SELECTOR, "input[autocomplete='postal-code']")

    # ==================================================
    # ACCOUNT SECTION
    # ==================================================

    ACCOUNT_CUSTOMER_CHECKBOX = (By.ID, "AccountCustomer")

    PAYMENT_TERMS_DAYS = (
        By.XPATH,
        "//label[contains(text(),'Payment Terms')]/following::input[1]"
    )

    # ==================================================
    # CUSTOMER DETAILS
    # ==================================================

    CUSTOMER_DETAILS_CONTAINER = (By.XPATH, "//app-customer-details")

    # ==================================================
    # LIST MODAL
    # ==================================================

    CUSTOMER_LIST_DROPDOWN = (By.NAME, "customerListId")
    MODAL_CONTAINER = (By.XPATH, "//div[contains(@class,'modal-content')]")

    # ==================================================
    # ADDRESS SECTION
    # ==================================================

    ADDRESS_SECTION = (
        By.XPATH,
        "//h5[normalize-space()='Addresses']/ancestor::div[contains(@class,'card')]"
    )

    ADDRESS_EDIT_BUTTON = (
        By.XPATH,
        "//h5[normalize-space()='Addresses']/ancestor::div[contains(@class,'card')]//button[normalize-space()='Edit']"
    )

    NEW_ADDRESS_BUTTON = (By.XPATH, "//button[normalize-space()='New Address']")

    ADDRESS_DELETE_BUTTONS = (
        By.XPATH,
        "//h5[normalize-space()='Addresses']/ancestor::div[contains(@class,'card')]//button[normalize-space()='Delete']"
    )

    ADDRESS_DELETE_CONFIRM_MODAL = (
        By.XPATH,
        "//div[contains(@class,'modal-content') and .//button[normalize-space()='Yes']]"
    )

    ADDRESS_DELETE_CONFIRM_YES_BUTTON = (
        By.XPATH,
        "//div[contains(@class,'modal-content')][.//button[normalize-space()='Yes']]"
        "//button[normalize-space()='Yes']"
    )

    # ==================================================
    # ADDRESS MODAL
    # ==================================================

    ADDRESS_MODAL = (By.XPATH, "//div[contains(@class,'modal-content')]")

    ADDRESS_MODAL_SUBURB = (
        By.XPATH,
        "//div[contains(@class,'modal-content')]//label[normalize-space()='Suburb']/following::input[1]"
    )

    ADDRESS_MODAL_POSTCODE = (
        By.XPATH,
        "//div[contains(@class,'modal-content')]//input[@autocomplete='postal-code']"
    )

    ADDRESS_MODAL_SAVE_BUTTON = (
        By.XPATH,
        "//div[contains(@class,'modal-footer')]//button[normalize-space()='Save']"
    )

    # ==================================================
    # NEW ADDRESS MODAL
    # ==================================================

    NEW_ADDRESS_MODAL_ADDRESS1 = (
        By.XPATH,
        "//div[contains(@class,'modal-content')]//input[@autocomplete='address-line1']"
    )

    NEW_ADDRESS_MODAL_SUBURB = (
        By.XPATH,
        "(//div[contains(@class,'modal-content')]//label[normalize-space()='Suburb']/following::input[1])[1]"
    )

    NEW_ADDRESS_MODAL_STATE = (
        By.XPATH,
        "//div[contains(@class,'modal-content')]//label[normalize-space()='State']/following::select[1]"
    )

    NEW_ADDRESS_MODAL_POSTCODE = (
        By.XPATH,
        "//div[contains(@class,'modal-content')]//input[@autocomplete='postal-code']"
    )

    NEW_ADDRESS_MODAL_COUNTRY = (
        By.XPATH,
        "//div[contains(@class,'modal-content')]//select[@autocomplete='country']"
    )

    NEW_ADDRESS_MODAL_SAVE_BUTTON = (
        By.XPATH,
        "//div[contains(@class,'modal-footer')]//button[normalize-space()='Save']"
    )

    # ==================================================
    # PHONE SECTION
    # ==================================================

    PHONE_NUMBER_TYPE = (By.NAME, "type")
    PHONE_NUMBER_INPUT = (By.NAME, "number")

    PHONE_NUMBER_ADD_BUTTON = (
        By.XPATH,
        "//button[contains(@class,'add-button')]"
    )

    PHONE_NUMBER_DELETE_BUTTON = (
        By.XPATH,
        "//customer-phone-number-list//button[normalize-space()='Delete']"
    )

    PHONE_NUMBER_EDIT_BUTTON = (
        By.XPATH,
        "//customer-phone-number-list//button[normalize-space()='Edit']"
    )

    PHONE_NUMBER_EDIT_INPUT = (
        By.XPATH,
        "//customer-phone-number-list//input[@name='number']"
    )

    PHONE_NUMBER_SAVE_BUTTON = (
        By.XPATH,
        "//customer-phone-number-list//button[normalize-space()='Save']"
    )

    EMAIL_FORM_CONTAINER = (
        By.XPATH,
        "//emails-list//following::*[contains(@class,'modal') or contains(@class,'email')][1]"
    )

    NEW_EMAIL_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='New Email']"
    )

    EMAIL_TEMPLATE_DROPDOWN = (
        By.XPATH,
        "//select[@name='templateId']"
    )

    EMAIL_ADD_ATTACHMENT_BUTTON = (
        By.XPATH,
        "//span[contains(text(),'Add Attachments') or contains(text(),'Add Attachment')]"
    )

    EMAIL_ATTACHMENT_INPUT = (
        By.XPATH,
        "//input[@type='file']"
    )

    SEND_EMAIL_BUTTON = (
        By.XPATH,
        "//div[contains(@class,'modal-content') and not(contains(@style,'display: none'))]"
        "//button[normalize-space()='Send' and not(@disabled)]"
    )

    NEW_ORDER_BUTTON = (
        By.XPATH,
        "//h3[normalize-space()='Orders']/ancestor::div[contains(@class,'card') or contains(@class,'row')]//button[contains(@class,'btn') and normalize-space()='New Order']"
    )