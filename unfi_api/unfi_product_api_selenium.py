from __future__ import print_function

import csv
import sys

from openpyxl import Workbook

from unfi_api.unfi_web_queries import run_query, make_query_list
from unfi_api import UnfiAPI

try:
    from past.builtins import raw_input
except ImportError:
    pass

try:
    import tkinter as tk
    from tkinter import ttk
    from tkinter import messagebox as mb
    from tkinter import simpledialog

except ImportError:
    import Tkinter as tk
    from Tkinter import ttk
    import tkMessageBox as mb
    import tkSimpledialog as simpledialog

LARGE_FONT = ("Arial", 16, "bold")
SUBTITLE_FONT = ("Arial", 12, 'bold')
CONTENT_FONT = ("Arial", 10)
LARGE_LBL_ARGS = {'padx': 10, 'pady': 10}

TEST_QUERY = """
042563-60307
052603-06756
850348-00328
850348-00328
850348-00328
853715-00358
853982-00458
853982-00462
858195-00327
858195-00329
858234-00665
858234-00665
862284-00001
862284-00001
"""

TOKEN = None

default_token = None


def uncaught_exception_handler(type, value, tb):
    print(type, value, tb)
    input("PROCESS FAILED PRESS ENTER TO QUIT")


sys.excepthook = uncaught_exception_handler


def main():
    tkroot = tk.Tk()
    tkroot.withdraw()
    query = simpledialog.askstring("Search For Products", "Search For: ")
    query_list = make_query_list(query)
    print("Loading UNFI Driver")
    api = UnfiAPI("CapellaAPI", "CapellaAPI2489")
    token = api.auth_token

    products = {}
    search = True

    # TOKEN = simpledialog.askstring("Enter your Ridgefield token", "Enter your Ridgefield token: ")
    if not token:
        token = default_token

    products.update(run_query(query_list, token, False))
    wb = make_xlsx_workbook(products)
    write_xlsx(wb, "C:\\query.xlsx")
    print("Setting account to Ridgefield")
    input("Complete. Press Enter to exit.")


def write_csv(ws, path):
    with open(path, 'w', newline='') as csvfile:
        csvw = csv.writer(csvfile, 'excel')
        for row in ws:
            csvw.writerow(row)
    return True


def write_xlsx(wb, path):
    """
    :type wb: Workbook
    """
    wb.save(path)


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


if __name__ == "__main__":
    main()
