Feature: #Enter feature name here
  # Enter feature description here

  Scenario Outline: Adding Products to the Basket by User Login
    Given user opens homepage
    And user navigates to login page
    And user login with username and password
    And user login successfully
    And user searches a product:<product>
    And user clicks first product in search results
    When user adds product to basket from two different sellers
    And user navigates to basket page
    Then selected product added correctly
    And sellers are different
    Then user empties the basket
    And the basket is emptied
    Then user logout
    And logout is successful
    Examples:
      | product       |
      | FIFA 20       |
      | Sony Kulaklık |


  Scenario Outline: Adding Products to the Basket without User Login
    Given user opens homepage
    And user searches a product:<product>
    And user clicks first product in search results
    When user adds product to basket from two different sellers
    And user navigates to basket page
    Then selected product added correctly
    And sellers are different
    Then user empties the basket
    And the basket is emptied
    Examples:
      | product    |
      | Walkman    |
      | God Of War |

