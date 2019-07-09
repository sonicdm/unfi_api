# selenium

from seleniumrequests import Chrome
from unfi_api import unfi_web_queries, unfi_product_api
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import datetime, date
import time

timeout = 10
ridgefield_cust_num = "001014"
ridgefield_warehouse = 6
user_id = "34653"
login_url = "https://customers.unfi.com/_login/LoginPage/Login.aspx"
homepage = "https://customers.unfi.com/pages/Home.aspx"
account_page = "https://customers.unfi.com/pages/ChangeAccount.aspx"
# user = "grocery@capellamarket.com"
# password = "Organic1"

query = ["70816312193", "07215500005"]


class UnfiDriver:
    def __init__(self, options=None):
        if not options:
            options = Options()
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-extensions")
            options.add_argument('--window-size=800,600')
            options.add_argument("--start-maximized")
            options.add_argument("--hide-scrollbars")
            options.add_argument("--log-level=1")
            options.add_argument(
                '--user-agent="Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166"')
            # options.headless = True
        self.driver = Chrome(executable_path=r'C:\webdrivers\chromedriver.exe', options=options,
                             service_args=["--verbose", "--log-path=C:\\scriptlogs\cd.log"])
        self.account = ""

    def login(self, user, password):
        username_id = "userName"
        password_id = "Password"
        submit_id = "login_btn"

        self.driver.get(login_url)
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.ID, username_id))
            )
        except TimeoutException:
            print("Timed out waiting for login page to load")

        self.driver.find_element_by_id(username_id).send_keys(user)
        self.driver.find_element_by_id(password_id).send_keys(password)
        self.driver.find_element_by_id(submit_id).click()
        try:
            main_page_loaded = EC.url_to_be(homepage)
            WebDriverWait(self.driver, timeout).until(main_page_loaded)
        except TimeoutException:
            print("Timed out waiting for login to complete")

    def set_account(self, account):
        self.driver.get(account_page)
        try:
            # wait for an account with a Set Default link is loaded before running through the list. UNFI is very slow
            main_page_loaded = EC.presence_of_element_located((
                By.CSS_SELECTOR,
                r'#usersGrid > div.k-grid-content > table > tbody > tr:nth-child(1) > td:nth-child(10) > a'
            ))
            WebDriverWait(self.driver, timeout).until(main_page_loaded)
        except TimeoutException:
            print("Timed out loading account list")
        account_list = self.driver.find_element_by_id("usersGrid").find_elements_by_xpath(r"*/table/tbody/tr")
        for account_row in account_list:
            account_number = account_row.find_element_by_xpath("td[7]").text
            if account_number == account:
                print("Account found. Switching to : " + account_number)
                button = account_row.find_element_by_xpath(r"td[10]/a")
                button.click()
                break
        cur_url = self.driver.current_url

        # this is caps now for some stupid reason
        home_url = "https://customers.unfi.com/Pages/Home.aspx"
        self._wait_for_page(home_url)

    def get_token(self):
        return self.driver.find_element_by_id("hfTokValidator").get_attribute("value")

    def get_current_account(self):
        return self.driver.find_element_by_css_selector("#lblAccountNum").text.strip(",").strip()

    def get(self, url):
        self.driver.get(url)

    def quit(self):
        self.driver.quit()

    def close_window(self):
        self.driver.close()

    def _wait_for_page(self, page, fail_message=None):
        try:
            page_loaded = EC.url_to_be(page)
            WebDriverWait(self.driver, timeout).until(page_loaded)
        except TimeoutException:
            print("Timed out waiting for {page} to load".format(page=page))

    def _wait_for_css_element(self, element, failmsg="Element Search Timeout"):
        try:
            # wait for an account with a Set Default link is loaded before running through the list. UNFI is very slow
            main_page_loaded = EC.presence_of_element_located((By.CSS_SELECTOR, element))
            WebDriverWait(self.driver, timeout).until(main_page_loaded)
        except TimeoutException:
            print(failmsg)
