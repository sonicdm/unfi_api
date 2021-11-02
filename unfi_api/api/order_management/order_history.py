import requests
from unfi_api.utils.http import response_to_api_response, response_to_json
from unfi_api.api.base_classes import APICore

order_history_base_url = 'https://ordermanagement.unfi.com/api/OrderHistory/'


def get_grid_item(api: APICore, token: str, account_num: str, user_id:str, region, transaction_type=1, order_no='', po_no='', req_by='',
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

    response = api.get('https://ordermanagement.unfi.com/api/OrderHistory/GetGridItem', headers=headers,
                           params=params)
    # echo_response = requests.get('http://localhost:8000/api/OrderHistory/GetGridItem', headers=headers, params=params)
    # echo_json = echo_response.json()

    return response_to_api_response(response)


def get_open_orders_item_for_west(api: APICore, token):
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

    response = api.get(endpoint_url,
                           headers=headers, params=params)


def get_credit_invoice_detail_for_west(session, invoice_number, customer_number, command=None):
    "https://ordermanagement.unfi.com/api/OrderHistory/GetCreditInvoiceDetailForWest?invoiceNumber={invoicenum}&customerNumber={custnum}&command="

    endpoint = "GetCreditInvoiceDetailForWest"
    url = order_history_base_url + endpoint

    headers = {
        'authority': 'ordermanagement.unfi.com',
        'accept': '*/*',
        'dnt': '1',
        # 'authorization': '155369~bd799292-638e-4031-a179-f5913aed5bf6:77u/PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz48U1A+MDUudHx1bmZpc3RzfHBvc0BjYXBlbGxhbWFya2V0LmNvbSwwNS50fHVuZmlzdHN8cG9zQGNhcGVsbGFtYXJrZXQuY29tLDEzMjM1MDY5MzUyODcyMjMzNyxGYWxzZSxlcEhpRUdUVHphYWUvWnZMd3pxV2ZhZWhkdzRqZ2EvWEoyeGZ0RFAxcmVXcTUwNWo1U3RXU0ZHTEtKTEo2aUpaNEdqSFVpc0p3K1BSY3phZVBBa2lWSEJmQ2pGQlBaTEFuWThsM0xQY1QweTJRWDlCZlBmVkUvZXhuNmk2TElkRkQzbTQ2N05Nc0lmRVJhdUhBaDZpOHBRdW9ZSnkxY1VKemR3RTVlUlhON0pNaHk1SWVwUFF3M2srSGdJeVhsUTRtWS9FRWNmd0huVUtNemJaZWswZzc3czVHK1YyaEd3RzVuQ2RsUzlIelVuWjA0YzFsQnIyNktiQ3dKeXpJT0VFZmxoV3g0ZG9Qb1l3MWZuWlR4K3pwTXFGNE0zenY5bTRRNlY0eWtGSUdsaWlpbmdWbUVSYmh2TU12N1hIM3NHYVlPS05WazE3OG5PdU0zaFVxOG81YWc9PSxodHRwczovL2N1c3RvbWVycy51bmZpLmNvbS88L1NQPg==:1',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        'content-type': 'application/json; charset=utf-8',
        'origin': 'https://customers.unfi.com',
        'referer': 'https://customers.unfi.com/Pages/OrderHistory.aspx',
        'accept-language': 'en-US,en;q=0.9',
    }

    params = (
        ('invoiceNumber', invoice_number),
        ('customerNumber', customer_number),
        ('command', command),
    )

    response = requests.get('https://ordermanagement.unfi.com/api/OrderHistory/GetCreditInvoiceDetailForWest',
                            headers=headers, params=params)


def get_grid_item_detail(session, order_header_id, region, account_number, warehouse, transaction_type,
                         page_size=1000, page_number=1, sort_expression='', sort_direction=''):
    """
    Transaction types:
    1: Invoices
    2: Web Orders
    4: Credits
    :param session:
    :param order_header_id:
    :param region:
    :param account_number:
    :param warehouse:
    :param transaction_type:
    :param page_size:
    :param page_number:
    :param sort_expression:
    :param sort_direction:
    :return:
    """
    endpoint = "GetGridItemDetail"
    url = order_history_base_url + endpoint
    params = (
        ('OrderHeaderId', order_header_id),
        ('regionn', region),
        ('TransactionType', transaction_type),
        ('accountNumber', account_number),
        ('whs', warehouse),
        ('pageSize', page_size),
        ('pageNumber', page_number),
        ('sortExpression', sort_expression),
        ('sortDirection', sort_direction),
    )

    response = session.get(url, params=params)
    return response_to_json(response)
