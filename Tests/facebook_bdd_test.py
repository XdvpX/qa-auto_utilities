import pytest
from pytest_bdd import scenario


@scenario("../Feature/facebook/facebook_login.feature", "Login with invalid credentials")
def test_facebook_bdd():
    pass
