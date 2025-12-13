from pytest_bdd import given, when, then
from Pages.facebook_page import FacebookPage
from Data.login.login_data import INVALID_PASSWORD, INVALID_USER_NAME
from Data.output.output_data import ERROR_MESSAGE


@given("I am on Facebook login page")
def open_facebook():
    pass


@when("I enter invalid username")
def enter_username():
    FacebookPage.enter_username(INVALID_USER_NAME)


@when("I enter invalid password")
def enter_password():
    FacebookPage.enter_password(INVALID_PASSWORD)


@when("I click the submit button")
def click_submit():
    FacebookPage.click_submit_button()
    FacebookPage.wait_for_facebook_page_to_load()


@then("I should see an error message")
def verify_error():
    assert FacebookPage.get_error_text() == ERROR_MESSAGE
