from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import pytest

driver_type = 'chrome'  # chrome, firefox, safari, opera
if driver_type.lower() == 'chrome':
    driver_path = './drivers/chromedriver'
elif driver_type.lower() == 'firefox':
    driver_path = './drivers/geckodriver'
elif driver_type.lower() == 'opera':
    driver_path = './drivers/operadriver'

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


def open_page(my_driver, url):
    my_driver.get(url)
    my_driver.maximize_window()
    sleep(6)


def navigate_to_login_page(my_driver):
    element1 = my_driver.find_element(*LOC_MYACCOUNT)
    action = ActionChains(my_driver)
    action.move_to_element(element1).perform()
    sleep(1)
    element2 = my_driver.find_element(*LOC_LOGIN_USERNAME)
    action.click(element2)
    action.perform()
    sleep(3)


def login_with(my_driver, email, password):
    eml = my_driver.find_element(*LOC_EMAIL)
    eml.send_keys(email)
    psw = my_driver.find_element(*LOC_PASSWORD)
    psw.send_keys(password)
    psw.send_keys(Keys.RETURN)
    sleep(3)


def validate_that_login_is_successful(my_driver):
    element = my_driver.find_element(*LOC_USERNAME)
    print(element.text)
    assert str(element.text) == USER_NAME


def search_a_product(my_driver, term):
    elem = my_driver.find_element(*LOC_SEARCH)
    elem.send_keys(term)
    elem.send_keys(Keys.RETURN)
    sleep(5)


def click_first_product_in_search_results(my_driver):
    elements = my_driver.find_elements(*LOC_PRODUCT_LIST)
    elements[0].click()


def add_product_to_basket_from_two_different_sellers(my_driver):
    elements = my_driver.find_elements(*LOC_OTHER_SELLERS_ADD_BASKET)
    elements[1].click()
    sleep(5)
    elements[0].click()
    sleep(3)


def navigate_to_basket_page(my_driver):
    elem = my_driver.find_element(*LOC_BASKET_BUTTON)
    elem.click()
    sleep(3)


def validate_that_selected_product_added_correctly(my_driver):
    elements = my_driver.find_elements(*LOC_PRODUCT_NAME)
    print(elements[0].text, elements[1].text)
    assert elements[0].text == elements[1].text


def validate_that_sellers_are_different(my_driver):
    elements = my_driver.find_elements(*LOC_SELLERS)
    print(elements[0].text, elements[1].text)
    assert elements[0].text != elements[1].text


def empty_the_basket(my_driver):
    elements = my_driver.find_elements(*LOC_DELETE_BUTTON)
    while len(elements):
        elements[0].click()
        sleep(2)
        elements = my_driver.find_elements(*LOC_DELETE_BUTTON)
    sleep(3)


def validate_that_basket_is_emptied(my_driver):
    element = my_driver.find_elements(*LOC_PRODUCT_NAME)
    assert len(element) == 0


def logout(my_driver):
    element1 = my_driver.find_element(*LOC_MYACCOUNT)
    element2 = my_driver.find_element(*LOC_LOGOUT)
    action = ActionChains(my_driver)
    action.move_to_element(element1).perform()
    sleep(1)
    action.click(element2)
    action.perform()
    sleep(3)


def validate_that_logout_is_successful(my_driver):
    element = my_driver.find_element(*LOC_USERNAME)
    assert element.text == ''


# Test Cases
@pytest.mark.parametrize("product", ['Fifa 20', 'Sony Kulaklık'])
def test_adding_products_to_the_basket_by_user_login(my_driver, product):
    open_page(my_driver, BASE_URL)
    navigate_to_login_page(my_driver)
    login_with(my_driver, email=USER_EMAIL, password=USER_PASSWORD)
    validate_that_login_is_successful(my_driver)
    search_a_product(my_driver, term=product)
    click_first_product_in_search_results(my_driver)
    add_product_to_basket_from_two_different_sellers(my_driver)
    navigate_to_basket_page(my_driver)
    validate_that_selected_product_added_correctly(my_driver)
    validate_that_sellers_are_different(my_driver)
    empty_the_basket(my_driver)
    validate_that_basket_is_emptied(my_driver)
    logout(my_driver)
    validate_that_logout_is_successful(my_driver)


@pytest.mark.parametrize("product", ['Walkman', 'God Of War'])
def test_adding_products_to_the_basket_without_user_login(my_driver, product):
    open_page(my_driver, BASE_URL)
    search_a_product(my_driver, term=product)
    click_first_product_in_search_results(my_driver)
    add_product_to_basket_from_two_different_sellers(my_driver)
    navigate_to_basket_page(my_driver)
    validate_that_selected_product_added_correctly(my_driver)
    validate_that_sellers_are_different(my_driver)
    empty_the_basket(my_driver)
    validate_that_basket_is_emptied(my_driver)

