import pytest

from Data.login.login_data import INVALID_PASSWORD, INVALID_USER_NAME
from Data.output.output_data import ERROR_MESSAGE
from Pages.facebook_page import FacebookPage

pytestmark = [pytest.mark.Facebook, pytest.mark.regression]


def test_facebook_login_invalid_credentials():
    '''
    Configured facebook url in conftest file. If not facebook, change url in conftest file
    '''

    FacebookPage.enter_username(INVALID_USER_NAME)
    FacebookPage.enter_password(INVALID_PASSWORD)
    FacebookPage.click_submit_button()
    FacebookPage.wait_for_facebook_page_to_load()
    
    assert FacebookPage.get_error_text() == ERROR_MESSAGE
