from selenium.webdriver.common.by import By


class CompanyDetailsPage:

    # ======================================================
    # SIDEBAR - COMPANY DETAILS
    # ======================================================
    COMPANY_DETAILS_SIDEBAR = (
        By.XPATH,
        "//a[contains(@href,'/supplier/details')]"
    )

    # ======================================================
    # ABN
    # ======================================================
    ABN_INPUT = (
        By.XPATH,
        "//input[@type='text' "
        "and @inputmode='numeric' "
        "and @required "
        "and contains(@pattern,'11')]"
    )

    # ======================================================
    # REGISTERED FOR GST
    # ======================================================
    REGISTERED_FOR_GST_SELECT = (
        By.XPATH,
        "//label[contains(normalize-space(.),'Registered for GST')]"
        "/ancestor::div[contains(@class,'form-group')][1]"
        "//select"
    )

    # ======================================================
    # BUSINESS TYPE
    # ======================================================
    BUSINESS_TYPE_SELECT = (
        By.XPATH,
        "//label[contains(normalize-space(.),'Business Type')]"
        "/ancestor::div[contains(@class,'form-group')][1]"
        "//select"
    )

    # ======================================================
    # COMPANY DETAILS SAVE
    # ======================================================
    SAVE_BUTTON = (
        By.XPATH,
        "//button[@type='submit' and normalize-space()='Save']"
    )

    # ======================================================
    # ORGANISATION ADDRESS - EDIT
    # ======================================================
    ORGANISATION_ADDRESS_EDIT_BUTTON = (
        By.XPATH,
        "//organisation-addresses-list"
        "//button[normalize-space()='Edit']"
    )

    # ======================================================
    # ADDRESS MODAL
    # ======================================================
    ADDRESS_MODAL = (
        By.XPATH,
        "//div[contains(@class,'modal-dialog')]"
        "[.//form[@name='addressForm']]"
    )

    # ======================================================
    # EXISTING ADDRESS - ADDRESS 1
    # ======================================================
    ADDRESS_1_INPUT = (
        By.XPATH,
        "//form[@name='addressForm']"
        "//label[contains(normalize-space(.),'Address 1')]"
        "/ancestor::div[contains(@class,'form-group')][1]"
        "//input[@autocomplete='address-line1']"
    )

    # ======================================================
    # EXISTING ADDRESS - ADDRESS 2
    # ======================================================
    ADDRESS_2_INPUT = (
        By.XPATH,
        "//form[@name='addressForm']"
        "//label[contains(normalize-space(.),'Address 2')]"
        "/ancestor::div[contains(@class,'form-group')][1]"
        "//input[@autocomplete='address-line2']"
    )

    # ======================================================
    # EXISTING ADDRESS - SUBURB
    # ======================================================
    SUBURB_INPUT = (
        By.XPATH,
        "//form[@name='addressForm']"
        "//label[contains(normalize-space(.),'Suburb')]"
        "/ancestor::div[contains(@class,'form-group')][1]"
        "//input"
    )

    # ======================================================
    # EXISTING ADDRESS - STATE
    # ======================================================
    STATE_SELECT = (
        By.XPATH,
        "//form[@name='addressForm']"
        "//label[contains(normalize-space(.),'State')]"
        "/ancestor::div[contains(@class,'form-group')][1]"
        "//select"
    )

    # ======================================================
    # EXISTING ADDRESS - POSTCODE
    # ======================================================
    POSTCODE_INPUT = (
        By.XPATH,
        "//form[@name='addressForm']"
        "//label[contains(normalize-space(.),'Postcode')]"
        "/ancestor::div[contains(@class,'form-group')][1]"
        "//input[@autocomplete='postal-code']"
    )

    # ======================================================
    # EXISTING ADDRESS - SAVE
    # ======================================================
    ADDRESS_MODAL_SAVE_BUTTON = (
        By.XPATH,
        "//div[contains(@class,'modal-dialog')]"
        "[.//form[@name='addressForm']]"
        "//div[contains(@class,'modal-footer')]"
        "//button[@type='submit' and normalize-space()='Save']"
    )

    # ======================================================
    # NEW ADDRESS BUTTON
    # ======================================================
    NEW_ADDRESS_BUTTON = (
        By.XPATH,
        "//organisation-addresses-list"
        "//button[normalize-space()='New Address']"
    )

    # ======================================================
    # NEW ADDRESS - ADDRESS
    #
    # New Address modal uses:
    # <input autocomplete="address-line1">
    #
    # This is different from the Edit Address modal where
    # the label is "Address 1".
    # ======================================================
    NEW_ADDRESS_INPUT = (
        By.XPATH,
        "//form[@name='addressForm']"
        "//input[@autocomplete='address-line1']"
    )

    # ======================================================
    # NEW ADDRESS - ADDRESS 2
    # ======================================================
    NEW_ADDRESS_2_INPUT = (
        By.XPATH,
        "//form[@name='addressForm']"
        "//input[@autocomplete='address-line2']"
    )

    # ======================================================
    # NEW ADDRESS - SUBURB
    # ======================================================
    NEW_SUBURB_INPUT = (
        By.XPATH,
        "//form[@name='addressForm']"
        "//label[contains(normalize-space(.),'Suburb')]"
        "/ancestor::div[contains(@class,'form-group')][1]"
        "//input"
    )

    # ======================================================
    # NEW ADDRESS - STATE
    # ======================================================
    NEW_STATE_SELECT = (
        By.XPATH,
        "//form[@name='addressForm']"
        "//label[contains(normalize-space(.),'State')]"
        "/ancestor::div[contains(@class,'form-group')][1]"
        "//select"
    )

    # ======================================================
    # NEW ADDRESS - POSTCODE
    # ======================================================
    NEW_POSTCODE_INPUT = (
        By.XPATH,
        "//form[@name='addressForm']"
        "//input[@autocomplete='postal-code']"
    )

    # ======================================================
    # NEW ADDRESS - SAVE
    # ======================================================
    NEW_ADDRESS_SAVE_BUTTON = (
        By.XPATH,
        "//div[contains(@class,'modal-dialog')]"
        "[.//form[@name='addressForm']]"
        "//div[contains(@class,'modal-footer')]"
        "//button[@type='submit' and normalize-space()='Save']"
    )

    MAKE_PRIMARY_BUTTONS = (
        By.XPATH,
        "//organisation-addresses-list"
        "//button[normalize-space()='Make Primary']"
    )

    DELETE_ADDRESS_BUTTONS = (
        By.XPATH,
        "//organisation-addresses-list"
        "//button[normalize-space()='Delete']"
    )

    DELETE_CONFIRM_YES_BUTTON = (
        By.XPATH,
        "//div[contains(@class,'modal-dialog')]"
        "[.//div[contains(@class,'alert-box')]]"
        "//div[contains(@class,'modal-footer')]"
        "//button[@type='button' and normalize-space()='Yes']"
    )

    WEBSHOP_EXPAND_ARROW = (
        By.XPATH,
        "//table[contains(@class,'subscription-feature-table')]"
        "//th[contains(@class,'description-col-fixed-width')]"
        "//i[contains(@class,'fa-chevron-right')]"
    )

    EXPLORE_ALL_SUBSCRIPTIONS_BUTTON = (
        By.XPATH,
        "//app-company-feature-subscribes"
        "//button[contains(@class,'subscription-plan-card__details-button')]"
        "[contains(normalize-space(.),'Explore All Subscriptions')]"
    )

    SUBSCRIPTION_DETAILS_MODAL = (
        By.XPATH,
        "//div[contains(@class,'modal-dialog') "
        "and contains(@class,'modal-lg')]"
        "[.//app-company-subscription-details]"
    )

    SUBSCRIPTION_DETAILS_CLOSE_BUTTON = (
        By.XPATH,
        "//div[contains(@class,'modal-dialog') "
        "and contains(@class,'modal-lg')]"
        "[.//app-company-subscription-details]"
        "//button[contains(@class,'close')]"
    )

    CHANGE_SUBSCRIPTION_SELECT = (
        By.ID,
        "upgradePlanId"
    )

    CHANGE_SUBSCRIPTION_BUTTON = (
        By.XPATH,
        "//app-company-feature-subscribes"
        "//button[contains(@class,'subscription-plan-card__upgrade-button') "
        "and normalize-space()='Change Subscription']"
    )

    CONFIRM_CHANGE_SUBSCRIPTION_BUTTON = (
        By.XPATH,
        "//div[contains(@class,'modal-dialog')]"
        "[.//app-confirm-change-subscription-dialog]"
        "//button[@type='button' and normalize-space()='Confirm']"
    )

    BILLING_PORTAL_BUTTON = (
        By.XPATH,
        "//app-company-feature-subscribes"
        "//button[contains(@class,'subscription-plan-card__details-button') "
        "and normalize-space()='Billing Portal']"
    )