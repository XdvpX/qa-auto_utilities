from auto_utilities.ui_utilities import UIWaits, UIActions, BrowserActions


class FacebookPage:
    # CSS Selectors

    # Buttons

    submit_button = 'button[value="1"]'

    # Text Fields

    username_text_field = '#email'
    password_text_field = '#pass'

    # Text
    error_text = 'div._9ay7'

    # Methods

    # Setters
    @classmethod
    def enter_username(cls, value: str, index: int = 0):
        UIActions.enter_text(cls.username_text_field, value, index)

    @classmethod
    def enter_password(cls, value: str, index: int = 0):
        UIActions.enter_text(cls.password_text_field, value, index)

    # Clicks

    @classmethod
    def click_submit_button(cls):
        UIActions.click_element(cls.submit_button)

    # Getters

    @classmethod
    def get_error_text(cls):
        return UIActions.get_element_text(cls.error_text)

    # Waits

    @classmethod
    def wait_for_facebook_page_to_load(cls):
        UIWaits.wait_until_visible(cls.error_text, timeout=30)
