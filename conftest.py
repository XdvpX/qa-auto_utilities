import os
import logging

import pytest

from auto_utilities.webdriver_utility import CustomWebDriverManager

logger = logging.getLogger(__name__)


@pytest.fixture(autouse=True)
def driver_init():
    # Run Before Each Session
    CustomWebDriverManager.launch_driver(browser_type='chrome')
    web_driver = CustomWebDriverManager.get_active_driver()
    web_driver.maximize_window()
    web_driver.get('https://www.facebook.com/')

    yield

    # Run After Each Session
    web_driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        if report.failed:
            logger.error(f"Test {item.name} failed!")
            
