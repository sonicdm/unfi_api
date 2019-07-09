from __future__ import print_function

import datetime
import json
from html import escape

import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

from catalogboss.formatter import size_cols
from catalogboss.utils import strings_to_numbers
from unfi_api.Product import product_info
from unfi_api.settings import \
    xdock_cust_num, \
    xdock_warehouse, \
    ridgefield_cust_num, \
    ridgefield_warehouse, \
    user_id, \
    unfi_invoice_list_xhr, \
    invoice_xhr, \
    set_default_account_xhr, search_url
from unfi_api.tools import Threading


def run():
    pass


def pull_invoices(token, date, xdock=False):
    invoice_dict = {}
    threading = Threading()
    if xdock:
        num_days = 2
        dock = "Auburn X-Dock"
    else:
        num_days = 1
        dock = "Ridgefield"

    invoices = get_invoice_list(token, date, num_days=num_days, xdock=xdock)
    print("Downloading {COUNT} {DOCK} invoices...".format(DOCK=dock, COUNT=len(invoices)))

    def _add_invoice_to_dict(i):
        invoice_dict[i] = get_invoice(i, token, xdock)

    threading.thread_with_progressbar(_add_invoice_to_dict, invoices)

    # if xdock:
    #     print("Downloading XDOCK Invoices...")
    #     xdock_invoices = get_invoice_list(token, date, num_days=2, xdock=xdock)
    #     for idx, invoice in enumerate(xdock_invoices, 1):
    #         print("Pulling invoice {}/{}".format(idx, len(xdock_invoices)))
    #         invoice_dict[invoice] = get_invoice(invoice, token, xdock)
    # else:
    #     print("Downloading Ridgefield Invoices...")
    #     invoice_numbers = get_invoice_list(token, date)
    #     for idx, invoice in enumerate(invoice_numbers, 1):
    #         print("Pulling invoice {}/{}".format(idx, len(invoice_numbers)))
    #         invoice_dict[invoice] = get_invoice(invoice, token)

    return invoice_dict


def get_invoice_list(token, dateobj, num_days=1, xdock=False):
    header = {
        'authorization': '{token}'.format(token=token, )
    }

    if xdock:
        invoice_list_url = unfi_invoice_list_xhr.format(
            userid=user_id,
            custnum=xdock_cust_num,
        )
    else:
        invoice_list_url = unfi_invoice_list_xhr.format(
            userid=user_id,
            custnum=ridgefield_cust_num
        )
    invoice_date = dateobj - datetime.timedelta(days=num_days)
    invoice_date_string = invoice_date.strftime('%m/%d/%Y')
    response = requests.get(invoice_list_url, headers=header)
    invoices = json.loads(response.content)
    invoice_nums = []
    for invoice in invoices:
        if invoice['InvoiceDate'] == invoice_date_string:
            invoice_nums.append(invoice['InvoiceNumber'])
    return invoice_nums


def get_invoice(invoice_number, token, xdock=False, callback=None):
    if xdock:
        invoice_url = invoice_xhr.format(invoicenum=invoice_number.strip(), custnum=xdock_cust_num)
    else:
        invoice_url = invoice_xhr.format(invoicenum=invoice_number.strip(), custnum=ridgefield_cust_num)
    header = {
        'authorization': '{token}'.format(token=token)
    }
    invoice = requests.get(invoice_url, headers=header)
    invoicesoup = BeautifulSoup(invoice.content, "html.parser")
    tablerows = []
    eof = False
    tables = invoicesoup.findAll('table')
    for tablenum, table in enumerate(tables[5:]):
        if eof:
            break
        rows = table.findAll('tr')
        for rownum, row in enumerate(rows):
            cells = []
            webcells = row.findAll('td')
            for cell in webcells:
                cell = cell.text.replace('\\r', '').replace('\\t', '').replace('\\n', '').strip()

                cell = cell
                if 'Freight Details' in cell:
                    eof = True
                    break

                v = cell
                cells.append(v)
            if eof:
                break
            tablerows.append(strings_to_numbers(cells))
    return tablerows


