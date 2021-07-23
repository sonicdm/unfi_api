import json
import warnings

import requests
# from incapsula import IncapSession, RecaptchaBlocked
# session = IncapSession()
from bs4 import BeautifulSoup
from selenium.webdriver import ChromeOptions
from selenium.webdriver import Remote, Chrome, PhantomJS

from .admin_backend import AdminBackend
from .order_management import Brands
from .order_management import OrderManagement
from .products import Products

warnings.filterwarnings("ignore")

selenium_server = "http://%s:%s/wd/hub" % ("192.168.1.161", 4444)

login_page = r"https://customers.unfi.com/_login/LoginPage/Login.aspx"


class UnfiAPI(object):

    def __init__(self, user, password, incapsula_retry=False, incapsula_retry_limit=10, cookiestxt=None):
        self.incapsula_retry_count = 0
        self.incapsula_retry_limit = incapsula_retry_limit
        self.incapsula_retry = incapsula_retry
        self.session = requests.session()
        self.incapsula = False
        self.cookiejar = None
        self.cookiestxt = cookiestxt
        self.auth_token = None
        self.logged_in = False
        self.usermeta = {}
        self._admin_backend = AdminBackend(self)
        self._products = Products(self)
        self._brands = Brands(self)
        self._order_management = OrderManagement(self)
        self.driver = None
        self.login(user, password)
        self._load_incapsula_cookies()
        # if not self._test_incapsula():
        #     self._load_incapsula_cookies()

    def login(self, user, passwd):
        login_page_result = self.session.get(login_page)

        login_page_content = login_page_result.content.decode("utf-8")

        login_page_soup = BeautifulSoup(login_page_content, features="lxml")

        viewstate = login_page_soup.select_one("#__VIEWSTATE")['value']
        viewstate_generator = login_page_soup.select_one("#__VIEWSTATEGENERATOR")['value']
        event_validation = login_page_soup.select_one("#__EVENTVALIDATION")['value']

        params = (
            ('ReturnUrl', '/_layouts/15/Authenticate.aspx?Source=%2F'),
            ('Source', '/'),
        )

        data = {
            '__VIEWSTATE': viewstate,
            '__VIEWSTATEGENERATOR': viewstate_generator,
            '__EVENTVALIDATION': event_validation,
            'userName': user,
            'Password': passwd,
            'login_btn': 'Log In'
        }

        headers = {
            'authority': 'customers.unfi.com',
            'origin': 'https://customers.unfi.com',
            'referrer': 'https://customers.unfi.com',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                          ' AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/79.0.3945.130 Safari/537.36',
            'accept': 'application/json, text/html,application/xhtml+xml,application/xml,application/json;'
                      'q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
        }

        echo_url = "http://localhost:8000/"
        self.session.headers = headers
        login_result = self.session.post('https://customers.unfi.com/_login/loginpage/login.aspx',
                                         headers=headers,
                                         params=params,
                                         data=data

                                         )
        login_soup = BeautifulSoup(login_result.content, features="lxml")
        form_data = {}
        form_action = login_soup.form['action']
        for form_input in login_soup.find_all("input", type="hidden"):
            value_name = form_input['name']
            value = form_input['value']
            form_data[value_name] = value

        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                          ' AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/79.0.3945.130 Safari/537.36',
            'accept': 'application/json,text/html,application/xhtml+xml,application/xml;'
                      'q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'navigate',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
        }
        home_url = 'https://customers.unfi.com/_trust/pages/home.aspx'
        home = self.session.post(home_url, data=form_data, headers=headers)
        home_soup = BeautifulSoup(home.content, features="lxml")
        validator_tag = home_soup.select_one("#hfTokValidator")
        if validator_tag:
            self.auth_token = validator_tag['value']
            self.logged_in = True
            self.session.headers['authorization'] = self.auth_token
            # load page claims to get users metadata
            claims = json.loads(home_soup.select_one("#claims")['value'])
            self.usermeta = claims

            ############################################################################################################
            # url = self.products.api_endpoint + str(187126)
            # # self.session.get(url)
            # chrome_options = ChromeOptions()
            # # dc = DesiredCapabilities.HTMLUNIT
            # # driver = Remote(selenium_server)
            # # driver = PhantomJS(service_log_path=os.path.devnull)
            # # self.driver.delete_all_cookies()
            # self.driver = Remote(selenium_server, desired_capabilities=chrome_options.to_capabilities())
            # self.driver.get("https://products.unfi.com/187126")
            # page_source = self.driver.page_source
            # cookie_dict = list(self.session.cookies.items())
            # session_cookies = [{'name': name, 'value': value} for name, value in self.session.cookies.items()]
            # [self.driver.add_cookie(x) for x in session_cookies]
            # self.driver.get(url)
            # self.driver.get(url)
            #
            # cookies = self.driver.get_cookies()
            # if cookies:
            #     for cookie in cookies:
            #         self.session.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])
            #     test = self.products.get_product_by_int_id(187126)
            #     if test['error']:
            #         raise IncapsulaError
            # self.driver.quit()
            ############################################################################################################

        else:
            self.logged_in = False
            raise LoginException

    def _load_incapsula_cookies(self, incapsula_page=None, driver_type="remote", remote_selenium_address=None,
                                driver_options=None):
        """
        Use selenium to load the product detail endpoint and execute the incapsula javascript to set the session cookies
        driver type must be remote, chrome or phantomjs.
        :param incapsula_page: url to get the cookies from
        :param driver_type: remote, chrome or phantomjs
        :param remote_selenium_address: if using remote, location of the selenium server
        :param driver_options: options to provide to the driver, does not apply to phantomjs driver
        :return:
        """
        driver = None

        if not remote_selenium_address and driver_type == "remote":
            remote_selenium_address = selenium_server

        if driver_type == "remote":
            if driver_options:
                chrome_options = driver_options
            else:
                chrome_options = ChromeOptions()
            driver = Remote(remote_selenium_address, desired_capabilities=chrome_options.to_capabilities(),
                            options=chrome_options)

        elif driver_type == "chrome":
            if driver_options:
                chrome_options = driver_options
            else:
                chrome_options = ChromeOptions()
                chrome_options.headless = True
            driver = Chrome(chrome_options=chrome_options)

        elif driver_type == "phantomjs":
            driver = PhantomJS()

        else:
            raise AttributeError("driver type must be remote, chrome or phantomjs")

        if not incapsula_page:
            incapsula_page = "https://products.unfi.com/api/Products/187126"
        # test_page = self.session.get(incapsula_page)
        url = self.products.api_endpoint + str(187126)
        driver.get("https://products.unfi.com/187126")
        # self.session.get(url)
        cookie_dict = list(self.session.cookies.items())
        session_cookies = [{'name': name, 'value': value} for name, value in self.session.cookies.items()]
        for x in session_cookies:
            driver.add_cookie(x)

        driver.get(url)
        page_source = driver.page_source
        cookies = driver.get_cookies()
        if cookies:
            for cookie in cookies:
                self.session.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])

        if not self._test_incapsula():
            print("Incapsula has blocked the request")
            print(driver.get_cookies())
            if self.incapsula_retry and self.incapsula_retry_count <= self.incapsula_retry_limit:
                self.incapsula_retry_count += 1
                print(f"Retry {self.incapsula_retry_count} of {self.incapsula_retry_limit}")
                self._load_incapsula_cookies()
            else:
                driver.quit()
                raise IncapsulaError
        driver.quit()

    def _test_incapsula(self):
        """Test if the incapsula cookies are valid"""
        test = self.products.get_product_by_int_id("00001")
        if test['error']:
            return False
        else:
            return True
        pass

    def change_account(self, account_number):
        # self.admin_backend.user.insert_selected_account_as_default(account_number)
        pass

    def refresh_metadata(self):
        home_url = 'https://customers.unfi.com/pages/Home.aspx'
        home = self.session.post(home_url)
        home_soup = BeautifulSoup(home.content, features="lxml")
        validator_tag = home_soup.select_one("#hfTokValidator")
        if validator_tag:
            self.auth_token = validator_tag['value']
            self.logged_in = True
        else:
            self.logged_in = False
            raise Exception("Login Failed")

        # get page claims
        claims = json.loads(home_soup.select_one("#claims")['value'])
        self.usermeta = claims

    def search(self, query, ):
        pass

    @property
    def account(self):
        return self.usermeta['LastSelectedAccount']

    @property
    def user_id(self):
        return self.usermeta["UserId"]

    @property
    def warehouse_id(self):
        return self.usermeta["WarehouseId"]

    @property
    def warehouse(self):
        return self.usermeta["Warehouse"]

    @property
    def account_region(self):
        return self.usermeta['LastSelectedAccountRegion']

    @property
    def customer_number(self):
        return self.usermeta["CustomerNumber"]

    @property
    def order_management(self):
        return self._order_management

    @property
    def admin_backend(self):
        return self._admin_backend

    @property
    def products(self):
        return self._products

    @property
    def brands(self):
        return self._brands

    def get_product(self, product_code=None, product_id=None):
        return self.products.product(product_code, product_id)

    def get_context_info(self):
        headers = {
            'accept': 'application/json;odata=verbose',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'accept-language': 'en-US,en;q=0.9',
        }

        response = requests.post('https://customers.unfi.com/_api/contextinfo', headers=headers)


class IncapsulaError(Exception):
    pass


class LoginException(Exception):
    pass
