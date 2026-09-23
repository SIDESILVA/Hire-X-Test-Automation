from selenium.webdriver.common.by import By


class OrderPage:

    # =========================================================
    # ORDER
    # =========================================================

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

    # =========================================================
    # CUSTOMER
    # =========================================================

    CUSTOMER_DROPDOWN = (
        By.XPATH,
        "//ng-select"
    )

    CUSTOMER_OPTIONS = (
        By.XPATH,
        "//div[contains(@class,'ng-option')]"
    )

    # =========================================================
    # CUSTOMER EMAIL
    # =========================================================

    CUSTOMER_EMAIL_BUTTON = (
        By.XPATH,
        "//customer-details"
        "//label[normalize-space()='Email Address']"
        "/ancestor::div[contains(@class,'form-group')][1]"
        "//a[contains(@class,'btn-secondary')][1]"
    )

    # =========================================================
    # EMAIL MODAL
    # =========================================================

    EMAIL_MODAL = (
        By.XPATH,
        "//modal-container[@role='dialog']//app-email-dialog"
    )

    EMAIL_FORM = (
        By.XPATH,
        "//modal-container[@role='dialog']"
        "//app-email-dialog"
        "//form[@name='emailForm']"
    )

    EMAIL_TEMPLATE_DROPDOWN = (
        By.XPATH,
        "//modal-container[@role='dialog']"
        "//app-email-dialog"
        "//select[@name='templateId']"
    )

    EMAIL_TEMPLATE_OPTIONS = (
        By.XPATH,
        "//modal-container[@role='dialog']"
        "//app-email-dialog"
        "//select[@name='templateId']/option"
    )

    EMAIL_ATTACHMENT_INPUT = (
        By.XPATH,
        "//modal-container[@role='dialog']"
        "//app-email-dialog"
        "//input[@type='file' and @name='inputFieldName']"
    )

    EMAIL_SEND_BUTTON = (
        By.XPATH,
        "//modal-container[@role='dialog']"
        "//app-email-dialog"
        "//button[@type='submit' and normalize-space()='Send']"
    )

    # =========================================================
    # BILLING ADDRESS
    # =========================================================

    BILLING_ADDRESS_EDIT_BUTTON = (
        By.XPATH,
        "//customer-details"
        "//label[normalize-space()='Billing Address']"
        "/following-sibling::div"
        "//button[@type='button' and normalize-space()='Edit']"
    )

    # =========================================================
    # BILLING ADDRESS EDIT MODAL
    # =========================================================

    BILLING_ADDRESS_MODAL = (
        By.XPATH,
        "//modal-container[@role='dialog']"
        "[.//form[@name='addressForm']]"
    )

    BILLING_ADDRESS_FORM = (
        By.XPATH,
        "//modal-container[@role='dialog']"
        "//form[@name='addressForm']"
    )

    # =========================================================
    # ADDRESS 1
    # =========================================================

    BILLING_ADDRESS_1_INPUT = (
        By.XPATH,
        "//modal-container[@role='dialog']"
        "//form[@name='addressForm']"
        "//label[normalize-space()='Address 1']"
        "/parent::div[contains(@class,'form-group')]"
        "//input"
    )

    # =========================================================
    # ADDRESS 2
    # =========================================================

    BILLING_ADDRESS_2_INPUT = (
        By.XPATH,
        "//modal-container[@role='dialog']"
        "//form[@name='addressForm']"
        "//label[normalize-space()='Address 2']"
        "/parent::div[contains(@class,'form-group')]"
        "//input"
    )

    # =========================================================
    # SUBURB
    # =========================================================

    BILLING_SUBURB_INPUT = (
        By.XPATH,
        "//modal-container[@role='dialog']"
        "//form[@name='addressForm']"
        "//label[normalize-space()='Suburb']"
        "/parent::div[contains(@class,'form-group')]"
        "//input"
    )

    # =========================================================
    # STATE DROPDOWN
    # =========================================================

    BILLING_STATE_DROPDOWN = (
        By.XPATH,
        "//modal-container[@role='dialog']"
        "//form[@name='addressForm']"
        "//label[normalize-space()='State']"
        "/parent::div[contains(@class,'form-group')]"
        "//select"
    )   

    # =========================================================
    # POSTCODE
    # =========================================================

    BILLING_POSTCODE_INPUT = (
        By.XPATH,
        "//modal-container[@role='dialog']"
        "//form[@name='addressForm']"
        "//label[normalize-space()='Postcode']"
        "/parent::div[contains(@class,'form-group')]"
        "//input"   
    )

    # =========================================================
    # BILLING ADDRESS SAVE BUTTON
    # =========================================================

    BILLING_ADDRESS_SAVE_BUTTON = (
        By.XPATH,
        "//modal-container[@role='dialog']"
        "[.//form[@name='addressForm']]"
        "//div[contains(@class,'modal-footer')]"
        "//button[@type='submit' and normalize-space()='Save']"
    )

    # =========================================================
    # HIRE DETAILS
    # =========================================================

    START_DATE_INPUT = (
        By.NAME,
        "startDate"
    )

    START_TIME_DROPDOWN = (
        By.NAME,
        "startTime"
    )

    END_DATE_INPUT = (
        By.NAME,
        "endDate"
    )

    END_TIME_DROPDOWN = (
        By.NAME,
        "endTime"
    )

    # =========================================================
    # PRODUCT
    # =========================================================

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

    # =========================================================
    # MODAL
    # =========================================================

    CLOSE_MODAL = (
        By.XPATH,
        "//button[@aria-label='Close']"
    )

    # =========================================================
    # LOADING
    # =========================================================

    SPINNER = (
        By.XPATH,
        "//div[contains(@class,'spinner-wrapper')]"
    )

    OVERLAY = (
        By.XPATH,
        "//div[contains(@class,'modal-backdrop')]"
    )

    # =========================================================
    # LINK ORDER
    # =========================================================

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
        "//div[contains(@class,'modal-content')]"
        "//button[normalize-space()='Yes']"
    )

    # =========================================================
    # UNLINK ORDER
    # =========================================================

    UNLINK_ORDER_BUTTON = (
        By.XPATH,
        "//a[normalize-space()='Unlink Order']"
    )

    UNLINK_ORDER_YES_BUTTON = (
        By.XPATH,
        "//div[contains(@class,'modal-dialog')]"
        "//div[contains(@class,'modal-content')]"
        "//div[contains(@class,'alert-box')]"
        "//button[normalize-space()='Yes']"
    )

    # =========================================================
    # CONSUMABLES AND CHARGES
    # =========================================================

    CONSUMABLE_TYPE_DROPDOWN = (
        By.NAME,
        "type"
    )

    CONSUMABLE_QUANTITY_INPUT = (
        By.XPATH,
        "//form[@name='addConsumableForm']"
        "//input[@name='quantity']"
    )

    CONSUMABLE_ADD_BUTTON = (
        By.XPATH,
        "//form[@name='addConsumableForm']"
        "//button[@type='submit' and normalize-space()='Add']"
    )

    # =========================================================
    # CUSTOM FEE
    # =========================================================

    CUSTOM_FEE_DESCRIPTION = (
        By.XPATH,
        "//h5[normalize-space()='Custom Fees']"
        "/following::input[@name='description'][1]"
    )

    CUSTOM_FEE_QUANTITY = (
        By.XPATH,
        "//h5[normalize-space()='Custom Fees']"
        "/following::input[@name='quantity'][1]"
    )

    CUSTOM_FEE_BASE_PRICE = (
        By.XPATH,
        "//h5[normalize-space()='Custom Fees']"
        "/following::input[@name='basePrice'][1]"
    )

    CUSTOM_FEE_ADD_BUTTON = (
        By.XPATH,
        "//h5[normalize-space()='Custom Fees']"
        "/following::button[@type='submit'][1]"
    )

    # =========================================================
    # NOTES
    # =========================================================

    NOTES_TEXTAREA = (
        By.NAME,
        "notes"
    )

    SAVE_BUTTON = (
        By.XPATH,
        "//div[contains(@class,'justify-content-end')]"
        "//button[normalize-space()='Save']"
    )

    # =========================================================
    # MARK AS QUOTED
    # =========================================================

    MARK_AS_QUOTED_BUTTON = (
        By.XPATH,
        "//button[@type='button' and normalize-space()='Mark as Quoted']"
    )

    # =========================================================
    # EDIT ORDER LINE
    # =========================================================

    PRODUCT_EDIT_BUTTON = (
        By.XPATH,
        "//div[contains(@class,'order-line-row')]"
        "//button[normalize-space()='Edit']"
    )

    PRODUCT_EDIT_CONTAINER = (
        By.XPATH,
        "//form | //div[contains(@class,'order-line-row')]"
    )

    PRODUCT_QUANTITY_INPUT = (
        By.XPATH,
        "//input[@name='quantity']"
    )

    PRODUCT_BASE_PRICE_INPUT = (
        By.XPATH,
        "//input[@name='basePriceOverride']"
    )

    PRODUCT_SAVE_BUTTON = (
        By.XPATH,
        "//button[contains(.,'Save')]"
    )

    # =========================================================
    # DELETE PRODUCT LINE
    # =========================================================

    PRODUCT_DELETE_BUTTONS = (
        By.XPATH,
        "//div[contains(@class,'order-line-row')]"
        "//button[normalize-space()='Delete']"
    )

    DELETE_CONFIRM_YES_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Yes']"
    )

    # =========================================================
    # EDIT CONSUMABLE
    # =========================================================

    CONSUMABLE_EDIT_BUTTON = (
        By.XPATH,
        "//order-fees-list//button[normalize-space()='Edit'][1]"
    )

    CONSUMABLE_EDIT_TYPE = (
        By.XPATH,
        "//order-fees-list//select[@name='type']"
    )

    CONSUMABLE_EDIT_QUANTITY = (
        By.XPATH,
        "//order-fees-list//input[@name='quantity']"
    )

    CONSUMABLE_EDIT_BASE_PRICE = (
        By.XPATH,
        "//order-fees-list//input[@name='basePrice']"
    )

    CONSUMABLE_SAVE_BUTTON = (
        By.XPATH,
        "//order-fees-list"
        "//button[@type='submit' and normalize-space()='Save']"
    )

    # =========================================================
    # CHANGE STATUS TO ACCEPTED
    # =========================================================

    STATUS_DROPDOWN = (
        By.XPATH,
        "//button[contains(@class,'dropdown-toggle') "
        "and contains(normalize-space(),'Quoted')]"
    )

    ACCEPTED_OPTION = (
        By.XPATH,
        "//a[normalize-space()='Accepted'] "
        "| //button[normalize-space()='Accepted']"
    )

    ACCEPT_YES_BUTTON = (
        By.XPATH,
        "//app-order-quoted-dialog"
        "//button[@type='submit' and normalize-space()='Yes']"
    )

    # =========================================================
    # PAYMENT MODAL
    # =========================================================

    PAYMENT_MODAL = (
        By.XPATH,
        "//app-order-payment-dialog"
    )

    PAYMENT_TYPE_DROPDOWN = (
        By.XPATH,
        "//app-order-payment-dialog"
        "//select[@name='type']"
    )

    PAYMENT_DATE_INPUT = (
        By.XPATH,
        "//app-order-payment-dialog"
        "//input[@name='orderPayment']"
    )

    PAYMENT_AMOUNT_INPUT = (
        By.XPATH,
        "//app-order-payment-dialog"
        "//input[@name='paymentAmt']"
    )

    PAYMENT_REFERENCE_INPUT = (
        By.XPATH,
        "//app-order-payment-dialog"
        "//input[@name='reference']"
    )

    PAYMENT_CREATE_BUTTON = (
        By.XPATH,
        "//app-order-payment-dialog"
        "//button[@type='submit' and normalize-space()='Create']"
    )

    # =========================================================
    # RECORD PAYMENT
    # =========================================================

    RECORD_PAYMENT_BUTTON = (
        By.XPATH,
        "//order-payments-list"
        "//button[normalize-space()='Record Payment Details']"
    )

    RECORD_PAYMENT_MODAL = (
        By.XPATH,
        "//app-order-payment-dialog"
    )

    RECORD_PAYMENT_TYPE_DROPDOWN = (
        By.XPATH,
        "//app-order-payment-dialog"
        "//select[@name='type']"
    )

    RECORD_PAYMENT_CREATE_BUTTON = (
        By.XPATH,
        "//app-order-payment-dialog"
        "//button[@type='submit' and normalize-space()='Create']"
    )

    INVOICE_RECORDS_SECTION = (
        By.XPATH,
        "//div[contains(@class,'panel-title')]"
        "//button[@accordion-heading]"
        "[.//div[normalize-space()='Invoice Records']]"
    )

    CREATE_INVOICE_BUTTON = (
        By.XPATH,
        "//order-invoices-list"
        "//button[normalize-space()='Create Invoice']"
    )

    # =========================================================
    # INVOICE MODAL
    # =========================================================

    INVOICE_MODAL = (
        By.XPATH,
        "//app-order-invoice-dialog"
    )

    INVOICE_CREATE_BUTTON = (
        By.XPATH,
        "//app-order-invoice-dialog"
        "//form[@name='form']"
        "//button[@type='submit' and normalize-space()='Create']"
    )

        # =========================================================
    # CHANGE STATUS TO ON-HIRE
    # =========================================================

    ON_HIRE_STATUS_DROPDOWN = (
        By.XPATH,
        "//button[contains(@class,'dropdown-toggle') "
        "and contains(normalize-space(),'Accepted')]"
    )

    ON_HIRE_OPTION = (
        By.XPATH,
        "//a[normalize-space()='On-Hire']"
        " | //button[normalize-space()='On-Hire']"
    )

    # =========================================================
    # ATTACHMENTS
    # =========================================================

    ATTACHMENTS_SECTION = (
        By.XPATH,
        "//div[contains(@class,'panel-title')]"
        "//button[@accordion-heading]"
        "[.//div[normalize-space()='Attachments']]"
    )

    UPLOAD_FILES_BUTTON = (
        By.XPATH,
        "//order-attachments-list"
        "//file-uploader"
        "//span[contains(@class,'btn-file')"
        " and normalize-space()='Upload Files']"
    )

    ATTACHMENT_FILE_INPUT = (
        By.XPATH,
        "//order-attachments-list"
        "//file-uploader"
        "//input[@type='file' and @name='inputFieldName']"
    )

    # =========================================================
    # DOCUMENTS
    # =========================================================

    DOCUMENTS_SECTION = (
        By.XPATH,
        "//div[contains(@class,'panel-title')]"
        "//button[@accordion-heading]"
        "[.//div[normalize-space()='Documents']]"
    )

    ORDER_DETAILS_DOWNLOAD = (
        By.XPATH,
        "//order-documents-list"
        "//li[.//h5[normalize-space()='Order Details']]"
        "//i[contains(@class,'fa-download')]"
    )

    TERMS_CONDITIONS_DOWNLOAD = (
        By.XPATH,
        "//order-documents-list"
        "//li[.//h5[normalize-space()='Terms and Conditions']]"
        "//i[contains(@class,'fa-download')]"
    )

    EMAIL_DOCUMENTS_BUTTON = (
        By.XPATH,
        "//order-documents-list"
        "//button[normalize-space()='Email Documents']"
    )

    EMAIL_DOCUMENTS_MODAL = (
        By.XPATH,
        "//modal-container[@role='dialog']"
        "//app-email-dialog"
    )

    EMAIL_DOCUMENTS_TEMPLATE_DROPDOWN = (
        By.XPATH,
        "//modal-container[@role='dialog']"
        "//app-email-dialog"
        "//select[@name='templateId']"
    )

    EMAIL_DOCUMENTS_ATTACHMENT_INPUT = (
        By.XPATH,
        "//modal-container[@role='dialog']"
        "//app-email-dialog"
        "//input[@type='file' and @name='inputFieldName']"
    )

    EMAIL_DOCUMENTS_SEND_BUTTON = (
        By.XPATH,
        "//modal-container[@role='dialog']"
        "//app-email-dialog"
        "//button[@type='submit' and normalize-space()='Send']"
    )

    # =========================================================
    # EMAILS
    # =========================================================

    EMAILS_SECTION = (
        By.XPATH,
        "//div[contains(@class,'panel-title')]"
        "//button[@accordion-heading]"
        "[.//div[normalize-space()='Emails']]"
    )

    NEW_EMAIL_BUTTON = (
        By.XPATH,
        "//emails-list"
        "//button[normalize-space()='New Email']"
    )

    # =========================================================
    # NEW EMAIL MODAL
    # =========================================================

    NEW_EMAIL_MODAL = (
        By.XPATH,
        "//modal-container[@role='dialog']"
        "//app-email-dialog"
    )

    NEW_EMAIL_TEMPLATE_DROPDOWN = (
        By.XPATH,
        "//modal-container[@role='dialog']"
        "//app-email-dialog"
        "//select[@name='templateId']"
    )

    NEW_EMAIL_ATTACHMENT_INPUT = (
        By.XPATH,
        "//modal-container[@role='dialog']"
        "//app-email-dialog"
        "//input[@type='file' and @name='inputFieldName']"
    )

    NEW_EMAIL_SEND_BUTTON = (
        By.XPATH,
        "//modal-container[@role='dialog']"
        "//app-email-dialog"
        "//button[@type='submit' and normalize-space()='Send']"
    )

    NEW_TASK_BUTTON = (
        By.XPATH,
        "//notes-list//button[normalize-space()='New Task']"
    )

    # =========================================================
    # NEW TASKS MODAL
    # =========================================================

    TASK_MODAL = (
        By.XPATH,
        "//modal-container[@role='dialog']//app-note-dialog"
    )

    TASK_TYPE_DROPDOWN = (
        By.XPATH,
        "//modal-container[@role='dialog']//app-note-dialog"
        "//select[@name='noteTypeId']"
    )

    TASK_DUE_DATE_INPUT = (
        By.XPATH,
        "//modal-container[@role='dialog']//app-note-dialog"
        "//input[@name='dueDate']"
    )

    TASK_USER_DROPDOWN = (
        By.XPATH,
        "//modal-container[@role='dialog']//app-note-dialog"
        "//select[@name='user']"
    )

    TASK_SAVE_BUTTON = (
        By.XPATH,
        "//modal-container[@role='dialog']//app-note-dialog"
        "//button[@type='submit' and normalize-space()='Save']"
    )

    TASK_SPINNER = (
        By.XPATH,
        "//div[contains(@class,'spinner-wrapper')]"
    )

    # ---------------- Status Change ----------------

    ON_HIRE_STATUS_DROPDOWN = (
        By.XPATH,
        "//div[contains(@class,'card')]"
        "[.//h5[normalize-space()='Hire Details']]"
        "//button[contains(@class,'dropdown-toggle')]"
    )

    RETURNED_OPTION = (
        By.XPATH,
        "//ul[contains(@class,'dropdown-menu')]"
        "//a[normalize-space()='Returned']"
    )

    INVOICED_COMPLETED_OPTION = (
        By.XPATH,
        "//ul[contains(@class,'dropdown-menu')]"
        "//a[normalize-space()='Invoiced and Completed']"
    )

    CANCELLED_OPTION = (
        By.XPATH,
        "//ul[contains(@class,'dropdown-menu')]"
        "//a[normalize-space()='Cancelled']"
    )

    CANCELLATION_MODAL = (
        By.XPATH,
        "//modal-container[@role='dialog']"
        "//form[@name='orderCancelForm']"
    )

    CANCELLATION_REASON_DROPDOWN = (
        By.XPATH,
        "//modal-container[@role='dialog']"
        "//form[@name='orderCancelForm']"
        "//select[@name='cancelReason']"
    )

    SAVE_CANCEL_ORDER_BUTTON = (
        By.XPATH,
        "//modal-container[@role='dialog']"
        "//form[@name='orderCancelForm']"
        "//button[@type='submit' and normalize-space()='Save and cancel this order']"
    )