def create_invoice_workbook(invoicedict, outputpath=None):
    """
    Compile a dict of invoices numbers and rows into an xlsx workbook.
    save if requested (makes re-running the report much faster)
    :param invoicedict: {invoicenum: wbrows}
    :param outputpath: Where to save invoices.xlsx if defined. 
    :return: 
    """
    wb = Workbook()
    defaultws = wb.active
    i = 1
    for invoice, rows in sorted(invoicedict.items()):
        if i == 1:
            ws = wb.active
            ws.title = invoice
            i += 1
        else:
            ws = wb.create_sheet(invoice)
        for row in rows:
            ws.append(strings_to_numbers(row))
        size_cols(ws)

    sheets = {k: v for v, k in enumerate(wb.worksheets)}
    # sheets = sort_dict(sheets)

    workbook = []
    for ws in wb.worksheets:
        rowlist = []
        for row in ws.rows:
            rowlist.append([cell.value for cell in row])
        workbook.append(rowlist)
    if outputpath:
        wb.save(outputpath + r"\invoices.xlsx")

    return dict(sheetindex=sheets, workbook=workbook, original=wb)


def set_default_account(userid, account, token, region="West"):
    headers = {'authorization': token}
    payload = [{"UserId": userid, "SelectedAccount": account, "SelectedRegion": region}]
    request = requests.post(set_default_account_xhr, headers=headers, json=payload)


def make_query_list(query):
    # split query by white space and remove non text
    import re
    query_list = re.split(r'\s', query)
    query_list.remove("")
    return strings_to_numbers([re.sub('\W', "", x) for x in query_list])


def run_query(query_list, token, xdock=False):
    """
    Search unfi web site for queries
    :type xdock: bool
    :param xdock: whether or not to search cross dock
    :param token: authorization token
    :type token: str
    :type query_list: list
    :param query_list: List of upc to search for
    """
    search_results = []
    num_queried = 0
    query_list = query_list.copy()
    try:
        query_list.remove("")
    except ValueError:
        pass

    query_len = len(query_list)
    product_list = []
    warehouse = "Cross Dock" if xdock else "Ridgefield"
    print("Running query for %d terms from %s." % (query_len, warehouse))
    # run through query list until no items remain.

    search = True
    while search:
        search = False
        query = []
        for i in range(120):
            try:
                query.append(str(query_list.pop()))
            except IndexError:
                pass
        if len(query) > 0:
            join_query = " ".join(query)
            if len(query_list) > 0:
                print("Searching for {} terms out of remaining {} terms".format(len(query), query_len - num_queried))
            else:
                print("Searching for remaining {} terms.".format(len(query)))
            num_queried += len(query)
            search_result = search_products(join_query, token, xdock)
            product_list.extend(search_result.get('TopProducts'))
            search_results.append(search_result)
            search = True
    print("Found {} of {} items".format(len(product_list), query_len))
    if product_list:
        products = product_info(product_list, token, xdock=xdock)
        return products
    else:
        print('No results for your search.')


def search_products(query, token, xdock=False):
    """
    Poll the UNFI API for a query string. Returns the json response.
    :param query:
    :param token:
    :param xdock:
    :return:
    """
    header = {
        'authorization': '{token}'.format(token=token, )
    }
    query = escape(query)
    if xdock:
        query_url = search_url.format(
            query=query,
            userid=user_id,
            custnum=xdock_cust_num,
            warehouse=xdock_warehouse
        )
    else:
        query_url = search_url.format(
            query=query,
            userid=user_id,
            custnum=ridgefield_cust_num,
            warehouse=ridgefield_warehouse
        )
    print("Searching Database....")
    response = requests.get(query_url, headers=header)
    results = json.loads(response.content)
    print('Found: ', results['TotalHits'], " results.")
    return results
