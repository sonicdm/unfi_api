import requests
from selenium.webdriver import Chrome, ChromeOptions, Remote, PhantomJS
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from http import cookiejar
import webbrowser
import urllib.parse
# from incapsula import IncapSession, RecaptchaBlocked
# session = IncapSession()
from bs4 import BeautifulSoup
import json
from .order_management import OrderManagement, Brands
from .admin_backend import AdminBackend
from .products import Products
import sys
import warnings
import os

warnings.filterwarnings("ignore")

selenium_server = "http://%s:%s/wd/hub" % ("127.0.0.1", 4444)

login_page = r"https://customers.unfi.com/_login/LoginPage/Login.aspx"


class UnfiAPI(object):

    def __init__(self, user, password, cookiestxt=None):
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
        self.login(user, password)

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
            # try to check for an incapsula block.
            # test product.
            test = self.products.get_product_by_int_id(187126)
            if test['error']:
                error_content = BeautifulSoup(test['content'], features="lxml")
                if error_content.select('meta[name="ROBOTS"]') or error_content.select('meta[name="robots"]'):
                    self.incapsula = True
                    # iframe_src = error_content.iframe['src']
                    # split = urllib.parse.urlsplit(self.products.api_endpoint)
                    # newsplit = urllib.parse.SplitResult(scheme=split.scheme, netloc=split.netloc, path=iframe_src,
                    #                                     query='', fragment='')
            url = self.products.api_endpoint + str(187126)
            chrome_options = ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-proxy-server')
            # chrome = Chrome(chrome_options=chrome_options)
            dc = DesiredCapabilities.HTMLUNIT
            # driver = Remote(desired_capabilities=dc)
            driver = PhantomJS(service_log_path=os.path.devnull)
            driver.get("https://products.unfi.com/blahhs")
            session_cookies = [{'name': name, 'value': value} for name, value in self.session.cookies.items()]
            # c = [driver.add_cookie(x) for x in session_cookies]
            driver.get(url)
            cookies = driver.get_cookies()
            driver.quit()
            if cookies:
                for cookie in cookies:
                    self.session.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])
                test = self.products.get_product_by_int_id(187126)
                if test['error']:
                    raise Exception('Incapsula Error')

        else:
            self.logged_in = False
            raise Exception("Login Failed")

        # get page claims
        claims = json.loads(home_soup.select_one("#claims")['value'])
        self.usermeta = claims

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


def get_context_info(session):
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
