import pytest
import allure

from modules import company_details_module
from modules import company_details_module
from modules.company_details_module import CompanyDetailsModule


@pytest.mark.regression
@allure.title(
    "Company Details - Update Company and Organisation Address"
)
def test_open_company_details(driver, login):

    company_details_module = CompanyDetailsModule(driver)

    # ======================================================
    # STEP 1 - OPEN COMPANY DETAILS
    # ======================================================
    company_details_module.open_company_details()

    # ======================================================
    # STEP 2 - CHANGE ABN
    # ======================================================
    company_details_module.change_abn()

    # ======================================================
    # STEP 3 - TOGGLE REGISTERED FOR GST
    # ======================================================
    company_details_module.toggle_registered_for_gst()

    # ======================================================
    # STEP 4 - SELECT BUSINESS TYPE
    # ======================================================
    company_details_module.select_business_type()

    # ======================================================
    # STEP 5 - SAVE COMPANY DETAILS
    # ======================================================
    company_details_module.save_company_details()

    # ======================================================
    # STEP 6 - CLICK ORGANISATION ADDRESS EDIT
    # ======================================================
    company_details_module.click_organisation_address_edit()

    # ======================================================
    # STEP 7 - UPDATE ORGANISATION ADDRESS
    # ======================================================
    company_details_module.update_organisation_address()

    # ======================================================
    # STEP 8 - SAVE ORGANISATION ADDRESS
    # ======================================================
    company_details_module.save_organisation_address()

    # ======================================================
    # STEP 9 - CLICK NEW ADDRESS
    # ======================================================
    company_details_module.click_new_address()

    # ======================================================
    # STEP 10 - FILL NEW ADDRESS FORM
    # ======================================================
    company_details_module.fill_new_address()

    # ======================================================
    # STEP 11 - SAVE NEW ADDRESS
    # ======================================================
    company_details_module.save_new_address()

    # --------------------------------------------------
    # MAKE PRIMARY
    # --------------------------------------------------
    company_details_module.click_make_primary_randomly()

    # ======================================================
    # FINAL SUCCESS
    # ======================================================
    print(
        "✅ SUCCESS: Company Details and "
        "Organisation Address updated successfully"
    )

    # --------------------------------------------------
    # DELETE RANDOM ADDRESS
    # --------------------------------------------------
    company_details_module.delete_random_organisation_address()

    print(
        "✅ SUCCESS: Company Details updated, "
        "address updated, new address added, "
        "random address made primary, and "
        "random address deleted successfully"
    )

    company_details_module.save_company_details()

    company_details_module.expand_webshop_table()

    company_details_module.explore_all_subscriptions_and_close()

    company_details_module.change_subscription_randomly()

    company_details_module.click_billing_portal()
