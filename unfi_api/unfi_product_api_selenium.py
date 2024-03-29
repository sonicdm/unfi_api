import os
import re
import tkinter as tk
from tkinter import messagebox as mb
from tkinter import simpledialog

from openpyxl import Workbook

from unfi_api import UnfiAPI, UnfiApiClient
from unfi_api.settings import IMAGE_OUTPUT_PATH
from unfi_api.unfi_web_queries import run_query, make_query_list

# def uncaught_exception_handler(etype, value, tb):
#     # print(etype, value, tb)
#     traceback.print_exc()
#     input("PROCESS FAILED PRESS ENTER TO QUIT")


# sys.excepthook = uncaught_exception_handler
output_path = r"F:\pos\unfi\query.xlsx"
description_regex = re.compile(r'(?: at least.*| 100% Organic)', re.IGNORECASE)
fetch_images = True


def main():
    tkroot = tk.Tk()
    tkroot.withdraw()
    query = ask_query()
    if query:
        USER = os.getenv("UNFI_USER")
        PASSWORD = os.getenv("UNFI_PASSWORD")
        print("Loading UNFI Driver")
        api = UnfiAPI(USER,PASSWORD, incapsula_retry=True, incapsula=False)
        api_client = UnfiApiClient(api)
        search = True
        products = {}
        fields = set()
        # result = do_query(query, api)
        # products.update(result)
        # search = mb.askyesno("Run again?", "Run another search?")
        while search:
            if not query:
                query = ask_query()
            if query:
                result = do_query(query, api_client)
                fields.update(result.get('fields'))
                products.update(result.get('items'))
                query = None
                if fetch_images:
                    for upc, product in products.items():
                        download_product_image(api, product, IMAGE_OUTPUT_PATH)
                if mb.askyesno("Save Workbook", "Would you like to save the workbook?"):
                    save_workbook(products, fields)
                search = mb.askyesno("Run again?", "Run another search?")
            else:
                if not mb.askyesno("Empty Search", "Your search was empty. Retry?"):
                    search = False
                    save_workbook(products, fields)

    else:
        if mb.askyesno("Empty Query", "Re-run search?"):
            main()

    mb.showinfo("Quit", "Process Ended.")


def download_product_image(api, product, output_path):
    if product['imageavailable']:
        intid = product['productintid']
        upc = product['upc'][:-1]
        image_path = os.path.join(output_path, upc + ".jpg")
        if not os.path.exists(image_path):
            with open(os.path.join(output_path, upc + ".jpg"), "wb") as img_file:
                product_name = " ".join([product['brandname'], product['productname']])
                print("Fetching Image for {}".format(product_name))
                image_result = api.endpoints['products'].get_product_image(intid)
                if not image_result.get('error'):
                    image_data = image_result.get('data')
                    if image_data:
                        img_file.write(image_data)


def save_workbook(products, fields):
    print("Creating Workbook for {} products..".format(len(products)))
    wb = make_xlsx_workbook(products, fields)
    print("Saving workbook to: ", output_path)
    write_xlsx(wb, output_path)


def ask_query():
    query = simpledialog.askstring("Search For Products", "Search For: ")
    return query


def do_query(query, client: UnfiApiClient):
    query_list = make_query_list(query)
    token = client.auth_token
    # products = {}
    result = run_query(client, query_list, token, api=client.api)
    # if result:
    #     products.update(result)
    return result


def write_xlsx(wb, filepath):
    """
    :param filepath:
    :type wb: Workbook
    """
    wb.save(filepath)


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


def make_xlsx_workbook(products, fields):
    wb = Workbook()
    ws = wb.active
    # header = products.get('fields')
    ws.append(list(fields))
    for upc, product in products.items():
        if upc == "fields":
            continue
        row = []
        for col in fields:
            val = product.get(col)
            if col == "productname":
                val = description_regex.sub("", val)
                val = val.replace(",", " ").replace("  ", " ").replace("  ", " ").replace("'S", "'s").replace("`", "'")
            if col == "organiccode":
                if val in ["OG2", "OG1"]:
                    val = "Y"
                else:
                    val = ""
            if col == "brandname":
                val = val.replace(",", " ").replace("  ", " ").replace("  ", " ").replace("'S", "'s").replace("`", "'")

            row.append(val)
        ws.append(row)
    return wb


if __name__ == "__main__":
    main()
