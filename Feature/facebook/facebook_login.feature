Feature: Facebook Login

  Scenario: Login with invalid credentials
    Given I am on Facebook login page
    When I enter invalid username
    And I enter invalid password
    And I click the submit button
    Then I should see an error message
