from selenium.webdriver.common.by import By


class ListPage:

    # ---------------- BUTTONS ----------------

    NEW_BUTTON = (
        By.XPATH,
        "//button[@type='button' and normalize-space()='New']"
    )

    CREATE_BUTTON = (
        By.XPATH,
        "//button[@type='submit' and normalize-space()='Create']"
    )

    # ---------------- INPUTS ----------------

    LIST_NAME = (
        By.NAME,
        "listName"
    )