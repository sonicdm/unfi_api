from __future__ import print_function

import csv
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import tqdm
from openpyxl import Workbook

from unfi_api.utils import strings_to_numbers, divide_chunks
from unfi_api.utils.upc import stripcheckdigit

try:
    from past.builtins import raw_input
except ImportError:
    pass
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog



LARGE_FONT = ("Arial", 16, "bold")
SUBTITLE_FONT = ("Arial", 12, 'bold')
CONTENT_FONT = ("Arial", 10)
LARGE_LBL_ARGS = {'padx': 10, 'pady': 10}

TEST_QUERY = """
86170300011
013562-11172
013562-11366
013562-11367
013562-11368
013562-11645
013562-11666
015532-00010
620133-00221
780872-07938
810589-03031
810589-03032
810589-03033
810589-03034
813636-02226
813636-02227
815074-02269
815074-02270
815074-02271
815074-02272
815074-02273
829462-50202
843536-10177
843536-10180
843536-10182
851093-00444
859908-00304
859908-00312
859908-00355
859908-00366
859908-00383
891756-00015
"""
username = "Grocery@capellamarket.com"
password = "Organic1"


def uncaught_exception_handler(etype, value, tb):
    print(etype, value, tb)
    input("PROCESS FAILED PRESS ENTER TO QUIT")


# sys.excepthook = uncaught_exception_handler


def main():
    tkroot = tk.Tk()
    tkroot.withdraw()
    # query = simpledialog.askstring("Search For Products", "Search For: ")
    query = TEST_QUERY
    print("Loading UNFI Driver")
    # api = UnfiAPI(username, password)
    # if api.incapsula:
    #     print("Incapsula blocked us. It might not work.")
    # token = api.auth_token
    products = {}
    # search_result = search_products(api, query)
    # products.update(get_products(api, search_result))
    with open("C:\\pickle.pkl", "rb") as pkl:
        import pickle
        products = pickle.load(pkl)
    # products.update(run_query(query_list, token, False, api=api))
    wb = make_xlsx_workbook(products)
    write_xlsx(wb, "C:\\query.xlsx")
    input("Complete. Press Enter to exit.")


def search_products(api, query_string):
    """
    :type query_string: str
    :type api: `unfi_api.api.api.UnfiAPI`
    """
    query_chunks = make_query_list(query_string)
    results = []
    if len(query_chunks) < 1:
        return False
    for chunk in query_chunks:
        query = " ".join(str(x) for x in chunk)
        result = api.brands.get_products_by_full_text(query, limit=5000)
        if not result['error']:
            top_products = result['data']['TopProducts']
            results.extend(top_products)

    return index_results(results)


def index_results(results):
    products = {}
    for result in results:
        upc = int(stripcheckdigit(result['UPC']))
        product = products.setdefault(upc, {})
        product.update(result)

    return products


def get_products(api, results):
    """

    :type api: `unfi_api.api.api.UnfiAPI`
    """
    products = {}

    with ThreadPoolExecutor(10) as excecutor:
        futures = []

        with tqdm.tqdm(results.items()) as pb:
            def _get_product(d):
                p = api.get_product(d[1]['ProductCode'], d[1]["ProductIntID"])
                time.sleep(random.randint(1, 5))
                products[d[0]] = p
                pb.update()
                return p

            for item in results.items():
                futures.append(excecutor.submit(_get_product, item))
            results = []
            for future in as_completed(futures):
                results.append(future.result())

    return products


def write_csv(ws, path):
    with open(path, 'w', newline='') as csvfile:
        csvw = csv.writer(csvfile, 'excel')
        for row in ws:
            csvw.writerow(row)
    return True


def write_xlsx(wb, path):
    """
    :type path: str
    :type wb: Workbook
    """
    wb.save(path)


def make_query_list(query, chunk_size=120):
    # split query by white space and remove non text
    import re
    query_list = re.split(r'\s', query)
    query_list = [re.sub(r'\W+', "", x) for x in query_list]
    try:
        query_list.remove("")
    except ValueError:
        pass
    return list(divide_chunks(strings_to_numbers(query_list), chunk_size))


def make_worksheet(products):
    header = sorted(products.pop('fields'))
    rows = [header]
    for upc, product in products.items():
        row = []
        for col in header:
            p = product.get(col)
            row.append(p)
        rows.append(row)
    return rows


def make_xlsx_workbook(products):
    wb = Workbook()
    ws = wb.active
    header = sorted(products.pop('fields'))
    ws.append(header)
    for upc, product in products.items():
        row = []
        for col in header:
            p = product.get(col)
            row.append(p)
        ws.append(row)
    return wb


def product_to_row(product):
    pass


if __name__ == "__main__":
    main()
