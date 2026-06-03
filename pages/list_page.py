from selenium.webdriver.common.by import By


class ListPage:

    # ================= SIDEBAR =================
    SIDEBAR_LISTS = (
        By.XPATH,
        "//a[contains(@href,'/supplier/lists') or contains(.,'Lists')]"
    )

    # ================= BUTTONS =================
    NEW_BUTTON = (
        By.XPATH,
        "//button[@type='button' and normalize-space()='New']"
    )

    CREATE_BUTTON = (
        By.XPATH,
        "//button[@type='submit' and normalize-space()='Create']"
    )

    EMAIL_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Email']"
    )

    SEND_BUTTON = (
        By.XPATH,
        "//button[@type='submit' and contains(.,'Send')]"
    )

    SAVE_BUTTON = (
        By.XPATH,
        "//button[@type='submit' and normalize-space()='Save']"
    )

    VIEW_BUTTON = (
        By.XPATH,
        "//a[contains(@class,'btn-outline-primary') and normalize-space()='View']"
    )

    # ================= DELETE =================
    DELETE_BUTTON = (
        By.XPATH,
        "//button[@type='button' and normalize-space()='Delete']"
    )

    # ✅ YES BUTTON IN DELETE POPUP
    YES_BUTTON = (
        By.XPATH,
        "//div[contains(@class,'modal-footer')]//button[normalize-space()='Yes']"
    )

    # ================= TABLE =================
    LIST_ROWS = (
        By.XPATH,
        "//table//tbody/tr"
    )

    # ONLY ROW WHERE MEMBERS = 0
    ZERO_MEMBER_ROW = (
        By.XPATH,
        "//table//tbody/tr[td[2][normalize-space()='0']]"
    )

    # ================= INPUTS =================
    LIST_NAME = (
        By.NAME,
        "listName"
    )

    # ================= EMAIL =================
    TEMPLATE_DROPDOWN = (
        By.NAME,
        "templateId"
    )

    ATTACHMENT_INPUT = (
        By.XPATH,
        "//input[@type='file']"
    )

    # ================= MODAL =================
    MODAL_LIST_NAME_INPUT = (
        By.XPATH,
        "//input[@name='listName']"
    )

    MODAL_CREATE_BUTTON = (
        By.XPATH,
        "//div[contains(@class,'modal')]//button[@type='submit' and normalize-space()='Create']"
    )