from __future__ import print_function

import datetime
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from html import escape

import requests
from bs4 import BeautifulSoup
from catalogboss.formatter import size_cols
from catalogboss.utils import strings_to_numbers
from openpyxl import Workbook

import unfi_api
from unfi_api.old_product import product_info
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
from unfi_api.utils import divide_chunks


def run():
    pass


def uncaught_exception_handler(type, value, tb):
    print(type, value, tb)
    input("PROCESS FAILED PRESS ENTER TO QUIT")


sys.excepthook = uncaught_exception_handler


def pull_invoices(token, date, xdock=False, api=None):
    invoice_dict = {}
    threading = Threading()
    if xdock:
        num_days = 2
        dock = "Auburn X-Dock"
    else:
        num_days = 1
        dock = "Ridgefield"

    invoices = get_invoice_list(token, date, num_days=num_days, xdock=xdock, api=api)
    print("Downloading {COUNT} {DOCK} invoices...".format(DOCK=dock, COUNT=len(invoices)))

    def _add_invoice_to_dict(i):
        invoice_dict[i] = get_invoice(i, token, xdock, api=api)

    threading.thread_with_progressbar(_add_invoice_to_dict, invoices)
    # for invoice in invoices:
    #     _add_invoice_to_dict(invoice)

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


def get_invoice_list(token, dateobj, num_days=1, xdock=False, api=None):
    """

    :type api: 'unfi_api.api.api.UnfiAPI'
    """
    header = {
        'authorization': '{token}'.format(token=api.auth_token, )
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
    invoice_date = dateobj - datetime.timedelta(days=0)
    invoice_date_string = invoice_date.strftime('%m/%d/%Y')
    invoices = api.order_management.order_history.get_invoice_list()
    response = api.session.get(invoice_list_url)
    # invoice_search_result = json.loads(response.content)
    invoice_search_result = invoices['data']
    invoice_dict = {}
    for invoice in invoice_search_result:
        invoice_date = datetime.datetime.strptime(invoice['InvoiceDate'], '%m/%d/%Y')
        invoice_day = invoice_dict.get(invoice_date, [])
        invoice_day.append(invoice['InvoiceNumber'])
        invoice_dict[invoice_date] = invoice_day

    invoice_nums = invoice_dict[get_most_recent_date(invoice_dict.keys(), dateobj)]
    return invoice_nums


def get_most_recent_date(items, dateobj):
    found_date = None
    for day in items:
        if (dateobj - day).days < 0:
            continue
        if found_date is None or found_date < day:
            found_date = day
    return found_date


def get_invoice(invoice_number, token, xdock=False, callback=None, api: unfi_api.UnfiAPI = None):
    if xdock:
        invoice_url = invoice_xhr.format(invoicenum=invoice_number.strip(), custnum=xdock_cust_num)
    else:
        invoice_url = invoice_xhr.format(invoicenum=invoice_number.strip(), custnum=api.account)
    header = {
        'authorization': '{token}'.format(token=token)
    }
    invoice = api.session.get(invoice_url)
    # invoice = api.order_management.order_history.get_invoice(invoice_number)
    # invoicesoup = BeautifulSoup(invoice['data'], "html.parser")
    invoicesoup = BeautifulSoup(invoice.text, 'html.parser')
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


def create_invoice_workbook(invoicedict, outputpath=None, invdate=None):
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
    combined = []
    if not invdate:
        invdate = datetime.date.today()
    for invoice, rows in sorted(invoicedict.items()):
        if i == 1:
            header = rows[2].copy()
            header.insert(0, "Invoice #")
            header.insert(1, "Invoice Date")
            combined.append(header)
            ws = wb.active
            ws.title = invoice
            i += 1
        else:
            ws = wb.create_sheet(invoice)
        for row in rows:
            ws.append(strings_to_numbers(row))
        size_cols(ws)
        for l in rows[3:]:
            l.insert(0, invoice[:-4])
            l.insert(1, invdate.strftime("%m/%d/%y"))
            combined.append(l)

    combws = wb.create_sheet("All Invoices", 0)
    for l in combined:
        combws.append(l)

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

    return dict(sheetindex=sheets, workbook=workbook, original=wb, combined=combined)


def set_default_account(userid, account, token, region="West"):
    headers = {'authorization': token}
    payload = [{"UserId": userid, "SelectedAccount": account, "SelectedRegion": region}]
    request = requests.post(set_default_account_xhr, headers=headers, json=payload)


def make_query_list(query):
    # split query by white space and remove non text
    import re
    query_list = re.split(r'\s', query)
    query_list = [re.sub(r'\W+', "", x) for x in query_list]
    try:
        query_list.remove("")
    except ValueError:
        pass
    return strings_to_numbers(query_list)


def run_query(query_list, token, xdock=False, api=None):
    """
    Search unfi web site for queries
    :type xdock: bool
    :param xdock: whether or not to search cross dock

    :param api: authorization token
    :type api: `unfi_api.api.api.UnfiAPI`
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
    remaining_terms = query_len
    query_chunks = list(divide_chunks(query_list, 120))
    product_list = []
    warehouse = "Cross Dock" if xdock else "Ridgefield"
    print("Running query for %d terms from %s. Spawning %s threads." % (query_len, warehouse, len(query_chunks)))

    # token = token
    # run through query list until no items remain.
    def _search_chunk(c):

        return search_products(c, token, xdock, api)

    with ThreadPoolExecutor(max_workers=len(query_chunks)) as e:
        futures = []
        for chunk in query_chunks:
            join_query = " ".join(str(x) for x in chunk)
            # print("Searching for {} terms out of {}  remaining terms".format(len(chunk), remaining_terms))
            # search_result = search_products(join_query, token, xdock)
            # product_list.extend(search_result.get('TopProducts'))
            # search_results.append(search_result)
            # print("Found {} of {} items".format(len(product_list), query_len))
            print("Searching for {} terms.".format(len(chunk)))
            # search_products(_search_chunk,token,xdock)
            futures.append(e.submit(_search_chunk, join_query))

        for r in as_completed(futures):
            search_result = r.result()
            product_list.extend(search_result.get('TopProducts'))
            search_results.append(search_result)
            print("Found {} of {} items".format(len(product_list), query_len))
            remaining_terms -= len(chunk)

    # search = True
    # while search:
    #     search = False
    #     query = []
    #     for i in range(120):
    #         try:
    #             query.append(str(query_list.pop()))
    #         except IndexError:
    #             pass
    #     if len(query) > 0:
    #         join_query = " ".join(query)
    #         if len(query_list) > 0:
    #             print("Searching for {} terms out of remaining {} terms".format(len(query), query_len - num_queried))
    #         else:
    #             print("Searching for remaining {} terms.".format(len(query)))
    #         num_queried += len(query)
    #         search_result = search_products(join_query, token, xdock)
    #         product_list.extend(search_result.get('TopProducts'))
    #         search_results.append(search_result)
    #         search = True
    print("Found {} of {} items".format(len(product_list), query_len))
    if product_list:
        products = product_info(product_list, token, xdock=xdock, api=api)
        return products
    else:
        print('No results for your search.')
        return None


def search_products(query, token, xdock=False, api=None):
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
    # print("Searching Database....")
    response = requests.get(query_url, headers=header)
    results = json.loads(response.content)
    print('Found: ', results['TotalHits'], " results.")
    return results
