import os
import sys
import re
import tkinter as tk
from pathlib import Path
from tkinter import messagebox as mb
from tkinter import simpledialog
from typing import Dict

from openpyxl import Workbook

from unfi_api import UnfiAPI, UnfiApiClient
from unfi_api.exceptions import exception_retry_prompt
from unfi_api.product import UNFIProduct, UNFIProducts
from unfi_api.search.result import Result, Results
from unfi_api.settings import IMAGE_OUTPUT_PATH, PRODUCT_QUERY_OUTPUT_PATH
from unfi_api.unfi_web_queries import run_query, make_query_list
from unfi_api.utils.collections import divide_chunks

# def uncaught_exception_handler(etype, value, tb):
#     # print(etype, value, tb)
#     traceback.print_exc()
#     input("PROCESS FAILED PRESS ENTER TO QUIT")


# sys.excepthook = uncaught_exception_handler
# output_path = r"F:\pos\unfi\query.xlsx"
output_path = PRODUCT_QUERY_OUTPUT_PATH
image_path = IMAGE_OUTPUT_PATH
description_regex = re.compile(r"(?: at least.*| 100% Organic)", re.IGNORECASE)
FETCH_IMAGES = True


def main():
    user = os.environ.get("UNFI_USER")
    password = os.environ.get("UNFI_PASSWORD")
    tkroot = tk.Tk()
    tkroot.withdraw()
    query = ask_query()

    if query:
        api = init_api(user, password)
        client = UnfiApiClient(api)
        search = True
        products = UNFIProducts()
        fields = set()
        while True:
            results: Results = search_products(query, client)
            if results:
                products.update(download_products(results, client))
                if FETCH_IMAGES:
                    download_product_images(client, products, image_path)
                if len(products) > 0:
                    if mb.askyesno(
                        "Save Workbook", "Would you like to save the workbook?"
                    ):
                        wb = create_excel_workbook(products)
                        save_wb(wb, output_path)

                    if mb.askyesno("Run again?", "Run another search?"):
                        continue
                    else:
                        break
            else:
                if mb.askyesno(
                    "No Results Found", "No results found. Do another search?"
                ):
                    query = ask_query()

    mb.showinfo("Quit", "Process Ended.")


def init_api(user, password):
    print("Connecting to UNFI API")
    api = UnfiAPI(user, password, incapsula_retry=False, incapsula=False)
    if api.logged_in:
        print("Connected!")
        return api
    else:
        if mb.askretrycancel(
            "Login Error",
            f"Could not login to UNFI API with username: {user}.",
        ):
            init_api(user, password)
        else:
            mb.showerror("Login Error", "Could not login to UNFI API. Exiting now.")
            sys.exit(1)


def do_search(query: str, client: UnfiApiClient) -> Results:
    def __search_chunk(chunk: list):
        print(f"Searching for {len(chunk)} terms...")
        result = client.search(" ".join(chunk))
        print(f"Search Complete! Found {result.total_hits} items matching the query")
        return result

    from concurrent.futures import ThreadPoolExecutor, as_completed

    query_list = make_query_list(query)
    chunks = list(divide_chunks(query_list, 120))
    results = []
    with ThreadPoolExecutor(max_workers=len(chunks)) as executor:
        futures = [executor.submit(__search_chunk, chunk) for chunk in chunks]
        for future in as_completed(futures):
            results.append(future.result())
    return Results(results=results)


def search_products(query: str, client: UnfiApiClient) -> Results:
    if not query:
        if mb.askyesno("Empty Search", "Your search was empty. Retry?"):
            query = ask_query()
            search_products(query, client)
        else:
            return None

    results = do_search(query, client)
    if results.total_hits < 1:
        return None
    else:
        return client.search(query)


def download_products(results: Results, client: UnfiApiClient) -> UNFIProducts:
    from tqdm import tqdm

    with tqdm(total=results.total_hits, unit=" products") as pbar:
        pbar.smoothing = 0.1
        products: Dict[str, UNFIProduct] = results.download_products(
            client, lambda x: pbar.update(), threaded=True, thread_count=4
        )

    return products


def download_product_images(
    client: UnfiApiClient, products: UNFIProducts, image_directory: str
):
    for product in products:
        if product.image_available:
            filename = os.path.join(image_directory, f"{product.upc}.jpg")
            if not os.path.exists(filename):
                with open(filename, "wb") as img_file:
                    image_data = product.get_image(client)
                    if image_data:
                        img_file.write(image_data)


def save_wb(wb, output_file=output_path) -> None:
    while True:
        try:
            wb.save(output_path)
        except PermissionError:
            if mb.askyesno(
                f"Permission Error",
                "Permission Error, could not write to:\n {product_query_output_path}. Retry?",
            ):
                continue
            else:
                mb.showerror(
                    "Save Error",
                    f"Could not save workbook to {output_path}. Ending Program",
                )
                sys.exit(1)
        else:
            return


def ask_query():
    query = simpledialog.askstring("Search For Products", "Search For: ")

    return query


def create_excel_workbook(products: UNFIProducts):
    from openpyxl import Workbook

    excel_dicts = products.to_excel()
    dict_keys: set = set()
    for d in excel_dicts.values():
        dict_keys.update(list(d.keys()))
    header = list(dict_keys)
    rows = [header]
    for product_code, excel_dict in excel_dicts.items():
        row = [excel_dict.get(key) for key in header]
        rows.append(row)
    wb = Workbook()
    ws = wb.active
    for row in rows:
        ws.append(row)
    return wb


if __name__ == "__main__":
    main()
