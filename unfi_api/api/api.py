import requests
from bs4 import BeautifulSoup

login_page = r"https://customers.unfi.com/_login/LoginPage/Login.aspx"


class UnfiAPI(object):

    def __init__(self, user, password):
        self.session = requests.session()
        self.hfTokValidator = None
        self.login(user, password)

    def login(self, user, passwd):
        login_page_result = self.session.get(login_page)

        login_page_content = login_page_result.content.decode("utf-8")

        login_page_soup = BeautifulSoup(login_page_content)
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
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'referer': 'https://customers.unfi.com/_login/LoginPage/Login.aspx?ReturnUrl=%2f_layouts%2f15%2fAuthenticate.aspx%3fSource%3d%252F&Source=%2F',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
        }

        echo_url = "http://localhost:8000/"
        login_result = self.session.post('https://customers.unfi.com/_login/LoginPage/Login.aspx',
                                    headers=headers,
                                    params=params,
                                    data=data

                                    )
        # print(login_result.json())
        login_soup = BeautifulSoup(login_result.content)
        form_data = {}
        form_action = login_soup.form['action']
        for form_input in login_soup.find_all("input", type="hidden"):
            value_name = form_input['name']
            value = form_input['value']
            form_data[value_name] = value

        headers = {
            'authority': 'customers.unfi.com',
            'cache-control': 'max-age=0',
            'origin': 'https://stsuser.unfi.com',
            'upgrade-insecure-requests': '1',
            'dnt': '1',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
            'sec-fetch-user': '?1',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'navigate',
            'referer': 'https://stsuser.unfi.com/?wa=wsignin1.0&wtrealm=https%3a%2f%2fcustomers.unfi.com%2f_trust%2fpages%2fhome.aspx&wctx=rm%3d0%26id%3dpassive%26ru%3dhttps%253a%252f%252fcustomers.unfi.com%252f_trust%252fpages%252fhome.aspx&wct=2020-02-22T05%3a09%3a04Z&wreply=https%3a%2f%2fcustomers.unfi.com%2f_trust%2fpages%2fhome.aspx&username=Capellabulk&password=lPrxMV%2f3aebdjyNtbmqMWg%3d%3d',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            # 'cookie': 'visid_incap_536781=QRzIRFM6TC2qvoPgKWYeav+YUF4AAAAAQUIPAAAAAADn26qujEl9ESHhCxmN8LG4; visid_incap_544876=QuVHDFBpRt22lsPgKwjaCQKZUF4AAAAAQUIPAAAAAAC3WxN8v7615w58HkuGKolA; visid_incap_545234=OTE6OEpcTCisxRUNc3lStASZUF4AAAAAQUIPAAAAAADHjfUZfUm3oij1jDmU8yMM; BIGipServerSharePoint_2013.app~SharePoint_2013_pool=2036007178.20480.0000; ASP.NET_SessionId=5jz0li44umpgapiw5f2b25ms; WSS_FullScreenMode=false; menuAlertFlag=visible; nlbi_536781=FQmvN2s31TnvHjhiKsD0NQAAAADy9O+pMftQAogXYdpyAGA9; incap_ses_207_536781=44crZwUgBlIVOxqjB87fAjCsUF4AAAAABcuRqMuiVh+ue2i8J4fvpg==; incap_ses_207_544876=jZL0T7iCVShtuiajB87fAum2UF4AAAAA0N9hwpn0Nz/6scr/vYI5Eg==; incap_ses_207_545234=iHPnY1/qoR0nuyajB87fAuq2UF4AAAAAkFo2I0PP4aVRJAn8VC7PUg==',
        }

        home = self.session.post('https://customers.unfi.com/_trust/pages/home.aspx', data=form_data, headers=headers)
        home_soup = BeautifulSoup(home.content, features="lxml")
        validator_tag = home_soup.select_one("#hfTokValidator")
        if validator_tag:
            self.hfTokValidator = validator_tag['value']
            self.logged_in = True
        else:
            self.logged_in = False
            raise Exception("Login Failed")




