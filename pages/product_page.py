from selenium.webdriver.common.by import By


class ProductPage:

    # ---------------- PRODUCT FIELDS ----------------
    NAME = (By.NAME, "name")
    SHORT_DESC = (By.NAME, "shortDescription")
    PRICE_NOTE = (By.NAME, "priceNote")
    BASE_PRICE = (By.NAME, "basePrice")
    BOND = (By.NAME, "bond")
    IMAGE_UPLOAD = (By.NAME, "inputFieldName")

    CREATE_BTN = (
        By.XPATH,
        "//button[@type='submit' and normalize-space()='Create']"
    )

    # ---------------- CATEGORY ----------------
    CATEGORY_DROPDOWN = (
        By.XPATH,
        "//button[contains(@class,'dropdown-toggle') and contains(.,'Please select')]"
    )

    MEALS_EXPAND_ICON = (
        By.XPATH,
        "//label[normalize-space()='Meals']/preceding-sibling::span"
    )

    BREAKFAST_OPTION = (
        By.XPATH,
        "//label[normalize-space()='Breakfast']"
    )

    # ---------------- POST FLOW ----------------
    FINALISE_NOW = (
        By.XPATH,
        "//a[normalize-space()='Finalise Now']"
    )

    QTY = (By.NAME, "qty")
    IS_FEATURED = (By.NAME, "isFeatured")

    SAVE_BTN = (
        By.XPATH,
        "//button[@type='submit' and normalize-space()='Save']"
    )

    # ---------------- TABS ----------------
    ORDERS_TAB = (
        By.XPATH,
        "//span[normalize-space()='Orders']"
    )

    TASKS_TAB = (
        By.XPATH,
        "//span[normalize-space()='Tasks']"
    )

    PHOTOS_TAB = (
        By.XPATH,
        "//span[normalize-space()='Photos']"
    )

    SHIPPING_TAB = (
        By.XPATH,
        "//span[normalize-space()='Shipping']"
    )

    PRICING_TAB = (
        By.XPATH,
        "//span[normalize-space()='Pricing']"
    )

    # ---------------- STOCK TAB ----------------
    STOCK_TAB = (
        By.XPATH,
        "//span[normalize-space()='Stock']"
    )

    STOCK_NEW_BTN = (
        By.XPATH,
        "//tab[contains(@class,'active')]//button[normalize-space()='New']"
    )

    # ---------------- STOCK ITEM MODAL (ADDED) ----------------
    STOCK_SKU = (
        By.NAME,
        "sku"
    )

    STOCK_SERIAL_NUMBER = (
        By.NAME,
        "serialNumber"
    )

    STOCK_BARCODE = (
        By.NAME,
        "barcode"
    )

    STOCK_VALUE = (
        By.NAME,
        "value"
    )

    STOCK_LOCATION_DROPDOWN = (
        By.NAME,
        "organisationAddressId"
    )

    STOCK_CREATE_BTN = (
        By.XPATH,
        "//div[contains(@class,'modal-footer')]//button[@type='submit']"
    )

    # ---------------- TASKS ----------------
    NEW_TASK_BTN = (
        By.XPATH,
        "//button[contains(normalize-space(),'New Task')]"
    )

    TASK_TYPE_DROPDOWN = (By.NAME, "noteTypeId")
    USER_DROPDOWN = (By.NAME, "user")

    TASK_MODAL_SAVE_BTN = (
        By.XPATH,
        "//div[contains(@class,'modal-footer')]//button[@type='submit']"
    )

    # ---------------- PHOTOS TAB ----------------
    PHOTOS_UPLOAD_INPUT = (
        By.XPATH,
        "//input[@type='file' and @name='inputFieldName']"
    )

    # ---------------- SHIPPING TAB ----------------
    SHIPPING_EDIT_BTN = (
        By.XPATH,
        "//tab[contains(@class,'active')]//button[normalize-space()='Edit']"
    )

    SHIPPING_TOGGLE = (By.NAME, "deliverableSwitch")

    SHIPPING_TOGGLE_SLIDER = (
        By.XPATH,
        "//input[@name='deliverableSwitch']/following-sibling::div[contains(@class,'slider')]"
    )

    SHIPPING_STATUS_TEXT = (
        By.XPATH,
        "//span[contains(@class,'pl-2')]"
    )

    SHIPPING_SAVE_BTN = (
        By.XPATH,
        "//tab[contains(@class,'active')]//button[normalize-space()='Save']"
    )

    # ---------------- PRICING (FORM) ----------------
    PRICING_SECURITY_DEPOSIT = (
        By.XPATH,
        "(//input[@name='bond'])[last()]"
    )

    PRICING_NOTE = (
        By.XPATH,
        "(//input[@name='priceNote'])[last()]"
    )

    PRICING_SAVE_BTN = (
        By.XPATH,
        "(//button[@type='submit' and normalize-space()='Save'])[last()]"
    )

    # ---------------- PRICING GRID ----------------
    PRICING_SECTION = (
        By.XPATH,
        "(//div[contains(@class,'grid-striped')])[last()]"
    )

    PRICING_EDIT_BTN = (
        By.XPATH,
        "(//div[contains(@class,'grid-striped')])[last()]//button[normalize-space()='Edit']"
    )

    PRICING_TOGGLE = (
        By.XPATH,
        "(//div[contains(@class,'grid-striped')])[last()]//input[@type='checkbox' and @name='customSwitch']"
    )

    PRICING_STATUS_TEXT = (
        By.XPATH,
        "(//div[contains(@class,'grid-striped')])[last()]//span[contains(@class,'pl-2')]"
    )

    PRICING_SAVE_BTN_GRID = (
        By.XPATH,
        "(//div[contains(@class,'grid-striped')])[last()]//button[contains(.,'Save')]"
    )