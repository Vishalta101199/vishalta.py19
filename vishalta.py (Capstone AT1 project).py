import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Pass multiple browser params for cross browser testing 
@pytest.fixture(params=["chrome", "firefox"], scope="function")
def init_driver(request) :
    if request.param == "chrome":
        options = Options()
        options.add_argument("start-maximized")
        web_driver = webdriver.Chrome(options=options)
    if request.param == "firefox":
        web_driver = webdriver.Firefox()
        web_driver.maximize_window()
    request.cls.driver = web_driver
    yield
    web_driver.close()

    from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

""" This class is the parent of all pages it contains 
all the generic methods and utilities for all the pages """


class BasePage:

    def _init_(self, driver):
        self.driver = driver

    def do_click(self, by_locator):
        WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(by_locator)).click()

    def do_send_keys(self, by_locator, text):
        element = WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(by_locator))
        element.send_keys(text)

    def get_element(self, by_locator):
        element = WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(by_locator))
        return element

    def get_element_text(self, by_locator):
        element = WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(by_locator))
        return element.text

    def is_visible(self, by_locator):
        element = WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(by_locator))
        return bool(element)
    
    def get_title(self, title):
        WebDriverWait(self.driver, 15).until(EC.title_is(title))
        return self.driver.title
    
    def text_present(self, by_locator, text_):
        elem = WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element((by_locator), text_))
        return bool(elem)
    
    from Pages.BasePage import BasePage
from Config.config import TestData, WebLocators


class LoginPage(BasePage) :
    # constructor of the page class
    def _init_(self, driver):
        super()._init_(driver)
        self.driver.get(TestData.BASE_URL)

    # this is used to get the page title
    def get_login_page_title(self, title):
        return self.get_title(title)

    # this is used to login to app
    def do_login(self, username, password):
        self.do_send_keys(WebLocators.USERNAME, username)
        self.do_send_keys(WebLocators.PASSWORD, password)
        self.do_click(WebLocators.LOGIN)
    
    # this is used to fetch text
    def get_element_value(self, locator):
        if self.is_visible(locator):
            return self.get_element_text(locator)
                    
                    