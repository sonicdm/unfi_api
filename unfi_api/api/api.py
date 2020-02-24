import requests
from bs4 import BeautifulSoup

login_page = r"https://customers.unfi.com/_login/LoginPage/Login.aspx"


class UnfiAPI(object):

    def __init__(self, user, password):
        self.session = requests.session()
        self.hfTokValidator = None
        self.user_id = None
        self.account_id = None
        self.account_number = None
        self.warehouse_id = None
        self.region = None
        self.logged_in = False
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
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                          ' AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/79.0.3945.130 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;'
                      'q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
        }

        echo_url = "http://localhost:8000/"
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
            'accept': 'text/html,application/xhtml+xml,application/xml;'
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
            self.hfTokValidator = validator_tag['value']
            self.logged_in = True
        else:
            self.logged_in = False
            raise Exception("Login Failed")

    def change_account(self):
        pass


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
