import pytest
import allure

from modules.task_module import TaskModule
from utils.screenshot import take_screenshot


@pytest.mark.smoke
@allure.title("TC03 - Create Task")
def test_create_task(driver, login):

    task = TaskModule(driver)

    with allure.step("Open Tasks Page"):

        task.open_tasks(
            "https://app-hire-x-dev-multi-tenant-angular-01-bkgee7ewapa0c5es.southeastasia-01.azurewebsites.net/supplier/tasks"
        )

    with allure.step("Create New Task"):

        task.click_new_task()

        task.select_rotating_task_type()

        task.select_rotating_user()

        task.click_create()

    take_screenshot(driver, "task_created")