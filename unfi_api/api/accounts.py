import requests


def insert_selected_account_as_default(token, user_id, account):
    endpoint_url = 'https://adminbackend.unfi.com/api/User/InsertSelectedAccountAsDefault'
    headers = {
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Sec-Fetch-Dest': 'empty',
        'Authorization': token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
        'DNT': '1',
        'Content-Type': 'application/json; charset=UTF-8',
        'Origin': 'https://customers.unfi.com',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Referer': 'https://customers.unfi.com/Pages/ChangeAccount.aspx',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    data = '[{"UserId":"140963","SelectedAccount":"001014    ","SelectedRegion":"West"}]'

    response = requests.post(endpoint_url, headers=headers,
                             data=data)


def get_users_data(token, user_id):
    endpoint_url = 'https://adminbackend.unfi.com/api/User/GetUsersData'
    headers = {
        'Accept': '*/*',
        'Authorization': token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
        'Origin': 'https://customers.unfi.com',
        'Referer': 'https://customers.unfi.com/Pages/ChangeAccount.aspx',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    params = (
        ('userName', ''),
        ('firstName', ''),
        ('lastName', ''),
        ('city', ''),
        ('state', ''),
        ('zip', ''),
        ('accountType', ''),
        ('accountName', ''),
        ('accountNo', ''),
        ('company', ''),
        ('EmailAddress', ''),
        ('account', ''),
        ('pageSize', '20'),
        ('pageNumber', '1'),
        ('UserId', user_id),
        ('sortExpression', ''),
        ('sortDirection', ''),
        ('apptype', ''),
    )

    response = requests.get(endpoint_url, headers=headers, params=params)
