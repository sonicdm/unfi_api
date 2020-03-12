import requests
from unfi_api.utils.http import response_to_json


def get_grid_item(token, account_num, user_id, region, transaction_type=1, order_no='', po_no='', req_by='',
                  invoice_no='', page_size=5000, page_number=1, sort_expression='', sort_direction=''):
    """
    get list of orders per type and criteria
    Transaction types:
    1: Invoices
    2: Web Orders
    4: Credits
    :rtype: `dict`
    """
    headers = {
        # 'authority': 'ordermanagement.unfi.com',
        # 'accept': 'application/json, text/javascript, */*; q=0.01',
        # 'dnt': '1',
        'authorization': token,
        # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        #               ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        # 'origin': 'https://customers.unfi.com',
        # 'sec-fetch-site': 'same-site',
        # 'sec-fetch-mode': 'cors',
        # 'referer': 'https://customers.unfi.com/Pages/OrderHistory.aspx',
        # 'accept-encoding': 'gzip, deflate, br',
        # 'accept-language': 'en-US,en;q=0.9',
    }

    # params = (
    #     ('custNum', '001014    '),
    #     ('UserId', '155329'),
    #     ('region', 'West'),
    #     ('TransactionType', '2'),  # web order: 2 - Invoice: 1
    #     ('OrderNo', ''),
    #     ('PONO', ''),
    #     ('ReqBy', ''),
    #     ('InvoiceNo', ''),
    #     ('pageSize', '10'),
    #     ('pageNumber', '1'),
    #     ('sortExpression', ''),
    #     ('sortDirection', ''),
    # )

    params = {
        'custNum': account_num,
        'UserId': user_id,
        'region': region,
        'TransactionType': transaction_type,
        'OrderNo': order_no,
        'PONO': po_no,
        'ReqBy': req_by,
        'InvoiceNo': invoice_no,
        'pageSize': page_size,
        'pageNumber': page_number,
        'sortExpression': sort_expression,
        'sortDirection': sort_direction,
    }

    response = requests.get('https://ordermanagement.unfi.com/api/OrderHistory/GetGridItem', headers=headers,
                            params=params)
    # echo_response = requests.get('http://localhost:8000/api/OrderHistory/GetGridItem', headers=headers, params=params)
    # echo_json = echo_response.json()

    return response_to_json(response)


def get_open_orders_item_for_west(token):
    endpoint_url = 'https://ordermanagement.unfi.com/api/OrderHistory/GetOpenOrdersItemForWest'
    headers = {
        'authority': 'order_management.unfi.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'authorization': token,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                      ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'origin': 'https://customers.unfi.com',
        'referer': 'https://customers.unfi.com/Pages/OrderHistory.aspx',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
    }

    params = (
        ('custNum', '001014    '),
        ('OrderNo', ''),
        ('PONO', ''),
        ('InvoiceNo', ''),
    )

    response = requests.get(endpoint_url,
                            headers=headers, params=params)
