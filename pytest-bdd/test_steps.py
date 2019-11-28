from pytest_bdd import scenario, scenarios, given, when, then, steps
from selenium.webdriver.common.by import By
from selenium import webdriver
import pytest
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


BASE_URL = 'https://www.hepsiburada.com'
USER_EMAIL = 'test.hepsiburada@yopmail.com'
USER_PASSWORD = 'Burada'
USER_NAME = 'Hepsi Burada'
# LOCATORS
# Login Page
LOC_EMAIL = (By.ID, 'email')
LOC_PASSWORD = (By.ID, 'password')
LOC_LOGIN_BUTTON = (By.CSS_SELECTOR, '.btn-login-submit')
# Header: MyAccount
LOC_MYACCOUNT = (By.CSS_SELECTOR, '#myAccount.icon-view-account')
LOC_LOGIN_USERNAME = (By.ID, 'login')
LOC_LOGOUT = (By.CSS_SELECTOR, '.logout')
LOC_USERNAME = (By.CSS_SELECTOR, '.usersProsess .login.user-name')
# Header: Basket
LOC_BASKET_BUTTON = (By.CSS_SELECTOR, '.icon-view-basket')
# Header: Product Search
LOC_SEARCH = (By.ID, 'productSearch')
LOC_SEARCH_BUTTON = (By.ID, 'buttonProductSearch')
# Search Results Page
LOC_PRODUCT_LIST = (By.CSS_SELECTOR, '.box.product')
# Product Details Page
LOC_OTHER_SELLERS_ADD_BASKET = (By.CSS_SELECTOR, '.add-to-basket.button.small')
# Basket Page
LOC_BASKET_CONTAINER = (By.CSS_SELECTOR, '.box.umbrella')
LOC_PRODUCT_NAME = (By.CSS_SELECTOR, '.box.umbrella .product-name .hbus')
LOC_SELLERS = (By.CSS_SELECTOR, '.box.umbrella .merchant .hbus')
LOC_DELETE_BUTTON = (By.CSS_SELECTOR, '.btn-delete.hbus')

scenarios('adding_product_to_basket.feature')

driver_type = 'chrome'  # chrome, firefox, safari, opera
if driver_type.lower() == 'chrome':
    driver_path = './drivers/chromedriver'
elif driver_type.lower() == 'firefox':
    driver_path = './drivers/geckodriver'
elif driver_type.lower() == 'opera':
    driver_path = './drivers/operadriver'


@pytest.fixture
def my_driver():
    if driver_type.lower() == 'chrome':
        browser = webdriver.Chrome(driver_path)
    elif driver_type.lower() == 'firefox':
        browser = webdriver.Firefox(executable_path=driver_path)
    elif driver_type.lower() == 'opera':
        browser = webdriver.Opera(executable_path=driver_path)
    elif driver_type.lower() == 'safari':
        driver = webdriver.Safari()
    yield browser
    browser.close()


@given("user opens homepage")
def user_opens_homepage(my_driver):
    my_driver.get(BASE_URL)
    # driver.maximize_window()
    sleep(6)


@given("user navigates to login page")
def user_navigates_to_login_page(my_driver):
    element1 = my_driver.find_element(*LOC_MYACCOUNT)
    # element3 = driver.find_element_by_css_selector('.usersProsess .login.user-name')
    action = ActionChains(my_driver)
    action.move_to_element(element1).perform()
    sleep(1)
    element2 = my_driver.find_element(*LOC_LOGIN_USERNAME)
    action.click(element2)
    action.perform()
    sleep(3)


@given("user login with username and password")
def user_login_with_username_and_password(my_driver):
    eml = my_driver.find_element(*LOC_EMAIL)
    eml.send_keys(USER_EMAIL)
    psw = my_driver.find_element(*LOC_PASSWORD)
    psw.send_keys(USER_PASSWORD)
    psw.send_keys(Keys.RETURN)
    sleep(3)


@given("user login successfully")
def user_login_successfully(my_driver):
    element = my_driver.find_element(*LOC_USERNAME)
    print(element.text)
    assert str(element.text) == USER_NAME


@given("user searches a product:<product>")
def user_searches_a_product(my_driver, product):
    elem = my_driver.find_element(*LOC_SEARCH)
    elem.send_keys(product)
    elem.send_keys(Keys.RETURN)
    sleep(5)


@given("user clicks first product in search results")
def user_clicks_first_product_in_search_results(my_driver):
    elements = my_driver.find_elements(*LOC_PRODUCT_LIST)
    elements[0].click()


@when("user adds product to basket from two different sellers")
def user_adds_product_to_basket_from_two_different_sellers(my_driver):
    elements = my_driver.find_elements(*LOC_OTHER_SELLERS_ADD_BASKET)
    elements[0].click()
    sleep(3)
    elements[1].click()
    sleep(3)


@when("user navigates to basket page")
def user_navigates_to_basket_page(my_driver):
    elem = my_driver.find_element(*LOC_BASKET_BUTTON)
    elem.click()
    sleep(3)


@then("selected product added correctly")
def selected_product_added_correctly(my_driver):
    elements = my_driver.find_elements(*LOC_PRODUCT_NAME)
    print(elements[0].text, elements[1].text)
    assert elements[0].text == elements[1].text


@then("sellers are different")
def sellers_are_different(my_driver):
    elements = my_driver.find_elements(*LOC_SELLERS)
    print(elements[0].text, elements[1].text)
    assert elements[0].text != elements[1].text


@then("user empties the basket")
def user_empties_the_basket(my_driver):
    elements = my_driver.find_elements(*LOC_DELETE_BUTTON)
    while len(elements):
        elements[0].click()
        sleep(3)
        elements = my_driver.find_elements(*LOC_DELETE_BUTTON)
    sleep(3)


@then("the basket is emptied")
def the_basket_is_emptied(my_driver):
    element = my_driver.find_elements(*LOC_PRODUCT_NAME)
    assert len(element) == 0


@then("user logout")
def user_logout(my_driver):
    element1 = my_driver.find_element(*LOC_MYACCOUNT)
    element2 = my_driver.find_element(*LOC_LOGOUT)
    action = ActionChains(my_driver)
    action.move_to_element(element1).perform()
    sleep(1)
    action.click(element2)
    action.perform()
    sleep(3)


@then("logout is successful")
def logout_is_successful(my_driver):
    element = my_driver.find_element(*LOC_USERNAME)
    assert element.text == ''
