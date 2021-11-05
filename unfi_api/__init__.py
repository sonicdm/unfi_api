import os
from typing import Dict
from retry import retry
import tqdm

from unfi_api.settings import product_query_output_path
from unfi_api.api.api import UnfiAPI
from unfi_api.client import UnfiApiClient
from unfi_api.product import UNFIProduct
from unfi_api.utils.output import exception_retry_prompt

from unfi_api.search.result import ProductResult, Result, Results


def main():
    print("Connecting to api...")
    api = UnfiAPI(os.environ["UNFI_USER"], os.environ["UNFI_PASSWORD"], incapsula=False)
    print("Connected!")
    print("Creating Client...")
    api_client = UnfiApiClient(api)
    print("Client Created!")
    print("Enter Query: ")

    lines = []
    line = ""
    while True:
        line = input()  # get input
        if line:
            lines.append(line)
        else:
            break
    query = "\n".join(lines)
    if not query:
        query = "santa cruz"
    print("Searching for products...")
    result: Result = api_client.search(query)
    print(f"Found {result.total_hits} results.")
    excel_dicts: Dict[str, dict] = {}
    print(f"Downloading {result.total_hits} products...")
    with tqdm.tqdm(total=result.total_hits, unit=" products") as pbar:
        pbar.smoothing = 0.1
        products: Dict[str, UNFIProduct] = result.download_products(
            api_client, lambda x: pbar_callback(x, pbar), threaded=True, thread_count=4
        )
        # pbar.display(f"Downloaded {len(products)} products.")

    for product_code, product in products.items():
        products[product.product_code] = product
        excel_dict = product.to_excel()
        excel_dicts[product_code] = excel_dict
    wb = create_excel_workbook(excel_dicts)
    save_wb(wb)


@exception_retry_prompt(
    exception=PermissionError,
    prompt="Try again?",
    max_tries=3,
    message="Failed to write excel file (file may be in use).",
)
def save_wb(wb, output_file=product_query_output_path):
    wb.save(product_query_output_path)


def pbar_callback(product: UNFIProduct, pbar: tqdm.tqdm):
    pbar.set_description(product.product_code)
    pbar.update()


def create_excel_workbook(excel_dicts: Dict[str, dict]):
    from openpyxl import Workbook

    output_file = "F:\\pos\\unfi\\query_new.xlsx"
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
